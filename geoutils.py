from datetime import datetime
from datetime import timedelta
from datetime import timezone
from math import radians, sin, cos, asin, sqrt

from astral import Observer
from astral.sun import elevation
from astral import LocationInfo
from astral.sun import sun



def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def is_daytime(lat, lon, when=None, verbose=False):
    """
    Returns True if it is currently daytime at the given lat/long, 
    and False if it is nighttime.
    """
    # 1. Create a dummy location container for the coordinates
    location = LocationInfo(latitude=lat, longitude=lon)
    
    # 2. Get the current time in UTC
    # current_time_utc = datetime.utcnow()
    current_time_utc = when or datetime.utcnow()
    
    try:
        # 3. Calculate astronomical event times (sunrise, sunset, etc.) for today
        sun_events = sun(location.observer, date=current_time_utc.date())
        
        # 4. Extract sunrise and sunset (returned as UTC-aware datetimes)
        # We strip the timezone info to easily compare with our naive UTC datetime
        sunrise = sun_events['sunrise'].replace(tzinfo=None)
        sunset = sun_events['sunset'].replace(tzinfo=None)

        if sunrise > sunset:
            sunset = sunset + timedelta(days=1)

        print(sunrise, current_time_utc, sunset)

        # 5. It is daytime if the current time is between sunrise and sunset
        return sunrise <= current_time_utc <= sunset
        
    except ValueError:
        # This exception happens in Polar regions when the sun doesn't rise or set
        # We check the sun's altitude to see if it is polar day or polar night
        sun_altitude = elevation(location.observer, current_time_utc)
        return sun_altitude > 0

