from datetime import timedelta
from xml.etree import ElementTree

import pandas as pd
import requests
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
    if args.reviewed:
        searcher.reviewed = "REVIEWED"
    else:
        searcher.reviewed = "COMPREHENSIVE"
    # TODO: Setup saerch region

    # TODO dep, mag, and phase filters

    searcher.optional_outputs = ""
    if args.include_null_mag:
        searcher.optional_outputs += "&null_mag=on"
    if args.include_null_phs:
        searcher.optional_outputs += "&null_phs=on"
    if args.only_prime_hypo:
        searcher.optional_outputs += "&prime_only=on"
    if args.include_phases:
        searcher.optional_outputs += "&include_phases=on"
    if args.include_magnitudes:
        searcher.optional_outputs += "&include_magnitudes=on"
    if args.include_weblinks:
        searcher.optional_outputs += "&include_links=on"
    if args.include_headers:
        searcher.optional_outputs += "&include_headers=on"
    if args.include_comments:
        searcher.optional_outputs += "&include_comments=on"

    searcher.source = "ISC Bulletin"


def format_url(searcher, args):
    """
    searcher -> url
    """
    # Extract search params
    _dict_bibli_search(searcher, args)
    # Format URL
    base = "https://www.isc.ac.uk/cgi-bin/web-db-run"
    request = f"?request={searcher.reviewed}"
    output_format = "&out_format=QuakeML"
    # TODO: setup saerch region
    shape = "&searchshape=RECT"
    rect_search = "&bot_lat=&top_lat=&left_lon=&right_lon="
    circ_search = "&ctr_lat=&ctr_lon=&radius=&max_dist_units=deg"
    seismic_region = "&srn="
    geographic_region = "&grn="
    start_year = f"&start_year={searcher.start_date.year}"
    start_month = f"&start_month={searcher.start_date.month}"
    start_day = f"&start_day={searcher.start_date.day}"
    start_time = "&start_time=00%3A00%3A00"
    end_year = f"&end_year={searcher.end_date.year}"
    end_month = f"&end_month={searcher.end_date.month}"
    end_day = f"&end_day={searcher.end_date.day}"
    end_time = "&end_time=23%3A59%3A59"
    # TODO dep, mag, and phase filters
    min_dep = "&min_dep="
    max_dep = "&max_dep="
    min_mag = "&min_mag="
    max_mag = "&max_mag="
    mag_type = "&req_mag_type="
    mag_agency = "&req_mag_agcy="
    min_defining_phase = "&min_def="
    max_defining_phase = "&max_def="
    optional_outputs = searcher.optional_outputs

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


def fetch_xml(url):
    """
    fetch html and parse out body text
    """
    print("Searching URL...\n", url, "\n")

    response = requests.get(url)
    xml_data = response.content

    return xml_data


def parse_quakeML(searcher, xml_data):
    """
    parse catalog from xml string
    """
    # TODO: May not import local module
    import quakeML as qml

    if 1:
        print(xml_data.decode("ascii"))
        with open("20220812.xml", "w+") as fOut:
            for line in xml_data.decode("ascii"):
                fOut.write(line)
    # Check response
    if b"your request cannot be processed at the present time" in xml_data:
        print(
            "\n\nSorry, the online repository is unresponsive at the moment."
            + " Please try again in a few minutes."
        )
        exit()
    # Check empty search
    if b"No events were found" in xml_data:
        print("\n\nSorry, the search criterion yield no event.")
        exit()

    # TODO: overfilled search string
    # Check overfilled search
    if b'OVERFILLED"' in xml_data:
        print(
            "\n\nSorry, the search criterion yield more than XXX events."
            + " Please consider limiting the date range."
        )
        exit()

    # Extract events from XML
    xml_tree = ElementTree.fromstring(xml_data)  # build xml tree
    xml_event_parameters = qml.getEventParameters(xml_tree)
    xml_events = qml.getEvents(xml_event_parameters)
    print(f"\nFound {len(xml_events)} events...\n")

    """
    https://sites.psu.edu/charlesammon/2017/01/31/parsing-usgs-quakeml-files-with-python/

    https://docs.python.org/3/library/xml.etree.elementtree.html

    https://github.com/Jamalreyhani/pyquakeml/blob/master/src/pyquakeml.py

    https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
    """
    namespaces = qml.get_namespaces()
    # TODO: itearte each event
    catalog = []
    for xml_event in xml_events:
        # TODO: extract earthquake info from xml
        #  following:
        #    https://sites.psu.edu/charlesammon/2017/01/31/parsing-usgs-quakeml-files-with-python/
        #    https://docs.python.org/3/library/xml.etree.elementtree.html

        # build event dictionary
        origins = qml.getEventOrigins(xml_event)
        for origin in origins:
            print("ori", origin.attrib)
        ev = {}
        try:
            ev["eventid"] = xml_event.attrib[
                "{http://anss.org/xmlns/catalog/0.1}eventid"
            ]
        except KeyError:
            print("no eventID")
        try:
            ev["publicID"] = xml_event.attrib["publicID"]
            ev["eventsource"] = xml_event.attrib[
                "{http://anss.org/xmlns/catalog/0.1}eventsource"
            ]
        except KeyError:
            print("no publicID")
        try:
            ev["datasource"] = xml_event.attrib[
                "{http://anss.org/xmlns/catalog/0.1}datasource"
            ]
        except KeyError:
            print("no datasource")
        try:
            ev["preferredOriginID"] = xml_event.find("d:preferredOriginID", namespaces)
        except KeyError:
            print("no prefOriginID")
        try:
            ev["preferredMagnitudeID"] = xml_event.find(
                "d:preferredMagnitudeID", namespaces
            )
        except KeyError:
            print("no prefMagID")
        mags = xml_event.findall("d:magnitude", namespaces)
        print(mags)

        print(ev)
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
            ]
            rows.append(row)
    catalog = pd.DataFrame(rows, columns=header_info)
    searcher.earthquake_catalog = catalog
