#! /usr.bin/env python3

from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
from obspy.core import UTCDateTime


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
        "source": "isc-event_bibli",
    }


def format_url(bibli_search):
    base = "http://isc-mirror.iris.washington.edu/cgi-bin/bibsearch.pl"
    shape = f"?searchshape={bibli_search['shape']}"
    coords = f"&coordvals={bibli_search['coords']}"
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


def parse_bibli_page(body):
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
    return catalog
