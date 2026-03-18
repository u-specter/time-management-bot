# Telegram Bot + Mini App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a personal Telegram bot with Mini App (Web App) that delivers smart daily notifications and a glassmorphism dashboard accessible from Telegram — hosted entirely for free.

**Architecture:** Python serverless functions on Vercel handle bot webhook and data API. GitHub Actions runs cron notification scripts. The existing `index.html` becomes a Telegram Mini App. JSON files stored in the GitHub repo via GitHub API serve as the database.

**Tech Stack:** Python 3.11, httpx, Vercel serverless (BaseHTTPRequestHandler), GitHub Actions, Telegram Bot API, Telegram Web App SDK.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `requirements.txt` | Create | Python deps for Vercel + scripts |
| `vercel.json` | Create | Vercel routing config |
| `.env.example` | Create | Documents required env vars |
| `data/.gitkeep` | Create | Ensures data/ dir exists in repo |
| `lib/__init__.py` | Create | Makes lib a package |
| `lib/schedule_data.py` | Create | SCHEDULE_NORMAL, SCHEDULE_MARTIAL, MARTIAL_DAYS, WEEK_THEMES, DAY_NAMES, helpers |
| `lib/github_storage.py` | Create | read_day_data(), write_day_data(), count_done() via GitHub API |
| `api/data.py` | Create | Vercel: GET/POST /api/data |
| `api/webhook.py` | Create | Vercel: POST /api/webhook (bot commands) |
| `scripts/notify_morning.py` | Create | Morning briefing notification |
| `scripts/notify_evening.py` | Create | Evening stats notification |
| `scripts/notify_martial.py` | Create | Martial arts reminder |
| `scripts/notify_weekly.py` | Create | Sunday planning reminder |
| `.github/workflows/morning.yml` | Create | Cron 02:00 UTC daily |
| `.github/workflows/evening.yml` | Create | Cron 17:30 UTC daily |
| `.github/workflows/martial.yml` | Create | Cron 15:45 UTC Tue/Thu/Sat |
| `.github/workflows/weekly.yml` | Create | Cron 15:00 UTC Sunday |
| `index.html` | Modify | Add Telegram SDK, add API storage alongside localStorage |
| `.gitignore` | Modify | Add .env |

---

### Task 1: Project scaffold

**Files:** `requirements.txt`, `vercel.json`, `.env.example`, `data/.gitkeep`, `lib/__init__.py`, `.gitignore`

- [ ] **Step 1: Create `requirements.txt`**

```
httpx==0.27.0
```

> **Note:** The spec mentions `fastapi` and `python-telegram-bot` as deps, but this implementation uses Python's built-in `BaseHTTPRequestHandler` instead of FastAPI (no cold-start overhead, zero extra deps) and raw Telegram Bot API via httpx instead of the SDK. Only `httpx` is needed.

- [ ] **Step 2: Create `vercel.json`**

```json
{
  "version": 2,
  "builds": [
    { "src": "api/*.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/api/webhook", "dest": "/api/webhook.py" },
    { "src": "/api/data", "dest": "/api/data.py" }
  ]
}
```

- [ ] **Step 3: Create `.env.example`**

```
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=username/time-managment
MINI_APP_URL=https://username.github.io/time-managment/
```

- [ ] **Step 4: Create scaffold dirs and files**

```bash
mkdir -p data lib api scripts .github/workflows
touch data/.gitkeep lib/__init__.py
```

- [ ] **Step 5: Update `.gitignore`**

Append (create if missing):
```
.env
__pycache__/
*.pyc
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt vercel.json .env.example data/.gitkeep lib/__init__.py .gitignore
git commit -m "feat: project scaffold for telegram bot"
```

---

### Task 2: Schedule data library

**Files:** `lib/schedule_data.py`

- [ ] **Step 1: Create `lib/schedule_data.py` with this exact content:**

