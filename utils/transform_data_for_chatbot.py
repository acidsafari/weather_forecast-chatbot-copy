# Importing packages
from utils.make_urls import *
from utils.get_forecasts import *
from itertools import chain
import pandas as pd
# libraries used for functional testing
from pprint3x import pprint

"""
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
"""


def extract_raw_data(raw_data: dict) -> list:
    """
    Extracting and renaming raw data from the OpenWeatherAPI response list for each of the nested dictionaries,
    returning a time filtered selection of features in a list of nested dictionaries for each location.
    Function to be used in bronze_forecast_data, which iterates and repacks through the OpenWeatherAPI response list.
    It overrides issues encountered due to copy/view processing error prompts.
    NOTE: Creating a single step function, instead of complicating it with nested loops.

    :param raw_data: the list of nested json (dict) formatted OpenWeatherAPI responses from the GetWeatherRequests.
    :return forecast_list: a list of each of the forecasts made for 12:00:00
    """

    if raw_data['city'] != 'Sorry, something went wrong':
        i = 1
        forecast_list = []
        while i < raw_data['cnt']:
            weather_items = {'city': raw_data['city']['name'],
                             'date_time': raw_data['list'][i]['dt_txt'],
                             'date': raw_data['list'][i]['dt_txt'][0:10],
                             'time': raw_data['list'][i]['dt_txt'][11:],
                             'temperature': round(raw_data['list'][i]['main']['temp'], 1),
                             'maximum_temp': round(raw_data['list'][i]['main']['temp_max'], 1),
                             'minimum_temp': round(raw_data['list'][i]['main']['temp_max'], 1),
                             'weather': raw_data['list'][i]['weather'][0]['main'],
                             'weather_description': raw_data['list'][i]['weather'][0]['description']}
            if weather_items['time'] == '12:00:00':
                forecast_list.append(weather_items)
                i += 1
            else:
                i += 1
        return forecast_list
    else:
        return [raw_data]


def bronze_forecast_data(raw_data: list) -> list:
    """
    Function that loops through the list of raw data from the OpenWeatherAPI response list of nested dictionaries,
    returning a list of nested dictionaries for each of the 5-day forecasts for each city.
    NOTE - This function was necessary to be able to re-package the required data, without encountering copy/view
    processing error, in which we did not know if the result was either.

    :param raw_data: list of nested json (dict) formatted OpenWeatherAPI responses from the GetWeatherRequests.
    :return repacked_data: list of nested dictionaries for each of the 5-day forecasts for each city.
    """
    i = 0
    data = []
    while i < len(raw_data):
        data.append(extract_raw_data(raw_data[i]))
        i += 1

    # Flattening the output
    repacked_data = list(chain(*data))

    return repacked_data


"""
# EXTRACTING DATA FROM RAW
bronze_forecast_data = bronze_forecast_data(raw_forecast_data)
# print(bronze_forecast_data)
"""


def silver_forecast_data(extracted_data: list) -> pd.DataFrame:
    """
    Function that resets the possible changes (observed) on the city names made by the returned request.
    Articulates the data in a DataFrame format, in order to perform other transformations.
    Creates a forecast day column for NLP use.
    Drops unused columns.

    :param extracted_data: extracted data from the raw request data.
    :ivar city_list: list with the city name as per the original input.
    :ivar forecast_days: list with NLP format forecast day.
    :return df: a dataframe with the data we need to answer chatbot questions.
    """
    df = pd.DataFrame(extracted_data)
    # I am sure there is a better way to code this!
    city_list_50 = ['Cumbria', 'Cumbria', 'Cumbria', 'Cumbria', 'Cumbria',
                    'Corfe Castle', 'Corfe Castle', 'Corfe Castle', 'Corfe Castle', 'Corfe Castle',
                    'The Cotswolds', 'The Cotswolds', 'The Cotswolds', 'The Cotswolds', 'The Cotswolds',
                    'Cambridge', 'Cambridge', 'Cambridge', 'Cambridge', 'Cambridge',
                    'Bristol', 'Bristol', 'Bristol', 'Bristol', 'Bristol',
                    'Oxford', 'Oxford', 'Oxford', 'Oxford', 'Oxford',
                    'Norwich', 'Norwich', 'Norwich', 'Norwich', 'Norwich',
                    'Stonehenge', 'Stonehenge', 'Stonehenge', 'Stonehenge', 'Stonehenge',
                    'Watergate Bay', 'Watergate Bay', 'Watergate Bay', 'Watergate Bay', 'Watergate Bay',
                    'Birmingham', 'Birmingham', 'Birmingham', 'Birmingham', 'Birmingham']
    city_list_40 = ['Cumbria', 'Cumbria', 'Cumbria', 'Cumbria',
                    'Corfe Castle', 'Corfe Castle', 'Corfe Castle', 'Corfe Castle',
                    'The Cotswolds', 'The Cotswolds', 'The Cotswolds', 'The Cotswolds',
                    'Cambridge', 'Cambridge', 'Cambridge', 'Cambridge',
                    'Bristol', 'Bristol', 'Bristol', 'Bristol',
                    'Oxford', 'Oxford', 'Oxford', 'Oxford',
                    'Norwich', 'Norwich', 'Norwich', 'Norwich',
                    'Stonehenge', 'Stonehenge', 'Stonehenge', 'Stonehenge',
                    'Watergate Bay', 'Watergate Bay', 'Watergate Bay', 'Watergate Bay',
                    'Birmingham', 'Birmingham', 'Birmingham', 'Birmingham']

    forecast_days_50 = ['1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days',
                        '1 day', '2 days', '3 days', '4 days', '5 days']
    forecast_days_40 = ['1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days',
                        '1 day', '2 days', '3 days', '4 days']

    # column 0 = 'city'
    if extracted_data[0] != 'Sorry, something went wrong':
        if len(df) == 40:
            df['city'] = city_list_40
        else:
            df['city'] = city_list_50

        if len(df) == 40:
            df['day'] = forecast_days_40
        else:
            df['day'] = forecast_days_50

        df.drop(columns=['date_time', 'time'], axis=1, inplace=True)

        return df

    else:
        df['day'] = forecast_days_50

        df.drop(columns=['date_time', 'time'], axis=1, inplace=True)

        return df


