import logging
import requests

import cache
from conf import OPEN_WEATHER_MAP_API_KEY


def isEnabled():
    return None != OPEN_WEATHER_MAP_API_KEY


def getCurrentWeather(location): 
    logging.debug(f"Fetching weather from OpenWeatherMap for Location({location['latitude']},{location['longitude']})")
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                            params={
                                'lat': location['latitude'],
                                'lon': location['longitude']   ,
                                'appid': OPEN_WEATHER_MAP_API_KEY
                            })
    if 200 != response.status_code:
        return None
    return response.json()


