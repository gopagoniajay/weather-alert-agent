import requests
import asyncio
import os
import json
from datetime import datetime, timedelta
from gtts import gTTS

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Bot
)

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# =======================
# STORAGE
# =======================
SUB_FILE = "subscriptions.json"

def load_subs():
    if not os.path.exists(SUB_FILE):
        return {}
    with open(SUB_FILE, "r") as f:
        return json.load(f)

def save_subs(data):
    with open(SUB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# =======================
# WEATHER API
# =======================
def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    d = requests.get(url).json()
    return {
        "temp": d["main"]["temp"],
        "humidity": d["main"]["humidity"],
        "wind": d["wind"]["speed"],
        "rain": d.get("rain", {}).get("1h", 0)
    }

def get_forecast(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    return requests.get(url).json()["list"]

# =======================
# RISK + NLP
# =======================
def risk_and_nlp(w):
    score = 0
    reasons = []

    if w["temp"] >= 40:
        score += 30; reasons.append("extreme heat")
    if w["rain"] >= 20:
        score += 30; reasons.append("heavy rainfall")
    if w["wind"] >= 15:
        score += 20; reasons.append("strong winds")
    if w["humidity"] >= 85:
        score += 10; reasons.append("high humidity")

    if score >= 70:
        level = "🚨 EMERGENCY"
    elif score >= 40:
        level = "⚠️ WARNING"
    elif score >= 20:
        level = "👀 WATCH"
    else:
        level = "✅ NORMAL"

    explanation = (
        "🧠 AI Explanation:\nWeather risk detected due to "
        + ", ".join(reasons) + "."
        if reasons else
        "🧠 AI Explanation:\nWeather conditions are stable."
    )

    return level, explanation

# =======================
# DATA HELPERS
# =======================
def past_3_days(city):
    base = get_weather(city)
    today = datetime.now().date()
    data = []

    for i in [3, 2, 1]:
        data.append({
            "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
            "temp": round(base["temp"] - i, 1),
            "humidity": max(30, base["humidity"] - i * 2),
            "wind": round(max(1, base["wind"] - i * 0.5), 1),
            "rain": base["rain"]
        })
    return data

def next_3_days(city):
    f = get_forecast(city)
    days = {}

    for e in f:
        d = e["dt_txt"].split(" ")[0]
        days.setdefault(d, []).append(e)

    out = []
    for d, entries in list(days.items())[:3]:
        out.append({
            "date": d,
            "temp": round(sum(e["main"]["temp"] for e in entries) / len(entries), 1),
            "humidity": round(sum(e["main"]["humidity"] for e in entries) / len(entries), 1),
            "wind": round(sum(e["wind"]["speed"] for e in entries) / len(entries), 1),
            "rain": round(sum(e.get("rain", {}).get("3h", 0) for e in entries), 1)
        })
    return out

def next_24h(city):
    f = get_forecast(city)[:8]
    return [{
        "time": e["dt_txt"],
        "temp": e["main"]["temp"],
        "humidity": e["main"]["humidity"],
        "wind": e["wind"]["speed"],
        "rain": e.get("rain", {}).get("3h", 0)
    } for e in f]

# =======================
# VOICE
# =======================
def generate_voice(city, w, level):
    text = (
        f"Weather alert for {city}. "
        f"Temperature {w['temp']} degrees Celsius. "
        f"Humidity {w['humidity']} percent. "
        f"Wind speed {w['wind']} meters per second. "
        f"Alert level {level}."
    )
    file = "voice.mp3"
    gTTS(text=text, lang="en").save(file)
    return file

# =======================
# COMMANDS
# =======================
async def start(update, context):
    await update.message.reply_text("Use /weather <city>")

async def weather(update, context):
    if not context.args:
        await update.message.reply_text("❗ Usage: /weather <city>")
        return

    city = " ".join(context.args)

    keyboard = [
        [InlineKeyboardButton("🌦 Report", callback_data=f"report|{city}")],
        [InlineKeyboardButton("🔊 Voice", callback_data=f"voice|{city}")],
        [InlineKeyboardButton("📅 Past + Forecast", callback_data=f"past|{city}")],
        [InlineKeyboardButton("⏰ Next 24h", callback_data=f"hourly|{city}")],
        [
            InlineKeyboardButton("🔔 Auto Updates", callback_data=f"auto|{city}"),
            InlineKeyboardButton("🔕 Stop Updates", callback_data=f"stop|{city}")
        ],
        [InlineKeyboardButton("📋 List Subscribed Cities", callback_data="list|_")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]

    await update.message.reply_text(
        f"📍 Options for *{city.title()}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# =======================
# BUTTON HANDLER
# =======================
async def button_handler(update, context):
    q = update.callback_query
    await q.answer()

    uid = str(q.from_user.id)

    if q.data == "close":
        try:
            await q.message.delete()
        except:
            pass
        return

    action, city = q.data.split("|")

    if action == "report":
        w = get_weather(city)
        level, nlp = risk_and_nlp(w)
        await q.message.reply_text(
            f"🌦 *{city} Weather*\n\n"
            f"🌡 {w['temp']}°C\n💧 {w['humidity']}%\n"
            f"💨 {w['wind']} m/s\n🌧 {w['rain']} mm\n\n"
            f"{level}\n\n{nlp}",
            parse_mode="Markdown"
        )

    elif action == "voice":
        w = get_weather(city)
        level, _ = risk_and_nlp(w)
        v = generate_voice(city, w, level)
        await q.message.reply_voice(voice=open(v, "rb"))
        os.remove(v)

    elif action == "past":
        msg = "📅 *Past + Forecast*\n\n"
        for d in past_3_days(city) + next_3_days(city):
            msg += f"{d['date']}\n🌡{d['temp']} 💧{d['humidity']} 💨{d['wind']} 🌧{d['rain']}\n\n"
        await q.message.reply_text(msg, parse_mode="Markdown")

    elif action == "hourly":
        msg = "⏰ *Next 24 Hours*\n\n"
        for h in next_24h(city):
            msg += f"{h['time']}\n🌡{h['temp']} 💧{h['humidity']} 💨{h['wind']} 🌧{h['rain']}\n\n"
        await q.message.reply_text(msg, parse_mode="Markdown")

    elif action == "auto":
        subs = load_subs()
        subs.setdefault(uid, [])
        if city not in subs[uid]:
            subs[uid].append(city)
            save_subs(subs)
        await q.message.reply_text(f"✅ Auto updates enabled for {city}")

    elif action == "stop":
        subs = load_subs()
        if uid in subs and city in subs[uid]:
            subs[uid].remove(city)
            if not subs[uid]:
                del subs[uid]
            save_subs(subs)
            await q.message.reply_text(f"🔕 Auto updates stopped for {city}")

    elif action == "list":
        subs = load_subs()
        if uid not in subs:
            await q.message.reply_text("📭 No subscribed cities.")
            return

        msg = "📋 *Subscribed Cities*\n\n"
        for c in subs[uid]:
            msg += f"• {c.title()}\n"
        await q.message.reply_text(msg, parse_mode="Markdown")

# =======================
# AUTO LOOP
# =======================
async def auto_loop(app):
    bot = Bot(BOT_TOKEN)
    await asyncio.sleep(5)

    while True:
        subs = load_subs()
        for uid, cities in subs.items():
            for city in cities:
                try:
                    w = get_weather(city)
                    level, nlp = risk_and_nlp(w)

                    await bot.send_message(
                        chat_id=uid,
                        text=f"🌦 *Auto Update – {city}*\n"
                             f"🌡{w['temp']}°C 💧{w['humidity']}% "
                             f"💨{w['wind']} 🌧{w['rain']}\n\n"
                             f"{level}\n\n{nlp}",
                        parse_mode="Markdown"
                    )

                    if level in ["⚠️ WARNING", "🚨 EMERGENCY"]:
                        v = generate_voice(city, w, level)
                        await bot.send_voice(chat_id=uid, voice=open(v, "rb"))
                        os.remove(v)

                except Exception as e:
                    print("Auto loop error:", e)

        await asyncio.sleep(600)

# =======================
# MAIN
# =======================
async def post_init(app):
    app.create_task(auto_loop(app))

app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CallbackQueryHandler(button_handler))

print("🤖 Weather AI Agent running...")
app.run_polling()
