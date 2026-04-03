import telebot
from flask import Flask
import threading

# 🔑 Replace with your bot token
TOKEN = "8677219552:AAHiJMXb3fg0RWDozvyyuN9od0XTpE7_Jno"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🧠 Store data per user
user_notes = {}
user_quiz = {}

# ------------------ START ------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "📚 Study Assistant Bot\n\n"
        "Commands:\n"
        "/add <notes>\n"
        "/flashcards\n"
        "/quiz\n"
        "/next"
    )

# ------------------ ADD NOTES ------------------

@bot.message_handler(commands=['add'])
def add_notes(message):
    text = message.text.replace("/add", "").strip()

    if not text:
        bot.reply_to(message, "Send notes after /add")
        return

    user_notes[message.from_user.id] = text
    bot.reply_to(message, "Notes saved ✅")

# ------------------ FLASHCARDS ------------------

@bot.message_handler(commands=['flashcards'])
def flashcards(message):
    notes = user_notes.get(message.from_user.id)

    if not notes:
        bot.reply_to(message, "No notes found. Use /add first.")
        return

    sentences = [s.strip() for s in notes.split(".") if len(s.strip()) > 5]

    for s in sentences:
        bot.send_message(message.chat.id, f"Q: {s}?\nA: {s}")

# ------------------ QUIZ ------------------

@bot.message_handler(commands=['quiz'])
def quiz(message):
    notes = user_notes.get(message.from_user.id)

    if not notes:
        bot.reply_to(message, "Add notes first using /add")
        return

    sentences = [s.strip() for s in notes.split(".") if len(s.strip()) > 5]

    if not sentences:
        bot.reply_to(message, "No valid content found")
        return

    user_quiz[message.from_user.id] = sentences

    bot.send_message(message.chat.id, f"Q: {sentences[0]}?")

# ------------------ NEXT QUESTION ------------------

@bot.message_handler(commands=['next'])
def next_q(message):
    quiz_list = user_quiz.get(message.from_user.id)

    if not quiz_list:
        bot.reply_to(message, "Start quiz first using /quiz")
        return

    if len(quiz_list) > 1:
        quiz_list.pop(0)
        bot.send_message(message.chat.id, f"Q: {quiz_list[0]}?")
    else:
        bot.send_message(message.chat.id, "Quiz finished ✅")

# ------------------ FALLBACK ------------------

@bot.message_handler(func=lambda msg: True)
def fallback(message):
    bot.reply_to(message, "Use /add, /flashcards, /quiz, /next")

# ------------------ FLASK ------------------

@app.route('/')
def home():
    return "Study Bot Running"

# ------------------ BOT THREAD ------------------

def run_bot():
    print("Bot polling started...")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

# ------------------ SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
