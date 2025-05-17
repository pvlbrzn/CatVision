# 🐱 CatVision – Remote Cat Surveillance with Telegram and Flask

CatVision is a lightweight Python project that lets you remotely watch your cat (or anything else!) through your webcam via a Telegram bot. It supports live video streaming, photo snapshots, and a stylish web interface — even from your phone.

---

## 🚀 Features

* 📷 Take instant webcam **photos** via Telegram
* 📺 Start/stop **live stream** from anywhere
* 💬 Telegram **bot interface**
* 🧠 Smart camera control (auto-release to prevent freeze)
* 💥 Responsive & modern **web interface**

---

## 🎞 Requirements

* Python 3.8+
* Node.js (for `localtunnel`)
* Webcam

### Python packages

Install with pip:

```bash
pip install -r requirements.txt
```

## ⚙️ Setup

### 1. Clone the project

```bash
git clone https://github.com/pvlbrzn/CatVision.git
cd CatVision
```

### 2. Set up `.env`

Create a `.env` file with your Telegram credentials:

```
TG_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
```

You can find your `CHAT_ID` using [this bot](https://t.me/userinfobot).

---

## ▶️ Running

```bash
python bot.py
```

The bot will respond to:

* `/start` – show menu
* 📷 **Фото** – take a snapshot
* 📺 **Стрим** – start live stream
* 📛 **Стоп** – stop the stream

You’ll receive a **live video link** through localtunnel like:

---

## 🧠 Project Structure

```
CatVision/
│
├── bot.py          # Telegram bot logic
├── utils.py        # Flask stream server + tunnel mgmt
├── photo.py        # Webcam snapshot util
├── photos/         # Saved photos
├── .env            # Secret credentials
└── README.md       # You are here
```

---

## 🛡 Known Issues

* ❗ On Windows, make sure `npx` is available in PATH.
* 💻 The camera may hang if used simultaneously by multiple processes. This is handled by releasing the device properly in code.

---

## 📜 License

MIT – use it freely, just don’t spy on humans 😼

---

