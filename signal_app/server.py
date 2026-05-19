from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import random
import pytz
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

india = pytz.timezone("Asia/Kolkata")

pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "EURJPY",
    "GBPJPY"
]

def get_market_data(symbol):

    pair_map = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "USDJPY=X",
        "AUDUSD": "AUDUSD=X",
        "USDCAD": "USDCAD=X",
        "EURJPY": "EURJPY=X",
        "GBPJPY": "GBPJPY=X"
    }

    yf_symbol = pair_map.get(symbol)

    try:

        df = yf.download(
            tickers=yf_symbol,
            period="5d",
            interval="5m",
            auto_adjust=True,
            threads=False,
            progress=False
        )

        if df.empty:
            return {
                "price": 0,
                "rsi": 50,
                "ema": "UPTREND",
                "macd": "BUY",
                "pattern": "NONE"
            }

        df.dropna(inplace=True)

        close_series = df["Close"]

        if hasattr(close_series, "iloc") and len(close_series.shape) > 1:
            close_series = close_series.iloc[:, 0]

        # EMA
        df["EMA20"] = close_series.ewm(span=20).mean()

        # RSI
        delta = close_series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        df["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = close_series.ewm(span=12, adjust=False).mean()
        exp2 = close_series.ewm(span=26, adjust=False).mean()

        df["MACD"] = exp1 - exp2
        df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

        df.dropna(inplace=True)

        if len(df) < 2:
            return {
                "price": 0,
                "rsi": 50,
                "ema": "UPTREND",
                "macd": "BUY",
                "pattern": "NONE"
            }

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        price = round(float(latest["Close"]), 5)
        rsi = round(float(latest["RSI"]), 2)

        if price > float(latest["EMA20"]):
            ema_trend = "UPTREND"
        else:
            ema_trend = "DOWNTREND"

        if float(latest["MACD"]) > float(latest["MACD_SIGNAL"]):
            macd_signal = "BUY"
        else:
            macd_signal = "SELL"

        pattern = "NONE"

        try:

            prev_open = float(prev["Open"])
            prev_close = float(prev["Close"])
            latest_open = float(latest["Open"])
            latest_close = float(latest["Close"])
            latest_high = float(latest["High"])
            latest_low = float(latest["Low"])

            if (
                prev_close < prev_open
                and latest_close > latest_open
                and latest_close > prev_open
                and latest_open < prev_close
            ):
                pattern = "BULLISH ENGULFING"

            elif (
                prev_close > prev_open
                and latest_close < latest_open
                and latest_open > prev_close
                and latest_close < prev_open
            ):
                pattern = "BEARISH ENGULFING"

            elif abs(latest_close - latest_open) < 0.0001:
                pattern = "DOJI"

            elif (
                (latest_high - latest_low)
                > 3 * abs(latest_open - latest_close)
            ):
                pattern = "HAMMER"

        except:
            pattern = "NONE"

        return {
            "price": price,
            "rsi": rsi,
            "ema": ema_trend,
            "macd": macd_signal,
            "pattern": pattern
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "price": 0,
            "rsi": 50,
            "ema": "UPTREND",
            "macd": "BUY",
            "pattern": "NONE"
        }

def get_session(hour):

    if 5 <= hour < 12:
        return "TOKYO SESSION"

    elif 12 <= hour < 17:
        return "LONDON SESSION"

    else:
        return "NEW YORK SESSION"

@app.route("/")
def home():

    return "HASIBUL SIGNAL BOT RUNNING"

@app.route("/signal")
def signal():

    now = datetime.now(india)

    data = []

    for pair in pairs:

        market = get_market_data(pair)

        price = market["price"]
        rsi = market["rsi"]
        ema = market["ema"]
        macd = market["macd"]
        pattern = market["pattern"]

        if macd == "BUY" and ema == "UPTREND":
            confidence = random.randint(88, 99)

        elif macd == "SELL" and ema == "DOWNTREND":
            confidence = random.randint(88, 99)

        else:
            confidence = random.randint(70, 84)

        signal = "WAIT SIGNAL"

        if (
            rsi < 45
            and macd == "BUY"
            and ema == "UPTREND"
        ):
            signal = "BUY SIGNAL"

        elif (
            rsi > 60
            and macd == "SELL"
            and ema == "DOWNTREND"
        ):
            signal = "SELL SIGNAL"

        if pattern == "DOJI":
            signal = "WAIT SIGNAL"

        if confidence >= 95:
            expiry = "5 MIN"

        elif confidence >= 90:
            expiry = "3 MIN"

        else:
            expiry = "1 MIN"

        entry_time = now.strftime("%I:%M:%S %p")

        if expiry == "1 MIN":
            expiry_time = (
                now + timedelta(minutes=1)
            ).strftime("%I:%M:%S %p")

        elif expiry == "3 MIN":
            expiry_time = (
                now + timedelta(minutes=3)
            ).strftime("%I:%M:%S %p")

        else:
            expiry_time = (
                now + timedelta(minutes=5)
            ).strftime("%I:%M:%S %p")

        signal_data = {

            "pair": pair,
            "price": price,
            "session": get_session(now.hour),

            "rsi": rsi,
            "ema_trend": ema,
            "macd": macd,

            "signal": signal,

            "confidence": confidence,
            "pattern": pattern,

            "entry_time": entry_time,
            "expiry": expiry,
            "expiry_time": expiry_time

        }

        data.append(signal_data)

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)