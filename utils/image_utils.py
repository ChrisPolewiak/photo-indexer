# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
image_utils.py

Purpose:
    Utility functions for image manipulation, such as resizing images to fit a maximum file size.

Main Functions:
    - resize_image(img, max_size_bytes): Compresses and resizes a PIL Image object to ensure it does not exceed the specified size in bytes.
    - rescale_image(image, height=None, width=None): Rescales the image to a specified height or width while maintaining the aspect ratio.
    - pil_image_to_bytes(image, format="JPEG"): Converts a PIL Image object to bytes in the specified format.

This module is used to prepare images for processing or uploading by reducing their size while maintaining reasonable quality.
"""

import io
from io import BytesIO
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

def rescale_image(image, height=None, width=None):
    """
    Rescale the image to a specified height while maintaining the aspect ratio.
    """
    original_width, original_height = image.size
    log_debug(f"Original image size: {original_width}x{original_height}")

    if height is not None:
        aspect_ratio = original_width / original_height
        new_width = int(height * aspect_ratio)
        log_debug(f"New image size: {new_width}x{height}")
        new_size = (new_width, height)
    elif width is not None:
        aspect_ratio = original_height / original_width
        new_height = int(width * aspect_ratio)
        log_debug(f"New image size: {width}x{new_height}")
        new_size = (width, new_height)
    else:
        log_error("Either height or width must be specified for rescaling.")

    return image.resize(new_size, Image.Resampling.LANCZOS)


def pil_image_to_bytes(image, format="JPEG"):
    buf = BytesIO()
    image.save(buf, format=format)
    buf.seek(0)
    return buf