from googletrans import Translator
import telebot
import time
import requests
from bs4 import BeautifulSoup


def get_weather(city):
    city = city[0].upper() + city[1:].lower()

    translator = Translator()
    translation = translator.translate(city, dest="en").text
    url = "https://www.google.com/search?q=" + "weather" + translation
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    return temp, str_


token = "7500190044:AAEjms7teDUN-OeYR5IGAZls5y6DeALhrw8"

bot = telebot.TeleBot(token)
cities = {}
current_operation = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "пожалуйста, укажите Ваш населенный пункт с помощью /set_city и включите функцию погоды с помощью /run")

@bot.message_handler(commands=['set_city'])
def set_city(msg0):
    bot.send_message(msg0.chat.id, "введите название населенного пункта")
    current_operation[msg0.chat.id] = 2
    @bot.message_handler(func=lambda aaa: current_operation[msg0.chat.id] == 2)
    def check(msg):
        city = msg.text
        try:
            get_weather(city)
            cities[msg.chat.id] = city
            bot.reply_to(msg, "успешно!")
            current_operation[msg.chat.id] = 0
            return
        except AttributeError:
            bot.reply_to(msg, "город не найден! попробуйте еще раз.")

@bot.message_handler(commands=['run'])
def send(msg0):
    try:
        city = cities[msg0.chat.id]
    except KeyError:
        bot.send_message(msg0.chat.id, "сначала укажите Ваш населенный пункт с помощью /set_city")
        return
    bot.send_message(msg0.chat.id, "введите период отправки погоды в секундах\n(1 час = 3600 сек, 1 день = 86400 сек)")
    current_operation[msg0.chat.id] = 3
    @bot.message_handler(func=lambda aaa: current_operation[msg0.chat.id] == 3)
    def sender(msg):
        try:
            period = int(msg.text)
            bot.send_message(msg.chat.id, "для остановки процесса напишите /cancel")
            current_operation[msg.chat.id] = 1
            city1 = cities[msg.chat.id]
            while current_operation[msg.chat.id] == 1:
                bot.send_message(msg.chat.id, 'на улице: ' + '\n'.join(get_weather(city1)))
                time.sleep(period)
            return

        except ValueError:
            bot.send_message(msg.chat.id, "период - натуральное число секунд без пробелов, запятых, точек, обозначений величины и т.п.")

@bot.message_handler(commands=["cancel"])
def stop(msg):
    current_operation[msg.chat.id] = 0
    bot.send_message(msg.chat.id, "действие отменено")

@bot.message_handler(func=lambda message: (not current_operation[message.chat.id]) if message.chat.id in current_operation.keys() else 1)
def none(msg):
    bot.reply_to(msg, "команда не найдена")


bot.infinity_polling()
