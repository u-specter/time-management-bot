DAY_NAMES = {
    "ru": {1: "Понедельник", 2: "Вторник", 3: "Среда",
           4: "Четверг", 5: "Пятница", 6: "Суббота", 0: "Воскресенье"},
    "uz": {1: "Dushanba", 2: "Seshanba", 3: "Chorshanba",
           4: "Payshanba", 5: "Juma", 6: "Shanba", 0: "Yakshanba"},
}

WEEK_THEMES = {
    "ru": {
        1: "Стартап-день 🚀", 2: "Бой-день 🥋", 3: "Карьера-день 📈",
        4: "Бой-день 🥋", 5: "Итоги-день 💰", 6: "Свободный день + тренировка 🥋",
        0: "День отдыха 🔄",
    },
    "uz": {
        1: "Startup kuni 🚀", 2: "Jang kuni 🥋", 3: "Martaba kuni 📈",
        4: "Jang kuni 🥋", 5: "Yakunlar kuni 💰", 6: "Erkin kun + mashg'ulot 🥋",
        0: "Dam olish kuni 🔄",
    },
}

S = {
    "ru": {
        # /start
        "start": (
            "👋 <b>Умиджон, твой личный командный центр</b>\n\n"
            "/today — расписание дня\n"
            "/done 3 — отметить задачу #3\n"
            "/stats — прогресс за сегодня\n"
            "/week — план недели"
        ),
        # /app
        "app": "📱 Открыть дашборд:",
        # /today
        "today_btn": "📱 Открыть день →",
        # /done
        "done_invalid": "❌ Используй: /done 3",
        "done_no_task": "❌ Нет задачи #{n}. Всего: {total}",
        "done_ok": "✅ <b>{icon} {text}</b>\n\nЗадача #{n} отмечена.",
        "done_err": "⚠️ Ошибка: {e}",
        # /stats
        "stats": "📊 <b>Прогресс сегодня</b>\n\n✅ {done}/{total} ({pct}%) {mood}",
        "stats_err": "⚠️ Ошибка: {e}",
        # /week
        "week": "🗓 <b>{day}</b> — {theme}\n\nПолный план в дашборде:",
        # /lang
        "lang_set_uz": "🌐 Til o'zgartirildi: O'zbek 🇺🇿",
        "lang_set_ru": "🌐 Язык изменён: Русский 🇷🇺",
        "lang_invalid": "❌ Используй: /lang uz или /lang ru",
        # keyboard
        "btn_dashboard": "📱 Открыть дашборд",
        "btn_open": "📱 Посмотреть →",
        "btn_finances": "📱 Открыть финансы →",
        # notifications
        "morning": (
            "🌅 <b>Доброе утро, Умиджон!</b>\n\n"
            "📅 <b>{day}</b> — {theme}\n"
            "Сегодня: <b>{count} задач</b>\n\n"
            "⏰ Первый блок в {time} {icon}"
        ),
        "morning_btn": "📱 Открыть день →",
        "evening": "📊 <b>Итоги дня — {day}</b>\n\n{stats}",
        "evening_stats": "✅ Выполнено: <b>{done}/{total}</b> ({pct}%) {mood}",
        "evening_fallback": "📊 Открой дашборд для статистики",
        "evening_btn": "📱 Посмотреть →",
        "martial": "🥋 <b>Через 15 минут — ЕДИНОБОРСТВА!</b>\n\nВыходи в 20:30 🚶",
        "weekly": (
            "📅 <b>Время планирования недели!</b>\n\n"
            "💰 Не забудь финансовый учёт\n"
            "📊 Подведи итоги 7 дней"
        ),
        "weekly_btn": "📱 Открыть финансы →",
        # hourly
        "hourly_notify": "⏰ <b>{time}</b> — {icon} {text}",
        "poll_question": "📊 Как прошло?\n{icon} {time} — {text}",
        "poll_yes": "✅ Выполнено",
        "poll_no": "❌ Не выполнено",
        # quote
        "quote_prompt": (
            "Напиши одну короткую вдохновляющую цитату или мудрую мысль на русском языке "
            "(не более 2 предложений) для человека, который развивает продуктивные привычки, "
            "учит английский, занимается шахматами и единоборствами. "
            "Только саму цитату, без кавычек и атрибуции."
        ),
    },
    "uz": {
        # /start
        "start": (
            "👋 <b>Umidjon, shaxsiy boshqaruv markazingiz</b>\n\n"
            "/today — bugungi jadval\n"
            "/done 3 — 3-vazifani belgilash\n"
            "/stats — bugungi progress\n"
            "/week — hafta rejasi"
        ),
        # /app
        "app": "📱 Dashboardni ochish:",
        # /today
        "today_btn": "📱 Kunni ochish →",
        # /done
        "done_invalid": "❌ Foydalanish: /done 3",
        "done_no_task": "❌ {n}-vazifa yo'q. Jami: {total}",
        "done_ok": "✅ <b>{icon} {text}</b>\n\n{n}-vazifa belgilandi.",
        "done_err": "⚠️ Xatolik: {e}",
        # /stats
        "stats": "📊 <b>Bugungi progress</b>\n\n✅ {done}/{total} ({pct}%) {mood}",
        "stats_err": "⚠️ Xatolik: {e}",
        # /week
        "week": "🗓 <b>{day}</b> — {theme}\n\nTo'liq reja dashboardda:",
        # /lang
        "lang_set_uz": "🌐 Til o'zgartirildi: O'zbek 🇺🇿",
        "lang_set_ru": "🌐 Язык изменён: Русский 🇷🇺",
        "lang_invalid": "❌ Foydalanish: /lang uz yoki /lang ru",
        # keyboard
        "btn_dashboard": "📱 Dashboardni ochish",
        "btn_open": "📱 Ko'rish →",
        "btn_finances": "📱 Moliyani ochish →",
        # notifications
        "morning": (
            "🌅 <b>Xayrli tong, Umidjon!</b>\n\n"
            "📅 <b>{day}</b> — {theme}\n"
            "Bugun: <b>{count} ta vazifa</b>\n\n"
            "⏰ Birinchi blok {time} {icon}"
        ),
        "morning_btn": "📱 Kunni ochish →",
        "evening": "📊 <b>Kun yakunlari — {day}</b>\n\n{stats}",
        "evening_stats": "✅ Bajarildi: <b>{done}/{total}</b> ({pct}%) {mood}",
        "evening_fallback": "📊 Statistika uchun dashboardni oching",
        "evening_btn": "📱 Ko'rish →",
        "martial": "🥋 <b>15 daqiqadan so'ng — KURASH!</b>\n\nChiqishga tayyorlaning, 20:30 da chiqing 🚶",
        "weekly": (
            "📅 <b>Hafta rejalashtirish vaqti!</b>\n\n"
            "💰 Moliyaviy hisobni unutmang\n"
            "📊 7 kunni yakunlang"
        ),
        "weekly_btn": "📱 Moliyani ochish →",
        # hourly
        "hourly_notify": "⏰ <b>{time}</b> — {icon} {text}",
        "poll_question": "📊 Qanday bo'ldi?\n{icon} {time} — {text}",
        "poll_yes": "✅ Bajarildi",
        "poll_no": "❌ Bajarilmadi",
        # quote
        "quote_prompt": (
            "O'zbek tilida bitta qisqa ilhomlantiruvchi iqtibos yoki dono fikr yoz "
            "(2 jumladan ko'p bo'lmasin) samarali odatlar shakllantiruvchi, "
            "ingliz tili o'rganuvchi, shaxmat va kurash bilan shug'ullanuvchi kishi uchun. "
            "Faqat iqtibosning o'zini yoz, tirnoqsiz va manbasiz."
        ),
    },
}
