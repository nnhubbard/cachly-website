#!/usr/bin/env python3
"""Splice _newbodies/<id>.body.html into the matching page() call in
_generate.py, and swap that page's SCREENSHOTS entries from
_newbodies/<id>.shots.json. Backs up _generate.py to _generate.py.bak first."""
import json, os, re, sys

DOCS = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(DOCS, "_generate.py")
NEW = os.path.join(DOCS, "_newbodies")

src = open(GEN, encoding="utf-8").read()
open(GEN + ".bak", "w", encoding="utf-8").write(src)

page_ids = sorted(f[:-10] for f in os.listdir(NEW) if f.endswith(".body.html"))
if not page_ids:
    sys.exit("no bodies found in _newbodies/")

for pid in page_ids:
    body = open(f"{NEW}/{pid}.body.html", encoding="utf-8").read()
    assert '"""' not in body, f"{pid}: body contains triple quotes"
    body = body.rstrip() + "\n"
    # The body is the final argument: a triple-quoted string ending `""")`.
    pat = re.compile(r'(page\("%s",.*?\n)""".*?"""\)' % re.escape(pid), re.S)
    new_src, n = pat.subn(lambda m: m.group(1) + '"""' + body + '""")', src, count=1)
    if n != 1:
        sys.exit(f"FAILED to locate body for page {pid}")
    src = new_src
    print(f"spliced body: {pid}")

# Rebuild SCREENSHOTS entries for the spliced pages.
m = re.search(r"SCREENSHOTS\s*=\s*\{(.*?)\n\}", src, re.S)
if not m:
    sys.exit("SCREENSHOTS dict not found")
dict_body = m.group(1)
entries = dict(re.findall(r'\n    "([a-z-]+)":\s*(\[.*?\])(?=,?\n    "|\Z)', dict_body + "\n", re.S))

for pid in page_ids:
    shots_file = f"{NEW}/{pid}.shots.json"
    if not os.path.exists(shots_file):
        continue
    shots = json.load(open(shots_file, encoding="utf-8"))
    for fname, _cap in shots:
        assert os.path.exists(f"{DOCS}/assets/screenshots/{fname}"), f"{pid}: missing screenshot {fname}"
    lines = ",\n            ".join(
        "(%r, %r)" % (fname, cap) for fname, cap in shots)
    entries[pid] = f"[{lines}]"
    print(f"updated shots: {pid} ({len(shots)})")

new_dict = "SCREENSHOTS = {\n" + "".join(
    f'    "{k}": {v},\n' for k, v in entries.items()) + "}"
src = re.sub(r"SCREENSHOTS\s*=\s*\{.*?\n\}", lambda _: new_dict, src, count=1, flags=re.S)

open(GEN, "w", encoding="utf-8").write(src)
print("wrote _generate.py")
