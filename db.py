import sqlite3
from contextlib import contextmanager

from config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature TEXT,
    cpu_usage REAL,
    ram_usage REAL,
    ping_time REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""


@contextmanager
def get_connection():
    conn = sqlite3.connect(settings.db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute(SCHEMA)
        conn.commit()


def insert_measurement(temperature, cpu_usage, ram_usage, ping_time):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO data (temperature, cpu_usage, ram_usage, ping_time) VALUES (?, ?, ?, ?)",
            (temperature, cpu_usage, ram_usage, ping_time),
        )
        conn.commit()


def get_latest():
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT temperature, cpu_usage, ram_usage, ping_time FROM data ORDER BY timestamp DESC LIMIT 1"
        )
        return cursor.fetchone()
