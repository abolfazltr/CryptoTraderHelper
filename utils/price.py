import requests
import pandas as pd
from datetime import datetime, timedelta

def get_ohlcv(symbol="ethereum", interval="5m", limit=100):
    try:
        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - (limit * 5 * 60)

        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range"
        params = {
            "vs_currency": "usd",
            "from": start_time,
            "to": end_time
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print("Coingecko API error:", response.text)
            return None

        data = response.json()
        prices = data.get("prices", [])
        if not prices:
            print("Empty OHLCV from Coingecko")
            return None

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["close"].shift(1)
        df["high"] = df["close"]
        df["low"] = df["close"]
        df = df.dropna().tail(limit)

        return df[["timestamp", "open", "high", "low", "close"]]

    except Exception as e:
        print("Coingecko OHLCV fetch error:", str(e))
        return None