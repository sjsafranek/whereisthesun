from datetime import datetime, timezone
from math import radians, sin, cos, asin, sqrt

from astral import Observer
from astral.sun import elevation


def is_day(lat, lon, when, threshold_deg=-0.833):
    when = when or datetime.now(timezone.utc)
    return elevation(Observer(latitude=lat, longitude=lon), when) > threshold_deg


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))

