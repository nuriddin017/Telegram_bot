from flask import Flask, request
import telebot
from dotenv import load_dotenv
import os

load_dotenv()  # .env faylni yuklaydi
API_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Bot ishga tushdi!'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid content type', 403

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Flask webhook orqali bog‘landim.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
