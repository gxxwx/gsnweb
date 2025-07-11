import telebot
from telebot import types

API_TOKEN = '8051087916:AAEVUFHTHMHj4KUoDvC0K86m2Bik0qsDitk'
bot = telebot.TeleBot(API_TOKEN)

# Старт и приветствие
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Открыть сбор данных", url="https://YOUR_RENDER_URL/index.html")
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку ниже и разреши сбор данных на сайте.", reply_markup=markup)

# Команда для теста
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Отправь мне команду /start для начала.")

# Приём данных с сайта (через Telegram API нет прямой возможности, 
# мы будем использовать отдельный сервер для приёма и пересылки данных)

# Запуск бота
bot.infinity_polling()
