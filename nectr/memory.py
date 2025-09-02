import sqlite3
from datetime import datetime
from pathlib import Path
import json
import csv
import logging # Added import

class MemoryManager:
    def __init__(self, config: dict):
        self.config = config
        self.db_path = config.get("path", "data/memory.sqlite")
        self.conn = None # Initialize connection to None
        self._initialize()

    def _initialize(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        try:
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
        except sqlite3.Error as e:
            logging.error(f"Error initializing memory database at {self.db_path}: {e}")
            self.conn = None # Ensure connection is closed or set to None on error

    def _ensure_connection(self):
        if self.conn is None:
            self._initialize()
        try:
            # Test connection by executing a simple query
            self.conn.execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
            logging.warning(f"Lost connection to memory database. Re-initializing: {e}")
            self._initialize()

    def store(self, signal: str, insight: str):
        self._ensure_connection()
        if self.conn: # Only proceed if connection is valid
            try:
                self.conn.execute(
                    "INSERT INTO memory (timestamp, signal, insight) VALUES (?, ?, ?)",
                    (datetime.now().isoformat(), signal, insight)
                )
                self.conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error storing data to memory: {e}")

    def fetch_recent(self, limit: int = 10):
        self._ensure_connection()
        if self.conn:
            try:
                return self.conn.execute(
                    "SELECT timestamp, signal, insight FROM memory ORDER BY id DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            except sqlite3.Error as e:
                logging.error(f"Error fetching recent data from memory: {e}")
                return []
        return []

    def fetch_by_time_range(self, start_time: str, end_time: str):
        self._ensure_connection()
        if self.conn:
            try:
                return self.conn.execute(
                    "SELECT * FROM memory WHERE timestamp BETWEEN ? AND ?",
                    (start_time, end_time)
                ).fetchall()
            except sqlite3.Error as e:
                logging.error(f"Error fetching data by time range from memory: {e}")
                return []
        return []

    def search_by_keyword(self, keyword: str):
        self._ensure_connection()
        if self.conn:
            try:
                return self.conn.execute(
                    "SELECT * FROM memory WHERE signal LIKE ? OR insight LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                ).fetchall()
            except sqlite3.Error as e:
                logging.error(f"Error searching data by keyword from memory: {e}")
                return []
        return []

    def export_jsonl(self, path: str = "data/memory_dump.jsonl"):
        self._ensure_connection()
        if self.conn:
            try:
                rows = self.conn.execute("SELECT * FROM memory").fetchall()
                with open(path, "w", encoding="utf-8") as f:
                    for row in rows:
                        f.write(json.dumps(dict(zip(["id", "timestamp", "signal", "insight"], row))) + "\n")
            except (sqlite3.Error, IOError) as e:
                logging.error(f"Error exporting memory to JSONL: {e}")

    def export_csv(self, path: str = "data/memory_dump.csv"):
        self._ensure_connection()
        if self.conn:
            try:
                rows = self.conn.execute("SELECT * FROM memory").fetchall()
                with open(path, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "timestamp", "signal", "insight"])
                    writer.writerows(rows)
            except (sqlite3.Error, IOError) as e:
                logging.error(f"Error exporting memory to CSV: {e}")

    # ---- Placeholder: future learning and optimization ----

    def compress_memory():
        """Stub: reduce memory bloat by summarizing old entries"""
        pass

    def tag_signal(self, signal_id: int, tag: str):
        """Stub: tag memory entries for later clustering"""
        pass

    def vectorize():
        """Stub: optional hook for vector DB integration"""
        pass