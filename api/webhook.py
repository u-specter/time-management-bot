import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from datetime import date

import httpx

from lib.schedule_data import get_today_schedule, get_dow
from lib.github_storage import read_day_data, write_day_data, count_done
from lib.settings import get_lang, set_lang
from lib.strings import S, DAY_NAMES, WEEK_THEMES

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = str(os.environ["CHAT_ID"])
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"


def keyboard(label: str):
    return {"inline_keyboard": [[
        {"text": label, "web_app": {"url": MINI_APP_URL}}
    ]]}


def send(chat_id: str, text: str, kb=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if kb:
        payload["reply_markup"] = json.dumps(kb)
    httpx.post(f"{TG}/sendMessage", json=payload, timeout=10)


def today() -> str:
    return date.today().isoformat()


def handle(text: str, chat_id: str):
    lang = get_lang()
    t = S[lang]
    cmd = text.split()[0].lower().split("@")[0]

    if cmd == "/start":
        send(chat_id, t["start"], keyboard(t["btn_dashboard"]))

    elif cmd == "/app":
        send(chat_id, t["app"], keyboard(t["btn_dashboard"]))

    elif cmd == "/today":
        schedule = get_today_schedule()
        dow = get_dow()
        day = DAY_NAMES[lang][dow]
        theme = WEEK_THEMES[lang][dow]
        lines = "\n".join(
            f"{i+1}. {task['icon']} <b>{task['time']}</b> {task['text']}"
            for i, task in enumerate(schedule)
        )
        send(chat_id,
             f"📅 <b>{day} — {theme}</b>\n\n{lines}",
             keyboard(t["today_btn"]))

    elif cmd == "/done":
        parts = text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            send(chat_id, t["done_invalid"])
            return
        n = int(parts[1]) - 1
        schedule = get_today_schedule()
        if not (0 <= n < len(schedule)):
            send(chat_id, t["done_no_task"].format(n=n + 1, total=len(schedule)))
            return
        try:
            d = today()
            data = read_day_data(d)
            data.setdefault("schedule", {})[str(n)] = True
            write_day_data(d, data)
            task = schedule[n]
            send(chat_id,
                 t["done_ok"].format(icon=task["icon"], text=task["text"], n=n + 1),
                 keyboard(t["btn_dashboard"]))
        except Exception as e:
            send(chat_id, t["done_err"].format(e=e))

    elif cmd == "/stats":
        try:
            done, total = count_done(today())
            pct = round(done / total * 100) if total else 0
            mood = "🔥" if pct >= 70 else ("📈" if pct >= 40 else "💪")
            send(chat_id,
                 t["stats"].format(done=done, total=total, pct=pct, mood=mood),
                 keyboard(t["btn_dashboard"]))
        except Exception as e:
            send(chat_id, t["stats_err"].format(e=e))

    elif cmd == "/week":
        dow = get_dow()
        send(chat_id,
             t["week"].format(day=DAY_NAMES[lang][dow], theme=WEEK_THEMES[lang][dow]),
             keyboard(t["btn_dashboard"]))

    elif cmd == "/lang":
        parts = text.split()
        if len(parts) < 2 or parts[1].lower() not in ("ru", "uz"):
            send(chat_id, t["lang_invalid"])
            return
        new_lang = parts[1].lower()
        try:
            set_lang(new_lang)
            key = "lang_set_uz" if new_lang == "uz" else "lang_set_ru"
            send(chat_id, S[new_lang][key])
        except Exception as e:
            send(chat_id, f"⚠️ {e}")


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            update = json.loads(self.rfile.read(length))
        except Exception:
            self._ok()
            return
        msg = update.get("message", {})
        text = msg.get("text", "")
        chat_id = str(msg.get("chat", {}).get("id", ""))
        if chat_id == CHAT_ID and text.startswith("/"):
            try:
                handle(text, chat_id)
            except Exception as e:
                try:
                    httpx.post(f"{TG}/sendMessage", json={
                        "chat_id": chat_id, "text": f"⚠️ Internal error: {e}"
                    }, timeout=5)
                except Exception:
                    pass

        poll_answer = update.get("poll_answer")
        if poll_answer:
            poll_id = str(poll_answer["poll_id"])
            option_ids = poll_answer.get("option_ids", [])
            done = 0 in option_ids  # option 0 = Yes/Да/Ha
            try:
                from lib.github_storage import read_polls, read_day_data, write_day_data
                polls = read_polls()
                if poll_id in polls:
                    p = polls[poll_id]
                    day_data = read_day_data(p["date"])
                    day_data.setdefault("schedule", {})[str(p["task_idx"])] = done
                    write_day_data(p["date"], day_data)
            except Exception:
                pass

        self._ok()

    def _ok(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *args):
        pass
