import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_album, get_album, add_user_verification, is_user_verified
from utils import format_file_info

# Initialize Bot
app = Client("my_bot", 
             api_id=os.getenv("API_ID"), 
             api_hash=os.getenv("API_HASH"), 
             bot_token=os.getenv("BOT_TOKEN"))

ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_message(filters.media_group & filters.user(ADMIN_ID))
async def handle_album(client, message):
    # Album ki sabhi files collect karna
    media_group = await client.get_media_group(message.chat.id, message.id)
    files_list = []
    
    # Pehli file se Thumbnail nikalna
    thumb = media_group[0].thumbs[0].file_id if media_group[0].thumbs else None
    
    for msg in media_group:
        files_list.append({
            "file_id": msg.document.file_id if msg.document else msg.video.file_id,
            "name": msg.document.file_name if msg.document else "Video",
            "size": msg.document.file_size if msg.document else msg.video.file_size
        })
    
    album_id = message.media_group_id
    await add_album(album_id, files_list)
    
    # Final message with Thumbnail and Info
    text = f"✅ **Album Uploaded!**\n\nTotal Files: {len(files_list)}\nClick below to get access."
    await client.send_photo(message.chat.id, photo=thumb, caption=text, 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Link", url=f"YOUR_DOMAIN/verify?id={album_id}")]]))

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if await is_user_verified(message.from_user.id):
        await message.reply("Aap verified hain! Files access karein.")
    else:
        await message.reply("Access ke liye pehle 24 hours ki verification poori karein:", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Verify Now", url="YOUR_SHORTENER_LINK")]]))

@app.on_message(filters.command("get") & filters.private)
async def send_file(client, message):
    user_id = message.from_user.id
    if not await is_user_verified(user_id):
        return await message.reply("❌ Aapka 24 hours ka session khatam ho gaya hai ya aap verify nahi hain.")
    
    # File ke niche note
    await message.reply("📄 **File Name** | **Size**\n\n_Note: Yeh file aapke liye sirf 1 ghante tak valid hai._",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Video", url="YOUR_STREAMING_LINK")]]))

app.run()
