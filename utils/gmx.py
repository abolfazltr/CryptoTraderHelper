import json
from web3 import Web3
from config.settings import RPC_URL, PRIVATE_KEY

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

with open('abi/PositionRouter.json') as f:
    position_router_abi = json.load(f)
with open('abi/Vault.json') as f:
    vault_abi = json.load(f)

POSITION_ROUTER_ADDRESS = '0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868'
VAULT_ADDRESS = '0x489ee077994B6658eAfA855C308275EAd8097C4A'
WETH_ADDRESS = web3.to_checksum_address('0x82af49447d8a07e3bd95bd0d56f35241523fbab1')

position_router = web3.eth.contract(address=POSITION_ROUTER_ADDRESS, abi=position_router_abi)
vault = web3.eth.contract(address=VAULT_ADDRESS, abi=vault_abi)

def get_token_price(token, is_max=True):
    if is_max:
        return vault.functions.getMaxPrice(token).call()
    else:
        return vault.functions.getMinPrice(token).call()

def open_position(signal, leverage, amount_usd, token):
    is_long = signal == "long"
    collateral_token = WETH_ADDRESS
    index_token = WETH_ADDRESS
    path = [WETH_ADDRESS]

    price = get_token_price(index_token, is_max=not is_long) / 1e30
    amount_in_eth = amount_usd / price
    amount_in_wei = int(amount_in_eth * 1e18)
    size_delta = amount_in_wei * leverage

    acceptable_price = int(get_token_price(index_token, is_max=not is_long) * (1.03 if is_long else 0.97))
    execution_fee = web3.to_wei(0.0003, 'ether')
    referral_code = b'\x00' * 32
    callback_target = '0x0000000000000000000000000000000000000000'

    tx = position_router.functions.createIncreasePosition(
        path,
        index_token,
        amount_in_wei,
        0,
        size_delta,
        collateral_token,
        wallet_address,
        acceptable_price,
        is_long,
        execution_fee,
        referral_code,
        callback_target
    ).build_transaction({
        'from': wallet_address,
        'value': execution_fee,
        'gas': 800000,
        'gasPrice': web3.to_wei('2', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[+] پوزیشن ارسال شد! Tx Hash: {web3.to_hex(tx_hash)}")