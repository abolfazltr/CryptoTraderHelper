import requests
import pandas as pd

# قیمت لحظه‌ای واقعی از GMX V2
def get_token_price(token):
    addresses = {
        "ETH": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",  # WETH
        "LINK": "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4"   # LINK
    }

    if token not in addresses:
        raise Exception("توکن پشتیبانی نمی‌شود")

    url = f"https://arbitrum-api.gmx.io/prices/{addresses[token]}"
    response = requests.get(url)
    data = response.json()
    return data['price'] / 1e30

# گرفتن دیتای کندلی برای تحلیل تکنیکال از Binance
def get_last_prices(token, limit=100):
    symbol_map = {
        "ETH": "ETHUSDT",
        "LINK": "LINKUSDT"
    }

    if token not in symbol_map:
        raise Exception("توکن نامعتبر است")

    symbol = symbol_map[token]
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit={limit}"
    response = requests.get(url)
    raw = response.json()
    df = pd.DataFrame(raw, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df