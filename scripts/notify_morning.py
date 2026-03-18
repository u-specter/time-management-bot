#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import httpx
from lib.schedule_data import get_dow, get_today_schedule
from lib.settings import get_lang
from lib.strings import S, DAY_NAMES, WEEK_THEMES

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

lang     = get_lang()
t        = S[lang]
dow      = get_dow()
schedule = get_today_schedule()
first    = next(task for task in schedule if task["time"] >= "09:00")

text = t["morning"].format(
    day=DAY_NAMES[lang][dow],
    theme=WEEK_THEMES[lang][dow],
    count=len(schedule),
    time=first["time"],
    icon=first["icon"],
)

httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID, "text": text, "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": t["morning_btn"], "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Morning sent")
