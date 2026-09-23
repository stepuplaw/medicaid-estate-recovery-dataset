#!/usr/bin/env python3
"""Fetch a legacy Word .doc (binary) and save its readable text runs with a provenance header.

Usage: python3 tools/fetch_doc.py <name> <url>
Crude extraction: keeps runs of printable characters (8-bit and UTF-16LE). Not verbatim formatting.
"""
import re, sys, os, datetime, urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..", "data", "sources")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
name, url = sys.argv[1], sys.argv[2]
raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
runs8 = re.findall(rb"[\x20-\x7e\r\n\t\x91-\x97\xa7]{40,}", raw)
runs16 = re.findall(rb"(?:[\x20-\x7e\r\n\t]\x00){40,}", raw)
t8 = "\n".join(r.decode("cp1252", "replace") for r in runs8)
t16 = "\n".join(r.decode("utf-16le", "replace") for r in runs16)
text = t8 if len(t8) >= len(t16) else t16
for k in ["-", "-", "-", "-"]:
    text = text.replace(k, "-")
text = text.replace("\r", "\n")
path = os.path.normpath(os.path.join(BASE, f"{name}.txt"))
open(path, "w").write(f"Source URL: {url}\nRetrieved: {datetime.date.today().isoformat()}\nNote: text extracted from a Word .doc file by printable-run extraction; wording verbatim, layout not.\n\n{text}\n")
print(f"saved {path} ({len(text)} chars)")
