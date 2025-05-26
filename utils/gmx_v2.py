import json
import time
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)
with open("abi/OrderBook.json") as f:
    orderbook_abi = json.load(f)

POSITION_ROUTER = Web3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868")
ORDER_BOOK = Web3.to_checksum_address("0x58B5730a272dfC2D6eEa383753d4a45C07F1B4Ce")
WETH = Web3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
LINK = Web3.to_checksum_address("0xf97c3c3d8f7c9ceba6ba9da3cea7f3e60295a16a")

position_router = w3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)
orderbook = w3.eth.contract(address=ORDER_BOOK, abi=orderbook_abi)

def set_tp_sl(token, is_long, entry_price):
    print(f"🎯 تنظیم حد سود و حد ضرر برای {token.upper()}")

    token_address = WETH if token == "eth" else LINK
    size_usd = 80
    size_delta = int(size_usd * 1e30)

    if is_long:
        tp_price = entry_price * 1.035
        sl_price = entry_price * 0.98
    else:
        tp_price = entry_price * 0.96
        sl_price = entry_price * 1.025

    tp_price_scaled = int(tp_price * 1e30)
    sl_price_scaled = int(sl_price * 1e30)
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    tx_tp = orderbook.functions.createDecreasePosition(
        [token_address],
        token_address,
        size_delta,
        token_address,
        0,
        is_long,
        tp_price_scaled,
        True
    ).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "value": w3.to_wei("0.0003", "ether"),
        "nonce": nonce,
        "gas": 800000,
        "gasPrice": w3.to_wei("2", "gwei")
    })

    tx_sl = orderbook.functions.createDecreasePosition(
        [token_address],
        token_address,
        size_delta,
        token_address,
        0,
        is_long,
        sl_price_scaled,
        False
    ).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "value": w3.to_wei("0.0003", "ether"),
        "nonce": nonce + 1,
        "gas": 800000,
        "gasPrice": w3.to_wei("2", "gwei")
    })

    signed_tp = w3.eth.account.sign_transaction(tx_tp, private_key=PRIVATE_KEY)
    signed_sl = w3.eth.account.sign_transaction(tx_sl, private_key=PRIVATE_KEY)

    tx_hash_tp = w3.eth.send_raw_transaction(signed_tp.raw_transaction)
    tx_hash_sl = w3.eth.send_raw_transaction(signed_sl.raw_transaction)

    print(f"✅ حد سود ثبت شد: {w3.to_hex(tx_hash_tp)}")
    print(f"✅ حد ضرر ثبت شد: {w3.to_hex(tx_hash_sl)}")

def open_position(token, is_long, entry_price):
    print(f"🚀 باز کردن پوزیشن واقعی برای {token.upper()} - {'لانگ' if is_long else 'شورت'}")

    token_address = WETH if token == "eth" else LINK
    size_usd = 80
    collateral_usd = 40
    collateral = int((collateral_usd / entry_price) * 1e18)

    acceptable_price = int(entry_price * (0.99 if is_long else 1.01) * 1e30)
    min_out = int(entry_price * 0.99 * 1e30)

    execution_fee = w3.to_wei("0.0004", "ether")
    referral_code = b'\x00' * 32
    callback_target = "0x0000000000000000000000000000000000000000"
    should_unwrap_native_token = False
    callback_gas_limit = 0

    for attempt in range(3):
        try:
            nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

            tx = position_router.functions.createIncreasePosition(
                [token_address],
                token_address,
                collateral,
                min_out,
                int(size_usd * 1e30),
                is_long,
                acceptable_price,
                execution_fee,
                referral_code,
                callback_target,
                should_unwrap_native_token,
                callback_gas_limit
            ).build_transaction({
                "from": ACCOUNT_ADDRESS,
                "value": execution_fee,
                "nonce": nonce,
                "gas": 700000,
                "gasPrice": w3.to_wei("2", "gwei")
            })

            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            print(f"⏳ در انتظار تایید پوزیشن... {w3.to_hex(tx_hash)}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt.status == 1:
                print(f"✅ پوزیشن باز شد با TP/SL واقعی: {w3.to_hex(tx_hash)}")
                set_tp_sl(token, is_long, entry_price)
            else:
                print(f"❌ تراکنش انجام نشد (پوزیشن باز نشد): {w3.to_hex(tx_hash)}")
            break

        except Exception as e:
            print(f"⛔ تلاش {attempt+1} برای باز کردن پوزیشن ناموفق بود: {str(e)}")
            time.sleep(3)