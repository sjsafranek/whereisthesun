import logging

import cache
import openmetro
import openweathermap


class Weather(object):

    def __init__(self, data):
        self.data = data   

    def toDict(self):
        return self.data


class OpenWeatherMapWeather(Weather):
    def __init__(self, data):
        self.data = data

    @property
    def source(self):
        return "OpenWeatherMap"

    @property
    def cloud_cover(self):
        return self.data["clouds"]["all"]
    
    @property
    def precipitation(self):
        return self.data.get("rain", {}).get("1h", 0.0)


class OpenMetroWeather(Weather):
    def __init__(self, data):
        self.data = data

    @property
    def source(self):
        return "OpenMetro"

    @property
    def cloud_cover(self):
        return self.data["cloud_cover"]
    
    @property
    def precipitation(self):
        return self.data["precipitation"]


def _getCurrentWeather(location):
    if openweathermap.isEnabled():
        weather = openweathermap.getCurrentWeather(location)
        if weather:
            weather['_source'] = "OpenWeatherMap"
            return OpenWeatherMapWeather(weather)

    weather = openmetro.getCurrentWeather(location)
    if weather:
        weather['_source'] = "OpenMetro"
        return OpenMetroWeather(weather)

    return None


def getCurrentWeather(location):
    lat = location['latitude']
    lon = location['longitude']
    key = f'weather:{lat},{lon}'

    # Check cache for existing response
    item = cache.get(key)
    if item:
        logging.debug(f"Recieved weather from cache for Location({lat},{lon})")
        if "_source" in item:
            if "OpenMetro" == item["_source"]:
                return OpenMetroWeather(item)
            elif "OpenWeatherMap" == item["_source"]:
                return OpenWeatherMapWeather(item)

    # Fetch weather from api
    weather = _getCurrentWeather(location)
    if not weather:
    	return None

    # Cache the response
    cache.set(key, weather.data)

    return weather

