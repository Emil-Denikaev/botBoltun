import json
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters

config_file = open("big_bot_config.json", "r")
BOT_CONFIG = json.load(config_file)

X = []
y = []

for name, data in BOT_CONFIG["intents"].items():
    for example in data['examples']:
        X.append(example)
        y.append(name)

vectorizer = CountVectorizer()
vectorizer.fit(X)

vecX = vectorizer.transform(X)

# model = LogisticRegression()
# model.fit(vecX, y)
#
# test = vectorizer.transform(["меньше чем за миллион я не согласился бы"])
# model.predict(test)
#
# model.score(vecX, y)
#
# y_pred = model.predict(vecX)

model = RandomForestClassifier()
model.fit(vecX, y)

# model.predict(vectorizer.transform(["меньше чем за миллион я не согласился бы"]))

model.score(vecX, y)
BOT_KEY = '#'

upd = Updater(BOT_KEY)

def filter(text):
    alphabet = 'абвгджзеёийклмнопрстуфхцчшщьыъэюя -'
    result = [c for c in text if c in alphabet]  # Фильтрует символы не входящие в список
    return ''.join(result)


# Если текст похож на example то вернуть "True", "False"
def match(text, example):
    text = filter(text.lower())
    example = example.lower()

    distance = nltk.edit_distance(text, example) / len(example)  # 0..1+
    return distance < 0.6


def get_intent(text):
    for intent in BOT_CONFIG["intents"]:
        for example in BOT_CONFIG["intents"][intent]["examples"]:
            if match(text, example):
                return intent


def bot(text):
    intent = get_intent(text)  # Пытаемся сходу понять намерение

    if not intent:  # Если не получилось, привлекаем модель МО
        transformed_text = vectorizer.transform([text])
        intent = model.predict(transformed_text)[0]

    if intent:  # Если намерение найдено - выдаем случайный ответ
        return random.choice(BOT_CONFIG["intents"][intent]["examples"])

    # Если не найдено
    return random.choice(BOT_CONFIG["failure_phrases"])


def botReactOnMessage(update: Update, context):
    text = update.message.text
    print(f"[user]: {text}")
    reply = bot(text)
    update.message.reply_text(reply)


handler = MessageHandler(Filters.text, botReactOnMessage)
upd.dispatcher.add_handler(handler)

upd.start_polling()
upd.idle()
