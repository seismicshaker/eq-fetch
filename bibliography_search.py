#! /usr.bin/env python3

from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
from obspy.core import UTCDateTime


def dict_bibli_search(searcher, args):
    """
    arg -> search parameters
    """
    #
    if args.date is None:
        searcher.start_date = args.start_date
        searcher.end_date = args.end_date
    else:
        searcher.start_date = args.date
        searcher.end_date = searcher.start_date + timedelta(days=1)
    searcher.published_min_year = args.published_min_year
    searcher.published_max_year = args.published_max_year
    searcher.published_author = args.published_author
    searcher.publisher = args.publisher
    searcher.sort_by = args.sort_by
    # TODO: extract shape and coords from args.shape
    if args.shape is not None:
        searcher.shape = args.shape
        searcher.coords = args.coords


def format_url(searcher):
    """
    searcher -> url
    """
    base = "http://isc-mirror.iris.washington.edu/cgi-bin/bibsearch.pl"
    shape = f"?searchshape={searcher.shape}"
    coords = f"&coordvals={searcher.coords}"
    start_year = f"&start_year={searcher.start_date.year}"
    start_month = f"&start_month={searcher.start_date.month}"
    start_day = f"&start_day={searcher.start_date.day}"
    start_time = "&stime=00%3A00%3A00"
    end_year = f"&end_year={searcher.end_date.year}"
    end_month = f"&end_month={searcher.end_date.month}"
    end_day = f"&end_day={searcher.end_date.day}"
    end_time = "&etime=00%3A00%3A00"
    min_year = f"&minyear={searcher.published_min_year}"
    max_year = f"&maxyear={searcher.published_max_year}"
    sort_by = f"&sortby=day{searcher.sort_by}"
    publisher = f"&publisher={searcher.publisher}"
    author = f"&authors={searcher.published_author}"

    url = (
        base
        + shape
        + coords
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
    print("Search URL:\n", url)
    # reqest web page
    response = requests.get(url)
    # get HTML text
    html = response.text
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # isolate body text
    body = soup.body

    return body


def parse_bibli_page(searcher, body):
    lines = [line for line in body.strings]
    # Check empty search
    # TODO: Raise exception
    if "No events with references were found" in lines[23]:
        return "Empty"
    # TODO:split search catalog
    if "limited to 500 seismic events" in lines[23]:
        return "too many"
    # Parse content
    header_pos = [n for n, line in enumerate(lines) if line[:4] == " ISC"]
    header_pos.append(len(lines))
    # init catalog
    header_info = [
        "origin_time",
        "lat",
        "lon",
        "dep",
        "mag_type",
        "mag",
        "mag_reporting_agency",
        "event_reporting_agency",
        "event_code",
        "articles",
    ]
    catalog = pd.DataFrame(
        index=range(len(header_pos) - 1), columns=header_info
    )
    for n, pos in enumerate(header_pos[:-1]):
        headers = lines[pos].split()
        event_info = lines[pos + 2].split()
        catalog["event_reporting_agency"].loc[n] = event_info[0]
        catalog["origin_time"] = UTCDateTime(
            event_info[1] + "T" + event_info[2]
        )
        catalog["lat"].loc[n] = event_info[3]
        catalog["lon"].loc[n] = event_info[4]
        catalog["dep"].loc[n] = event_info[5]
        if len(event_info) < 10:
            num_articles = int(event_info[6])
        else:
            # TODO: sep mag type and mag source
            catalog["mag_type"].loc[n] = event_info[6]
            catalog["mag"].loc[n] = event_info[8]
            # Parse numhber of articles
            num_articles = int(event_info[9])
        article_lines = "".join(lines[pos + 3 : header_pos[n + 1]]).split("\n")
        articles = []
        for m in range(num_articles):
            articles.append(article_lines[m])
        catalog["articles"].loc[n] = articles
        # Check for event_code
        if "code" in headers:
            catalog["event_code"] = event_info[-1]
    searcher.results = catalog
