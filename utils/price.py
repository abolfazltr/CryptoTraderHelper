import requests
import pandas as pd

def get_price_data(symbol="ETHUSDT", interval="5m", limit=100):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close',
            'volume', 'close_time', 'quote_asset_volume',
            'number_of_trades', 'taker_buy_base_volume',
            'taker_buy_quote_volume', 'ignore'
        ])

        df['close'] = df['close'].astype(float)
        return df[['close']]
    except Exception as e:
        print("خطا در دریافت قیمت:", str(e))
        return None

# تابعی که در gmx.py نیاز است
def get_current_price(symbol="ETHUSDT"):
    df = get_price_data(symbol)
    if df is not None and not df.empty:
        return df['close'].iloc[-1]
    return None