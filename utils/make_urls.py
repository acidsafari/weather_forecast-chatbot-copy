# Importing libraries
import requests
from pprint3x import pprint
from utils.api_keys import my_api_keys

# Creating variables
api_keys = my_api_keys()
GeoCoding_API_key = api_keys["GeoCoding_API_key"]
OpenWeather_API_key = api_keys["OpenWeather_API_key"]
"""
location_list = ['Cumbria',
                 'Corfe Castle',
                 'The Cotswolds',
                 'Cambridge',
                 'Bristol',
                 'Oxford',
                 'Norwich',
                 'Stonehenge',
                 'Watergate Bay',
                 'Birmingham']
"""


def lat_long_location_dict(locations: list) -> dict:
    """
    A function that requests the latitude and longitude of a list of locations by name.

    :param locations: list of the cities names to retrieve the coordinates for
    :return api_ready_loc: a dictionary of city:latitude,longitude
    """
    # Reformatting the location list to make the Google API call
    gcp_format_locationlist = []

    for loc in locations:
        format_loc = loc.replace(" ", "$")
        gcp_format_locationlist.append(format_loc)

    # Creating a new dictionary with LOCATION:{LAT,LONG} combination
    # list of coordinates
    loc_coord = []

    for gcp_loc in gcp_format_locationlist:
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={gcp_loc}+UK" "&key=" + GeoCoding_API_key
        resp_google = requests.get(geo_url)
        if resp_google.status_code == 200:
            loc_coord.append(resp_google.json()['results'][0]['geometry']['location'])
        else:
            return {locations[i]: {"lat": 0, "long": 0} for i in range(len(locations))}

    api_ready_loc = {locations[i]: loc_coord[i] for i in range(len(locations))}

    return api_ready_loc


def build_urls_for_weather_requests(geo_coord_locations: dict) -> dict:
    """
    Transforms city:lat/long data returned from Google's Geo Coding API and returns a dictionary ready to generate
    OpenWeather API requests.

    :param geo_coord_locations: a dictionary containing city:lat/long data.
    :return urls: a dictionary containing city:OpenWeatherAPI urls ready for requests.
    """
    # Creating URL dictionary
    urls = {}
    for key, val in geo_coord_locations.items():
        weather_url = (
                f"https://api.openweathermap.org/data/2.5/forecast?lat={val['lat']}&lon={val['lng']}&units=metric"
                + "&appid=" + OpenWeather_API_key
        )
        urls[key] = weather_url

    return urls


"""
# Running Test Data
my_locations = lat_long_location_dict(location_list)
my_urls = build_urls_for_weather_requests(my_locations)
pprint(my_locations)
pprint(my_urls)
"""
