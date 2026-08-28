import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from brain import get_answer

TOKEN = os.environ["BOT_TOKEN"]

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
