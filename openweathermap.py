import logging
import requests

import cache
from conf import OPEN_WEATHER_MAP_API_KEY


def isEnabled():
    return None != OPEN_WEATHER_MAP_API_KEY


def getCurrentWeather(location):
    lat = location['latitude']
    lon = location['longitude']

    # Check cache for existing response
    key = f'weather:{lat},{lon}'
    item = cache.get(key)
    if item:
        logging.debug(f"Getting weather from cache: location={lat},{lon}")
        return item

    # Fetch weather from api
    logging.debug(f"Getting weather from OpenWeatherMap: location={lat},{lon}")
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                            params={
                                'lat': lat,
                                'lon': lon,
                                'appid': OPEN_WEATHER_MAP_API_KEY
                            })
    if 200 != response.status_code:
        return None
    data = response.json()

    # Cache the response
    cache.set(key, data)

    return data

