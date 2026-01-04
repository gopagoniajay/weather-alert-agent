from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(TELEGRAM_BOT_TOKEN)

def send_alert(level, city, reasons, weather):
    message = f"""
🌦️ Weather Alert: {level}
📍 Location: {city}

🌡️ Temperature: {weather['temp']}°C
💨 Wind Speed: {weather['wind']} m/s
🌧️ Rainfall: {weather['rain']} mm
💧 Humidity: {weather['humidity']}%

⚠️ Reasons:
- {', '.join(reasons)}

📝 Advisory:
Please stay alert and follow local safety instructions.
"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
