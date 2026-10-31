# SQL Log Analysis — Suspicious Login Detection

## Project Overview

A self-directed project built to practice SQL-based log analysis,
the kind of work a junior SOC analyst does when triaging
authentication logs for suspicious activity. Rather than analyzing
a pre-made dataset with pre-written questions, I built the whole
pipeline myself: generated a synthetic login-activity dataset with
known security incidents hidden inside it, loaded it into a SQLite
database, wrote detection queries from scratch, and verified that
each query actually caught what it was designed to catch.

This builds directly on the SQL and Linux skills from the Google
Cybersecurity Professional Certificate, applied to an original
scenario rather than a guided lab.

## Objective

Simulate the first step of an authentication-log investigation:
given two tables of login activity and employee data, write SQL
queries that surface four common classes of suspicious login
behavior, without relying on any single log line standing out on
its own.

## Dataset

A synthetic dataset was generated with Python (`generate_data.py`,
fixed random seed for reproducibility):

- **20 employees** (`employees.csv`) — department, office, and home
  country for each.
- **239 login events** (`login_attempts.csv`) over a 14-day period —
  mostly realistic baseline traffic (business-hours logins, occasional
  honest failed attempts), with four incidents deliberately embedded:

| # | Incident type | What was embedded |
|---|---|---|
| 1 | Brute-force burst | One external IP sends 18 failed login attempts against a single username in 17 minutes |
| 2 | Impossible travel | One user has two successful logins, 13.8 minutes apart, from the US and Vietnam |
| 3 | Off-hours failures | One account has 4 failed logins between 02:10 and 02:31 local time |
| 4 | Slow credential stuffing | One account accumulates 7 failed logins spread across 7 different days from 7 different IPs — no single day looks alarming on its own |

The data was loaded into a local SQLite database
(`security_logs.db`) with two tables: `employees` and
`login_attempts`.

## Detection Queries

### 1. Brute-force detection

Groups failed logins by username, source IP, and day, flagging any
combination with 10 or more failures — the signature of a scripted
attack hammering one account from one source, rather than a person
mistyping their password a couple of times.

```sql
SELECT
    username,
    ip_address,
    login_date,
    COUNT(*)            AS failed_attempts,
    MIN(login_time)      AS first_attempt,
    MAX(login_time)      AS last_attempt
FROM login_attempts
WHERE success = 0
GROUP BY username, ip_address, login_date
HAVING COUNT(*) >= 10
ORDER BY failed_attempts DESC;
```

**Result:**

| username | ip_address | login_date | failed_attempts | first_attempt | last_attempt |
|---|---|---|---|---|---|
| taylor04 | 185.220.101.47 | 2026-09-06 | 18 | 14:10:20 | 14:27:08 |

### 2. Impossible travel

Self-joins the login table against itself on username, pairing every
successful login with a later successful login by the same user, and
flags pairs where the country changed within 60 minutes — too short
a window for a real person to have actually traveled between the two
locations.

```sql
SELECT
    a.username,
    a.login_date,
    a.login_time AS first_login_time,
    a.country    AS first_country,
    b.login_time AS second_login_time,
    b.country    AS second_country,
    ROUND(
        (JULIANDAY(b.login_date || ' ' || b.login_time) -
         JULIANDAY(a.login_date || ' ' || a.login_time)) * 24 * 60,
        1
    ) AS minutes_apart
FROM login_attempts a
JOIN login_attempts b
    ON a.username = b.username
   AND a.event_id < b.event_id
   AND a.success = 1
   AND b.success = 1
   AND a.country <> b.country
WHERE
    (JULIANDAY(b.login_date || ' ' || b.login_time) -
     JULIANDAY(a.login_date || ' ' || a.login_time)) * 24 * 60 <= 60
ORDER BY minutes_apart ASC;
```

**Result:**

| username | login_date | first_login_time | first_country | second_login_time | second_country | minutes_apart |
|---|---|---|---|---|---|---|
| finley08 | 2026-09-09 | 09:14:02 | US | 09:27:48 | VNM | 13.8 |

### 3. Off-hours failed logins

Flags failed login attempts between midnight and 05:00, grouped per
user per day, since legitimate employee activity in that window is
unlikely.

```sql
SELECT
    username,
    login_date,
    COUNT(*)        AS off_hours_failed_attempts,
    MIN(login_time)  AS first_attempt,
    MAX(login_time)  AS last_attempt
FROM login_attempts
WHERE success = 0
  AND login_time >= '00:00:00'
  AND login_time <  '05:00:00'
GROUP BY username, login_date
ORDER BY off_hours_failed_attempts DESC;
```

**Result:**

| username | login_date | off_hours_failed_attempts | first_attempt | last_attempt |
|---|---|---|---|---|
| kendall13 | 2026-09-11 | 4 | 02:10:20 | 02:31:19 |

