import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler

import httpx

from lib.schedule_data import get_dow, get_today_schedule
from lib.settings import get_lang
from lib.strings import S, DAY_NAMES, WEEK_THEMES

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
OPENAI_KEY   = os.environ.get("OPENAI_KEY", "")
CRON_SECRET  = os.environ.get("CRON_SECRET", "")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _authorized(headers) -> bool:
    if not CRON_SECRET:
        return True
    return headers.get("Authorization", "") == f"Bearer {CRON_SECRET}"


def _get_ai_quote(prompt: str) -> str:
    if not OPENAI_KEY:
        return ""
    try:
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}"},
            json={"model": "gpt-4o-mini",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 120, "temperature": 0.9},
            timeout=8,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if not _authorized(self.headers):
            self._respond(401, {"error": "unauthorized"})
            return
        try:
            lang     = get_lang()
            t        = S[lang]
            dow      = get_dow()
            schedule = get_today_schedule()
            first    = next(task for task in schedule if task["time"] >= "08:00")

            httpx.post(f"{TG}/sendMessage", json={
                "chat_id": CHAT_ID,
                "text": t["morning"].format(
                    day=DAY_NAMES[lang][dow],
                    theme=WEEK_THEMES[lang][dow],
                    count=len(schedule),
                    time=first["time"],
                    icon=first["icon"],
                ),
                "parse_mode": "HTML",
                "reply_markup": json.dumps({"inline_keyboard": [[
                    {"text": t["morning_btn"], "web_app": {"url": MINI_APP_URL}}
                ]]}),
            }, timeout=10)

            quote = _get_ai_quote(t["quote_prompt"])
            if quote:
                httpx.post(f"{TG}/sendMessage", json={
                    "chat_id": CHAT_ID,
                    "text": f"💡 <i>{quote}</i>",
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
