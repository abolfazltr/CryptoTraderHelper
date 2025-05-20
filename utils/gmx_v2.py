import json
from web3 import Web3
from config.settings import PRIVATE_KEY, RPC_URL, ACCOUNT_ADDRESS

# اتصال به شبکه
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# بارگذاری ABIها
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

# آدرس قراردادها
POSITION_ROUTER = w3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868")
VAULT = w3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A")

# آدرس توکن‌ها
TOKENS = {
    "ETHUSD": w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1"),
    "LINKUSDT": w3.to_checksum_address("0xf97f4df75117a78c1A5a0DBb814Af92458539FB4"),
}

# ساخت قراردادها
position_router_contract = w3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)
vault_contract = w3.eth.contract(address=VAULT, abi=vault_abi)

def open_position(symbol, signal):
    token = TOKENS.get(symbol)
    if not token:
        print(f"⛔ توکن {symbol} در لیست نیست.")
        return

    amount_in = w3.to_wei(0.008, 'ether')  # تقریباً ۲۰ دلار
    is_long = signal == "buy"
    acceptable_price = 10**30  # قیمت قابل قبول برای اجرای معامله
    min_out = 0
    size_delta = w3.to_wei(0.04, 'ether')  # حجم معامله با لوریج ۵ (تقریباً ۱۰۰ دلار)

    params = [
        [token],        # path
        token,          # indexToken
        amount_in,      # amountIn
        min_out,        # minOut
        acceptable_price,  # acceptablePrice
        is_long,        # isLong
        size_delta,     # sizeDelta
        0,              # triggerPrice
        acceptable_price # acceptablePrice
    ]

    try:
        tx = position_router_contract.functions.createIncreasePosition(
            *params,
            0,  # referralCode
            "0x0000000000000000000000000000000000000000"  # callbackTarget
        ).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'value': 0,
            'gas': 800000,
            'gasPrice': w3.to_wei("2", "gwei"),
            'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ پوزیشن واقعی {signal} برای {symbol} ارسال شد. هش: {w3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"⛔ خطا در ارسال پوزیشن برای {symbol}: {e}")