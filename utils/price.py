import requests
import logging

logging.basicConfig(level=logging.INFO)

# گرفتن قیمت از GMX
def get_price_from_gmx(symbol):
    try:
        url = f"https://api.gmx.io/prices/{symbol}"
        response = requests.get(url)
        data = response.json()
        price = round(float(data['price']) / 1e30, 2)
        logging.debug(f"قیمت GMX برای {symbol}: {price}")
        return price
    except Exception as e:
        logging.warning(f"خطا در دریافت قیمت از GMX برای {symbol}: {e}")
        return None

# گرفتن قیمت از CoinGecko
def get_price_from_coingecko(id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        price = float(data[id]["usd"])
        logging.debug(f"قیمت CoinGecko برای {id}: {price}")
        return price
    except Exception as e:
        logging.warning(f"خطا در دریافت قیمت از CoinGecko برای {id}: {e}")
        return None

# برگرداندن لیست ۲۰تایی قیمت واقعی برای تحلیل
def get_last_prices(symbol):
    gmx_symbol = ""
    if symbol == "ETHUSDT":
        gmx_symbol = "ETH"
    elif symbol == "LINKUSDT":
        gmx_symbol = "LINK"
    else:
        logging.error(f"نماد نامعتبر برای تحلیل: {symbol}")
        return []

    price = get_price_from_gmx(gmx_symbol)
    if price is None:
        logging.info(f"قیمت از GMX برای {gmx_symbol} نیامد. تلاش برای CoinGecko...")
        if gmx_symbol == "ETH":
            price = get_price_from_coingecko("ethereum")
        elif gmx_symbol == "LINK":
            price = get_price_from_coingecko("chainlink")

    if price is None:
        logging.error(f"هیچ قیمتی یافت نشد برای {symbol}")
        return []

    return [price for _ in range(20)]