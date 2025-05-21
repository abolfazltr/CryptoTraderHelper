import json
from web3 import Web3
from config.settings import PRIVATE_KEY, RPC_URL, ACCOUNT_ADDRESS

# اتصال به شبکه
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# بارگذاری ABI
with open("abi/ExchangeRouter.json") as f:
    exchange_router_abi = json.load(f)

exchange_router_address = w3.to_checksum_address("0x7c68c7866a64fa2160f78eeae12217ffbf871fa8")
exchange_router = w3.eth.contract(address=exchange_router_address, abi=exchange_router_abi)

# توکن‌ها و بازارها
markets = {
    "ETH": {
        "market": w3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A"),
        "collateral": w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
    },
    "LINK": {
        "market": w3.to_checksum_address("0x1A3AC2A1dcC55dEF09E2Fe43b74Ec37D3D5316"),
        "collateral": w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
    }
}

def set_tp_sl(token_symbol, position_key, tp_price, sl_price):
    if token_symbol not in markets:
        raise Exception("توکن نامعتبر")

    market_info = markets[token_symbol]

    # ساخت آرگومان‌های سفارش کاهش موقعیت
    decrease_order = {
        "receiver": ACCOUNT_ADDRESS,
        "callbackContract": "0x0000000000000000000000000000000000000000",
        "market": market_info["market"],
        "initialCollateralToken": market_info["collateral"],
        "sizeDeltaUsd": 0,  # مقدار کاهش (در ادامه وارد کن)
        "acceptablePrice": 0,  # قیمتی که کاهش را می‌پذیری
        "triggerPrice": 0,     # قیمت فعال‌سازی
        "triggerAboveThreshold": True,
        "executionFee": 0,
        "shouldUnwrapNativeToken": False
    }

    # ساخت سفارش SL
    sl_order = decrease_order.copy()
    sl_order["triggerPrice"] = int(sl_price * (10 ** 30))
    sl_order["triggerAboveThreshold"] = False  # چون می‌خوایم وقتی قیمت افت کرد فعال شه

    # ساخت سفارش TP
    tp_order = decrease_order.copy()
    tp_order["triggerPrice"] = int(tp_price * (10 ** 30))
    tp_order["triggerAboveThreshold"] = True  # چون وقتی قیمت بالا رفت فعال شه

    # ارسال تراکنش (برای SL)
    tx1 = exchange_router.functions.createOrder(sl_order).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 1_500_000,
        'gasPrice': w3.to_wei('0.02', 'gwei')
    })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=PRIVATE_KEY)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
    print("Stop Loss TX:", tx_hash1.hex())

    # ارسال تراکنش (برای TP)
    tx2 = exchange_router.functions.createOrder(tp_order).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 1_500_000,
        'gasPrice': w3.to_wei('0.02', 'gwei')
    })
    signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key=PRIVATE_KEY)
    tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
    print("Take Profit TX:", tx_hash2.hex())