```python
MARTIAL_DAYS = {2, 4, 6}  # Tue=2, Thu=4, Sat=6 (weekday()+1, Sun=0)

DAY_NAMES = {
    1: "Понедельник", 2: "Вторник", 3: "Среда",
    4: "Четверг", 5: "Пятница", 6: "Суббота", 0: "Воскресенье",
}

WEEK_THEMES = {
    1: "Стартап-день 🚀",
    2: "Бой-день 🥋",
    3: "Карьера-день 📈",
    4: "Бой-день 🥋",
    5: "Итоги-день 💰",
    6: "Свободное утро + бой 🥋",
    0: "Перезагрузка 🔄",
}

SCHEDULE_NORMAL = [
    {"time": "07:00", "icon": "🌅", "text": "Подъём + намаз + умывание + сборы"},
    {"time": "07:30", "icon": "🚌", "text": "Дорога на работу — English listening / подкаст"},
    {"time": "08:30", "icon": "📚", "text": "Приехал — Книга №1 (рабочая)"},
    {"time": "09:00", "icon": "💼", "text": "РАБОТА — основные задачи (глубокая работа)"},
    {"time": "11:00", "icon": "🎓", "text": "Coursera / Udemy — 1 урок"},
    {"time": "13:00", "icon": "🥗", "text": "Обед + дайджест стартапов + Книга №1"},
    {"time": "14:00", "icon": "⚡", "text": "Личное время → Vibe-coding / Коран / риторика"},
    {"time": "16:00", "icon": "💼", "text": "РАБОТА — задачи, встречи"},
    {"time": "18:00", "icon": "🏠", "text": "Завершение работы / дорога домой"},
    {"time": "19:00", "icon": "😮‍💨", "text": "Дома: ужин / переключение / отдых"},
    {"time": "19:30", "icon": "🚀", "text": "БЛОК: проект / риторика / Книга №2"},
    {"time": "21:30", "icon": "📖", "text": "Книга №2 / Курс Коран / Английский Anki"},
    {"time": "22:30", "icon": "📝", "text": "Планирование следующего дня — 15 мин"},
    {"time": "22:45", "icon": "🌙", "text": "Вечерний намаз + расслабление"},
    {"time": "23:00", "icon": "😴", "text": "СОН"},
]

SCHEDULE_MARTIAL = [
    {"time": "07:00", "icon": "🌅", "text": "Подъём + намаз + умывание + сборы"},
    {"time": "07:30", "icon": "🚌", "text": "Дорога на работу — English listening / подкаст"},
    {"time": "08:30", "icon": "📚", "text": "Приехал — Книга №1 (рабочая)"},
    {"time": "09:00", "icon": "💼", "text": "РАБОТА — основные задачи (глубокая работа)"},
    {"time": "11:00", "icon": "🎓", "text": "Coursera / Udemy — 1 урок"},
    {"time": "13:00", "icon": "🥗", "text": "Обед + дайджест стартапов + Книга №1"},
    {"time": "14:00", "icon": "⚡", "text": "Личное время → Vibe-coding / Коран / риторика"},
    {"time": "16:00", "icon": "💼", "text": "РАБОТА — задачи, встречи"},
    {"time": "18:00", "icon": "🏠", "text": "Завершение работы / дорога домой"},
    {"time": "19:00", "icon": "😮‍💨", "text": "Дома: ужин / переключение / отдых"},
    {"time": "19:30", "icon": "🥊", "text": "Подготовка к единоборству / разминка дома"},
    {"time": "20:30", "icon": "🚶", "text": "Выход на единоборства"},
    {"time": "21:00", "icon": "🥋", "text": "ЕДИНОБОРСТВА"},
    {"time": "22:30", "icon": "🚿", "text": "Возврат + душ + восстановление"},
    {"time": "22:45", "icon": "📝", "text": "Планирование следующего дня — 15 мин"},
    {"time": "23:00", "icon": "😴", "text": "СОН"},
]


def get_dow() -> int:
    """Return day-of-week: Mon=1 ... Sun=0"""
    from datetime import datetime
    dow = datetime.now().weekday() + 1
    return 0 if dow == 7 else dow


def get_today_schedule() -> list:
    return SCHEDULE_MARTIAL if get_dow() in MARTIAL_DAYS else SCHEDULE_NORMAL
```

