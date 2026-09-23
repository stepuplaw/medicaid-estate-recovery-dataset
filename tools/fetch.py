#!/usr/bin/env python3
"""Fetch a URL, strip HTML to text, save to data/sources/<name>.txt with a provenance header.

Usage: python3 tools/fetch.py <name> <url> [--grep WORD ...]
Prints the saved path, byte count, and optionally lines containing any --grep word.
"""
import html, re, sys, datetime, urllib.request, ssl, os, subprocess

BASE = os.path.join(os.path.dirname(__file__), "..", "data", "sources")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def to_text(raw: bytes, ctype: str) -> str:
    if raw[:4] == b"%PDF" or "pdf" in ctype:
        tmp = "/tmp/_fetch.pdf"
        open(tmp, "wb").write(raw)
        try:
            return subprocess.run(["pdftotext", "-layout", tmp, "-"], capture_output=True, text=True).stdout
        except FileNotFoundError:
            return "[pdf; pdftotext not installed]"
    s = raw.decode("utf-8", errors="replace")
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


DASHES = {"\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2015": "-", "\u2212": "-"}


def main():
    name, url = sys.argv[1], sys.argv[2]
    greps = []
    if "--grep" in sys.argv:
        greps = [g.lower() for g in sys.argv[sys.argv.index("--grep") + 1:]]
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            raw, ctype, final = r.read(), r.headers.get("Content-Type", ""), r.geturl()
    except Exception as e:
        print(f"FAIL {url}: {e}")
        sys.exit(1)
    text = to_text(raw, ctype)
    # Brief forbids em/en dashes in any file; normalize them to ASCII hyphens in saved copies.
    for k, v in DASHES.items():
        text = text.replace(k, v)
    path = os.path.normpath(os.path.join(BASE, f"{name}.txt"))
    with open(path, "w") as f:
        f.write(f"Source URL: {final}\nRetrieved: {datetime.date.today().isoformat()}\n\n{text}\n")
    print(f"saved {path} ({len(text)} chars)")
    if greps:
        for line in text.splitlines():
            if any(g in line.lower() for g in greps):
                print("  |", line.strip()[:400])


if __name__ == "__main__":
    main()
