from flask import Flask, jsonify
from flask_cors import CORS

from market import get_market_data
from signals import generate_signal

import os

app = Flask(__name__)

CORS(app)

pairs = [

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "EURJPY",
    "GBPJPY",
    "EURGBP",
    "NZDUSD",
    "USDCHF"

]

@app.route("/")

def home():

    return "HASIBUL REAL SIGNAL BOT RUNNING"

@app.route("/signal/<pair>")

def signal(pair):

    pair = pair.upper()

    if pair not in pairs:

        return jsonify({

            "error": "INVALID PAIR"

        })

    try:

        df = get_market_data(pair)

        result = generate_signal(df)

        result["pair"] = pair

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "error": str(e)

        })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )