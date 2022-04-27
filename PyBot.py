import random
import nltk

BOT_CONFIG = {
    "hello": {
        "examples": ["Приветик", "Шалом", "Здравствуйте", "Салютики", "Хеллоу", "Здарова"],
        "responses": ["Приветик", "Шалом", "Здравствуйте", "Салютики", "Хеллоу", "Здарова"],
    },
    "how-do-you-do": {
        "examples": ["Как дела?", "Чем занят?", "Как ты?"],
        "responses": ["Отдыхаю", "Нормас", "Отлично"],
    },
    "buy": {
        "examples": ["Пока", "Досвидос", "Бай", "До свидания"],
        "responses": ["Пока", "Досвидос", "Бай", "Удачи!", "До свидания"],
    },
}


def filter(text):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя -'
    result = [c for c in text if c in alphabet]
    return ''.join(result)


def match(text, example):
    text = filter(text.lower())
    example = filter(example.lower())
    distance = nltk.edit_distance(text, example) / len(example)
    return distance < 0.6


def get_answer(text):
    for intent in BOT_CONFIG:
        for example in BOT_CONFIG[intent]["examples"]:
            if match(text, example):
                return random.choice(BOT_CONFIG[intent]["responses"])


text = input()
answer = get_answer(text)
print(answer)
