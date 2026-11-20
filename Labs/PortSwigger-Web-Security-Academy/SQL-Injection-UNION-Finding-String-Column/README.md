# SQL Injection UNION Attack — Finding a Column Containing Text (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
the second lab in the "SQL injection UNION attacks" section. It
builds directly on the previous lab's technique for determining a
query's column count, adding the next logical step of a UNION
attack: once the number of columns is known, each column has to be
tested to see which ones can hold string data before real data can
be extracted from other tables via that column.

## Objective

Using a SQL injection UNION attack, identify which column returned
by the product category filter's query is compatible with string
data, by making a lab-provided random value appear in the page's
output.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition) — Proxy and Repeater,
  Firefox with FoxyProxy

## Techniques Practiced

- Reusing the `ORDER BY`/`UNION SELECT NULL,...--` column-counting
  technique from the previous lab to confirm the query returns 3
  columns
- Substituting a `NULL` placeholder with a literal string value, one
  column position at a time, to test which column accepts string
  data
- Reading the rendered page to confirm whether an injected string
  value appears in the output, rather than relying on the HTTP
  status code alone
- Iterating a UNION payload in Burp Suite's Repeater tool

## Key Findings

Starting from the baseline payload used to confirm the column
count:

```
category=Gifts'+UNION+SELECT+NULL,NULL,NULL--
```

each `NULL` is a placeholder for a column whose data type isn't yet
known. To find out which of the 3 columns can hold a string, the
lab provides a random value to inject and look for in the response.
Replacing the `NULL` in the second position with that value:

```
category=Gifts'+UNION+SELECT+NULL,'BNrkb2',NULL--
```

returned the value `BNrkb2` visibly on the page, confirming that
**column 2** is compatible with string data. Had that column not
accepted a string, the database would have thrown a type-conversion
error instead, which would have ruled it out and pointed to testing
the next position.

## What I Learned

This lab was a direct, logical extension of the previous one rather
than a new technique on its own: the column count found via `ORDER
BY`/`UNION SELECT NULL,...` isn't the end goal, it's a prerequisite
for the real objective of a UNION attack — getting data of a
specific type to actually show up in the response. Since a UNION
SELECT has to match the original query's column count *and* have
compatible data types in each position, testing each `NULL` one at
a time with a real string value is the natural next step once the
count is known.

It also reinforced something from the previous lab: checking the
response content (the rendered page, not just a 200 vs. 500 status
code) is what confirms success here — a 200 response alone doesn't
guarantee the string actually landed in a visible column, only that
the column count and type were syntactically acceptable.

Solving this one went noticeably more smoothly than the previous
lab, since the proxy and Repeater workflow (editing in place,
checking the Response/Render tab) was already familiar from
troubleshooting the column-count lab.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems or production data were involved.
