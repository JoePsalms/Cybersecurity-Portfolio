# SQL Injection UNION Attack — Retrieving Multiple Values in a Single Column (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
the fourth lab in the "SQL injection UNION attacks" section. It
extends the previous "Retrieving data from other tables" lab by
solving a new problem: what to do when the vulnerable query only
has **one** string-compatible column, but you need to extract
**multiple** values (such as a username and a password) at once.

## Objective

Perform a SQL injection UNION attack that retrieves multiple
values from the `users` table — usernames and passwords — within
a single string-compatible column, then use the exposed
administrator credentials to log in as `administrator`.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition) — Proxy and Repeater,
  Firefox with FoxyProxy

## Techniques Practiced

- Confirming the query's column count and string-compatible column
  using the same `UNION SELECT` placeholder technique from previous
  labs
- Using the `||` string concatenation operator to combine two
  column values (`username` and `password`) into a single text
  value, with a separator character (`~`) in between so the two
  fields stay distinguishable in the output
- Reading multiple concatenated rows off the rendered page to
  identify the administrator's credentials among them
- Recognizing that the lab's actual solve condition was logging in
  specifically as `administrator`, not merely demonstrating that
  other extracted credentials could log in successfully

## Key Findings

With only 2 columns returned by the query and column 2 confirmed as
string-compatible (tested first with
`'+UNION+SELECT+NULL,'abc'--`), there was no second string column
available to hold a password separately from a username the way the
previous lab did. The fix was to combine both values into the one
available column using string concatenation:

```
'+UNION+SELECT+NULL,username||'~'||password+FROM+users--
```

This returned every row of the `users` table as a single
`username~password` string per row, displayed in column 2 of the
page. Scanning through the output for the `administrator` row
revealed their password alongside it.

## What I Learned

This lab's real lesson was about working within a constraint rather
than learning a new exploit primitive: concatenation (`||`) isn't a
new injection technique on its own, it's a practical workaround for
when a UNION attack has fewer string-compatible columns than the
number of values you need to extract. Pairing two fields together
with a separator character kept the output readable enough to pick
out the value that mattered.

The other thing worth noting from this attempt: logging in with
*any* valid username/password pair pulled from the dump succeeded
as a login, but didn't solve the lab. Only logging in specifically
as `administrator` did. It was a good reminder that a lab's (or a
real engagement's) actual objective can be narrower than "any
successful exploitation" — here the goal was specifically
administrator-level access, so a successful login with a
lower-privileged account, while technically a result of the same
vulnerability, wasn't the thing being measured.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems, production data, or real user
credentials were involved.
