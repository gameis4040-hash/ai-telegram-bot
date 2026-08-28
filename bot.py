import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from brain import get_answer

TOKEN = os.environ["BOT_TOKEN"]

# --- health check server (keeps Render happy + gives cron-job a URL to ping) ---
def run_health_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")

    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# ... rest of your bot.py unchanged


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Ask me anything.\nI can also browse the web for current info 🔍"
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thinking = await update.message.reply_text("Thinking... 🤔")
    try:
        reply = await asyncio.to_thread(get_answer, update.message.text)
    except Exception:
        reply = "⚠️ Something went wrong. Try again."
    await thinking.edit_text(reply[:4096])


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
