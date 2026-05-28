from indicators import calculate_indicators
from patterns import candlestick_pattern
from strength import candle_strength
from trend_strength import trend_strength

from datetime import datetime, timedelta

import pytz


# =====================================
# WILLIAMS %R
# =====================================

def williams_r(df, period=14):

    highest_high = df["high"].rolling(period).max()

    lowest_low = df["low"].rolling(period).min()

    wr = (

        (highest_high - df["close"])

        / (highest_high - lowest_low)

    ) * -100

    return float(wr.iloc[-1])


# =====================================
# MOVING AVERAGE
# =====================================

def moving_average(df, period=50):

    ma = df["close"].rolling(period).mean()

    return float(ma.iloc[-1])


# =====================================
# MAIN SIGNAL FUNCTION
# =====================================

def generate_signal(df):

    # =====================================
    # INDIAN TIME
    # =====================================

    india = pytz.timezone("Asia/Kolkata")

    now = datetime.now(india)

    entry_time = now.strftime("%H:%M:%S")

    # =====================================
    # CURRENT PRICE
    # =====================================

    current_price = float(

        df["close"].iloc[-1]

    )

    # =====================================
    # LIVE COUNTDOWN
    # =====================================

    seconds_left = 60 - now.second

    countdown = f"00:{seconds_left:02d}"

    # =====================================
    # ENTRY ZONE
    # =====================================

    if seconds_left >= 35:

        entry_zone = "SAFE ENTRY"

        zone_color = "GREEN"

    elif seconds_left >= 20:

        entry_zone = "RISKY ENTRY"

        zone_color = "YELLOW"

    else:

        entry_zone = "NO ENTRY"

        zone_color = "RED"

    # =====================================
    # INDICATORS
    # =====================================

    indicators = calculate_indicators(df)

    rsi = float(indicators["rsi"])

    ema10 = float(indicators["ema10"])

    ema20 = float(indicators["ema20"])

    # =====================================
    # WILLIAMS %R
    # =====================================

    wr = williams_r(df)

    # =====================================
    # MOVING AVERAGE
    # =====================================

    ma50 = moving_average(df)

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

    ema_gap = abs(

        ema10 - ema20

    )

    # =====================================
    # DEFAULT VALUES
    # =====================================

    signal = "WAIT"

    confidence = 50

    expiry = "WAIT"

    expiry_time = "--"

    entry_status = "WAIT"

    # =====================================
    # LAST MOMENT ENTRY BLOCK
    # =====================================

    if seconds_left <= 20:

        return {

            "price": round(current_price, 5),

            "signal": "WAIT",

            "confidence": 50,

            "entry_status": "WAIT NEXT CANDLE",

            "entry_time": entry_time,

            "expiry": "WAIT",

            "expiry_time": "--",

            "countdown": countdown,

            "entry_zone": entry_zone,

            "zone_color": zone_color,

            "rsi": round(rsi, 2),

            "wr": round(wr, 2),

            "ma50": round(ma50, 5),

            "ema10": round(ema10, 5),

            "ema20": round(ema20, 5),

            "ema_gap": round(ema_gap, 5),

            "pattern": pattern,

            "strength": round(strength, 2),

            "trend": trend

        }

    # =====================================
    # HIGH QUALITY BUY LOGIC
    # =====================================

    if (

        trend == "STRONG"

        and ema10 > ema20

        and current_price > ma50

        and ema_gap > 0.00030

        and rsi > 58

        and wr > -20

        and strength >= 75

        and pattern in [

            "BULLISH_ENGULFING",

            "HAMMER"

        ]

    ):

        signal = "UP"

        confidence = 88

        entry_status = "ENTER NOW"

        # =====================================
        # ULTRA STRONG BUY
        # =====================================

        if (

            rsi >= 65

            and strength >= 85

            and ema_gap > 0.00050

            and wr > -10

        ):

            confidence = 95

            expiry = "2 MIN"

        else:

            expiry = "3 MIN"

    # =====================================
    # HIGH QUALITY SELL LOGIC
    # =====================================

    elif (

        trend == "STRONG"

        and ema10 < ema20

        and current_price < ma50

        and ema_gap > 0.00030

        and rsi < 42

        and wr < -80

        and strength >= 75

        and pattern in [

            "BEARISH_ENGULFING",

            "SHOOTING_STAR"

        ]

    ):

        signal = "DOWN"

        confidence = 88

        entry_status = "ENTER NOW"

        # =====================================
        # ULTRA STRONG SELL
        # =====================================

        if (

            rsi <= 35

            and strength >= 85

            and ema_gap > 0.00050

            and wr < -90

        ):

            confidence = 95

            expiry = "2 MIN"

        else:

            expiry = "3 MIN"

    # =====================================
    # NO CLEAR TREND
    # =====================================

    else:

        signal = "WAIT"

        confidence = 50

        expiry = "WAIT"

        entry_status = "NO CLEAR TREND"

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

    # =====================================
    # SIGNAL QUALITY BAR
    # =====================================

    if confidence >= 95:

        quality = "██████████"

    elif confidence >= 88:

        quality = "████████"

    elif confidence >= 70:

        quality = "██████"

    else:

        quality = "████"

    # =====================================
    # MARKET DIRECTION
    # =====================================

    if ema10 > ema20:

        market_direction = "BULLISH"

    elif ema10 < ema20:

        market_direction = "BEARISH"

    else:

        market_direction = "SIDEWAYS"

    # =====================================
    # FINAL RESULT
    # =====================================

    return {

        "price": round(current_price, 5),

        "signal": signal,

        "confidence": confidence,

        "signal_quality": quality,

        "entry_status": entry_status,

        "entry_time": entry_time,

        "expiry": expiry,

        "expiry_time": expiry_time,

        "countdown": countdown,

        "entry_zone": entry_zone,

        "zone_color": zone_color,

        "market_direction": market_direction,

        "rsi": round(rsi, 2),

        "wr": round(wr, 2),

        "ma50": round(ma50, 5),

        "ema10": round(ema10, 5),

        "ema20": round(ema20, 5),

        "ema_gap": round(ema_gap, 5),

        "pattern": pattern,

        "strength": round(strength, 2),

        "trend": trend

    }