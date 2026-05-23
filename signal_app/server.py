from flask import Flask
from flask_cors import CORS

from market import get_market_data
from signal_logic import generate_signal

from datetime import datetime

import os

app = Flask(__name__)

CORS(app)

# =========================
# BEST 5 FOREX PAIRS
# =========================

pairs = [

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "EURJPY"

]

# =========================
# CHART SYMBOL MAP
# =========================

chart_symbols = {

    "EURUSD": "FX:EURUSD",
    "GBPUSD": "FX:GBPUSD",
    "USDJPY": "FX:USDJPY",
    "AUDUSD": "FX:AUDUSD",
    "EURJPY": "FX:EURJPY"

}

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    current_time = datetime.now().strftime("%I:%M:%S %p")

    signal_cards = ""

    chart_boxes = ""

    # =========================
    # SIGNAL CARDS
    # =========================

    for pair in pairs:

        try:

            # LIVE MARKET DATA
            df = get_market_data(pair)

            # SIGNAL LOGIC
            data = generate_signal(df)

            # SIGNAL COLOR
            signal_color = "#ffd700"

            if data["signal"] == "UP":

                signal_color = "#00ff99"

            elif data["signal"] == "DOWN":

                signal_color = "#ff4d4d"

            # =========================
            # SIGNAL CARD
            # =========================

            signal_cards += f"""

            <div class="card">

                <h2>{pair}</h2>

                <div class="signal"
                style="color:{signal_color};">

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

                <p>🕒 EXPIRY TIME : {data['expiry_time']}</p>

            </div>

            """

            # =========================
            # MULTI LIVE CHART
            # =========================

            chart_boxes += f"""

            <div class="chart-card">

                <h2>📈 {pair} LIVE CHART</h2>

                <iframe
                src="https://s.tradingview.com/widgetembed/?symbol={chart_symbols[pair]}&interval=1&theme=dark&hidesidetoolbar=1"
                width="100%"
                height="400"
                frameborder="0">
                </iframe>

            </div>

            """

        except Exception as e:

            signal_cards += f"""

            <div class="card">

                <h2>{pair}</h2>

                <p style="color:red; font-size:22px;">

                    API ERROR

                </p>

            </div>

            """

    # =========================
    # FULL HTML
    # =========================

    html = f"""

    <html>

    <head>

        <title>HASIBUL LIVE SIGNAL BOT</title>

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
                box-shadow: 0px 0px 15px black;

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
                box-shadow: 0px 0px 10px black;

            }}

            .grid {{

                display: grid;
                grid-template-columns:
                repeat(auto-fit,minmax(320px,1fr));
                gap: 20px;

            }}

            .card {{

                background: #111827;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 0px 15px black;
                transition: 0.3s;
                border: 2px solid #1e293b;

            }}

            .card:hover {{

                transform: scale(1.02);
                border: 2px solid #00ff99;

            }}

            .card h2 {{

                color: #00ff99;
                margin-bottom: 15px;
                font-size: 30px;
                text-align: center;

            }}

            .signal {{

                font-size: 45px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;

            }}

            p {{

                font-size: 18px;
                line-height: 34px;
                background: #1e293b;
                padding: 8px;
                border-radius: 8px;

            }}

            .chart-section {{

                margin-top: 40px;

            }}

            .chart-grid {{

                display:grid;
                grid-template-columns:
                repeat(auto-fit,minmax(500px,1fr));
                gap:25px;

            }}

            .chart-card {{

                background:#111827;
                padding:20px;
                border-radius:15px;
                box-shadow:0px 0px 15px black;

            }}

            .chart-card h2 {{

                color:#00ff99;
                text-align:center;
                margin-bottom:15px;

            }}

            iframe {{

                border-radius:10px;

            }}

        </style>

    </head>

    <body>

        <div class="topbar" id="clock">

            🚀 HASIBUL LIVE SIGNAL BOT

            <br><br>

            ⏰ LIVE CLOCK : {current_time}

        </div>

        <div class="timer" id="refreshTimer">

            NEXT REFRESH IN : 60

        </div>

        <div class="timer" id="candleTimer">

            CANDLE CLOSE IN : 00:59

        </div>

        <!-- SIGNALS -->

        <div class="grid">

            {signal_cards}

        </div>

        <!-- MULTI LIVE CHART -->

        <div class="chart-section">

            <div class="topbar">

                📊 MULTI LIVE FOREX CHART

            </div>

            <div class="chart-grid">

                {chart_boxes}

            </div>

        </div>

        <script>

            // =========================
            // AUTO REFRESH TIMER
            // =========================

            let seconds = 60;

            setInterval(() => {{

                seconds--;

                if(seconds <= 0) {{

                    seconds = 60;

                    location.reload();

                }}

                document.getElementById("refreshTimer")
                .innerHTML =

                "NEXT REFRESH IN : " + seconds;

            }},1000);

            // =========================
            // LIVE CLOCK
            // =========================

            setInterval(() => {{

                const now = new Date();

                const time = now.toLocaleTimeString();

                document.getElementById("clock")
                .innerHTML =

                "🚀 HASIBUL LIVE SIGNAL BOT" +

                "<br><br>" +

                "⏰ LIVE CLOCK : " + time;

            }},1000);

            // =========================
            // REAL MARKET CANDLE TIMER
            // =========================

            setInterval(() => {{

                const now = new Date();

                const sec = now.getSeconds();

                const remaining = 60 - sec;

                document.getElementById("candleTimer")
                .innerHTML =

                "CANDLE CLOSE IN : 00:" +

                String(remaining).padStart(2,'0');

            }},1000);

        </script>

    </body>

    </html>

    """

    return html


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(

        host="0.0.0.0",
        port=port,
        debug=True

    )