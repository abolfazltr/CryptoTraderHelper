import requests
import logging

logging.basicConfig(level=logging.INFO)

# گرفتن قیمت از GMX V2
def get_price_from_gmx(symbol):
    try:
        url = "https://arbitrum-api.gmxinfra.io/prices/tokens"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logging.warning(f"GMX قیمت نیامد. status: {response.status_code}")
            return None
        data = response.json()
        symbol = symbol.upper()
        if symbol in data and "priceUsd" in data[symbol]:
            price = float(data[symbol]["priceUsd"])
            logging.debug(f"قیمت GMX برای {symbol}: {price}")
            return round(price, 4)
        else:
            logging.warning(f"توکن {symbol} در پاسخ GMX نبود.")
            return None
    except Exception as e:
        logging.warning(f"خطا در GMX برای {symbol}: {e}")
        return None

# گرفتن قیمت از CoinGecko
def get_price_from_coingecko(id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd&precision=6"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logging.warning(f"CoinGecko قیمت نیامد. status: {response.status_code}")
            return None
        data = response.json()
        if id in data:
            price = float(data[id]["usd"])
            logging.debug(f"قیمت CoinGecko برای {id}: {price}")
            return round(price, 4)
        else:
            logging.warning(f"توکن {id} در پاسخ CoinGecko نبود.")
            return None
    except Exception as e:
        logging.warning(f"خطا در CoinGecko برای {id}: {e}")
        return None

# گرفتن لیست قیمت برای تحلیل
def get_last_prices(symbol):
    # تعریف شناسه‌ها
    gmx_symbol = ""
    cg_id = ""

    if symbol == "ETHUSDT":
        gmx_symbol = "ETH"
        cg_id = "ethereum"
    elif symbol == "LINKUSDT":
        gmx_symbol = "LINK"
        cg_id = "chainlink"
    else:
        logging.error(f"نماد نامعتبر: {symbol}")
        return []

    # گرفتن قیمت از دو منبع
    price = get_price_from_gmx(gmx_symbol)
    if price is None:
        logging.info(f"قیمت GMX برای {gmx_symbol} یافت نشد، تلاش برای CoinGecko...")
        price = get_price_from_coingecko(cg_id)

    if price is None:
        logging.error(f"هیچ قیمتی یافت نشد برای {symbol}")
        return []

    return [price for _ in range(20)]