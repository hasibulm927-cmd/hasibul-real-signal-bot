import yfinance as yf

pairs = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "USDJPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "USDCAD=X",
    "EURJPY": "EURJPY=X",
    "GBPJPY": "GBPJPY=X",
    "EURGBP": "EURGBP=X",
    "USDCHF": "USDCHF=X",
    "NZDUSD": "NZDUSD=X"
}

def get_market_data(pair):

    symbol = pairs.get(pair)

    df = yf.download(
        symbol,
        period="2d",
        interval="1m",
        progress=False
    )

    df.dropna(inplace=True)

    return df