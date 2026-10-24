import sqlite3

DB_FILE = "api_monitor.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
    SELECT url,
           COUNT(*) AS total_checks,
           ROUND(AVG(response_time_ms), 2) AS avg_ms,
           MAX(response_time_ms) AS max_ms,
           SUM(is_error) AS errors
    FROM api_logs
    GROUP BY url
""")

print("=" * 70)
print("API PERFORMANCE REPORT")
print("=" * 70)
for url, total, avg_ms, max_ms, errors in cur.fetchall():
    error_rate = round(errors / total * 100, 1)
    print(f"URL          : {url}")
    print(f"Total checks : {total}")
    print(f"Avg response : {avg_ms} ms")
    print(f"Max response : {max_ms} ms")
    print(f"Errors       : {errors} ({error_rate}%)")
    print("-" * 70)

conn.close()