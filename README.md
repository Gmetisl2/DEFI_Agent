# DEFI_Agent Documentation
![image](https://github.com/user-attachments/assets/21a4d8ff-6bd3-456a-81cd-1a2a463b6e66)

## Business Logic

The `DEFI_Agent` script is designed to streamline decentralized finance (DeFi) operations on the Aave V3 protocol deployed on the Metis Layer 2 blockchain. It provides an automated interface for lending, borrowing, and repaying tokens via a Telegram bot. The script integrates with the Aave protocol and uses the Alith framework to enable seamless interaction with users.

**THIS PROJECT IS BARELY A POC NOT A FINAL PRODUCT**
The current features are only showcasing the possibilities and expanded by contributors "


### Key Features:
1. **Lending**: Users can supply tokens (e.g., USDC, USDT, DAI) to the Aave lending pool to earn interest.
2. **Borrowing**: Users can borrow tokens from the Aave lending pool by providing collateral.
3. **Repayment**: Users can repay borrowed tokens to the Aave lending pool.
4. **Telegram Bot Integration**: Users interact with the system through a Telegram bot, which processes commands and executes transactions.
5. **Secure Transactions**: The script uses private keys securely loaded from environment variables to sign and send transactions.

### Workflow:
1. **User Interaction**: Users send commands (e.g., "lend 100 usdc") to the Telegram bot.
2. **Approval Process**: The script approves the Aave lending pool to spend the specified token amount.
3. **Transaction Execution**: The script performs the requested action (lend, borrow, or repay) on the Aave protocol.
4. **Feedback**: The bot provides a transaction summary and a link to the transaction receipt on the Metis blockchain explorer.

---

## Technical Architecture

### Components:
1. **Environment Variables**:
   - `DEEPSEEK_API_KEY`: API key for the Alith framework.
   - `TELEGRAM_BOT_TOKEN`: Token for the Telegram bot.
   - `PRIVATE_KEY`: Private key for signing transactions.
   - `WALLET_ADDRESS`: Wallet address for executing transactions.

2. **Web3 Integration**:
   - The script uses the `web3` library to interact with the Metis blockchain.
   - It connects to the Metis RPC URL (`https://andromeda.metis.io/?owner=1088`) to send transactions.

3. **Aave Protocol Integration**:
   - The script interacts with the Aave V3 lending pool using its ABI and contract address.
   - Supported tokens (USDC, USDT, DAI) are defined with their respective contract addresses and ABIs.

4. **Telegram Bot**:
   - Built using the `python-telegram-bot` library.
   - Listens for user messages and processes commands using the Alith Agent.

5. **Alith Agent**:
   - The Alith framework is used to process user inputs and execute predefined tools (`borrow`, `lend`, `repay`).
   - The agent is configured with a preamble describing its purpose and functionality.

### Code Structure:
- **Environment Setup**:
  - Loads environment variables using `dotenv`.
  - Initializes Web3 connection and validates connectivity.

- **ABI Loading**:
  - Reads ABI files from the `assets` directory to interact with smart contracts.

- **Token Approval**:
  - Approves the Aave lending pool to spend tokens on behalf of the user.

- **Transaction Execution**:
  - Builds and signs transactions for lending, borrowing, and repaying tokens.
  - Sends transactions to the blockchain and waits for confirmation.

- **Telegram Bot**:
  - Handles user messages and forwards them to the Alith Agent for processing.
  - Sends responses back to the user with transaction details.

### Directory Structure
```
DEFI_Agent/
│
├── Agent.py           # Main script with bot and protocol logic
├── .env              # Environment variables configuration
│
├── assets/           # Smart contract ABIs
│   ├── AAVE_LENDING_POOL.ABI
│   ├── USDC.ABI
│   ├── USDT.ABI
│   └── DAI.ABI
│
├── llm_logs/         # Debug and transaction logs
├── LICENSE           # MIT License file
└── README.md         # Project documentation
```


### Key Functions:
1. **`approve_token_spend(token, amount)`**:
   - Approves the Aave lending pool to spend a specified amount of a token.

2. **`perform_action(action, token, amount)`**:
   - Executes a lending, borrowing, or repayment action on the Aave protocol.

3. **`_execute_token_action(action, amount, token)`**:
   - Helper function to handle the approval and execution of token actions.

4. **Telegram Bot Handlers**:
   - `handle_message(update, context)`: Processes user messages and sends responses.

---

## Usage

1. **Setup**:
   - Create a `.env` file with the required environment variables.
   - Ensure the ABI files are present in the `assets` directory.

2. **Run the Script**:
   - Execute `Agent.py` to start the Telegram bot.

3. **Interact with the Bot**:
   - Send commands like `lend 100 usdc`, `borrow 50 dai`, or `repay 20 usdt` to the bot.

4. **Monitor Transactions**:
   - Check the transaction receipt link provided by the bot to verify the transaction on the Metis blockchain.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
