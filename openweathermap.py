import logging
import requests

import cache
from conf import OPEN_WEATHER_MAP_API_KEY


def isEnabled():
    return None != OPEN_WEATHER_MAP_API_KEY


OPEN_WEATHER_MAP_URL = "https://api.openweathermap.org"


def getCurrentWeather(location): 
    logging.debug(f"Fetching weather from OpenWeatherMap for Location({location['latitude']},{location['longitude']})")
    response = requests.get(f"{OPEN_WEATHER_MAP_URL}/data/2.5/weather", 
                            params={
                                'lat': location['latitude'],
                                'lon': location['longitude']   ,
                                'appid': OPEN_WEATHER_MAP_API_KEY
                            })
    if 200 != response.status_code:
        return None
    return response.json()


