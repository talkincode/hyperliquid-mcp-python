# HyperLiquid MCP Server

A comprehensive Model Context Protocol (MCP) server for HyperLiquid trading using FastMCP. This server provides AI assistants with tools to interact with HyperLiquid's perpetual futures and spot trading platform.

## Features

### Trading Tools

- **Order Management**: Place limit orders, market orders, and bracket orders with take profit/stop loss
- **Order Control**: Cancel orders (by ID or client ID), cancel all orders, modify existing orders
- **Position Management**: View positions, close positions, get PnL information
- **Advanced Trading**: Bracket orders with automatic TP/SL placement

### Account Management

- **Balance Information**: Get account balance and margin details
- **Position Tracking**: Monitor all open positions with unrealized PnL
- **Trade History**: Retrieve trade fills and transaction history
- **Leverage Control**: Update leverage settings for different assets

### Market Data

- **Real-time Prices**: Get current market data for any trading pair
- **Order Books**: Retrieve live order book data with configurable depth
- **Funding Rates**: Access historical funding rate information

### Utility Functions

- **Account Summary**: Get comprehensive account overview
- **Position Closing**: Quick position closing with percentage-based sizing
- **Transfer Tools**: Move funds between spot and perpetual accounts

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd hyperliquid-mcp-python
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or if using the package directly:
   pip install .
   ```

## Configuration

You have two options for configuration:

### Option 1: Environment Variables

Set the following environment variables:

```bash
export HYPERLIQUID_PRIVATE_KEY="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
export HYPERLIQUID_TESTNET="false"  # or "true" for testnet
export HYPERLIQUID_ACCOUNT_ADDRESS="0x..."  # optional, will be derived from private key if not provided
```

### Option 2: Configuration File

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
python main.py
```

The server will start and display configuration information:

```
HyperLiquid MCP Server
Network: Mainnet
Account: 0x1234567890abcdef1234567890abcdef12345678
Starting server...
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
   - Comprehensive account overview

#### Trading

1. **`place_limit_order(coin, side, size, price, reduce_only=False, client_order_id=None)`**

   ```python
   # Example: Buy 0.1 BTC at $45,000
   place_limit_order("BTC", "buy", 0.1, 45000.0)
   ```

2. **`place_market_order(coin, side, size, reduce_only=False, client_order_id=None)`**

   ```python
   # Example: Sell 0.1 ETH at market price
   place_market_order("ETH", "sell", 0.1)
   ```

3. **`place_bracket_order(coin, side, size, entry_price, take_profit_price, stop_loss_price, client_order_id=None)`**

   ```python
   # Example: Long BTC with TP and SL
   place_bracket_order("BTC", "buy", 0.1, 45000, 47000, 43000)
   ```

4. **`cancel_order(coin, order_id)`**

   ```python
   cancel_order("BTC", 12345)
   ```

5. **`cancel_all_orders(coin=None)`**

   ```python
   # Cancel all orders for BTC
   cancel_all_orders("BTC")
   # Cancel all orders for all coins
   cancel_all_orders()
   ```

6. **`close_position(coin, percentage=100.0)`**
   ```python
   # Close 50% of BTC position
   close_position("BTC", 50.0)
   ```

#### Market Data

1. **`get_market_data(coin)`**

   ```python
   get_market_data("BTC")
   ```

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
   # Set 10x leverage for BTC
   update_leverage("BTC", 10, True)
   ```

2. **`transfer_between_spot_and_perp(amount, to_perp=True)`**
   ```python
   # Transfer $1000 from spot to perp
   transfer_between_spot_and_perp(1000.0, True)
   ```

## Example Usage Scenarios

### Basic Trading

```python
# Check account status
balance = get_account_balance()
positions = get_open_positions()

# Place a limit order
order = place_limit_order("BTC", "buy", 0.1, 45000)

# Monitor and close position
summary = get_account_summary()
close_position("BTC", 100.0)  # Close entire position
```

### Advanced Trading with Risk Management

```python
# Place bracket order with stop loss and take profit
bracket = place_bracket_order(
    coin="ETH",
    side="buy",
    size=1.0,
    entry_price=3000,
    take_profit_price=3200,
    stop_loss_price=2900
)

# Monitor funding rates
funding = get_funding_history("ETH", 7)
```

### Portfolio Management

```python
# Get complete portfolio overview
summary = get_account_summary()

# Adjust leverage for multiple assets
update_leverage("BTC", 5)
update_leverage("ETH", 10)

# Rebalance between spot and perp
transfer_between_spot_and_perp(5000, True)
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

## Security Best Practices

1. **Use Testnet First**: Always test your strategies on testnet before using real funds
2. **API Wallets**: Consider using HyperLiquid's API wallet feature for additional security
3. **Private Key Safety**: Never share your private key or commit it to version control
4. **Environment Variables**: Use environment variables or secure config files for credentials
5. **Monitor Positions**: Always monitor your positions and set appropriate stop losses

## Network Information

- **Mainnet**: Default production environment
- **Testnet**: Set `testnet: true` in config or `HYPERLIQUID_TESTNET=true`
- **Rate Limits**: The server respects HyperLiquid's rate limits automatically

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
