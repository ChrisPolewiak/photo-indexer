import os

def read_files_from_directory(directory_path):
    log_debug(f"Reading files from directory: {directory_path}")
    files = []
    for root, dirs, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.heic')):
                files.append(os.path.join(root, filename))
    log_debug(f"Todal files found: {len(files)}")
    return files
