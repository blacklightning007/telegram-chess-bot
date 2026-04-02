import telebot
from flask import Flask
import threading
import chess
import random
import chess.svg
import cairosvg

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

# 🖼️ Send board with highlight
def send_board_image(chat_id, board, last_move=None):
    try:
        if last_move:
            svg_data = chess.svg.board(
                board=board,
                fill={
                    last_move.from_square: "#aaffaa",
                    last_move.to_square: "#ffaaaa"
                }
            )
        else:
            svg_data = chess.svg.board(board=board)

        cairosvg.svg2png(bytestring=svg_data, write_to="board.png")

        with open("board.png", "rb") as photo:
            bot.send_photo(chat_id, photo)

    except Exception as e:
        print("Image error:", e)
        bot.send_message(chat_id, str(board))  # fallback

# 🧠 Game status
def check_game_status(chat_id, board):
    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        bot.send_message(chat_id, f"🏁 Checkmate! {winner} wins!")
    elif board.is_stalemate():
        bot.send_message(chat_id, "🤝 Stalemate! It's a draw.")
    elif board.is_check():
        bot.send_message(chat_id, "⚠️ Check!")

# ------------------ COMMANDS ------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chess bot ready ♟️\nUse /move E2 E4")

@bot.message_handler(commands=['reset'])
def reset(message):
    board = chess.Board()

    # 🔴 Force white turn (safety)
    board.turn = chess.WHITE

    user_boards[message.from_user.id] = board

    bot.reply_to(message, "Game reset ♟️")
    send_board_image(message.chat.id, board)

@bot.message_handler(commands=['move'])
def move_handler(message):
    try:
        print("Received move:", message.text)

        parts = message.text.split()

        if len(parts) != 3:
            bot.reply_to(message, "Usage: /move E2 E4")
            return

        board = get_board(message.from_user.id)

        # 🔴 Turn check
        if board.turn != chess.WHITE:
            bot.reply_to(message, "Wait for your turn ⏳")
            return

        from_pos = parts[1].lower()
        to_pos = parts[2].lower()

        move = chess.Move.from_uci(from_pos + to_pos)

        if move not in board.legal_moves:
            bot.reply_to(message, "Invalid move ❌")
            return

        # ✅ Player move
        board.push(move)

        bot.reply_to(
            message,
            f"Your move: {from_pos.upper()} → {to_pos.upper()} ♟️"
        )

        check_game_status(message.chat.id, board)

        # 🤖 AI move
        if not board.is_game_over():
            ai_move = random.choice(list(board.legal_moves))
            board.push(ai_move)

            bot.send_message(
                message.chat.id,
                f"Bot plays: {str(ai_move).upper()} 🤖"
            )

            check_game_status(message.chat.id, board)

            send_board_image(message.chat.id, board, ai_move)
        else:
            send_board_image(message.chat.id, board, move)

    except Exception as e:
        print("Move error:", e)
        bot.reply_to(message, "Error processing move ❌")

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
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

# ------------------ SERVER ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
