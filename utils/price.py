from utils.twelvedata_price import get_twelvedata_candles

def get_current_price(token: str):
    candles = get_twelvedata_candles(token, interval="15min", limit=1)
    if candles is None or candles.empty:
        print(f"❌ دریافت قیمت برای {token} ناموفق بود")
        return None

    current_price = candles["close"].iloc[-1].item()  # تبدیل به float
    print(f"🟡 قیمت لحظه‌ای {token.upper()}: {current_price}")
    return current_price

def get_recent_candles(token: str, limit: int = 100):
    candles = get_twelvedata_candles(token, interval="15min", limit=limit)
    if candles is None or candles.empty:
        print(f"❌ دریافت کندل‌ها برای {token} ناموفق بود")
        return None

    return candles