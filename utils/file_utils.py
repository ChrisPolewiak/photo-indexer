import os
from utils.log_utils import log_debug, log_info, log_warning, log_error

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
        # Exclude subdirectories that start with non-alphanumeric characters
        dirs[:] = [d for d in dirs if d and d[0].isalnum()]

        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.heic')):
                full_path = os.path.join(root, filename)
                # Include file only if the path is considered valid
                if is_valid_path(full_path):
                    files.append(full_path)

    log_debug(f"Total files found: {len(files)}")
    return files