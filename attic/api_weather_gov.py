import requests


def getCurrentWeather(location):
    headers = {
        "User-Agent": "(WhereIsTheSun, sjsafranek@gmail.com)",
        "Accept": "application/geo+json"
    }

    lat = location['latitude']
    lon = location['longitude']

    # 1. Get the observation stations list URL for the coordinates
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_data = requests.get(points_url, headers=headers).json()
    if 200 != points_data.get('status', 200):
        # print(points_data)
        return None
    stations_url = points_data["properties"]["observationStations"]

    # 2. Get the closest station ID
    stations_data = requests.get(stations_url, headers=headers).json()
    if 200 != stations_data.get('status', 200):
        # print(stations_data)
        return None    
    closest_station_id = stations_data["features"][0]["properties"]["stationIdentifier"]

    # 3. Get the latest weather observation from that station
    latest_obs_url = f"https://api.weather.gov/stations/{closest_station_id}/observations/latest"
    weather_data = requests.get(latest_obs_url, headers=headers).json()
    if 200 != weather_data.get('status', 200):
        # print(weather_data)
        return None
    props = weather_data["properties"]

    # 4. Get current condition
    return props


