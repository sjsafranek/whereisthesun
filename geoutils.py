from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
from math import radians, sin, cos, asin, sqrt

from astral import Observer
from astral.sun import elevation
from astral import LocationInfo
from astral.sun import sun



def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))



def is_daytime(lat, lon, timezone, verbose=False):
    """
    Returns True if it is currently daytime at the given lat/long, 
    and False if it is nighttime.
    """
    # 1. Create a dummy location container for the coordinates
    location = LocationInfo(latitude=lat, longitude=lon, timezone=timezone)
    
    # 2. Get the current time in UTC
    now = datetime.now(ZoneInfo(timezone))
    
    try:
        # 3. Calculate astronomical event times (sunrise, sunset, etc.) for today
        sun_events = sun(location.observer, date=now.date(), tzinfo=location.timezone)
        
        # 4. Extract sunrise and sunset (returned as UTC-aware datetimes)
        # We strip the timezone info to easily compare with our naive UTC datetime
        sunrise = sun_events['sunrise']
        sunset = sun_events['sunset']

        # if verbose:
        #     print(sunrise.strftime("%m/%d/%Y %H:%M:%S"), now.strftime("%m/%d/%Y %H:%M:%S"), sunset.strftime("%m/%d/%Y %H:%M:%S"))
        #     print(sunrise <= now <= sunset)

        if sunrise > sunset:
            sunset = sunset + timedelta(days=1)
            
        # 5. It is daytime if the current time is between sunrise and sunset
        return sunrise <= now <= sunset
        
    except ValueError as err:
        print(err)
        
        # This exception happens in Polar regions when the sun doesn't rise or set
        # We check the sun's altitude to see if it is polar day or polar night
        sun_altitude = elevation(location.observer, current_time_utc)
        return sun_altitude > 0

