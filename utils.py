import subprocess
import threading
import time
from typing import Optional
from flask import Flask, Response, request, redirect
import cv2

# Flask приложение
flask_app = Flask(__name__)

# Глобальные переменные
camera: Optional[cv2.VideoCapture] = None
flask_thread: Optional[threading.Thread] = None
tunnel_proc: Optional[subprocess.Popen] = None


def gen_frames():
    """
    Генератор кадров с камеры для видеопотока.
    Возвращает кадры как multipart/jpeg поток.
    """
    global camera

    if camera is None:
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("[ERROR] Не удалось открыть камеру.")
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    except GeneratorExit:
        pass
    finally:
        print("[INFO] Поток кадров завершён.")


@flask_app.route('/video')
def video() -> Response:
    """HTTP endpoint для видеопотока."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@flask_app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>🐱 CatSpy Live</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #121212;
                color: #fff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                text-align: center;
            }

            h2 {
                margin-bottom: 20px;
                font-size: 2rem;
                color: #f5c542;
            }

            img {
                width: 90vw;
                max-width: 600px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
            }

            .button {
                margin-top: 20px;
                padding: 12px 24px;
                font-size: 1rem;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            .button:hover {
                background-color: #c0392b;
            }

            @media (max-width: 480px) {
                h2 {
                    font-size: 1.5rem;
                }

                .button {
                    width: 80%;
                    font-size: 1rem;
                }
            }
        </style>
    </head>
    <body>
        <h2>🐱 CatSpy Live</h2>
        <img src="/video" alt="Live Stream" />
        <form action="/stop" method="post">
            <button class="button" type="submit">🛑 Stop Stream</button>
        </form>
    </body>
    </html>
    """


@flask_app.route('/stop', methods=['POST'])
def stop_stream():
    """
    Endpoint triggered by the 'Stop Stream' button in the UI.
    """
    stop_all()
    return redirect('/')


def run_flask() -> None:
    """Запускает Flask сервер."""
    flask_app.run(host='0.0.0.0', port=5000)


def start_flask() -> None:
    """
    Запускает Flask сервер в отдельном потоке.
    Ждёт 2 секунды для инициализации.
    """
    global flask_thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(2)


def start_tunnel() -> subprocess.Popen:
    """
    Запускает туннель через localtunnel на порту 5000.
    Возвращает процесс туннеля.
    """
    global tunnel_proc
    tunnel_proc = subprocess.Popen(
        ["C:\\Program Files\\nodejs\\npx.cmd", "localtunnel", "--port", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return tunnel_proc


def get_tunnel_url(proc: subprocess.Popen) -> Optional[str]:
    """
    Получает URL туннеля из stdout процесса.
    """
    for line in proc.stdout:
        if "your url is:" in line:
            return line.strip().split("your url is:")[-1].strip()
    return None


def stop_all() -> None:
    """
    Останавливает камеру и туннель.
    Flask поток продолжает работать.
    """
    global camera, tunnel_proc

    if camera is not None:
        camera.release()
        camera = None
        print("[INFO] Камера остановлена")

    if tunnel_proc is not None:
        tunnel_proc.terminate()
        tunnel_proc = None
        print("[INFO] Туннель остановлен")
