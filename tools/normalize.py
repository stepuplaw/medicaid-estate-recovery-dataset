#!/usr/bin/env python3
"""One-time cleanup: strip em/en dashes from saved files and reduce tod_deed_effective to a bare date.

Any act or chapter detail in tod_deed_effective is moved into the row's flags so nothing is lost.
"""
import glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DASHES = str.maketrans({chr(c): "-" for c in (0x2012, 0x2013, 0x2014, 0x2015)})

for f in glob.glob(os.path.join(ROOT, "data", "sources", "*.txt")) + glob.glob(os.path.join(ROOT, "tools", "*.py")):
    s = open(f, encoding="utf-8", errors="replace").read()
    if s.translate(DASHES) != s:
        open(f, "w").write(s.translate(DASHES))
        print("dashes fixed:", os.path.basename(f))

for f in sorted(glob.glob(os.path.join(ROOT, "data", "rows", "*.json"))):
    r = json.load(open(f))
    m = re.match(r"^(\d{4}(?:-\d{2}-\d{2})?)\s*(.*)$", r["tod_deed_effective"])
    if m and m.group(2):
        detail = m.group(2).strip().strip("()").strip().rstrip(".")
        r["tod_deed_effective"] = m.group(1)
        flags = r["flags"].rstrip()
        r["flags"] = (flags + " " if flags else "") + f"TOD deed effective date detail: {m.group(1)}, {detail}."
        json.dump(r, open(f, "w"), indent=2, ensure_ascii=False)
        print("tod date:", r["code"], r["tod_deed_effective"])
