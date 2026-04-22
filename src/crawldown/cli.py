import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from crawldown.crawler import _crawl
from crawldown.models import CrawlConfig, PageResult

app = typer.Typer(help="Crawl any website and save every page as organized Markdown files.")
console = Console()


def _version_callback(value: bool):
    if value:
        from importlib.metadata import version

        typer.echo(f"crawldown {version('crawldown')}")
        raise typer.Exit()


@app.command()
def main(
    url: str = typer.Argument(..., help="The URL to start crawling from"),
    output: Path = typer.Option(
        Path("crawldown-output"), "--output", "-o", help="Output directory"
    ),
    depth: int | None = typer.Option(
        None, "--depth", "-d", help="Max crawl depth (default: unlimited)"
    ),
    delay: float = typer.Option(0.0, "--delay", help="Seconds to wait between requests"),
    no_robots: bool = typer.Option(False, "--no-robots", help="Ignore robots.txt"),
    include: list[str] = typer.Option(
        [], "--include", help="URL path glob to include (repeatable, e.g. /docs/*)"
    ),
    exclude: list[str] = typer.Option(
        [], "--exclude", help="URL path glob to exclude (repeatable, e.g. /api/*)"
    ),
    version: bool | None = typer.Option(
        None, "--version", callback=_version_callback, is_eager=True
    ),
):
    config = CrawlConfig(
        url=url,
        output_dir=output,
        max_depth=depth,
        delay=delay,
        respect_robots=not no_robots,
        include=list(include),
        exclude=list(exclude),
    )

    done = 0
    errors = 0

    def on_page(page: PageResult):
        nonlocal done, errors
        done += 1
        if page.error:
            errors += 1
            console.print(f"  [red]FAIL[/red] {page.url}  ({page.error})")
        else:
            console.print(f"  [green]OK[/green]   {page.url}  -> {page.output_path}")

    console.print(f"\n[bold]crawldown[/bold] {url}\n")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ):
            asyncio.run(_crawl(config, on_page=on_page))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted — partial results saved to output directory.[/yellow]")

    console.print(
        f"\n[bold]Done.[/bold] {done} pages crawled, {errors} errors. Output: {output}\n"
    )
