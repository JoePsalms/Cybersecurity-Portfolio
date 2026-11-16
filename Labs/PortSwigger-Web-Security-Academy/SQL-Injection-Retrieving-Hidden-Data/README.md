# SQL Injection — Retrieving Hidden Data (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
part of the SQL injection topic. The lab simulates an e-commerce
site with a product category filter that is vulnerable to SQL
injection in its `WHERE` clause.

## Objective

Perform a SQL injection attack that causes the application to
display one or more unreleased products that would not normally
be visible through the category filter.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition), Firefox configured to
  proxy through Burp

## Techniques Practiced

- Intercepting and modifying HTTP requests with Burp Suite's Proxy
- Configuring a browser (Firefox) to route traffic through a local
  proxy, including importing Burp's CA certificate for HTTPS
  interception
- SQL injection via a vulnerable `WHERE` clause
- Using `OR 1=1` to make a `WHERE` condition unconditionally true
- Using `--` as a SQL comment to discard the remainder of a query

## Key Findings

The application filtered products with a query shaped like:

```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

The `category` parameter was passed directly into this query
without sanitization. Intercepting the request that sets the
category filter (`GET /filter?category=Gifts`) with Burp Suite and
modifying the parameter to:

```
category=Gifts'+OR+1=1--
```

changed the resulting query to:

```sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
```

Since `1=1` evaluates to true for every row, and `OR` only requires
one side of the condition to be true, the entire `WHERE` clause
became true for every row in the table regardless of its actual
category. The trailing `--` commented out the rest of the query,
removing the `AND released = 1` check as well. Forwarding the
modified request returned products from every category, including
unreleased ones, solving the lab.

## What I Learned

This lab was my first hands-on SQL injection, and most of the
actual learning curve was in the tooling rather than the SQL
itself: configuring Firefox to proxy through Burp Suite, importing
Burp's CA certificate so HTTPS traffic could be intercepted without
warnings, and getting comfortable pausing, editing, and forwarding
a request in Burp's Intercept tab. That workflow — proxy → capture
→ edit → forward — is the same one I'll reuse for every lab going
forward.

On the SQL side, the key realization was how `OR 1=1` works: it
doesn't change what data exists, it changes the *logic* of the
`WHERE` clause so that the condition is satisfied for every row,
regardless of the actual column values. Combined with `--` to
discard anything after the injection point, this is enough to
bypass a filter entirely without needing to know the real
category values.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems or production data were involved.
