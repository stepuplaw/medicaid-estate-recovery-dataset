#!/usr/bin/env python3
"""Compare dataset classifications with the popular secondary lists saved in data/sources/US-popular-*.txt.

Prints one line per conflict. Secondary lists are compared, never used as a source for any cell.
"""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "data", "sources")
rows = {r["name"]: r for r in json.load(open(os.path.join(ROOT, "data", "states.json")))}
by_code = {r["code"]: r for r in rows.values()}

print("== medicaidlongtermcare.org scope table (updated Jan 30, 2026) ==")
lines = [l.strip() for l in open(os.path.join(SRC, "US-popular-mltc-estate-recovery.txt")).read().splitlines()]
start = next(i for i, l in enumerate(lines) if "State by State Differences" in l)
seen = set()
for i in range(start, len(lines) - 1):
    name = lines[i]
    if name in rows and name not in seen:
        seen.add(name)
        s = lines[i + 1]
        pop = "expanded" if "xpanded" in s else ("probate_only" if "robate" in s else "?:" + s[:40])
        ours = rows[name]["recovery_scope"]
        conflict = (pop == "expanded") != (ours != "probate_only")
        print(f"{rows[name]['code']} popular={pop} ours={ours}{'  CONFLICT' if conflict else ''}")
print("not in table:", sorted(set(rows) - seen))

print("\n== Nolo TOD deed list ==")
lines = [l.strip().rstrip("*").strip() for l in open(os.path.join(SRC, "US-popular-nolo-tod.txt")).read().splitlines()]
start = next(i for i, l in enumerate(lines) if l == "Alaska")
nolo = set()
for l in lines[start:]:
    if l in rows:
        nolo.add(rows[l]["code"])
    elif l.startswith("*") or l == "":
        break
ours = {c for c, r in by_code.items() if r["tod_deed_recognized"] == "yes"}
print(f"nolo count={len(nolo)} ours={len(ours)}")
print("ours but not nolo:", sorted(ours - nolo))
print("nolo but not ours:", sorted(nolo - ours))

print("\n== Five lady bird states (Nolo / ElderLawAnswers: FL MI TX VT WV) ==")
five = set("FL MI TX VT WV".split())
yes = {c for c, r in by_code.items() if r["lady_bird_deed_recognized"] == "yes"}
for c in sorted(five | yes):
    r = by_code[c]
    print(c, "in_five" if c in five else "not_in_five", r["lady_bird_deed_recognized"], r["lady_bird_authority_type"])
