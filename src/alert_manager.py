import os
import hashlib
import time
import re
import yaml
from datetime import datetime
from utils import compute_file_hash, load_yaml_config
# from endpoint_security import EndpointSecurity

class AlertManager:
    def __init__(self, monitored_file_paths, monitored_directory_paths, alert_config_file="config/alerts.yaml"):
        self.monitored_file_paths = monitored_file_paths
        self.monitored_directory_paths = monitored_directory_paths
        self.alert_config = load_yaml_config(alert_config_file)
        self.file_hashes = {}  # Store file hashes to detect changes
        self.dir_hashes = {}  # Store directory hashes to detect changes
        # self.endpoint_security = EndpointSecurity()

    def load_alert_config(self, config_file):
        """Load alert definitions from the YAML configuration file."""
        try:
            with open(config_file, "r") as file:
                return yaml.safe_load(file)["alerts"]
        except FileNotFoundError:
            print(f"Alert config file not found: {config_file}")
            return []

    def check_file_changes(self):
        """Check for file creation or modifications."""
        for path in self.monitored_directory_paths:
            new_hash = compute_file_hash(path)
            hash_is_dir = False
            if len(str(new_hash)) > 32:
                hash_is_dir = True
                new_hashes = new_hash
                new_hash = list(new_hash.keys())[0]
                if new_hash not in self.dir_hashes.keys():
                    self.dir_hashes.update(new_hashes)
            # Directory branch
            if path not in self.file_hashes and hash_is_dir:
                # New directory detected
                self.file_hashes[path] = new_hash
                if new_hash is not None:
                    self.send_alert(f"New directory hash detected: {path}: {new_hash}")
            elif hash_is_dir and self.file_hashes[path] != new_hash:
                if new_hash in self.dir_hashes.keys():
                    old_dir_hash = self.file_hashes[path]
                    old_dir_hashes = self.dir_hashes[old_dir_hash]
                    diff = set(old_dir_hashes.items()) ^ set(new_hashes[new_hash].items())
                    self.dir_hashes.update(new_hashes)
                    # Directory modified
                    self.file_hashes[path] = new_hash
                    self.send_alert(f"File(s) in monitored directory \'{path}\' changed:\nOld Directory MD5: {old_dir_hash}\nNew Directory MD5: {new_hash}\nFile(s) Changed: {diff}")
            # File branch
            elif not hash_is_dir and path not in self.file_hashes:
                # New file detected
                self.file_hashes[path] = new_hash
                if new_hash is not None:
                    self.send_alert(f"New file hash detected: {path}: {new_hash}")
            elif not hash_is_dir and self.file_hashes[path] != new_hash:
                orig_file_hash = self.file_hashes[path]
                orig_file_hash = self.file_hashes[path]
                self.file_hashes[path] = new_hash
                self.send_alert(f"File modified: {path}:\n Old MD5: {orig_file_hash}\n New MD5: {new_hash}")

    def search_logs(self):
        """Search log files for suspicious patterns defined in alerts."""
        for alert in self.alert_config:
            if alert["type"] == "regex":
                pattern = re.compile(alert["pattern"])
                context = alert.get("context", "")
                for path in self.monitored_file_paths:
                    if os.path.isfile(path):
                        with open(path, "r") as file:
                            for line in file:
                                if pattern.search(line):
                                    self.send_alert(f"Pattern match for \'{path}\': {alert['name']}\nContext: {context}\nLine: {line.strip()}")

    def check_endpoint_security_events(self):
        """Process endpoint security events."""
        # The EndpointSecurity class invokes send_alert directly.
        # This method is a placeholder for additional processing if needed.
        pass

    def send_alert(self, message):
        """Log the alert message to a results file."""
        results_file = "data/results/alerts.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"[{timestamp}] {message}"
        print(alert_message)  # Print alert to the console
        with open(results_file, "a") as file:
            file.write(alert_message + "\n")

    # def initialize(self):
    #     """Initialize components."""
    #     self.endpoint_security.initialize()

    def run(self):
        """Main loop to monitor files and trigger alerts."""
        try:
            self.initialize()
            while True:
                self.check_file_changes()
                self.search_logs()
                # self.check_endpoint_security_events()
                time.sleep(3600)  # Default 1 hour
        except KeyboardInterrupt:
            # self.endpoint_security.shutdown()
            print("Shutting down gracefully.")
