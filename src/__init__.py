"""
Red Flannel Logging and Alerting Tool
----------------------------------
Modules:
- file_monitor: Monitors file paths for changes and events.
- alert_manager: Handles alert definitions and triggers.
- scheduler: Manages scheduled queries and monitoring.
- query_engine: Processes queries and matches patterns.

"""

# Expose key modules at the package level
from .file_monitor import initialize_monitored_file_paths, initialize_monitored_dir_paths
from .alert_manager import AlertManager
from .scheduler import Scheduler
from .query_engine import QueryEngine

__all__ = [
    "initialize_monitored_paths",
    "AlertManager",
    "Scheduler",
    "QueryEngine",
]

# Define package-level constants (optional)
PACKAGE_NAME = "red-flannel"
VERSION = "1.0.0"
