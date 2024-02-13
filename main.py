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
import sys

from catalog import SearchCatalog
from formatting import date_fromisoformat
from write import write_to_csv, write_to_json


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
        "-d",
        "--date",
        type=date_fromisoformat,
        help="Event origin date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    hypo.add_argument(
        "-s",
        "--start_date",
        type=date_fromisoformat,
        help="Event origin start date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    hypo.add_argument(
        "-e",
        "--end_date",
        type=date_fromisoformat,
        help="Event origin end date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    hypo.add_argument(
        "--search_region",
        default="global",
        type=str,
        help="Search Region options\n"
        "global [DEFAULT]\n"
        "rect [Bottom Latitude (-90 to 90)] "
        "[Top Latitude -90 to 90)] [Left Longitude -180 to 180] "
        "[Right Longitude -180 to 180]\n"
        "circ [Central Latitude (-90 to 90)] [Central Longitude -180 to 180] "
        "[Radius (deg/km]]\n"
        "seis_region [Seismic region number (1 to 50)]"
        "geo_region [Geographic region number (1 to 757]]",
    )
    hypo.add_argument(
        "--reviewed",
        action="store_true",
        help="Reviewed ISC Bulletin",
    )
    hypo.add_argument(
        "--min_depth",
        type=str,
        help="min depth ",
    )
    hypo.add_argument(
        "--max_depth",
        type=str,
        help="max depth ",
    )
    hypo.add_argument(
        "--min_mag",
        type=str,
        help="min magnitude ",
    )
    hypo.add_argument(
        "--max_mag",
        type=str,
        help="max mag ",
    )
    hypo.add_argument(
        "--mag_type",
        type=str,
        help="magnitude type",
    )
    hypo.add_argument(
        "--mag_author",
        type=str,
        help="magnitude author ",
    )
    hypo.add_argument(
        "--min_phase",
        type=str,
        help="min defining phase ",
    )
    hypo.add_argument(
        "--max_phase",
        type=str,
        help="max defining phase ",
    )
    hypo.add_argument(
        "--include_null_depth",
        action="store_true",
        help="include unknown depths ",
    )
    hypo.add_argument(
        "--include_null_mag",
        action="store_true",
        help="include unknown magnitudes ",
    )
    hypo.add_argument(
        "--include_null_phs",
        action="store_true",
        help="include unknown phases ",
    )
    hypo.add_argument(
        "--only_prime_hypo",
        action="store_true",
        help="include  ",
    )
    hypo.add_argument(
        "--include_phases",
        action="store_true",
        help="include phases ",
    )
    hypo.add_argument(
        "--include_magnitudes",
        action="store_true",
        help="include  ",
    )
    hypo.add_argument(
        "--include_weblinks",
        action="store_true",
        help="include  ",
    )
    hypo.add_argument(
        "--include_headers",
        action="store_true",
        help="include  ",
    )
    hypo.add_argument(
        "--include_comments",
        action="store_true",
        help="include ",
    )

    hypo.add_argument(
        "-o",
        "--outfile",
        type=pathlib.Path,
        help="File in which to save structured results. "
        "If omitted, results are printed to standard output.",
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
    # TODO: format shape input to read shape and coords
    bibli.add_argument(
        "--shape",
        type=str,
        help="Shape and coordinates e.g.: ...",
    )
    # TODO: lookup sort_by options
    bibli.add_argument(
        "--sort_by",
        default="day",
        type=str,
        help="Sort by e.g.: ...",
    )
    # TODO: check that year is correct format
    bibli.add_argument(
        "--published_min_year",
        default="",
        type=str,
        help="search parameter, " "in YYYY (e.g. 2020).",
    )
    # TODO: check that year is correct format
    bibli.add_argument(
        "--published_max_year",
        default="",
        type=str,
        help="search parameter, " "in YYYY (e.g. 2021).",
    )
    bibli.add_argument(
        "--publisher",
        default="",
        type=str,
        help="search parameter, " " (e.g. BSSA).",
    )
    bibli.add_argument(
        "--published_author",
        default="",
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


def hypo_search(searcher, args):
    """
    event search
    """
    # Query the database with the collection of filters.
    catalog = searcher.hypo_search(args)

    if not args.outfile:
        # Write the results to stdout, limiting to 10 entries if not specified.
        print("No outfile specified:\n", catalog)
    else:
        # Write the results to a file.
        if args.outfile.suffix == ".csv":
            write_to_csv(catalog, args.outfile)
        elif args.outfile.suffix == ".json":
            write_to_json(catalog, args.outfile)
        else:
            print(
                "Please use an output file that ends with `.csv` or `.json`.",
                file=sys.stderr,
            )


def bibli_search(searcher, args):
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
    catalog = searcher.bibli_search(args)

    if not args.outfile:
        # Write the results to stdout, limiting to 10 entries if not specified.
        print("No outfile specified:\n", catalog)
    else:
        # Write the results to a file.
        if args.outfile.suffix == ".csv":
            write_to_csv(catalog, args.outfile)
        elif args.outfile.suffix == ".json":
            write_to_json(catalog, args.outfile)
        else:
            print(
                "Please use an output file that ends with `.csv` or `.json`.",
                file=sys.stderr,
            )


class SearchShell(cmd.Cmd):
    """
    interactive search
    """

    def __init__(self):
        self.status = "working on it"


if __name__ == "__main__":
    """Run the main script."""
    parser, inspect_parser, query_parser = make_parser()
    args = parser.parse_args()
    searcher = SearchCatalog()

    # Run the chosen subcommand.
    if args.cmd == "hypo":
        hypo_search(searcher, args)
    elif args.cmd == "bibli":
        bibli_search(searcher, args)
    elif args.cmd == "interactive":
        SearchShell()
