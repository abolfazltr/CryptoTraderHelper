import requests

def get_price_from_coingecko(token):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd")
        if response.status_code == 429:
            raise Exception("Rate limit from CoinGecko")
        return response.json()[token]["usd"]
    except Exception as e:
        print(f"❌ CoinGecko شکست خورد: {e}")
        return None

def get_price_from_bitget(symbol):
    try:
        response = requests.get(f"https://api.bitget.com/api/spot/v1/market/ticker?symbol={symbol}")
        data = response.json()
        return float(data["data"]["close"])
    except Exception as e:
        print(f"❌ Bitget شکست خورد: {e}")
        return None

def get_current_price(token):
    # نقشه بین توکن‌ها و سمبل بیت‌گت
    bitget_map = {
        "eth": "ETHUSDT",
        "link": "LINKUSDT"
    }

    price = get_price_from_coingecko(token)
    if price is None:
        symbol = bitget_map.get(token)
        price = get_price_from_bitget(symbol)

    return price