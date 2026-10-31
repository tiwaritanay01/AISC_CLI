"""Main Command-Line Interface application for LabX Remote."""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple
import typer
from rich.prompt import Confirm

from labx import __version__
from labx.config import get_remote_url, DEFAULT_REMOTE_URL
from labx.client import LabXRemoteClient, LabXNetworkError
from labx.cache import LabXCache
from labx.models import Catalog, ExperimentManifest
from labx.search import ExperimentSearchEngine
from labx.downloader import ExperimentDownloader
from labx.runners.registry import default_registry
from labx.ui import (
    console,
    error_console,
    print_banner,
    print_catalog_table,
    print_search_results,
    prompt_select_ambiguous,
    print_experiment_info,
    print_success,
    print_warning,
    print_error
)

app = typer.Typer(
    name="labx",
    help="LabX Remote: Production-Ready Experiment Distribution and Execution System",
    no_args_is_help=False,
    add_completion=False
)


def get_catalog_and_client(remote_url: Optional[str] = None) -> tuple[LabXRemoteClient, Optional[Catalog], bool]:
    """Retrieve catalog using client with automatic fallback to local disk cache."""
    client = LabXRemoteClient(base_url=remote_url)
    cache = LabXCache()
    catalog: Optional[Catalog] = None
    offline = False

    try:
        catalog = client.fetch_catalog()
        # Save to disk cache for offline use
        import dataclasses
        cache.save_catalog(dataclasses.asdict(catalog))
    except Exception:
        # Fallback to local cache
        catalog = cache.load_catalog()
        offline = True

    return client, catalog, offline


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Display LabX CLI version."),
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """LabX root command callback displaying branding and status if no command specified."""
    if version:
        console.print(f"LabX Remote version: [bold green]{__version__}[/bold green]")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        client = LabXRemoteClient(base_url=remote_url)
        connected, remote_ver, _ = client.check_connection()
        cache = LabXCache()
        cached_cat = cache.load_catalog()
        count = len(cached_cat.experiments) if cached_cat else 0

        print_banner(connected=connected, version_info=remote_ver, count=count)

        console.print("[bold cyan]Available Commands:[/bold cyan]")
        console.print("  [bold green]labx list[/bold green]                         List all experiments in catalogue")
        console.print("  [bold green]labx search <query>[/bold green]                Fuzzy search experiments by name/concept")
        console.print("  [bold green]labx info <id|title>[/bold green]               Inspect experiment aim, theory & algorithm")
        console.print("  [bold green]labx download <id|title|all>[/bold green]       Download single experiment or complete collection")
        console.print("  [bold green]labx run <id|title>[/bold green]                Compile & execute an experiment")
        console.print("  [bold green]labx update[/bold green]                       Refresh local metadata cache")
        console.print("  [bold green]labx remove <id|title>[/bold green]              Remove downloaded experiment folder\n")
        console.print("[dim]Run [bold]labx <command> --help[/bold] for command options.[/dim]\n")


