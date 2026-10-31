"""Downloader module for individual experiment manifests/files and full ZIP archives."""

import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional, Callable
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.prompt import Confirm

from labx.client import LabXRemoteClient, LabXNetworkError
from labx.models import ExperimentManifest, CatalogItem
from labx.ui import console, print_error, print_success, print_warning


def is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """Ensure target path does not escape base directory (Path traversal protection)."""
    try:
        resolved_base = base_dir.resolve()
        resolved_target = target_path.resolve()
        return resolved_base in resolved_target.parents or resolved_base == resolved_target
    except Exception:
        return False


def generate_experiment_readme(manifest: ExperimentManifest) -> str:
    """Generate markdown documentation file for the experiment."""
    algo_md = "\n".join([f"{i}. {step}" for i, step in enumerate(manifest.algorithm, 1)])
    files_md = "\n".join([f"- `{f.path}` ({f.role})" for f in manifest.files])

    return f"""# Experiment {manifest.id:02d}: {manifest.title}

**Language:** {manifest.language.capitalize()}  
**Version:** {manifest.version}

---

## Aim
{manifest.aim}

---

## Description
{manifest.description}

---

## Theory
{manifest.theory}

---

## Algorithm
{algo_md}

---

## Experiment Files
{files_md}

---

## Execution
Run this experiment using the LabX CLI:
```bash
labx run {manifest.id}
```
Or directly using the appropriate language toolchain:
- Entry point: `{manifest.run.entry}`
"""


