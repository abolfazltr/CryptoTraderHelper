import json
from web3 import Web3
from config.settings import RPC_URL, ACCOUNT_ADDRESS, PRIVATE_KEY
from utils.helpers import load_abi

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.to_checksum_address(ACCOUNT_ADDRESS)

vault_abi = load_abi("abi/Vault.json")
router_abi = load_abi("abi/PositionRouter.json")
manager_abi = load_abi("abi/PositionManager.json")

VAULT = w3.to_checksum_address("0x489ee077994B6658eAfA855C308275EAd8097C4A")
POSITION_ROUTER = w3.to_checksum_address("0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868")
POSITION_MANAGER = w3.to_checksum_address("0xB70B10361dD3C8E3B4B1C1f476233c37E3B2877D")

vault = w3.eth.contract(address=VAULT, abi=vault_abi)
router = w3.eth.contract(address=POSITION_ROUTER, abi=router_abi)
manager = w3.eth.contract(address=POSITION_MANAGER, abi=manager_abi)

WETH = w3.to_checksum_address("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
LINK = w3.to_checksum_address("0xFf970A61A04b1cA14834A43f5dE4533eBDDB5CC8")

def set_tp_sl(path, index_token, is_long, size_delta, tp_price, sl_price):
    print("⚙️ در حال تنظیم TP و SL واقعی در GMX V2...")

    tx = manager.functions.updateOrder(
        account,
        path,
        index_token,
        size_delta,
        is_long,
        tp_price,
        sl_price
    ).build_transaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 800000,
        'gasPrice': w3.to_wei('1.5', 'gwei')
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("✅ TX تنظیم TP و SL:", tx_hash.hex())
    return tx_hash.hex()