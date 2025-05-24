# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris Polewiak

"""
log_utils.py

Purpose:
    Logging and progress bar utilities for the Photo Auto Tag Processor project.

Main Functions:
    - set_test_mode(test_mode): Enables or disables test/debug logging mode.
    - log_debug(msg): Prints debug messages (only in test mode).
    - log_info(msg): Prints informational messages.
    - log_warning(msg): Prints warning messages in yellow.
    - log_error(msg): Prints error messages in red and exits the program.
    - render_progress_bar(current, total, width): Renders a textual progress bar for console output.

This module supports colored console logging and simple progress visualization.
"""

from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

log_path = os.environ.get("LOGS_PATH", "./logs/photo-indexer.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

logger = logging.getLogger("photo-indexer")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False



is_test = False  # Domyślnie False
def set_test_mode(test_mode: bool):
    global is_test
    is_test = test_mode

# Logging colors
RESET  = "\033[0m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
GRAY   = "\033[90m"


def log_debug(msg):
    if is_test:
        print(f"{GRAY}[DEBUG] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}", flush=True)
        logger.debug(msg)

def log_info(msg):
    print(f"[INFO] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)
    logger.info(msg)

def log_warning(msg):
    print(f"{YELLOW}[WARNING] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}", flush=True)
    logger.warning(msg)

def log_error(msg):
    print(f"{RED}[ERROR] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}", flush=True)
    logger.error(msg)
    exit(0)

def render_progress_bar(current, total, width=100):
    done = int(width * current / total)
    percent = int((current / total) * 100)
    return f"[{'█' * done}{'-' * (width - done)}] {percent}%"