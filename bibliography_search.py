#! /usr.bin/env python3

from datetime import timedelta

import requests
from bs4 import BeautifulSoup


def _dict_bibli_search(args):
    """
    arg -> search parameters
    """
    #
    if args.date is None:
        start_date = args.start_date
        end_date = args.end_date
    else:
        start_date = args.date
        end_date = start_date + timedelta(days=1)
    published_min_year = args.published_min_year
    published_max_year = args.published_max_year
    published_author = args.published_author
    publisher = args.publisher
    sort_by = args.sort_by
    # TODO: extract shape and coords from args.shape
    if args.shape is None:
        shape = "POLY"
        coords = ""
    else:
        shape = args.shape
        coords = args.coords

    return {
        "syear": start_date.year,
        "smonth": start_date.month,
        "sday": start_date.day,
        "eyear": end_date.year,
        "emonth": end_date.month,
        "eday": end_date.day,
        "published_min_year": published_min_year,
        "published_max_year": published_max_year,
        "published_author": published_author,
        "publisher": publisher,
        "shape": shape,
        "coords": coords,
        "sort_by": sort_by,
    }


def format_url(args):
    bibli_search = _dict_bibli_search(args)

    base = "http://isc-mirror.iris.washington.edu/cgi-bin/bibsearch.pl"
    shape = f"?searchshape={bibli_search['shape']}&coordvals={bibli_search['coords']}"
    start_year = f"&start_year={bibli_search['syear']}"
    start_month = f"&start_month={bibli_search['smonth']}"
    start_day = f"&start_day={bibli_search['sday']}"
    start_time = "&stime=00%3A00%3A00"
    end_year = f"&end_year={bibli_search['eyear']}"
    end_month = f"&end_month={bibli_search['emonth']}"
    end_day = f"&end_day={bibli_search['eday']}"
    end_time = "&etime=00%3A00%3A00"
    min_year = f"&minyear={bibli_search['published_min_year']}"
    max_year = f"&maxyear={bibli_search['published_max_year']}"
    sort_by = f"&sortby=day{bibli_search['sort_by']}"
    publisher = f"&publisher={bibli_search['publisher']}"
    author = f"&authors={bibli_search['published_author']}"

    url = (
        base
        + shape
        + start_year
        + start_month
        + start_day
        + start_time
        + end_year
        + end_month
        + end_day
        + end_time
        + min_year
        + max_year
        + sort_by
        + publisher
        + author
    )

    return url


def fetch_url(url):
    # reqest web page
    response = requests.get(url)
    # get HTML text
    html = response.text
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # isolate body text
    body = soup.body.get_text().strip()

    return body


def parse_bibli_page(body):
    cat = body

    return cat
