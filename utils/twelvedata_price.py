import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TWELVEDATA_API_KEY")

def get_twelvedata_candles(symbol, interval="15min", limit=100):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol.upper() + "/USD",
        "interval": interval,
        "outputsize": limit,
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "values" not in data:
            print(f"❌ دریافت کندل‌ها برای {symbol.upper()} ناموفق بود: {data}")
            return None

        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.set_index("datetime", inplace=True)
        df = df.astype(float)
        df = df.sort_index()

        return df[["open", "high", "low", "close"]]  # بدون volume

    except Exception as e:
        print(f"❌ خطا در دریافت کندل‌های {symbol.upper()}: {e}")
        return None