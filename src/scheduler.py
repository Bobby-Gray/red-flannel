import time
from src.query_engine import QueryEngine

class Scheduler:
    def __init__(self, interval=60):
        self.query_engine = QueryEngine()
        self.interval = interval

    def run_once(self):
        self.query_engine.run_queries()

    def start(self):
        while True:
            self.run_once()
            time.sleep(self.interval)