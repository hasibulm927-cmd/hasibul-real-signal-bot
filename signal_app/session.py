from datetime import datetime
import pytz

def get_market_session():

    india = pytz.timezone("Asia/Kolkata")

    now = datetime.now(india)

    hour = now.hour

    if 5 <= hour < 12:
        return "ASIAN SESSION"

    elif 12 <= hour < 17:
        return "LONDON SESSION"

    elif 17 <= hour < 22:
        return "NEW YORK SESSION"

    else:
        return "MARKET CLOSED"