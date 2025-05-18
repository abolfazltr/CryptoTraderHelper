import pandas as pd
import requests
import pandas_ta as ta

def fetch_ohlcv(symbol="ETHUSDT", interval="5m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "_", "_", "_", "_", "_", "_"
    ])
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    return df

def generate_signal():
    df = fetch_ohlcv("ETHUSDT", "5m")

    # محاسبه SuperTrend با تنظیمات 2, 3, 10
    st = ta.supertrend(df["high"], df["low"], df["close"], length=10, multiplier=3)
    df = pd.concat([df, st], axis=1)

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # سیگنال Long: وقتی close بالای Supertrend بشه و trend تغییر کنه
    if prev["SUPERT_10_3.0"] > prev["close"] and latest["SUPERT_10_3.0"] < latest["close"]:
        return "long"

    # سیگنال Short: وقتی close زیر Supertrend بره و trend تغییر کنه
    if prev["SUPERT_10_3.0"] < prev["close"] and latest["SUPERT_10_3.0"] > latest["close"]:
        return "short"

    return None