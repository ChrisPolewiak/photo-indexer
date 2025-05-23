import os
import sys
import argparse
from datetime import datetime
import time
import traceback
import shutil
import subprocess
from PIL import Image
from dotenv import load_dotenv
from pillow_heif import register_heif_opener
register_heif_opener()

from utils import (
    log_debug, log_info, log_warning, log_error, render_progress_bar, set_test_mode,
    image_analyse,
    resize_image, 
    get_photo_datetime, write_datetime_to_exif,
    apply_exiftool_metadata, get_metadata_owner,
    read_files_from_directory,
    ExifToolSession
)

load_dotenv()

parser = argparse.ArgumentParser(description='Process and tag photos.')
parser.add_argument('--test', '-t', type=str, help='Test mode (y/n)')
args = parser.parse_args()
is_test = args.test == 'y'
set_test_mode(is_test)

source_dir = os.environ.get("SOURCE_DIR")
action_describe = 'y'
azureAIVisionMaxImageSize = 20 * 1024 * 1024  # 20 MB

if is_test:
    target_dir = os.environ.get("TARGET_TEST_DIR")
    log_info("🧪 Test mode enabled.")
    action_move = False
    debug_status = True

else:
    target_dir = os.environ.get("TARGET_DIR")
    log_info("🚀 Production mode.")
    action_move = True
    debug_status = False

# ----------------- MAIN PROCESS ------------------

def process_images():

    # Record the script start time
    start_time = time.time()
    log_info("Script started.")

    all_files = read_files_from_directory(source_dir)
    all_files.sort()
    file_times = []

    session = ExifToolSession()

    for idx, file_in in enumerate(all_files, start=1):
        try:
            # Record the start time for processing this file
            file_start = time.time()
            log_debug(f"Processing file: {file_in}")
            if file_in.lower().endswith(".heic"):
                heic_path = file_in
                jpg_path = file_in.rsplit(".", 1)[0] + ".jpg"
                log_info(f"Converting HEIC to JPG: {file_in} -> {jpg_path}")

                with Image.open(heic_path) as image:
                    image = image.convert("RGB")
                    image.save(jpg_path, "JPEG")

                log_debug(f"Copy EXIF data from HEIC to JPG: {file_in}->{jpg_path}")
                subprocess.run(["exiftool", "-overwrite_original", "-TagsFromFile", heic_path, jpg_path], check=True)
                # os.remove(file_in)
                file_in = jpg_path

            file_start = time.time()
            progress_bar = render_progress_bar(idx, len(all_files))
            log_info(f"Filename: {os.path.basename(file_in)}")

            with Image.open(file_in) as image:

                log_debug(f"Reading EXIF data from {file_in}")
                exif_data = image._getexif() or {}

                camera_make = exif_data.get(271, '').strip()
                camera_model = exif_data.get(272, '').strip()

                dt = get_photo_datetime(exif_data, os.path.basename(file_in))

                # Update EXIF datetime if not present
                if not exif_data.get(36867) and not exif_data.get(306):
                    write_datetime_to_exif(file_in, dt)

                date_yyyy, date_mm, date_dd = f"{dt.year:04}", f"{dt.month:02}", f"{dt.day:02}"
                time_hh, time_mm, time_ss = f"{dt.hour:02}", f"{dt.minute:02}", f"{dt.second:02}"

                log_info(f"Image Date time: {date_yyyy}-{date_mm}-{date_dd} {time_hh}:{time_mm}:{time_ss}")
                log_info(f"Camera: '{camera_make} {camera_model}'")
                cameraOwner = get_metadata_owner(camera_make, camera_model)

                log_debug(f"Camera Owner: {cameraOwner}")
                dest_dir = os.path.join(target_dir, date_yyyy, f"{date_yyyy}-{date_mm}")
                log_debug(f"Destination Directory: {dest_dir}")
                os.makedirs(dest_dir, exist_ok=True)

                dest_filename = f"{date_yyyy}-{date_mm}-{date_dd}_{time_hh}{time_mm}{time_ss}.jpg"
                log_debug(f"Destination Filename: {dest_filename}")

                dest_path = os.path.join(dest_dir, dest_filename)
                if os.path.exists(dest_path):
                    log_debug(f"File already exists: {dest_path}")
                    i = 1
                    base_name = dest_filename.rsplit('.', 1)[0]
                    while os.path.exists(os.path.join(dest_dir, f"{base_name}_{i}.jpg")):
                        i += 1
                    dest_filename = f"{base_name}_{i}.jpg"
                    log_warning(f"File already exists, new filename: {dest_filename}")
                    dest_path = os.path.join(dest_dir, dest_filename)

                shutil.copy2(file_in, dest_path)
                log_debug(f"File copied to {dest_path}")

                metadata = {}
                if action_describe:
                    log_debug(f"Analyzing image: {file_in}")
                    original_size = os.path.getsize(file_in)
                    if original_size == 0:
                        log_error(f"File {file_in} is empty — skipping.")

                    if original_size > azureAIVisionMaxImageSize:
                        log_debug(f"Image size is { round(original_size/1024/1024,2) }MB — resizing to {azureAIVisionMaxImageSize/1024/1024}MB")
                        image_data = resize_image(image, azureAIVisionMaxImageSize)
                        log_debug("Image resized before analysis")
                    else:
                        log_debug(f"Image size is { round(original_size/1024/1024,2) }MB — using original for analysis")
                        with open(file_in, "rb") as f:
                            image_data = f.read()

                        if not image_data:
                            log_error(f"File {file_in} is empty or unreadable")

                    metadata = image_analyse(image_data)
                    log_debug(f"Metadata size: {len(metadata)}")

                if metadata:
                    apply_exiftool_metadata(
                        dest_path,
                        metadata,
                        cameraOwner
                        )

            if action_move:
                log_debug(f"Moving file to {dest_path}")
                if os.path.exists(dest_path):
                    log_debug(f"Removing original file: {file_in}")
                    os.remove(file_in)

            file_times.append(time.time() - file_start)
            log_info(f"Done: {file_in}")

        except Exception as e:
            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            log_error(f"Failed: {file_in} | {type(e).__name__} - {e} at {tb.filename}:{tb.lineno}")

    session.close()

    # Calculate and log total and average processing times
    total = sum(file_times)
    avg = total / len(file_times) if file_times else 0
    end_time = time.time()
    log_info(f"Script finished. Start: {datetime.fromtimestamp(start_time):%Y-%m-%d %H:%M:%S}, End: {datetime.fromtimestamp(end_time):%Y-%m-%d %H:%M:%S}")
    log_info(f"All done. Total: {total:.2f}s | Avg per file: {avg:.2f}s")



if __name__ == '__main__':
    process_images()