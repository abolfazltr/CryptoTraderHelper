import requests
import logging

logging.basicConfig(level=logging.INFO)

# گرفتن کندل 5 دقیقه‌ای از Gate.io
def get_last_prices(symbol):
    try:
        # تبدیل نماد به فرمت Gate.io
        if symbol == "ETHUSDT":
            gate_symbol = "ETH_USDT"
        elif symbol == "LINKUSDT":
            gate_symbol = "LINK_USDT"
        else:
            logging.error(f"نماد نامعتبر: {symbol}")
            return []

        url = f"https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair={gate_symbol}&interval=5m&limit=20"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            logging.warning(f"خطا در دریافت کندل برای {symbol}: {response.status_code}")
            return []

        data = response.json()

        # گرفتن قیمت بسته‌شدن (close) هر کندل
        prices = [float(candle[2]) for candle in data]  # candle[2] = close
        prices.reverse()  # از قدیمی به جدید

        logging.info(f"دریافت {len(prices)} کندل برای {symbol} انجام شد.")
        return prices

    except Exception as e:
        logging.warning(f"استثنا در دریافت قیمت برای {symbol}: {e}")
        return []

# گرفتن قیمت فعلی از CoinGecko برای backup
def get_price_from_coingecko(id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data[id]["usd"])
    except:
        return None