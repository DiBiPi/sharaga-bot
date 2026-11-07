import os
import datetime
import telebot
from telebot import types

# =====================================================================
# ИНИЦИАЛИЗАЦИЯ БОТА И НАСТРОЙКИ
# =====================================================================

# Загружаем токен из переменных окружения (GitHub Secrets)
TOKEN = os.getenv("9216880435:AAG_SChikwd2uhIcFUYfhPiYfL5qaP5qODw")
if not TOKEN:
    raise ValueError("Ошибка: не задана переменная окружения BOT_TOKEN!")

bot = telebot.TeleBot(TOKEN)

# Приветственный текст с контактом для обратной связи и заказов
WELCOME_TEXT = (
    "👋 Привет! Этот бот сделан по запросу.\n\n"
    "Для вашего удобства присутствует обратная связь: если у вас есть какие-то "
    "пожелания, идеи или предложения, можете писать @dikango.\n\n"
    "Также, если хотите, вы можете профинансировать создание подобных ботов, "
    "сайтов или веб-приложений.\n\n"
    "👇 <b>Выберите нужную неделю в меню ниже:</b>"
)

# Список дней недели для генерации кнопок и проверки нажатий
DAYS_OF_WEEK = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

# =====================================================================
# БАЗА ДАННЫХ РАСПИСАНИЯ (ГРУППА 10-кЮРо25-6)
# Ключ верхнего уровня — дата понедельника соответствующей недели (ГГГГ-ММ-ДД)
# =====================================================================

