import pathlib

from formatting import date_fromisoformat


def date_range(parser):
    """ """
    parser.add_argument(
        "-d",
        "--date",
        type=date_fromisoformat,
        help="Event origin date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    parser.add_argument(
        "-s",
        "--start_date",
        type=date_fromisoformat,
        help="Event origin start date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    parser.add_argument(
        "-e",
        "--end_date",
        type=date_fromisoformat,
        help="Event origin end date search parameter, "
        "in YYYY-MM-DD format (e.g. 2020-12-31).",
    )
    return parser


def depth_range(parser):
    """ """
    parser.add_argument(
        "--min_depth",
        type=str,
        help="min depth ",
    )
    parser.add_argument(
        "--max_depth",
        type=str,
        help="max depth ",
    )
    return parser


def mag_range(parser):
    """ """

    parser.add_argument(
        "--min_mag",
        type=str,
        help="min magnitude ",
    )
    parser.add_argument(
        "--max_mag",
        type=str,
        help="max mag ",
    )
    return parser


def mag_info(parser):
    """ """
    parser.add_argument(
        "--mag_type",
        type=str,
        help="magnitude type",
    )
    parser.add_argument(
        "--mag_author",
        type=str,
        help="magnitude author ",
    )
    return parser


def phase_list(parser):
    """ """
    parser.add_argument(
        "--min_phase",
        type=str,
        help="min defining phase ",
    )
    parser.add_argument(
        "--max_phase",
        type=str,
        help="max defining phase ",
    )
    return parser


def outfile(parser):
    """ """
    parser.add_argument(
        "-o",
        "--outfile",
        type=pathlib.Path,
        help="File in which to save structured results. "
        "If omitted, results are printed to standard output.",
    )
    return parser


def hypo_region(parser):
    """ """
    parser.add_argument(
        "--search_region",
        default="global",
        type=str,
        help="Search Region options\n"
        "global [DEFAULT]\n"
        "rect [Bottom Latitude (-90 to 90)] "
        "[Top Latitude -90 to 90)] [Left Longitude -180 to 180] "
        "[Right Longitude -180 to 180]\n"
        "circ [Central Latitude (-90 to 90)] [Central Longitude -180 to 180] "
        "[Radius (deg/km]]\n"
        "seis_region [Seismic region number (1 to 50)]"
        "geo_region [Geographic region number (1 to 757]]",
    )
    return parser


def hypo_review(parser):
    """ """
    parser.add_argument(
        "--reviewed",
        action="store_true",
        help="Reviewed ISC Bulletin",
    )
    return parser


def hypo_nulls(parser):
    """ """
    parser.add_argument(
        "--include_null_depth",
        action="store_true",
        help="include unknown depths ",
    )
    parser.add_argument(
        "--include_null_mag",
        action="store_true",
        help="include unknown magnitudes ",
    )
    parser.add_argument(
        "--include_null_phs",
        action="store_true",
        help="include unknown phases ",
    )
    return parser


def hypo_prime(parser):
    """ """
    parser.add_argument(
        "--only_prime_hypo",
        action="store_true",
        help="include  ",
    )
    return parser


def hypo_misc(parser):
    """ """

    parser.add_argument(
        "--include_phases",
        action="store_true",
        help="include phases ",
    )
    parser.add_argument(
        "--include_magnitudes",
        action="store_true",
        help="include  ",
    )
    parser.add_argument(
        "--include_weblinks",
        action="store_true",
        help="include  ",
    )
    parser.add_argument(
        "--include_headers",
        action="store_true",
        help="include  ",
    )
    parser.add_argument(
        "--include_comments",
        action="store_true",
        help="include ",
    )
    return parser


def bibli_region(parser):
    """ """
    # TODO: format shape input to read shape and coords
    parser.add_argument(
        "--shape",
        type=str,
        help="Shape and coordinates e.g.: ...",
    )
    return parser


def bibli_sort(parser):
    """ """
    # TODO: lookup sort_by options
    parser.add_argument(
        "--sort_by",
        default="day",
        type=str,
        help="Sort by e.g.: ...",
    )
    return parser


def bibli_pub_info(parser):
    """ """
    # TODO: check that year is correct format
    parser.add_argument(
        "--published_min_year",
        default="",
        type=str,
        help="search parameter, " "in YYYY (e.g. 2020).",
    )
    # TODO: check that year is correct format
    parser.add_argument(
        "--published_max_year",
        default="",
        type=str,
        help="search parameter, " "in YYYY (e.g. 2021).",
    )
    parser.add_argument(
        "--publisher",
        default="",
        type=str,
        help="search parameter, " " (e.g. BSSA).",
    )
    parser.add_argument(
        "--published_author",
        default="",
        type=str,
        help="search parameter, " " (e.g. Warren).",
    )

    return parser
