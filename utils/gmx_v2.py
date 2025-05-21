import json
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS
from utils.helpers import load_abi
from utils.price import get_current_price

# اتصال به شبکه
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.to_checksum_address(ACCOUNT_ADDRESS)

# بارگذاری ABI
router_abi = load_abi("abi/PositionRouter.json")
router = w3.eth.contract(
    address=w3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868"),
    abi=router_abi
)

# آدرس توکن‌ها (دقیق)
WETH = w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
LINK = w3.to_checksum_address("0xf97f4df75117a78c1A5a0DBb814Af92458539FB4")

def open_position(token_symbol, direction):
    print(f"🚀 باز کردن پوزیشن برای {token_symbol.upper()} به صورت {direction.upper()}")

    # انتخاب توکن
    if token_symbol.lower() == "eth":
        index_token = WETH
    elif token_symbol.lower() == "link":
        index_token = LINK
    else:
        print("❌ توکن ناشناخته است.")
        return

    path = [index_token]
    is_long = direction.lower() == "long"

    # قیمت لحظه‌ای
    price = get_current_price(token_symbol)
    print(f"✅ قیمت فعلی: {price}")

    # تنظیمات پوزیشن
    collateral = 20
    leverage = 5
    size_usd = collateral * leverage
    size_delta = int(size_usd * 1e30)

    # محاسبه TP و SL طبق استراتژی واقعی
    if is_long:
        tp_price = price * 1.035     # +3.5%
        sl_price = price * 0.978     # -2.2%
    else:
        tp_price = price * 0.965     # -3.5%
        sl_price = price * 1.022     # +2.2%

    tp_price_scaled = int(tp_price * 1e30)
    sl_price_scaled = int(sl_price * 1e30)
    acceptable_price = int(price * 1e30)

    # هزینه اجرای واقعی تراکنش
    execution_fee = w3.to_wei("0.003", "ether")

    # ساخت تراکنش باز کردن پوزیشن
    tx = router.functions.createIncreasePosition(
        path,
        index_token,
        size_delta,
        is_long,
        acceptable_price,
        execution_fee
    ).build_transaction({
        'from': account,
        'value': execution_fee,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 800000,
        'gasPrice': w3.to_wei('1.5', 'gwei')
    })

    # ارسال تراکنش
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("✅ پوزیشن ثبت شد | TX Hash:", tx_hash.hex())

    print(f"🎯 حد سود: {tp_price:.2f} | حد ضرر: {sl_price:.2f}")
    return tx_hash.hex()