# SAVING FILE TO CSV
# forecasts_df.to_csv('/Users/samuelklettnavarro/Dropbox/PY4E/pyCharm/COS60016/chatbot/training_data/weather_forecast.csv')

# print(forecasts_df.columns)
"""
# TRANSFORMING DATA
silver_forecast_data = silver_forecast_data(bronze_forecast_data)
# print(silver_forecast_data.head(1))
"""


def q_and_a_generator(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates a number of desired
    questions and answers to train the chatbot.
    NOTE - The chatbot responds better to completely formulated questions and answers.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q1 = f"What is the weather in {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q1)
        a1 = f"The weather in {data.iloc[i, 0]} looks like {data.iloc[i, -2]} with {data.iloc[i, 2]} C"
        q_and_a_list.append(a1)
        q2 = f"What is the forecast for {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q2)
        a2 = f"The forecast for {data.iloc[i, 0]} is {data.iloc[i, -3]} with a maximum of {data.iloc[i, 3]} C"
        q_and_a_list.append(a2)
        q3 = f"What will be the weather at {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q3)
        a3 = f"It looks like it is going to be {data.iloc[i, -2]} with {data.iloc[i, 2]} C of temperature in {data.iloc[i, 0]}"
        q_and_a_list.append(a3)
        q4 = f"How hot will it be in {data.iloc[i, -1]} in {data.iloc[i, 0]}?"
        q_and_a_list.append(q4)
        a4 = f"The maximum temperature for {data.iloc[i, 0]} is {data.iloc[i, 3]} C in {data.iloc[i, -1]}"
        q_and_a_list.append(a4)
        i += 1

    return q_and_a_list


def q_and_a_generator_1(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for What is the weather in [city] in [days]? to train the chatbot.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q1 = f"What is the weather in {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q1)
        a1 = f"The weather in {data.iloc[i, 0]} looks like {data.iloc[i, -2]} with {data.iloc[i, 2]} C"
        q_and_a_list.append(a1)
        i += 1

    return q_and_a_list


def q_and_a_generator_2(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for - What is the forecast for {city} in {days}? to train the chatbot.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q2 = f"What is the forecast for {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q2)
        a2 = f"The forecast for {data.iloc[i, 0]} is {data.iloc[i, -3]} with a maximum of {data.iloc[i, 3]} C"
        q_and_a_list.append(a2)
        i += 1

    return q_and_a_list


def q_and_a_generator_3(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for - What will be the weather at {city} in {days}?.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q3 = f"What will be the weather at {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q3)
        a3 = f"It looks like it is going to be {data.iloc[i, -2]} with {data.iloc[i, 2]} C of temperature in {data.iloc[i, 0]}"
        q_and_a_list.append(a3)
        i += 1

    return q_and_a_list


def q_and_a_generator_4(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for - How hot will it be in {city} in {days}?.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q4 = f"How hot will it be in {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q4)
        a4 = f"The maximum temperature for {data.iloc[i, 0]} is {data.iloc[i, 3]} C in {data.iloc[i, -1]}"
        q_and_a_list.append(a4)
        i += 1

    return q_and_a_list


def q_and_a_generator_5(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for - What is the maximum temperature at {city} in {days}?.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q5 = f"What is the maximum temperature at {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q5)
        a5 = f"The maximum temperature for {data.iloc[i, 0]} is {data.iloc[i, 3]} C in {data.iloc[i, -1]}"
        q_and_a_list.append(a5)
        i += 1

    return q_and_a_list


def q_and_a_generator_6(data: pd.DataFrame) -> list:
    """
    This function takes the weather information for the DataFrame and generates questions and answers
    for - What is the minimum temperature at {city} in {days}?.

    :param data: the DataFrame curated on the
    :return q_and_a_list:
    """
    q_and_a_list = []
    i = 0
    while i < len(data):
        q6 = f"What is the minimum temperature at {data.iloc[i, 0]} in {data.iloc[i, -1]}?"
        q_and_a_list.append(q6)
        a6 = f"The minimum temperature for {data.iloc[i, 0]} is {data.iloc[i, 4]} C in {data.iloc[i, -1]}"
        q_and_a_list.append(a6)
        i += 1

    return q_and_a_list

"""
# GENERATING DATA READY FOR LIST TRAINING
training_data_list = q_and_a_generator(silver_forecast_data)
print(training_data_list)
"""


