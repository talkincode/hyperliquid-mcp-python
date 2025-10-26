# HyperLiquid MCP Agent 操作指南

## 概述

这是一个为AI代理设计的HyperLiquid交易MCP服务器操作指南。本文档提供了详细的工具使用说明、最佳实践和常见场景的处理方法。

## 快速开始

### 环境配置

1. **配置私钥和网络**：
```bash
# 方式1：环境变量
export HYPERLIQUID_PRIVATE_KEY="0x..."
export HYPERLIQUID_TESTNET="true"  # 建议先用测试网
export HYPERLIQUID_ACCOUNT_ADDRESS="0x..."  # 可选

# 方式2：创建 .env 文件
echo 'HYPERLIQUID_PRIVATE_KEY=0x...' > .env
echo 'HYPERLIQUID_TESTNET=true' >> .env

# 方式3：创建 config.json
echo '{"private_key": "0x...", "testnet": true}' > config.json
```

2. **启动服务器**：
```bash
# HTTP模式（推荐）
poetry start

# Stdio模式（MCP客户端）
poetry stdio
```

## 核心工具使用指南

### 账户管理

#### 获取账户概览
```python
# 获取完整账户信息
summary = await get_account_summary()
# 返回：余额、仓位、订单的综合信息

# 单独获取信息
balance = await get_account_balance()
positions = await get_open_positions()
orders = await get_open_orders()
```

#### 查看交易历史
```python
# 获取最近7天交易记录
trades = await get_trade_history(7)

# 获取更长期历史
trades = await get_trade_history(30)
```

### 交易操作

#### 🚨 重要：订单大小计算
**关键点**：所有交易函数的 `size` 参数表示**代币数量**，不是美元金额！

```python
# ❌ 错误做法
market_open_position("SOL", "buy", 100)  # 这不是$100，而是100个SOL！

# ✅ 正确做法
# 1. 先计算代币数量
calc = await calculate_token_amount_from_dollars("SOL", 100)  # $100美元
token_amount = calc["token_amount"]  # 例如：0.667 SOL

# 2. 再下单
market_open_position("SOL", "buy", token_amount)
```

#### 开仓操作

**市价开仓**（推荐用于快速执行）：
```python
# 计算代币数量
calc = await calculate_token_amount_from_dollars("BTC", 1000)  # $1000美元
size = calc["token_amount"]

# 开多仓
result = await market_open_position("BTC", "buy", size)

# 开空仓
result = await market_open_position("BTC", "sell", size)
```

**限价开仓**：
```python
# 限价买入
result = await place_limit_order(
    coin="ETH",
    side="buy", 
    size=0.5,  # 0.5个ETH
    price=3000.0,  # $3000每个ETH
    reduce_only=False
)
```

**带止盈止损的开仓**：
```python
# 使用括号订单（推荐用于新仓位）
result = await place_bracket_order(
    coin="SOL",
    side="buy",
    size=1.0,  # 1个SOL
    entry_price=150.0,  # 入场价格
    take_profit_price=180.0,  # 止盈价格
    stop_loss_price=130.0   # 止损价格
)
```

#### 平仓操作

**全仓平仓**（推荐）：
```python
# 平掉所有BTC仓位
result = await market_close_position("BTC")

# 或使用通用平仓工具
result = await close_position("BTC", 100.0)  # 100%平仓
```

**限价平仓**：
```python
# 使用reduce_only限价单
result = await place_limit_order(
    coin="ETH",
    side="sell",  # 平多仓用sell，平空仓用buy
    size=0.5,
    price=3200.0,
    reduce_only=True  # 关键：只能平仓，不能开新仓
)
```

#### 为现有仓位设置止盈止损

```python
# 为现有BTC仓位设置止盈止损
result = await set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=47000.0,
    stop_loss_price=43000.0
)

# 只设置止盈
result = await set_take_profit("BTC", 47000.0)

# 只设置止损
result = await set_stop_loss("BTC", 43000.0)
```

### 订单管理

