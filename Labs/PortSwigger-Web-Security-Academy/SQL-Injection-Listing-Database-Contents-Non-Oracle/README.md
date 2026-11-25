# SQL Injection Attack — Listing the Database Contents on Non-Oracle Databases (Practitioner)

## Lab Overview

A Practitioner-level lab from PortSwigger's Web Security Academy —
a step up from the Apprentice UNION-attack labs completed so far.
Unlike those earlier labs, nothing here is handed to you: there's
no known table or column name to target. The whole point is to
enumerate the database's own schema information first, using SQL
injection against `information_schema`, before the actual
credential extraction can happen at all.

## Objective

Using SQL injection, enumerate the names of all tables in the
database, identify a table holding user credentials, discover its
column names, extract the administrator's password, and log in as
`administrator`.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition) — Proxy and Repeater,
  Firefox with FoxyProxy

## Techniques Practiced

- Querying `information_schema.tables` via a UNION attack to list
  every table in the database
- Filtering that enumeration down to just the application's own
  tables with `WHERE table_schema = current_schema()`, since an
  unfiltered query returns hundreds of the database engine's own
  internal system tables (PostgreSQL's `pg_*` tables and other
  `information_schema` views) mixed in with genuine application
  data, making the real table hard to spot
- Querying `information_schema.columns` filtered by `table_name` to
  discover a specific table's column names once the table itself
  was identified
- Chaining three separate UNION injections together — one to find
  the table, one to find its columns, one to dump the data — since
  table and column names here are randomized specifically to
  prevent guessing them

## Key Findings

The first enumeration attempt was unfiltered:

```
'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--
```

This returned a huge list of tables, but almost all of them were
PostgreSQL's own internal catalog tables (`pg_event_trigger`,
`pg_amop`, `schemata`, `routines`, and so on) — metadata about the
database engine itself, not application data. Scrolling through
that list to find anything useful wasn't practical.

Filtering to the application's own schema fixed this:

```
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables+WHERE+table_schema=current_schema()--
```

This immediately surfaced the real table: `users_mylmba` — a
randomized name, confirming table names can't simply be guessed in
this lab and have to be discovered.

With the table name known, its columns were enumerated the same
way:

```
'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_mylmba'--
```

which revealed two randomized column names: `username_tcflpt` and
`password_mmeztl`. The final extraction combined all three pieces
of discovered information into one payload:

```
GET /filter?category=Gifts'+UNION+SELECT+username_tcflpt,+password_mmeztl+FROM+users_mylmba-- HTTP/2
```

This returned every username/password pair in the table, displayed
inline among the normal product listings. Locating the
`administrator` row and using its password to log in solved the
lab.

## What I Learned

This lab was a genuine step beyond the earlier UNION-attack labs:
those gave you the table and column names up front, so the only
problem to solve was column count and type compatibility. Here,
*nothing* is known in advance — the real skill being tested is
using the database's own metadata (`information_schema`) as a
reconnaissance tool against itself, one query at a time, before any
actual data extraction becomes possible.

The biggest practical lesson was the importance of filtering the
`information_schema.tables` query by schema. An unfiltered query
technically "works" (no error, data returned), but it buries the
one table that matters under hundreds of internal engine tables
that have nothing to do with the application. Knowing that
`information_schema` and `pg_catalog` hold engine metadata, while
application tables live in the `public` schema (or more generally,
whatever `current_schema()` returns), turned an unusable wall of
output into a two-row answer.

It was also a good reminder that these labs deliberately randomize
table and column names precisely to stop shortcuts like guessing
`users`/`username`/`password` outright — the enumeration steps
aren't busywork, they're the actual vulnerability being exploited:
the database will honestly answer any question you ask it about
its own structure, if the query injection point lets you ask.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems, production data, or real user
credentials were involved.
