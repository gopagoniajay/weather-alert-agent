def decide_alert(risk):
    if risk >= 4:
        return "EMERGENCY"
    elif risk >= 2:
        return "WARNING"
    elif risk == 1:
        return "WATCH"
    else:
        return "NORMAL"
