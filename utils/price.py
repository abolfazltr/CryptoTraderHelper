import json
from web3 import Web3
from config.settings import RPC_URL

w3 = Web3(Web3.HTTPProvider(RPC_URL))

VAULT = Web3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A")
WETH = Web3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")

with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

vault = w3.eth.contract(address=VAULT, abi=vault_abi)

def get_current_price():
    try:
        min_price = vault.functions.getMinPrice(WETH).call()
        eth_price = w3.from_wei(min_price, 'ether')
        print(f"✅ قیمت لحظه‌ای ETH از GMX Vault: {eth_price} دلار")
        return float(eth_price)
    except Exception as e:
        print("⚠️ خطا در دریافت قیمت از GMX Vault:")
        print(f"→ علت: {e}")
        return None