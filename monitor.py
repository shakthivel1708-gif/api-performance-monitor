import requests
import sqlite3
import schedule
import time
from datetime import datetime

DB_FILE = "api_monitor.db"

# APIs to monitor (free public APIs for practice)
APIS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://api.github.com",
    "https://httpbin.org/status/500",  # intentionally returns error
]


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            status_code INTEGER,
            response_time_ms REAL,
            is_error INTEGER,
            checked_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def check_api(url):
    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed_ms = round((time.time() - start) * 1000, 2)
        status = response.status_code
        is_error = 1 if status >= 400 else 0
    except Exception:
        status = 0
        elapsed_ms = 0
        is_error = 1

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO api_logs (url, status_code, response_time_ms, is_error, checked_at) VALUES (?, ?, ?, ?, ?)",
        (url, status, elapsed_ms, is_error, checked_at),
    )
    conn.commit()
    conn.close()
    print(f"[{checked_at}] {url} -> {status} ({elapsed_ms} ms)")


def run_checks():
    print("Checking APIs...")
    for url in APIS:
        check_api(url)
    print()


if __name__ == "__main__":
    init_db()
    run_checks()  # run once immediately
    schedule.every(1).minutes.do(run_checks)
    print("Monitor running... Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)