import requests

def get_current_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data["ethereum"]["usd"]
    except Exception as e:
        print(f"خطا در دریافت قیمت از CoinGecko: {e}")
        return None