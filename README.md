# HyperLiquid MCP Server

A comprehensive Model Context Protocol (MCP) server for HyperLiquid trading using FastMCP. This server provides AI assistants with tools to interact with HyperLiquid's perpetual futures and spot trading platform.

## Features

### Trading Tools

- **Market Orders**: Optimized market opening and closing using HyperLiquid's native functions
- **Limit Orders**: Place limit orders with optional reduce-only and client order ID tracking
- **Bracket Orders**: Create new positions with automatic take profit/stop loss using OCO behavior
- **Order Management**: Cancel orders by ID or client ID, cancel all orders, modify existing orders
- **Position Management**: View positions, close positions (full or partial), get PnL information
- **Advanced TP/SL**: Set take profit and stop loss on existing positions with OCO grouping

### Account Management

- **Balance Information**: Get account balance and margin details
- **Position Tracking**: Monitor all open positions with unrealized PnL
- **Trade History**: Retrieve trade fills and transaction history
- **Leverage Control**: Update leverage settings for different assets
- **Transfers**: Move funds between spot and perpetual accounts

### Market Data

- **Real-time Prices**: Get current market data including bid/ask spreads
- **Order Books**: Retrieve live order book data with configurable depth
- **Funding Rates**: Access historical funding rate information

### Utility Functions

- **Account Summary**: Get comprehensive account overview
- **Dollar Conversion**: Calculate token amounts from dollar values using current prices
- **Position Management**: Dedicated tools for existing position management

## Installation

### Prerequisites

