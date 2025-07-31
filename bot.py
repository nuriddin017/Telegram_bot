from flask import Flask, request
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Bu yerda foydalanuvchining vaqtincha ma’lumotlarini saqlaymiz
user_data = {}

# START komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Yangi user uchun bo'sh joy
    bot.send_message(chat_id, "Assalomu alaykum Innovate IT School rasmiy botiga xush kelibsiz!\n"
                              "Bu bot sizga har kunlik farzandingizning davomati va natijalari haqida xabar beradi.")
    bot.send_message(chat_id, "Bot sizga aniq ma'lumotlarni jo'natishi uchun iltimos, farzandingiz ma'lumotlarini to‘ldiring.")
    bot.send_message(chat_id, "1. Farzandingiz familiyasi va ismi?")

    # Holatni belgilang – 1-savolga navbat
    user_data[chat_id]["step"] = "name"

# Har qanday xabarni ushlash
@bot.message_handler(func=lambda message: True)
def collect_info(message):
    chat_id = message.chat.id

    # Foydalanuvchi hali start bosmagan bo‘lsa
    if chat_id not in user_data:
        bot.send_message(chat_id, "Iltimos /start buyrug‘ini bosing.")
        return

    step = user_data[chat_id].get("step")

    if step == "name":
        user_data[chat_id]["name"] = message.text
        user_data[chat_id]["step"] = "school"
        bot.send_message(chat_id, "2. Farzandingiz tahsil olayotgan maktab?")
    elif step == "school":
        user_data[chat_id]["school"] = message.text
        user_data[chat_id]["step"] = "grade"
        bot.send_message(chat_id, "3. Farzandingiz sinfi?")
    elif step == "grade":
        user_data[chat_id]["grade"] = message.text
        user_data[chat_id]["step"] = "address"
        bot.send_message(chat_id, "4. Farzandingiz yashash manzili?")
    elif step == "address":
        user_data[chat_id]["address"] = message.text
        user_data[chat_id]["step"] = "phone"
        bot.send_message(chat_id, "5. Siz bilan bog‘lanish uchun telefon raqamingiz?")
    elif step == "phone":
        user_data[chat_id]["phone"] = message.text
        user_data[chat_id]["telegram_id"] = chat_id

        # Barcha ma’lumotlarni ko‘rsatamiz (keyin sheetsga yozamiz)
        summary = f"""✅ Ma'lumotlar qabul qilindi!
👤 Ism: {user_data[chat_id]['name']}
🏫 Maktab: {user_data[chat_id]['school']}
📚 Sinf: {user_data[chat_id]['grade']}
🏠 Manzil: {user_data[chat_id]['address']}
📞 Tel: {user_data[chat_id]['phone']}
🆔 Telegram ID: {user_data[chat_id]['telegram_id']}
"""
        bot.send_message(chat_id, summary)
        user_data[chat_id]["step"] = "done"

    else:
        bot.send_message(chat_id, "Ma'lumotlar allaqachon to‘plangan. Rahmat!")

# Flask route'lar
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
