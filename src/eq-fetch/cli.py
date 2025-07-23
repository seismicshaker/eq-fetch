"""Command Line Interface Module."""

import click
from downloader import download_catalog
from filter import filter_catalog
from process import process_data


@click.group()
def cli():
    pass


@cli.command()
@click.option("--source", required=True, help="Source URL for catalog")
@click.option("--output", required=True, help="Output filename")
def download(source, output):
    """Download earthquake catalog from a source."""
    download_catalog(source, output)


@cli.command()
@click.option("--input", required=True, help="Input catalog file")
@click.option("--min-magnitude", type=float, help="Minimum earthquake magnitude")
def filter(input, min_magnitude):
    """Filter downloaded catalog by magnitude."""
    filter_catalog(input, min_magnitude)


@cli.command()
@click.option("--input", required=True, help="Input catalog file")
def process(input):
    """Process catalog data (possibly using C/Cython)."""
    process_data(input)


if __name__ == "__main__":
    cli()
