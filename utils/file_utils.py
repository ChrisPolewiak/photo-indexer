# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
file_utils.py

Purpose:
    Utility functions for file and directory operations used throughout the project.

Main Functions:
    - is_valid_path(path): Checks if a path is valid by ensuring all directory parts start with an alphanumeric character.
    - read_files_from_directory(directory_path): Reads all .jpg, .jpeg, and .heic files from a directory, excluding hidden/system directories.
    - move_file_to_unsupported(src): Moves a file to the unsupported directory.
    - has_pending_files(directory): Checks if there are any pending files in a directory, excluding hidden/system directories.

Use this module for all file system interactions in the project.
"""

import os
from utils.log_utils import *


def is_valid_path(path):
    """
    Checks if all directory parts of the path start with an alphanumeric character.
    This filters out system/hidden folders like .git, @eaDir, _tmp, etc.
    """
    parts = os.path.normpath(path).split(os.sep)
    for part in parts:
        if part and not part[0].isalnum():
            return False
    return True

def read_files_from_directory(directory_path):
    """
    Reads all .jpg, .jpeg, and .heic files from a given directory,
    excluding files in hidden or system directories.
    """
    log_debug(f"Reading files from directory: {directory_path}")
    files = []
    
    for root, dirs, filenames in os.walk(directory_path):
        original_dirs = list(dirs)
        # Exclude subdirectories that start with non-alphanumeric characters
        EXCLUDED_PREFIXES = ('.', '_', '@')
        dirs[:] = [d for d in dirs if d and d[0] not in EXCLUDED_PREFIXES]

        # Log which directories are being skipped
        skipped_dirs = [d for d in original_dirs if d not in dirs]
        for skipped in skipped_dirs:
            log_debug(f"Skipping directory: {os.path.join(root, skipped)}")

        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.heic')):
                full_path = os.path.join(root, filename)
                # Include file only if the path is considered valid
                if is_valid_path(full_path):
                    files.append(full_path)

    log_debug(f"Total files found: {len(files)}")
    return files

def move_file_to_unsupported(src):
    """
    Moves a file to the unsupported directory.
    """
    dirname = ".unsupported"
    dst = os.path.join(os.path.dirname(src), dirname, os.path.basename(src))
    # create the unsupported directory if it doesn't exist
    if not os.path.exists(os.path.dirname(dst)):
        try:
            os.makedirs(os.path.dirname(dst))
            log_debug(f"Created unsupported directory: {os.path.dirname(dst)}")
        except Exception as e:
            log_error(f"Failed to create unsupported directory: {e}")
            return
    log_info(f"Moving unsupported file: {src} -> {dst}")
    try:
        os.rename(src, dst)
        log_debug(f"File moved successfully: {src} -> {dst}")
    except Exception as e:
        log_error(f"Failed to move file {src} to {dst}: {e}")

def has_pending_files(directory_path):
    """
    Returns True if there are files to process in the directory.
    Uses the same logic as read_files_from_directory.
    """
    files = read_files_from_directory(directory_path)
    return len(files) > 0

