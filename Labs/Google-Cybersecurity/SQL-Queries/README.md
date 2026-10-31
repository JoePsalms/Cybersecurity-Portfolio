# SQL Query Portfolio — Table Formats — Google Cybersecurity Professional Certificate

## Project Description

A guided project exploring the structure of an organization's
database in preparation for writing security-related SQL
queries against it. The database contains two tables,
`log_in_attempts` and `employees`, used throughout this and
related SQL exercises.

## Objective

- Identify the tables available in the organization database.
- Document the columns and purpose of each table.
- Confirm table structure directly in the MariaDB shell.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment)
- Database: MariaDB
- Tool: MariaDB shell (SQL)

## Techniques Practiced

- Querying a database's schema/column structure
- Documenting table design for reference in later queries
- Working in the MariaDB command-line shell

## Key Findings

The database contains two relevant tables:

**`log_in_attempts`** — records login activity, with columns
for `event_id`, `username`, `login_date`, `login_time`,
`country`, `ip_address`, and `success` (a boolean where `FALSE`
indicates a failed login attempt).

**`employees`** — records employee and device information, with
columns for `employee_id`, `device_id`, `username`,
`department`, and `office`.

Both table structures were confirmed directly in the MariaDB
shell, returning each column name as stored in the database.
This schema became the foundation for the filtered security
queries written in the related
[SQL Query Filters](../SQL-Query-Filters/README.md) project.

## What I Learned

This project reinforced the importance of understanding a
database's schema before writing queries against it — knowing
exactly which columns exist, their purpose, and their expected
values (such as `success` being boolean) makes it possible to
write accurate, targeted SQL later rather than guessing at
column names or data formats.

## Ethical Considerations

This exercise was performed in an authorized, sandboxed guided
lab environment using simulated organizational data. No
production systems or real user data were involved.

## Note

Lab-specific screenshots and raw terminal output have been
summarized rather than reproduced verbatim in this public
write-up.
