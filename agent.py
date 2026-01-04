import time
from weather_api import get_weather
from reasoning import analyze_weather
from alert_engine import decide_alert
from notifier import send_alert
from config import CITY

def run_agent():
    weather = get_weather(CITY)
    risk, reasons = analyze_weather(weather)
    alert_level = decide_alert(risk)

    if alert_level != "NORMAL":
        send_alert(alert_level, CITY, reasons, weather)

    print(f"[Agent] {CITY} → {alert_level}")

while True:
    run_agent()
    time.sleep(300)  # runs every 5 minutes
