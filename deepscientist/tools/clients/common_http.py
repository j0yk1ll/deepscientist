import logging
from datetime import datetime
from typing import Optional

import httpx

from ...settings import Settings

logger = logging.getLogger(__name__)


def parse_year_from_iso(date_str: Optional[str]) -> Optional[int]:
    """Parse a year from a variety of ISO-like date strings.

    Handles:
    - YYYY
    - YYYY-MM-DD
    - full ISO timestamps, with or without timezone / 'Z'
    Returns None if parsing fails.
    """
    if not date_str:
        return None
    try:
        ds = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ds)
        return dt.year
    except Exception:
        try:
            return int(date_str[:4])
        except Exception:
            logger.debug(f"Could not parse year from date string: %s", date_str)
            return None


def make_http_client(settings: Optional[Settings] = None) -> httpx.Client:
    """Create a configured httpx.Client for all tools.

    Centralised here so you can tweak timeouts, headers, proxies, etc. in one place.
    """
    effective_settings = settings or Settings()
    return effective_settings.build_client()
