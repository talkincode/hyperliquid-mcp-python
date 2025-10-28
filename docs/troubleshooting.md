# 故障排除

本页面列出了常见问题及解决方案。

## 安装问题

### Python 版本不兼容

**问题**：使用 Python 3.14 时出现编译错误

**原因**：依赖包 `ckzg` 尚未提供 Python 3.14 预编译包

**解决方案**：

```bash
# 使用 Python 3.13
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp

# 或使用 pyenv 切换版本
pyenv install 3.13
pyenv local 3.13
```

### 命令未找到

**问题**：`hyperliquid-mcp: command not found`

**解决方案**：

```bash
# 检查是否已安装
pip show hyperliquid-mcp-python

# 使用完整路径
python -m cli

# 或使用 uvx
uvx --from hyperliquid-mcp-python hyperliquid-mcp
```

## 配置问题

### 私钥格式错误

**问题**：`Invalid private key format`

**解决方案**：

- 确保私钥以 `0x` 开头
- 私钥长度为 66 个字符（含 `0x`）
- 示例：`0x1234...abcd`（64 个十六进制字符 + `0x`）

### 找不到配置文件

**问题**：`Configuration file not found`

**解决方案**：

```bash
# 确保 .env 在项目根目录
ls -la .env

# 或使用环境变量
export HYPERLIQUID_PRIVATE_KEY="0x..."
```

### API 钱包配置

**问题**：使用 API 钱包时无法操作

**解决方案**：

```bash
# 必须同时设置账户地址
HYPERLIQUID_PRIVATE_KEY=0x...      # API 钱包私钥
HYPERLIQUID_ACCOUNT_ADDRESS=0x...  # 主账户地址
```

## 连接问题

### 连接超时

**问题**：`Connection timeout`

**解决方案**：

1. 检查网络连接
2. 确认防火墙设置
3. 尝试更换网络
4. 检查 HyperLiquid API 状态

### 认证失败

**问题**：`Authentication failed`

**解决方案**：

1. 验证私钥正确性
2. 确认网络配置（测试网/主网）
3. 检查账户地址设置
4. 重新生成 API 钱包

## 交易问题

### Size 参数错误

**问题**：订单大小不符合预期

**原因**：**`size` 参数表示代币数量，不是美元金额！**

**示例**：

```python
# ❌ 错误 - 这会尝试购买 20 个 SOL 代币，而非 $20
market_open_position("SOL", "buy", 20.0)

# ✅ 正确 - 先转换美元到代币数量
calc = calculate_token_amount_from_dollars("SOL", 20.0)
market_open_position("SOL", "buy", calc["token_amount"])
```

### 订单被拒绝

**问题**：`Order rejected`

**可能原因**：

1. 余额不足
2. 订单大小低于最小值
3. 价格偏离市场价过大
4. 杠杆设置不当

**解决方案**：

```bash
# 检查余额
make test-balance

# 查看市场数据
uv run python test_scripts/test_market_data.py

# 调整杠杆
update_leverage("BTC", 5, True)
```

### 找不到仓位

**问题**：`Position not found`

**原因**：尝试对不存在的仓位设置止盈止损

**解决方案**：

```python
# 先检查是否有仓位
positions = get_open_positions()

# 确认仓位存在后再设置 TP/SL
if positions["data"]:
    set_take_profit_stop_loss("BTC", tp_price=50000, sl_price=45000)
```

### OCO 订单组行为

**问题**：止盈止损订单未正确关联

**解决方案**：

- **新仓位**：使用 `place_bracket_order()` 创建带 TP/SL 的入场订单
- **现有仓位**：使用 `set_take_profit_stop_loss()` 为已有仓位设置 TP/SL

```python
# ✅ 新仓位 - 使用 bracket 订单
place_bracket_order("BTC", "buy", 0.1, 45000, 47000, 43000)

# ✅ 现有仓位 - 使用专用函数
set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)
```

## 测试问题

### 测试脚本运行失败

**问题**：无法运行测试脚本

**解决方案**：

```bash
# 确保在项目根目录
cd /path/to/hyperliquid-mcp-python

# 使用 uv 运行
uv run python test_scripts/test_connection.py

# 或使用 Makefile
make test-quick
```

### 测试网余额为 0

**问题**：测试网账户无余额

**解决方案**：

1. 访问 HyperLiquid 测试网
2. 申请测试 USDC
3. 等待几分钟后再测试

## MCP 客户端集成问题

### Claude Desktop 无法连接

**问题**：Claude Desktop 显示服务器离线

**解决方案**：

```json
// 检查 config.json 路径
// ~/Library/Application Support/Claude/claude_desktop_config.json

{
  "mcpServers": {
    "hyperliquid": {
      "command": "uv",
      "args": [
        "--directory",
        "/完整/绝对/路径/hyperliquid-mcp",
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

### 日志查看

**查看服务器日志**：

```bash
# 主日志文件
tail -f hyperliquid_mcp.log

# Claude Desktop 日志
tail -f ~/Library/Logs/Claude/mcp*.log
```

## 性能问题

### 响应缓慢

**可能原因**：

1. 网络延迟
2. API 限流
3. 订单簿深度过大

**解决方案**：

```python
# 减少订单簿深度
get_orderbook("BTC", depth=10)  # 而非 100

# 使用缓存的市场数据
# 避免频繁调用 API
```

## 错误日志分析

### 启用详细日志

```python
# 在 main.py 中
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 常见错误代码

| 错误信息               | 原因       | 解决方案           |
| ---------------------- | ---------- | ------------------ |
| `Invalid signature`    | 私钥错误   | 检查私钥配置       |
| `Insufficient balance` | 余额不足   | 充值或减少订单大小 |
| `Order size too small` | 订单太小   | 增加订单大小       |
| `Rate limit exceeded`  | API 限流   | 减少请求频率       |
| `Position not found`   | 仓位不存在 | 先开仓再操作       |

## 获取帮助

如果以上方案无法解决问题：

1. **查看日志**：`hyperliquid_mcp.log`
2. **运行诊断**：`make test-all`
3. **提交 Issue**：[GitHub Issues](https://github.com/talkincode/hyperliquid-mcp-python/issues)
4. **查看文档**：[完整文档](https://talkincode.github.io/hyperliquid-mcp-python/)

## 诊断清单

运行完整诊断：

```bash
# 1. 检查配置
make config

# 2. 测试连接
make test-quick

# 3. 检查余额
make test-balance

# 4. 测试市场数据
make test-market

# 5. 查看日志
tail -f hyperliquid_mcp.log
```

## 常见误区

### ❌ 错误理解

1. **Size 是美元金额** → Size 是代币数量
2. **可以直接修改 TP/SL** → 需要取消重新下单
3. **测试网和主网通用** → 需要分别配置
4. **API 钱包可以独立使用** → 需要主账户地址

### ✅ 正确理解

1. 使用 `calculate_token_amount_from_dollars()` 转换
2. 使用专用的 TP/SL 管理函数
3. 明确设置 `HYPERLIQUID_TESTNET`
4. API 钱包需配合主账户地址使用
