import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from lib.github_storage import read_day_data, write_day_data

ALLOWED_ORIGIN = os.environ.get("MINI_APP_URL", "https://umidjon.github.io").rstrip("/")


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors()
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        date = params.get("date", [None])[0]
        if not date:
            self._json(400, {"error": "date param required"})
            return
        try:
            self._json(200, read_day_data(date))
        except Exception as e:
            self._json(503, {"error": str(e)})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length))
        except Exception:
            self._json(400, {"error": "invalid JSON"})
            return

        date = body.get("date")
        type_ = body.get("type")   # "schedule" | "goals" | "finance"
        key = body.get("key")
        value = body.get("value")
        subkey = body.get("subkey")

        if not date or not type_ or key is None:
            self._json(400, {"error": "date, type, key required"})
            return
        try:
            data = read_day_data(date)
            if subkey is not None:
                # nested: data[type_][key][subkey] = value  (e.g. goals.sport.0 = true)
                data.setdefault(type_, {}).setdefault(str(key), {})[str(subkey)] = value
            else:
                data.setdefault(type_, {})[str(key)] = value
            write_day_data(date, data)
            self._json(200, {"ok": True})
        except Exception as e:
            self._json(503, {"error": str(e)})

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
