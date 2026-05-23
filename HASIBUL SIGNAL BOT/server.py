from flask import Flask
from flask_cors import CORS

from market import get_market_data
from signal_logic import generate_signal

from datetime import datetime

import os

app = Flask(__name__)

CORS(app)

pairs = [

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD"

]

@app.route("/")
def home():

    current_time = datetime.now().strftime("%I:%M:%S %p")

    signal_cards = ""

    for pair in pairs:

        try:

            df = get_market_data(pair)

            data = generate_signal(df)

            signal_color = "#00ff99"

            if data["signal"] == "DOWN":

                signal_color = "#ff4d4d"

            elif data["signal"] == "WAIT":

                signal_color = "#ffd700"

            signal_cards += f"""

            <div class="card">

                <h2>{pair}</h2>

                <div class="signal" style="color:{signal_color};">

                    {data['signal']}
                </div>

                <p>💰 PRICE : {data['price']}</p>

                <p>📊 RSI : {data['rsi']}</p>

                <p>⚡ STRENGTH : {data['strength']}</p>

                <p>📈 TREND : {data['trend']}</p>

                <p>🕯️ PATTERN : {data['pattern']}</p>

                <p>🎯 CONFIDENCE : {data['confidence']}%</p>

                <p>⏳ COUNTDOWN : {data['countdown']}</p>

                <p>⏰ ENTRY : {data['entry_status']}</p>

                <p>⌛ EXPIRY : {data['expiry']}</p>

            </div>

            """

        except Exception as e:

            signal_cards += f"""

            <div class="card">

                <h2>{pair}</h2>

                <p style="color:red;">

                    API ERROR
                </p>

            </div>

            """

    html = f"""

    <html>

    <head>

        <title>HASIBUL LIVE SIGNAL BOT</title>

        <meta http-equiv="refresh" content="60">

        <style>

            body {{

                background: #0f172a;

                color: white;

                font-family: Arial;

                padding: 20px;

            }}

            .topbar {{

                background: #111827;

                padding: 20px;

                border-radius: 15px;

                text-align: center;

                color: #00ff99;

                font-size: 30px;

                font-weight: bold;

                margin-bottom: 20px;

            }}

            .timer {{

                background: #1e293b;

                padding: 15px;

                border-radius: 12px;

                text-align: center;

                font-size: 24px;

                color: yellow;

                margin-bottom: 20px;

                font-weight: bold;

            }}

            .grid {{

                display: grid;

                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));

                gap: 20px;

            }}

            .card {{

                background: #111827;

                padding: 20px;

                border-radius: 15px;

                box-shadow: 0px 0px 15px black;

            }}

            .card h2 {{

                color: #00ff99;

                margin-bottom: 15px;

            }}

            .signal {{

                font-size: 38px;

                font-weight: bold;

                margin-bottom: 15px;

            }}

            p {{

                font-size: 18px;

                line-height: 30px;

            }}

        </style>

    </head>

    <body>

        <div class="topbar">

            🚀 HASIBUL LIVE SIGNAL BOT

            <br><br>

            ⏰ LIVE CLOCK : {current_time}

        </div>

        <div class="timer" id="timer">

            NEXT REFRESH IN : 60
        </div>

        <div class="grid">

            {signal_cards}

        </div>

        <script>

            let seconds = 60;

            setInterval(() => {{

                seconds--;

                document.getElementById("timer").innerHTML =

                    "NEXT REFRESH IN : " + seconds;

                if(seconds <= 0) {{

                    location.reload();

                }}

            }}, 1000);

        </script>

    </body>

    </html>

    """

    return html


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(

        host="0.0.0.0",
        port=port,
        debug=True

    )