@app.command("list")
def list_experiments(
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Fetch remote catalogue and display all available experiments in a table."""
    client, catalog, offline = get_catalog_and_client(remote_url)
    if not catalog or not catalog.experiments:
        print_error("Unable to load catalogue from remote host or local cache.")
        raise typer.Exit(code=1)

    print_catalog_table(catalog, offline=offline)


@app.command("search")
def search_experiments(
    query: str = typer.Argument(..., help="Search query (ID, title, topic, or keyword)"),
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Perform fuzzy search across experiment titles, topics, and aliases."""
    client, catalog, _ = get_catalog_and_client(remote_url)
    if not catalog:
        print_error("Catalogue unavailable. Connect to internet or run 'labx update' first.")
        raise typer.Exit(code=1)

    engine = ExperimentSearchEngine(catalog)
    results = engine.search(query)
    print_search_results(query, results)


@app.command("info")
def info_experiment(
    query: str = typer.Argument(..., help="Experiment ID or name"),
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Display aim, description, theory, algorithm, and file details for an experiment."""
    client, catalog, offline = get_catalog_and_client(remote_url)
    if not catalog:
        print_error("Catalogue unavailable.")
        raise typer.Exit(code=1)

    engine = ExperimentSearchEngine(catalog)
    item, candidates, is_ambiguous = engine.resolve(query)

    if is_ambiguous:
        item = prompt_select_ambiguous(candidates)

    if not item:
        print_error(f"No experiment found matching '{query}'.")
        raise typer.Exit(code=1)

    # Fetch manifest
    cache = LabXCache()
    manifest = cache.load_manifest(item.id)
    if not manifest and not offline:
        try:
            manifest = client.fetch_manifest(item.manifest_url)
            import dataclasses
            cache.save_manifest(item.id, dataclasses.asdict(manifest))
        except Exception as exc:
            print_error(f"Failed to fetch manifest from remote: {exc}")

    if not manifest:
        print_error(f"Could not load manifest for experiment {item.id}.")
        raise typer.Exit(code=1)

    print_experiment_info(manifest)


@app.command("download")
def download_experiment(
    target: str = typer.Argument(..., help="Experiment ID, title, or 'all'"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Target working directory (default: current directory)"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite without confirmation"),
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Download an individual experiment or the complete ZIP collection into working directory."""
    dest_dir = Path(path).resolve() if path else Path.cwd().resolve()
    client, catalog, offline = get_catalog_and_client(remote_url)

    if not catalog:
        print_error("Cannot download: remote catalogue is unreachable and no cache exists.")
        raise typer.Exit(code=1)

    downloader = ExperimentDownloader(client)

    # Check for "all"
    if target.strip().lower() == "all":
        success = downloader.download_all_zip(catalog.zip_url, dest_dir, force=force)
        if not success:
            raise typer.Exit(code=1)
        return

    # Individual download
    engine = ExperimentSearchEngine(catalog)
    item, candidates, is_ambiguous = engine.resolve(target)

    if is_ambiguous:
        item = prompt_select_ambiguous(candidates)

    if not item:
        print_error(f"No experiment found matching '{target}'. Use 'labx list' to browse.")
        raise typer.Exit(code=1)

    success = downloader.download_individual(item, dest_dir, force=force)
    if not success:
        raise typer.Exit(code=1)


def find_local_experiment_dir(query: str, base_dir: Path, catalog: Optional[Catalog]) -> Optional[Tuple[Path, ExperimentManifest]]:
    """Locate downloaded experiment folder in base_dir corresponding to query."""
    import json
    # 1. First resolve ID if possible
    exp_id = None
    if catalog:
        engine = ExperimentSearchEngine(catalog)
        item, _, _ = engine.resolve(query)
        if item:
            exp_id = item.id

    if exp_id is None:
        try:
            exp_id = int(query.strip())
        except ValueError:
            pass

    # Search folders in base_dir and optional labx_experiments subfolder
    search_roots = [base_dir]
    nested = base_dir / "labx_experiments"
    if nested.is_dir():
        search_roots.append(nested)

    for root in search_roots:
        for item in root.iterdir():
            if item.is_dir():
                # Check manifest.json inside directory
                mf_path = item / "manifest.json"
                if mf_path.exists():
                    try:
                        with open(mf_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        manifest = ExperimentManifest.from_dict(data)
                        if exp_id is not None and manifest.id == exp_id:
                            return item, manifest
                        if query.lower() in item.name.lower() or query.lower() in manifest.title.lower():
                            return item, manifest
                    except Exception:
                        continue
                else:
                    # Check directory name pattern (e.g. Experiment03_...)
                    if exp_id is not None and (item.name.startswith(f"Experiment{exp_id:02d}") or item.name.startswith(f"Experiment{exp_id}")):
                        # Try to reconstruct manifest from cache
                        cache = LabXCache()
                        mf = cache.load_manifest(exp_id)
                        if mf:
                            return item, mf

    return None


@app.command("run")
def run_experiment(
    query: str = typer.Argument(..., help="Experiment ID or title to execute"),
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Component to run (for multi-process experiments, e.g. 'server' or 'client')"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Base directory where experiment was downloaded"),
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Compile and execute an experiment in the current working directory."""
    work_dir = Path(path).resolve() if path else Path.cwd().resolve()
    _, catalog, _ = get_catalog_and_client(remote_url)

    found = find_local_experiment_dir(query, work_dir, catalog)

    if not found:
        print_error(f"Experiment '{query}' not found in directory: {work_dir}")
        console.print("[yellow]Hint: You must download the experiment before running it:[/yellow]")
        console.print(f"  [bold cyan]labx download {query}[/bold cyan]\n")
        raise typer.Exit(code=1)

    exp_dir, manifest = found
    runner = default_registry.get_runner(manifest.run.kind) or default_registry.get_runner(manifest.language)

    if not runner:
        print_error(f"No execution runner registered for language/kind: '{manifest.run.kind}'")
        raise typer.Exit(code=1)

    # Check if experiment has components and user didn't specify one
    if manifest.run.components and not component:
        comp_keys = list(manifest.run.components.keys())
        console.print(f"[cyan]Notice: Experiment #{manifest.id:02d} has multiple components: {', '.join(comp_keys)}[/cyan]")
        console.print(f"[dim]Defaulting to entry component or '{comp_keys[0]}'. Use '--component <name>' to select.[/dim]")
        component = comp_keys[0]

    exit_code = runner.run(exp_dir, manifest.run, component_name=component)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command("update")
def update_metadata(
    remote_url: Optional[str] = typer.Option(None, "--url", help="Override remote catalogue base URL.")
):
    """Force refresh the local catalogue and experiment manifests from remote host."""
    client = LabXRemoteClient(base_url=remote_url)
    cache = LabXCache()

    console.print("[cyan]Fetching fresh catalogue from remote...[/cyan]")
    try:
        catalog = client.fetch_catalog()
        import dataclasses
        cache.save_catalog(dataclasses.asdict(catalog))
        print_success(f"Catalogue updated successfully ({len(catalog.experiments)} experiments).")

        # Refresh individual manifests
        console.print("[cyan]Updating manifests...[/cyan]")
        updated_count = 0
        for exp in catalog.experiments:
            try:
                mf = client.fetch_manifest(exp.manifest_url)
                cache.save_manifest(exp.id, dataclasses.asdict(mf))
                updated_count += 1
            except Exception:
                pass

        print_success(f"Updated {updated_count} experiment manifests in local cache.")
    except Exception as exc:
        print_error(f"Failed to update metadata: {exc}")
        raise typer.Exit(code=1)


@app.command("remove")
def remove_experiment(
    query: str = typer.Argument(..., help="Experiment ID or title to remove"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Directory containing the experiment"),
    force: bool = typer.Option(False, "--force", "-f", help="Bypass confirmation prompt")
):
    """Remove a downloaded experiment folder from the working directory."""
    work_dir = Path(path).resolve() if path else Path.cwd().resolve()
    _, catalog, _ = get_catalog_and_client()
    found = find_local_experiment_dir(query, work_dir, catalog)

    if not found:
        print_error(f"Experiment folder for '{query}' not found in {work_dir}.")
        raise typer.Exit(code=1)

    exp_dir, manifest = found

    # Safety check: ensure directory is indeed an experiment folder
    if not (exp_dir / "manifest.json").exists() and not exp_dir.name.startswith("Experiment"):
        print_error(f"Refusing to delete directory without LabX manifest confirmation: {exp_dir}")
        raise typer.Exit(code=1)

    if not force:
        confirm = Confirm.ask(
            f"Are you sure you want to remove '{exp_dir.name}' (Experiment #{manifest.id:02d}: {manifest.title})?",
            default=False
        )
        if not confirm:
            console.print("[yellow]Removal cancelled.[/yellow]")
            return

    import shutil
    shutil.rmtree(exp_dir)
    print_success(f"Removed {exp_dir.name} successfully.")


if __name__ == "__main__":
    app()
