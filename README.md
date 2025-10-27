# HyperLiquid MCP Server

基于 FastMCP 的 HyperLiquid 交易 MCP 服务器。为 AI 助手提供与 HyperLiquid 永续合约和现货交易平台交互的工具。

> **致谢**: 本项目 Fork 自 [GigabrainGG/hyperliquid-mcp](https://github.com/GigabrainGG/hyperliquid-mcp)，感谢原作者的出色工作！

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

### 方式 1：使用 uvx（推荐）🚀

**最简单的方式** - 无需安装，直接运行：

```bash
# 查看帮助
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp --help

# 启动 HTTP 服务器
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp start

# 启动 stdio 服务器（用于 MCP 客户端）
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp stdio
```

> **为什么要指定 `--python 3.13`?**  
> 依赖包 `ckzg` 目前只提供到 Python 3.13 的预编译包，Python 3.14 还不支持。指定版本可以避免编译错误。

### 方式 2：本地开发安装

```bash
# 克隆仓库
git clone https://github.com/talkincode/hyperliquid-mcp-python.git
cd hyperliquid-mcp-python

# 安装依赖（uv 会自动处理编译）
uv sync

# 配置
cp .env.example .env  # 然后编辑 .env 文件
# 或设置环境变量
export HYPERLIQUID_PRIVATE_KEY="0x..."
export HYPERLIQUID_TESTNET="true"  # 强烈建议先用测试网！

# 运行
uv run hyperliquid-mcp              # HTTP 模式（默认 127.0.0.1:8080）
uv run hyperliquid-mcp stdio        # stdio 模式（用于 MCP 客户端）
uv run hyperliquid-mcp --help       # 查看帮助
```

### 方式 3：pip 安装（需要 Python 3.10-3.13）

```bash
# 使用 pip（需要 Python 3.10-3.13）
pip install hyperliquid-mcp-python

# 运行
hyperliquid-mcp --help
```

> **注意**: 包要求 Python 3.10-3.13。Python 3.14 还不支持。

## 配置

创建 `.env` 文件或设置环境变量：

```bash
HYPERLIQUID_PRIVATE_KEY=0x...  # 必填
HYPERLIQUID_TESTNET=true       # 可选，默认: false
HYPERLIQUID_ACCOUNT_ADDRESS=   # 可选，自动从私钥派生
```

⚠️ **安全提示**：绝不提交 `.env` 文件。先用测试网。建议使用 API 钱包 https://app.hyperliquid.xyz/API

## 使用方法

### 方式 1：使用 Makefile（推荐）⭐

```bash
# 查看所有可用命令
make help

# 安装依赖
make install

# 查看配置
make config

# 快速验证（连接+余额+地址）
make test-quick

# 启动 HTTP 服务器
make run-http

# 启动 stdio 服务器（用于 MCP 客户端）
make run-stdio
```

### 方式 2：直接使用命令

```bash
# 已安装的包（推荐）
hyperliquid-mcp                # HTTP 服务器（默认）
hyperliquid-mcp stdio          # stdio 模式（用于 MCP 客户端）
hyperliquid-mcp --help         # 显示帮助

# 本地开发
uv run hyperliquid-mcp
uv run hyperliquid-mcp stdio
```

### MCP 客户端集成 (Claude Desktop)

添加到 `~/Library/Application Support/Claude/claude_desktop_config.json`：

**推荐配置（本地安装）**

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/hyperliquid-mcp",
        "run",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x...",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

**如果全局安装成功**

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "hyperliquid-mcp",
      "args": ["stdio"],
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

## 测试工具

项目包含一套完整的测试脚本，帮助你验证配置和快速上手。

### 使用 Makefile（推荐）⭐

```bash
# 运行所有只读测试
make test-all

# 快速验证
make test-quick

# 运行特定测试
make test-market      # 市场数据测试
make test-account     # 账户信息测试
make test-balance     # 余额检查
make test-orderbook   # 订单簿测试
make test-funding     # 资金费率历史
make test-calculator  # 价格计算器
make test-address     # 地址验证

# 列出所有可用测试
make list-tests

# 查看测试帮助
make test-help
```

### 手动运行测试

```bash
# 基础连接测试
uv run python test_scripts/test_connection.py

# 检查所有账户余额（现货 + 合约）
uv run python test_scripts/check_all_balances.py

# 交互式测试工具（推荐）⭐
uv run python test_scripts/interactive_test.py

# 或使用测试套件脚本
./test_scripts/run_tests.sh all
```

更多测试工具和详细说明，请查看 [test_scripts/README.md](test_scripts/README.md)

## 故障排除

- **Size 参数**：使用代币数量，不是美元。用 `calculate_token_amount_from_dollars()` 转换
- **客户端订单 ID**：必须是 128 位十六进制字符串（如 `0x1234...`）
- **未找到仓位**：设置止盈止损前确保仓位存在
- **网络**：先用测试网：`HYPERLIQUID_TESTNET=true`
- **余额为 0**：运行 `uv run python test_scripts/check_address.py` 验证地址配置
- **API 钱包**：如使用 API 钱包，需在 `.env` 中设置 `HYPERLIQUID_ACCOUNT_ADDRESS` 为主账号地址

## 相关链接

- [HyperLiquid 文档](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [FastMCP](https://fastmcp.com)
- [MCP 协议](https://github.com/anthropics/mcp)

## 免责声明

仅供学习使用。先在测试网测试。加密货币交易涉及重大风险。
