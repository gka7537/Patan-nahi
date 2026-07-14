import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_file, get_file, add_user_verification, is_user_verified
from utils import format_file_info
from dotenv import load_dotenv

load_dotenv()

app = Client("my_bot", 
             api_id=os.getenv("API_ID"), 
             api_hash=os.getenv("API_HASH"), 
             bot_token=os.getenv("BOT_TOKEN"))

ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_message(filters.document | filters.video & filters.user(ADMIN_ID))
async def handle_uploads(client, message):
    # Auto-generate Link logic
    file_id = message.document.file_id if message.document else message.video.file_id
    file_name = message.document.file_name if message.document else "Video"
    file_size = message.document.file_size if message.document else message.video.file_size
    
    # Database mein save karna
    await add_file(file_id, file_name, file_size)
    
    # Link generate karke bhejna
    short_link = f"{os.getenv('SHORTENER_URL')}/verify?file={file_id}"
    await message.reply(f"✅ File Saved!\nLink: {short_link}")

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if await is_user_verified(user_id):
        await message.reply("Welcome back! You are verified.")
    else:
        await message.reply("Please verify via this link to access files:", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Verify Now", url="YOUR_SHORTENER_LINK")]]))

# 1-Hour Stream Limit logic (middleware concept)
@app.on_message(filters.command("getfile"))
async def get_file_handler(client, message):
    user_id = message.from_user.id
    if not await is_user_verified(user_id):
        return await message.reply("Verify first!")
    
    # File send logic with 1-hour session note
    await message.reply("Here is your file. It will be available for 1 hour.", 
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open File", url="LINK")]]))
    
    # Yahan 1 hour ke baad link expire karne ka logic add hoga
    print(f"User {user_id} started session at {time.time()}")

app.run()

