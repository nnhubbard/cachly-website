#!/usr/bin/env python3
"""Serve the capture preview with live note-saving.

    python3 _serve_preview.py        # then open http://localhost:8642/_preview.html

Serves the docs/ folder and accepts POST /save-notes, writing the annotation
JSON to docs/cachly-capture-notes.json on every change — notes persist on disk
immediately, so you can close the page and come back any time.
"""
import http.server, json, os, socketserver, subprocess

DOCS = os.path.dirname(os.path.abspath(__file__))
PORT = 8642
NOTES = os.path.join(DOCS, "cachly-capture-notes.json")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS, **kwargs)

    def do_GET(self):
        # Rebuild the contact sheet on refresh so newly dropped screenshots
        # (e.g. taken manually on a device) appear without running anything.
        if self.path.split("?")[0] == "/_preview.html":
            subprocess.run(["python3", os.path.join(DOCS, "_make_preview.py")],
                           capture_output=True)
        super().do_GET()

    def do_POST(self):
        if self.path != "/save-notes":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            notes = json.loads(body)
            assert isinstance(notes, dict)
        except Exception:
            self.send_error(400, "invalid JSON")
            return
        with open(NOTES, "w") as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def log_message(self, *args):
        pass  # keep the terminal quiet


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving preview at http://localhost:{PORT}/_preview.html")
        print(f"Notes save to {NOTES}")
        httpd.serve_forever()
