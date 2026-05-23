def candlestick_pattern(df):

    last = df.iloc[-1]

    prev = df.iloc[-2]

    # Bullish Engulfing
    if (

        prev["close"] < prev["open"]

        and last["close"] > last["open"]

        and last["close"] > prev["open"]

        and last["open"] < prev["close"]

    ):

        return "BULLISH_ENGULFING"

    # Bearish Engulfing
    elif (

        prev["close"] > prev["open"]

        and last["close"] < last["open"]

        and last["open"] > prev["close"]

        and last["close"] < prev["open"]

    ):

        return "BEARISH_ENGULFING"

    # Hammer
    elif (

        (last["close"] - last["low"]) >

        ((last["high"] - last["low"]) * 0.6)

    ):

        return "HAMMER"

    # Shooting Star
    elif (

        (last["high"] - last["close"]) >

        ((last["high"] - last["low"]) * 0.6)

    ):

        return "SHOOTING_STAR"

    return "NONE"