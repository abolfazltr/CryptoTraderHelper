import requests

def get_price_from_gmx(token_symbol):
    token_map = {
        "eth": "ETH",
        "link": "LINK"
    }
    if token_symbol.lower() not in token_map:
        return None

    try:
        response = requests.get("https://api.gmx.io/prices")
        response.raise_for_status()
        data = response.json()
        price = data[token_map[token_symbol.lower()]] / 1e30  # GMX returns price with 30 decimals
        return round(price, 2)
    except Exception as e:
        print(f"GMX price fetch error: {e}")
        return None

def get_price_from_dexscreener(token_symbol):
    try:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/pairs")
        response.raise_for_status()
        data = response.json()
        for pair in data["pairs"]:
            if token_symbol.lower() in pair["baseToken"]["symbol"].lower():
                return float(pair["priceUsd"])
        return None
    except Exception as e:
        print(f"Dexscreener price fetch error: {e}")
        return None

def get_current_price(token_symbol):
    token_symbol = token_symbol.lower()
    if token_symbol in ["eth", "link"]:
        return get_price_from_gmx(token_symbol)
    else:
        return get_price_from_dexscreener(token_symbol)