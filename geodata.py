import geonamescache


def fetch_cities():
    return geonamescache.GeonamesCache().get_cities().values()


def get_continents():
    return geonamescache.GeonamesCache().get_continents().values()


def get_countries():
    return geonamescache.GeonamesCache().get_countries().values()


def get_us_counties():
    return geonamescache.GeonamesCache().get_us_counties().values()


def get_us_states():
    return geonamescache.GeonamesCache().get_us_states().values()

