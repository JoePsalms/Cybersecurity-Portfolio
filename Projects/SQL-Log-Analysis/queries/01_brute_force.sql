-- 01_brute_force.sql
--
-- Detects brute-force activity: a single username targeted by many
-- failed login attempts from the same source IP on the same day.
-- A legitimate user mistyping their password a couple of times
-- shouldn't trip this; a scripted attack hammering one account
-- should.

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
