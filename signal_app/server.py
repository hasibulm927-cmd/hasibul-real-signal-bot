from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import random
import os

app = Flask(__name__)
CORS(app)

pairs = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "USDJPY=X"
}

@app.route("/")
def home():
    return "HASIBUL SIGNAL BOT RUNNING"

@app.route("/signal")
def signal():

    data = []

    for pair_name, pair_symbol in pairs.items():

        try:

            df = yf.download(
                pair_symbol,
                period="1d",
                interval="5m",
                progress=False
            )

            close_price = round(
                float(df["Close"].iloc[-1]),
                5
            )

            previous_price = round(
                float(df["Close"].iloc[-2]),
                5
            )

            if close_price > previous_price:
                signal = "BUY SIGNAL"

            elif close_price < previous_price:
                signal = "SELL SIGNAL"

            else:
                signal = "WAIT SIGNAL"

        except Exception as e:

            close_price = 0
            signal = "WAIT SIGNAL"

        data.append({

            "pair": pair_name,
            "price": close_price,
            "signal": signal

        })

    return jsonify(data)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )