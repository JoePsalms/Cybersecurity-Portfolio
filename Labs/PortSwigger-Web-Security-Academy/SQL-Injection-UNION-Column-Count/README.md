# SQL Injection UNION Attack — Determining the Number of Columns Returned by the Query (Apprentice)

## Lab Overview

An Apprentice-level lab from PortSwigger's Web Security Academy,
the first lab in the "SQL injection UNION attacks" section. Before
a UNION-based SQL injection can be used to pull data out of a
different table, the number of columns returned by the original
query has to be determined — a UNION SELECT only works if it
returns the exact same number of columns as the query it's being
appended to.

## Objective

Determine the number of columns returned by the original SQL
query behind the product category filter, using SQL injection.

## Environment

- Platform: PortSwigger Web Security Academy
- Operating System: Kali Linux (personal lab VM)
- Tools: Burp Suite (Community Edition) — Proxy and Repeater,
  Firefox with FoxyProxy

## Techniques Practiced

- Using `ORDER BY <n>--` to find a query's column count by
  incrementing `n` until the database throws a column-position
  error
- Using `UNION SELECT NULL,NULL,...--` as a second, independent
  method to confirm the same column count, since `NULL` is
  compatible with virtually any column's data type
- Using Burp Suite's **Repeater** tool to rapidly re-send and edit
  a request multiple times, rather than re-capturing it in
  Intercept for every attempt
- Reading HTTP status codes (`200` vs `500`) and response content
  in Repeater to determine whether an injected query succeeded or
  failed

## Key Findings

Testing `category=Gifts' ORDER BY <n>--` with increasing values of
`n` showed a clean `200 OK` through `ORDER BY 3--`, and a `500
Internal Server Error` at `ORDER BY 4--` — indicating the query
returns **3 columns**. This was independently confirmed with
`category=Gifts' UNION SELECT NULL,NULL,NULL--` (3 `NULL`s)
returning `200 OK`, while adding a fourth `NULL` produced a `500`.

## What I Learned — and What Went Wrong Along the Way

This lab involved more real debugging than the previous two, and
most of what I actually learned came from diagnosing my own
mistakes rather than the technique itself:

- **Testing the wrong request entirely.** Early on, I was sending
  requests to Repeater and getting no errors no matter how high I
  raised the `ORDER BY` number. Checking the Request tab's first
  line revealed I was actually testing `GET / HTTP/2` — the
  homepage — with my injected payload sitting unused in the
  `Referer` header. I had sent the wrong captured request to
  Repeater. Always checking that first request line before relying
  on a result is now a habit.
- **Stacking edits instead of replacing them.** After fixing that,
  my next request read `ORDER BY 1, ORDER BY 2--` — I had been
  appending each new attempt on top of the last instead of
  replacing the previous number. That produced a genuine SQL syntax
  error unrelated to column counting. The fix was straightforward
  once spotted: edit the existing value in place, not append to it.
- **A Burp/HTTP2 proxy glitch ("Stream failed to close
  correctly").** When trying to trigger the lab's official solve
  condition by navigating directly in the browser, Burp returned
  its own error page rather than forwarding to the real server.
  This turned out to be an unrelated, transient proxy hiccup — a
  simple reload resolved it.
- **The real solve condition wasn't just a 200 status.** The lab's
  published solution clarified that solving requires the response
  to include *additional content* from the injected row (visible
  as an extra, blank-looking entry in the product listing) — not
  merely an error-free response. Checking Burp's **Render** tab on
  the response (rather than just the status code) confirmed this
  visually, including the "Congratulations, you solved the lab!"
  banner rendered directly from the server's response.
- **A stale browser tab masked the real result.** Even after Burp
  confirmed the lab was solved server-side, the actual browser
  window still showed "Not solved" — simply because that tab
  hadn't been reloaded since the solving request was sent. Lab
  status is tracked server-side against the session, so a reload
  was all that was needed to see it reflected.

Taken together, this lab was a good reminder that SQL injection
work in practice involves a lot of "why isn't this doing what I
expect" moments that have nothing to do with the SQL itself —
wrong request, malformed edits, tooling quirks, and stale page
state all showed up in a single session.

## Ethical Considerations

This lab was performed in PortSwigger's own sandboxed Web Security
Academy environment, built specifically for practicing these
techniques. No real systems or production data were involved.
