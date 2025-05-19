from web3 import Web3
from config.settings import RPC_URL
import pandas as pd
from datetime import datetime
import json  # برای خواندن ABI به صورت json

VAULT = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

# بارگذاری ABI به‌صورت JSON (اصلاح شده)
with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

def get_ohlcv():
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        vault = w3.eth.contract(address=VAULT, abi=vault_abi)

        price_raw = vault.functions.getMinPrice(WETH).call()
        price = price_raw / 1e30

        now = datetime.utcnow()
        df = pd.DataFrame([{
            "timestamp": now,
            "open": price * 0.99,
            "high": price * 1.01,
            "low": price * 0.98,
            "close": price
        } for _ in range(100)])

        return df

    except Exception as e:
        print("GMX Vault price fetch error:", str(e))
        return None

def get_current_price():
    df = get_ohlcv()
    if df is not None and not df.empty:
        return df["close"].iloc[-1]
    return None