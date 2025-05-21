import requests
import time

def get_current_price(symbol: str) -> float:
    """
    گرفتن قیمت لحظه‌ای از MEXC
    symbol باید مثل ETHUSDT یا LINKUSDT باشه
    """
    try:
        url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"❌ خطا در دریافت قیمت {symbol}: {e}")
        return None

def get_candles(symbol: str, interval='5m', limit=20):
    """
    گرفتن کندل‌ها از MEXC برای تحلیل
    interval مثل 1m, 5m, 15m, 1h, ...
    """
    try:
        url = f"https://api.mexc.com/api/v3/klines?symbol={symbol.upper()}USDT&interval={interval}&limit={limit}"
        response = requests.get(url)
        data = response.json()

        candles = []
        for d in data:
            candles.append({
                'timestamp': d[0],
                'open': float(d[1]),
                'high': float(d[2]),
                'low': float(d[3]),
                'close': float(d[4]),
                'volume': float(d[5])
            })

        return candles
    except Exception as e:
        print(f"❌ خطا در دریافت کندل‌های {symbol}: {e}")
        return []