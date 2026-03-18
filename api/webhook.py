import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from datetime import date

import httpx

from lib.schedule_data import get_today_schedule, get_dow, DAY_NAMES, WEEK_THEMES
from lib.github_storage import read_day_data, write_day_data, count_done

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = str(os.environ["CHAT_ID"])
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"


def keyboard():
    return {"inline_keyboard": [[
        {"text": "📱 Открыть дашборд", "web_app": {"url": MINI_APP_URL}}
    ]]}


def send(chat_id: str, text: str, kb=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if kb:
        payload["reply_markup"] = json.dumps(kb)
    httpx.post(f"{TG}/sendMessage", json=payload, timeout=10)


def today() -> str:
    return date.today().isoformat()


def handle(text: str, chat_id: str):
    cmd = text.split()[0].lower().split("@")[0]

    if cmd == "/start":
        send(chat_id,
             "👋 <b>Умиджон, твой личный командный центр</b>\n\n"
             "/today — расписание дня\n"
             "/done 3 — отметить задачу #3\n"
             "/stats — прогресс за сегодня\n"
             "/week — план недели",
             keyboard())

    elif cmd == "/app":
        send(chat_id, "📱 Открыть дашборд:", keyboard())

    elif cmd == "/today":
        schedule = get_today_schedule()
        dow = get_dow()
        lines = "\n".join(
            f"{i+1}. {t['icon']} <b>{t['time']}</b> {t['text']}"
            for i, t in enumerate(schedule)
        )
        send(chat_id,
             f"📅 <b>{DAY_NAMES[dow]} — {WEEK_THEMES[dow]}</b>\n\n{lines}",
             keyboard())

    elif cmd == "/done":
        parts = text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            send(chat_id, "❌ Используй: /done 3")
            return
        n = int(parts[1]) - 1
        schedule = get_today_schedule()
        if not (0 <= n < len(schedule)):
            send(chat_id, f"❌ Нет задачи #{n+1}. Всего: {len(schedule)}")
            return
        try:
            d = today()
            data = read_day_data(d)
            data.setdefault("schedule", {})[str(n)] = True
            write_day_data(d, data)
            task = schedule[n]
            send(chat_id,
                 f"✅ <b>{task['icon']} {task['text']}</b>\n\nЗадача #{n+1} отмечена.",
                 keyboard())
        except Exception as e:
            send(chat_id, f"⚠️ Ошибка: {e}")

    elif cmd == "/stats":
        try:
            done, total = count_done(today())
            pct = round(done / total * 100) if total else 0
            mood = "🔥" if pct >= 70 else ("📈" if pct >= 40 else "💪")
            send(chat_id,
                 f"📊 <b>Прогресс сегодня</b>\n\n✅ {done}/{total} ({pct}%) {mood}",
                 keyboard())
        except Exception as e:
            send(chat_id, f"⚠️ Ошибка: {e}")

    elif cmd == "/week":
        dow = get_dow()
        send(chat_id,
             f"🗓 <b>{DAY_NAMES[dow]}</b> — {WEEK_THEMES[dow]}\n\nПолный план в дашборде:",
             keyboard())


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
            handle(text, chat_id)
        self._ok()

    def _ok(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *args):
        pass
