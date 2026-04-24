import os
import logging
import asyncio
import signal
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Start command received")
    # Your requested welcome message
    welcome_text = "**Oasiso_bot i!**\nSend me a photo and a title to start"
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found!")
        return

    # Initialize the bot
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("--- Oasiso_bot STARTING ---")

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)

    # This is the critical part: This loop keeps the background worker 
    # alive so it NEVER 'exits early'.
    stop_event = asyncio.Event()
    
    # Keep running until the process is killed by Render
    try:
        await stop_event.wait()
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Fatal crash: {e}")
