# SQL Injection — Login Bypass (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
part of the "Subverting application logic" section of the SQL
injection learning path. The lab simulates a login form vulnerable
to SQL injection in its authentication query.

## Objective

Perform a SQL injection attack that logs in to the application as
the `administrator` user, without knowing their password.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition), Firefox with the
  FoxyProxy extension for quick proxy switching

## Techniques Practiced

- Intercepting and modifying an HTTP `POST` request with Burp
  Suite's Proxy
- Managing Intercept state deliberately: leaving Intercept **off**
  while navigating/loading pages, and switching it **on** only
  immediately before submitting the request to be tampered with,
  to avoid having to forward every unrelated request (images,
  scripts, etc.) one at a time
- SQL injection via a vulnerable authentication query
- Using `'--` as a SQL comment to bypass a password check entirely
- Leaving unrelated request parameters (such as a CSRF token)
  untouched so the request is still accepted by the server

## Key Findings

The login form's authentication check was shaped like:

```sql
SELECT * FROM users WHERE username = 'administrator' AND password = 'whatever_was_typed'
```

For a login to succeed normally, **both** the username and password
conditions must be true. Submitting the login form with
`administrator` as the username and an arbitrary password produced
a `POST` request with a body like:

```
csrf=<token>&username=administrator&password=test
```

Intercepting this request in Burp and editing the `username` value
to:

```
administrator'--
```

changed the body to:

```
csrf=<token>&username=administrator'--&password=test
```

which changed the resulting query to:

```sql
SELECT * FROM users WHERE username = 'administrator'--' AND password = 'whatever_was_typed'
```

The `--` comments out everything after it, including the entire
`AND password = '...'` check. The database only ever evaluates
`WHERE username = 'administrator'`, which is true — so the
password submitted is never checked at all, and the request logs
in as `administrator` regardless of what was typed into the
password field. The CSRF token in the request body was left
unmodified throughout, since altering it would have caused the
server to reject the request independently of the SQL injection.

## What I Learned

This lab extended the comment-based injection technique from the
"Retrieving hidden data" lab to a different context: instead of
removing a filter condition on a product search, the same `--`
trick removes an entire authentication check. It reinforced that
the underlying technique — using a comment to discard the rest of
a query — is reusable across very different parts of an
application, not tied to one specific feature.

I also picked up a more efficient Burp Suite workflow in this lab:
rather than leaving Intercept on throughout and forwarding every
single request a page generates, it's far more practical to leave
Intercept **off** while a page loads normally, and switch it **on**
only right before performing the one action (submitting a form,
in this case) whose request you actually want to capture and edit.
This avoids needing to click "Forward" repeatedly on unrelated
requests like images, stylesheets, and scripts.

Finally, this lab was a reminder to pay attention to which
parameters in a request are safe to modify and which aren't — the
CSRF token had to be preserved exactly as issued, since it's a
session-specific, single-use value the server checks independently
of the SQL injection itself.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems or production data were involved.
