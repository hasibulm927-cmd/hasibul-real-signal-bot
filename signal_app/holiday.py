from datetime import datetime

def market_holiday():

    day = datetime.utcnow().weekday()

    if day == 5 or day == 6:

        return True

    return False