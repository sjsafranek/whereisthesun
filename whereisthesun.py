from geocoder import forward_geocode
from geocoder import reverse_geocode
from geodata import fetch_cities
from geoutils import is_daytime
from geoutils import haversine_km
from weather import fetch_weather


# 1. Candidate cities, nearest first, daylight only (cheap local check)
def fetch_candidate_cities(lat, lon, when=None, min_population=50_000):
    candidates = []
    cities = fetch_cities()
    for city in cities:
        if city["population"] < min_population:
            continue
        if not is_daytime(city["latitude"], city["longitude"], when):
            continue
        city = dict(city, distance_km=haversine_km(lat, lon, city["latitude"], city["longitude"]))
        candidates.append(city)
    candidates.sort(key=lambda city: city["distance_km"])
    return candidates


def find_closest_sunny_city(lat, lon, batch_size=50, max_cloud_cover=30, min_population=50_000, when=None):
    """
    Closest city that is in daylight, has cloud cover <= max_cloud_cover (%),
    and no current precipitation.
    """
    
    # 1. Candidate cities, nearest first, daylight only (cheap local check)
    cities = fetch_candidate_cities(lat, lon, when=when, min_population=min_population)

    # 2. Check weather in batches, walking outward until one qualifies
    for i in range(0, len(cities), batch_size):
        batch = cities[i:i + batch_size]
        for city, weather in zip(batch, fetch_weather(batch)):
            if (
                weather["is_day"] == 1
                and weather["cloud_cover"] <= max_cloud_cover
                and weather["precipitation"] == 0
            ):
                return {
                    "name": city["name"],
                    "country": city["countrycode"],
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "distance_km": round(city["distance_km"], 1),
                    "weather": weather
                }
    return None


def find_closest_sunny_cities(lat, lon, batch_size=50, limit=1, max_cloud_cover=30, min_population=50_000, when=None):
    """
    Closest city that is in daylight, has cloud cover <= max_cloud_cover (%),
    and no current precipitation.
    """
    
    # 1. Candidate cities, nearest first, daylight only (cheap local check)
    cities = fetch_candidate_cities(lat, lon, when=when, min_population=min_population)

    # 2. Check weather in batches, walking outward until one qualifies
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
                    "country": city["countrycode"],
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "distance_km": round(city["distance_km"], 1),
                    "weather": weather
                })
                if limit <= len(results):
                    return results[0:limit]
    return results