- [ ] **Step 2: Verify import works**

```bash
cd /Users/umidjon/Desktop/Developer/time-managment
python3 -c "from lib.schedule_data import get_today_schedule; print(len(get_today_schedule()), 'tasks')"
```

Expected output: `15 tasks` or `16 tasks`

- [ ] **Step 3: Commit**

```bash
git add lib/schedule_data.py
git commit -m "feat: schedule data library"
```

---

### Task 3: GitHub storage library

**Files:** `lib/github_storage.py`

- [ ] **Step 1: Create `lib/github_storage.py`**

```python
import os
import json
import base64

import httpx

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]   # e.g. "umidjon/time-managment"
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _url(date: str) -> str:
    return f"{BASE_URL}/repos/{GITHUB_REPO}/contents/data/{date}.json"


def read_day_data(date: str) -> dict:
    """Return day JSON dict. Returns {} if file not found."""
    r = httpx.get(_url(date), headers=HEADERS, timeout=10)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    raw = base64.b64decode(r.json()["content"]).decode("utf-8")
    return json.loads(raw)


def write_day_data(date: str, data: dict) -> None:
    """Create or update data/{date}.json in the repo."""
    encoded = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    sha = None
    r = httpx.get(_url(date), headers=HEADERS, timeout=10)
    if r.status_code == 200:
        sha = r.json()["sha"]

    payload: dict = {"message": f"data: update {date}", "content": encoded}
    if sha:
        payload["sha"] = sha

    r = httpx.put(_url(date), headers=HEADERS, json=payload, timeout=15)
    r.raise_for_status()


def count_done(date: str) -> tuple:
    """Returns (done, total) schedule tasks for date."""
    data = read_day_data(date)
    schedule_map = data.get("schedule", {})
    from lib.schedule_data import get_today_schedule
    total = len(get_today_schedule())
    done = sum(1 for v in schedule_map.values() if v is True)
    return done, total
```

- [ ] **Step 2: Commit**

```bash
git add lib/github_storage.py
git commit -m "feat: github storage library (read_day_data, write_day_data, count_done)"
```

---

### Task 4: Data API endpoint

**Files:** `api/data.py`

- [ ] **Step 1: Create `api/data.py`**

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from lib.github_storage import read_day_data, write_day_data

ALLOWED_ORIGIN = os.environ.get("MINI_APP_URL", "https://umidjon.github.io").rstrip("/")


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors()
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        date = params.get("date", [None])[0]
        if not date:
            self._json(400, {"error": "date param required"})
            return
        try:
            self._json(200, read_day_data(date))
        except Exception as e:
            self._json(503, {"error": str(e)})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length))
        except Exception:
            self._json(400, {"error": "invalid JSON"})
            return

        date = body.get("date")
        type_ = body.get("type")   # "schedule" | "goals" | "finance"
        key = body.get("key")
        value = body.get("value")

        if not date or not type_ or key is None:
            self._json(400, {"error": "date, type, key required"})
            return
        try:
            data = read_day_data(date)
            if type_ not in data:
                data[type_] = {}
            data[type_][str(key)] = value
            write_day_data(date, data)
            self._json(200, {"ok": True})
        except Exception as e:
            self._json(503, {"error": str(e)})

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
```

- [ ] **Step 2: Commit**

```bash
git add api/data.py
git commit -m "feat: data API endpoint GET/POST"
```

---

### Task 5: Bot webhook endpoint

**Files:** `api/webhook.py`

- [ ] **Step 1: Create `api/webhook.py`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add api/webhook.py
git commit -m "feat: bot webhook /start /today /done /stats /week"
```

