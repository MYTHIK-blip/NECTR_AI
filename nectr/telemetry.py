from datetime import datetime
from pathlib import Path
import json
import logging # Added import

class TelemetryLogger:
    def __init__(self, log_path="data/attack_logs/agent.log"):
        self.log_path = Path(log_path)
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logging.error(f"Could not create log directory {self.log_path.parent}: {e}")
            # Decide how to handle this critical error, e.g., disable logging or raise

    def log(self, message: str):
        """Default plain text log"""
        timestamp = datetime.now().isoformat()
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} :: {message}\n")
        except IOError as e:
            logging.error(f"Could not write to log file {self.log_path}: {e}")

    def log_json(self, data: dict):
        """Structured JSON log entry"""
        timestamp = datetime.now().isoformat()
        record = {"timestamp": timestamp, **data}
        try:
            with open(self.log_path.with_suffix(".jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except IOError as e:
            logging.error(f"Could not write to JSONL log file {self.log_path.with_suffix('.jsonl')}: {e}")

    def log_event(self, event_type: str, payload: dict):
        """Unified telemetry logging for typed events"""
        entry = {
            "type": event_type,
            "payload": payload
        }
        self.log_json(entry)

    def get_recent_logs(self, limit: int = 10) -> list[str]:
        """Reads and returns the last 'limit' lines from the log file."""
        try:
            if not self.log_path.exists():
                return []
            with open(self.log_path, "r", encoding="utf-8") as f:
                # Read all lines and return the last 'limit'
                return f.readlines()[-limit:]
        except IOError as e:
            logging.error(f"Could not read from log file {self.log_path}: {e}")
            return []
