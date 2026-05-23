import pandas as pd

def calculate_indicators(df):

    close_prices = df["close"]

    # RSI

    delta = close_prices.diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()

    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    # EMA

    ema_10 = close_prices.ewm(span=10).mean()

    ema_20 = close_prices.ewm(span=20).mean()

    return {

        "rsi": rsi.iloc[-1],

        "ema10": ema_10.iloc[-1],

        "ema20": ema_20.iloc[-1]

    }