#!/usr/bin/env python3
import os, httpx
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": "🥋 <b>Через 15 минут — ЕДИНОБОРСТВА!</b>\n\nВыходи в 20:30 🚶",
    "parse_mode": "HTML",
}, timeout=10)
print("Martial sent")
