# API Performance Monitor

## Description
A Python tool that monitors the performance of web APIs. It checks
each API on a schedule, records the response time and status code in
SQLite, and generates a performance report.

## Technologies
- Python
- Requests
- SQLite
- Schedule

## Features
- Monitors multiple APIs automatically every 1 minute
- Records status code and response time (ms)
- Flags errors (status 400+ or failed requests)
- Report with average time, max time, and error rate per API

## How to Run
1. Install libraries:
   pip install requests schedule
2. Start the monitor:
   python monitor.py
3. Press Ctrl+C to stop after a few minutes.
4. Generate the report:
   python report.py

## Files
- monitor.py : checks APIs on a schedule and logs results
- report.py : generates the performance report
- api_monitor.db : SQLite database with logs

## Outcome
Monitor response times, API errors, and generate performance insights.
