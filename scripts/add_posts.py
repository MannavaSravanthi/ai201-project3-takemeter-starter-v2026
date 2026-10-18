"""Pull headlines out of copied r/Arkansas pages and append new ones to labels.csv.

Usage: python scripts/add_posts.py raw/raw_posts_02.txt
A headline is the line just before the "NEWS" flair line. Posts already in
labels.csv (ignoring curly quotes and case) are skipped. New rows get an
empty label so they can be labelled by hand.
"""
import csv, sys

SKIP = {  # same story as a post already kept
    "little rock school district to close three elementary schools | arkansas democrat gazette",
}

def key(s):
    return s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').strip().lower()

with open("labels.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
seen = {key(r["text"]) for r in rows} | SKIP

added = []
for path in sys.argv[1:]:
    lines = open(path, encoding="utf-8").read().splitlines()
    for i, line in enumerate(lines):
        if "NEWS" in line and "\U0001f5de" in line and i > 0:
            head = lines[i - 1].strip()
            if head and key(head) not in seen:
                seen.add(key(head))
                added.append(head)

with open("labels.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for h in added:
        w.writerow([h, "", ""])

print(f"added {len(added)} new posts; labels.csv now has {len(rows) + len(added)} rows")
for h in added:
    print("  +", h)
