import os
import math

def get_readable_size(size_in_bytes):
    """File size ko readable format mein badalne ke liye."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

async def format_file_info(file_obj):
    """File ka name aur size format karne ke liye."""
    name = file_obj.file_name if hasattr(file_obj, 'file_name') else "Unknown"
    size = get_readable_size(file_obj.file_size)
    return f"📄 **Name:** {name}\n📦 **Size:** {size}"

async def get_thumbnail(app, message):
    """File ka thumbnail extract karne ke liye."""
    try:
        # Agar user ne custom thumbnail set kiya hai ya file ka apna thumbnail hai
        return await app.download_media(message, in_memory=True)
    except Exception:
        return None
      
