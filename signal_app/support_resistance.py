def support_resistance(df):

    support = df["low"].min()

    resistance = df["high"].max()

    return {

        "support": round(support, 2),

        "resistance": round(resistance, 2)

    }