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
        total = len(content)
        start, end = 0, total - 1
        status = 200
        requested = self.headers.get("Range", "")
        if file.suffix == ".mp3" and requested.startswith("bytes="):
            try:
                spec = requested[6:]
                if "," in spec:
                    raise ValueError("multiple ranges unsupported")
                a, b = spec.split("-", 1)
                if not a and b:
                    suffix = int(b)
                    if suffix <= 0:
                        raise ValueError("invalid suffix")
                    start = max(0, total - suffix)
                else:
                    start = int(a)
                    end = int(b) if b else total - 1
                if start < 0 or start >= total or end < start:
                    raise ValueError("invalid range")
                end = min(end, total - 1)
                status = 206
            except (ValueError, TypeError):
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{total}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        if file.suffix == ".mp3":
            self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{total}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store" if file.suffix == ".html" else "public, max-age=3600")
        self.end_headers()
        self.wfile.write(content[start:end + 1])
if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
