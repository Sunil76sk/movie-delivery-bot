import asyncio
import logging
import os
from pyrogram import Client, idle

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

import handlers.start
import handlers.upload
import handlers.callbacks


async def main():
    logger.info("Starting Movie Delivery Bot...")
    await app.start()
    logger.info("Bot started successfully!")
    me = await app.get_me()
    logger.info(f"Bot username: @{me.username}")
    await idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
