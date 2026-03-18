#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import httpx
from lib.schedule_data import get_dow, get_today_schedule, DAY_NAMES, WEEK_THEMES

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

dow      = get_dow()
schedule = get_today_schedule()
first    = next(t for t in schedule if t["time"] >= "09:00")

text = (
    f"🌅 <b>Доброе утро, Умиджон!</b>\n\n"
    f"📅 <b>{DAY_NAMES[dow]}</b> — {WEEK_THEMES[dow]}\n"
    f"Сегодня: <b>{len(schedule)} задач</b>\n\n"
    f"⏰ Первый блок в {first['time']} {first['icon']}"
)

httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID, "text": text, "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": "📱 Открыть день →", "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Morning sent")
