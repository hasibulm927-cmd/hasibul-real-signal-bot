from indicators import calculate_indicators
from patterns import candlestick_pattern
from strength import candle_strength
from trend_strength import trend_strength

from datetime import datetime, timedelta


def generate_signal(df):

    # =====================================
    # CURRENT PRICE
    # =====================================

    current_price = float(df["close"].iloc[-1])

    # =====================================
    # TIME
    # =====================================

    now = datetime.now()

    entry_time = now.strftime("%H:%M:%S")

    # =====================================
    # INDICATORS
    # =====================================

    indicators = calculate_indicators(df)

    rsi = float(indicators["rsi"])

    ema10 = float(indicators["ema10"])

    ema20 = float(indicators["ema20"])

    # =====================================
    # PATTERN
    # =====================================

    pattern = candlestick_pattern(df)

    # =====================================
    # STRENGTH
    # =====================================

    strength = candle_strength(df)

    # =====================================
    # TREND
    # =====================================

    trend = trend_strength(df)

    # =====================================
    # EMA GAP
    # =====================================

    ema_gap = abs(ema10 - ema20)

    # =====================================
    # DEFAULT VALUES
    # =====================================

    signal = "WAIT"

    confidence = 50

    expiry = "5 MIN"

    entry_status = "WAIT NEXT CANDLE"

    # =====================================
    # STRONG BUY LOGIC
    # =====================================

    if (

        ema10 > ema20

        and rsi > 50

        and ema_gap > 0.00010

        and pattern in [

            "BULLISH_ENGULFING",
            "HAMMER"

        ]

        and strength >= 60

    ):

        signal = "UP"

        confidence = 78

        entry_status = "ENTER NOW"

        # =====================================
        # SUPER STRONG BUY
        # =====================================

        if (

            strength >= 80

            and trend == "STRONG"

            and rsi > 60

        ):

            confidence = 90

        # =====================================
        # DYNAMIC EXPIRY
        # =====================================

        if strength >= 90:

            expiry = "2 MIN"

        elif strength >= 80:

            expiry = "3 MIN"

        else:

            expiry = "5 MIN"

    # =====================================
    # STRONG SELL LOGIC
    # =====================================

    elif (

        ema10 < ema20

        and rsi < 50

        and ema_gap > 0.00010

        and pattern in [

            "BEARISH_ENGULFING",
            "SHOOTING_STAR"

        ]

        and strength >= 60

    ):

        signal = "DOWN"

        confidence = 78

        entry_status = "ENTER NOW"

        # =====================================
        # SUPER STRONG SELL
        # =====================================

        if (

            strength >= 80

            and trend == "STRONG"

            and rsi < 40

        ):

            confidence = 90

        # =====================================
        # DYNAMIC EXPIRY
        # =====================================

        if strength >= 90:

            expiry = "2 MIN"

        elif strength >= 80:

            expiry = "3 MIN"

        else:

            expiry = "5 MIN"

    # =====================================
    # MEDIUM MARKET
    # =====================================

    elif (

        trend == "MEDIUM"

        and strength >= 55

    ):

        signal = "WAIT"

        confidence = 65

        expiry = "5 MIN"

    # =====================================
    # WEAK MARKET
    # =====================================

    else:

        signal = "WAIT"

        confidence = 50

        expiry = "5 MIN"

    # =====================================
    # REAL CANDLE COUNTDOWN
    # =====================================

    seconds_left = 60 - now.second

    countdown = f"00:{seconds_left:02d}"

    # =====================================
    # ENTRY FILTER
    # =====================================

    if seconds_left <= 8:

        entry_status = "WAIT NEXT CANDLE"

    # =====================================
    # EXPIRY TIME
    # =====================================

    if expiry == "2 MIN":

        expiry_time = (

            now + timedelta(minutes=2)

        ).strftime("%H:%M:%S")

    elif expiry == "3 MIN":

        expiry_time = (

            now + timedelta(minutes=3)

        ).strftime("%H:%M:%S")

    else:

        expiry_time = (

            now + timedelta(minutes=5)

        ).strftime("%H:%M:%S")

    # =====================================
    # FINAL RESULT
    # =====================================

    return {

        "price": round(current_price, 5),

        "signal": signal,

        "confidence": confidence,

        "entry_status": entry_status,

        "entry_time": entry_time,

        "expiry": expiry,

        "expiry_time": expiry_time,

        "countdown": countdown,

        "rsi": round(rsi, 2),

        "ema10": round(ema10, 5),

        "ema20": round(ema20, 5),

        "ema_gap": round(ema_gap, 5),

        "pattern": pattern,

        "strength": round(strength, 2),

        "trend": trend

    }