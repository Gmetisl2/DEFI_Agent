from web3 import Web3
from eth_account import Account
import json
import time
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
clean_WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# Constants
WALLET_ADDRESS = Web3.to_checksum_address(clean_WALLET_ADDRESS)  # Replace with your wallet address
RPC_URL = "https://andromeda.metis.io/?owner=1088"  # Replace with your preferred RPC URL
AAVE_POOL_ADDRESS = Web3.to_checksum_address("0x90df02551bb792286e8d4f13e0e357b4bf1d6a57")  # Pool address
TOKEN_ADDRESSES = {
    "usdc": Web3.to_checksum_address("0xEA32A96608495e54156Ae48931A7c20f0dcc1a21"),
    "usdt": Web3.to_checksum_address("0xbB06DCA3AE6887fAbF931640f67cab3e3a16F4dC"),
    "dai": Web3.to_checksum_address("0x4c078361FC9BbB78DF910800A991C7c3DD2F6ce0")
}
ABI_PATHS = {
    "pool": "./assets/AAVE_LENDING_POOL.ABI",
    "usdc": "./assets/USDC.ABI",
    "usdt": "./assets/USDT.ABI",
    "dai": "./assets/DAI.ABI"
}

# Initialize web3 connection
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Unable to connect to RPC URL")

print(f"Connected to network: {web3.is_connected()}")

# Load ABI from file
def load_abi(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Prepare contracts
pool_abi = load_abi(ABI_PATHS["pool"])
pool_contract = web3.eth.contract(address=Web3.to_checksum_address("0x90df02551bb792286e8d4f13e0e357b4bf1d6a57"), abi=pool_abi)

def approve_token_spend(token, amount):
    """Approve the Aave lending pool to spend tokens."""
    token_address = TOKEN_ADDRESSES[token]
    token_abi = load_abi(ABI_PATHS[token])
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
    gas_price = web3.eth.gas_price
    estimated_gas = 200000

    tx = token_contract.functions.approve(
        pool_contract.address, amount
    ).build_transaction({
        'chainId': 1088,  # Update to your chain ID
        'gas': estimated_gas,
        'gasPrice': gas_price,
        'nonce': nonce
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Approval transaction sent: {tx_hash.hex()}")

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approval transaction confirmed: {receipt.status}")
    return receipt

def perform_action(action, token, amount):
    """Perform the specified action on Aave."""
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
    gas_price = web3.eth.gas_price
    estimated_gas = 300000  # Adjust as needed
    token_address = TOKEN_ADDRESSES[token]

    if action == "lend":
        tx = pool_contract.functions.supply(
            token_address, amount, WALLET_ADDRESS, 0
        ).build_transaction({
            'chainId': 1088,
            'gas': estimated_gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })
    elif action == "borrow":
        tx = pool_contract.functions.borrow(
            token_address, amount, 2, 0, WALLET_ADDRESS
        ).build_transaction({
            'chainId': 1088,
            'gas': estimated_gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })
    elif action == "repay":
        tx = pool_contract.functions.repay(
            token_address, amount, 2, WALLET_ADDRESS
        ).build_transaction({
            'chainId': 1088,
            'gas': estimated_gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })
    else:
        raise ValueError("Invalid action. Please choose 'lend', 'borrow', or 'repay'.")

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"{action.capitalize()} transaction sent: {tx_hash.hex()}")

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"{action.capitalize()} transaction confirmed: {receipt.status}")
    return receipt, tx_hash.hex()


#_____________________________________________________________________________________________________________________
# AGENT DEFINITION
#_____________________________________________________________________________________________________________________

import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CallbackContext,
)
from alith import Agent




def _execute_token_action(action: str, amount: int, token: str) -> str:
    """Helper function to execute token actions (borrow/lend/repay)"""
    if token not in TOKEN_ADDRESSES:
        return "Invalid token. Please choose 'usdc', 'usdt', or 'dai'."

    print(f"Approving {token.upper()} spend...")
    approve_token_spend(token, amount)

    print("Waiting for approval to be processed...")
    time.sleep(5)

    print(f"Performing {action} action with {amount} {token.upper()}...")
    _, tx = perform_action(action, token, amount)

    return (
        "===== Transaction Summary =====\n"
        f"Action: {action.capitalize()}\n"
        f"Token: {token.upper()}\n"
        f"Amount: {amount}\n"
        "==============================\n"
        f"{action.capitalize()} process completed!\n"
        f"Transaction Receipt: https://andromeda-explorer.metis.io/tx/{tx}"
    )

def borrow(amount: int, token: str) -> str:
    """borrow token"""
    return _execute_token_action("borrow", amount, token)

def lend(amount: int, token: str) -> str:
    """lend token"""
    return _execute_token_action("lend", amount, token)

def repay(amount: int, token: str) -> str:
    """repay token"""
    return _execute_token_action("repay", amount, token)

# Initialize Alith Agent
agent = Agent(
    name="Telegram Bot Agent",
    # model="gpt-4",
    model="deepseek-chat",  # or `deepseek-reasoner` for DeepSeek R1 Model
    api_key=deepseek_api_key,  # Replace with your api key or read it from env.
    base_url="api.deepseek.com",
    preamble="""You are an advanced AI assistant that performs lending, borrowing and repaying operations on aave v3 Metis L2 chain""",
    tools=[borrow, lend, repay],
)

# Initialize Telegram Bot
#bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

app = Application.builder().token(bot_token).build()


# Define message handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    # Use the agent to generate a response
    response = agent.prompt(update.message.text)
    # Send the reply back to the Telegram chat
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


# Add handlers to the application
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Start the bot
if __name__ == "__main__":
    app.run_polling()
