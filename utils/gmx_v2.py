import json
import time
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS
from utils.price import get_current_price

# اتصال به آربیتروم
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# آدرس‌ها و ABIها
POSITION_ROUTER = "0x27c65d220046a8f2b3b0a3942d3f226e708c4b0f"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

with open("abi/PositionRouter.json") as f:
    router_abi = json.load(f)

router = w3.eth.contract(address=POSITION_ROUTER, abi=router_abi)

def open_position(signal):
    try:
        print(f"سیگنال دریافتی: {signal}")
        is_long = signal == "buy"
        eth_price = get_current_price()
        usd_amount = 20
        leverage = 5
        eth_amount = usd_amount / eth_price
        eth_in_wei = w3.to_wei(eth_amount, 'ether')
        execution_fee = w3.to_wei(0.0003, 'ether')
        entry_price = eth_price
        tp_price = entry_price * 1.06 if is_long else entry_price * 0.94
        sl_price = entry_price * 0.98 if is_long else entry_price * 1.02

        # مرحله ۱: سفارش ورود به پوزیشن
        print("ارسال سفارش ورود به پوزیشن...")
        tx = router.functions.createIncreaseOrder(
            WETH,
            WETH,
            eth_in_wei,
            0,
            int(entry_price * leverage),
            is_long,
            execution_fee,
            b'\x00' * 32,
            "0x0000000000000000000000000000000000000000"
        ).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'value': execution_fee,
            'gas': 800000,
            'gasPrice': w3.to_wei('2', 'gwei'),
            'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"پوزیشن باز شد! TX: {tx_hash.hex()}")

        # کمی صبر می‌کنیم تا سفارش ورود ثبت بشه
        time.sleep(10)

        # سفارش TP
        print("ثبت سفارش حد سود...")
        tp_tx = router.functions.createDecreaseOrder(
            WETH,
            WETH,
            eth_in_wei,
            int(tp_price),
            is_long,
            ACCOUNT_ADDRESS,
            execution_fee,
            b'\x00' * 32,
            "0x0000000000000000000000000000000000000000"
        ).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'value': execution_fee,
            'gas': 800000,
            'gasPrice': w3.to_wei('2', 'gwei'),
            'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        })

        signed_tp = w3.eth.account.sign_transaction(tp_tx, PRIVATE_KEY)
        tp_hash = w3.eth.send_raw_transaction(signed_tp.rawTransaction)
        print(f"سفارش TP ثبت شد! TX: {tp_hash.hex()}")

        # سفارش SL
        print("ثبت سفارش حد ضرر...")
        sl_tx = router.functions.createDecreaseOrder(
            WETH,
            WETH,
            eth_in_wei,
            int(sl_price),
            is_long,
            ACCOUNT_ADDRESS,
            execution_fee,
            b'\x00' * 32,
            "0x0000000000000000000000000000000000000000"
        ).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'value': execution_fee,
            'gas': 800000,
            'gasPrice': w3.to_wei('2', 'gwei'),
            'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        })

        signed_sl = w3.eth.account.sign_transaction(sl_tx, PRIVATE_KEY)
        sl_hash = w3.eth.send_raw_transaction(signed_sl.rawTransaction)
        print(f"سفارش SL ثبت شد! TX: {sl_hash.hex()}")

    except Exception as e:
        print(f"خطا در open_position GMX V2: {e}")