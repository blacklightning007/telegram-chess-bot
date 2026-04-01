import telebot

TOKEN = "YOUR_TOKEN_HERE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is live 🚀")

print("Bot is running...")
bot.polling()