#### 取消订单
```python
# 通过订单ID取消
await cancel_order("BTC", 12345)

# 通过客户端订单ID取消
await cancel_order_by_client_id("BTC", "0x1234567890abcdef1234567890abcdef")

# 取消所有BTC订单
await cancel_all_orders("BTC")

# 取消所有订单
await cancel_all_orders()
```

#### 修改订单
```python
# 修改现有订单的价格和数量
await modify_order(
    coin="ETH",
    order_id=12345,
    new_size=1.0,
    new_price=3100.0
)
```

### 市场数据

#### 获取价格信息
```python
# 获取市场数据
market_data = await get_market_data("BTC")
# 包含：中间价、最佳买卖价、杠杆信息等

# 获取订单簿
orderbook = await get_orderbook("ETH", depth=10)

# 获取资金费率历史
funding = await get_funding_history("SOL", days=14)
```

### 账户设置

#### 调整杠杆
```python
# 设置BTC为10倍全仓杠杆
await update_leverage("BTC", 10, cross_margin=True)

# 设置ETH为5倍逐仓杠杆
await update_leverage("ETH", 5, cross_margin=False)
```

#### 资金转账
```python
# 从现货转到合约账户
await transfer_between_spot_and_perp(1000.0, to_perp=True)

# 从合约转到现货账户
await transfer_between_spot_and_perp(500.0, to_perp=False)
```

## 常见交易场景

### 场景1：简单的多空交易
```python
# 1. 检查账户状态
balance = await get_account_balance()
print(f"可用余额: {balance['data']['marginSummary']['accountValue']}")

# 2. 计算仓位大小（$500美元的SOL）
calc = await calculate_token_amount_from_dollars("SOL", 500)
size = calc["token_amount"]

# 3. 开多仓
long_result = await market_open_position("SOL", "buy", size)

# 4. 设置止盈止损
await set_take_profit_stop_loss(
    coin="SOL",
    take_profit_price=calc["current_price"] * 1.1,  # 10%止盈
    stop_loss_price=calc["current_price"] * 0.95    # 5%止损
)

# 5. 监控仓位
positions = await get_open_positions()
```

### 场景2：网格交易策略
```python
# 设置多个限价单形成网格
base_price = 150.0  # SOL基准价格
grid_levels = 5
grid_spacing = 0.02  # 2%间距
order_size = 0.1  # 每格0.1 SOL

for i in range(grid_levels):
    # 买入订单（低于市价）
    buy_price = base_price * (1 - (i + 1) * grid_spacing)
    await place_limit_order("SOL", "buy", order_size, buy_price)
    
    # 卖出订单（高于市价）
    sell_price = base_price * (1 + (i + 1) * grid_spacing)
    await place_limit_order("SOL", "sell", order_size, sell_price)
```

### 场景3：DCA定投策略
```python
import asyncio

async def dca_strategy(coin, dollar_amount, interval_hours):
    """定投策略：定期投入固定美元金额"""
    while True:
        try:
            # 计算当前价格下的代币数量
            calc = await calculate_token_amount_from_dollars(coin, dollar_amount)
            
            # 市价买入
            result = await market_open_position(coin, "buy", calc["token_amount"])
            
            print(f"DCA买入: {calc['token_amount']:.4f} {coin} @ ${calc['current_price']:.2f}")
            
            # 等待下次执行
            await asyncio.sleep(interval_hours * 3600)
            
        except Exception as e:
            print(f"DCA策略错误: {e}")
            await asyncio.sleep(300)  # 出错后等5分钟重试

# 每4小时投入$100买BTC
# await dca_strategy("BTC", 100, 4)
```

