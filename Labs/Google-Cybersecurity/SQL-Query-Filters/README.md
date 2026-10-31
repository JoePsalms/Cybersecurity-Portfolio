# Apply Filters to SQL Queries — Google Cybersecurity Professional Certificate

## Project Description

A guided project simulating a security investigation for an
organization, using filtered SQL queries against login and
employee data to identify suspicious activity and target
specific employee machines for security updates. Builds on the
table structure documented in the related
[SQL Queries](../SQL-Queries/README.md) project.

## Objective

- Filter login attempt data to investigate specific security
  incidents (after-hours failures, activity on specific dates,
  logins outside an expected country).
- Filter employee data to identify machines needing updates,
  based on department and office location.
- Apply `AND`, `OR`, `NOT`, and `LIKE` to narrow SQL query
  results to exactly what each task required.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment)
- Database: MariaDB
- Tool: MariaDB shell (SQL)

## Techniques Practiced

- Filtering with `WHERE`
- Combining conditions with `AND` / `OR`
- Negating conditions with `NOT`
- Pattern matching with `LIKE` and the `%` wildcard
- Comparing timestamps and dates in `WHERE` clauses

## Key Findings

**After-hours failed logins:** Filtered `log_in_attempts` for
records where `login_time > '18:00'` **and** `success = FALSE`,
to surface failed login attempts outside of business hours for
investigation.

**Logins on specific dates:** Filtered `log_in_attempts` for
`login_date = '2022-05-09'` **or** `login_date = '2022-05-08'`,
to review all login activity around the date of a reported
suspicious event.

**Logins outside Mexico:** Filtered `log_in_attempts` with
`NOT country LIKE 'MEX%'`, using the `%` wildcard since the
dataset represented Mexico inconsistently (`MEX` and `MEXICO`).

**Marketing employees in the East building:** Filtered
`employees` for `department = 'Marketing'` **and**
`office LIKE 'East%'`, to produce a targeted list of machines
to update.

**Finance or Sales employees:** Filtered `employees` for
`department = 'Finance'` **or** `department = 'Sales'`, to
combine two departments' machines into a single update list.

**Employees outside IT:** Filtered `employees` with
`NOT department = 'Information Technology'`, to identify every
machine needing a separate, non-IT-specific update.

## What I Learned

This project reinforced how choosing the right logical operator
changes query results dramatically — `AND` narrows results to
records meeting every condition, while `OR` broadens results to
records meeting any one of several conditions, and `NOT`
excludes records that would otherwise match. I also learned how
`LIKE` with the `%` wildcard handles inconsistent or partial
data (such as multiple representations of the same value, or
office numbers nested under a building name) that an exact-match
filter would miss.

## Ethical Considerations

This exercise was performed in an authorized, sandboxed guided
lab environment using simulated organizational data. No
production systems or real user data were involved.

## Note

Lab-specific screenshots and raw terminal output have been
summarized rather than reproduced verbatim in this public
write-up.
