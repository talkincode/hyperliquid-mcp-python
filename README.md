# HyperLiquid MCP Server

基于 FastMCP 的 HyperLiquid 交易 MCP 服务器。为 AI 助手提供与 HyperLiquid 永续合约和现货交易平台交互的工具。

## 功能特性

### 交易工具

- **市价订单**：使用 HyperLiquid 原生函数优化的开仓和平仓
- **限价订单**：支持 reduce-only 和自定义订单 ID 追踪
- **括号订单**：一键创建带止盈止损的新仓位（OCO 行为）
- **订单管理**：按 ID 或客户端 ID 取消订单、批量取消、修改订单
- **仓位管理**：查看仓位、平仓（全部或部分）、获取盈亏信息
- **高级止盈止损**：为现有仓位设置 OCO 止盈止损

### 账户管理

- **余额信息**：获取账户余额和保证金详情
- **仓位跟踪**：监控所有开仓及未实现盈亏
- **交易历史**：查询成交记录和交易历史
- **杠杆控制**：为不同资产更新杠杆设置
- **资金划转**：在现货和合约账户间转移资金

### 市场数据

- **实时价格**：获取当前市场数据，包括买卖价差
- **订单簿**：获取可配置深度的实时订单簿数据
- **资金费率**：访问历史资金费率信息

### 实用工具

- **账户总览**：获取账户综合概览
- **美元转换**：根据当前价格计算代币数量
- **仓位管理**：专用的现有仓位管理工具

## 快速开始

### 方式 1: 无需安装直接试用 (uvx)

```bash
# 设置配置
export HYPERLIQUID_PRIVATE_KEY="0x..."
export HYPERLIQUID_TESTNET="true"  # 先用测试网！

# 直接从 GitHub 运行
uvx --from git+https://github.com/jamiesun/hyperliquid-mcp.git hyperliquid-mcp
```

### 方式 2: 本地开发

```bash
# 安装 uv（如需要）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆并设置
git clone <repository-url>
cd hyperliquid-mcp
uv sync

# 配置（复制并编辑 .env.example 为 .env）
cp .env.example .env

# 运行
uv run hyperliquid-mcp
```

### 方式 3: 全局安装

```bash
uv pip install git+https://github.com/jamiesun/hyperliquid-mcp.git
hyperliquid-mcp
```

## 配置

创建 `.env` 文件或设置环境变量：

```bash
HYPERLIQUID_PRIVATE_KEY=0x...  # 必填
HYPERLIQUID_TESTNET=true       # 可选，默认: false
HYPERLIQUID_ACCOUNT_ADDRESS=   # 可选，自动从私钥派生
```

⚠️ **安全提示**：绝不提交 `.env` 文件。先用测试网。建议使用 API 钱包 https://app.hyperliquid.xyz/API
## 使用方法

```bash
# 本地开发
uv run hyperliquid-mcp              # HTTP 服务器（默认）
uv run hyperliquid-mcp stdio        # stdio 模式（用于 MCP 客户端）
uv run hyperliquid-mcp --help       # 显示帮助

# 远程执行（无需安装）
uvx --from git+https://github.com/jamiesun/hyperliquid-mcp.git hyperliquid-mcp

# 全局安装后
hyperliquid-mcp
```

### MCP 客户端集成 (Claude Desktop)

添加到 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uv",
      "args": ["--directory", "/path/to/hyperliquid-mcp", "run", "hyperliquid-mcp", "stdio"],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x...",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

The server will start and display configuration information:

```
HyperLiquid MCP Server starting...
Network: Mainnet
Account: 0x1234567890abcdef1234567890abcdef12345678
Logs will be written to: /path/to/hyperliquid_mcp.log
```

## 可用工具

### 快速示例

```python
# 账户信息
get_account_balance()
get_open_positions()
get_account_summary()

# 交易 - 新仓位
market_open_position("BTC", "buy", 0.1)              # 市价单
place_limit_order("BTC", "buy", 0.1, 45000)          # 限价单
place_bracket_order("BTC", "buy", 0.1, 45000, 47000, 43000)  # 入场 + 止盈止损

# 交易 - 管理现有仓位
market_close_position("BTC")                         # 平仓
set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)  # 设置止盈止损

# 订单管理
cancel_order("BTC", order_id)
cancel_all_orders("BTC")

# 市场数据
get_market_data("BTC")
get_orderbook("BTC", depth=20)

# 实用工具
calculate_token_amount_from_dollars("SOL", 20.0)    # 将 $20 转换为 SOL 代币数量
update_leverage("BTC", 10, cross_margin=True)
```

⚠️ **重要**：`size` 参数是**代币数量**，不是美元金额！
- ✅ 正确：`market_open_position("SOL", "buy", 0.133)`  # 0.133 个 SOL 代币
- ❌ 错误：`market_open_position("SOL", "buy", 20.0)` 误以为是 $20

使用 `calculate_token_amount_from_dollars()` 将美元转换为代币数量。

## 常见用例

```python
# 基础交易流程
calc = calculate_token_amount_from_dollars("SOL", 50.0)  # 将 $50 转换为代币
market_open_position("SOL", "buy", calc["token_amount"])  # 开仓
set_take_profit_stop_loss("SOL", tp_price=160, sl_price=140)  # 设置止盈止损
market_close_position("SOL")  # 准备好时平仓

# 括号订单（一键入场 + 止盈止损）
calc = calculate_token_amount_from_dollars("ETH", 100.0)
place_bracket_order("ETH", "buy", calc["token_amount"], 3000, 3200, 2900)

# 投资组合管理
summary = get_account_summary()
update_leverage("BTC", 5, True)
transfer_between_spot_and_perp(5000, True)
```

## 返回格式

所有工具返回标准化响应：

```json
{"success": true, "data": {...}}      // 成功
{"success": false, "error": "..."}    // 错误
```

日志写入 `hyperliquid_mcp.log`。

## 故障排除

- **Size 参数**：使用代币数量，不是美元。用 `calculate_token_amount_from_dollars()` 转换
- **客户端订单 ID**：必须是 128 位十六进制字符串（如 `0x1234...`）
- **未找到仓位**：设置止盈止损前确保仓位存在
- **网络**：先用测试网：`HYPERLIQUID_TESTNET=true`

## 相关链接

- [HyperLiquid 文档](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [FastMCP](https://fastmcp.com)
- [MCP 协议](https://github.com/anthropics/mcp)

## 免责声明

仅供学习使用。先在测试网测试。加密货币交易涉及重大风险。
