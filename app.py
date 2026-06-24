import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client(
    "movie_delivery_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

from handlers import (
    start_handler,
    upload_handler,
    force_join_check,
    callback_handler
)

from handlers.start import start_handler, help_handler, search_handler
from handlers.upload import upload_handler, receive_poster, receive_movie_file, receive_text_input, cancel_upload
from handlers.forcejoin import force_join_check
from handlers.callbacks import (
    show_movie,
    download_movie,
    show_analytics,
    delete_movie,
    back_to_menu
)


async def main():
    logger.info("Starting Movie Delivery Bot...")
    await app.start()
    logger.info("Bot started successfully!")
    
    me = await app.get_me()
    logger.info(f"Bot username: @{me.username}")
    
    await asyncio.Event().wait()


if __name__ == "__main__":
    from pyrogram import idle
    
    loop = asyncio.get_event_loop()
    
    async def run():
        await app.start()
        logger.info("Bot is running...")
        await idle()
        await app.stop()
    
    loop.run_until_complete(run())
