# Importing packages
import requests
# Libraries from individual testing

# Creating variables
OpenWeather_API_key = "insert you api here"  # WILL REQUIRE API KEY

location_list = ['change for your location list']  # WILL REQUIRE LOCATION LIST

""" # FOR TESTING

# Transforming variables for weather request
my_locations = CoordinateBuilder()
my_locations = dict(my_locations.lat_long_location_dict(location_list))

# Creating URL dictionary
urls = {}

for key, val in my_locations.items():
    weather_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?lat={val['lat']}&lon={val['lng']}&units=metric"
            + "&appid=" + OpenWeather_API_key
    )
    urls[key] = weather_url

pprint(urls)
"""


class GetForecastRequests:  # requests
    """An OpenWeather API requests class

     :param : url the url for the forecast location
     :ivar : resp contains the results of the GET request
     :ivar : forecast_list is a list containing forecasts dictionaries elements
    """
    # Adding some properties in case it errors # Delete them after testing
    def __iter__(self):
        return self

    def __next__(self):
        return self

    def url_dict_for_weather_requests(self, my_locations):
        # Creating URL dictionary
        urls = {}
        for key, val in my_locations.items():
            weather_url = (
                    f"https://api.openweathermap.org/data/2.5/forecast?lat={val['lat']}&lon={val['lng']}&units=metric"
                    + "&appid=" + OpenWeather_API_key
            )
            urls[key] = weather_url

    # Inserting a method to make the request
    def make_get_requests(self, url):
        """
        The forecast json response for each city.

        :param url: the url generated for the location
        :return resp_data: a response in json format or a pre-formatted error response
        """
        # Making the request
        resp = requests.get(url=url)
        # Checking response validity
        if resp.status_code == 200:
            # creating variable holding the response data
            resp_data = resp.json()
            return resp_data
        else:
            # Returning a response with the same post-processing format that comes from using et_weather_data
            return {'city': 'Sorry, something went wrong',
                    'date': '1998-01-01',
                    'time': '12:00:00',
                    'temperature': -50,
                    'maximum_temp': 60,
                    'minimum_temp': -200,
                    'weather': 'we hope it is nice',
                    'weather_description': 'it is the UK after all'
                    }


"""
# FOR TESTING PURPOSES
my_get = GetForecastRequests()
pprint(my_get.make_get_requests(urls["Cumbria"]))

my_get_data = my_get.make_get_requests(urls["Cumbria"])
print(my_get_data)"""
