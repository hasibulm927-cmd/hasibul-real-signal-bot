import pandas as pd

def calculate_ema(series, period=20):

    return series.ewm(span=period).mean()

def calculate_rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_macd(series):

    ema12 = series.ewm(span=12).mean()
    ema26 = series.ewm(span=26).mean()

    macd = ema12 - ema26

    signal = macd.ewm(span=9).mean()

    return macd, signal