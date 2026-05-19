from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import random
import os

app = Flask(__name__)
CORS(app)

pairs = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X"
]

@app.route("/")
def home():
    return "HASIBUL SIGNAL BOT RUNNING"

@app.route("/signal")
def signal():

    data = []

    for pair in pairs:

        try:

            df = yf.download(
                pair,
                period="1d",
                interval="5m",
                progress=False
            )

            price = round(float(df["Close"].iloc[-1]), 5)

        except:

            price = 0

        signal = random.choice([
            "BUY SIGNAL",
            "SELL SIGNAL",
            "WAIT SIGNAL"
        ])

        data.append({
            "pair": pair,
            "price": price,
            "signal": signal
        })

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)