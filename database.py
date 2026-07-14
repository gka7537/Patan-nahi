import motor.motor_asyncio
import os
import time
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncMongoClient(MONGO_URI)
db = client["file_bot_db"]

# Collections
files_col = db["files"]  # Files aur Albums
users_col = db["users"]  # Users verification

async def add_album(album_id, files_data):
    """Multiple files ko ek sath album_id ke sath save karna."""
    data = {
        "album_id": album_id,
        "files": files_data,  # Yeh ek list hogi files ki
        "created_at": time.time()
    }
    await files_col.insert_one(data)

async def get_album(album_id):
    """Album details fetch karne ke liye."""
    return await files_col.find_one({"album_id": album_id})

async def add_user_verification(user_id):
    """User ko 24 hours ke liye verify karna."""
    expiry_time = time.time() + (24 * 60 * 60) # 24 hours in seconds
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"expiry_time": expiry_time}},
        upsert=True
    )

async def is_user_verified(user_id):
    """Check karna ki kya user ka 24 hours verify time bacha hai."""
    user = await users_col.find_one({"user_id": user_id})
    if user:
        if time.time() < user['expiry_time']:
            return True
        else:
            # Time khatam hone par record delete kar dena
            await users_col.delete_one({"user_id": user_id})
    return False
    
