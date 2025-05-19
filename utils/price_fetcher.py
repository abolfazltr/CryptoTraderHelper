import requests

def get_current_price(symbol="ETHUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["price"])