SCHEDULE_DB = {
    # ----------------- НЕДЕЛЯ 1 (02.11.2026 — 07.11.2026) -----------------
    "2026-11-02": {
        "Понедельник": [
            {"time": "10.40-12.10", "subject": "МДК.02.02 Уголовный процесс (л)", "teacher": "Сенчихин С.П.", "room": "203"},
            {"time": "12.50-14.20", "subject": "Язык и стиль юридических документов (л)", "teacher": "Мамедов Э.Р.", "room": "203"},
            {"time": "14.30-16.00", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "203"},
        ],
        "Вторник": [
            {"time": "09.00-10.30", "subject": "Жилищное право (л)", "teacher": "Ковалева А.Д.", "room": "203"},
            {"time": "10.40-12.10", "subject": "МДК.03.02 Архивное дело в суде (л)", "teacher": "Борисова А.А.", "room": "203"},
            {"time": "12.50-14.20", "subject": "МДК.01.03 Гражданский процесс (л)", "teacher": "Крылова Н.Н.", "room": "203"},
            {"time": "14.30-16.00", "subject": "МДК.02.02 Уголовный процесс (л)", "teacher": "Сенчихин С.П.", "room": "203"},
        ],
        "Среда": [
            {"time": "Весь день", "subject": "🎉 Нерабочий праздничный день — День народного единства", "teacher": None, "room": None},
        ],
        "Четверг": [
            {"time": "09.00-10.30", "subject": "МДК.01.03 Гражданский процесс (л)", "teacher": "Крылова Н.Н.", "room": "203"},
            {"time": "10.40-12.10", "subject": "МДК.03.02 Архивное дело в суде (л)", "teacher": "Борисова А.А.", "room": "203"},
            {"time": "12.50-14.20", "subject": "МДК.02.03 Правоохранительные и судебные органы (л)", "teacher": "Алексеева Т.С.", "room": "203"},
            {"time": "14.30-16.00", "subject": "Социология и политология (л)", "teacher": "Кисель М.А.", "room": "203"},
        ],
        "Пятница": [
            {"time": "10.40-12.10", "subject": "МДК.01.03 Гражданский процесс (л)", "teacher": "Крылова Н.Н.", "room": "203"},
            {"time": "12.50-14.20", "subject": "Жилищное право (л)", "teacher": "Ковалева А.Д.", "room": "203"},
            {"time": "14.30-16.00", "subject": "Основы бережливого производства (л)", "teacher": "Сайдов А.В.", "room": "203"},
        ],
        "Суббота": [
            {"time": "09.00-10.30", "subject": "МДК.02.03 Правоохранительные и судебные органы (л)", "teacher": "Алексеева Т.С.", "room": "203"},
            {"time": "10.40-12.10", "subject": "Социология и политология (л)", "teacher": "Кисель М.А.", "room": "203"},
            {"time": "12.50-14.20", "subject": "МДК.02.03 Правоохранительные и судебные органы (л)", "teacher": "Алексеева Т.С.", "room": "203"},
        ],
    },

    # ----------------- НЕДЕЛЯ 2 (09.11.2026 — 14.11.2026) -----------------
    "2026-11-09": {
        "Понедельник": [
            {"time": "12.50-14.20", "subject": "МДК.02.03 Правоохранительные и судебные органы (с)", "teacher": "Алексеева Т.С.", "room": "304"},
            {"time": "14.30-16.00", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "207"},
            {"time": "16.10-17.40", "subject": "Язык и стиль юридических документов (с)", "teacher": "Мамедов Э.Р.", "room": "204"},
        ],
        "Вторник": [
            {"time": "09.00-10.30", "subject": "МДК.03.02 Архивное дело в суде (л)", "teacher": "Борисова А.А.", "room": "201"},
            {"time": "10.40-12.10", "subject": "Основы бережливого производства (с)", "teacher": "Сайдов А.В.", "room": "42"},
            {"time": "12.50-14.20", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "201"},
            {"time": "14.30-16.00", "subject": "Социология и политология (с)", "teacher": "Кисель М.А.", "room": "105"},
            {"time": "16.10-17.40", "subject": "Язык и стиль юридических документов (с)", "teacher": "Мамедов Э.Р.", "room": "105"},
        ],
        "Среда": [
            {"time": "09.00-10.30", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "42"},
            {"time": "10.40-12.10", "subject": "МДК.03.02 Архивное дело в суде (с)", "teacher": "Борисова А.А.", "room": "303"},
            {"time": "12.50-14.20", "subject": "МДК.02.03 Правоохранительные и судебные органы (с)", "teacher": "Алексеева Т.С.", "room": "42"},
            {"time": "14.30-16.00", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "206"},
        ],
        "Четверг": [
            {"time": "12.50-14.20", "subject": "МДК.02.02 Уголовный процесс (л)", "teacher": "Сенчихин С.П.", "room": "201"},
        ],
        "Пятница": [
            {"time": "09.00-10.30", "subject": "Социология и политология (с)", "teacher": "Кисель М.А.", "room": "102"},
            {"time": "10.40-12.10", "subject": "МДК.03.02 Архивное дело в суде (с)", "teacher": "Борисова А.А.", "room": "42"},
            {"time": "12.50-14.20", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "203"},
            {"time": "14.30-16.00", "subject": "МДК.03.02 Архивное дело в суде (с)", "teacher": "Борисова А.А.", "room": "27"},
        ],
        "Суббота": [
            {"time": "14.30-16.00", "subject": "Жилищное право (с)", "teacher": "Ковалева А.Д.", "room": "208"},
        ],
    },

    # ----------------- НЕДЕЛЯ 3 (16.11.2026 — 21.11.2026) -----------------
    "2026-11-16": {
        "Понедельник": [
            {"time": "09.00-10.30", "subject": "МДК.03.02 Архивное дело в суде (с)", "teacher": "Борисова А.А.", "room": "303"},
            {"time": "10.40-12.10", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "42"},
            {"time": "12.50-14.20", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "105"},
        ],
        "Вторник": [
            {"time": "12.50-14.20", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "202"},
            {"time": "14.30-16.00", "subject": "Социология и политология (с)", "teacher": "Кисель М.А.", "room": "202"},
        ],
        "Среда": [
            {"time": "09.00-10.30", "subject": "МДК.03.02 Архивное дело в суде (с)", "teacher": "Борисова А.А.", "room": "206"},
            {"time": "10.40-12.10", "subject": "Язык и стиль юридических документов (с)", "teacher": "Мамедов Э.Р.", "room": "206"},
            {"time": "12.50-14.20", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "101"},
            {"time": "14.30-16.00", "subject": "Основы бережливого производства (зачет)", "teacher": "Сайдов А.В.", "room": "105"},
        ],
        "Четверг": [
            {"time": "09.00-10.30", "subject": "МДК.02.03 Правоохранительные и судебные органы (с)", "teacher": "Алексеева Т.С.", "room": "102"},
            {"time": "10.40-12.10", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "203"},
        ],
        "Пятница": [
            {"time": "12.50-14.20", "subject": "МДК.03.02 Архивное дело в суде (зачет)", "teacher": "Борисова А.А.", "room": "303"},
            {"time": "14.30-16.00", "subject": "Социология и политология (зачет)", "teacher": "Кисель М.А.", "room": "105"},
        ],
        "Суббота": [
            {"time": "09.00-10.30", "subject": "Язык и стиль юридических документов (зачет)", "teacher": "Мамедов Э.Р.", "room": "204"},
            {"time": "10.40-12.10", "subject": "МДК.02.02 Уголовный процесс (с)", "teacher": "Сенчихин С.П.", "room": "203"},
            {"time": "14.30-16.00", "subject": "Жилищное право (зачет)", "teacher": "Ковалева А.Д.", "room": "204"},
        ],
    },

    # ----------------- НЕДЕЛЯ 4 (с 23.11.2026) -----------------
    "2026-11-23": {
        "Понедельник": [
            {"time": "10.40-12.10", "subject": "МДК.01.03 Гражданский процесс (с)", "teacher": "Крылова Н.Н.", "room": "303"},
            {"time": "12.50-14.20", "subject": "МДК.02.03 Правоохранительные и судебные органы (зачет)", "teacher": "Алексеева Т.С.", "room": "42"},
        ],
    },
}

