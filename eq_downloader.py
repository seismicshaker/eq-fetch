#!/usr/bin/env python3
"""Download search results from ISC.

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
import sys
from importlib import import_module

# Import local src code
import_path = ".".join(__name__.split(".")[:-1])
print(import_path)
adds = import_module(import_path + "src.parser_adds")
SearchCatalog = import_module("src.catalog").SearchCatalog
write_to_csv = import_module("src.write").write_to_csv
write_to_json = import_module("src.write").write_to_json


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
    # Search criterion args
    adds.date_range(hypo)
    adds.depth_range(hypo)
    adds.mag_range(hypo)
    adds.mag_info(hypo)
    adds.outfile(hypo)

    # ISC Bulletin args
    adds.hypo_region(hypo)
    adds.hypo_review(hypo)
    adds.hypo_nulls(hypo)
    adds.hypo_prime(hypo)
    adds.hypo_misc(hypo)

    # Add the 'bibli' subcommand parser.
    bibli = subparsers.add_parser(
        "bibli",
        description="Event bibliography search.",
    )
    # Search criterion args
    adds.date_range(bibli)
    adds.depth_range(bibli)
    adds.mag_range(bibli)
    adds.outfile(bibli)

    # Bibilography args
    adds.bibli_region(bibli)
    adds.bibli_sort(bibli)
    adds.bibli_pub_info(bibli)

    # Iterative Search
    adds.iter_search(bibli)

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


def gcmt_search(searcher, args):
    """
    event search
    """
    return "In development"


def hypo_search(searcher, args):
    """
    event search
    """
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
    if args.cmd == "bibli":
        bibli_search(searcher, args)
    elif args.cmd == "hypo":
        print("\n\tFetching QuakeML file. This may take a few minutes...\n\n")
        hypo_search(searcher, args)
    elif args.cmd == "gcmt":
        gcmt_search(searcher, args)
    elif args.cmd == "interactive":
        SearchShell()
