import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from datetime import date

import httpx

from lib.schedule_data import get_dow
from lib.github_storage import count_done
from lib.settings import get_lang
from lib.strings import S, DAY_NAMES

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
CRON_SECRET  = os.environ.get("CRON_SECRET", "")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _authorized(headers) -> bool:
    if not CRON_SECRET:
        return True
    return headers.get("Authorization", "") == f"Bearer {CRON_SECRET}"


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if not _authorized(self.headers):
            self._respond(401, {"error": "unauthorized"})
            return
        try:
            lang = get_lang()
            t    = S[lang]
            try:
                done, total = count_done(date.today().isoformat())
                pct  = round(done / total * 100) if total else 0
                mood = "🔥" if pct >= 70 else ("📈" if pct >= 40 else "💪")
                stats = t["evening_stats"].format(done=done, total=total, pct=pct, mood=mood)
            except Exception:
                stats = t["evening_fallback"]

            httpx.post(f"{TG}/sendMessage", json={
                "chat_id": CHAT_ID,
                "text": t["evening"].format(day=DAY_NAMES[lang][get_dow()], stats=stats),
                "parse_mode": "HTML",
                "reply_markup": json.dumps({"inline_keyboard": [[
                    {"text": t["evening_btn"], "web_app": {"url": MINI_APP_URL}}
                ]]}),
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