# Словарь для хранения выбранной недели каждым пользователем (chat_id -> 0 или 1)
user_week_offset = {}


# =====================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И КЛАВИАТУРЫ
# =====================================================================

def get_monday_key(week_offset: int = 0) -> str:
    """
    Возвращает дату понедельника в формате 'ГГГГ-ММ-ДД'.
    week_offset = 0 -> текущая неделя
    week_offset = 1 -> следующая неделя
    """
    today = datetime.date.today()
    current_monday = today - datetime.timedelta(days=today.weekday())
    target_monday = current_monday + datetime.timedelta(weeks=week_offset)
    return target_monday.strftime("%Y-%m-%d")


def format_date_ru(monday_str: str, day_index: int) -> str:
    """Вычисляет точную дату выбранного дня недели в формате ДД.ММ.ГГГГ."""
    monday_date = datetime.datetime.strptime(monday_str, "%Y-%m-%d").date()
    target_date = monday_date + datetime.timedelta(days=day_index)
    return target_date.strftime("%d.%m.%Y")


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    """Создает главное нижнее меню с двумя кнопками выбора недели."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_current = types.KeyboardButton("Текущая неделя")
    btn_next = types.KeyboardButton("Следующая неделя")
    markup.add(btn_current, btn_next)
    return markup


def get_days_keyboard() -> types.ReplyKeyboardMarkup:
    """Создает нижнее меню с 6 днями недели и кнопкой возврата."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    day_buttons = [types.KeyboardButton(day) for day in DAYS_OF_WEEK]
    btn_back = types.KeyboardButton("🔙 Назад")
    markup.add(*day_buttons)
    markup.add(btn_back)
    return markup


# =====================================================================
# ОБРАБОТЧИКИ СООБЩЕНИЙ И КНОПОК
# =====================================================================

@bot.message_handler(commands=["start"])
def handle_start(message):
    """Приветствует пользователя и выводит меню с выбором недели."""
    user_week_offset[message.chat.id] = 0
    bot.send_message(
        message.chat.id,
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda msg: msg.text in ["Текущая неделя", "Следующая неделя"])
def handle_week_choice(message):
    """Запоминает выбранную неделю и переключает клавиатуру на 6 дней недели."""
    if message.text == "Текущая неделя":
        user_week_offset[message.chat.id] = 0
        week_title = "текущую неделю"
    else:
        user_week_offset[message.chat.id] = 1
        week_title = "следующую неделю"

    monday_key = get_monday_key(user_week_offset[message.chat.id])
    monday_formatted = format_date_ru(monday_key, 0)

    bot.send_message(
        message.chat.id,
        f"📅 Выбрано расписание на <b>{week_title}</b> (с {monday_formatted}).\n"
        f"Выберите день недели на клавиатуре ниже:",
        parse_mode="HTML",
        reply_markup=get_days_keyboard()
    )


@bot.message_handler(func=lambda msg: msg.text == "🔙 Назад")
def handle_back_button(message):
    """Возвращает пользователя к выбору текущей или следующей недели."""
    bot.send_message(
        message.chat.id,
        "Выберите неделю:",
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda msg: msg.text in DAYS_OF_WEEK)
def handle_day_choice(message):
    """Выводит расписание на конкретный выбранный день."""
    day_name = message.text
    day_index = DAYS_OF_WEEK.index(day_name)

    # Берем сохраненную неделю пользователя (по умолчанию 0 — текущая)
    offset = user_week_offset.get(message.chat.id, 0)
    monday_key = get_monday_key(offset)
    exact_date = format_date_ru(monday_key, day_index)

    # Ищем расписание в базе
    week_schedule = SCHEDULE_DB.get(monday_key, {})
    day_lessons = week_schedule.get(day_name, [])

    if not day_lessons:
        bot.send_message(
            message.chat.id,
            f"📌 <b>{day_name} ({exact_date})</b>\n\nНа этот день учебных занятий нет (выходной или день самостоятельной работы).",
            parse_mode="HTML"
        )
        return

    # Формируем текст сообщения с парами
    header = f"📚 <b>Расписание на {day_name} ({exact_date})</b>\n👥 Группа: 10-кЮРо25-6\n"
    lessons_text = []

    for lesson in day_lessons:
        block = f"⏰ <b>{lesson['time']}</b>\n📖 {lesson['subject']}"

        # Выводим аудиторию, только если она указана
        if lesson.get("room"):
            block += f"\n🚪 Аудитория: {lesson['room']}"

        # Выводим преподавателя, только если он указан
        if lesson.get("teacher"):
            block += f"\n👤 Преподаватель: {lesson['teacher']}"

        lessons_text.append(block)

    full_response = header + "\n" + "\n\n".join(lessons_text)
    bot.send_message(message.chat.id, full_response, parse_mode="HTML")


# =====================================================================
# ЗАПУСК БОТА
# =====================================================================

if __name__ == "__main__":
    print("Бот sharaga.py успешно запущен и ожидает сообщений...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)