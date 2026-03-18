MARTIAL_DAYS = {2, 4}  # Tue=2, Thu=4 (Sat now has its own schedule)

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
    6: "Свободный день + тренировка 🥋",
    0: "День отдыха 🔄",
}

SCHEDULE_NORMAL = [
    {"time": "07:00", "icon": "🌅", "cat": "gray",   "text": "Подъём + намаз + умывание + сборы"},
    {"time": "07:30", "icon": "🚌", "cat": "blue",   "text": "Дорога на работу — English listening / подкаст"},
    {"time": "08:30", "icon": "📚", "cat": "yellow",  "text": "Приехал — Книга №1 (рабочая)"},
    {"time": "09:00", "icon": "💼", "cat": "blue",   "text": "РАБОТА — основные задачи (глубокая работа)"},
    {"time": "11:00", "icon": "🎓", "cat": "purple",  "text": "Coursera / Udemy — 1 урок"},
    {"time": "13:00", "icon": "🥗", "cat": "orange",  "text": "Обед + дайджест стартапов + Книга №1"},
    {"time": "14:00", "icon": "⚡", "cat": "purple",  "text": "Личное время → Vibe-coding / Коран / риторика"},
    {"time": "16:00", "icon": "💼", "cat": "blue",   "text": "РАБОТА — задачи, встречи"},
    {"time": "18:00", "icon": "🏠", "cat": "gray",   "text": "Завершение работы / дорога домой"},
    {"time": "19:00", "icon": "😮‍💨", "cat": "gray",  "text": "Дома: ужин / переключение / отдых"},
    {"time": "19:30", "icon": "🚀", "cat": "purple",  "text": "БЛОК: проект / риторика / Книга №2"},
    {"time": "21:30", "icon": "📖", "cat": "yellow",  "text": "Книга №2 / Курс Коран / Английский Anki"},
    {"time": "22:30", "icon": "📝", "cat": "gray",   "text": "Планирование следующего дня — 15 мин"},
    {"time": "22:45", "icon": "🌙", "cat": "gray",   "text": "Вечерний намаз + расслабление"},
    {"time": "23:00", "icon": "😴", "cat": "gray",   "text": "СОН"},
]

SCHEDULE_MARTIAL = [
    {"time": "07:00", "icon": "🌅", "cat": "gray",   "text": "Подъём + намаз + умывание + сборы"},
    {"time": "07:30", "icon": "🚌", "cat": "blue",   "text": "Дорога на работу — English listening / подкаст"},
    {"time": "08:30", "icon": "📚", "cat": "yellow",  "text": "Приехал — Книга №1 (рабочая)"},
    {"time": "09:00", "icon": "💼", "cat": "blue",   "text": "РАБОТА — основные задачи (глубокая работа)"},
    {"time": "11:00", "icon": "🎓", "cat": "purple",  "text": "Coursera / Udemy — 1 урок"},
    {"time": "13:00", "icon": "🥗", "cat": "orange",  "text": "Обед + дайджест стартапов + Книга №1"},
    {"time": "14:00", "icon": "⚡", "cat": "purple",  "text": "Личное время → Vibe-coding / Коран / риторика"},
    {"time": "16:00", "icon": "💼", "cat": "blue",   "text": "РАБОТА — задачи, встречи"},
    {"time": "18:00", "icon": "🏠", "cat": "gray",   "text": "Завершение работы / дорога домой"},
    {"time": "19:00", "icon": "😮‍💨", "cat": "gray",  "text": "Дома: ужин / переключение / отдых"},
    {"time": "19:30", "icon": "🥊", "cat": "red",    "text": "Подготовка к единоборству / разминка дома"},
    {"time": "20:30", "icon": "🚶", "cat": "red",    "text": "Выход на единоборства"},
    {"time": "21:00", "icon": "🥋", "cat": "red",    "text": "ЕДИНОБОРСТВА"},
    {"time": "22:30", "icon": "🚿", "cat": "gray",   "text": "Возврат + душ + восстановление"},
    {"time": "22:45", "icon": "📝", "cat": "gray",   "text": "Планирование следующего дня — 15 мин"},
    {"time": "23:00", "icon": "😴", "cat": "gray",   "text": "СОН"},
]

SCHEDULE_SATURDAY = [
    {"time": "08:00", "icon": "🌅", "cat": "gray",   "text": "Подъём + намаз + умывание"},
    {"time": "09:00", "icon": "☕", "cat": "orange",  "text": "Завтрак + отдых / семья"},
    {"time": "10:00", "icon": "🚀", "cat": "purple",  "text": "Личный проект / Vibe-coding"},
    {"time": "12:00", "icon": "🥗", "cat": "orange",  "text": "Обед"},
    {"time": "13:00", "icon": "♟️", "cat": "blue",   "text": "Шахматы / Английский"},
    {"time": "15:00", "icon": "📖", "cat": "yellow",  "text": "Чтение / Коран"},
    {"time": "17:00", "icon": "🚶", "cat": "green",   "text": "Прогулка / свежий воздух"},
    {"time": "19:00", "icon": "🍽️", "cat": "orange",  "text": "Ужин + отдых"},
    {"time": "19:30", "icon": "🥊", "cat": "red",    "text": "Подготовка к единоборству"},
    {"time": "20:30", "icon": "🚶", "cat": "red",    "text": "Выход на единоборства"},
    {"time": "21:00", "icon": "🥋", "cat": "red",    "text": "ЕДИНОБОРСТВА"},
    {"time": "22:30", "icon": "🚿", "cat": "gray",   "text": "Возврат + душ + восстановление"},
    {"time": "23:00", "icon": "😴", "cat": "gray",   "text": "СОН"},
]

SCHEDULE_SUNDAY = [
    {"time": "09:00", "icon": "🌅", "cat": "gray",   "text": "Подъём без будильника + намаз"},
    {"time": "10:00", "icon": "☕", "cat": "orange",  "text": "Завтрак + семейное время"},
    {"time": "11:00", "icon": "📖", "cat": "yellow",  "text": "Чтение / Книга №1 или №2"},
    {"time": "13:00", "icon": "🥗", "cat": "orange",  "text": "Обед"},
    {"time": "14:00", "icon": "🔄", "cat": "blue",   "text": "Обзор недели + планирование следующей"},
    {"time": "16:00", "icon": "🚶", "cat": "green",   "text": "Прогулка / свежий воздух"},
    {"time": "18:00", "icon": "🍽️", "cat": "orange",  "text": "Ужин"},
    {"time": "19:00", "icon": "♟️", "cat": "blue",   "text": "Шахматы / Английский Anki"},
    {"time": "20:00", "icon": "📊", "cat": "yellow",  "text": "Финансовый учёт + итоги недели"},
    {"time": "21:00", "icon": "📖", "cat": "yellow",  "text": "Чтение / расслабление"},
    {"time": "22:30", "icon": "🌙", "cat": "gray",   "text": "Вечерний намаз + подготовка ко сну"},
    {"time": "23:00", "icon": "😴", "cat": "gray",   "text": "СОН"},
]


def get_dow() -> int:
    """Return day-of-week: Mon=1 ... Sun=0"""
    from datetime import datetime
    dow = datetime.now().weekday() + 1
    return 0 if dow == 7 else dow


def get_today_schedule() -> list:
    dow = get_dow()
    if dow == 0:
        return SCHEDULE_SUNDAY
    if dow == 6:
        return SCHEDULE_SATURDAY
    if dow in MARTIAL_DAYS:
        return SCHEDULE_MARTIAL
    return SCHEDULE_NORMAL
