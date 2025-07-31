"""Command Line Interface Module."""

import click
from eq_fetch.search import build_query, preview_results
from eq_fetch.downloader import CATALOG_SOURCES, download_catalog
from eq_fetch.filter import interactive_filter
from eq_fetch.export import export_results


@click.command()
def main():
    click.echo("Welcome to Earthquake Fetcher!")
    # 1. Catalog source selection
    sources: list[str] = list(CATALOG_SOURCES.keys())
    source: str = click.prompt("Choose catalog source", type=click.Choice(sources))
    input(source)
    # 2. Initial search criteria
    criteria = click.prompt("Enter search criteria (e.g., start_year=2020 min_mag=6.0)")
    input(criteria)
    params = build_query(source, criteria)
    # 3. Download + preview results
    results = download_catalog(source, params, dest_path=None)
    summary = preview_results(results)
    click.echo(summary)
    # 4. Interactive filter loop
    results = interactive_filter(results)
    # 5. Export
    if click.confirm("Export results?"):
        fmt = click.prompt("Choose format", type=click.Choice(["csv", "json", "xml"]))
        filename = click.prompt("Filename")
        export_results(results, fmt, filename)
        click.echo(f"Saved to {filename}")
    click.echo("Done!")


if __name__ == "__main__":
    main()
