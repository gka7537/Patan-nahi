import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncMongoClient(MONGO_URI)
db = client["file_bot_db"]

# Collections
files_col = db["files"]  # Files aur Albums ke liye
users_col = db["users"]  # Verification status ke liye

async def add_file(file_id, file_name, file_size, album_id=None):
    """File ya Album ko database mein add karne ke liye."""
    data = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "album_id": album_id
    }
    await files_col.insert_one(data)

async def get_file(file_id):
    """File details fetch karne ke liye."""
    return await files_col.find_one({"file_id": file_id})

async def add_user_verification(user_id, expiry_time):
    """User ka verification status save karne ke liye (24 hours)."""
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"expiry_time": expiry_time}},
        upsert=True
    )

async def is_user_verified(user_id):
    """Check karne ke liye ki user verify hai ya nahi."""
    user = await users_col.find_one({"user_id": user_id})
    if user:
        return True # Yahan logic aage add karenge expiry check ke liye
    return False
  
