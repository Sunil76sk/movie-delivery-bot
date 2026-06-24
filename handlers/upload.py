from pyrogram import Client, filters
from pyrogram.types import Message
from database import movies_db
from config import STORAGE_CHANNEL_ID, BACKUP_CHANNEL_ID, ADMIN_IDS
from utils.helpers import format_file_size

upload_states = {}


@Client.on_message(filters.command("uploadmovie") & filters.private & filters.user(ADMIN_IDS))
async def upload_handler(client: Client, message: Message):
    user_id = message.from_user.id
    upload_states[user_id] = {"step": "poster"}
    await message.reply_text("📤 **Upload Movie**\n\nStep 1/7: Send the movie poster image.")


@Client.on_message(filters.photo & filters.private & filters.user(ADMIN_IDS))
async def receive_poster(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in upload_states or upload_states[user_id].get("step") != "poster":
        return
    upload_states[user_id]["poster_file_id"] = message.photo.file_id
    upload_states[user_id]["step"] = "file"
    await message.reply_text("Step 2/7: Send the movie file (MP4, MKV, AVI, ZIP, PDF).")


@Client.on_message(filters.document & filters.private & filters.user(ADMIN_IDS))
async def receive_movie_file(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in upload_states or upload_states[user_id].get("step") != "file":
        return
    file = message.document
    upload_states[user_id]["file_id"] = file.file_id
    upload_states[user_id]["file_unique_id"] = file.file_unique_id
    upload_states[user_id]["file_size"] = format_file_size(file.file_size)
    upload_states[user_id]["step"] = "title"
    await message.reply_text("Step 3/7: Send the movie name.")


@Client.on_message(filters.text & filters.private & filters.user(ADMIN_IDS))
async def receive_text_input(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in upload_states:
        return
    state = upload_states[user_id]
    text = message.text

    if state["step"] == "title":
        state["title"] = text
        state["step"] = "language"
        await message.reply_text("Step 4/7: Send the language.")
    elif state["step"] == "language":
        state["language"] = text
        state["step"] = "year"
        await message.reply_text("Step 5/7: Send the release year.")
    elif state["step"] == "year":
        state["year"] = text
        state["step"] = "genre"
        await message.reply_text("Step 6/7: Send the genre.")
    elif state["step"] == "genre":
        state["genre"] = text
        state["step"] = "rating"
        await message.reply_text("Step 7/7: Send the rating.")
    elif state["step"] == "rating":
        state["rating"] = text
        await complete_upload(client, message, user_id)


async def complete_upload(client: Client, message: Message, user_id: int):
    state = upload_states[user_id]

    file_msg = await client.send_document(chat_id=STORAGE_CHANNEL_ID, document=state["file_id"], caption=state["title"])
    await client.send_document(chat_id=BACKUP_CHANNEL_ID, document=state["file_id"], caption=state["title"])

    movie_data = {
        "_id": str(file_msg.id),
        "title": state["title"],
        "language": state["language"],
        "year": state["year"],
        "genre": state["genre"],
        "rating": state["rating"],
        "poster_file_id": state.get("poster_file_id"),
        "movie_file_id": file_msg.id,
        "file_unique_id": state["file_unique_id"],
        "file_size": state["file_size"]
    }

    await movies_db.add_movie(movie_data)
    await message.reply_text(f"✅ **Movie Uploaded!**\n\n🎬 {state['title']}\nID: `{file_msg.id}`")
    del upload_states[user_id]
