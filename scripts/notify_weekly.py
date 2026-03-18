#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json, httpx
from lib.settings import get_lang
from lib.strings import S

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

lang = get_lang()
t    = S[lang]
httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": t["weekly"],
    "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": t["weekly_btn"], "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Weekly sent")
