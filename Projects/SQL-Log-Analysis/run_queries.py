#!/usr/bin/env python3
"""Runs every .sql file in queries/ against security_logs.db and
prints + saves a formatted table of results for each."""

import glob
import sqlite3

DB_PATH = "security_logs.db"


def format_table(headers, rows):
    if not rows:
        return "(no rows returned)\n"
    widths = [len(h) for h in headers]
    str_rows = [[str(c) for c in row] for row in rows]
    for row in str_rows:
        for i, c in enumerate(row):
            widths[i] = max(widths[i], len(c))
    lines = []
    header_line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("  ".join("-" * w for w in widths))
    for row in str_rows:
        lines.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(row)))
    return "\n".join(lines) + "\n"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for path in sorted(glob.glob("queries/*.sql")):
        with open(path) as f:
            sql = f.read()
        cur.execute(sql)
        headers = [d[0] for d in cur.description]
        rows = cur.fetchall()

        table = format_table(headers, rows)
        print(f"=== {path} ===")
        print(f"({len(rows)} row(s) returned)\n")
        print(table)

        out_path = "results/" + path.split("/")[-1].replace(".sql", ".txt")
        with open(out_path, "w") as out:
            out.write(f"Query: {path}\n")
            out.write(f"Rows returned: {len(rows)}\n\n")
            out.write(table)

    conn.close()


if __name__ == "__main__":
    main()
