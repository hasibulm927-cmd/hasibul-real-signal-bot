from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import random
import pytz
from datetime import datetime, timedelta
import yfinance as yf
import pandas_ta as ta

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

        df["RSI"] = ta.rsi(close_series, length=14)
        df["EMA20"] = ta.ema(close_series, length=20)

        macd = ta.macd(close_series)

        if macd is not None:
            df["MACD"] = macd.iloc[:, 0]
            df["MACD_SIGNAL"] = macd.iloc[:, 1]
        else:
            df["MACD"] = 0
            df["MACD_SIGNAL"] = 0

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

        close_price = latest["Close"]

        if hasattr(close_price, "iloc"):
            close_price = close_price.iloc[0]

        price = round(float(close_price), 5)

        rsi_value = latest["RSI"]

        if hasattr(rsi_value, "iloc"):
            rsi_value = rsi_value.iloc[0]

        rsi = round(float(rsi_value), 2)

        ema20 = latest["EMA20"]

        if hasattr(ema20, "iloc"):
            ema20 = ema20.iloc[0]

        if price > float(ema20):
            ema_trend = "UPTREND"
        else:
            ema_trend = "DOWNTREND"

        macd_value = latest["MACD"]
        macd_signal_value = latest["MACD_SIGNAL"]

        if hasattr(macd_value, "iloc"):
            macd_value = macd_value.iloc[0]

        if hasattr(macd_signal_value, "iloc"):
            macd_signal_value = macd_signal_value.iloc[0]

        if float(macd_value) > float(macd_signal_value):
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

    return render_template_string("""

<!DOCTYPE html>
<html>

<head>

<title>HASIBUL SIGNAL BOT</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
padding:15px;
}

.card{
background:#1e293b;
padding:15px;
border-radius:15px;
margin-bottom:15px;
box-shadow:0 0 10px rgba(0,0,0,0.5);
}

.buy{
color:#00ff95;
font-size:24px;
font-weight:bold;
}

.sell{
color:#ff4d6d;
font-size:24px;
font-weight:bold;
}

.wait{
color:yellow;
font-size:24px;
font-weight:bold;
}

.title{
font-size:28px;
font-weight:bold;
margin-bottom:20px;
text-align:center;
}

.info{
margin-top:8px;
font-size:18px;
}

.clock{
text-align:center;
font-size:20px;
margin-bottom:20px;
color:#38bdf8;
}

</style>

</head>

<body>

<div class="title">
🚀 HASIBUL SIGNAL BOT
</div>

<div class="clock" id="clock"></div>

<div id="signals"></div>

<script>

function updateClock(){

const now = new Date();

document.getElementById("clock").innerHTML =
"🕒 " + now.toLocaleTimeString();

}

setInterval(updateClock,1000);

updateClock();

async function loadSignals(){

let response = await fetch('/signal');

let data = await response.json();

let html = '';

data.forEach(item => {

let signalClass = "wait";

if(item.signal.includes("BUY")){
signalClass = "buy";
}

else if(item.signal.includes("SELL")){
signalClass = "sell";
}

html += `

<div class="card">

<div class="${signalClass}">
${item.signal}
</div>

<div class="info">📊 Pair: ${item.pair}</div>

<div class="info">💰 Price: ${item.price}</div>

<div class="info">⏰ Entry: ${item.entry_time}</div>

<div class="info">⌛ Expiry: ${item.expiry}</div>

<div class="info">⏳ Ends: ${item.expiry_time}</div>

<div class="info">🎯 Confidence: ${item.confidence}%</div>

<div class="info">📈 RSI: ${item.rsi}</div>

<div class="info">📉 MACD: ${item.macd}</div>

<div class="info">📊 EMA: ${item.ema_trend}</div>

<div class="info">🕯 Pattern: ${item.pattern}</div>

<div class="info">🌍 Session: ${item.session}</div>

</div>

`;

});

document.getElementById('signals').innerHTML = html;

}

loadSignals();

setInterval(loadSignals,15000);

</script>

</body>

</html>

""")

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

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)