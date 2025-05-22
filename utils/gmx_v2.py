import json
from web3 import Web3
from config.settings import PRIVATE_KEY, RPC_URL, ACCOUNT_ADDRESS

# اتصال به آربیتروم
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# بارگذاری ABIها
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

# آدرس قراردادها در GMX V2
POSITION_ROUTER = "0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
LINK = "0xf97c3c3d8f7c9ceba6ba9da3cea7f3e60295a16a"

position_router = w3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)

def open_position(token, is_long, entry_price):
    print(f"🚀 باز کردن پوزیشن واقعی برای {token.upper()} - {'لانگ' if is_long else 'شورت'}")

    token_address = WETH if token == "eth" else LINK
    size_usd = 100  # معادل ۲۰ دلار × لوریج ۵
    collateral = w3.to_wei(20, 'ether')

    # محاسبه قیمت‌های قابل قبول
    acceptable_price = int(entry_price * (1.01 if is_long else 0.99) * 1e30)

    # محاسبه TP و SL برای استفاده در همان تراکنش
    tp_price = entry_price * (1.03 if is_long else 0.97)
    sl_price = entry_price * (0.97 if is_long else 1.03)
    tp_price_scaled = int(tp_price * 1e30)
    sl_price_scaled = int(sl_price * 1e30)

    tx = position_router.functions.createIncreasePosition(
        [token_address],
        token_address,
        collateral,
        0,
        int(size_usd * 1e30),
        is_long,
        acceptable_price,
        tp_price_scaled,  # TP واقعی
        sl_price_scaled   # SL واقعی
    ).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "value": 0,
        "nonce": w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        "gas": 900000,
        "gasPrice": w3.to_wei("2", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"✅ پوزیشن باز شد با TP/SL واقعی: {w3.to_hex(tx_hash)}")