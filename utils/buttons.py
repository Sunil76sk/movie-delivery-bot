from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import MAIN_CHANNEL_ID, BACKUP_JOIN_CHANNEL_ID


def get_force_join_buttons() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📺 Join Main Channel", url=f"https://t.me/+{abs(MAIN_CHANNEL_ID)}")],
        [InlineKeyboardButton("📺 Join Backup Channel", url=f"https://t.me/+{abs(BACKUP_JOIN_CHANNEL_ID)}")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
    ]
    return InlineKeyboardMarkup(buttons)


def get_movie_buttons(movie_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⬇️ Download Movie", callback_data=f"download_{movie_id}")]
    ]
    return InlineKeyboardMarkup(buttons)
