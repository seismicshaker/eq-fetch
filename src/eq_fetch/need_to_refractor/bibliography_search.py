"""."""

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from obspy.core import UTCDateTime


def _dict_bibli_search(searcher, args):
    """arg -> search parameters."""
    if args.date is None:
        searcher.start_date = args.start_date
        searcher.end_date = args.end_date
    else:
        searcher.start_date = args.date
        searcher.end_date = args.date
    searcher.published_min_year = args.published_min_year
    searcher.published_max_year = args.published_max_year
    searcher.published_author = args.published_author
    searcher.publisher = args.publisher
    searcher.sort_by = args.sort_by
    # TODO: extract shape and coords from args.shape
    if args.shape is not None:
        searcher.shape = args.shape
        searcher.coords = args.coords
    else:
        searcher.shape = "POLY"
        searcher.coords = ""
    searcher.source = "ISC Event Bibliography"
    searcher.min_depth = args.min_depth
    searcher.max_depth = args.max_depth
    searcher.min_mag = args.min_mag
    searcher.max_mag = args.max_mag


def format_url(searcher, args):
    """searcher -> url."""
    # Extract search params
    _dict_bibli_search(searcher, args)
    # Format URL
    base = "https://www.isc.ac.uk/cgi-bin/bibsearch.pl"
    shape = f"?searchshape={searcher.shape}"
    coords = f"&coordvals={searcher.coords}"
    start_year = f"&start_year={searcher.start_date.year}"
    start_month = f"&start_month={searcher.start_date.month}"
    start_day = f"&start_day={searcher.start_date.day}"
    start_time = "&stime=00%3A00%3A00"
    end_year = f"&end_year={searcher.end_date.year}"
    end_month = f"&end_month={searcher.end_date.month}"
    end_day = f"&end_day={searcher.end_date.day}"
    end_time = "&etime=23%3A59%3A29"
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
    """Fetch html and parse out body text."""
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


def parse_bibli_page(searcher, body, iter_search=False):
    """Parse catalog from html body text."""
    lines = [line for line in body.strings]
    # Check empty search
    if "No events with references were found" in lines[23]:
        print()
        print(lines[23])
        exit()
    if "limited to 500 seismic events" in lines[23]:
        print(
            "\n" + lines[23][21:-11] + ", or consider an iterative search."
            "\n  i.e., eq_downloader.py --iter_search [increment]\n"
        )
        exit()
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
        "article_num",
        "articles",
    ]
    rows = []
    for n, pos in enumerate(header_pos[:-1]):
        # Split headers and event info
        headers = lines[pos].split()
        event_info = lines[pos + 2].split()
        # Parse

        event_reporting_agency = event_info[0]
        origin_time = UTCDateTime(event_info[1] + "T" + event_info[2])
        lat = float(event_info[3])
        lon = float(event_info[4])
        dep = float(event_info[5])
        if len(event_info) < 10:
            num_articles = int(event_info[6])
            mag_type = ""
            mag_reporting_agency = ""
            mag = np.nan
        else:
            # TODO: sep mag type and mag source
            mag_type = event_info[6].split("(")[0]
            mag_reporting_agency = event_info[6].split("(")[0]
            mag = float(event_info[8])
            # Parse numhber of articles
            num_articles = int(event_info[9])
        # Check for event_code
        if "code" in headers:
            event_code = event_info[-1]
        else:
            event_code = ""
        # Iterate through articles
        article_lines = "".join(lines[pos + 3 : header_pos[n + 1]]).split("\n")
        for m in range(num_articles):
            row = [
                origin_time,
                lat,
                lon,
                dep,
                mag_type,
                mag,
                mag_reporting_agency,
                event_reporting_agency,
                event_code,
                m + 1,
                article_lines[m],
            ]
            rows.append(row)
    catalog = pd.DataFrame(rows, columns=header_info)
    searcher.earthquake_catalog = catalog


def filter_depths(searcher):
    """If defined, filter depth ranges."""
    # Define range
    min_depth = 0.0 if searcher.min_depth is None else searcher.min_depth
    max_depth = 6371.0 if searcher.max_depth is None else searcher.max_depth
    # Subset catalog
    catalog = searcher.earthquake_catalog
    searcher.earthquake_catalog = catalog[
        (catalog["dep"] >= min_depth) & (catalog["dep"] <= max_depth)
    ]


def filter_mags(searcher):
    """If defined, filter magnitude ranges."""
    # Define range
    min_mag = -10.0 if searcher.min_mag is None else searcher.min_mag
    max_mag = 10.0 if searcher.max_mag is None else searcher.max_mag
    # Subset catalog
    catalog = searcher.earthquake_catalog
    searcher.earthquake_catalog = catalog[
        (catalog["mag"] >= min_mag) & (catalog["mag"] <= max_mag)
    ]
