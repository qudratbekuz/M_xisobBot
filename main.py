import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

TOKEN = '7555424938:AAG4CfKSuJ3Cd4Aq3iE9G_d05mhtFEJ4GH0'
SPREADSHEET_NAME = 'M_xisobBot'
SHEET_KIRIM = 'SHEETS1'
SHEET_CHIQIM = 'SHEETS2'

bot = telebot.TeleBot(TOKEN)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("genuine-plate-461307-u4-b8849574a044.json", scope)
client = gspread.authorize(creds)
sheet_kirim = client.open(SPREADSHEET_NAME).worksheet(SHEET_KIRIM)
sheet_chiqim = client.open(SPREADSHEET_NAME).worksheet(SHEET_CHIQIM)

user_state = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📥 Kirim", "📤 Chiqim")
    markup.add("💰 Balans", "📊 Statistika")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 M_xisobBotga xush kelibsiz!", reply_markup=main_menu())

@bot.message_handler(func=lambda msg: msg.text == "📥 Kirim")
def kirim_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💵 Oylik daromad", "💼 Qo‘shimcha daromad", "📦 Boshqa kirimlar", "🔙 Ortga")
    bot.send_message(message.chat.id, "Kirim turini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "📤 Chiqim")
def chiqim_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍞 Oziq-ovqat", "🏡 Oila uchun", "🚕 Taksi", "🚗 Avtomobil")
    markup.add("💡 Oylik to‘lovlar", "💊 Salomatlik", "🎮 Ko‘ngil ochar")
    markup.add("🎁 Sovgalar/Xayriya", "❓ Boshqa chiqimlar", "🔙 Ortga")
    bot.send_message(message.chat.id, "Chiqim turini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "🔙 Ortga")
def back_handler(message):
    bot.send_message(message.chat.id, "Bosh menyu:", reply_markup=main_menu())

@bot.message_handler(func=lambda msg: msg.text in [
    "💵 Oylik daromad", "💼 Qo‘shimcha daromad", "📦 Boshqa kirimlar"
])
def kirim_turi_tanlandi(message):
    user_state[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Summani va izohni yuboring. (Masalan: `1000000 Oylikdan tushdi`)")

@bot.message_handler(func=lambda msg: msg.text in [
    "🍞 Oziq-ovqat", "🏡 Oila uchun", "🚕 Taksi", "🚗 Avtomobil",
    "💡 Oylik to‘lovlar", "💊 Salomatlik", "🎮 Ko‘ngil ochar", 
    "🎁 Sovgalar/Xayriya", "❓ Boshqa chiqimlar"
])
def chiqim_turi_tanlandi(message):
    user_state[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Summani va izohni yuboring. (Masalan: `50000 Taksiga bordim`)")

@bot.message_handler(func=lambda msg: msg.chat.id in user_state)
def summa_izoh_qabul(message):
    kategoriya = user_state.pop(message.chat.id)
    parts = message.text.strip().split(" ", 1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❗ Format xato. Masalan: `1000000 Oylikdan tushdi`")
        return

    summa, izoh = parts
    try:
        summa_val = int(summa.replace(",", ""))
    except ValueError:
        bot.send_message(message.chat.id, "❗ Son noto‘g‘ri formatda.")
        return

    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
    foydalanuvchi = message.from_user.first_name

    if kategoriya in ["💵 Oylik daromad", "💼 Qo‘shimcha daromad", "📦 Boshqa kirimlar"]:
        sheet_kirim.append_row([foydalanuvchi, kategoriya, izoh, summa_val, "so‘m", sana])
        bot.send_message(message.chat.id, "✅ Kirim yozildi!", reply_markup=main_menu())
    else:
        sheet_chiqim.append_row([foydalanuvchi, kategoriya, izoh, summa_val, "so‘m", sana])
        bot.send_message(message.chat.id, "✅ Chiqim yozildi!", reply_markup=main_menu())

bot.polling()
