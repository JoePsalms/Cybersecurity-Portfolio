-- 03_off_hours_failures.sql
--
-- Detects failed login attempts that occurred late at night
-- (00:00-05:00), when legitimate employee activity is unlikely.
-- Grouped per user/day so a single overnight failure doesn't stand
-- out as much as a repeated pattern does.

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
