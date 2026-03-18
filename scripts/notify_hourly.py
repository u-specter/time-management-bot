#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime, timezone, timedelta
import httpx

from lib.schedule_data import get_today_schedule, get_dow
from lib.github_storage import add_poll
from lib.settings import get_lang
from lib.strings import S, DAY_NAMES, WEEK_THEMES

BOT_TOKEN    = os.environ["BOT_TOKEN"]
CHAT_ID      = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
TZ           = timedelta(hours=5)  # UTC+5 Tashkent


def now_local() -> datetime:
    return datetime.now(timezone.utc) + TZ


def send_message(text: str) -> None:
    httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": CHAT_ID, "text": text, "parse_mode": "HTML",
    }, timeout=10)


def send_poll(question: str, yes: str, no: str, date: str, task_idx: int, task_text: str) -> None:
    r = httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json={
        "chat_id": CHAT_ID,
        "question": question[:300],   # Telegram poll question limit
        "options": [yes, no],
        "is_anonymous": False,
    }, timeout=10)
    if r.status_code == 200 and r.json().get("ok"):
        poll_id = str(r.json()["result"]["poll"]["id"])
        try:
            add_poll(poll_id, date, task_idx, task_text)
        except Exception as e:
            print(f"Warning: could not save poll {poll_id}: {e}")


def main():
    lang     = get_lang()
    t        = S[lang]
    now      = now_local()
    cur_hour = now.hour
    today    = now.strftime("%Y-%m-%d")
    schedule = get_today_schedule()

    # Find tasks starting in the current hour window [cur_hour:00, cur_hour+1:00)
    for idx, task in enumerate(schedule):
        task_hour = int(task["time"].split(":")[0])
        if task_hour != cur_hour:
            continue

        # 1. Notify about this task starting
        send_message(t["hourly_notify"].format(
            time=task["time"], icon=task["icon"], text=task["text"]
        ))
        print(f"Notified: {task['time']} {task['text']}")

        # 2. Poll about the PREVIOUS task (it just ended)
        if idx > 0:
            prev = schedule[idx - 1]
            question = t["poll_question"].format(
                icon=prev["icon"], time=prev["time"], text=prev["text"]
            )
            send_poll(question, t["poll_yes"], t["poll_no"], today, idx - 1, prev["text"])
            print(f"Poll sent for: {prev['time']} {prev['text']}")


if __name__ == "__main__":
    main()
