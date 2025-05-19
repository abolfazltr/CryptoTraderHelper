import requests
import pandas as pd

def get_ohlcv(symbol="ETHUSDT", interval="5m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Binance API error:", response.text)
            return None

        data = response.json()
        if not data:
            print("Empty data from Binance.")
            return None

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])

        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        return df[['timestamp', 'open', 'high', 'low', 'close']]

    except Exception as e:
        print("Error fetching OHLCV:", str(e))
        return None