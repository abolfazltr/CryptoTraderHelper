import requests
import pandas as pd
from utils.gmx_v2 import w3, vault_contract, TOKENS

def get_price_data(symbol):
    # قیمت از CoinGecko
    coingecko_price = None
    try:
        if symbol == "ETHUSD":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        elif symbol == "LINKUSDT":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=chainlink&vs_currencies=usd"
        else:
            url = ""
        response = requests.get(url)
        data = response.json()
        if symbol == "ETHUSD":
            coingecko_price = data["ethereum"]["usd"]
        elif symbol == "LINKUSDT":
            coingecko_price = data["chainlink"]["usd"]
    except Exception as e:
        print(f"⚠️ ارور دریافت قیمت از CoinGecko برای {symbol}:", e)

    # قیمت از GMX
    gmx_price = None
    try:
        token_address = TOKENS[symbol]
        price = vault_contract.functions.getMinPrice(token_address).call()
        gmx_price = price / 1e30
    except Exception as e:
        print(f"❌ ارور GMX برای {symbol}:", e)

    print(f"✅ {symbol} از GMX: {gmx_price}")
    print(f"✅ {symbol} از CoinGecko: {coingecko_price}")

    final_price = gmx_price if gmx_price else coingecko_price
    if not final_price:
        return None

    # ساخت دیتافریم برای تحلیل تکنیکال
    df = pd.DataFrame({
        'high': [final_price] * 10,
        'low': [final_price * 0.98] * 10,
        'close': [final_price * 0.99] * 10
    })

    return final_price, df