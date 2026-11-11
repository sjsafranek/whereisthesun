from geopy.geocoders import Nominatim


# Note: Nominatim requires a unique user_agent string to identify your application.
geolocator = Nominatim(user_agent="where_is_the_sun_app")


def forward_geocode(address_string):
    """Converts an address string into latitude and longitude coordinates."""
    # timeout parameter prevents the script from hanging on poor network connections
    location = geolocator.geocode(address_string, timeout=10)
    if location:
        return {
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "raw": location.raw
        }

def reverse_geocode(latitude, longitude):
    """Converts coordinate points back into a human-readable address."""
    location = geolocator.reverse((latitude, longitude), timeout=10)
    if location:
        return {
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "raw": location.raw
        }
