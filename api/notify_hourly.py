import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, parse_qs

import httpx

from lib.schedule_data import get_today_schedule
from lib.settings import get_lang
from lib.strings import S

BOT_TOKEN   = os.environ["BOT_TOKEN"]
CHAT_ID     = os.environ["CHAT_ID"]
CRON_SECRET = os.environ.get("CRON_SECRET", "")
TZ          = timedelta(hours=5)  # UTC+5 Tashkent
TG          = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _authorized(headers, path: str = "") -> bool:
    if not CRON_SECRET:
        return True
    qs = parse_qs(urlparse(path).query)
    if qs.get("secret", [""])[0] == CRON_SECRET:
        return True
    return headers.get("Authorization", "") == f"Bearer {CRON_SECRET}"


def _now_local() -> datetime:
    return datetime.now(timezone.utc) + TZ


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if not _authorized(self.headers, self.path):
            self._respond(401, {"error": "unauthorized"})
            return
        try:
            lang     = get_lang()
            t        = S[lang]
            now      = _now_local()
            cur_hour = now.hour
            today    = now.strftime("%Y-%m-%d")
            schedule = get_today_schedule()
            sent     = 0

            for idx, task in enumerate(schedule):
                task_hour = int(task["time"].split(":")[0])
                if task_hour != cur_hour:
                    continue

                text = t["hourly_notify"].format(
                    time=task["time"], icon=task["icon"], text=task["text"]
                )
                reply_markup = None
                if idx > 0:
                    prev = schedule[idx - 1]
                    text += f"\n\n└ {prev['icon']} <b>{prev['time']}</b> {prev['text']}"
                    reply_markup = {"inline_keyboard": [[
                        {"text": t["poll_yes"], "callback_data": f"mark:{today}:{idx - 1}:1"},
                        {"text": t["poll_no"],  "callback_data": f"mark:{today}:{idx - 1}:0"},
                    ]]}

                payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
                if reply_markup:
                    payload["reply_markup"] = json.dumps(reply_markup)
                httpx.post(f"{TG}/sendMessage", json=payload, timeout=10)
                sent += 1

            self._respond(200, {"ok": True, "sent": sent, "hour": cur_hour})
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
