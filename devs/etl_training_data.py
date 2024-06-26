# Importing packages
from utils.make_urls import *
from utils.get_forecasts import *
from utils.transform_data_for_chatbot import *
from pprint3x import pprint
from itertools import chain
import pandas as pd

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

# gathering all the data from OpenWeather_API request/s
raw_forecast_data = make_forecast_requests(weather_urls)
# pprint(raw_forecast_data)


# Creating a standard ETL class
class TrainingDataETL:
    """
    An ETL class for a weather chatbot

     :param : json_file: the json formatted response from the GetWeatherRequests
     :ivar : resp: contains the results of the GET request
     :ivar : forecast_list: list containing forecasts dictionaries elements
    """

    # Inserting a method to make the request
    def etlessl_forecast_data(self, json_file):
        """
        Extracting and transforming the data from json_file.

        :param json_file: the json formatted OpenWeatherAPI response from the GetWeatherRequests
        :return forecast_list: a list of each of the forecasts made for 12:00:00
        """

        if json_file['city'] != 'Sorry, something went wrong':
            i = 1
            forecast_list = []
            while i < json_file['cnt']:
                weather_items = {'city': json_file['city']['name'],
                                 'date_time': json_file['list'][i]['dt_txt'],
                                 'date': json_file['list'][i]['dt_txt'][0:10],
                                 'time': json_file['list'][i]['dt_txt'][11:],
                                 'temperature': round(json_file['list'][i]['main']['temp'], 1),
                                 'maximum_temp': round(json_file['list'][i]['main']['temp_max'], 1),
                                 'minimum_temp': round(json_file['list'][i]['main']['temp_max'], 1),
                                 'weather': json_file['list'][i]['weather'][0]['main'],
                                 'weather_description': json_file['list'][i]['weather'][0]['description']}
                if weather_items['time'] == '12:00:00':
                    forecast_list.append(weather_items)
                    i += 1
                else:
                    i += 1
            return forecast_list
        else:
            return [json_file]


# Transforming the data and repacking it to be able to compile
frcsts = 0
forecast_data = []
while frcsts < len(raw_forecast_data):
    et_data = TrainingDataETL()
    frcsts_data = et_data.etlessl_forecast_data(raw_forecast_data[frcsts])
    forecast_data.append(frcsts_data)
    frcsts += 1

# print(forecast_data)


# Flattening the output
forecast_data_ready = list(chain(*forecast_data))
pprint(forecast_data_ready)
print(len(forecast_data_ready))

df = pd.read_csv('/training_data/weather_forecast.csv')
print(df.shape)
print(df.head())

"""
# THESE FUNCTIONS DO THE SAME THAN THE CLASS AND THE WHILE LOOP ABOVE
# Testing the functions
forecast_data_ready = repack_forecast_data(raw_forecast_data)
print(forecast_data_ready)
"""

# EXTRA DATA MANIPULATION
forecasts_df = pd.DataFrame(forecast_data_ready)

# Resetting the locations as per the original list # SORRY I COULD NOT MAKE THIS PRETTIER SettingWithCopyWarning
city_list = ['Cumbria', 'Cumbria', 'Cumbria', 'Cumbria', 'Cumbria',
             'Corfe Castle', 'Corfe Castle', 'Corfe Castle', 'Corfe Castle', 'Corfe Castle',
             'The Cotswolds', 'The Cotswolds', 'The Cotswolds', 'The Cotswolds', 'The Cotswolds',
             'Cambridge', 'Cambridge', 'Cambridge', 'Cambridge', 'Cambridge',
             'Bristol', 'Bristol', 'Bristol', 'Bristol', 'Bristol',
             'Oxford', 'Oxford', 'Oxford', 'Oxford', 'Oxford',
             'Norwich', 'Norwich', 'Norwich', 'Norwich', 'Norwich',
             'Stonehenge', 'Stonehenge', 'Stonehenge', 'Stonehenge', 'Stonehenge',
             'Watergate Bay', 'Watergate Bay', 'Watergate Bay', 'Watergate Bay', 'Watergate Bay',
             'Birmingham', 'Birmingham', 'Birmingham', 'Birmingham', 'Birmingham']
forecasts_df['city'] = city_list

# Dropping excess columns
forecasts_df.drop(columns=['date_time', 'time',], axis=1, inplace=True)
print(forecasts_df.head())
# SAVING FILE TO CSV
forecasts_df.to_csv('/Users/samuelklettnavarro/Dropbox/PY4E/pyCharm/COS60016/chatbot/training_data/weather_forecast.csv')

# print(forecasts_df.columns)


