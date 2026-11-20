# SQL Injection UNION Attack — Retrieving Data from Other Tables (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
the third lab in the "SQL injection UNION attacks" section. This
lab is where the previous two labs' techniques come together for
the first time to achieve an actual data breach: using a UNION
attack to pull real credentials out of a `users` table, then using
one of those credentials to log in as the administrator.

## Objective

Perform a SQL injection UNION attack that retrieves all usernames
and passwords from the application's `users` table, then use the
exposed administrator credentials to log in as `administrator`.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition) — Proxy and Repeater,
  Firefox with FoxyProxy

## Techniques Practiced

- Confirming the query's column count and string-compatible columns
  using the same `UNION SELECT` placeholder technique from the two
  previous labs (tested with `'abc','def'` in place of `NULL`s to
  confirm both columns accept strings)
- Extracting real data from a different table (`users`) entirely,
  rather than just proving a column's data type
- Reading multiple rows of extracted data directly off the
  application's rendered page
- Falling back on extracted data (a real password) when a previously
  learned technique (the `administrator'--` comment-based login
  bypass) didn't apply to this lab

## Key Findings

With the column count and string compatibility already confirmed,
the final payload used was:

```
'+UNION+SELECT+username,+password+FROM+users--
```

This returned every row of the `users` table — usernames in one
column, passwords in the other — directly on the product listing
page, including a row for `administrator` with their actual
password.

Before reaching that final payload, I first tried the login-bypass
technique from the earlier "Login Bypass" lab
(`administrator'--`), assuming it might apply here too — it didn't
work for this lab's setup. Rather than getting stuck on that, I
moved on, ran the UNION payload above, and noticed the
administrator's password sitting right there in the dumped results.
Logging in with `administrator` and that password solved the lab.

## What I Learned

This lab was the payoff for the two UNION labs before it: having
already confirmed the column count and which column accepts
strings, actually extracting real data was just a matter of
swapping the test placeholders (`'abc'`, `'def'`) for genuine column
names (`username`, `password`) from a table I knew existed. It
reinforced that a UNION attack's setup work (columns, types) isn't
the goal in itself — it's the groundwork that makes the real
extraction trivial once it's done.

The more important lesson, though, was realizing that not every
technique from an earlier lab transfers directly to a new one. When
the comment-based login bypass didn't work here, the right move
wasn't to keep forcing it — it was to recognize that this lab's
vulnerability (UNION-based data extraction) was a completely
different attack surface from the login form's injection, and that
the data I'd already pulled out of the database was the actual key
to solving it. In a real engagement, that's exactly how an attacker
would pivot: use whatever a successful injection exposes, rather
than assuming one exploit technique applies everywhere.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems, production data, or real user
credentials were involved.
