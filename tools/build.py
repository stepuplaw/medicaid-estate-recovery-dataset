#!/usr/bin/env python3
"""Assemble data/rows/<CODE>.json into data/states.csv and data/states.json.

Each state is researched and saved as its own row file so a crash loses at most one state.
Run after every state: python3 tools/build.py   (add --check to only validate)
"""
import csv, json, os, sys, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
METHODS = ["life_estate", "lady_bird_deed", "tod_deed", "joint_tenancy", "revocable_trust"]
COLUMNS = (
    ["code", "name", "recovery_scope", "recovery_scope_note", "recovery_statute", "recovery_statute_url",
     "state_plan_4_17_a_url"]
    + [c for m in METHODS for c in (m, f"{m}_note", f"{m}_cite")]
    + ["tod_deed_recognized", "tod_deed_statute", "tod_deed_effective", "tod_deed_uniform_act",
       "lady_bird_deed_recognized", "lady_bird_authority_type", "lady_bird_authority",
       "hardship_waiver_home", "recovery_exemptions_note", "karp_2005_scope",
       "last_verified", "sources", "confidence", "flags"]
)
ENUMS = {
    "recovery_scope": {"probate_only", "expanded", "expanded_partial"},
    "tod_deed_recognized": {"yes", "no"},
    "tod_deed_uniform_act": {"yes", "no", "n/a"},
    "lady_bird_deed_recognized": {"yes", "no", "unclear"},
    "lady_bird_authority_type": {"statute", "case_law", "agency_rule", "practice", "none", "unclear"},
    "confidence": {"high", "medium", "low"},
    "karp_2005_scope": {"probate_only", "expanded", "not_in_survey", ""},
}
for m in METHODS:
    ENUMS[m] = {"reachable", "not_reachable", "unclear", "n/a"}
STATES = dict(x.split(":") for x in (
    "AL:Alabama AK:Alaska AZ:Arizona AR:Arkansas CA:California CO:Colorado CT:Connecticut DE:Delaware "
    "DC:District_of_Columbia FL:Florida GA:Georgia HI:Hawaii ID:Idaho IL:Illinois IN:Indiana IA:Iowa KS:Kansas "
    "KY:Kentucky LA:Louisiana ME:Maine MD:Maryland MA:Massachusetts MI:Michigan MN:Minnesota MS:Mississippi "
    "MO:Missouri MT:Montana NE:Nebraska NV:Nevada NH:New_Hampshire NJ:New_Jersey NM:New_Mexico NY:New_York "
    "NC:North_Carolina ND:North_Dakota OH:Ohio OK:Oklahoma OR:Oregon PA:Pennsylvania RI:Rhode_Island "
    "SC:South_Carolina SD:South_Dakota TN:Tennessee TX:Texas UT:Utah VT:Vermont VA:Virginia WA:Washington "
    "WV:West_Virginia WI:Wisconsin WY:Wyoming").split())
STATES = {k: v.replace("_", " ") for k, v in STATES.items()}
BAD = [chr(0x2012), chr(0x2013), chr(0x2014), chr(0x2015)]  # figure, en, em, horizontal-bar dashes

# Karp, Sabatino and Wood, AARP PPI / ABA (June 2005), p. 20 and Table 8 (data/sources/US-karp-2005-aarp-survey.txt).
# Adjusted finding: 13 states limited to the probate estate, 33 go beyond it. CO, GA, MI, MO, TX are not in Table 8.
KARP_PROBATE = set("AZ MD MS NE NH NM NY OH PA RI SC VT WV".split())
KARP_ABSENT = set("CO GA MI MO TX".split())


def karp(code):
    if code in KARP_ABSENT:
        return "not_in_survey"
    return "probate_only" if code in KARP_PROBATE else "expanded"


def validate(row, fname):
    errs = []
    for c in COLUMNS:
        if c not in row:
            errs.append(f"missing {c}")
    for c in row:
        if c not in COLUMNS:
            errs.append(f"unknown column {c}")
    for c, allowed in ENUMS.items():
        if c in row and row[c] not in allowed:
            errs.append(f"{c}={row[c]!r} not in {sorted(allowed)}")
    for c, v in row.items():
        if any(b in str(v) for b in BAD):
            errs.append(f"em/en dash in {c}")
    if row.get("code") not in STATES:
        errs.append("bad code")
    return [f"{fname}: {e}" for e in errs]


def main():
    rows, errs = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "rows", "*.json"))):
        row = json.load(open(f))
        row["karp_2005_scope"] = karp(row.get("code"))  # filled centrally, not by researchers
        errs += validate(row, os.path.basename(f))
        rows.append(row)
    rows.sort(key=lambda r: r.get("name", ""))
    for e in errs:
        print("ERROR", e)
    if "--check" in sys.argv:
        print(f"{len(rows)} rows, {len(errs)} errors")
        return
    with open(os.path.join(ROOT, "data", "states.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    with open(os.path.join(ROOT, "data", "states.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    done = {r["code"] for r in rows}
    print(f"built {len(rows)} rows, {len(errs)} errors; missing: {' '.join(sorted(set(STATES) - done))}")


if __name__ == "__main__":
    main()
