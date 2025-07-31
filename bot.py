from flask import Flask, request
import telebot
from dotenv import load_dotenv
import os
from telebot import types

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

# /start va /help uchun reply keyboard tugmalar
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Salom 👋')
    btn2 = types.KeyboardButton('Yordam 🆘')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Salom! Tugmalardan birini tanlang:", reply_markup=markup)

# Oddiy matnli tugmalar bosilganda javob
@bot.message_handler(func=lambda message: message.text == 'Salom 👋')
def greet(message):
    bot.reply_to(message, "Assalomu alaykum! Qanday yordam berishim mumkin?")

@bot.message_handler(func=lambda message: message.text == 'Yordam 🆘')
def help_msg(message):
    bot.reply_to(message, "Buyruqlar ro‘yxati:\n/start - boshlash\n/buttons - inline tugmalar")

# /buttons komandasi uchun inline tugmalar
@bot.message_handler(commands=['buttons'])
def send_inline_buttons(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Saytga kirish", url="https://example.com")
    btn2 = types.InlineKeyboardButton("Bosaman", callback_data="btn_pressed")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Tanlang:", reply_markup=markup)

# Inline tugmalar bosilganda callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "btn_pressed":
        bot.answer_callback_query(call.id, "Tugma bosildi!")
        bot.send_message(call.message.chat.id, "Siz tugmani bosdingiz!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
