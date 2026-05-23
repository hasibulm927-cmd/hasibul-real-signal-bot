from datetime import datetime

def news_time_filter():

    minute = datetime.utcnow().minute

    if minute in [28, 29, 30, 58, 59, 0]:

        return True

    return False