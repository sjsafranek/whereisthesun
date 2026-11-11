# Where is the Sun

This application helps you find the closest city to a given location that is currently sunny. It provides a web-based interface with an interactive map and a command-line tool for quick lookups.

## Features

-   **Sunny City Finder**: Locates the nearest city with clear skies and no precipitation.
-   **Web Interface**: An interactive map powered by Leaflet that visualizes your location and the found sunny city.
-   **Automatic Geolocation**: Uses the browser's geolocation API to find your current position.
-   **Command-Line Interface (CLI)**: A simple CLI for running a search from your terminal.
-   **Customizable Search**: Adjust parameters like minimum city population, maximum cloud cover, and the number of results.
-   **Efficient Search**: Filters cities by population and daylight before checking weather conditions in batches to minimize API calls.

## How It Works

1.  The application receives a starting latitude and longitude, either from the browser's geolocation feature or from a command-line argument.
2.  It builds a list of candidate cities from the `geonamescache` database, filtering them by a minimum population threshold.
3.  It performs a local, inexpensive check to filter out any cities where it is currently nighttime using the `astral` library.
4.  The remaining cities are sorted by their distance from the starting location using the Haversine formula.
5.  The application then queries the [Open-Meteo API](https://open-meteo.com/) for current weather conditions (cloud cover, precipitation) for the nearest cities in batches.
6.  The first city in the distance-sorted list that meets the "sunny" criteria (daylight, cloud cover below a threshold, and no precipitation) is returned as the result.
7.  The result is either displayed on the web map or printed to the console.

## Getting Started

### Prerequisites

-   Python 3.x
-   A virtual environment tool (e.g., `venv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sjsafranek/whereisthesun.git
    cd whereisthesun
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Application

You can run the application using either the Flask development server or a production-grade server like Gunicorn.

**For development:**

```bash
flask run --host=0.0.0.0 --port=5001
```

Navigate to `http://127.0.0.1:5001` in your web browser. The app will ask for your location to find the nearest sunny spot.

**For production (with Gunicorn):**

```bash
gunicorn --workers 4 --bind 127.0.0.1:5001 app:app
```

### Command-Line Interface (CLI)

Use the CLI to quickly find a sunny city from your terminal. Pass your location as a string argument.

```bash
python cli.py "Springfield, Oregon"
```

The tool will geocode your location, find the closest sunny city, and print the result as a JSON object.

**Example Output:**

```json
{
    "name": "Redding",
    "admin1code": "CA",
    "country": "US",
    "latitude": 40.58654,
    "longitude": -122.39168,
    "distance_km": 305.9,
    "weather": {
        "latitude": 40.583332,
        "longitude": -122.416664,
        "generationtime_ms": 0.0438690185546875,
        "utc_offset_seconds": -25200,
        "timezone": "America/Los_Angeles",
        "timezone_abbreviation": "PDT",
        "elevation": 140.0,
        "time": "2024-05-22T11:00",
        "cloud_cover": 0,
        "precipitation": 0.0,
        "is_day": 1,
        "cloud_cover_unit": "%",
        "precipitation_unit": "mm",
        "is_day_unit": ""
    }
}
```

## API

The application exposes a simple JSON API endpoint to find sunny cities.

### `POST /api/v1/sun`

Finds the closest sunny cities based on the provided coordinates.

**Request Body:**

```json
{
  "params": {
    "latitude": 34.05,
    "longitude": -118.24,
    "min_population": 50000,
    "max_cloud_cover": 25,
    "limit": 1
  }
}
```

**Parameters:**

-   `latitude` (float, **required**): The starting latitude.
-   `longitude` (float, **required**): The starting longitude.
-   `min_population` (integer, optional): The minimum population for a city to be considered. Defaults to `50000`.
-   `max_cloud_cover` (integer, optional): The maximum allowed cloud cover percentage. Defaults to `30`.
-   `limit` (integer, optional): The maximum number of sunny cities to return. Defaults to `1`.

**Success Response (200 OK):**

```json
{
  "status": "ok",
  "data": {
    "cities": [
      {
        "name": "Sunnyvale",
        "admin1code": "CA",
        "country": "US",
        "latitude": 37.36883,
        "longitude": -122.03635,
        "distance_km": 499.7,
        "weather": { ... }
      }
    ]
  }
}
```

**Error Response (4xx/5xx):**

```json
{
  "status": "error",
  "error": {
    "code": 404,
    "message": "Missing Parameter: 'params.latitude'"
  }
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.