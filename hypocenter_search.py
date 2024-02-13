#! /usr.bin/env python3

from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
from obspy.core import UTCDateTime


def _dict_bibli_search(searcher, args):
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
    if args.shape is not None:
        searcher.shape = args.shape
        searcher.coords = args.coords
    else:
        searcher.shape = "POLY"
        searcher.coords = ""


def format_url(searcher, args):
    """
    searcher -> url
    """
    # Extract search params
    _dict_bibli_search(searcher, args)
    # Format URL
    base = "http://isc-mirror.iris.washington.edu/cgi-bin/web-db-run"
    request = "?request=REVIEWED"
    output_format = "&out_format=ISF2"
    shape = "&searchshape=RECT"
    rect_search = "&bot_lat=&top_lat=&left_lon=&right_lon="
    circ_search = "&ctr_lat=&ctr_lon=&radius=&max_dist_units=deg"
    seismic_region = "&srn="
    geographic_region = "&grn="
    start_year = "&start_year=2022"
    start_month = "&start_month=1&"
    start_day = "start_day=01"
    start_time = "&start_time=00%3A00%3A00"
    end_year = "&end_year=2022"
    end_month = "&end_month=2"
    end_day = "&end_day=01"
    end_time = "&end_time=00%3A00%3A00"
    min_dep = "&min_dep="
    max_dep = "&max_dep="
    min_mag = "&min_mag="
    max_mag = "&max_mag="
    mag_type = "&req_mag_type="
    mag_agency = "&req_mag_agcy="
    min_defining_phase = "&min_def="
    max_defining_phase = "&max_def="
    null_mags = "&null_mag=on"  # optional
    null_phases = "&null_phs=on"  # optional
    output_prime_hypocenters = "&prime_only=on"  # optional
    output_phases = "&include_phases=on"  # optional
    output_magnitudes = "&include_magnitudes=on"  # optional
    output_weblinks = "&include_links=on"  # optional
    output_headers = "&include_headers=on"  # optional
    output_comments = "&include_comments=on"  # optional
    optional_outputs = (
        null_mags
        + null_phases
        + output_prime_hypocenters
        + output_phases
        + output_magnitudes
        + output_weblinks
        + output_headers
        + output_comments
    )

    url = (
        base
        + request
        + output_format
        + shape
        + rect_search
        + circ_search
        + seismic_region
        + geographic_region
        + start_year
        + start_month
        + start_day
        + start_time
        + end_year
        + end_month
        + end_day
        + end_time
        + min_dep
        + max_dep
        + min_mag
        + max_mag
        + mag_type
        + mag_agency
        + min_defining_phase
        + max_defining_phase
        + optional_outputs
    )

    return url


def fetch_url(url):
    """
    fetch html and parse out body text
    """
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
    """
    parse catalog from html body text
    """
    lines = [line for line in body.strings]
    # TODO: integrate RegularExpressions
    # Check empty search
    if "No events with references were found" in lines[23]:
        print()
        print(lines[23])
        exit()
    # TODO:split search catalog
    if "limited to 500 seismic events" in lines[23]:
        print()
        print(lines[23])
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
        lat = event_info[3]
        lon = event_info[4]
        dep = event_info[5]
        if len(event_info) < 10:
            num_articles = int(event_info[6])
            mag_type = ""
            mag_reporting_agency = ""
            mag = ""
        else:
            # TODO: sep mag type and mag source
            mag_type = event_info[6].split("(")[0]
            mag_reporting_agency = event_info[6].split("(")[0]
            mag = event_info[8]
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
