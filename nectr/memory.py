# memory.py
import sqlite3
from datetime import datetime
from pathlib import Path

class MemoryManager:
    def __init__(self, config):
        self.db_path = config.get("path", "data/memory.sqlite")
        self._initialize()

    def _initialize(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            signal TEXT,
            insight TEXT
        )
        """)
        self.conn.commit()

    def store(self, signal, insight):
        self.conn.execute(
            "INSERT INTO memory (timestamp, signal, insight) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), signal, insight)
        )
        self.conn.commit()

    def fetch_recent(self, limit=10):
        return self.conn.execute(
            "SELECT timestamp, signal, insight FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
