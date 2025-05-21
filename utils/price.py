import requests
from config.tokens import TOKENS

# دریافت قیمت از CoinGecko
def get_price_from_coingecko(symbol):
    coingecko_id = None
    for token in TOKENS:
        if token["gmx_id"].lower() == symbol.lower():
            coingecko_id = token["coingecko_id"]
            break

    if not coingecko_id:
        raise ValueError(f"شناسه CoinGecko برای {symbol} یافت نشد.")

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
    res = requests.get(url)
    data = res.json()

    return float(data[coingecko_id]["usd"])

# تابع اصلی برای گرفتن قیمت فعلی هر توکن
def get_current_price(symbol):
    return get_price_from_coingecko(symbol)