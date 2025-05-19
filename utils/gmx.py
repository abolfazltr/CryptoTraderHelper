import json
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS
from utils.price_fetcher import get_current_price

# بارگذاری ABIها
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)
with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

# آدرس‌ها
POSITION_ROUTER = "0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868"
VAULT = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

# اتصال به وب۳
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

position_router = web3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)
vault = web3.eth.contract(address=VAULT, abi=vault_abi)

def open_position(signal):
    print(f"دریافت سیگنال: {signal}")
    is_long = signal.lower() == "buy"

    # دریافت قیمت لحظه‌ای
    price = get_current_price("ethereum")
    print(f"قیمت فعلی ETH: {price}")

    # محاسبه مقادیر
    amount_in_eth = 0.006  # حدود ۲۰ دلار
    amount_in_wei = web3.to_wei(amount_in_eth, 'ether')
    leverage = 5
    sl_percent = 0.02  # حد ضرر ۲٪
    tp_percent = 0.06  # حد سود ۶٪

    # محاسبه حد ضرر و حد سود بر اساس سیگنال
    if is_long:
        sl_price = int(price * (1 - sl_percent))
        tp_price = int(price * (1 + tp_percent))
        acceptable_price = int(price * 1.01)
    else:
        sl_price = int(price * (1 + sl_percent))
        tp_price = int(price * (1 - tp_percent))
        acceptable_price = int(price * 0.99)

    execution_fee = web3.to_wei(0.0003, 'ether')

    # آرگومان‌های تابع ایجاد پوزیشن
    path = [WETH]
    index_token = WETH
    min_out = 0
    size_delta = leverage * amount_in_wei
    referral_code = b'\x00' * 32
    callback_target = "0x0000000000000000000000000000000000000000"

    # ساخت تراکنش
    tx = position_router.functions.createIncreasePosition(
        path,
        index_token,
        amount_in_wei,
        min_out,
        size_delta,
        is_long,
        ACCOUNT_ADDRESS,
        acceptable_price,
        execution_fee,
        referral_code,
        callback_target
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'value': execution_fee,
        'nonce': web3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 800000,
        'gasPrice': web3.to_wei('5', 'gwei'),
    })

    # امضا و ارسال تراکنش
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"پوزیشن {'لانگ' if is_long else 'شورت'} باز شد. هش تراکنش: {web3.to_hex(tx_hash)}")