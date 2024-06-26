# Import statements
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from nltk.corpus import stopwords


# Create a chatbot instance
my_bot = ChatBot(
    name="PyBot",
    read_only=True,
    logic_adapters=["chatterbot.logic.MathematicalEvaluation",
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

math_talk_1 = [
    'pythagorean theorem',
    'a squared plus b squared equals c squared.'
]

math_talk_2 = [
    'law of cosines',
    'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)'
]

# Training the bot
list_trainer = ListTrainer(my_bot)

for item in (small_talk, math_talk_1, math_talk_2):
    list_trainer.train(item)

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')

"""
# Print test iteration
print(my_bot.get_response("Hi"))
print(my_bot.get_response("How are you?"))
print(my_bot.get_response("What is your name?"))
"""

# Chatting with the bot
while True:
    try:
        bot_input = input("You: ")
        bot_response = my_bot.get_response(bot_input)
        print(f"{my_bot.name}: {bot_response}")
    except(KeyboardInterrupt, EOFError, SystemExit):
        break

