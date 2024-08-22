from web3 import Web3
import json
import time

# Connect to the local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set the default account
w3.eth.default_account = w3.eth.accounts[0]

# Load the contract ABI
with open('build/contracts/SimpleBank.json') as f:
    abi = json.load(f)['abi']

# Get the contract instance
contract = w3.eth.contract(address="0x1eEa0d6728835F4FC605CA253d6daBFe6aBfAc61", abi=abi)
print(w3.eth.accounts[0])

# tx_hash = contract.functions.enroll(w3.eth.accounts[0], "Kumar").transact()
# print(f"Transaction sent: {tx_hash.hex()}")
# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(f"Transaction confirmed in block: {receipt.blockNumber}")