---

### Task 6: Notification scripts

**Files:** `scripts/notify_morning.py`, `scripts/notify_evening.py`, `scripts/notify_martial.py`, `scripts/notify_weekly.py`

- [ ] **Step 1: Create `scripts/notify_morning.py`**

```python
#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import httpx
from lib.schedule_data import get_dow, get_today_schedule, DAY_NAMES, WEEK_THEMES

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

dow      = get_dow()
schedule = get_today_schedule()
first    = next(t for t in schedule if t["time"] >= "09:00")

text = (
    f"🌅 <b>Доброе утро, Умиджон!</b>\n\n"
    f"📅 <b>{DAY_NAMES[dow]}</b> — {WEEK_THEMES[dow]}\n"
    f"Сегодня: <b>{len(schedule)} задач</b>\n\n"
    f"⏰ Первый блок в {first['time']} {first['icon']}"
)

httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID, "text": text, "parse_mode": "HTML",
    "reply_markup": json.dumps({"inline_keyboard": [[
        {"text": "📱 Открыть день →", "web_app": {"url": MINI_APP_URL}}
    ]]}),
}, timeout=10)
print("Morning sent")
```

- [ ] **Step 2: Create `scripts/notify_evening.py`**

```python
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
```

- [ ] **Step 3: Create `scripts/notify_martial.py`**

```python
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
```

- [ ] **Step 4: Create `scripts/notify_weekly.py`**

```python
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
```

- [ ] **Step 5: Commit**

```bash
git add scripts/
git commit -m "feat: notification scripts morning/evening/martial/weekly"
```

---

### Task 7: GitHub Actions workflows

**Files:** `.github/workflows/morning.yml`, `evening.yml`, `martial.yml`, `weekly.yml`

- [ ] **Step 1: Create `.github/workflows/morning.yml`**

```yaml
name: Morning Notification
on:
  schedule:
    - cron: '0 2 * * *'   # 07:00 UTC+5 daily
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install httpx
      - run: python scripts/notify_morning.py
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          MINI_APP_URL: ${{ secrets.MINI_APP_URL }}
          GITHUB_REPO: ${{ github.repository }}
```

- [ ] **Step 2: Create `.github/workflows/evening.yml`**

```yaml
name: Evening Notification
on:
  schedule:
    - cron: '30 17 * * *'  # 22:30 UTC+5 daily
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install httpx
      - run: python scripts/notify_evening.py
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          MINI_APP_URL: ${{ secrets.MINI_APP_URL }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPO: ${{ github.repository }}
```

- [ ] **Step 3: Create `.github/workflows/martial.yml`**

```yaml
name: Martial Arts Reminder
on:
  schedule:
    - cron: '45 15 * * 2,4,6'  # 20:45 UTC+5 Tue/Thu/Sat
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install httpx
      - run: python scripts/notify_martial.py
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
```

- [ ] **Step 4: Create `.github/workflows/weekly.yml`**

```yaml
name: Weekly Planning Reminder
on:
  schedule:
    - cron: '0 15 * * 0'  # 20:00 UTC+5 Sunday
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install httpx
      - run: python scripts/notify_weekly.py
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          MINI_APP_URL: ${{ secrets.MINI_APP_URL }}
```

- [ ] **Step 5: Commit**

```bash
git add .github/
git commit -m "feat: github actions cron workflows"
```

---

### Task 8: Adapt index.html as Telegram Mini App

**Files:** `index.html`

The existing index.html uses localStorage for all state. We add the Telegram Web App SDK and an API layer that syncs to Vercel/GitHub when running inside Telegram. When opened in a regular browser, localStorage continues to work as fallback.

- [ ] **Step 1: Add Telegram SDK before `</head>`**

