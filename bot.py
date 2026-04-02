import telebot
from flask import Flask
import threading
import chess
import random
# 🔑 Your Telegram Token
TOKEN = "8750289393:AAGRLZCFmEhrpnnpHXrdptm8EXarGyptH_E"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🧠 Store board per user
user_boards = {}

def get_board(user_id):
    if user_id not in user_boards:
        user_boards[user_id] = chess.Board()
    return user_boards[user_id]

# ------------------ COMMANDS ------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chess bot ready ♟️\nUse /move E2 E4")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_boards[message.from_user.id] = chess.Board()
    bot.reply_to(message, "Game reset ♟️")

@bot.message_handler(commands=['move'])
def move_handler(message):
    try:
        parts = message.text.split()

        if len(parts) != 3:
            bot.reply_to(message, "Usage: /move E2 E4")
            return

        board = get_board(message.from_user.id)

        # 🔴 Check turn (user always white)
        if board.turn != chess.WHITE:
            bot.reply_to(message, "Wait for your turn ⏳")
            return

        from_pos = parts[1].lower()
        to_pos = parts[2].lower()

        move = chess.Move.from_uci(from_pos + to_pos)

        if move in board.legal_moves:
            board.push(move)

            bot.reply_to(
                message,
                f"Your move: {from_pos.upper()} → {to_pos.upper()} ♟️"
            )

            # 🤖 AI move
            if not board.is_game_over():
                import random
                ai_move = random.choice(list(board.legal_moves))
                board.push(ai_move)

                bot.send_message(
                    message.chat.id,
                    f"Bot plays: {str(ai_move).upper()} 🤖"
                )

            bot.send_message(message.chat.id, str(board))

        else:
            bot.reply_to(message, "Invalid move ❌")

    except Exception as e:
        bot.reply_to(message, "Error processing move")
        print(e)

            # 🤖 AI move (simple)
            if not board.is_game_over():
                ai_move = randome.choice(list(board.legal_moves))  # simple AI
                board.push(ai_move)

                bot.send_message(
                    message.chat.id,
                    f"Bot plays: {str(ai_move).upper()} 🤖"
                )

            bot.send_message(message.chat.id, str(board))

        else:
            bot.reply_to(message, "Invalid move ❌")

    except Exception as e:
        bot.reply_to(message, "Error processing move")
        print(e)

@bot.message_handler(func=lambda msg: True)
def fallback(message):
    bot.reply_to(message, "Use /move E2 E4")

# ------------------ FLASK ------------------

@app.route('/')
def home():
    return "Bot is running"

# ------------------ BOT THREAD ------------------

def run_bot():
    print("Bot polling started...")
    bot.polling()

threading.Thread(target=run_bot).start()

# ------------------ SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
