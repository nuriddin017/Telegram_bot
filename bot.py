from flask import Flask, request
import telebot
from dotenv import load_dotenv
import os
from app.handlers import register_handlers

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

register_handlers(bot)

@app.route('/', methods=['GET'])
def index():
    return 'Bot ishga tushdi!'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.data.decode("utf-8"))
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid content type', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
