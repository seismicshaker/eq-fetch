#! /usr.bin/env python3

from datetime import timedelta


def format_search_paraams(args):
    """
    arg -> search parameters
    """
    if args.date is not None:
        start_date = args.date
        end_date = start_date + timedelta(days=1)
    else:
        start_date = args.start_date
        end_date = args.end_date
    if args.published_min_year is None:
        published_min_year = ""
    else:
        published_min_year = args.published_min_year
    if args.published_max_year is None:
        published_max_year = ""
    else:
        published_max_year = args.published_max_year
    if args.published_author is None:
        published_author = ""
    else:
        published_author = args.published_author
    print("args", args)

    search_params = {
        "start_date": start_date,
        "end_date": end_date,
        "published_min_year": published_min_year,
        "published_max_year": published_max_year,
        "published_author": published_author,
    }
    return search_params


def format_url(search_params):
    base = "http://isc-mirror.iris.washington.edu/cgi-bin/bibsearch.pl"
    shape = "?searchshape=POLY&coordvals="
    start_date = "&start_year=2018&start_month=01&start_day=01"
    start_time = "&stime=00%3A00%3A00"
    end_date = "&end_year=2018&end_month=06&end_day=01"
    end_time = "&etime=00%3A00%3A00"
    min_year = "&minyear="
    max_year = "&maxyear="
    sort_by = "&sortby=day"
    publisher = "&publisher="
    author = "&authors="

    url = (
        base
        + shape
        + start_date
        + start_time
        + end_date
        + end_time
        + min_year
        + max_year
        + sort_by
        + publisher
        + author
    )

    return url
