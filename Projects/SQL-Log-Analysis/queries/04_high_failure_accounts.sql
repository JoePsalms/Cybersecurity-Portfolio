-- 04_high_failure_accounts.sql
--
-- Detects accounts with an unusually high TOTAL number of failed
-- login attempts across the whole monitoring period, even if those
-- failures are spread thinly across many days (which would let them
-- slip past a single-day burst query like 01_brute_force.sql). This
-- is meant to catch slow, low-and-slow credential stuffing against
-- one account rather than a loud, fast attack.

SELECT
    username,
    COUNT(*)                                   AS total_failed_attempts,
    COUNT(DISTINCT login_date)                  AS days_with_failures,
    COUNT(DISTINCT ip_address)                  AS distinct_source_ips
FROM login_attempts
WHERE success = 0
GROUP BY username
HAVING COUNT(*) >= 5
ORDER BY total_failed_attempts DESC;
