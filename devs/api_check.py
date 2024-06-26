import requests
import os
from pprint3x import pprint

api_key = "48da4********"  # Introduce working API key

# api_key = os.environ.get('OpenWeather_API_key')
weather_url = "https://api.openweathermap.org/data/2.5/forecast?lat=51.509865&lon=-0.118092&units=metric"+"&appid="+api_key
# url = f"api.openweathermap.org/data/2.5/forecast/hourly?lat=44.34&lon=10.99&appid=${api_key}"


resp1 = requests.get(weather_url)
pprint(resp1.json())  # "Today's weather in London:",
