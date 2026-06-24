from pyrogram import Client, filters
from pyrogram.types import Message
from database import users_db, movies_db
from utils.buttons import get_force_join_buttons
from utils.filters import check_channel_membership
from utils.helpers import create_movie_caption
from utils.buttons import get_movie_buttons


WELCOME_TEXT = (
    "🎬 **Welcome to Movie Delivery Bot!**\n\n"
    "Send me a movie name or use inline search to find movies.\n"
    "Join our channels to download."
)


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await users_db.add_user(user_id, username)

    if len(message.command) > 1:
        movie_id = message.command[1]
        membership = await check_channel_membership(client, user_id)
        if not membership["both"]:
            await message.reply_text(
                "⚠️ **Please join our channels first.**",
                reply_markup=get_force_join_buttons()
            )
            return
        movie = await movies_db.get_movie(movie_id)
        if not movie:
            await message.reply_text("❌ Movie not found.")
            return
        caption = create_movie_caption(movie)
        if movie.get("poster_file_id"):
            await message.reply_photo(photo=movie["poster_file_id"], caption=caption, reply_markup=get_movie_buttons(movie_id))
        else:
            await message.reply_text(caption, reply_markup=get_movie_buttons(movie_id))
        return

    await message.reply_text(WELCOME_TEXT)
