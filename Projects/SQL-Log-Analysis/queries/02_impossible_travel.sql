-- 02_impossible_travel.sql
--
-- Detects "impossible travel": the same user successfully logging in
-- from two different countries within a window too short for a real
-- person to have actually traveled between them (here, under 60
-- minutes). A self-join pairs up every successful login with every
-- later successful login by the same user, then filters for a
-- country change inside that window.

SELECT
    a.username,
    a.login_date,
    a.login_time        AS first_login_time,
    a.country            AS first_country,
    b.login_time        AS second_login_time,
    b.country             AS second_country,
    ROUND(
        (JULIANDAY(b.login_date || ' ' || b.login_time) -
         JULIANDAY(a.login_date || ' ' || a.login_time)) * 24 * 60,
        1
    )                     AS minutes_apart
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
