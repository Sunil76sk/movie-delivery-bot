from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from database import movies_db, analytics_db
from config import STORAGE_CHANNEL_ID
from utils.filters import check_channel_membership
from utils.buttons import get_force_join_buttons, get_movie_buttons
from utils.helpers import create_movie_caption


@Client.on_callback_query(filters.regex("^check_membership$"))
async def check_membership_cb(client: Client, callback: CallbackQuery):
    membership = await check_channel_membership(client, callback.from_user.id)
    if membership["both"]:
        await callback.message.edit_text("✅ **Verified!** Use /start to continue.")
    else:
        await callback.answer("Please join both channels first!", show_alert=True)


@Client.on_callback_query(filters.regex("^movie_"))
async def show_movie(client: Client, callback: CallbackQuery):
    movie_id = callback.data.split("_", 1)[1]
    membership = await check_channel_membership(client, callback.from_user.id)
    if not membership["both"]:
        await callback.message.edit_text("⚠️ **Join our channels first.**", reply_markup=get_force_join_buttons())
        return
    movie = await movies_db.get_movie(movie_id)
    if not movie:
        await callback.answer("Movie not found!", show_alert=True)
        return
    await analytics_db.track_view(movie_id, callback.from_user.id)
    await movies_db.increment_views(movie_id)
    caption = create_movie_caption(movie)
    await callback.message.delete()
    if movie.get("poster_file_id"):
        await client.send_photo(chat_id=callback.from_user.id, photo=movie["poster_file_id"], caption=caption, reply_markup=get_movie_buttons(movie_id))
    else:
        await client.send_message(chat_id=callback.from_user.id, text=caption, reply_markup=get_movie_buttons(movie_id))


@Client.on_callback_query(filters.regex("^download_"))
async def download_movie(client: Client, callback: CallbackQuery):
    movie_id = callback.data.split("_", 1)[1]
    membership = await check_channel_membership(client, callback.from_user.id)
    if not membership["both"]:
        await callback.message.edit_text("⚠️ **Join our channels first.**", reply_markup=get_force_join_buttons())
        return
    movie = await movies_db.get_movie(movie_id)
    if not movie:
        await callback.answer("Movie not found!", show_alert=True)
        return
    await callback.answer("Sending movie...", show_alert=False)
    await analytics_db.track_download(movie_id, callback.from_user.id)
    await movies_db.increment_downloads(movie_id)
    try:
        await client.copy_message(chat_id=callback.from_user.id, from_chat_id=STORAGE_CHANNEL_ID, message_id=movie["movie_file_id"])
    except Exception:
        await callback.message.reply_text("❌ Error sending movie. Try again later.")


@Client.on_callback_query(filters.regex("^back_to_menu$"))
async def back_to_menu(client: Client, callback: CallbackQuery):
    await callback.message.edit_text("🎬 **Movie Delivery Bot**\n\nSend /start to begin.")
