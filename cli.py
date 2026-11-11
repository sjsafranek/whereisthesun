import json
import argparse

from geocoder import forward_geocode
from geocoder import reverse_geocode
from whereisthesun import find_closest_sunny_cities


if "__main__" == __name__:
    
    parser = argparse.ArgumentParser(description="A simple CLI tool greeting users.")
    parser.add_argument("location", help="Your location")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()

    location = args.location

    origin = forward_geocode(location)
    
    result = find_closest_sunny_cities(origin['latitude'], origin['longitude'])[0]
    print(json.dumps(result))




'''

py -3.15 cli.py 'Springfield, Oregon'

'''


