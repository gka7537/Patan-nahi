import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_album, is_user_verified
from render_keep_alive import keep_alive 

app = Client("my_bot", 
             api_id=int(os.environ.get("API_ID")), 
             api_hash=os.environ.get("API_HASH"), 
             bot_token=os.environ.get("BOT_TOKEN"))

# --- ADMIN UPLOAD HANDLER ---
@app.on_message(filters.media_group & filters.user(int(os.environ.get("ADMIN_ID"))))
async def handle_album(client, message):
    files = []
    thumb = None
    try:
        if message.document and message.document.thumbs:
            thumb = message.document.thumbs[0].file_id
        elif message.video and message.video.thumbs:
            thumb = message.video.thumbs[0].file_id
    except:
        thumb = None

    async for msg in client.get_media_group(message.chat.id, message.id):
        files.append({
            "file_id": msg.document.file_id if msg.document else msg.video.file_id,
            "name": msg.document.file_name if msg.document else "Video",
            "size": msg.document.file_size if msg.document else msg.video.file_size
        })
    
    await add_album(message.media_group_id, files)
    link = f"{os.environ.get('SHORTENER_URL')}/verify?id={message.media_group_id}"
    
    if thumb:
        await client.send_photo(message.chat.id, photo=thumb, caption=f"✅ Album Saved!\n[Click here]({link})")
    else:
        await message.reply(f"✅ Album Saved!\n[Click here]({link})", disable_web_page_preview=True)

# --- START COMMAND ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome! Main ek file streaming bot hoon. \n\nAdmin ki files access karne ke liye mujhe follow karein.")

# --- GET FILE HANDLER ---
@app.on_message(filters.command("get") & filters.private)
async def get_file(client, message):
    if await is_user_verified(message.from_user.id):
        await message.reply("✅ Aap verified hain! \n\n_Note: Yeh link 1 ghante tak valid hai._", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Video", url="YOUR_STREAMING_URL")]]))
    else:
        link = f"{os.environ.get('SHORTENER_URL')}/verify?user={message.from_user.id}"
        await message.reply("❌ Aap verified nahi hain. \n\nAccess ke liye yahan click karein:", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Verify Now", url=link)]]))

if __name__ == "__main__":
    keep_alive()
    app.run()
  
