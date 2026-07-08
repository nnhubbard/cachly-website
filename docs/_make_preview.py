#!/usr/bin/env python3
"""Regenerate _preview.html — a contact sheet of docs/assets/screenshots/ with
per-screen annotation boxes.

Note persistence, in order of preference:
1. Live to disk: run `python3 _serve_preview.py` and open
   http://localhost:8642/_preview.html — every keystroke is written (debounced)
   to docs/cachly-capture-notes.json.
2. Browser autosave: opened as a plain file, notes persist in localStorage;
   use "Export notes" to download the JSON and drop it in docs/.
3. "Import notes" restores from a previously exported JSON file.

Regenerating this page pre-seeds the boxes from docs/cachly-capture-notes.json,
so saved notes always come back."""
import os, html, json, re

DOCS = os.path.dirname(os.path.abspath(__file__))
SHOTS = f"{DOCS}/assets/screenshots"

def sort_key(f):
    # Group multi-part captures: "settings-general" before "settings-general-2"
    name = f[:-4]
    m = re.match(r"^(.*?)-(\d+)$", name)
    return (m.group(1), int(m.group(2))) if m else (name, 1)

shots = sorted((f for f in os.listdir(SHOTS) if f.endswith(".png")), key=sort_key)
older = [f for f in shots if f[0].isdigit() or f.startswith("_")]
current = [f for f in shots if f not in older]
# The numbered captures are embedded in the published pages (via _generate.py)
# — keep them until the rewrite swaps them for the new set.

seeded = {}
notes_path = f"{DOCS}/cachly-capture-notes.json"
if os.path.exists(notes_path):
    seeded = json.load(open(notes_path))

def cards(files):
    out = []
    for f in files:
        name = f[:-4]
        note = html.escape(seeded.get(name, ""))
        out.append(f'''<figure data-name="{name}">
<a href="assets/screenshots/{f}" target="_blank"><img loading="lazy" src="assets/screenshots/{f}"></a>
<figcaption>{html.escape(name)}</figcaption>
<textarea placeholder="Notes for the docs… (what this screen is for, wording to use, things to call out or skip)">{note}</textarea>
</figure>''')
    return "\n".join(out)

seeded_json = json.dumps(seeded, ensure_ascii=False).replace("</", "<\\/")

page = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Cachly docs — capture preview</title>
<style>
body{{font-family:-apple-system,sans-serif;margin:20px;background:#f4f4f6}}
h1{{font-size:20px}} h2{{font-size:16px;margin-top:28px}}
p{{color:#555;max-width:70em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}}
figure{{margin:0;background:#fff;border-radius:10px;padding:8px;box-shadow:0 1px 3px rgba(0,0,0,.12);display:flex;flex-direction:column}}
img{{width:100%;border-radius:6px;display:block}}
figcaption{{font-size:11px;font-family:ui-monospace,monospace;margin:6px 0 4px;word-break:break-all;text-align:center}}
textarea{{width:100%;box-sizing:border-box;min-height:52px;font-size:12px;border:1px solid #ddd;border-radius:6px;padding:6px;resize:vertical}}
textarea.saved{{border-color:#7bc47f;background:#f6fff6}}
#bar{{position:fixed;right:16px;bottom:16px;z-index:10;display:flex;gap:8px;align-items:center}}
#bar button{{background:#1a7f37;color:#fff;border:0;border-radius:8px;padding:10px 16px;font-size:14px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
#bar button.secondary{{background:#555}}
#status{{background:#fff;border-radius:8px;padding:10px 12px;font-size:13px;color:#333;box-shadow:0 2px 8px rgba(0,0,0,.25);max-width:260px}}
#status .disk{{color:#1a7f37;font-weight:600}}
#status .browser{{color:#b45309;font-weight:600}}
</style></head><body>
<h1>Cachly documentation — screen capture preview</h1>
<p>{len(current)} captures. Click an image for full size. Type notes under any screen — they save automatically as you type, and you can close this page and come back later; your notes will still be here. The status box (bottom right) tells you where notes are being saved: <b>to disk</b> when the preview is opened through the little save server (<code>python3 docs/_serve_preview.py</code>, then <code>http://localhost:8642/_preview.html</code>), otherwise <b>in this browser</b> — in that case click <b>Export notes</b> when done and put <code>cachly-capture-notes.json</code> in the <code>docs/</code> folder.</p>
<div id="bar"><span id="status"></span><button class="secondary" onclick="importNotes()">Import notes</button><button onclick="exportNotes()">Export notes</button></div>
<div class="grid">{cards(current)}</div>
<h2>Screenshots currently used by the live docs pages ({len(older)}) — will be replaced by the new set during the rewrite</h2>
<div class="grid">{cards(older)}</div>
<input type="file" id="importer" accept=".json" style="display:none">
<script>
const KEY = 'cachly-capture-notes';
const seeded = {seeded_json};
// Merge: localStorage wins over seeded file (it's the more recent local edit).
const store = Object.assign({{}}, seeded, JSON.parse(localStorage.getItem(KEY) || '{{}}'));
let diskOK = false, saveTimer = null, lastSaved = null;

function applyStore() {{
  document.querySelectorAll('figure').forEach(fig => {{
    const ta = fig.querySelector('textarea');
    const v = store[fig.dataset.name] || '';
    if (ta.value !== v) ta.value = v;
    ta.classList.toggle('saved', !!v.trim());
  }});
}}

function persist() {{
  localStorage.setItem(KEY, JSON.stringify(store));
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveToDisk, 600);
  updateStatus('typing…');
}}

async function saveToDisk() {{
  try {{
    const r = await fetch('/save-notes', {{method: 'POST', body: JSON.stringify(store)}});
    diskOK = r.ok;
  }} catch (e) {{ diskOK = false; }}
  lastSaved = new Date();
  updateStatus();
}}

function updateStatus(extra) {{
  const n = Object.keys(store).filter(k => store[k].trim()).length;
  const when = lastSaved ? ' at ' + lastSaved.toLocaleTimeString() : '';
  const where = diskOK ? '<span class="disk">saved to disk</span>' + when
                       : '<span class="browser">saved in this browser</span>' + when;
  document.getElementById('status').innerHTML =
    n + ' screens annotated · ' + (extra || where);
}}

document.querySelectorAll('figure').forEach(fig => {{
  const name = fig.dataset.name, ta = fig.querySelector('textarea');
  ta.addEventListener('input', () => {{
    if (ta.value.trim()) store[name] = ta.value; else delete store[name];
    ta.classList.toggle('saved', !!ta.value.trim());
    persist();
  }});
}});

function exportNotes() {{
  const blob = new Blob([JSON.stringify(store, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'cachly-capture-notes.json';
  a.click();
}}

function importNotes() {{ document.getElementById('importer').click(); }}
document.getElementById('importer').addEventListener('change', e => {{
  const f = e.target.files[0]; if (!f) return;
  f.text().then(t => {{
    Object.assign(store, JSON.parse(t));
    applyStore(); persist();
  }});
}});

applyStore();
saveToDisk();  // probe the server so the status is accurate
</script>
</body></html>"""

open(f"{DOCS}/_preview.html", "w").write(page)
print(f"wrote _preview.html: {len(current)} current + {len(older)} older captures, {len(seeded)} seeded notes")