Find `</head>` and insert this line immediately before it:
```html
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
```

- [ ] **Step 2: Add Telegram init + API helpers at top of `<script>` block**

Find the line `// ============================================================` that starts the DATA section. Insert this block immediately before it:

```js
// ============================================================
//  TELEGRAM MINI APP + API STORAGE
// ============================================================
const IS_TG = !!(window.Telegram && window.Telegram.WebApp);
const tg = IS_TG ? window.Telegram.WebApp : null;
const API_BASE = 'https://YOUR-APP.vercel.app'; // replace after Vercel deploy

if (tg) {
  tg.ready();
  tg.expand();
  // Follow Telegram's color scheme (dark/light)
  document.documentElement.setAttribute('data-bs-theme',
    tg.colorScheme === 'dark' ? 'dark' : 'light');
}

async function apiLoad(date) {
  if (!IS_TG) return null;
  try {
    const r = await fetch(API_BASE + '/api/data?date=' + date);
    return r.ok ? r.json() : null;
  } catch { return null; }
}

async function apiSave(date, type, key, value) {
  if (!IS_TG) return;
  try {
    await fetch(API_BASE + '/api/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, type, key, value }),
    });
  } catch { /* localStorage already updated — silent fail */ }
}
```

- [ ] **Step 3: Make `renderSchedule` async and load API data**

The current `renderSchedule(dow)` function reads localStorage per-task inside the forEach loop. Replace it with an async version that loads all data upfront from the API when in Telegram, falling back to localStorage otherwise.

Find the entire `function renderSchedule(dow)` block and replace with:

```js
async function renderSchedule(dow) {
  const isMartial = MARTIAL_DAYS.includes(dow);
  const tasks = isMartial ? SCHEDULE_MARTIAL : SCHEDULE_NORMAL;
  const dateKey = todayKey();
  const list = document.getElementById('schedule-list');
  list.innerHTML = '';

  const apiData = await apiLoad(dateKey);
  const apiSched = apiData ? (apiData.schedule || {}) : null;

  tasks.forEach((task, idx) => {
    const lsKey = 'sched-' + dateKey + '-' + idx;
    const done = apiSched ? apiSched[String(idx)] === true : localStorage.getItem(lsKey) === '1';
    const color = CAT_COLORS[task.cat] || '#6c757d';

    const row = document.createElement('div');
    row.className = 'schedule-row' + (done ? ' done' : '');
    row.innerHTML = [
      '<div class="cat-bar" style="background:' + color + ';"></div>',
      '<span class="task-time">' + task.time + '</span>',
      '<span class="task-icon">' + task.icon + '</span>',
      '<span class="task-text">' + task.text + '</span>',
      '<span class="task-check">' + (done ? '\u2713' : '') + '</span>',
    ].join('');

    row.addEventListener('click', () => {
      const cur = apiSched ? apiSched[String(idx)] === true : localStorage.getItem(lsKey) === '1';
      const next = !cur;
      localStorage.setItem(lsKey, next ? '1' : '0');
      apiSave(dateKey, 'schedule', idx, next);
      renderSchedule(dow);
    });
    list.appendChild(row);
  });

  updateDayProgress(tasks, dateKey);
}
```

- [ ] **Step 4: Update goal checkbox click to also sync via API (nested structure)**

`apiSave` needs to write goals as `{ "goals": { "sport": { "0": true } } }` matching the spec. Update the function signature to accept an optional `subkey`:

Find `async function apiSave(date, type, key, value)` and replace with:
```js
async function apiSave(date, type, key, value, subkey) {
  if (!IS_TG) return;
  try {
    await fetch(API_BASE + '/api/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, type, key, value, subkey }),
    });
  } catch { /* localStorage already updated — silent fail */ }
}
```

Update `api/data.py` POST handler to support optional `subkey` for nested writes. Find:
```python
        try:
            data = read_day_data(date)
            if type_ not in data:
                data[type_] = {}
            data[type_][str(key)] = value
```

