# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
metadata_utils.py

Purpose:
    Functions for applying and managing metadata (EXIF, XMP, IPTC) in image files.

Main Functions:
    - apply_exiftool_metadata(file_path, metadata, owner_info, session): Applies metadata to an image using ExifTool.
    - get_metadata_owner(make, model): Returns author/copyright info based on camera make/model.
    - is_ai_edited(file_path): Checks if an image has been marked as AI edited in its metadata.

This module centralizes all metadata writing logic for the photo processing pipeline.
"""

import os
import json
import subprocess
from utils.log_utils import *


def apply_exiftool_metadata(file_path, metadata, owner_info=None, session=None):

    author = owner_info["author"]
    copyright_text = owner_info["copyright"]
    label = owner_info.get("label")

    args = ['-overwrite_original', '-P']

    log_info("ExifTool metadata apply")
    
    filename = os.path.basename(file_path)
    skip_author = "-not-mine.jpg" in filename

    caption = metadata.get('caption', '').strip()
    if caption:
        args.append(f'-XPTitle={caption}')
        args.append(f'-XPSubject={caption}')
        comment_hex = ''.join(f'{b:02x}' for b in 'AI Edited'.encode("utf-16le") + b'\x00\x00')
        args.append(f'-XPComment#={comment_hex}')
        args.append(f'-XMP-dc:Description={caption}')
        args.append(f'-XMP-dc:Title={caption}')

    if copyright_text:
        args.append(f'-XMP-dc:Rights={copyright_text}')
        args.append('-XMP-xmpRights:Marked=True')

    if author and not skip_author:
        args.append(f'-XMP-dc:Creator={author}')
        args.append(f'-Artist={author}')
        args.append(f'-XPAuthor={author}')

    if label:
        args.append(f'-XMP:Label={label}')

    keywords = [kw.strip() for kw in metadata.get('keywords', []) if kw.strip()]
    if keywords:
        joined = '; '.join(keywords)
        args.append(f'-XPKeywords={joined}')

        for kw in keywords:
            args.append(f'-XMP-dc:Subject+={kw}')
            args.append(f'-XMP-lr:HierarchicalSubject+=AITags|{kw}')

    args.append(file_path)

    try:
        if session:
            session.run_command(args)
        else:
            subprocess.run(["exiftool"] + args, check=True)

    except subprocess.CalledProcessError as e:
        log_error(f"ExifTool failed: {e}")

with open('.camera_owners.json', 'r', encoding='utf-8') as f:
    CAMERA_OWNERS = json.load(f)

def get_metadata_owner(make, model):
    key = f"{make} {model}"
    owner = CAMERA_OWNERS.get(key)
    if not owner:
        owner = CAMERA_OWNERS.get('Unknown')
        log_warning(f"Uknown camera: {key}")
    return owner

def is_ai_described(file_path):
    log_debug(f"Checking if {file_path} is AI described")
    try:
        result = subprocess.run(
            ["exiftool", "-s3", "-XMP-lr:HierarchicalSubject", file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        line = result.stdout.strip()
        tags = [tag.strip() for tag in line.split(",")]
        log_debug(f"AI tags found: {tags}")
        return any(tag.startswith("AITags") for tag in tags)
    except Exception as e:
        log_warning(f"Could not check AI tags for {file_path}: {e}")
        return False