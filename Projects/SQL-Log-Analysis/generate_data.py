#!/usr/bin/env python3
"""
Generates a synthetic employees.csv and login_attempts.csv for the
SQL Log Analysis portfolio project.

The data is entirely fictional but is shaped to include a baseline of
normal login activity plus four deliberately embedded incident
patterns, so that the detection queries have something real to catch:

  1. Brute-force burst  -> one external IP hammering one username
                            with many failed logins in a short window
  2. Impossible travel  -> one legitimate user with successful logins
                            from two distant countries minutes apart
  3. Off-hours failures -> failed login attempts in the middle of the
                            night, local time, for one account
  4. Slow credential stuffing -> one account with an unusually high
                            total failure count spread across many
                            days (not a single burst)

A fixed random seed is used so the dataset — and therefore every
query result in the report — is reproducible.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = "data"

DEPARTMENTS = ["Marketing", "Finance", "Sales", "Engineering",
               "Information Technology", "Human Resources"]
OFFICES = ["East-101", "East-102", "West-201", "West-202",
           "North-301", "South-401"]
COUNTRIES = ["US", "CAN", "MEX", "GBR", "DEU", "GHA"]

FIRST_NAMES = ["alex", "jordan", "taylor", "morgan", "casey", "riley",
               "sam", "drew", "jamie", "avery", "quinn", "reese",
               "parker", "rowan", "skyler", "emerson", "hayden",
               "finley", "dakota", "kendall"]

NUM_EMPLOYEES = 20
START_DATE = datetime(2026, 9, 1)
NUM_DAYS = 14


def random_ip():
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}." \
           f"{random.randint(0, 255)}.{random.randint(1, 254)}"


def build_employees():
    employees = []
    used_usernames = set()
    for i in range(1, NUM_EMPLOYEES + 1):
        first = random.choice(FIRST_NAMES)
        username = f"{first}{i:02d}"
        while username in used_usernames:
            username = f"{first}{random.randint(1, 999)}"
        used_usernames.add(username)
        employees.append({
            "employee_id": i,
            "device_id": 1000 + i,
            "username": username,
            "department": random.choice(DEPARTMENTS),
            "office": random.choice(OFFICES),
            "home_country": random.choice(COUNTRIES),
        })
    return employees


def normal_logins(employees):
    """Baseline traffic: mostly successful, business-hours, home country."""
    events = []
    for day in range(NUM_DAYS):
        date = START_DATE + timedelta(days=day)
        for emp in employees:
            # not every employee logs in every day
            if random.random() > 0.75:
                continue
            hour = random.randint(8, 17)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            success = random.random() > 0.05  # occasional honest typo
            events.append({
                "username": emp["username"],
                "login_date": date.strftime("%Y-%m-%d"),
                "login_time": f"{hour:02d}:{minute:02d}:{second:02d}",
                "country": emp["home_country"],
                "ip_address": random_ip(),
                "success": success,
            })
    return events


def incident_brute_force(employees):
    """One attacker IP hammers one username with rapid failed attempts."""
    target = employees[3]["username"]
    attacker_ip = "185.220.101.47"
    date = (START_DATE + timedelta(days=5)).strftime("%Y-%m-%d")
    events = []
    base_minute = 14 * 60 + 10  # 14:10
    for i in range(18):
        minute_offset = base_minute + i  # roughly one attempt per minute
        hour, minute = divmod(minute_offset, 60)
        events.append({
            "username": target,
            "login_date": date,
            "login_time": f"{hour:02d}:{minute:02d}:{random.randint(0,59):02d}",
            "country": "RUS",
            "ip_address": attacker_ip,
            "success": False,
        })
    return events


def incident_impossible_travel(employees):
    """Same user, successful logins from two distant countries, minutes apart."""
    target = employees[7]["username"]
    date = (START_DATE + timedelta(days=8)).strftime("%Y-%m-%d")
    events = [
        {
            "username": target,
            "login_date": date,
            "login_time": "09:14:02",
            "country": "US",
            "ip_address": random_ip(),
            "success": True,
        },
        {
            "username": target,
            "login_date": date,
            "login_time": "09:27:48",
            "country": "VNM",
            "ip_address": random_ip(),
            "success": True,
        },
    ]
    return events


def incident_off_hours(employees):
    """Repeated failed logins in the middle of the night for one account."""
    target = employees[12]["username"]
    date = (START_DATE + timedelta(days=10)).strftime("%Y-%m-%d")
    events = []
    for i in range(4):
        hour = 2
        minute = 10 + i * 7
        events.append({
            "username": target,
            "login_date": date,
            "login_time": f"{hour:02d}:{minute:02d}:{random.randint(0,59):02d}",
            "country": employees[12]["home_country"],
            "ip_address": random_ip(),
            "success": False,
        })
    return events


def incident_slow_credential_stuffing(employees):
    """One account racks up an unusually high TOTAL failure count,
    spread thin across many days so no single day looks alarming."""
    target = employees[16]["username"]
    events = []
    for day in range(NUM_DAYS):
        if random.random() > 0.55:
            continue
        date = START_DATE + timedelta(days=day)
        hour = random.randint(8, 21)
        minute = random.randint(0, 59)
        events.append({
            "username": target,
            "login_date": date.strftime("%Y-%m-%d"),
            "login_time": f"{hour:02d}:{minute:02d}:{random.randint(0,59):02d}",
            "country": employees[16]["home_country"],
            "ip_address": random_ip(),
            "success": False,
        })
    return events


def main():
    employees = build_employees()

    all_events = []
    all_events += normal_logins(employees)
    all_events += incident_brute_force(employees)
    all_events += incident_impossible_travel(employees)
    all_events += incident_off_hours(employees)
    all_events += incident_slow_credential_stuffing(employees)

    # sort chronologically and assign event ids
    all_events.sort(key=lambda e: (e["login_date"], e["login_time"]))
    for idx, e in enumerate(all_events, start=1):
        e["event_id"] = idx

    with open(f"{OUT_DIR}/employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "employee_id", "device_id", "username", "department",
            "office", "home_country"])
        writer.writeheader()
        writer.writerows(employees)

    with open(f"{OUT_DIR}/login_attempts.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "event_id", "username", "login_date", "login_time",
            "country", "ip_address", "success"])
        writer.writeheader()
        for e in all_events:
            writer.writerow(e)

    print(f"Employees:      {len(employees)}")
    print(f"Login events:   {len(all_events)}")
    print("Wrote data/employees.csv and data/login_attempts.csv")


if __name__ == "__main__":
    main()