### 场景4：动态止损
```python
async def trailing_stop_loss(coin, trail_percent=0.05):
    """移动止损：价格上涨时上调止损价格"""
    positions = await get_open_positions()
    
    for pos in positions["positions"]:
        if pos["coin"] != coin:
            continue
            
        entry_price = float(pos["entry_price"])
        current_market = await get_market_data(coin)
        current_price = float(current_market["market_data"]["mid_price"])
        
        # 计算移动止损价格
        if float(pos["size"]) > 0:  # 多仓
            trail_stop = current_price * (1 - trail_percent)
            if trail_stop > entry_price * (1 - trail_percent):
                await set_stop_loss(coin, trail_stop)
                print(f"更新多仓止损: {trail_stop:.2f}")
        else:  # 空仓
            trail_stop = current_price * (1 + trail_percent)
            if trail_stop < entry_price * (1 + trail_percent):
                await set_stop_loss(coin, trail_stop)
                print(f"更新空仓止损: {trail_stop:.2f}")
```

## 错误处理和调试

### 常见错误

1. **订单大小错误**：
```python
# ❌ 用户输入"我要买$100的BTC"
# 错误理解为：
await market_open_position("BTC", "buy", 100)  # 这是100个BTC！

# ✅ 正确处理：
calc = await calculate_token_amount_from_dollars("BTC", 100)
await market_open_position("BTC", "buy", calc["token_amount"])
```

2. **客户端订单ID格式错误**：
```python
# ❌ 错误格式
await place_limit_order("BTC", "buy", 0.1, 45000, cloid="my_order_1")

# ✅ 正确格式（128位十六进制）
await place_limit_order("BTC", "buy", 0.1, 45000, 
                        cloid="0x1234567890abcdef1234567890abcdef")
```

3. **仓位不存在错误**：
```python
# 尝试为不存在的仓位设置止盈止损
try:
    result = await set_take_profit_stop_loss("DOGE", 0.10, 0.08)
    if not result["success"]:
        print(f"错误: {result['error']}")
        # 先检查是否有仓位
        positions = await get_open_positions()
except Exception as e:
    print(f"操作失败: {e}")
```

### 调试技巧

1. **检查返回值**：
```python
result = await market_open_position("BTC", "buy", 0.1)
if result["success"]:
    print("成功:", result["order_result"])
else:
    print("失败:", result["error"])
```

2. **日志查看**：
```bash
# 查看详细日志
tail -f hyperliquid_mcp.log
```

3. **测试网验证**：
```python
# 在测试网上先验证策略
# 设置 HYPERLIQUID_TESTNET=true
```

## 安全建议

### 风险控制
1. **仓位大小管理**：单次交易不超过账户的5-10%
2. **止损设置**：每个仓位都设置止损
3. **杠杆控制**：新手建议使用低杠杆（2-5倍）

### 最佳实践
1. **测试网先行**：新策略先在测试网验证
2. **小仓位试验**：实盘先用小金额测试
3. **监控仓位**：定期检查账户状态
4. **备份私钥**：安全保存私钥，不要提交到代码库

### 紧急操作
```python
# 紧急平掉所有仓位
async def emergency_close_all():
    positions = await get_open_positions()
    for pos in positions["positions"]:
        await market_close_position(pos["coin"])
        print(f"已平仓: {pos['coin']}")

# 取消所有挂单
await cancel_all_orders()
```

## 支持的交易对

该服务器支持HyperLiquid上的所有交易对，包括：
- **主流币种**: BTC, ETH, SOL, AVAX等
- **DeFi代币**: UNI, AAVE, COMP等  
- **Meme币**: DOGE, SHIB, PEPE等

使用时请确保使用HyperLiquid上的确切符号（如"BTC"、"ETH"、"SOL"）。

## 故障排除

### 连接问题
```bash
# 检查网络连接
curl -s https://api.hyperliquid.xyz/info | jq .

# 验证配置
poetry run python -c "from main import get_config; print(get_config())"
```

### 权限问题
```bash
# 检查私钥格式
echo $HYPERLIQUID_PRIVATE_KEY | wc -c  # 应该是66字符(包含0x)
```

### 性能优化
1. **批量操作**：使用`get_account_summary()`而不是分别调用多个函数
2. **避免频繁调用**：市场数据有速率限制
3. **异步处理**：利用async/await处理并发操作

---

**免责声明**: 本工具仅供教育和开发目的。加密货币交易存在风险，请谨慎操作，不要投入超过您能承受损失的资金。