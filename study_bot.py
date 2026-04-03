import telebot
from flask import Flask
import threading

# 🔑 Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"

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
        words = s.split()

        if len(words) > 3:
            answer = words[0]
            question = " ".join(["____"] + words[1:])

            bot.send_message(
                message.chat.id,
                f"Q: {question}?\nA: {answer}"
            )

# ------------------ QUIZ ------------------

@bot.message_handler(commands=['quiz'])
def quiz(message):
    notes = user_notes.get(message.from_user.id)

    if not notes:
        bot.reply_to(message, "Add notes first using /add")
        return

    sentences = [s.strip() for s in notes.split(".") if len(s.strip()) > 5]

    quiz_data = []

    for s in sentences:
        words = s.split()
        if len(words) > 3:
            answer = words[0]
            question = " ".join(["____"] + words[1:])
            quiz_data.append((question, answer))

    if not quiz_data:
        bot.reply_to(message, "No valid content")
        return

    user_quiz[message.from_user.id] = quiz_data

    q, _ = quiz_data[0]
    bot.send_message(message.chat.id, f"Q: {q}?")

# ------------------ NEXT ------------------

@bot.message_handler(commands=['next'])
def next_q(message):
    quiz_list = user_quiz.get(message.from_user.id)

    if not quiz_list:
        bot.reply_to(message, "Start quiz first using /quiz")
        return

    if len(quiz_list) > 1:
        quiz_list.pop(0)
        q, _ = quiz_list[0]
        bot.send_message(message.chat.id, f"Q: {q}?")
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
    bot.remove_webhook()   # 🔥 prevents webhook conflict
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

# ------------------ SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
