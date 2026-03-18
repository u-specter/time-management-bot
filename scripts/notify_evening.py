#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from datetime import date
import httpx
from lib.schedule_data import get_dow
from lib.github_storage import count_done
from lib.settings import get_lang
from lib.strings import S, DAY_NAMES

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

lang = get_lang()
t    = S[lang]

try:
    done, total = count_done(date.today().isoformat())
    pct  = round(done / total * 100) if total else 0
    mood = "🔥" if pct >= 70 else ("📈" if pct >= 40 else "💪")
    stats = t["evening_stats"].format(done=done, total=total, pct=pct, mood=mood)
except Exception:
    stats = t["evening_fallback"]

httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": t["evening"].format(day=DAY_NAMES[lang][get_dow()], stats=stats),
    "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": t["evening_btn"], "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Evening sent")
