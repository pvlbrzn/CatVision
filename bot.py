import os
import cv2
from datetime import datetime
from dotenv import load_dotenv
import telebot
from utils import start_flask, start_tunnel, get_tunnel_url, stop_all

# Загрузка переменных окружения
load_dotenv()

# Получение токена и ID чата из .env
TOKEN: str = os.getenv("TG_TOKEN", "")
CHAT_ID: str = os.getenv("CHAT_ID", "")

bot = telebot.TeleBot(TOKEN)

# Директория для фото
PHOTO_DIR: str = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и кнопки управления.
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📷 Фото", "📺 Стрим", "🛑 Стоп")
    bot.send_message(message.chat.id, "🐾 CatVision готов следить за котом!", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == "📷 Фото")
def photo_cmd(message: telebot.types.Message) -> None:
    """
    Делает снимок с камеры и отправляет фото в чат.
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_path = os.path.join(PHOTO_DIR, f"cat_{timestamp}.jpg")
        cv2.imwrite(photo_path, frame)
        with open(photo_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "❌ Не удалось сделать фото")


@bot.message_handler(func=lambda msg: msg.text == "📺 Стрим")
def stream_cmd(message: telebot.types.Message) -> None:
    """
    Запускает Flask-сервер и туннель через localtunnel.
    Отправляет ссылку на прямой эфир.
    """
    start_flask()
    tunnel_proc = start_tunnel()
    url = get_tunnel_url(tunnel_proc)

    if url:
        bot.send_message(message.chat.id, f"🔴 Прямой эфир доступен по ссылке:\n{url}")
    else:
        bot.send_message(message.chat.id, "❌ Не удалось получить ссылку на стрим")


@bot.message_handler(func=lambda msg: msg.text == "🛑 Стоп")
def stop_cmd(message: telebot.types.Message) -> None:
    """
    Останавливает камеру и туннель.
    """
    stop_all()
    bot.send_message(message.chat.id, "🛑 Стрим остановлен")


if __name__ == "__main__":
    bot.polling()
