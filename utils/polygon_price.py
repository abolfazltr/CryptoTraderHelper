import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("POLYGON_API_KEY")

def get_polygon_candles(symbol: str, interval: str = "5", limit: int = 100):
    """
    دریافت کندل‌ها از Polygon.io برای یک توکن مشخص.
    :param symbol: مثل ETHUSDT یا LINKUSDT
    :param interval: تایم‌فریم به دقیقه (مثلاً "5")
    :param limit: تعداد کندل‌هایی که می‌خوایم
    :return: لیست کندل‌ها یا None در صورت خطا
    """
    try:
        now = datetime.utcnow()
        to_time = now.isoformat()
        from_time = (now - timedelta(minutes=int(interval) * limit)).isoformat()

        url = f"https://api.polygon.io/v2/aggs/ticker/X:{symbol}/range/{interval}/minute/{from_time}/{to_time}?adjusted=true&sort=asc&limit={limit}&apiKey={API_KEY}"

        response = requests.get(url)
        data = response.json()

        if "results" not in data:
            print(f"❌ خطا در دریافت کندل از Polygon برای {symbol}: {data}")
            return None

        candles = []
        for item in data["results"]:
            candles.append({
                "timestamp": item["t"],
                "open": item["o"],
                "high": item["h"],
                "low": item["l"],
                "close": item["c"],
                "volume": item["v"]
            })

        print(f"✅ دریافت {len(candles)} کندل برای {symbol} از Polygon.io")
        return candles

    except Exception as e:
        print(f"❌ خطای غیرمنتظره در دریافت کندل از Polygon: {e}")
        return None