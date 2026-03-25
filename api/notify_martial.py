import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import httpx

from lib.settings import get_lang
from lib.strings import S

BOT_TOKEN   = os.environ["BOT_TOKEN"]
CHAT_ID     = os.environ["CHAT_ID"]
CRON_SECRET = os.environ.get("CRON_SECRET", "")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _authorized(headers, path: str = "") -> bool:
    if not CRON_SECRET:
        return True
    qs = parse_qs(urlparse(path).query)
    if qs.get("secret", [""])[0] == CRON_SECRET:
        return True
    return headers.get("Authorization", "") == f"Bearer {CRON_SECRET}"


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if not _authorized(self.headers, self.path):
            self._respond(401, {"error": "unauthorized"})
            return
        try:
            lang = get_lang()
            httpx.post(f"{TG}/sendMessage", json={
                "chat_id": CHAT_ID,
                "text": S[lang]["martial"],
                "parse_mode": "HTML",
            }, timeout=10)
            self._respond(200, {"ok": True})
        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _respond(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
