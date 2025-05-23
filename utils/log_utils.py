from datetime import datetime
import os

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
        print(f"{GRAY}[DEBUG] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}")

def log_info(msg):
    print(f"[INFO] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}")

def log_warning(msg):
    print(f"{YELLOW}[WARNING] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}")

def log_error(msg):
    print(f"{RED}[ERROR] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}{RESET}")
    exit(0)

def render_progress_bar(current, total, width=100):
    done = int(width * current / total)
    percent = int((current / total) * 100)
    return f"[{'█' * done}{'-' * (width - done)}] {percent}%"