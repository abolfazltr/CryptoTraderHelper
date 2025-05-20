import requests

# گرفتن قیمت از GMX
def get_price_from_gmx(symbol):
    try:
        url = f"https://api.gmx.io/prices/{symbol}"
        response = requests.get(url)
        data = response.json()
        return round(float(data['price']) / 1e30, 2)
    except:
        return None

# گرفتن قیمت از CoinGecko
def get_price_from_coingecko(id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return float(data[id]["usd"])
    except:
        return None

# برگرداندن لیست ۲۰تایی قیمت واقعی برای تحلیل
def get_last_prices(symbol):
    # تطبیق برای توکن‌های GMX
    gmx_symbol = ""
    if symbol == "ETHUSDT":
        gmx_symbol = "ETH"
    elif symbol == "LINKUSDT":
        gmx_symbol = "LINK"
    else:
        return []

    price = get_price_from_gmx(gmx_symbol)
    if price is None:
        if gmx_symbol == "ETH":
            price = get_price_from_coingecko("ethereum")
        elif gmx_symbol == "LINK":
            price = get_price_from_coingecko("chainlink")

    if price is None:
        return []

    return [price for _ in range(20)]