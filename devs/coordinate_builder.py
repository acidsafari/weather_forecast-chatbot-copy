# Creating a CoordinateBuilder class

# Importing libraries
import requests
from pprint3x import pprint
from api_keys import my_api_keys

# Creating variables
GeoCoding_API_key = my_api_keys()
GeoCoding_API_key = GeoCoding_API_key["GeoCoding_API_key"]
"""
OpenWeather_API_key = "insert you api here"  # WILL REQUIRE API KEY
"""
location_list = ['change for your location list']  # WILL REQUIRE LOCATION LIST


class CoordinateBuilder:
    """
    A name to coordinate class utilising GeoCoding API from Google consisting on a single method

     :param locations: list of the location names to retrieve the coordinates
     :ivar resp_google: contains the results of the GET request

    """
    def lat_long_location_dict(self, locations: list) -> dict:
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
                return resp_google.status_code

        api_ready_loc = {locations[i]: loc_coord[i] for i in range(len(locations))}

        return api_ready_loc


"""
# Running Test Data
my_locations = CoordinateBuilder()
pprint(my_locations.location_dict(locationlist))

"""