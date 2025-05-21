import json
from web3 import Web3
from config.settings import PRIVATE_KEY, RPC_URL, ACCOUNT_ADDRESS
from utils.tp_sl_manager import set_tp_sl  # تابع تنظیم TP/SL

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# بارگذاری ABI
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

position_router_address = w3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868")
position_router = w3.eth.contract(address=position_router_address, abi=position_router_abi)

# آدرس بازار و وثیقه‌ها برای هر توکن
markets = {
    "ETH": {
        "market": w3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A"),
        "collateral": w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")  # WETH
    },
    "LINK": {
        "market": w3.to_checksum_address("0x1A3AC2A1dcC55dEF09E2Fe43b74Ec37D3D5316"),
        "collateral": w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")  # WETH
    }
}

def open_position(token_symbol, is_long, amount_usd, entry_price, tp_price, sl_price):
    if token_symbol not in markets:
        raise Exception("توکن پشتیبانی نمی‌شود")

    market = markets[token_symbol]["market"]
    collateral_token = markets[token_symbol]["collateral"]

    execution_fee = w3.to_wei("0.0003", "ether")
    size_delta = int(amount_usd * (10 ** 30))
    acceptable_price = int(entry_price * (1.01 if is_long else 0.99) * 10**30)

    # ساخت تراکنش باز کردن پوزیشن
    tx = position_router.functions.createIncreasePosition(
        [market, collateral_token, collateral_token],
        size_delta,
        acceptable_price,
        is_long,
        0
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'value': execution_fee,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 1_800_000,
        'gasPrice': w3.to_wei("0.03", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("TX Hash (Open Position):", tx_hash.hex())

    # فرض می‌کنیم position_key همون مارکت+اکانت باشه (درصورت نیاز می‌تونیم دقیق‌تر بسازیم)
    position_key = ACCOUNT_ADDRESS[:10] + "_" + token_symbol

    # بلافاصله بعدش تنظیم TP و SL
    set_tp_sl(token_symbol, position_key, tp_price, sl_price)