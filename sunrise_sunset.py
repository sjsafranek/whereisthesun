#!/usr/bin/env python3
"""
determine_day_or_night.py

Return whether a given geographic location (latitude, longitude) is currently
day or night using the Sunrise-Sunset API.

Usage:
    python check_day.py <lat> <lng>

Example:
    python check_day.py 37.7749 -122.4194

The script queries https://www.sunrise-sunset.org/api (or a similar public
API) for today's sunrise/sunset times in UTC, then compares the current UTC time
to those values.

Note: The exact query format of the Sunrise-Sunset API may vary; adjust the
URL construction below if you encounter a different response structure.
"""

import sys
import requests
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_BASE_URL = "https://www.sunrise-sunset.org/api"  # <-- verify this URL

# If your API requires an explicit trailing slash or query-parameter order,
# modify the f-string below accordingly.
def build_url(lat: float, lng: float, date: str | None = None) -> str:
    params = {}
    if date is not None:
        params["date"] = date
    url = f"{API_BASE_URL}/json"
    url += f"?lat={lat}&lng={lng}"
    if date is not None:
        url += f"&date={date}"
    return url


def fetch_sunrise_sunset(lat: float, lng: float, date: str | None = None) -> dict:
    """
    Call the Sunrise-Sunset API and return the parsed JSON response.

    Parameters
    ----------
    lat : float
        Latitude of the location (e.g., 37.7749).
    lng : float
        Longitude of the location (e.g., -122.4194).
    date : str, optional
        Date in YYYY-MM-DD format. Defaults to today's date.

    Returns
    ----------
        A dict containing at least 'results' with keys 'sunrise' and 'sunset'.
    """
    url = build_url(lat, lng, date)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to reach Sunrise-Sunset API: {exc}") from exc

    # The response shape varies; support both wrapped and flat structures.
    results = data.get("results", data)
    sunrise_str = results.get("sunrise")
    sunset_str = results.get("sunset")

    if not sunrise_str or not sunset_str:
        raise ValueError(
            f"Unexpected API response: {data}. "
            "Expected 'results' containing 'sunrise' and 'sunset' fields."
        )

    # Strip trailing 'Z' (UTC designator) and replace with '+00:00'
    sunrise_dt = _parse_iso(sunrise_str)
    sunset_dt = _parse_iso(sunset_str)
    return (sunrise_dt, sunset_dt)


def _parse_iso(dt_str):
    """Convert a sunrise/sunset time string into a timezone-aware datetime."""
    dt_str = dt_str.strip()
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    # Handle 12-hour format with AM/PM (e.g., "2:36:26 PM")
    for fmt in ("%I:%M:%S %p", "%H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    # Fall back to the standard ISO-8601 format (e.g., "2024-06-01T04:36:26Z")
    return datetime.fromisoformat(dt_str.replace('+00:00', 'Z'))


def is_day(lat: float, lng: float) -> str:
    """
    Determine whether the current UTC time at the given location is day or night.

    Parameters
    ----------
    lat : float
        Latitude.
    lng : float
        Longitude.

    Returns
    -------
        'day'  if sunrise <= now < sunset (i.e., daylight)
        'night' otherwise
    """
    # Today's date in ISO format (YYYY-MM-DD)
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        sunrise_dt, sunset_dt = fetch_sunrise_sunset(lat, lng, date=today)
    except Exception as exc:
        raise RuntimeError(f"Could not determine day/night for {lat},{lng}: {exc}") from exc

    now_utc = datetime.now(timezone.utc)
    return "day" if sunrise_dt <= now_utc < sunset_dt else "night"


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <latitude> <longitude>")
        sys.exit(1)

    lat_str = sys.argv[1]
    lng_str = sys.argv[2]

    try:
        lat = float(lat_str)
        lng = float(lng_str)
    except ValueError:
        print(f"Error: latitude and longitude must be numeric. Got '{lat_str}', '{lng_str}'")
        sys.exit(1)

    result = is_day(lat, lng)
    print(f"Location ({lat}, {lng}): {'day' if result == 'day' else 'night'}")


if __name__ == "__main__":
    main()
