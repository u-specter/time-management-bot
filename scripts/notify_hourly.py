#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime, timezone, timedelta
import httpx

from lib.schedule_data import get_today_schedule
from lib.settings import get_lang
from lib.strings import S

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
TZ        = timedelta(hours=5)  # UTC+5 Tashkent


def now_local() -> datetime:
    return datetime.now(timezone.utc) + TZ


def send_message(text: str, reply_markup=None) -> None:
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
               json=payload, timeout=10)


def main():
    lang     = get_lang()
    t        = S[lang]
    now      = now_local()
    cur_hour = now.hour
    today    = now.strftime("%Y-%m-%d")
    schedule = get_today_schedule()

    for idx, task in enumerate(schedule):
        task_hour = int(task["time"].split(":")[0])
        if task_hour != cur_hour:
            continue

        # Notification text for current task
        text = t["hourly_notify"].format(
            time=task["time"], icon=task["icon"], text=task["text"]
        )

        # Inline buttons to mark the PREVIOUS task (it just ended)
        reply_markup = None
        if idx > 0:
            prev = schedule[idx - 1]
            text += f"\n\n└ {prev['icon']} <b>{prev['time']}</b> {prev['text']}"
            reply_markup = {"inline_keyboard": [[
                {"text": t["poll_yes"], "callback_data": f"mark:{today}:{idx - 1}:1"},
                {"text": t["poll_no"],  "callback_data": f"mark:{today}:{idx - 1}:0"},
            ]]}

        send_message(text, reply_markup)
        print(f"Notified: {task['time']} {task['text']}")


if __name__ == "__main__":
    main()
