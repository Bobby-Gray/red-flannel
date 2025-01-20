import os
import getpass
import hashlib
import logging
from checksumdir import dirhash
from datetime import datetime
import yaml

# Get the local home directory path
def get_user_home_directory():
    """Get the current user's home directory dynamically."""
    username = getpass.getuser()  # Fetch the username of the logged-in user
    home_directory = os.path.join("/Users", username)
    if os.path.exists(home_directory):
        return home_directory
    else:
        raise FileNotFoundError(f"Home directory not found for user: {username}")

# Initialize logging for the project
def initialize_logger(log_file="data/results/tool.log", level=logging.INFO):
    """Set up the logger for the project."""
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()
    logger.info("Logger initialized.")
    return logger

# File hash utility
def compute_file_hash(path):
    """
    Compute the MD5 hash for a file or a folder.
    - If the path is a file, return its MD5 hash.
    - If the path is a folder, return a dictionary with the folder hash as the key
      and a dictionary of file paths and their hashes as the value.
    """
    if not os.path.exists(path):
        print(f"Invalid path: {path} (path does not exist)")
        return None
    if not os.access(path, os.R_OK):
        print(f"Cannot access path: {path} (insufficient permissions)")
        return None

    if os.path.isfile(path):
        return _hash_file(path)
    elif os.path.isdir(path):
        folder_hash, file_hashes = _hash_folder(path)
        return {folder_hash: file_hashes}
    else:
        print(f"Invalid path: {path} (not a file or directory)")
        return None

def _hash_file(file_path):
    """Compute MD5 hash for a single file."""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}\nSkipping!")
        return None
    return md5_hash.hexdigest()

def _hash_folder(folder_path):
    """Compute a combined MD5 hash for all files in a folder (recursively) and return file hashes."""
    md5_hash = hashlib.md5()
    file_hashes = {}

    for root, _, files in os.walk(folder_path):
        for file in sorted(files):  # Sort files for consistency
            file_path = os.path.join(root, file)
            if os.access(file_path, os.R_OK):
                file_hash = _hash_file(file_path)
                relative_path = os.path.relpath(file_path, folder_path)
                file_hashes[relative_path] = file_hash
                # Update folder hash with file hash and relative file path
                md5_hash.update(f"{relative_path}:{file_hash}".encode())

    return md5_hash.hexdigest(), file_hashes

# Timestamp utility
def get_current_timestamp():
    """Get the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# YAML configuration loader
def load_yaml_config(config_file):
    """Load and parse a YAML configuration file."""
    try:
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_file}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file {config_file}: {e}")
        return None

# Path validation utility
def validate_paths(paths):
    """Check if a list of paths exists, logging warnings for missing ones."""
    valid_paths = []
    for path in paths:
        if os.path.exists(path):
            valid_paths.append(path)
        else:
            logging.warning(f"Path does not exist: {path}")
    return valid_paths

# Directory creation utility
def ensure_directory_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
