# Telegram Bot + Mini App — Design Spec

**Date:** 2026-03-18
**Project:** Персональный тайм-менеджмент — Telegram Bot + Mini App
**Scope:** Личный инструмент (один пользователь — Умиджон). Без монетизации, без регистрации.

---

## Стек

| Компонент | Технология | Хостинг | Стоимость |
|---|---|---|---|
| Bot webhook + API | Python FastAPI | Vercel (serverless) | $0 |
| Mini App (фронт) | HTML/CSS/JS (адаптация index.html) | GitHub Pages | $0 |
| Уведомления | GitHub Actions (cron) | GitHub | $0 |
| Хранилище данных | JSON файлы | GitHub repo (via API) | $0 |

**Итого: $0 навсегда.**

---

## Архитектура

```
┌─────────────────────────────────────────────────────┐
│                   TELEGRAM                          │
│  Бот (@umidjon_timebot)  │  Mini App (Web App)      │
│  команды + уведомления   │  glassmorphism дашборд   │
└────────────┬─────────────┴──────────┬───────────────┘
             │ webhook                │ fetch API
             ▼                        ▼
┌─────────────────────────────────────────────────────┐
│              VERCEL (бесплатно)                     │
│  /api/webhook   — принимает апдейты от Telegram     │
│  /api/data      — GET/POST данных для Mini App      │
└─────────────────────┬───────────────────────────────┘
                      │ GitHub API
                      ▼
┌─────────────────────────────────────────────────────┐
│         GITHUB REPO (хранилище + Mini App)          │
│  data/YYYY-MM-DD.json  — чекбоксы, цели, финансы   │
│  index.html            — Mini App (GitHub Pages)    │
└─────────────────────────────────────────────────────┘
             ▲
             │ cron schedule
┌─────────────────────────────────────────────────────┐
│         GITHUB ACTIONS (уведомления)                │
│  morning.yml   — 07:00 UTC+5 ежедневно              │
│  evening.yml   — 22:30 UTC+5 ежедневно              │
│  martial.yml   — 20:45 UTC+5 Вт/Чт/Сб              │
│  weekly.yml    — 20:00 UTC+5 воскресенье            │
└─────────────────────────────────────────────────────┘
```

---

## Структура репозитория

```
time-managment/
├── index.html                  # Mini App (GitHub Pages)
├── api/
│   ├── webhook.py              # Vercel serverless: бот webhook
│   └── data.py                 # Vercel serverless: GET/POST данных
├── .github/
│   └── workflows/
│       ├── morning.yml         # Утренний брифинг 07:00
│       ├── evening.yml         # Итоги дня 22:30
│       ├── martial.yml         # Напоминание единоборств 20:45
│       └── weekly.yml          # Воскресный отчёт 20:00
├── scripts/
│   ├── notify_morning.py       # Скрипт утреннего уведомления
│   ├── notify_evening.py       # Скрипт вечернего уведомления
│   ├── notify_martial.py       # Скрипт напоминания единоборств
│   └── notify_weekly.py        # Скрипт воскресного отчёта
├── data/                       # JSON файлы (создаются автоматически)
│   └── YYYY-MM-DD.json
├── vercel.json                 # Конфиг Vercel
└── requirements.txt            # fastapi, httpx, python-telegram-bot
```

---

## Компонент 1: Vercel API

### `api/webhook.py` — Bot Webhook

Принимает POST от Telegram, обрабатывает команды:

| Команда | Ответ |
|---|---|
| `/start` | Приветствие + inline кнопка «Открыть дашборд» (Mini App) |
| `/today` | Сегодняшнее расписание (обычный или боевой день) нумерованным списком |
| `/done 3` | Отмечает задачу #3 ✅, обновляет JSON в GitHub |
| `/stats` | «Выполнено X/15 (Y%). Стрик: N дней 🔥» |
| `/week` | Тема текущего дня + список задач недели |
| `/app` | Inline кнопка «Открыть дашборд» |

**Секреты (Vercel Environment Variables):**
- `BOT_TOKEN` — токен от @BotFather
- `CHAT_ID` — Telegram chat ID Умиджона
- `GITHUB_TOKEN` — Personal Access Token (repo scope)
- `GITHUB_REPO` — `username/time-managment`

### `api/data.py` — Data API для Mini App

```
GET  /api/data?date=2026-03-18
     → читает data/2026-03-18.json из GitHub repo
     → возвращает JSON или {} если файл не существует

POST /api/data
     body: { date, type, key, value }
     → читает текущий JSON
     → обновляет нужное поле
     → записывает обратно в GitHub repo через API
```

