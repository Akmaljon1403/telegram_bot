import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = '7481666323:AAFk2IL8E7dzFRJPhCs119VrtuvxaMjkjm4'
ADMIN_USERS = ['@dr_muzaffarovna2309', '@MrCandidus']
CONFIRMATION_ADMIN_ID = 5648060455  # @dr_muzaffarovna2309 user_id

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Buyurtma berish", "Tariflar")
    markup.row("Loyiha haqida", "Bog‘lanish")
    bot.send_message(message.chat.id, "Xush kelibsiz! Quyidagilardan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "Buyurtma berish":
        user_data[message.chat.id] = {}
        msg = bot.send_message(message.chat.id, "Tabrik qilinadigan odamning ismini yozing:", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_receiver_name)
    elif message.text == "Tariflar":
        tarif_text = (
            "📦 *Tariflar bilan tanishing*:\n\n"
            "*ODDIY TABRIK*\n"
            "💲 4️⃣0️⃣ ming SO'M\n"
            "🎶🔕  Qo'shiqsiz, faqat tabrik\n"
            "⏳ Davomiyligi: 5 daqiqa\n\n"
            "*TABRIK ➕*\n"
            "💲 5️⃣0️⃣ ming SO'M\n"
            "🎶🔉 Ohirida go'zal qo'shiq bilan\n"
            "⏳ Davomiyligi: 10–15 daqiqa\n\n"
            "*TABRIK PRO*\n"
            "💲 5️⃣0️⃣ ming SO'M\n"
            "📝 O'ziga xos: Chat el davlatlariga tabrik (🇷🇺 🇹🇩 🇩🇪 🌎)\n\n"
            "*VIDEO TABRIK*\n"
            "💲 7️⃣0️⃣ ming SO'M\n"
            "📸 Video montaj (siz xohlagan uslubda)\n"
        )
        bot.send_message(message.chat.id, tarif_text, parse_mode="Markdown")
    elif message.text == "Bog‘lanish":
        bot.send_message(message.chat.id, "Qo'shimcha ma'lumotlar uchun bog'laning: @MrCandidus")
    elif message.text == "Loyiha haqida":
        bot.send_message(message.chat.id, "Bu loyiha orqali sizga onlayn audio/video tabriklar tayyorlab beramiz.")
    else:
        bot.send_message(message.chat.id, "Iltimos, menyudan tanlang.")

def process_receiver_name(message):
    user_data[message.chat.id]['receiver_name'] = message.text
    msg = bot.send_message(message.chat.id, "Tabrik qilinadigan odamning telefon raqamini kiriting:")
    bot.register_next_step_handler(msg, process_receiver_phone)

def process_receiver_phone(message):
    user_data[message.chat.id]['receiver_phone'] = message.text
    msg = bot.send_message(message.chat.id, "Ismingizni kiriting:")
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    user_data[message.chat.id]['sender_name'] = message.text
    msg = bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:")
    bot.register_next_step_handler(msg, process_phone)

def process_phone(message):
    user_data[message.chat.id]['sender_phone'] = message.text
    msg = bot.send_message(message.chat.id, "Tabrik sanasini kiriting (masalan: 2025-05-10):")
    bot.register_next_step_handler(msg, process_date)

def process_date(message):
    user_data[message.chat.id]['date'] = message.text
    msg = bot.send_message(message.chat.id, "Endi tarifni tanlang:", reply_markup=tarif_buttons())
    bot.register_next_step_handler(msg, process_tarif)

def process_tarif(message):
    user_data[message.chat.id]['tarif'] = message.text
    if message.text == "ODDIY TABRIK":
        user_data[message.chat.id]['price'] = "40,000 SO'M"
    elif message.text == "TABRIK ➕":
        user_data[message.chat.id]['price'] = "50,000 SO'M"
    elif message.text == "TABRIK PRO":
        user_data[message.chat.id]['price'] = "50,000 SO'M"
    elif message.text == "VIDEO TABRIK":
        user_data[message.chat.id]['price'] = "70,000 SO'M"

    pay_text = (
        f"Siz tanlagan tarif: {message.text}\n"
        f"To‘lov summasi: {user_data[message.chat.id]['price']}\n"
        "Iltimos, to‘lovni quyidagi karta raqamiga amalga oshiring:\n"
        "`9860 1601 3285 5794 Muslimaxon Tojiyeva`\n\n"
        "To‘lovni amalga oshirgach, chekning rasmini yuboring:"
    )
    bot.send_message(message.chat.id, pay_text, parse_mode="Markdown")
    bot.register_next_step_handler(message, wait_for_receipt)

def wait_for_receipt(message):
    if message.content_type in ['photo', 'document']:
        user_data[message.chat.id]['receipt'] = message
        bot.forward_message(CONFIRMATION_ADMIN_ID, message.chat.id, message.message_id)
        confirm_text = (
            f"Buyurtma so‘rovi:\n\n"
            f"Tabriklanadigan: {user_data[message.chat.id]['receiver_name']}\n"
            f"Telefon: {user_data[message.chat.id]['receiver_phone']}\n"
            f"Buyurtmachi: {user_data[message.chat.id]['sender_name']}\n"
            f"Tel: {user_data[message.chat.id]['sender_phone']}\n"
            f"Sabab: {user_data[message.chat.id]['reason']}\n"
            f"Tabrik sanasi: {user_data[message.chat.id]['date']}\n\n"
            f"Tarif: {user_data[message.chat.id]['tarif']}\n"
            f"To‘lov summasi: {user_data[message.chat.id]['price']}\n\n"
            f"Quyidagi chekka tasdiq bering:"
        )
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("✅ Tasdiqlayman", "❌ Rad etaman")
        bot.send_message(CONFIRMATION_ADMIN_ID, confirm_text, reply_markup=markup)
        user_data[message.chat.id]['waiting_confirmation'] = True
    else:
        msg = bot.send_message(message.chat.id, "Iltimos, faqat to‘lov chekini rasm yoki fayl ko‘rinishida yuboring:")
        bot.register_next_step_handler(msg, wait_for_receipt)

@bot.message_handler(func=lambda m: m.chat.id == CONFIRMATION_ADMIN_ID and m.text in ["✅ Tasdiqlayman", "❌ Rad etaman"])
def handle_confirmation(m):
    for uid in user_data:
        if user_data[uid].get('waiting_confirmation'):
            if m.text == "✅ Tasdiqlayman":
                bot.send_message(uid, "Buyurtmangiz qabul qilindi. Tez orada aloqaga chiqamiz.", reply_markup=main_menu())
                text = (
                    "Yangi buyurtma (tasdiqlandi):\n\n"
                    f"Tabriklanadigan: {user_data[uid]['receiver_name']}\n"
                    f"Telefon: {user_data[uid]['receiver_phone']}\n"
                    f"Buyurtmachi: {user_data[uid]['sender_name']}\n"
                    f"Tel: {user_data[uid]['sender_phone']}\n"
                    f"Sabab: {user_data[uid]['reason']}\n"
                    f"Tabrik sanasi: {user_data[uid]['date']}\n"
                    f"Tarif: {user_data[uid]['tarif']}\n"
                    f"To‘lov summasi: {user_data[uid]['price']}\n"
                )
                for admin in ADMIN_USERS:
                    bot.send_message(admin, text)
            else:
                bot.send_message(uid, "Chek rad etildi. Iltimos, soxta chek ko‘rsatmang.")
            user_data[uid]['waiting_confirmation'] = False
            break

def tarif_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("ODDIY TABRIK", "TABRIK ➕")
    markup.row("TABRIK PRO", "VIDEO TABRIK")
    return markup

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Buyurtma berish", "Tariflar")
    markup.row("Loyiha haqida", "Bog‘lanish")
    return markup

print("Bot ishga tushdi...")
bot.polling(non_stop=True, interval=0, timeout=10)