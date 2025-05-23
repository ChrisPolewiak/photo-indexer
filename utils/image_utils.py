import io
from PIL import Image
from utils.log_utils import *

def resize_image(img, max_size_bytes):

    log_info(f"Resizing image to under {max_size_bytes / (1024 * 1024)} MB")
    img_format = img.format or "JPEG"
    quality = 95
    step = 5
    buffer = io.BytesIO()

    while quality > 10:
        buffer.seek(0)
        buffer.truncate()
        log_debug(f" - Trying quality {quality}")
        img.save(buffer, format=img_format, quality=quality)
        if buffer.tell() < max_size_bytes:
            return buffer.getvalue()
        quality -= step

    width, height = img.size
    while buffer.tell() >= max_size_bytes and (width > 800 or height > 800):
        width = int(width * 0.9)
        height = int(height * 0.9)
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        buffer.seek(0)
        buffer.truncate()
        resized_img.save(buffer, format=img_format, quality=quality)

    return buffer.getvalue()

