"""
Formatting search and IO paramaters
"""

import argparse
import datetime


def date_fromisoformat(date_string):
    """Return a `datetime.date` corresponding to a string in YYYY-MM-DD format.

    In Python 3.7+, there is `datetime.date.fromisoformat`, but alas - we're
    supporting Python 3.6+.

    :param date_string: A date in the format YYYY-MM-DD.
    :return: A `datetime.date` correspondingo the given date string.
    """
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{date_string}' is not a valid date. Use YYYY-MM-DD."
        )


def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year, month,
    date, hour, and minute values. Additionally, this function provides the date
    in the usual ISO 8601 YYYY-MM-DD format to avoid ambiguities with
    locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")
