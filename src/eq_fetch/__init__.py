from typing import TypedDict, Literal
from obspy.core.utcdatetime import UTCDateTime
from pathlib import Path
import argparse
import rich_click as click


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


class RangeParams(click.ParamType):
    name: str = "FLOAT_RANGE"

    def convert(self, value: str, param, ctx) -> list[float]:
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


# class LocationCriteria(TypedDict, total=False):
#     global_search: bool
#     seismic_region: int | None
#     geographic_region: int | None
#     center_lat: float | None
#     center_lon: float | None
#     radius_km: float | None
#     lat_min: float | None
#     lat_max: float | None
#     lon_min: float | None
#     lon_max: float | None
#     depth_min: float | None
#     depth_max: float | None
#     time_start: UTCDateTime | None
#     time_end: UTCDateTime | None
#
#
# class MagnitudeCriteria(TypedDict, total=False):
#     mag_min: float | None
#     mag_max: float | None
#     mag_type: Literal["Mw", "Mb", "Ms", "Ml", ""]
#
#
# class MechanismCriteria(TypedDict, total=False):
#     mechanism: Literal["normal", "thrust", "strike-slip", "unknown", ""]
#     source: str
#     centroid_time_shift_min: float | None
#     centroid_time_shift_max: float | None
#     tension_axis_plunge_min: float | None
#     tension_axis_plunge_max: float | None
#     null_axis_plunge_min: float | None
#     null_axis_plunge_max: float | None
#     strike_min: float | None
#     strike_max: float | None
#     dip_min: float | None
#     dip_max: float | None
#     rake_min: float | None
#     rake_max: float | None
#
#
# class SearchCriteria(
#     LocationCriteria,
#     MagnitudeCriteria,
#     BibliographyCriteria,
#     MechanismCriteria,
#     total=False,
# ):
#     pass
#
#
# def initialize_criteria() -> SearchCriteria:
#     """Return default criteria dict with correct types."""
#     return SearchCriteria(
#         global_search=True,
#         seismic_region=None,
#         geographic_region=None,
#         center_lat=None,
#         center_lon=None,
#         radius_km=None,
#         lat_min=-90.0,
#         lat_max=90.0,
#         lon_min=-180.0,
#         lon_max=180.0,
#         depth_min=0.0,
#         depth_max=1000.0,
#         time_start=None,
#         time_end=None,
#         mag_min=None,
#         mag_max=None,
#         mag_type="",
#         journal="",
#         author="",
#         mechanism="",
#         source="",
#         centroid_time_shift_min=None,
#         centroid_time_shift_max=None,
#         tension_axis_plunge_min=None,
#         tension_axis_plunge_max=None,
#         null_axis_plunge_min=None,
#         null_axis_plunge_max=None,
#         strike_min=None,
#         strike_max=None,
#         dip_min=None,
#         dip_max=None,
#         rake_min=None,
#         rake_max=None,
#     )
