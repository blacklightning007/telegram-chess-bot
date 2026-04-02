import telebot
from flask import Flask
import threading

TOKEN = "8750289393:AAGRLZCFmEhrpnnpHXrdptm8EXarGyptH_E"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ---- Telegram Commands ----
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is live 🚀")

# ---- Flask route (for Render) ----
@app.route('/')
def home():
    return "Bot is running"

# ---- Run bot in separate thread ----
def run_bot():
    print("Bot polling started...")
    bot.polling()

threading.Thread(target=run_bot).start()

# ---- Run web server ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