**CORS:** разрешён только с домена GitHub Pages (`https://username.github.io`). Явно прописать origin в заголовках ответа.

**Авто-создание файла:** GET `/api/data` — если `data/YYYY-MM-DD.json` не существует, вернуть `{}` (не 404). POST создаёт файл автоматически.

**Лимиты GitHub API:** при ошибке записи вернуть 503. Rate limit для личного токена: 5000 запросов/час — для одного пользователя более чем достаточно.

---

## Компонент 2: Mini App (index.html адаптация)

**Изменения в `index.html`:**

1. Добавить Telegram Web App SDK:
```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

2. При старте инициализировать Telegram:
```js
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand(); // полноэкранный режим
```

3. Заменить localStorage на API вызовы:
```js
// Было: localStorage.getItem(key)
// Стало:
async function loadData(date) {
  const res = await fetch(`/api/data?date=${date}`);
  return res.json();
}

async function saveData(date, type, key, value) {
  await fetch('/api/data', {
    method: 'POST',
    body: JSON.stringify({ date, type, key, value })
  });
}
```

4. Цветовая тема:
```js
// Следовать теме Telegram (dark/light)
document.documentElement.setAttribute('data-bs-theme',
  tg.colorScheme === 'dark' ? 'dark' : 'light');
```

**Хостинг:** GitHub Pages (ветка `main`, папка root или `/docs`)
**URL:** `https://username.github.io/time-managment/`

---

## Компонент 3: GitHub Actions — Уведомления

### Расписание (UTC+5 = Ташкент)

| Workflow | Cron (UTC) | Время (UTC+5) | Дни |
|---|---|---|---|
| morning.yml | `0 2 * * *` | 07:00 | Ежедневно |
| evening.yml | `30 17 * * *` | 22:30 | Ежедневно |
| martial.yml | `45 15 * * 2,4,6` | 20:45 | Вт/Чт/Сб |
| weekly.yml | `0 15 * * 0` | 20:00 | Воскресенье |

### Содержание уведомлений

**Утро (07:00):**
```
🌅 Доброе утро, Умиджон!

📅 Среда — Карьера-день 📈
Сегодня: 15 задач

⏰ Первый блок в 09:00 💼

[Открыть день →]
```

**Вечер (22:30):**
```
📊 Итоги дня

✅ Выполнено: 11/15 (73%)
📈 Вчера: 60% · Стрик: 5 дней 🔥

[Посмотреть →]
```

**Единоборства (20:45 Вт/Чт/Сб):**
```
🥋 Через 15 минут — ЕДИНОБОРСТВА!

Подготовься, выходи в 20:30 🚶
```

**Воскресенье (20:00):**
```
📅 Время планирования недели!

💰 Не забудь финансовый учёт
📊 Подведи итоги 7 дней

[Открыть финансы →]
```

### Реализация скриптов

Каждый `scripts/notify_*.py` делает одно:
1. Вычисляет сегодняшний день недели → выбирает расписание
2. Читает `data/YYYY-MM-DD.json` (статистика за вчера для вечернего)
3. Отправляет сообщение через Telegram Bot API
4. Добавляет inline кнопку «Открыть дашборд» (Mini App URL)

**Секреты в GitHub Actions:**
- `BOT_TOKEN`
- `CHAT_ID`
- `GITHUB_TOKEN` (автоматически доступен как `secrets.GITHUB_TOKEN`)

---

## Структура данных (JSON)

```json
// data/2026-03-18.json
{
  "date": "2026-03-18",
  "schedule": {
    "0": true,
    "1": true,
    "2": false,
    "3": false
  },
  "goals": {
    "sport": { "0": true, "1": false },
    "chess": { "0": false, "1": false, "2": false },
    "english": { "0": true, "1": false, "2": false }
  },
  "finance": {
    "Кредит (обязательно)": 6000000,
    "Расходы на машину": 1800000
  }
}
```

---

## Настройка (шаги деплоя)

1. **BotFather** → создать бота → получить `BOT_TOKEN`
2. **GitHub** → Personal Access Token (scope: `repo`)
3. **Vercel** → импортировать repo → добавить env vars → деплой
4. **Telegram** → установить webhook: `POST api.telegram.org/bot{TOKEN}/setWebhook?url=https://your-app.vercel.app/api/webhook`
5. **GitHub Pages** → включить в настройках репозитория
6. **GitHub Secrets** → добавить `BOT_TOKEN`, `CHAT_ID`

---

## Что НЕ входит в скоуп

- Мульти-юзер / авторизация
- AI-подсказки / аналитика
- Редактирование расписания через бота (только через Mini App)
- Уведомления для каждого часового блока (только ключевые)
