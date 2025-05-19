import requests
import pandas as pd
from datetime import datetime

def get_ohlcv():
    try:
        url = "https://arbitrum-api.gmxinfra.io/prices"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("GMX price fetch error:", response.text)
            return None

        data = response.json()
        weth_price = data.get("WETH", {}).get("minPrice", None)
        if weth_price is None:
            print("WETH price not found in GMX data.")
            return None

        price = int(weth_price) / 1e30  # GMX قیمت رو با ۳۰ رقم اعشار می‌ده

        now = datetime.utcnow()
        df = pd.DataFrame([{
            "timestamp": now,
            "open": price * 0.99,
            "high": price * 1.01,
            "low": price * 0.98,
            "close": price
        } for _ in range(100)])

        return df

    except Exception as e:
        print("Error fetching price from GMX:", str(e))
        return None