import argparse
from src.scheduler import Scheduler

def main():
    parser = argparse.ArgumentParser(description="Command-line Logging and Alerting Tool")
    parser.add_argument('--run-once', action='store_true', help="Run a single query cycle and exit.")
    args = parser.parse_args()

    scheduler = Scheduler()
    if args.run_once:
        scheduler.run_once()
    else:
        scheduler.start()

if __name__ == "__main__":
    main()