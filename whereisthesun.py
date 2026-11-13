import logging
from geodata import fetch_cities
from geoutils import haversine_km
from geoutils import is_daytime
from weather import fetch_weather
import openweathermap


# 1. Candidate cities, nearest first, daylight only (cheap local check)
def fetch_candidate_cities(lat, lon, min_population=50_000, **kwargs):
    candidates = []
    cities = fetch_cities()
    for city in cities:
        if city["population"] <= min_population:
            continue
        if not is_daytime(city["latitude"], city["longitude"], city['timezone']):
            continue
        city = dict(city, distance_km=haversine_km(lat, lon, city["latitude"], city["longitude"]))
        candidates.append(city)
    candidates.sort(key=lambda city: city["distance_km"])
    return candidates


def find_closest_sunny_cities(lat, lon, batch_size=50, limit=1, max_cloud_cover=30, **kwargs):
    """
    Closest city that is in daylight, has cloud cover <= max_cloud_cover (%),
    and no current precipitation.
    """
    
    # 1. Candidate cities, nearest first, daylight only (cheap local check)
    cities = fetch_candidate_cities(lat, lon, **kwargs)

    # 2. OpenWeatherApi :: Fetch weather
    if openweathermap.isEnabled():
        logging.info("Using OpenWeatherApi")
        results = []
        for city in cities:
            weather = openweathermap.getCurrentWeather(city)    
            if not weather:
                continue
            if (
                (weather["clouds"]["all"] <= max_cloud_cover or "Clear" == weather["weather"][0]["main"])
                and 0.0 == weather.get("rain", {}).get("1h", 0.0)
            ):
                results.append({
                    "name": city["name"],
                    "admin1code": city["admin1code"],
                    "country": city["countrycode"],
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "distance_km": round(city["distance_km"], 1),
                    "weather": weather
                })
                if limit <= len(results):
                    return results[0:limit]
        return results

    # 2. OpenMetroApi :: Check weather in batches, walking outward until one qualifies
    results = []
    for i in range(0, len(cities), batch_size):
        batch = cities[i:i + batch_size]
        for city, weather in zip(batch, fetch_weather(batch)):
            if (
                weather["is_day"] == 1
                and weather["cloud_cover"] <= max_cloud_cover
                and weather["precipitation"] == 0
            ):
                results.append({
                    "name": city["name"],
                    "admin1code": city["admin1code"],
                    "country": city["countrycode"],
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "distance_km": round(city["distance_km"], 1),
                    "weather": weather
                })
                if limit <= len(results):
                    return results[0:limit]
    return results

