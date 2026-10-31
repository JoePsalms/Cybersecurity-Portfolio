#!/usr/bin/env python3
"""Builds security_logs.db (SQLite) from the CSV files in data/."""

import csv
import sqlite3

DB_PATH = "security_logs.db"

SCHEMA = """
DROP TABLE IF EXISTS login_attempts;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id   INTEGER PRIMARY KEY,
    device_id     INTEGER,
    username      TEXT UNIQUE,
    department    TEXT,
    office        TEXT,
    home_country  TEXT
);

CREATE TABLE login_attempts (
    event_id    INTEGER PRIMARY KEY,
    username    TEXT,
    login_date  TEXT,
    login_time  TEXT,
    country     TEXT,
    ip_address  TEXT,
    success     INTEGER  -- 0 = failed, 1 = succeeded
);
"""


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    with open("data/employees.csv") as f:
        reader = csv.DictReader(f)
        rows = [(r["employee_id"], r["device_id"], r["username"],
                  r["department"], r["office"], r["home_country"])
                 for r in reader]
        cur.executemany(
            "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", rows)

    with open("data/login_attempts.csv") as f:
        reader = csv.DictReader(f)
        rows = [(r["event_id"], r["username"], r["login_date"],
                  r["login_time"], r["country"], r["ip_address"],
                  1 if r["success"] == "True" else 0)
                 for r in reader]
        cur.executemany(
            "INSERT INTO login_attempts VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows)

    conn.commit()

    emp_count = cur.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    login_count = cur.execute(
        "SELECT COUNT(*) FROM login_attempts").fetchone()[0]
    print(f"Loaded {emp_count} employees, {login_count} login attempts "
          f"into {DB_PATH}")

    conn.close()


if __name__ == "__main__":
    main()
