#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from datetime import date
import httpx
from lib.schedule_data import get_dow, DAY_NAMES
from lib.github_storage import count_done

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

try:
    done, total = count_done(date.today().isoformat())
    pct  = round(done / total * 100) if total else 0
    mood = "🔥" if pct >= 70 else ("📈" if pct >= 40 else "💪")
    stats = f"✅ Выполнено: <b>{done}/{total}</b> ({pct}%) {mood}"
except Exception:
    stats = "📊 Открой дашборд для статистики"

httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": f"📊 <b>Итоги дня — {DAY_NAMES[get_dow()]}</b>\n\n{stats}",
    "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": "📱 Посмотреть →", "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Evening sent")
