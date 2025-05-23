# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
exif_utils.py

Purpose:
    Utility functions for reading, extracting, and writing EXIF metadata in image files.

Main Functions:
    - get_photo_datetime(exif_data, filename): 
        Extracts the photo's datetime from EXIF data if available, or tries to parse it from the filename.
        Returns a datetime object or logs an error if not found.
    - write_datetime_to_exif(file_path, dt): 
        Writes the given datetime to the EXIF DateTime, DateTimeOriginal, and DateTimeDigitized fields in the image file.

This module is used by the main processing script to ensure correct and consistent date metadata in images.
"""

from datetime import datetime
import piexif
import re
from utils.log_utils import *


def get_photo_datetime(exif_data, filename):
    """
    Extracts the photo datetime from EXIF data or, if unavailable, from the filename.
    Returns a datetime object or logs an error if not found.
    """
    dt_str = exif_data.get(36867) or exif_data.get(306)
    if isinstance(dt_str, datetime):
        return dt_str
    if dt_str:
        try:
            date_part, time_part = dt_str.split()
            normalized = f"{re.sub(r'[:\-]', '-', date_part)} {re.sub(r'[:\-]', ':', time_part)}"
            return datetime.strptime(normalized, "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    match = re.search(r"(20\d{2}-\d{2}-\d{2})_(\d{6})", filename)
    if match:
        date_str, time_str = match.groups()
        dt_str = f"{date_str} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    match = re.search(r"(20\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if match:
        y, m, d, hh, mm, ss = match.groups()
        return datetime.strptime(f"{y}-{m}-{d} {hh}:{mm}:{ss}", "%Y-%m-%d %H:%M:%S")
    log_error(f"There is no date in EXIF and in {filename}")


def write_datetime_to_exif(file_path, dt: datetime):
    """
    Writes the given datetime to the EXIF DateTime, DateTimeOriginal, and DateTimeDigitized fields.
    """
    exif_dict = piexif.load(file_path)
    dt_string = dt.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict["0th"][piexif.ImageIFD.DateTime] = dt_string
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = dt_string
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = dt_string
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path)
    log_info(f"EXIF datetime written to file: {dt_string}")
