#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import httpx
from lib.settings import get_lang
from lib.strings import S

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

lang = get_lang()
httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": S[lang]["martial"],
    "parse_mode": "HTML",
}, timeout=10)
print("Martial sent")
