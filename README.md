# 🌦️ Peri Weather AI Agent – Telegram Bot

🤖 **Live Demo Bot:** [@peri_weather_bot](https://t.me/peri_weather_bot)
---

🚀 A production-ready, cloud-deployed Telegram bot that autonomously monitors weather conditions, analyzes risk, and delivers intelligent text & voice alerts in real time.

---

## ✨ Overview

**Weather AI Agent** is an autonomous Telegram-based backend system that continuously tracks weather conditions using live APIs, performs AI-style risk analysis, and sends **smart alerts, forecasts, and voice notifications** to users.

The bot runs **24/7 in the cloud** and supports **multi-city subscriptions**, making it suitable for real-world alerting systems and AI agent demonstrations.

---

## 🔥 Key Features

### 🌍 Weather Intelligence
- Current weather report
- Past 3-day weather analysis
- Next 3-day forecast
- Next 24-hour (3-hour interval) breakdown


### 🧠 AI-Style Reasoning
- Risk-based alert classification:
  - ✅ Normal
  - 👀 Watch
  - ⚠️ Warning
  - 🚨 Emergency
- NLP-generated explanations explaining *why* an alert was triggered

### 🔔 Autonomous Alerts
- Auto weather updates **every 10 minutes**
- Multi-city subscriptions per user
- Stop / resume alerts anytime

### 🔊 Voice Alerts
- Text-to-speech alerts for **Warning & Emergency** conditions
- Helps users react quickly during critical weather events

### 🎛 User-Friendly UI
- Inline buttons (Telegram UI)
- One-click subscribe / unsubscribe
- List subscribed cities
- Clean interactive experience

---

## 🏗️ Architecture
```
Telegram User
↓
Telegram Bot API
↓
Weather AI Agent (Python Backend)

├─ Weather API Integration
├─ Risk Analysis & NLP
├─ Background Scheduler (10-min loop)
├─ Voice Alert Engine
└─ Subscription Manager
↓
OpenWeatherMap API

```


> The bot itself functions as an **asynchronous backend service**, similar to a microservice.

---

## 🛠️ Tech Stack

- **Python**
- **python-telegram-bot (v20+)**
- **OpenWeatherMap API**
- **gTTS (Text-to-Speech)**
- **Async background processing**
- **Railway (Cloud Deployment)**

---

## ☁️ Deployment

The bot is deployed on **Railway** as a continuously running background service.

✔ Runs **24/7**  
✔ No sleep / downtime  
✔ Secure environment variables  
✔ Production-ready setup  

---

## ⚙️ Setup & Run Locally

###  Clone Repository

```bash
git clone https://github.com/gopagoniajay/weather-alert-agent/weather-ai-agent.git
cd weather-ai-agent

## Install Dependencies
pip install -r requirements.txt

## Configure Environment
Create config.py (not committed):

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

## Run Bot
python bot.py

```
---

📂 Project Structure
```bash

weather-ai-agent/
│
├── bot.py                 # Main backend service
├── config.example.py      # Environment template
├── requirements.txt
├── runtime.txt            # Python version (Railway)
├── .gitignore
└── README.md
```
---

🔐 Security Practices

- API keys are never committed
- Secrets managed via environment variables
- User subscription data stored locally
- GitHub secret scanning handled correctly
---

🧠 Why This Is an AI Agent

- This project qualifies as an AI-style autonomous agent because it:
- Continuously observes external data (weather APIs)
- Makes decisions based on risk scoring
- Generates natural-language explanations
- Acts autonomously via background scheduling
- Escalates alerts intelligently with voice output



