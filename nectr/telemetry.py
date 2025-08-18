# telemetry.py
from datetime import datetime
from pathlib import Path

class TelemetryLogger:
    def __init__(self, log_path="data/attack_logs/agent.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        timestamp = datetime.now().isoformat()
        with open(self.log_path, "a") as f:
            f.write(f"{timestamp} :: {message}\n")
