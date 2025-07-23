from typing import TypedDict, Literal
from obspy.core.utcdatetime import UTCDateTime


class LocationCriteria(TypedDict, total=False):
    global_search: bool
    seismic_region: int | None
    geographic_region: int | None
    center_lat: float | None
    center_lon: float | None
    radius_km: float | None
    lat_min: float | None
    lat_max: float | None
    lon_min: float | None
    lon_max: float | None


class RangeCriteria(TypedDict, total=False):
    depth_min: float | None
    depth_max: float | None
    mag_min: float | None
    mag_max: float | None
    time_start: UTCDateTime | None
    time_end: UTCDateTime | None
    # TODO: add mag type


class BibliographyCriteria(TypedDict, total=False):
    journal: str
    author: str


class MechanismCriteria(TypedDict, total=False):
    mechanism: Literal["normal", "thrust", "strike-slip", "unknown", ""]
    source: str
    centroid_time_shift_min: float | None
    centroid_time_shift_max: float | None
    tension_axis_plunge_min: float | None
    tension_axis_plunge_max: float | None
    null_axis_plunge_min: float | None
    null_axis_plunge_max: float | None
    strike_min: float | None
    strike_max: float | None
    dip_min: float | None
    dip_max: float | None
    rake_min: float | None
    rake_max: float | None


class SearchCriteria(
    LocationCriteria,
    RangeCriteria,
    BibliographyCriteria,
    MechanismCriteria,
    total=False,
):
    pass


def initialize_criteria() -> SearchCriteria:
    """Return default criteria dict with correct types."""
    return SearchCriteria(
        global_search=True,
        seismic_region=None,
        geographic_region=None,
        center_lat=None,
        center_lon=None,
        radius_km=None,
        lat_min=-90.0,
        lat_max=90.0,
        lon_min=-180.0,
        lon_max=180.0,
        depth_min=0.0,
        depth_max=700.0,
        mag_min=None,
        mag_max=None,
        time_start=None,
        time_end=None,
        journal="",
        author="",
        mechanism="",
        source="",
        centroid_time_shift_min=None,
        centroid_time_shift_max=None,
        tension_axis_plunge_min=None,
        tension_axis_plunge_max=None,
        null_axis_plunge_min=None,
        null_axis_plunge_max=None,
        strike_min=None,
        strike_max=None,
        dip_min=None,
        dip_max=None,
        rake_min=None,
        rake_max=None,
    )
