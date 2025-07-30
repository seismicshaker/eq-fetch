import argparse
import csv
import random
import sqlite3
import sys
import time
from pathlib import Path

import pandas as pd
import requests
import rich_click as click
from bs4 import BeautifulSoup
from obspy.core.utcdatetime import UTCDateTime
from rich.console import Console
from rich.progress import track

console = Console()

_DB_PATH = Path("data/event_index.db")


class BibliographyCriteria(argparse.Namespace):
    # Instances
    output: Path
    start_time: UTCDateTime
    end_time: UTCDateTime
    lats: list[float]
    lons: list[float]
    deps: list[float]
    mags: list[float]
    journal: str
    author: str

    def __init__(self):
        self.output = Path("./bibliographies.csv")
        self.start_time = UTCDateTime("1800/01/01")
        self.end_time = UTCDateTime("2025/12/31")
        self.lats = [-90.0, 90.0]
        self.lons = [-180.0, 180.0]
        self.deps = [0, 3500]
        self.mags = [10e-10, 10]
        self.journal = ""
        self.author = ""

        super().__init__()


class OneOrTwoFloatsParamType(click.ParamType):
    name: str = "FLOAT_RANGE"

    def convert(self, value: str, param, ctx):
        try:
            float_values = [float(v) for v in value.split()]
        except ValueError:
            self.fail(
                f"{value!r} is not a valid float or space-separated list of floats.",
                param,
                ctx,
            )

        if not (1 <= len(float_values) <= 2):
            self.fail(
                f"Expected 1 or 2 values, but got {len(float_values)} for {param.name}.",
                param,
                ctx,
            )

        if len(float_values) == 1:
            return [float_values[0], float_values[0]]
        else:
            return float_values


ONE_OR_TWO_FLOATS = OneOrTwoFloatsParamType()


