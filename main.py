#!/usr/bin/env python3
"""Download search results from ISC

See `README.md` for a detailed discussion of this project.

This script can be invoked from the command line::

    $ python3 main.py {event,bibli,interactive} [args]

The `hypo` subcommand searches event catalog:

    $ python3 main.py hypo --date 1969-07-29
    $ python3 main.py hypo --start-date 2020-01-01 --end-date 2020-01-31
    $ python3 main.py hypo --date 1969-07-29 --outfile results.csv
    $ python3 main.py hypo --date 1969-07-29 --outfile results.json
    TODO: more search options

The `bibli` subcommand searches for event bibliography:

    $ python3 main.py bibli --date 1969-07-29
    $ python3 main.py bibli --start-date 2020-01-01 --end-date 2020-01-31
    $ python3 main.py bibli --date 1969-07-29 --outfile results.csv
    $ python3 main.py bibli --date 1969-07-29 --outfile results.json
    TODO: more search options


The `interactive` subcommand spawns an interactive command shell that can
repeatedly execute `hypo` or `bibli` commands without having to wait to save
the search results each time.

"""
import argparse
import cmd
import pathlib
import shlex
import sys
import time

from catalog import EventCatalog
from formatting import date_fromisoformat
from write import write_to_csv, write_to_json

# The current time, used with the kill-on-change feat of the interactive shell.
_START = time.time()


def make_parser():
    """Create an ArgumentParser for this script.

    :return: A tuple of the top-level, event, and bibliography parsers.
    """
    parser = argparse.ArgumentParser(
        description="Define search criterion for ISC Bulletin."
    )
    subparsers = parser.add_subparsers(dest="cmd")

    # Add the 'hypo' subcommand parser.
    hypo = subparsers.add_parser(
        "hypo",
        description="Event hypocenter search.",
    )
    hypo.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Additionally, print all known close approaches of this NEO.",
    )

    # Add the 'bibli' subcommand parser.
    bibli = subparsers.add_parser(
        "bibli",
        description="Event bibliography search.",
    )
    bibli.add_argument(
        "-d",
        "--date",
        type=date_fromisoformat,
        help="Event origin date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    bibli.add_argument(
        "-s",
        "--start_date",
        type=date_fromisoformat,
        help="Event origin start date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    bibli.add_argument(
        "-e",
        "--end_date",
        type=date_fromisoformat,
        help="Event origin end date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    bibli.add_argument(
        "--published_min_year",
        type=date_fromisoformat,
        help="search parameter, " "in YYYY (e.g. 2020).",
    )
    bibli.add_argument(
        "--published_max_year",
        type=date_fromisoformat,
        help="search parameter, " "in YYYY (e.g. 2021).",
    )
    bibli.add_argument(
        "--published_author",
        type=str,
        help="search parameter, " " (e.g. Warren).",
    )

    bibli.add_argument(
        "-o",
        "--outfile",
        type=pathlib.Path,
        help="File in which to save structured results. "
        "If omitted, results are printed to standard output.",
    )

    repl = subparsers.add_parser(
        "interactive",
        description="Start an interactive command session "
        "to repeatedly run `interact` and `query` commands.",
    )
    repl.add_argument(
        "-a",
        "--aggressive",
        action="store_true",
        help="If specified, kill the session whenever a search is modified.",
    )
    return parser, hypo, bibli


def hypo_search(catalog, args):
    """
    event search
    """
    print(catalog, args)


def bibli_search(catalog, args):
    """Perform the `bibli subcommand.

    Create a collection of search parameters with `create_search_param` and
    apply them to the ISC Bulletin search.

    If an output file wasn't given, print these results to stdout, limiting to
    10 entries if no limit was specified. If an output file was given, use the
    file's extension to infer whether the file should hold CSV or JSON data,
    and then write the results to the output file in that format.

    :param catalog: The 'EventCatalog' to save search results.
    :param args: All arguments from the command line, as parsed by the top-
                 level parser.
    """
    # Query the database with the collection of filters.
    results = catalog.bibli_search(args)
    print("printout")
    results.get_search_params()

    if not args.outfile:
        # Write the results to stdout, limiting to 10 entries if not specified.
        print("No outfile specified:\n", results)
    else:
        # Write the results to a file.
        if args.outfile.suffix == ".csv":
            write_to_csv(results, args.outfile)
        elif args.outfile.suffix == ".json":
            write_to_json(results, args.outfile)
        else:
            print(
                "Please use an output file that ends with `.csv` or `.json`.",
                file=sys.stderr,
            )


class SearchShell(cmd.Cmd):
    """ 
    interactive search
    """
    print('working on it')

if __name__ == "__main__":
    """Run the main script."""
    parser, inspect_parser, query_parser = make_parser()
    args = parser.parse_args()
    catalog = EventCatalog()

    # Run the chosen subcommand.
    if args.cmd == "event":
        hypo_search(catalog, args)
    elif args.cmd == "bibli":
        bibli_search(catalog, args)
    elif args.cmd == "interactive":
        SearchShell()
