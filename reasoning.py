def analyze_weather(w):
    risk = 0
    reasons = []

    if w["temp"] >= 42:
        risk += 2
        reasons.append("Extreme heat")

    if w["rain"] >= 20:
        risk += 2
        reasons.append("Heavy rainfall")

    if w["wind"] >= 15:
        risk += 1
        reasons.append("Strong winds")

    if w["humidity"] >= 90:
        risk += 1
        reasons.append("Very high humidity")

    return risk, reasons
