import requests
import pandas as pd

API_KEY = "2ce4b507c77c48599f27e63ccb7b7de4"

def get_market_data(pair="EURUSD"):

    symbol = pair[:3] + "/" + pair[3:]

    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={symbol}"
        f"&interval=1min"
        f"&outputsize=100"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    if "values" not in data:

        raise Exception(str(data))

    candles = data["values"]

    rows = []

    for candle in candles:

        rows.append({

            "open": float(candle["open"]),

            "high": float(candle["high"]),

            "low": float(candle["low"]),

            "close": float(candle["close"])

        })

    df = pd.DataFrame(rows)

    df = df.iloc[::-1].reset_index(drop=True)

    return df