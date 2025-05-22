from utils.polygon_price import get_polygon_candles

def get_price_data(token_symbol: str):
    """
    دریافت کندل‌های ۵ دقیقه‌ای برای توکن مشخص از Polygon.io
    :param token_symbol: مثل ETH یا LINK
    :return: لیست کندل‌ها یا None
    """
    print(f"📡 درخواست کندل برای {token_symbol} از Polygon.io")
    candles = get_polygon_candles(symbol=token_symbol, interval="5", limit=100)

    if not candles:
        print(f"❌ دریافت قیمت برای {token_symbol} ناموفق بود.")
        return None

    return candles