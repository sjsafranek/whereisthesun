import logging
import requests


# https://open-meteo.com/en/docs
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def getCurrentWeather(location):
    logging.debug(f"Fetching weather from OpenMetro for Location({location['latitude']},{location['longitude']})")
    response = requests.get(OPEN_METEO_URL, params={
        "latitude": str(location['latitude']),
        "longitude": str(location['longitude']),
        "current": "cloud_cover,precipitation,is_day",
    }, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {
        **{key: value for key, value in data.items() if not isinstance(value, dict)},
        **data['current'], 
        **{f"{key}_unit": value for key, value in data['current_units'].items()}
    }


def getCurrentWeatherForBatch(cities):
    """Current weather for a batch of cities in a single API call."""
    params = {
        "latitude": ",".join(str(city["latitude"]) for city in cities),
        "longitude": ",".join(str(city["longitude"]) for city in cities),
        "current": "cloud_cover,precipitation,is_day",
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    # Open-Meteo returns a dict for one location, a list for several
    if not isinstance(data, list):
        data = [data]
    return [
        {
            **{key: value for key, value in item.items() if not isinstance(value, dict)},
            **item['current'], 
            **{f"{key}_unit": value for key, value in item['current_units'].items()}
        }
        for item in data
    ]

