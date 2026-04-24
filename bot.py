async def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("TOKEN MISSING")
        return

    # Use a fresh application build
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- Oasiso_bot STARTING UP ---")
    
    async with application:
        await application.initialize()
        await application.start()
        # 'drop_pending_updates=True' clears the queue of old messages
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the process alive
        while True:
            await asyncio.sleep(10)
            logger.info("Bot is active and waiting for a message...")
