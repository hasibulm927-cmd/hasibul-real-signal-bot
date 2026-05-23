from datetime import datetime

def candle_countdown():

    now = datetime.utcnow()

    seconds = now.second

    remaining = 60 - seconds

    return remaining