class ExperimentDownloader:
    """Handles downloading and local file extraction."""

    def __init__(self, client: LabXRemoteClient):
        self.client = client

    def download_individual(
        self,
        item: CatalogItem,
        destination_dir: Path,
        force: bool = False
    ) -> bool:
        """Download a single experiment's manifest, source files, and theory."""
        dest_dir = destination_dir.resolve()
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Standard experiment directory naming: Experiment03_Java_Socket_Programming
        slug_clean = item.slug.replace("-", "_")
        exp_folder_name = f"Experiment{item.id:02d}_{slug_clean}"
        target_dir = dest_dir / exp_folder_name

        if target_dir.exists() and any(target_dir.iterdir()):
            if not force:
                console.print(f"[yellow]Directory already exists: {target_dir.name}[/yellow]")
                confirm = Confirm.ask("Do you want to overwrite existing experiment files?", default=False)
                if not confirm:
                    console.print("[yellow]Download skipped by user.[/yellow]")
                    return False

        target_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            # 1. Fetch manifest
            fetch_task = progress.add_task(f"Fetching metadata for Exp #{item.id:02d}...", total=100)
            try:
                manifest = self.client.fetch_manifest(item.manifest_url)
                progress.update(fetch_task, completed=100)
            except Exception as exc:
                print_error(f"Could not load manifest for experiment {item.id}: {exc}")
                return False

            # 2. Download each source file
            file_task = progress.add_task(f"Downloading source files...", total=len(manifest.files) + 2)
            completed_files = 0

            # Compute relative base path for remote files from manifest_url
            manifest_base = os.path.dirname(item.manifest_url.lstrip("/"))

            for f_info in manifest.files:
                local_file_path = target_dir / f_info.path
                if not is_safe_path(target_dir, local_file_path):
                    print_error(f"Insecure file path detected: {f_info.path}")
                    return False

                remote_file_url = f"{manifest_base}/{f_info.source}" if manifest_base else f_info.source
                try:
                    self.client.download_file(remote_file_url, local_file_path)
                    completed_files += 1
                    progress.update(file_task, completed=completed_files)
                except Exception as exc:
                    print_error(f"Failed to download {f_info.path}: {exc}")
                    return False

            # 3. Save local manifest.json
            import json
            local_manifest_path = target_dir / "manifest.json"
            try:
                with open(local_manifest_path, "w", encoding="utf-8") as mf:
                    json.dump(manifest.to_dict(), mf, indent=2)
                completed_files += 1
                progress.update(file_task, completed=completed_files)
            except Exception as exc:
                print_error(f"Failed to write manifest.json: {exc}")

            # 4. Save formatted README.md
            readme_path = target_dir / "README.md"
            try:
                readme_content = generate_experiment_readme(manifest)
                with open(readme_path, "w", encoding="utf-8") as rf:
                    rf.write(readme_content)
                completed_files += 1
                progress.update(file_task, completed=completed_files)
            except Exception as exc:
                print_warning(f"Failed to generate README.md: {exc}")

        print_success(f"Downloaded Experiment {item.id:02d} ({item.title}) into [bold cyan]{target_dir.name}/[/bold cyan]")
        return True

    def download_all_zip(
        self,
        zip_url: str,
        destination_dir: Path,
        force: bool = False
    ) -> bool:
        """Download and safely extract the complete experiments ZIP archive."""
        dest_dir = destination_dir.resolve()
        dest_dir.mkdir(parents=True, exist_ok=True)

        zip_temp_path = dest_dir / "labx_experiments_download.zip"

        console.print(f"[bold cyan]Connecting to download complete experiments archive...[/bold cyan]")

        try:
            with Progress(
                TextColumn("[bold cyan]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                dl_task = progress.add_task("Downloading archive...", total=None)

                def update_progress(downloaded: int, total: Optional[int]):
                    if total and progress.tasks[dl_task].total is None:
                        progress.update(dl_task, total=total)
                    progress.update(dl_task, completed=downloaded)

                self.client.download_zip(zip_url, zip_temp_path, update_progress)

            # Validate ZIP integrity
            if not zipfile.is_zipfile(zip_temp_path):
                print_error("Downloaded file is not a valid ZIP archive.")
                if zip_temp_path.exists():
                    zip_temp_path.unlink()
                return False

            console.print("[cyan]Verifying archive integrity...[/cyan]")
            with zipfile.ZipFile(zip_temp_path, "r") as zf:
                corrupt_file = zf.testzip()
                if corrupt_file:
                    print_error(f"Archive corrupt at file: {corrupt_file}")
                    if zip_temp_path.exists():
                        zip_temp_path.unlink()
                    return False

                # Extract with path traversal protection and duplicate tracking
                extracted_count = 0
                skipped_count = 0

                console.print(f"[cyan]Extracting experiments into [bold]{dest_dir}[/bold]...[/cyan]")
                for member in zf.infolist():
                    # Strip top-level labx_experiments/ prefix to avoid nested directories
                    rel_name = member.filename
                    if rel_name.startswith("labx_experiments/"):
                        rel_name = rel_name[len("labx_experiments/"):]
                    elif rel_name.startswith("labx_experiments\\"):
                        rel_name = rel_name[len("labx_experiments\\"):]

                    if not rel_name or rel_name.strip() in ("", "/", "\\"):
                        continue

                    # Check for path traversal (zip-slip)
                    target_member_path = dest_dir / rel_name
                    if not is_safe_path(dest_dir, target_member_path):
                        print_warning(f"Skipping dangerous path in archive: {member.filename}")
                        continue

                    if member.is_dir() or member.filename.endswith("/"):
                        target_member_path.mkdir(parents=True, exist_ok=True)
                        continue

                    if target_member_path.exists() and not force:
                        skipped_count += 1
                        continue

                    target_member_path.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as src, open(target_member_path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    extracted_count += 1

            print_success(f"Extracted {extracted_count} files successfully into {dest_dir.name}/.")
            if skipped_count > 0:
                print_warning(f"Skipped {skipped_count} existing files (use --force to overwrite).")

            return True

        except Exception as exc:
            print_error(f"Bulk download failed: {exc}")
            return False
        finally:
            if zip_temp_path.exists():
                try:
                    zip_temp_path.unlink()
                except Exception:
                    pass
