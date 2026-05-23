def trend_strength(df):

    ema10 = df["close"].ewm(span=10).mean().iloc[-1]

    ema20 = df["close"].ewm(span=20).mean().iloc[-1]

    distance = abs(ema10 - ema20)

    if distance > 0.0030:
        return "STRONG"

    elif distance > 0.0015:
        return "MEDIUM"

    else:
        return "WEAK"