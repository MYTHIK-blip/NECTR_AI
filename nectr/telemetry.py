from datetime import datetime
from pathlib import Path
import json


class TelemetryLogger:
    def __init__(self, log_path="data/attack_logs/agent.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Default plain text log"""
        timestamp = datetime.now().isoformat()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} :: {message}\n")

    def log_json(self, data: dict):
        """Structured JSON log entry"""
        timestamp = datetime.now().isoformat()
        record = {"timestamp": timestamp, **data}
        with open(self.log_path.with_suffix(".jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def log_event(self, event_type: str, payload: dict):
        """Unified telemetry logging for typed events"""
        entry = {
            "type": event_type,
            "payload": payload
        }
        self.log_json(entry)
