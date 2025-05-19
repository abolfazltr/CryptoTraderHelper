import json
from web3 import Web3
from utils.price_fetcher import get_current_price
from config.settings import PRIVATE_KEY, RPC_URL, ACCOUNT_ADDRESS

# بارگذاری ABIها
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

# آدرس قراردادها
POSITION_ROUTER = "0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868"
VAULT = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

# اتصال به شبکه
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

position_router = w3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)
vault = w3.eth.contract(address=VAULT, abi=vault_abi)

def open_position(signal, leverage, amount_usd, token):
    entry_price = get_current_price(token)
    if not entry_price:
        print("خطا در دریافت قیمت")
        return

    is_long = signal == "long"
    amount_in = w3.to_wei(amount_usd / entry_price, 'ether')
    size_delta = w3.to_wei(amount_usd * leverage, 'ether')
    acceptable_price = int(entry_price * (1.01 if is_long else 0.99) * 1e30)
    execution_fee = w3.to_wei(0.0003, 'ether')
    referral_code = b'\x00' * 32
    path = [WETH]
    index_token = WETH
    min_out = 0

    params = [
        path,
        index_token,
        amount_in,
        min_out,
        size_delta,
        is_long,
        acceptable_price,
        execution_fee,
        referral_code
    ]

    try:
        tx = position_router.functions.createIncreasePosition(*params).build_transaction({
            "from": ACCOUNT_ADDRESS,
            "value": execution_fee,
            "nonce": w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
            "gas": 700000,
            "gasPrice": w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(f"\nپوزیشن {signal.upper()} باز شد.")
        print(f"قیمت ورود: {entry_price:.4f}")
        print("TX Hash:", w3.to_hex(tx_hash))

        # بعد از باز کردن پوزیشن، حد سود و ضرر رو ست کن
        set_tp_sl(signal, entry_price, size_delta, token)

    except Exception as e:
        print("خطا در باز کردن پوزیشن:", str(e))

def set_tp_sl(signal, entry_price, size_delta, token):
    is_long = signal == "long"
    tp_price = entry_price * (1 + 0.03) if is_long else entry_price * (1 - 0.03)
    sl_price = entry_price * (1 - 0.02) if is_long else entry_price * (1 + 0.02)

    acceptable_tp = int(tp_price * 1e30)
    acceptable_sl = int(sl_price * 1e30)

    for price, label in [(acceptable_tp, "TP"), (acceptable_sl, "SL")]:
        try:
            tx = position_router.functions.createDecreasePosition(
                [token],
                token,
                0,
                size_delta,
                is_long,
                account.address,
                price,
                0,
                False
            ).build_transaction({
                "from": ACCOUNT_ADDRESS,
                "nonce": w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
                "gas": 700000,
                "gasPrice": w3.eth.gas_price
            })

            signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"{label} ثبت شد. TX Hash:", w3.to_hex(tx_hash))

        except Exception as e:
            print(f"خطا در ست کردن {label}:", str(e))