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
OPENAI_KEY   = os.environ.get("OPENAI_KEY", "")


def get_ai_quote(prompt: str) -> str:
    if not OPENAI_KEY:
        return ""
    try:
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 120,
                "temperature": 0.9,
            },
            timeout=20,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Quote error: {e}")
        return ""


lang     = get_lang()
t        = S[lang]
dow      = get_dow()
schedule = get_today_schedule()
first    = next(task for task in schedule if task["time"] >= "08:00")

# Main morning message
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

# Motivational quote
quote = get_ai_quote(t["quote_prompt"])
if quote:
    httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": f"💡 <i>{quote}</i>",
        "parse_mode": "HTML",
    }, timeout=10)
    print("Quote sent")
