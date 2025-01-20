import os
import re
import yaml
from file_monitor import initialize_monitored_file_paths, initialize_monitored_dir_paths
from alert_manager import AlertManager

class QueryEngine:
    def __init__(self, alert_config_file="config/alerts.yaml"):
        self.monitored_file_paths = initialize_monitored_file_paths()
        self.monitored_dir_paths = initialize_monitored_dir_paths()
        self.alert_manager = AlertManager(self.monitored_file_paths, self.monitored_dir_paths, alert_config_file)
        self.alert_config = self.load_alert_config(alert_config_file)

    def load_alert_config(self, config_file):
        """Load alert definitions from the YAML configuration file."""
        try:
            with open(config_file, "r") as file:
                return yaml.safe_load(file)["alerts"]
        except FileNotFoundError:
            print(f"Alert config file not found: {config_file}")
            return []

    def execute_alert_logic(self):
        """Execute alert logic based on the configuration."""
        for alert in self.alert_config:
            if alert["type"] == "regex":
                self.process_regex_alert(alert)
            elif alert["type"] == "change":
                self.process_change_alert(alert)

    def process_regex_alert(self, alert):
        """Process regex-based alerts."""
        pattern = re.compile(alert["pattern"])
        context = alert.get("context", "")
        for path in self.monitored_file_paths:
            if os.path.isfile(path):
                try:
                    with open(path, "r") as file:
                        for line in file:
                            if pattern.search(line):
                                self.alert_manager.send_alert(
                                    f"Pattern match: {alert['name']}\nContext: {context}\nLine: {line.strip()}"
                                )
                except Exception as e:
                    print(f"Error reading file {path}: {e}")

    def process_change_alert(self, alert):
        """Process change-based alerts."""
        monitored_paths = alert.get("monitored_paths", [])
        for path in monitored_paths:
            if os.path.isdir(path):
                self.alert_manager.check_file_changes()

    def run_queries(self):
        """Run the query engine to execute all alert logic."""
        print("Executing alert logic...")
        self.execute_alert_logic()

if __name__ == "__main__":
    query_engine = QueryEngine()
    query_engine.run_queries()
