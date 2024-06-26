# Importing libraries
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from nltk.corpus import stopwords
# Importing packages
from utils.api_keys import my_api_keys
from utils.make_urls import *
from utils.get_forecasts import *
from utils.transform_data_for_chatbot import *
import pandas as pd

# GATHERING WEATHER DATA
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

# gathering RAW the data from OpenWeather_API request/s
raw_forecast_data = make_forecast_requests(weather_urls)

# EXTRACTING DATA FROM RAW
bronze_forecast_data = bronze_forecast_data(raw_forecast_data)

# TRANSFORMING DATA
silver_forecast_data = silver_forecast_data(bronze_forecast_data)

# GENERATING DATA READY FOR LIST TRAINING
qanda_1 = q_and_a_generator_1(silver_forecast_data)
qanda_2 = q_and_a_generator_2(silver_forecast_data)
qanda_3 = q_and_a_generator_3(silver_forecast_data)
qanda_4 = q_and_a_generator_4(silver_forecast_data)
qanda_5 = q_and_a_generator_5(silver_forecast_data)
qanda_6 = q_and_a_generator_6(silver_forecast_data)
# The longer training list seems to provide worst responses
# weather_training_data_list = q_and_a_generator(silver_forecast_data)


# Create a chatbot instance
my_bot = ChatBot(
    name="WeatherBot",
    read_only=True,
    logic_adapters=[  # "chatterbot.comparisons.LevenshteinDistance",
                      # 'chatterbot.logic.TimeLogicAdapter',
                    "chatterbot.logic.BestMatch"]
)

# Training data
small_talk = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]


# Training the bot
list_trainer = ListTrainer(my_bot)

for item in (small_talk,
             qanda_1, qanda_2, qanda_3, qanda_4, qanda_5, qanda_6  # ,
            # weather_training_data_list
             ):
    list_trainer.train(item)

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english'  # ,
                     # "chatterbot.corpus.english.greetings",
                     # "chatterbot.corpus.english.conversations"
                     )


# Create a webpage and run this chatbot
app = Flask(__name__)
app.static_folder = "static"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get("msg")

    return str(my_bot.get_response(user_text))


if __name__ == "__main__":
    app.run(debug=True)

