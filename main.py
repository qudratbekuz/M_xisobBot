import telebot
from telebot import types

TOKEN = '7555424938:AAG4CfKSuJ3Cd4Aq3iE9G_d05mhtFEJ4GH0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📥 Kirim", "📤 Chiqim", "📊 Statistika", "💰 Balans")
    bot.send_message(message.chat.id, "👋 Xush kelibsiz! M_xisobBot ishga tushdi!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.send_message(message.chat.id, f"Siz yubordingiz: {message.text}")

bot.polling()
