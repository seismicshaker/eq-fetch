"""Module for formatting searches."""

from typing import Any
from obspy.core.utcdatetime import UTCDateTime
from eq_fetch import SearchCriteria


def build_query(source: str, criteria: dict[str, Any]) -> SearchCriteria:
    """
    Converts validated criteria into source-specific query parameters.
    Returns a dict suitable for requests to download.py handlers.
    """
    params = {}

    print(type(criteria))
    # Location criteria
    if not criteria.get("global_search"):
        if criteria.get("seismic_region"):
            params["seismic_region"] = criteria["seismic_region"]
        if criteria.get("geographic_region"):
            params["geographic_region"] = criteria["geographic_region"]
        if (
            criteria.get("center_lat") is not None
            and criteria.get("center_lon") is not None
            and criteria.get("radius_km") is not None
        ):
            params["center_lat"] = criteria["center_lat"]
            params["center_lon"] = criteria["center_lon"]
            params["radius_km"] = criteria["radius_km"]
        if criteria.get("lat_min") is not None:
            params["lat_min"] = criteria["lat_min"]
        if criteria.get("lat_max") is not None:
            params["lat_max"] = criteria["lat_max"]
        if criteria.get("lon_min") is not None:
            params["lon_min"] = criteria["lon_min"]
        if criteria.get("lon_max") is not None:
            params["lon_max"] = criteria["lon_max"]

    # Range criteria
    if criteria.get("depth_min") is not None:
        params["depth_min"] = criteria["depth_min"]
    if criteria.get("depth_max") is not None:
        params["depth_max"] = criteria["depth_max"]
    if criteria.get("mag_min") is not None:
        params["mag_min"] = criteria["mag_min"]
    if criteria.get("mag_max") is not None:
        params["mag_max"] = criteria["mag_max"]
    if isinstance(criteria.get("time_start"), UTCDateTime):
        params["time_start"] = criteria["time_start"].isoformat()
    if isinstance(criteria.get("time_end"), UTCDateTime):
        params["time_end"] = criteria["time_end"].isoformat()

    # Source-specific criteria
    if source == "isc_event_bibliography":
        if criteria.get("journal"):
            params["journal"] = criteria["journal"]
        if criteria.get("author"):
            params["author"] = criteria["author"]
    if source in {"gcmt", "scardec"}:
        if criteria.get("mechanism"):
            params["mechanism"] = criteria["mechanism"]
        if criteria.get("source"):
            params["source"] = criteria["source"]

    # Add more source-specific mapping as needed
    return params


def preview_results(results) -> str:
    """
    Generates a human-readable summary of a search result set.
    Accepts either a dict, list, or DataFrame (if pandas is used).
    """
    if results is None:
        return "No results found or download failed."
    try:
        # If results is a pandas DataFrame
        import pandas as pd

        if isinstance(results, pd.DataFrame):
            count = len(results)
            if count == 0:
                return "No events found."
            top_event = results.iloc[0]
            summary = (
                f"{count} events found.\n"
                f"Top event: M{top_event.get('magnitude', '')}, "
                f"{top_event.get('region', '')}, "
                f"{top_event.get('origin_time', '')}"
            )
            return summary
        # If results is a list of dicts
        elif isinstance(results, list) and results and isinstance(results[0], dict):
            count = len(results)
            top_event = results[0]
            summary = (
                f"{count} events found.\n"
                f"Top event: M{top_event.get('magnitude', '')}, "
                f"{top_event.get('region', '')}, "
                f"{top_event.get('origin_time', '')}"
            )
            return summary
        # If results is a dict (single event)
        elif isinstance(results, dict):
            summary = (
                f"Single event found:\n"
                f"M{results.get('magnitude', '')}, "
                f"{results.get('region', '')}, "
                f"{results.get('origin_time', '')}"
            )
            return summary
        else:
            return f"Results found: {results}"
    except Exception as e:
        return f"Error summarizing results: {e}"
