import motor.motor_asyncio
import os
import time

# Render ke Variables se URI lega
client = motor.motor_asyncio.AsyncMongoClient(os.environ.get("MONGO_URI"))
db = client["file_bot_db"]
files_col = db["files"]
users_col = db["users"]

async def add_album(album_id, files_data):
    await files_col.insert_one({"album_id": album_id, "files": files_data, "time": time.time()})

async def add_user_verification(user_id):
    expiry = time.time() + (24 * 60 * 60) # 24 ghante
    await users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry}}, upsert=True)

async def is_user_verified(user_id):
    user = await users_col.find_one({"user_id": user_id})
    return user and (time.time() < user['expiry'])
    
