import telebot
from flask import Flask
import threading

# 🔑 Your Telegram Token
TOKEN = "8750289393:AAGRLZCFmEhrpnnpHXrdptm8EXarGyptH_E"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ------------------ COMMANDS ------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is live 🚀")

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.reply_to(message, "Reset done ✅")

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, f"You said: {message.text}")

# ------------------ FLASK ROUTE ------------------

@app.route('/')
def home():
    return "Bot is running"

# ------------------ BOT THREAD ------------------

def run_bot():
    print("Bot polling started...")
    bot.polling()

threading.Thread(target=run_bot).start()

# ------------------ START SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
