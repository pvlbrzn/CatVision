import cv2
import time
import os
from datetime import datetime
from typing import Optional

PHOTO_DIR = "photos"


def capture_photo() -> Optional[str]:
    """
    Делает снимок с камеры и сохраняет в папку `photos`.

    Returns:
        str | None: Путь к сохранённому фото, либо None при ошибке.
    """
    # Убедимся, что папка существует
    os.makedirs(PHOTO_DIR, exist_ok=True)

    # Уникальное имя по времени
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(PHOTO_DIR, f"photo_{timestamp}.jpg")

    # Открытие камеры
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Камера не открылась.")
        return None

    # Небольшая задержка (для автофокуса)
    time.sleep(0.5)

    # Захват кадра
    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(filename, frame)
        print(f"[INFO] Фото сохранено: {filename}")
        return filename

    print("[ERROR] Не удалось сделать снимок.")
    return None