- Python 3.11 or higher (project uses Python 3.13)
- [Poetry](https://python-poetry.org/) package manager

### Setup

1. **Install Poetry (if not already installed):**

   ```bash
   # On macOS and Linux:
   curl -sSL https://install.python-poetry.org | python3 -

   # On Windows:
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

   # Or with pip:
   pip install poetry
   ```

2. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd hyperliquid-mcp-python
   ```

3. **Install dependencies with Poetry:**

   ```bash
   # Install dependencies and create virtual environment
   poetry install

   # Or install without development dependencies
   poetry install --without dev
   ```

   This will install all dependencies defined in `pyproject.toml`:

   - `fastmcp^2.9.2` - FastMCP framework for MCP server
   - `hyperliquid-python-sdk^0.15.0` - Official HyperLiquid SDK
   - `python-dotenv^1.0.0` - Environment variable loading
   - `pydantic^2.0.0` - Data validation
   - `eth-account^0.10.0` - Ethereum account handling

## Configuration

You have three options for configuration:

### Option 1: Environment Variables

Set the following environment variables:

```bash
export HYPERLIQUID_PRIVATE_KEY="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
export HYPERLIQUID_TESTNET="false"  # or "true" for testnet
export HYPERLIQUID_ACCOUNT_ADDRESS="0x..."  # optional, will be derived from private key if not provided
```

### Option 2: .env File

Create a `.env` file in the project root:

```env
HYPERLIQUID_PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
HYPERLIQUID_TESTNET=false
HYPERLIQUID_ACCOUNT_ADDRESS=0x...
```

### Option 3: Configuration File

Create a `config.json` file in the project root:

```json
{
  "private_key": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
  "testnet": false,
  "account_address": "0x..."
}
```

**Important Security Notes:**

- Never commit your private key to version control
- Use testnet for development and testing
- Consider using API wallets for additional security (generate on https://app.hyperliquid.xyz/API)

## Usage

### Starting the Server

```bash
# Using Poetry (recommended)
poetry run python main.py

# Or activate the virtual environment first
poetry shell
python main.py
```

The server will start and display configuration information:

```
HyperLiquid MCP Server starting...
Network: Mainnet
Account: 0x1234567890abcdef1234567890abcdef12345678
Logs will be written to: /path/to/hyperliquid_mcp.log
```

### Available Tools

#### Account Management

1. **`get_account_balance()`**

   - Returns account balance and margin information

2. **`get_open_positions()`**

   - Lists all open positions with PnL data

3. **`get_open_orders()`**

   - Shows all active orders

4. **`get_trade_history(days=7)`**

   - Retrieves recent trade history

5. **`get_account_summary()`**
   - Comprehensive account overview combining balance, positions, and orders

#### Trading - New Positions

1. **`market_open_position(coin, side, size, client_order_id=None)`**

   ```python
   # Example: Open long position for 0.1 BTC at market price
   market_open_position("BTC", "buy", 0.1)

   # Example: Open short position for 1 SOL at market price
   market_open_position("SOL", "sell", 1.0)
   ```

   **Important**: `size` is the number of tokens, NOT dollar value. For $20 worth of SOL at $150/SOL, use size=0.133 (calculated as $20 ÷ $150).

2. **`place_limit_order(coin, side, size, price, reduce_only=False, client_order_id=None)`**

   ```python
   # Example: Buy 0.1 BTC at $45,000
   place_limit_order("BTC", "buy", 0.1, 45000.0)

   # Example: Reduce-only sell order to close position
   place_limit_order("ETH", "sell", 0.5, 3200.0, reduce_only=True)
   ```

3. **`place_bracket_order(coin, side, size, entry_price, take_profit_price, stop_loss_price, client_order_id=None)`**

   ```python
   # Example: Long BTC with TP and SL (creates new position with OCO orders)
   place_bracket_order("BTC", "buy", 0.1, 45000, 47000, 43000)
   ```

   **Note**: Uses `normalTpSl` grouping for proper OCO behavior where TP and SL orders cancel each other.

#### Trading - Position Management

1. **`market_close_position(coin, client_order_id=None)`**

   ```python
   # Close all positions for BTC at market price
   market_close_position("BTC")
   ```

2. **`close_position(coin, percentage=100.0)`**

   ```python
   # Close entire position (uses market_close_position)
   close_position("BTC", 100.0)

   # Note: Partial closure not supported with market orders
   close_position("BTC", 50.0)  # Will return error
   ```

3. **`set_take_profit_stop_loss(coin, take_profit_price=None, stop_loss_price=None, position_size=None)`**

   ```python
   # Set both TP and SL on existing BTC position
   set_take_profit_stop_loss("BTC", take_profit_price=47000, stop_loss_price=43000)

   # Set only take profit
   set_take_profit_stop_loss("ETH", take_profit_price=3200)

   # Set only stop loss
   set_take_profit_stop_loss("SOL", stop_loss_price=140)
   ```

4. **`set_take_profit(coin, take_profit_price, position_size=None)`**

   ```python
   # Set only take profit on existing position
   set_take_profit("BTC", 47000)
   ```

5. **`set_stop_loss(coin, stop_loss_price, position_size=None)`**

   ```python
   # Set only stop loss on existing position
   set_stop_loss("BTC", 43000)
   ```

#### Order Management

1. **`cancel_order(coin, order_id)`**

   ```python
   cancel_order("BTC", 12345)
   ```

2. **`cancel_order_by_client_id(coin, client_order_id)`**

   ```python
   # Cancel using 128-bit hex client order ID
   cancel_order_by_client_id("BTC", "0x1234567890abcdef1234567890abcdef")
   ```

3. **`cancel_all_orders(coin=None)`**

   ```python
   # Cancel all orders for BTC
   cancel_all_orders("BTC")
   # Cancel all orders for all coins
   cancel_all_orders()
   ```

4. **`modify_order(coin, order_id, new_size, new_price)`**

   ```python
   # Modify existing order
   modify_order("BTC", 12345, 0.2, 46000)
   ```

#### Market Data

1. **`get_market_data(coin)`**

   ```python
   get_market_data("BTC")
   ```

   Returns mid price, best bid/ask, sizes, and leverage information.

2. **`get_orderbook(coin, depth=20)`**

   ```python
   get_orderbook("ETH", 10)
   ```

3. **`get_funding_history(coin, days=7)`**
   ```python
   get_funding_history("SOL", 14)
   ```

#### Account Settings

1. **`update_leverage(coin, leverage, cross_margin=True)`**

   ```python
   # Set 10x leverage for BTC with cross margin
   update_leverage("BTC", 10, True)

   # Set 5x leverage for ETH with isolated margin
   update_leverage("ETH", 5, False)
   ```

2. **`transfer_between_spot_and_perp(amount, to_perp=True)`**

   ```python
   # Transfer $1000 from spot to perp
   transfer_between_spot_and_perp(1000.0, True)

   # Transfer $500 from perp to spot
   transfer_between_spot_and_perp(500.0, False)
   ```

#### Utility Tools

1. **`calculate_token_amount_from_dollars(coin, dollar_amount)`**

   ```python
   # Calculate how many SOL tokens $20 can buy
   result = calculate_token_amount_from_dollars("SOL", 20.0)
   # Returns: {"token_amount": 0.133, "current_price": 150.0, "dollar_amount": 20.0}
   ```

   **Use this tool** to convert dollar amounts to token amounts before placing orders.

## Important Notes

### Size Parameters

**Critical**: All `size` parameters represent the **number of tokens**, not dollar values.

- ✅ Correct: `market_open_position("SOL", "buy", 0.133)` for 0.133 SOL tokens
- ❌ Incorrect: `market_open_position("SOL", "buy", 20.0)` thinking this means $20

Use `calculate_token_amount_from_dollars()` to convert dollar amounts to token amounts.

### Client Order IDs

Client Order IDs must be 128-bit hexadecimal strings:

- ✅ Correct: `"0x1234567890abcdef1234567890abcdef"`
- ❌ Incorrect: `"my_order_123"`

### Position vs New Order Management

- **New Positions**: Use `market_open_position()`, `place_limit_order()`, or `place_bracket_order()`
- **Existing Positions**: Use `set_take_profit_stop_loss()`, `market_close_position()`, or reduce-only orders

### OCO Behavior

- **Bracket Orders** (new positions): Use `normalTpSl` grouping where TP and SL cancel each other
- **Position TP/SL** (existing positions): Use `positionTpSl` grouping for proper OCO behavior

## Example Usage Scenarios

### Basic Trading

```python
# Check account status
balance = get_account_balance()
positions = get_open_positions()

# Calculate token amount from dollar value
calc = calculate_token_amount_from_dollars("SOL", 50.0)  # $50 worth of SOL
token_amount = calc["token_amount"]  # e.g., 0.333 SOL

# Open position at market price
order = market_open_position("SOL", "buy", token_amount)

# Set stop loss and take profit on the position
set_take_profit_stop_loss("SOL", take_profit_price=160, stop_loss_price=140)

# Close position when ready
market_close_position("SOL")
```

### Advanced Trading with Risk Management

```python
# Calculate position size from dollar amount
calc = calculate_token_amount_from_dollars("ETH", 100.0)  # $100 worth
size = calc["token_amount"]

# Place bracket order for new position with TP/SL
bracket = place_bracket_order(
    coin="ETH",
    side="buy",
    size=size,
    entry_price=3000,
    take_profit_price=3200,
    stop_loss_price=2900,
    client_order_id="0x" + "1234567890abcdef" * 2  # 128-bit hex
)

# Monitor funding rates
funding = get_funding_history("ETH", 7)
```

### Portfolio Management

```python
# Get complete portfolio overview
summary = get_account_summary()

# Adjust leverage for multiple assets
update_leverage("BTC", 5, True)   # 5x cross margin
update_leverage("ETH", 10, False) # 10x isolated margin

# Rebalance between spot and perp
transfer_between_spot_and_perp(5000, True)  # $5000 spot -> perp

# Set stop losses on all open positions
positions = get_open_positions()
for pos in positions["positions"]:
    coin = pos["coin"]
    entry_price = float(pos["entry_price"])
    stop_price = entry_price * 0.95  # 5% stop loss
    set_stop_loss(coin, stop_price)
```

## Supported Trading Pairs

The server supports all trading pairs available on HyperLiquid, including:

- Major cryptocurrencies: BTC, ETH, SOL, AVAX, etc.
- DeFi tokens: UNI, AAVE, COMP, etc.
- Meme coins: DOGE, SHIB, PEPE, etc.
- And many more...

Use the exact symbol as it appears on HyperLiquid (e.g., "BTC", "ETH", "SOL").

## Error Handling

All tools return structured responses with success indicators:

```json
{
  "success": true,
  "data": { ... },
  "order_details": { ... }
}
```

Or in case of errors:

```json
{
  "success": false,
  "error": "Error description"
}
```

## Logging

The server writes detailed logs to `hyperliquid_mcp.log` in the project directory, including:

- Order placement and execution details
- API interactions and responses
- Error messages and stack traces
- Account operations and transfers

## Security Best Practices

1. **Use Testnet First**: Always test your strategies on testnet before using real funds
2. **API Wallets**: Consider using HyperLiquid's API wallet feature for additional security
3. **Private Key Safety**: Never share your private key or commit it to version control
4. **Environment Variables**: Use environment variables or secure config files for credentials
5. **Monitor Positions**: Always monitor your positions and set appropriate stop losses
6. **Position Sizing**: Use the dollar conversion utility to ensure proper position sizing

## Network Information

- **Mainnet**: Default production environment (`testnet: false`)
- **Testnet**: Set `testnet: true` in config or `HYPERLIQUID_TESTNET=true`
- **Rate Limits**: The server respects HyperLiquid's rate limits automatically

## Troubleshooting

### Common Issues

1. **"Size parameter is dollar value"**: Remember that `size` is always token count, not dollars. Use `calculate_token_amount_from_dollars()` first.

2. **"Invalid client order ID"**: Client order IDs must be 128-bit hex strings starting with "0x".

3. **"Position not found"**: Ensure you have an open position before using position management tools like `set_take_profit_stop_loss()`.

4. **"OCO orders not working"**: New positions use `place_bracket_order()` with `normalTpSl` grouping. Existing positions use `set_take_profit_stop_loss()` with `positionTpSl` grouping.

## Support

For HyperLiquid-specific questions:

- [HyperLiquid Documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [HyperLiquid Discord](https://discord.gg/hyperliquid)

For MCP-related questions:

- [FastMCP Documentation](https://fastmcp.com)
- [Model Context Protocol](https://github.com/anthropics/mcp)

## Disclaimer

This software is for educational and development purposes. Always:

- Test thoroughly on testnet before using real funds
- Understand the risks of leveraged trading
- Never invest more than you can afford to lose
- Be aware of liquidation risks in leveraged positions

Trading cryptocurrencies and derivatives involves substantial risk and may not be suitable for all investors.
