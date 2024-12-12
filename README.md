# Earthquake Catalog Downloader

## About the Project

This project is in early stage development. Any interested users should be able to clone package and use the ISC Event Bibliography search and save results as a CSV or JSON file. The ISC Bulletin saerch currently being worked on with the implimentation of GlobalCMT search next.

## Installation

_Below is an installation procedure for running **earthquakeCatalogDownloader**._

1. Clone this repo into a desired directory

```sh
git clone git@github.com:seismicshaker/earthquakeCatalogDownloader.git
```

# TODO: Setup conda env
2. Install Python dependencies

_Existing conda environment_
```sh
conda install --yes --file requirements.txt
```

_New conda environment_
```sh
conda create --name catalogDL --file requirements.txt
```

_Global python environment_
```sh
pip install -r requirements
```

## How it works

This project is driven by the `eq_downloader.py` script. That means that you'll run `python3 eq_downloader.py ... ... ...` at the command line to invoke the program that will call your code.

At a command line, you can run `python3 eq_downloader.py --help` for a list of search subcommands.

```python
usage: python eq_downloader.py {bibli,hypo,gcmt,interactive} ...

Define search criterion.

positional arguments:
  {hypo,gcmt,bibli,interactive}

optional arguments:
  -h, --help            show this help message and exit
```

The four subcommands (`bibli`, `hypo`, `gcmt`, and `interactive`) are explained futher below.

### `bibli`

ISC event Bibliography search

### `hypo` [in development]

ISC Bulletin search.

### `gcmt` [to be added in future patch]

GlobalCMT search.

### `interactive` [to be added in future patch]

Interactive search to modify search and filter criterion.
