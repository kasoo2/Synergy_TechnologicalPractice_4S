import os
import telebot
import spacy
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

nlp = spacy.load("ru_core_news_sm")

intents = {
    "greeting": {
        "keywords": {"привет", "здравствовать", "добрый", "hi"},
        "reply": "Здравствуйте! Я ИТ-ассистент АО «Северсталь-Инфоком». Чем могу помочь?"
    },
    "password": {
        "keywords": {"пароль", "сброс", "забывать", "доступ", "блокировка"},
        "reply": "Сбросить пароль можно на портале: https://it.severstal.com/login/?forgot_password=yes"
    },
    "contacts": {
        "keywords": {"телефон", "контакт", "связь"},
        "reply": "Основные контакты: +7 (8202) 53-09-30"
    },
    "name": {
        "keywords": {"название", "называться"},
        "reply": "Полное название: Акционерное общество «Северсталь-Инфоком»."
    },
    "location": {
        "keywords": {"адрес", "расположение", "располагаться"},
        "reply": "Юридический адрес: 162602, Россия, г. Череповец, ул. Ленина, д. 123А."
    },
    "service": {
        "keywords": {"услуга", "работа", "делать"},
        "reply": "1. Разработка компьютерного программного обеспечения;\n"
                 "2. Управление процессами ТОиР оборудования промышленных предприятий — программное обеспечение «Надежность» и комплекс решений для автоматизации ТОиР;\n"
                 "3. Автоматизация процессов управления производством — система «MES Металлургия»;\n"
                 "4. Оптимизация процессов планирования и цепочек поставок компании в различных отраслях — система производственного планирования IPS;\n"
                 "5. Методологический и технологический консалтинг для промышленных предприятий;\n"
                 "6. Услуги по внедрению и поддержке 1С решений;\n"
                 "7. Услуги по роботизации процессов (RPA);\n"
                 "8. Внедрение решений на базе искусственного интеллекта (CV/ML);\n"
                 "9. Иммеррасивные технологии VR/AR"
    },
    "employee": {
        "keywords": {"сотрудник", "работник", "специалист"},
        "reply": "В компании уже насчитывается более 3000 специалистов, а также имеется 23 офиса в России."
    },
    "gratitude": {
        "keywords": {"спасибо", "благодарить", "выручить"},
        "reply": "Пожалуйста, всегда рад помочь!"
    }
}
default_reply = "Не совсем понял вас. Попробуйте переформулировать или введите 'контакты', чтобы связаться с оператором."

def process_text(text):
    """NLP-обработка: токенизация и лемматизация"""
    doc = nlp(text.lower())
    lemmas = {token.lemma_ for token in doc if not token.is_stop and not token.is_punct}

    return lemmas

def get_reply(user_input):
    """Поиск совпадений и выдача ответа"""
    user_lemmas = process_text(user_input)

    for intent_name, intent_data in intents.items():
        if user_lemmas.intersection(intent_data["keywords"]):
            return intent_data["reply"]

    return default_reply


@bot.message_handler(commands=["start"])
def start_command(message):
    """Обработчик команды /start"""
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Я ИТ-ассистент АО «Северсталь-Инфоком».\n"
        "Задайте вопрос о паролях, услуге или контактах."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик текстовых сообщений"""
    user_text = message.text.strip()

    # Игнорируем команды выхода в Telegram (они просто не дают ответа)
    if user_text.lower() in {"выход", "exit", "q"}:
        bot.reply_to(message, "Чтобы завершить работу с ботом, просто закройте чат")

        return

    reply = get_reply(user_text)
    bot.reply_to(message, reply)


print("Telegram-бот запущен...")

bot.infinity_polling()