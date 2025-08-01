from telebot import TeleBot
from app.storage import user_data
from app.sheets import add_user_data 

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        user_data[chat_id] = {}
        bot.send_message(chat_id, "Assalomu alaykum Innovate IT School rasmiy botiga xush kelibsiz!\n"
                                  "Bu bot sizga har kunlik farzandingizning davomati va natijalari haqida xabar beradi.")
        bot.send_message(chat_id, "Bot sizga aniq ma'lumotlarni jo'natishi uchun iltimos, farzandingiz ma'lumotlarini to‘ldiring.")
        bot.send_message(chat_id, "1. Farzandingiz familiyasi va ismi?")
        user_data[chat_id]["step"] = "name"

    @bot.message_handler(func=lambda msg: msg.text == "✏️ Ma'lumotlarni tahrirlash")
    def edit_info(msg):
        chat_id = msg.chat.id
        user_data[chat_id]["step"] = "name"
        bot.send_message(chat_id, "1. Farzandingiz familiyasi va ismi?")

    @bot.message_handler(func=lambda m: True)
    def collect_info(m):
        chat_id = m.chat.id
        if chat_id not in user_data:
            bot.send_message(chat_id, "Iltimos /start buyrug‘ini bosing.")
            return

        step = user_data[chat_id].get("step")

        if step == "name":
            user_data[chat_id]["name"] = m.text
            user_data[chat_id]["step"] = "school"
            bot.send_message(chat_id, "2. Farzandingiz tahsil olayotgan maktab?")
        elif step == "school":
            user_data[chat_id]["school"] = m.text
            user_data[chat_id]["step"] = "grade"
            bot.send_message(chat_id, "3. Farzandingiz sinfi?")
        elif step == "grade":
            user_data[chat_id]["grade"] = m.text
            user_data[chat_id]["step"] = "address"
            bot.send_message(chat_id, "4. Farzandingiz yashash manzili?")
        elif step == "address":
            user_data[chat_id]["address"] = m.text
            user_data[chat_id]["step"] = "phone"
            bot.send_message(chat_id, "5. Siz bilan bog‘lanish uchun telefon raqamingiz?")
        elif step == "phone":
            user_data[chat_id]["phone"] = m.text
            user_data[chat_id]["telegram_id"] = chat_id
            # SHEETGA YOZISH UCHUN QO‘SHILDI:
            add_user_data(user_data[chat_id])
            msg_text = f"""✅ Ma'lumotlar qabul qilindi!
👤 Ism: {user_data[chat_id]['name']}
🏫 Maktab: {user_data[chat_id]['school']}
📚 Sinf: {user_data[chat_id]['grade']}
🏠 Manzil: {user_data[chat_id]['address']}
📞 Tel: {user_data[chat_id]['phone']}
🆔 Telegram ID: {user_data[chat_id]['telegram_id']}
"""
            bot.send_message(chat_id, msg_text)
            bot.send_message(chat_id, "✏️ Ma'lumotlaringizda xatolik bo‘lsa, iltimos \"✏️ Ma'lumotlarni tahrirlash\" tugmasini bosing.", 
                             reply_markup=generate_edit_button())
            user_data[chat_id]["step"] = "done"
        else:
            bot.send_message(chat_id, "Ma'lumotlar allaqachon to‘plangan. Rahmat!")

def generate_edit_button():
    from telebot.types import ReplyKeyboardMarkup, KeyboardButton
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("✏️ Ma'lumotlarni tahrirlash"))
    return markup
