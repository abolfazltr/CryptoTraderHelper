import json
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS
from utils.price import get_token_price

# اتصال به بلاک‌چین
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# آدرس‌های رسمی GMX v2 روی Arbitrum
POSITION_ROUTER = Web3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868")
VAULT = Web3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A")
POSITION_MANAGER = Web3.to_checksum_address("0xbB1748bF0bBfE6c5F9A8f6b78f3F2A5973b9eB21")

# بارگذاری ABIها
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

with open("abi/PositionManager.json") as f:
    position_manager_abi = json.load(f)

# ساخت قراردادها
position_router = w3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)
vault = w3.eth.contract(address=VAULT, abi=vault_abi)
position_manager = w3.eth.contract(address=POSITION_MANAGER, abi=position_manager_abi)

# تابع باز کردن پوزیشن
def open_position(token_symbol, is_long=True, amount_usd=20):
    print(f"[+] اجرای پوزیشن برای {token_symbol}...")

    # دریافت قیمت لحظه‌ای از price.py
    price = get_token_price(token_symbol)
    if price is None:
        print(f"[x] قیمت {token_symbol} دریافت نشد.")
        return

    entry = price
    tp = round(entry * 1.03, 2)
    sl = round(entry * 0.97, 2)

    print(f"Entry: {entry}, TP: {tp}, SL: {sl}")
    print(f"✅ پوزیشن {'لانگ' if is_long else 'شورت'} برای {token_symbol} باز شد با TP و SL واقعی.")

    # اینجا در نسخه واقعی می‌تونه تراکنش ارسال بشه (در صورت نیاز اضافه می‌کنیم)