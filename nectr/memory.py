import sqlite3
from datetime import datetime
from pathlib import Path
import json
import csv


class MemoryManager:
    def __init__(self, config: dict):
        self.config = config
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

    def _ensure_connection(self):
        try:
            self.conn.execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            self._initialize()

    def store(self, signal: str, insight: str):
        self._ensure_connection()
        self.conn.execute(
            "INSERT INTO memory (timestamp, signal, insight) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), signal, insight)
        )
        self.conn.commit()

    def fetch_recent(self, limit: int = 10):
        self._ensure_connection()
        return self.conn.execute(
            "SELECT timestamp, signal, insight FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

    def fetch_by_time_range(self, start_time: str, end_time: str):
        self._ensure_connection()
        return self.conn.execute(
            "SELECT * FROM memory WHERE timestamp BETWEEN ? AND ?",
            (start_time, end_time)
        ).fetchall()

    def search_by_keyword(self, keyword: str):
        self._ensure_connection()
        return self.conn.execute(
            "SELECT * FROM memory WHERE signal LIKE ? OR insight LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        ).fetchall()

    def export_jsonl(self, path: str = "data/memory_dump.jsonl"):
        self._ensure_connection()
        rows = self.conn.execute("SELECT * FROM memory").fetchall()
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(dict(zip(["id", "timestamp", "signal", "insight"], row))) + "\n")

    def export_csv(self, path: str = "data/memory_dump.csv"):
        self._ensure_connection()
        rows = self.conn.execute("SELECT * FROM memory").fetchall()
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "timestamp", "signal", "insight"])
            writer.writerows(rows)

    # ---- Placeholder: future learning and optimization ----

    def compress_memory(self):
        """Stub: reduce memory bloat by summarizing old entries"""
        pass

    def tag_signal(self, signal_id: int, tag: str):
        """Stub: tag memory entries for later clustering"""
        pass

    def vectorize(self):
        """Stub: optional hook for vector DB integration"""
        pass
