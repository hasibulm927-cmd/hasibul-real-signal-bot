def candle_strength(df):

    last = df.iloc[-1]

    body = abs(last["close"] - last["open"])

    full_range = last["high"] - last["low"]

    if full_range == 0:

        return 0

    strength = (body / full_range) * 100

    return round(strength, 2)