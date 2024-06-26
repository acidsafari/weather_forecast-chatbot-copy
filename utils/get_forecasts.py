# Importing packages
import requests
from utils.make_urls import *
# Libraries for functional testing
from pprint3x import pprint

"""
# FOR TESTING PURPOSES
# Creating variables
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

# generating lat/long dictionary with a GeoCoding_API request
geo_locations = lat_long_location_dict(location_list)


# generating urls for OpenWeather_API request
weather_urls = build_urls_for_weather_requests(geo_locations)
"""


def make_forecast_requests(urls: dict) -> list:
    """
    A Function to make OpenWeather_API requests returning a list of nested dictionaries
    of forecast json response/s for each city.

    :param urls: an OpenWeather_API url ready generated for the location/s
    :return raw_forecast_data: a list compiler of the responses in json format or a pre-formatted error response
    """
    # Looping through the urls dict to gather all the training data using GetWeatherRequests class
    raw_forecast_data = []
    for city, url in urls.items():
        # Making each individual request
        resp = requests.get(url=url)
        # Checking response validity
        if resp.status_code == 200:
            # creating variable holding the response data
            resp_data = resp.json()
        else:
            # Returning a response with the same post-processing format that comes from using et_weather_data
            resp_data = {'city': 'Sorry, something went wrong',
                         'date_time': '1998-01-01 12:00:00',
                         'date': '1999-12-31',
                         'time': '12:00:00',
                         'temperature': -50,
                         'maximum_temp': 60,
                         'minimum_temp': -200,
                         'weather': 'we hope it is nice',
                         'weather_description': 'it is the UK after all'
                         }
        # Packing the responses into a list variable
        raw_forecast_data.append(resp_data)

    # Returning the list variable
    return raw_forecast_data


"""
# FOR TESTING PURPOSES
my_forecast_data = make_forecast_requests(weather_urls)
pprint(my_forecast_data)

print(my_forecast_data)
"""