def fetch_bibliographies(event_id: int) -> list[str]:
    base_url = "https://www.isc.ac.uk/cgi-bin/FormatBibprint.pl"
    url: str = f"{base_url}?evid={event_id}"
    bibliographies: list[str] = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text_content = soup.get_text()
        lines = text_content.splitlines()

        if len(lines[24].split()) == 17:
            lines[25] = lines[25][91:]
        elif len(lines[24].split()) == 19:
            lines[25] = lines[25][107:]
        else:
            print(f"{len(lines[24].split())=}")
            sys.exit(0)

        for line in lines[25:-10]:
            if line:
                bibliographies.append(line.strip())

        time.sleep(round(random.uniform(0.45, 0.55), 2))

    except requests.exceptions.RequestException as e:
        console.print(
            f"[bold red]Error fetching bibliography for event {event_id}: {e}[/bold red]"
        )
    except Exception as e:
        console.print(
            f"[bold red]An unexpected error occurred for event {event_id}: {e}[/bold red]"
        )
    return bibliographies


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, writable=True),
    default="bibliographies.csv",
    show_default=True,
    help="Path to the output CSV file.",
)
@click.option(
    "--start-time",
    type=click.DateTime(formats=["%Y%m%d %H:%M:%S", "%Y%m%d"]),
    help="Start origin time (YYYYMMDD hh:mm:ss or YYYYMMDD).",
)
@click.option(
    "--end-time",
    type=click.DateTime(formats=["%Y%m%d %H:%M:%S", "%Y%m%d"]),
    help="End origin time (YYYYMMDD hh:mm:ss or YYYYMMDD).",
)
@click.option(
    "--lats",
    type=ONE_OR_TWO_FLOATS,
    help="Central latitude or latitude range. Provide 1 or 2 values separated by spaces.",
)
@click.option(
    "--lons",
    type=ONE_OR_TWO_FLOATS,
    help="Central longitude or longitude range. Provide 1 or 2 values separated by spaces.",
)
@click.option(
    "--deps",
    type=ONE_OR_TWO_FLOATS,
    help="Central depth or depth range in km. Provide 1 or 2 values separated by spaces.",
)
@click.option(
    "--mags",
    type=ONE_OR_TWO_FLOATS,
    help="Central magnitude or magnitude range. Provide 1 or 2 values separated by spaces.",
)
@click.option("--journal", type=str, help="Select Journal Name.")
@click.option("--author", type=str, help="Select Author Name.")
def main(
    output: str,
    start_time: UTCDateTime,
    end_time: UTCDateTime,
    lats: list[float],
    lons: list[float],
    deps: list[float],
    mags: list[float],
    author: str,
    journal: str,
):
    """
    Extracts bibliographies for ISC seismic events based on user-specified filters.

    The extracted data is saved to a CSV file.
    """
    search_criteria = BibliographyCriteria()

    search_criteria.output = Path(output)

    if start_time:
        search_criteria.start_time = UTCDateTime(start_time)
    if end_time:
        search_criteria.end_time = UTCDateTime(end_time)
    if lats:
        search_criteria.lats = lats
    if lons:
        search_criteria.lons = lons
    if deps:
        search_criteria.deps = deps
    if mags:
        search_criteria.mags = mags
    if journal:
        search_criteria.journal = journal
    if author:
        search_criteria.author = author

    # Search
    conn = None
    params = []
    query = ""
    try:
        conn = sqlite3.connect(_DB_PATH)
        query = "SELECT ISC_event, Origin_Time, Lat, Lon, Depth, Mag FROM isc_events WHERE 1=1"

        if search_criteria.start_time:
            query += " AND Origin_Time >= ?"
            params.append(
                str(search_criteria.start_time)
            )  # Convert UTCDateTime to string for comparison

        if search_criteria.end_time:
            query += " AND Origin_Time <= ?"
            params.append(str(search_criteria.end_time))

        if search_criteria.lats and len(search_criteria.lats) == 2:
            query += " AND Lat BETWEEN ? AND ?"
            params.extend(sorted(search_criteria.lats))

        if search_criteria.lons and len(search_criteria.lons) == 2:
            query += " AND Lon BETWEEN ? AND ?"
            params.extend(sorted(search_criteria.lons))

        if search_criteria.deps and len(search_criteria.deps) == 2:
            query += " AND Depth BETWEEN ? AND ?"
            params.extend(sorted(search_criteria.deps))

        if search_criteria.mags and len(search_criteria.mags) == 2:
            query += " AND Mag BETWEEN ? AND ?"
            params.extend(sorted(search_criteria.mags))

        events_df = pd.read_sql_query(query, conn, params=params)

        if events_df.empty:
            console.print(
                "[bold yellow]No events found matching the specified criteria in the local database. Exiting.[/bold yellow]"
            )
            sys.exit(0)

        console.print(
            f"[bold green]Found {len(events_df)} events matching the criteria in local DB. Proceeding to fetch bibliographies...[/bold green]"
        )

        all_bibliographies = []
        all_bibliographies.append(
            [
                "ISC_event",
                "Origin_Time",
                "Lat",
                "Lon",
                "Depth",
                "Mag",
                "Bibliography_Entry",
            ]
        )

        for _, event in track(
            events_df.iterrows(),
            total=len(events_df),
            description="Fetching bibliographies...",
            console=console,
        ):
            event_id: int = int(event["ISC_event"])
            origin_time = UTCDateTime(event["Origin_Time"])
            lat = float(event["Lat"])
            lon = float(event["Lon"])
            depth = float(event["Depth"])
            max_mag = float(event["Mag"])

            bibliographies = fetch_bibliographies(event_id)
            if bibliographies:
                for bib_entry in bibliographies:
                    all_bibliographies.append(
                        [
                            event_id,
                            origin_time,
                            lat,
                            lon,
                            depth,
                            max_mag,
                            bib_entry,
                        ]
                    )
            else:
                all_bibliographies.append(
                    [event_id, origin_time, lat, lon, depth, max_mag, ""]
                )

        with open(search_criteria.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(all_bibliographies)

        console.print(
            f"[bold green]Successfully extracted bibliographies to {search_criteria.output}[/bold green]"
        )

    except sqlite3.Error as e:
        console.print(f"[bold red]Database error: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred in main: {e}[/bold red]")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
