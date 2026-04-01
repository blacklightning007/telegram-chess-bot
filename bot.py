import telebot
import chess

# 🔑 Telegram Bot Token
import os
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# ♟️ Chess board
board = chess.Board()

# 🤖 Chess engine (use your correct path)

# ⚙️ Hardware toggle
USE_HARDWARE = False   # change to True when Pico is connected


# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am your chess bot 🤖♟️")


# /help command
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "Commands:\n/start\n/help\n/move E2 E4")


# ♟️ Move command
@bot.message_handler(commands=['move'])
def move_handler(message):
    try:
        parts = message.text.split()

        if len(parts) != 3:
            bot.reply_to(message, "Usage: /move E2 E4")
            return

        from_pos = parts[1].lower()
        to_pos = parts[2].lower()

        move = chess.Move.from_uci(from_pos + to_pos)

        # ✅ Validate move
        if move in board.legal_moves:
            board.push(move)

            bot.reply_to(message, f"Your move: {from_pos.upper()} → {to_pos.upper()} ♟️")

            # 🧠 Engine move


            if engine_move:
                board.push(chess.Move.from_uci(engine_move))

                bot.send_message(message.chat.id, f"Bot plays: {engine_move.upper()} 🤖")
                bot.send_message(message.chat.id, str(board))

                # 🎯 Hardware / Simulation layer
                if USE_HARDWARE:
                    # (future Pico communication)
                    print(f"[HARDWARE] Send: {from_pos}->{to_pos}")
                    print(f"[HARDWARE] Send: {engine_move}")
                else:
                    # current simulation
                    print(f"[SIMULATION] Player move: {from_pos} -> {to_pos}")
                    print(f"[SIMULATION] Bot move: {engine_move}")

        else:
            bot.reply_to(message, "Invalid move ❌")

    except Exception as e:
        bot.reply_to(message, "Error processing move")
        print(e)


print("Bot is running...")
bot.polling()
