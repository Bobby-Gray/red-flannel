import os
from alert_manager import AlertManager
from utils import load_yaml_config, get_user_home_directory

def initialize_monitored_file_paths():
    """Load paths from paths.yaml and dynamically replace <username> placeholders."""
    config_file = "config/paths.yaml"
    print(f'config_file: {config_file}')
    config = load_yaml_config(config_file)
    monitored_file_paths = []

    if config and "paths" in config:
        for path in config["paths"]["monitored_files"]:
            print(f'Monitored Files: {path}')
            # Replace <username> with the actual home directory
            if "<username>" in path:
                user_home = get_user_home_directory()
                path = path.replace("<username>", user_home)
                print(f'File path updated with user_home: {path}')
            monitored_file_paths.append(path)

    else:
        print(f"Warning: No valid paths found in {config_file}. Using default paths.")
        monitored_file_paths = [
            "/var/log/system.log",
            "/var/log/secure.log",
            "/Library/Logs",
        ]

    return monitored_file_paths

def initialize_monitored_dir_paths():
    """Load paths from paths.yaml and dynamically replace <username> placeholders."""
    config_file = "config/paths.yaml"
    print(f'config_file: {config_file}')
    config = load_yaml_config(config_file)
    monitored_directory_paths = []

    if config and "paths" in config:
        for path in config["paths"]["monitored_directories"]:
            print(f'Monitored Directories: {path}')
            # Replace <username> with the actual home directory
            if "<username>" in path:
                user_home = get_user_home_directory()
                path = path.replace("<username>", user_home)
                print(f'Directory path updated with user_home: {path}')
            monitored_directory_paths.append(path)

    else:
        print(f"Warning: No valid paths found in {config_file}. Using default paths.")
        monitored_directory_paths = [
            "/var/log/system.log",
            "/var/log/secure.log",
            "/Library/Logs",
        ]
    return monitored_directory_paths

if __name__ == "__main__":
    monitored_file_paths = initialize_monitored_file_paths()
    for path in monitored_file_paths:
        if not os.path.exists(path):
            print(f"Warning: Path does not exist - {path}")
        else:
            print(f"Monitoring path: {path}")
    monitored_dir_paths = initialize_monitored_dir_paths()
    for path in monitored_dir_paths:
        if not os.path.exists(path):
            print(f"Warning: Path does not exist - {path}")
        else:
            print(f"Monitoring path: {path}")
    alert_manager = AlertManager(monitored_file_paths, monitored_dir_paths)
    alert_manager.run()