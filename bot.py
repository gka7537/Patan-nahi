import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_album, is_user_verified

app = Client("my_bot", 
             api_id=int(os.environ.get("API_ID")), 
             api_hash=os.environ.get("API_HASH"), 
             bot_token=os.environ.get("BOT_TOKEN"))

SHORTENER_URL = os.environ.get("SHORTENER_URL")

@app.on_message(filters.media_group & filters.user(int(os.environ.get("ADMIN_ID"))))
async def handle_album(client, message):
    files = []
    async for msg in client.get_media_group(message.chat.id, message.id):
        # Thumbnail aur File Details nikalna
        thumb = msg.document.thumbs[0].file_id if msg.document and msg.document.thumbs else None
        files.append({
            "file_id": msg.document.file_id if msg.document else msg.video.file_id,
            "name": msg.document.file_name if msg.document else "Video",
            "size": msg.document.file_size if msg.document else msg.video.file_size
        })
    
    await add_album(message.media_group_id, files)
    link = f"{SHORTENER_URL}/verify?id={message.media_group_id}"
    await message.reply(f"✅ Album Saved!\n[Click here to get link]({link})", disable_web_page_preview=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    if await is_user_verified(message.from_user.id):
        await message.reply("Aap verified hain! Files access kar sakte hain.")
    else:
        link = f"{SHORTENER_URL}/verify?user={message.from_user.id}"
        await message.reply("Access ke liye 24-hours verification complete karein:", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Verify Now", url=link)]]))

app.run()