Replace with:
```python
        subkey = body.get("subkey")
        try:
            data = read_day_data(date)
            if subkey is not None:
                # nested: data[type_][key][subkey] = value
                data.setdefault(type_, {}).setdefault(str(key), {})[str(subkey)] = value
            else:
                data.setdefault(type_, {})[str(key)] = value
```

Inside `initGoalsTab`, find:
```js
        localStorage.setItem(key, now ? '0' : '1');
```

Replace with:
```js
        const newVal = !now;
        localStorage.setItem(key, newVal ? '1' : '0');
        apiSave(todayKey(), 'goals', section.id, newVal, idx);
```

This produces the spec-correct structure `{ "goals": { "sport": { "0": true } } }`.

- [ ] **Step 5: Open index.html in browser and verify no console errors**

```bash
open /Users/umidjon/Desktop/Developer/time-managment/index.html
```

DevTools → Console: should be empty. localStorage fallback works.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "feat: telegram mini app SDK + API storage layer in index.html"
```

---

### Task 9: Deploy and configure

This task is manual steps — no code to write.

- [ ] **Step 1: Create bot via @BotFather**

1. Telegram → @BotFather → `/newbot`
2. Choose name + username
3. Copy `BOT_TOKEN`

- [ ] **Step 2: Get your CHAT_ID**

```
https://api.telegram.org/bot{BOT_TOKEN}/getUpdates
```

Send any message to bot first, then open URL. Find `"chat": {"id": 123456789}`.

- [ ] **Step 3: Create GitHub Personal Access Token**

GitHub → Settings → Developer settings → Tokens (classic) → New token → scope: `repo` → copy as `GITHUB_PAT`

- [ ] **Step 4: Push to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/time-managment.git
git push -u origin main
```

- [ ] **Step 5: Enable GitHub Pages**

Repo → Settings → Pages → Branch: `main`, folder: `/ (root)` → Save

Note URL: `https://YOUR_USERNAME.github.io/time-managment/`

- [ ] **Step 6: Add GitHub Actions Secrets**

Repo → Settings → Secrets → Actions → add:
- `BOT_TOKEN`
- `CHAT_ID`
- `MINI_APP_URL` = `https://YOUR_USERNAME.github.io/time-managment/`

Note: `GITHUB_TOKEN` is automatically provided by GitHub Actions — no need to add it manually. The `evening.yml` workflow uses `${{ secrets.GITHUB_TOKEN }}` (built-in) for GitHub API access.

- [ ] **Step 7: Deploy to Vercel**

vercel.com → New Project → import repo → Framework: Other → add env vars:
- `BOT_TOKEN`, `CHAT_ID`, `MINI_APP_URL`
- `GITHUB_TOKEN` = your `GITHUB_PAT`
- `GITHUB_REPO` = `YOUR_USERNAME/time-managment`

Deploy → copy Vercel URL.

- [ ] **Step 8: Update API_BASE in index.html**

Find `const API_BASE = 'https://YOUR-APP.vercel.app';` and replace with actual URL. Commit + push.

- [ ] **Step 9: Register webhook**

```bash
curl "https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://YOUR-APP.vercel.app/api/webhook"
```

Expected: `{"ok":true,"result":true}`

- [ ] **Step 10: Register Mini App with BotFather**

BotFather → `/newapp` → select bot → URL: `https://YOUR_USERNAME.github.io/time-managment/`

- [ ] **Step 11: Smoke test**

Send to bot:
- `/start` → приветствие + кнопка
- `/today` → расписание
- `/done 1` → отмечает задачу
- `/stats` → прогресс

- [ ] **Step 12: Test notifications via workflow_dispatch**

GitHub → Actions → `Morning Notification` → Run workflow → check Telegram.

- [ ] **Step 13: Final push**

```bash
git push
```
