import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup to monitor the bot in Render's dashboard
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User triggered /start")
    # Updated welcome message about books, flowers, etc.
    welcome_text = "**Oasiso_bot i!**\nSend me a photo and a title to start"
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def health_check():
    """This prints to your Render logs every 10 seconds so you can see it is working."""
    while True:
        logger.info("HEARTBEAT: Oasiso_bot is running...")
        await asyncio.sleep(10)

async def main():
    # Fetch token from Render Environment Variables
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("ERROR: No TELEGRAM_TOKEN found in Render Environment Settings!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Register the /start command
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- Oasiso_bot STARTING UP ---")
    
    # Secure startup for Python 3.14 environments
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the background worker active
        await health_check()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot failed: {e}")