### 4. High total failure count (slow credential stuffing)

Catches accounts with an unusually high total number of failures
across the whole monitoring period, even when those failures are
spread thin across many days — a pattern the single-day burst query
above would miss entirely.

```sql
SELECT
    username,
    COUNT(*)                     AS total_failed_attempts,
    COUNT(DISTINCT login_date)    AS days_with_failures,
    COUNT(DISTINCT ip_address)    AS distinct_source_ips
FROM login_attempts
WHERE success = 0
GROUP BY username
HAVING COUNT(*) >= 5
ORDER BY total_failed_attempts DESC;
```

**Result:**

| username | total_failed_attempts | days_with_failures | distinct_source_ips |
|---|---|---|---|
| taylor04 | 18 | 1 | 1 |
| taylor17 | 7 | 7 | 7 |

This query also re-surfaced `taylor04` (the brute-force account from
query 1) — which is expected, since 18 failures in one day is also a
high total. The useful signal here is the shape of the data, not just
the count: `taylor04`'s failures came from **1 day and 1 IP** (a
fast, loud burst), while `taylor17`'s came from **7 days and 7
different IPs** (a slow, distributed pattern). The same query flagged
two genuinely different attack styles, and the extra columns are what
let an analyst tell them apart.

## Findings Summary

| Account | Behavior observed | Likely explanation |
|---|---|---|
| taylor04 | 18 failed logins in 17 minutes from one foreign IP | Automated brute-force attempt |
| finley08 | Successful logins from US and Vietnam 13.8 minutes apart | Compromised credentials used from two locations, or a VPN/location-spoofing artifact worth confirming with the user |
| kendall13 | 4 failed logins between 02:10–02:31 local time | Possible credential-testing outside business hours |
| taylor17 | 7 failed logins spread across 7 days, 7 different IPs | Slow, distributed credential-stuffing attempt designed to avoid burst-detection thresholds |

## Recommendations

- **taylor04 / brute-force IP:** Lock the account pending password
  reset; block or rate-limit the source IP at the firewall.
- **finley08 / impossible travel:** Contact the employee directly to
  confirm legitimate travel or VPN use before assuming compromise;
  if unconfirmed, force a password reset and review recent account
  activity for further anomalies.
- **kendall13 / off-hours failures:** Confirm whether the employee
  was legitimately working off-hours; if not, treat as a possible
  credential-testing attempt and monitor for recurrence.
- **taylor17 / distributed failures:** Flag for monitoring even
  though no single day crossed a burst threshold — the pattern itself
  (many IPs, many days, one account) is the indicator, and most
  single-day alerting rules would miss it.
- **General:** A real deployment would run these queries on a
  schedule (e.g., daily) against live log data rather than a static
  snapshot, and would tune thresholds (10 failures/day, 60-minute
  travel window, 5 total failures) against the organization's actual
  traffic patterns to reduce false positives.

## What I Learned

Building the dataset myself — rather than analyzing one that was
handed to me — made it clear how much query design depends on
knowing what pattern you're actually looking for. A single
`COUNT(*)` threshold works for a loud, fast brute-force attempt but
completely misses a slow, distributed one; catching both required
two different queries grouped on different dimensions (IP/day vs.
total-over-all-time).

The impossible-travel query was the most interesting to write: it
needed a self-join on the same table, matched on username, with a
time-difference calculation across two separate date+time columns.
Working out the `JULIANDAY()` arithmetic to get a clean "minutes
apart" value was good practice in handling time-based correlation in
SQL rather than just filtering single rows.

I also learned to design synthetic test data with the detection
queries in mind — placing one deliberately overlapping case
(`taylor04` showing up in two queries) turned out to be a useful,
realistic complication rather than a bug, since real investigations
often involve the same account triggering more than one alert.

## Tools Used

- Python (data generation, SQLite query execution)
- SQLite
- SQL (joins, aggregation, `HAVING`, `JULIANDAY()` time arithmetic)

## Ethical Considerations

All data in this project is synthetic and randomly generated for
the purpose of this exercise. No real employee, login, or IP address
data was used.

## Project Files

- `generate_data.py` — generates the synthetic dataset
- `build_db.py` — loads the CSV data into a SQLite database
- `data/employees.csv`, `data/login_attempts.csv` — the generated data
- `queries/` — the four detection queries
- `run_queries.py` — runs every query and prints/saves formatted results
- `results/` — saved output from each query

## How to Run

```bash
python3 generate_data.py   # regenerates data/employees.csv and data/login_attempts.csv
python3 build_db.py        # builds security_logs.db from the CSV data
python3 run_queries.py     # runs every query in queries/ and writes output to results/
```

The dataset is generated with a fixed random seed, so re-running
`generate_data.py` reproduces the exact same data — and the exact
same query results — shown in this write-up.
