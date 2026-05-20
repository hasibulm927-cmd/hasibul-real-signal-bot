from indicators import (
    calculate_ema,
    calculate_rsi,
    calculate_macd
)

def generate_signal(df):

    close = df["Close"]

    ema20 = calculate_ema(close, 20)

    rsi = calculate_rsi(close, 14)

    macd, signal_line = calculate_macd(close)

    latest_price = float(close.iloc[-1])

    latest_ema = float(ema20.iloc[-1])

    latest_rsi = float(rsi.iloc[-1])

    latest_macd = float(macd.iloc[-1])

    latest_signal = float(signal_line.iloc[-1])

    trend = "DOWNTREND"

    if latest_price > latest_ema:
        trend = "UPTREND"

    signal = "WAIT"

    confidence = 70

    if (
        latest_rsi < 45
        and latest_macd > latest_signal
        and trend == "UPTREND"
    ):

        signal = "BUY"

        confidence = 90

    elif (
        latest_rsi > 60
        and latest_macd < latest_signal
        and trend == "DOWNTREND"
    ):

        signal = "SELL"

        confidence = 90

    return {

        "price": round(latest_price, 5),

        "rsi": round(latest_rsi, 2),

        "ema": trend,

        "macd": round(latest_macd, 5),

        "signal_line": round(latest_signal, 5),

        "signal": signal,

        "confidence": confidence

    }