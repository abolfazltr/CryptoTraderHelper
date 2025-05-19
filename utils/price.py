import requests
from web3 import Web3
from config.settings import RPC_URL

# اتصال به آربیتروم برای خواندن قیمت از قرارداد
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# آدرس قرارداد Chainlink Price Feed برای ETH/USD روی Arbitrum
# توجه: این آدرس ممکنه تغییر کنه، از سورس رسمی Chainlink بررسی بشه
CHAINLINK_ETH_USD = Web3.to_checksum_address("0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612")

# ABI مختصر برای خواندن قیمت از Chainlink
PRICE_FEED_ABI = [{
    "inputs": [],
    "name": "latestAnswer",
    "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
    "stateMutability": "view",
    "type": "function"
}]

def get_current_price():
    try:
        print("⏳ در حال دریافت قیمت ETH از Chainlink...")
        contract = w3.eth.contract(address=CHAINLINK_ETH_USD, abi=PRICE_FEED_ABI)
        price = contract.functions.latestAnswer().call() / 1e8  # چون Chainlink 8 رقم اعشار دارد
        print(f"✅ قیمت واقعی ETH از Chainlink: {price} دلار")
        return price
    except Exception as e:
        print(f"⚠️ خطا در دریافت از Chainlink: {e}")

    # اگر نشد، تلاش با CoinGecko
    try:
        print("⏳ در حال دریافت قیمت از CoinGecko...")
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        price = response.json()['ethereum']['usd']
        print(f"✅ قیمت از CoinGecko: {price} دلار")
        return price
    except Exception as e:
        print(f"⚠️ خطا در دریافت CoinGecko: {e}")
        return None