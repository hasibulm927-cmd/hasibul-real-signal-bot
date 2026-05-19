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

    for pair, symbol in pairs.items():

        try:
            df = yf.download(
                symbol,
                period="1d",
                interval="1m",
                progress=False
            )

            price = round(float(df["Close"].iloc[-1]), 5)

        except:
            price = 0

        signal_type = random.choice([
            "BUY SIGNAL",
            "SELL SIGNAL"
        ])

        confidence = random.randint(85, 99)

        data.append({
            "pair": pair,
            "price": price,
            "signal": signal_type,
            "confidence": confidence
        })

    return jsonify(data)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )