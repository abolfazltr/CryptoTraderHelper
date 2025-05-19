from web3 import Web3
import json
from utils.price import get_current_price
from config.settings import RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS

# Load ABIs
with open("abi/PositionRouter.json") as f:
    position_router_abi = json.load(f)

with open("abi/Vault.json") as f:
    vault_abi = json.load(f)

# Addresses
POSITION_ROUTER = "0xb87a436B93fFE9D75c5cFA7bAcFff96430b09868"
VAULT = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
WETH = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"

def wrap_eth_to_weth(web3, amount_eth):
    weth_contract = web3.eth.contract(address=WETH, abi=[{
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }])
    tx = weth_contract.functions.deposit().build_transaction({
        'from': ACCOUNT_ADDRESS,
        'value': web3.to_wei(amount_eth, 'ether'),
        'nonce': web3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 100000,
        'gasPrice': web3.to_wei('2', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[✓] WETH wrapped | TX: {web3.to_hex(tx_hash)}")

def approve_weth_for_gmx(web3):
    erc20_abi = [{
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    weth = web3.eth.contract(address=WETH, abi=erc20_abi)
    amount = web3.to_wei(1000, 'ether')
    tx = weth.functions.approve(POSITION_ROUTER, amount).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': web3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 100000,
        'gasPrice': web3.to_wei('2', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[✓] WETH approved | TX: {web3.to_hex(tx_hash)}")

def open_position(signal):
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = web3.eth.account.from_key(PRIVATE_KEY)
    position_router = web3.eth.contract(address=POSITION_ROUTER, abi=position_router_abi)

    # Step 1: wrap ETH → WETH
    wrap_eth_to_weth(web3, 0.01)

    # Step 2: approve WETH
    approve_weth_for_gmx(web3)

    # Step 3: open position
    is_long = True if signal == "long" else False
    amount_usd = 20
    leverage = 5
    execution_fee = web3.to_wei("0.0005", "ether")

    price = get_current_price("ETHUSDT")
    acceptable_price = int(price * (1.005 if is_long else 0.995) * 1e30)
    size_delta = int(amount_usd * leverage * 1e30)

    params = [
        [WETH],              # _path
        WETH,                # _indexToken
        int(amount_usd * 1e6),  # _amountIn (بر حسب USDC معادل)
        0,                   # _minOut
        size_delta,          # _sizeDelta
        is_long,             # _isLong
        acceptable_price,    # _acceptablePrice
        execution_fee        # _executionFee
    ]

    tx = position_router.functions.createIncreasePosition(
        *params
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': web3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 800000,
        'gasPrice': web3.to_wei('2', 'gwei'),
        'value': execution_fee
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[✓] Position opened! TX: {web3.to_hex(tx_hash)}")