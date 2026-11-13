import logging
import requests

import cache
from conf import OPEN_WEATHER_MAP_API_KEY


def isEnabled():
    return None != OPEN_WEATHER_MAP_API_KEY


def getCurrentWeather(location):
    lat = location['latitude']
    lon = location['longitude']

    key = f'{lat},{lon}'
    item = cache.get(key)
    if item:
        logging.debug(f"Getting weather from cache {key}")
        return item

    params = {
    	'lat': lat,
    	'lon': lon,
    	'appid': OPEN_WEATHER_MAP_API_KEY
    }

    logging.debug(f"Getting weather from OpenWeatherMap {key}")
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    data = response.json()

    cache.set(key, data)

    return data

