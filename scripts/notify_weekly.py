#!/usr/bin/env python3
import os, json, httpx
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": "📅 <b>Время планирования недели!</b>\n\n💰 Не забудь финансовый учёт\n📊 Подведи итоги 7 дней",
    "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": "📱 Открыть финансы →", "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Weekly sent")
