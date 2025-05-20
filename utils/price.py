import requests

def get_price_data(symbol):
    if symbol == "ETHUSDT":
        gmx_price = get_price_from_gmx("ETH")
        coingecko_price = get_price_from_coingecko("ethereum")
    elif symbol == "LINKUSDT":
        gmx_price = get_price_from_gmx("LINK")
        coingecko_price = get_price_from_coingecko("chainlink")
    else:
        return None

    if gmx_price is None or coingecko_price is None:
        return None

    average_price = round((gmx_price + coingecko_price) / 2, 2)
    print(f"✅ قیمت نهایی {symbol}: {average_price}")
    return generate_dummy_candles(average_price)

def get_price_from_gmx(token):
    try:
        url = f"https://api.gmx.io/prices/{token.upper()}"
        response = requests.get(url)
        data = response.json()
        price = float(data["price"])
        print(f"✅ {token} از GMX: {price}")
        return price
    except:
        return None

def get_price_from_coingecko(token_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        price = float(data[token_id]["usd"])
        print(f"✅ {token_id} از CoinGecko: {price}")
        return price
    except:
        return None

def generate_dummy_candles(price):
    import pandas as pd
    data = {
        "open": [price * 0.99],
        "high": [price * 1.01],
        "low": [price * 0.98],
        "close": [price],
    }
    df = pd.DataFrame(data)
    return df