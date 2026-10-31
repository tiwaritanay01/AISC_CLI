"""Rich-based UI presentation, tables, banners, and progress indicators."""

from typing import List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm, Prompt

from labx import __version__
from labx.models import Catalog, CatalogItem, ExperimentManifest
from labx.search import SearchResult

console = Console()
error_console = Console(stderr=True)


def print_banner(connected: bool = True, version_info: Optional[str] = None, count: int = 0):
    """Display the LabX branding header and connection status."""
    banner_text = Text()
    banner_text.append("LABX REMOTE ", style="bold cyan")
    banner_text.append(f"v{__version__}\n", style="bold green")
    banner_text.append("Terminal-first experiment distribution & execution utility\n", style="dim italic")

    if connected:
        status_line = f"[+] Connected to remote catalogue"
        if version_info:
            status_line += f" (Catalog v{version_info})"
        if count > 0:
            status_line += f" • {count} experiments available"
        banner_text.append(status_line, style="green")
    else:
        banner_text.append("[-] Remote unreachable (Operating in offline / cached mode)", style="yellow")

    console.print(Panel(banner_text, border_style="cyan", padding=(0, 2)))


def print_catalog_table(catalog: Catalog, offline: bool = False):
    """Render a clean Rich table listing available experiments."""
    table = Table(
        title=f"LabX Experiment Catalogue{' [Offline Cache]' if offline else ''}",
        title_style="bold magenta",
        header_style="bold cyan",
        border_style="dim",
        expand=True
    )

    table.add_column("ID", justify="center", style="bold yellow", width=6)
    table.add_column("Experiment", style="bold white", min_width=25)
    table.add_column("Language", justify="center", style="bold green", width=14)
    table.add_column("Description", style="white")

    for exp in catalog.experiments:
        table.add_row(
            f"{exp.id:02d}",
            exp.title,
            exp.language.capitalize(),
            exp.description
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]Use [bold cyan]labx download <id>[/bold cyan] or [bold cyan]labx info <id>[/bold cyan] to inspect.[/dim]\n")


def print_search_results(query: str, results: List[SearchResult]):
    """Display ranked search results."""
    if not results:
        console.print(f"\n[yellow]No experiments found matching '[bold white]{query}[/bold white]'.[/yellow]")
        console.print("[dim]Try running [bold cyan]labx list[/bold cyan] to browse all available experiments.[/dim]\n")
        return

    table = Table(
        title=f"Search Results for '{query}'",
        title_style="bold magenta",
        header_style="bold cyan",
        border_style="dim",
        expand=True
    )

    table.add_column("ID", justify="center", style="bold yellow", width=6)
    table.add_column("Experiment", style="bold white", min_width=24)
    table.add_column("Language", justify="center", style="bold green", width=14)
    table.add_column("Match Type", justify="center", style="dim", width=16)
    table.add_column("Score", justify="right", style="cyan", width=8)

    for res in results:
        table.add_row(
            f"{res.item.id:02d}",
            res.item.title,
            res.item.language.capitalize(),
            res.match_type.replace("_", " ").title(),
            f"{res.score:.1f}%"
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]Run [bold cyan]labx download {results[0].item.id}[/bold cyan] to download top match.[/dim]\n")


def prompt_select_ambiguous(candidates: List[SearchResult]) -> Optional[CatalogItem]:
    """When multiple matches are close, prompt the user to choose or cancel."""
    console.print("\n[yellow]Multiple experiments match your query:[/yellow]")
    for idx, cand in enumerate(candidates[:5], start=1):
        console.print(f"  [bold cyan]{idx}[/bold cyan]. [bold white]#{cand.item.id:02d} {cand.item.title}[/bold white] ({cand.item.language}) [dim][{cand.score:.1f}% match][/dim]")
    console.print("  [bold red]0[/bold red]. Cancel")

    choice = Prompt.ask("\nEnter selection number", choices=[str(i) for i in range(len(candidates[:5]) + 1)], default="1")
    if choice == "0":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return None
    return candidates[int(choice) - 1].item


def print_experiment_info(manifest: ExperimentManifest):
    """Display comprehensive information about an experiment."""
    console.print()
    header = Text()
    header.append(f"Experiment {manifest.id:02d}: ", style="bold yellow")
    header.append(manifest.title, style="bold white")
    header.append(f" [{manifest.language.upper()}]", style="bold green")

    content = Text()
    content.append(f"\nAim:\n", style="bold cyan")
    content.append(f"  {manifest.aim}\n")

    content.append(f"\nDescription:\n", style="bold cyan")
    content.append(f"  {manifest.description}\n")

    content.append(f"\nTheory:\n", style="bold cyan")
    theory_lines = manifest.theory.strip().split("\n")
    for t_line in theory_lines:
        content.append(f"  {t_line}\n")

    content.append(f"\nAlgorithm:\n", style="bold cyan")
    for idx, step in enumerate(manifest.algorithm, start=1):
        content.append(f"  {idx}. {step}\n")

    content.append(f"\nFiles Included:\n", style="bold cyan")
    for f in manifest.files:
        content.append(f"  • {f.path} ({f.role})\n", style="white")

    content.append(f"\nExecution Target:\n", style="bold cyan")
    content.append(f"  Entry: {manifest.run.entry}\n")
    if manifest.run.hardware:
        content.append(f"  Hardware: {manifest.run.hardware}\n")
    if manifest.run.components:
        content.append("  Components:\n")
        for cname, comp in manifest.run.components.items():
            content.append(f"    - {cname}: {comp.entry} {comp.description}\n")

    console.print(Panel(content, title=header, border_style="cyan", padding=(0, 2)))
    console.print(f"[dim]Run [bold cyan]labx download {manifest.id}[/bold cyan] to download this experiment.[/dim]\n")


def print_success(message: str):
    console.print(f"[bold green][OK][/bold green] {message}")


def print_warning(message: str):
    console.print(f"[bold yellow][!][/bold yellow] {message}")


def print_error(message: str):
    error_console.print(f"[bold red][ERROR][/bold red] {message}")
