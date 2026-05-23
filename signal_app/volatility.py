def market_volatility(df):

    latest = df.iloc[-1]

    movement = latest["high"] - latest["low"]

    if movement > 1:

        return "HIGH"

    else:

        return "LOW"