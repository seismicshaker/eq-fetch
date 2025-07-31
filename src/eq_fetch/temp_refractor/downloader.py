"""Module for Downloading different earthquake catalogs."""

import requests
import logging
from typing import Callable

from eq_fetch import SearchCriteria

logger = logging.getLogger(__name__)


# --- Source handlers ---
def download_isc_event_bibliography(
    params: SearchCriteria, dest_path: str
) -> str | None:
    url = "https://www.isc.ac.uk/event_bibliography/index.php"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded ISC Event Bibliography to {dest_path}")
        return dest_path
    except Exception as e:
        logger.error(f"ISC Event Bibliography download failed: {e}")
        return None


def download_isc_bulletin(params: SearchCriteria, dest_path: str) -> str | None:
    """
    Download ISC Bulletin data.
    params: e.g. {'start_year': 2020, 'end_year': 2022, ...}
    """
    # Example ISC Bulletin URL. Adapt as needed.
    url = "https://www.isc.ac.uk/iscbulletin/search/catalogue/"
    # Typically, these endpoints require POST/GET with specific parameters.
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded ISC Bulletin to {dest_path}")
        return dest_path
    except Exception as e:
        logger.error(f"ISC Bulletin download failed: {e}")
        return None


def download_gcmt(params: SearchCriteria, dest_path: str) -> str | None:
    url = "https://www.globalcmt.org/CMTsearch.html"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded GCMT CMT solutions to {dest_path}")
        return dest_path
    except Exception as e:
        logger.error(f"GCMT download failed: {e}")
        return None


def download_scardec(params: SearchCriteria, dest_path: str) -> str | None:
    url = "http://scardec.projects.sismo.ipgp.fr/"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded SCARDEC source time functions to {dest_path}")
        return dest_path
    except Exception as e:
        logger.error(f"SCARDEC download failed: {e}")
        return None


def download_source(params: SearchCriteria, dest_path: str) -> str | None:
    """Download function Template."""
    url = "url"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded SCARDEC source time functions to {dest_path}")
        return dest_path
    except Exception as e:
        logger.error(f"SCARDEC download failed: {e}")
        return None


# --- Source registry ---
CATALOG_SOURCES: dict[str, Callable[SearchCriteria, str | None]] = {
    "bibli": download_isc_event_bibliography,
    "bulletin": download_isc_bulletin,
    "gcmt": download_gcmt,
    "scardec": download_scardec,
    # "source": download_source,
    # Add more sources here as needed
}


def download_catalog(source: str, params: SearchCriteria, dest_path: str) -> str | None:
    """Download an earthquake catalog from the specified source.

    source: One of the keys in CATALOG_SOURCES.
    params: Source-specific query parameters.
    dest_path: File path to save the result.
    """
    handler = CATALOG_SOURCES.get(source)
    if not handler:
        logger.error(f"Unknown catalog source: {source}")
        return None
    return handler(params, dest_path)
