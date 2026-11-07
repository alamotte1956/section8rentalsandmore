"""Minimal public-site server. No repository browsing, uploads, or admin pages."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os

ROOT = Path(__file__).resolve().parent
PUBLIC = {"/": "index.html", "/index.html": "index.html",
          "/presentation.html": "presentation.html",
          "/referral-partners.html": "referral-partners.html"}
ASSETS = {".mp3": "audio/mpeg", ".ics": "text/calendar"}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        name = PUBLIC.get(path)
        if name is None and path in ("/speech.mp3", "/Al LaMotte HUD speech.mp3"):
            name = path[1:]
        if name is None and path.startswith("/media/"):
            candidate = path.removeprefix("/media/")
            if candidate in ("speech.mp3", "Al LaMotte HUD speech.mp3"):
                name = candidate
        if name is None:
            self.send_error(404)
            return
        file = ROOT / name
        if not file.is_file():
            self.send_error(404)
            return
        content = file.read_bytes()
        ctype = "text/html; charset=utf-8" if file.suffix == ".html" else ASSETS.get(file.suffix, "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store" if file.suffix == ".html" else "public, max-age=3600")
        self.end_headers()
        self.wfile.write(content)
if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
