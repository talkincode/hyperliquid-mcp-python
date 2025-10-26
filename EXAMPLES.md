# HyperLiquid MCP 详细使用示例

本文档提供所有 MCP 工具的详细使用示例和最佳实践，所有示例均基于实际的 API 方法。

## 重要说明

⚠️ **所有示例中的 `size` 参数都是代币数量，不是美元金额！**

- ✅ 正确：`size=0.1` 表示 0.1 个 BTC
- ❌ 错误：`size=1000` 误认为是 $1000（实际是 1000 个 BTC）

💡 如需使用美元金额，请使用 `calculate_token_amount_from_dollars` 工具先转换。

## 目录

- [账户管理](#账户管理)
- [市场数据查询](#市场数据查询)
- [开仓交易](#开仓交易)
- [仓位管理](#仓位管理)
- [订单管理](#订单管理)
- [工具函数](#工具函数)
- [完整交易流程](#完整交易流程)

---

## 账户管理

### 1. 获取账户余额

**工具名称**：`get_account_balance`

```python
# 查询账户余额和保证金信息
result = await get_account_balance()

# 返回示例
{
    "success": True,
    "data": {
        "marginSummary": {
            "accountValue": "10000.00",      # 账户总价值
            "totalMarginUsed": "2000.00",    # 已用保证金
            "totalNtlPos": "5000.00",        # 总名义持仓
            "totalRawUsd": "8000.00"         # 可用余额
        },
        "assetPositions": [...]
    },
    "account_address": "0x..."
}
```

**使用场景**：
- 交易前检查账户余额
- 计算可开仓位大小
- 监控保证金使用率

---

### 2. 查看持仓

```python
# 获取所有开仓
positions = get_open_positions()

# 返回示例
{
    "success": true,
    "positions": [
        {
            "coin": "BTC",
            "size": "0.5",                    # 仓位大小（正数做多，负数做空）
            "entry_price": "45000.00",        # 开仓均价
            "unrealized_pnl": "500.00",       # 未实现盈亏
            "return_on_equity": "0.05",       # 收益率 5%
            "margin_used": "2250.00"          # 使用保证金
        },
        {
            "coin": "ETH",
            "size": "-2.0",                   # 负数表示做空
            "entry_price": "3000.00",
            "unrealized_pnl": "-100.00",
            "return_on_equity": "-0.02",
            "margin_used": "3000.00"
        }
    ],
    "total_positions": 2
}
```

**使用场景**：
- 查看当前持仓状态
- 计算总盈亏
- 决定是否需要调仓

---

### 3. 查看未成交订单

```python
# 获取所有挂单
orders = get_open_orders()

# 返回示例
{
    "success": true,
    "orders": [
        {
            "order_id": 12345,
            "coin": "BTC",
            "side": "buy",                    # buy 或 sell
            "size": "0.1",
            "limit_price": "44000.00",
            "reduce_only": false,
            "order_type": "limit",
            "timestamp": 1698765432000,
            "cloid": "0x1234..."              # 客户端订单ID（如有）
        }
    ],
    "total_orders": 1
}
```

---

### 4. 账户总览

```python
# 一次获取完整账户信息
summary = get_account_summary()

# 返回示例
{
    "success": true,
    "summary": {
        "balance": {...},                     # 余额信息
        "positions": [...],                   # 持仓列表
        "orders": [...],                      # 挂单列表
        "total_positions": 2,
        "total_orders": 3
    }
}
```

**使用场景**：
- 快速了解账户全貌
- 生成账户报告
- 交易前全面检查

---

## 市场数据查询

### 1. 获取市场行情

```python
# 查询 BTC 市场数据
market_data = get_market_data("BTC")

# 返回示例
{
    "success": true,
    "market_data": {
        "coin": "BTC",
        "mid_price": "45500.00",          # 中间价
        "best_bid": "45499.50",           # 最佳买价
        "best_ask": "45500.50",           # 最佳卖价
        "bid_size": "2.5",                # 买单量
        "ask_size": "1.8",                # 卖单量
        "max_leverage": 50,               # 最大杠杆
        "only_isolated": false,           # 是否仅支持逐仓
        "timestamp": 1698765432000
    }
}
```

**使用场景**：
- 获取实时价格
- 计算买卖价差
- 确定下单价格

---

### 2. 获取订单簿

```python
# 获取 ETH 订单簿（深度 10）
orderbook = get_orderbook("ETH", depth=10)

# 返回示例
{
    "success": true,
    "orderbook": {
        "coin": "ETH",
        "bids": [                         # 买单（按价格降序）
            {"px": "3000.00", "sz": "5.2"},
            {"px": "2999.50", "sz": "3.1"},
            ...
        ],
        "asks": [                         # 卖单（按价格升序）
            {"px": "3000.50", "sz": "4.8"},
            {"px": "3001.00", "sz": "6.3"},
            ...
        ],
        "timestamp": 1698765432000
    }
}
```

**使用场景**：
- 分析市场深度
- 寻找支撑位/阻力位
- 大单滑点估算

---

### 3. 查询资金费率

```python
# 获取 SOL 最近 7 天资金费率
funding = get_funding_history("SOL", days=7)

# 返回示例
{
    "success": true,
    "funding_history": [
        {
            "time": 1698700800000,
            "fundingRate": "0.0001",      # 0.01% 资金费率
            "premium": "0.00008"
        },
        ...
    ],
    "coin": "SOL",
    "days": 7
}
```

**使用场景**：
- 评估持仓成本
- 选择持仓时机
- 套利机会分析

---

## 开仓交易

### 1. 市价开仓（最简单）

```python
# 示例 1: 市价做多 0.1 BTC
result = market_open_position(
    coin="BTC",
    side="buy",           # "buy" 做多，"sell" 做空
    size=0.1              # 0.1 个 BTC（不是美元金额！）
)

# 示例 2: 市价做空 1 ETH
result = market_open_position(
    coin="ETH",
    side="sell",          # 做空
    size=1.0
)

# 返回示例
{
    "success": true,
    "action": "market_open_position",
    "order_result": {
        "status": "ok",
        "response": {
            "type": "order",
            "data": {
                "statuses": [
                    {
                        "filled": {
                            "totalSz": "0.1",
                            "avgPx": "45500.00"
                        }
                    }
                ]
            }
        }
    },
    "position_details": {
        "coin": "BTC",
        "side": "long",
        "size": "0.1",
        "order_type": "market"
    }
}
```

**重要提示**：
- ✅ `size=0.1` 表示 0.1 个 BTC
- ❌ `size=1000` 不是 $1000，而是 1000 个 BTC！

---

### 2. 美元金额开仓（推荐）

```python
# 第 1 步：将美元转换为代币数量
calc = await calculate_token_amount_from_dollars("SOL", 100.0)  # $100

# 返回示例
{
    "success": True,
    "coin": "SOL",
    "dollar_amount": 100.0,
    "current_price": 150.0,
    "token_amount": 0.66666667,           # $100 ÷ $150 = 0.667 SOL
    "calculation": "$100.0 ÷ $150.0 = 0.66666667 SOL"
}

# 第 2 步：使用计算出的代币数量开仓
result = await market_open_position(
    coin="SOL",
    side="buy",
    size=calc["token_amount"]            # 使用计算出的代币数量
)
```

---

### 3. 限价开仓

```python
# 限价单：在 $44000 买入 0.1 BTC
result = place_limit_order(
    coin="BTC",
    side="buy",
    size=0.1,
    price=44000.0,
    reduce_only=False,                   # False=可开新仓
    client_order_id="0x1234..."          # 可选：自定义订单ID
)

# 返回示例
{
    "success": true,
    "order_result": {...},
    "order_details": {
        "coin": "BTC",
        "side": "BUY",
        "size": 0.1,
        "limit_price": 44000.0,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": false
    }
}
```

**订单类型说明**：
- `Gtc` (Good Till Cancel): 一直有效直到成交或取消
- `Ioc` (Immediate Or Cancel): 立即成交否则取消
- `Alo` (Add Liquidity Only): 只做 Maker

---

### 4. 括号订单（开仓 + 止盈止损）

```python
# 一键开仓并设置止盈止损
result = place_bracket_order(
    coin="BTC",
    side="buy",
    size=0.1,
    entry_price=45000.0,      # 入场价
    take_profit_price=47000.0,  # 止盈价（+4.4%）
    stop_loss_price=43000.0     # 止损价（-4.4%）
)

# 返回示例
{
    "success": true,
    "bulk_result": {
        "status": "ok",
        "response": {...}
    },
    "order_details": {
        "coin": "BTC",
        "side": "BUY",
        "size": 0.1,
        "entry_price": 45000.0,
        "take_profit_price": 47000.0,
        "stop_loss_price": 43000.0,
        "grouping": "normalTpSl"         # OCO 分组
    }
}
```

**OCO 行为**：
- 止盈和止损互斥
- 触发一个，另一个自动取消
- 适合新开仓位

---

## 仓位管理

### 1. 为现有仓位设置止盈止损

```python
# 场景：已有 BTC 多仓，现在设置止盈止损

# 方式 1：同时设置止盈和止损
result = set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=47000.0,
    stop_loss_price=43000.0
    # position_size 会自动检测
)

# 方式 2：只设置止盈
result = set_take_profit("BTC", 47000.0)

# 方式 3：只设置止损
result = set_stop_loss("BTC", 43000.0)

# 返回示例
{
    "success": true,
    "bulk_result": {...},
    "position_details": {
        "coin": "BTC",
        "position_size": 0.5,             # 自动检测到的仓位大小
        "is_long": true,                  # 多仓
        "take_profit_price": 47000.0,
        "stop_loss_price": 43000.0,
        "grouping": "positionTpSl"        # 现有仓位的 OCO 分组
    }
}
```

**注意事项**：
- 必须先有仓位才能设置
- 自动检测仓位大小和方向
- 支持多次修改止盈止损

---

### 2. 市价平仓

```python
# 平掉所有 BTC 仓位
result = market_close_position("BTC")

# 返回示例
{
    "success": true,
    "action": "market_close_position",
    "order_result": {...},
    "order_details": {
        "coin": "BTC",
        "original_side": "long",          # 原仓位方向
        "original_size": "0.5",           # 原仓位大小
        "side": "sell",                   # 平仓方向（做多平空，做空平多）
        "reduce_only": true
    }
}
```

**使用场景**：
- 快速止损
- 获利了结
- 紧急平仓

---

### 3. 部分平仓

```python
# ⚠️ market_close_position 会平掉全部仓位
# 部分平仓需要用 place_limit_order + reduce_only=True

# 示例：平掉 50% 的 BTC 仓位

# 步骤 1: 获取当前仓位信息
positions = await get_open_positions()
btc_position = [p for p in positions["positions"] if p["coin"] == "BTC"][0]
position_size = abs(float(btc_position["size"]))
is_long = float(btc_position["size"]) > 0

# 步骤 2: 获取当前价格
market_data = await get_market_data("BTC")
current_price = float(market_data["market_data"]["mid_price"])

# 步骤 3: 使用限价单平掉一半
result = await place_limit_order(
    coin="BTC",
    side="sell" if is_long else "buy",  # 反向
    size=position_size * 0.5,           # 平 50%
    price=current_price * 0.999,        # 稍微激进的价格
    reduce_only=True                    # 重要：只减仓
)
```

---

### 4. 调整杠杆

```python
# 设置 BTC 为 10 倍全仓杠杆
result = update_leverage(
    coin="BTC",
    leverage=10,
    cross_margin=True                   # True=全仓，False=逐仓
)

# 设置 ETH 为 5 倍逐仓杠杆
result = update_leverage(
    coin="ETH",
    leverage=5,
    cross_margin=False
)

# 返回示例
{
    "success": true,
    "leverage_result": {...},
    "leverage_update": {
        "coin": "BTC",
        "leverage": 10,
        "cross_margin": true
    }
}
```

**注意事项**：
- 有持仓时调整杠杆可能受限
- 先平仓再调整更安全

---

## 订单管理

### 1. 取消单个订单

```python
# 按订单 ID 取消
result = cancel_order("BTC", order_id=12345)

# 按客户端订单 ID 取消
result = cancel_order_by_client_id(
    "BTC",
    "0x1234567890abcdef1234567890abcdef"
)

# 返回示例
{
    "success": true,
    "cancel_result": {...},
    "cancelled_order": {
        "coin": "BTC",
        "order_id": 12345
    }
}
```

---

### 2. 批量取消订单

```python
# 取消 BTC 的所有挂单
result = cancel_all_orders("BTC")

# 取消所有币种的所有挂单
result = cancel_all_orders()

# 返回示例
{
    "success": true,
    "cancelled_orders": 5,
    "failed_cancellations": 0,
    "results": [...]
}
```

---

### 3. 修改订单

```python
# 修改订单价格和数量
result = modify_order(
    coin="BTC",
    order_id=12345,
    new_size=0.2,                       # 新数量
    new_price=44500.0                   # 新价格
)

# 返回示例
{
    "success": true,
    "modify_result": {...},
    "modified_order": {
        "coin": "BTC",
        "order_id": 12345,
        "new_size": "0.2",
        "new_price": "44500.0"
    }
}
```

---

## 工具函数

### 1. calculate_token_amount_from_dollars - 美元转代币数量

这是最常用的辅助工具，用于将美元金额转换为代币数量。

```python
# 转换 $100 为 SOL 代币数量
calc = await calculate_token_amount_from_dollars(
    coin="SOL",
    dollar_amount=100.0
)

# 返回示例
{
    "success": True,
    "coin": "SOL",
    "dollar_amount": 100.0,
    "current_price": 150.0,
    "token_amount": 0.66666667,           # $100 ÷ $150 = 0.667 SOL
    "calculation": "$100.0 ÷ $150.0 = 0.66666667 SOL"
}
```

**组合使用示例**：
```python
# 步骤 1: 转换美元为代币数量
calc = await calculate_token_amount_from_dollars("BTC", 500.0)

# 步骤 2: 使用转换后的数量开仓
if calc["success"]:
    result = await market_open_position(
        coin="BTC",
        side="buy",
        size=calc["token_amount"]
    )
```

---

### 2. close_position - 关闭仓位（辅助函数）

这是对 `market_close_position` 的封装，支持百分比参数。

```python
# 关闭 100% 仓位
result = await close_position(
    coin="BTC",
    percentage=100.0
)

# ⚠️ 注意：不支持部分平仓
result = await close_position(coin="BTC", percentage=50.0)
# 会返回错误：
# "Partial position closure (50%) not supported with market orders."
```

**部分平仓需要使用 place_limit_order**：
```python
# 获取仓位信息
positions = await get_open_positions()
btc_pos = next(p for p in positions["positions"] if p["coin"] == "BTC")
position_size = abs(float(btc_pos["size"]))
is_long = float(btc_pos["size"]) > 0

# 获取当前价格
market_data = await get_market_data("BTC")
current_price = float(market_data["market_data"]["mid_price"])

# 平掉 50%
result = await place_limit_order(
    coin="BTC",
    side="sell" if is_long else "buy",
    size=position_size * 0.5,
    price=current_price * 0.999,
    reduce_only=True
)
```

---

## 完整交易流程示例

### 示例 1: 基于美元金额开仓并设置止盈止损

```python
# 步骤 1: 转换美元为代币数量
calc = await calculate_token_amount_from_dollars("BTC", 200.0)

if not calc["success"]:
    print(f"转换失败: {calc.get('error')}")
else:
    token_amount = calc["token_amount"]
    entry_price = calc["current_price"]
    
    # 步骤 2: 计算止盈止损价格（止盈 5%，止损 3%）
    tp_price = entry_price * 1.05  # 做多，止盈 +5%
    sl_price = entry_price * 0.97  # 做多，止损 -3%
    
    # 步骤 3: 开仓
    open_result = await market_open_position(
        coin="BTC",
        side="buy",
        size=token_amount
    )
    
    if not open_result["success"]:
        print(f"开仓失败: {open_result.get('error')}")
    else:
        # 步骤 4: 设置止盈止损
        tpsl_result = await set_take_profit_stop_loss(
            coin="BTC",
            take_profit_price=tp_price,
            stop_loss_price=sl_price
        )
        
        print(f"✅ 交易完成:")
        print(f"  投资: $200")
        print(f"  数量: {token_amount} BTC")
        print(f"  入场价: ${entry_price}")
        print(f"  止盈: ${tp_price} (+5%)")
        print(f"  止损: ${sl_price} (-3%)")
```

---

### 示例 2: 风险管理开仓

```python
# 目标: 用账户的 2% 风险做多 BTC，止损 5%

# 步骤 1: 获取账户余额
balance = await get_account_balance()
account_value = float(balance["data"]["marginSummary"]["accountValue"])

# 步骤 2: 计算风险金额和仓位大小
risk_percent = 0.02  # 2% 风险
stop_loss_percent = 0.05  # 5% 止损
risk_amount = account_value * risk_percent

# 获取当前价格
market_data = await get_market_data("BTC")
current_price = float(market_data["market_data"]["mid_price"])

# 计算仓位大小
# 风险金额 = 仓位价值 × 止损百分比
position_value = risk_amount / stop_loss_percent
position_size = position_value / current_price

# 步骤 3: 开仓
open_result = await market_open_position(
    coin="BTC",
    side="buy",
    size=position_size
)

# 步骤 4: 设置止损
stop_price = current_price * (1 - stop_loss_percent)
sl_result = await set_stop_loss("BTC", stop_price)

print(f"✅ 风险管理开仓完成:")
print(f"  账户价值: ${account_value}")
print(f"  最大风险: ${risk_amount} ({risk_percent*100}%)")
print(f"  仓位大小: {position_size} BTC")
print(f"  止损价格: ${stop_price}")
```

---

### 示例 3: 带错误处理的安全交易

```python
# 步骤 1: 检查账户余额
balance = await get_account_balance()
if not balance["success"]:
    print(f"获取余额失败: {balance.get('error')}")
else:
    account_value = float(balance["data"]["marginSummary"]["accountValue"])
    dollar_amount = 100.0
    
    # 安全检查: 不超过账户 90%
    if dollar_amount > account_value * 0.9:
        print("交易金额过大，超过账户 90%")
    else:
        # 步骤 2: 转换美元为代币数量
        calc = await calculate_token_amount_from_dollars("BTC", dollar_amount)
        if not calc["success"]:
            print(f"金额转换失败: {calc.get('error')}")
        else:
            # 步骤 3: 验证市场数据
            market_data = await get_market_data("BTC")
            if not market_data["success"]:
                print("获取市场数据失败")
            else:
                # 步骤 4: 开仓
                result = await market_open_position(
                    coin="BTC",
                    side="buy",
                    size=calc["token_amount"]
                )
                
                if not result["success"]:
                    print(f"开仓失败: {result.get('error')}")
                else:
                    # 步骤 5: 设置 5% 止损
                    current_price = float(market_data["market_data"]["mid_price"])
                    stop_price = current_price * 0.95
                    
                    sl_result = await set_stop_loss("BTC", stop_price)
                    
                    print(f"✅ 交易成功:")
                    print(f"  投资: ${dollar_amount}")
                    print(f"  数量: {calc['token_amount']} BTC")
                    print(f"  入场价: ${calc['current_price']}")
                    print(f"  止损: ${stop_price}")
```

---

## 常见问题

### Q1: 为什么我的订单没有成交？

```python
# 检查未成交订单并对比市场价格
orders = await get_open_orders()

for order in orders["orders"]:
    # 获取当前市价
    market = await get_market_data(order['coin'])
    current_price = float(market["market_data"]["mid_price"])
    order_price = float(order['limit_price'])
    
    print(f"币种: {order['coin']}")
    print(f"订单价格: ${order_price}")
    print(f"当前市价: ${current_price}")
    print(f"价差: ${abs(current_price - order_price):.2f}")
```

---

### Q2: 如何查看交易历史？

```python
# 获取最近 30 天交易记录
history = await get_trade_history(days=30)

if history["success"]:
    for trade in history["trades"]:
        side_text = "买入" if trade['side'] == "B" else "卖出"
        print(f"{trade['time']}: {side_text} {trade['size']} {trade['coin']} @ ${trade['price']}")
        print(f"  手续费: ${trade['fee']}")
```

---

### Q3: 如何在测试网和主网之间切换？

**方法 1: 环境变量**
```bash
# 测试网
export HYPERLIQUID_TESTNET=true

# 主网
export HYPERLIQUID_TESTNET=false
```

**方法 2: .env 文件**
```
HYPERLIQUID_TESTNET=true
```

**方法 3: config.json**
```json
{
    "private_key": "your_key",
    "testnet": true,
    "account_address": "your_address"
}
```

---

### Q4: 为什么止盈止损没有互斥？

确保使用正确的方法：

- **新仓位**: 使用 `place_bracket_order()` → 使用 `normalTpSl` 分组
- **现有仓位**: 使用 `set_take_profit_stop_loss()` → 使用 `positionTpSl` 分组

两者都会实现 OCO（One-Cancels-Other）行为。

---

### Q5: 如何部分平仓？

`market_close_position()` 会平掉所有仓位。部分平仓需要使用限价单：

```python
# 获取当前仓位
positions = await get_open_positions()
btc_pos = next(p for p in positions["positions"] if p["coin"] == "BTC")
position_size = abs(float(btc_pos["size"]))
is_long = float(btc_pos["size"]) > 0

# 获取当前价格
market_data = await get_market_data("BTC")
current_price = float(market_data["market_data"]["mid_price"])

# 平掉 50% - 使用限价单 + reduce_only
result = await place_limit_order(
    coin="BTC",
    side="sell" if is_long else "buy",
    size=position_size * 0.5,
    price=current_price * 0.999,  # 稍微激进的价格
    reduce_only=True
)
```

---

## 性能优化建议

### 1. 使用账户总览减少 API 调用

```python
# ❌ 不推荐: 多次调用
balance = await get_account_balance()
positions = await get_open_positions()
orders = await get_open_orders()

# ✅ 推荐: 一次获取所有信息
summary = await get_account_summary()
# summary 包含 balance, positions, orders
```

---

### 2. 并发获取多个币种数据

```python
import asyncio

# 并发获取 BTC、ETH、SOL 的市场数据
tasks = [
    get_market_data("BTC"),
    get_market_data("ETH"),
    get_market_data("SOL")
]
results = await asyncio.gather(*tasks)

# 访问结果
btc_data, eth_data, sol_data = results
print(f"BTC 价格: {btc_data['market_data']['mid_price']}")
print(f"ETH 价格: {eth_data['market_data']['mid_price']}")
print(f"SOL 价格: {sol_data['market_data']['mid_price']}")
```

---

## 总结

### 核心 MCP 工具列表

**账户管理工具**:
- `get_account_balance()` - 获取余额和保证金信息
- `get_open_positions()` - 查看所有持仓
- `get_open_orders()` - 查看所有未成交订单
- `get_account_summary()` - 获取账户完整信息
- `get_trade_history(days)` - 获取交易历史

**市场数据工具**:
- `get_market_data(coin)` - 获取实时行情
- `get_orderbook(coin, depth)` - 获取订单簿
- `get_funding_history(coin, days)` - 查询资金费率

**交易工具**:
- `market_open_position(coin, side, size)` - 市价开仓 ⭐
- `market_close_position(coin)` - 市价平仓
- `place_limit_order(coin, side, size, price, reduce_only)` - 限价订单
- `place_bracket_order(coin, side, size, entry_price, tp_price, sl_price)` - 括号订单（新仓位）

**订单管理工具**:
- `cancel_order(coin, order_id)` - 取消订单
- `cancel_order_by_client_id(coin, client_order_id)` - 按客户端ID取消
- `cancel_all_orders(coin)` - 批量取消订单
- `modify_order(coin, order_id, new_size, new_price)` - 修改订单

**仓位管理工具**:
- `set_take_profit_stop_loss(coin, tp_price, sl_price)` - 设置止盈止损（现有仓位）⭐
- `set_take_profit(coin, tp_price)` - 只设置止盈
- `set_stop_loss(coin, sl_price)` - 只设置止损
- `update_leverage(coin, leverage, cross_margin)` - 调整杠杆
- `transfer_between_spot_and_perp(amount, to_perp)` - 资金划转

**工具函数**:
- `calculate_token_amount_from_dollars(coin, dollar_amount)` - 美元转代币数量 ⭐
- `close_position(coin, percentage)` - 关闭仓位（辅助函数）

---

### 关键要点

1. ✅ **size 参数是代币数量**，不是美元金额
2. ✅ 使用 `calculate_token_amount_from_dollars()` 进行美元转换
3. ✅ 新仓位用 `place_bracket_order()`，现有仓位用 `set_take_profit_stop_loss()`
4. ✅ 市价开仓用 `market_open_position()`，市价平仓用 `market_close_position()`
5. ✅ 所有工具都是异步的，需要使用 `await`
6. ✅ 所有操作都有标准化的 `{"success": bool, ...}` 返回格式

---

### 安全提示

- 🔒 **始终在测试网先测试**策略和代码
- 🔒 **设置合理的止损**保护资金安全
- 🔒 **不要投入超过你能承受损失的资金**
- 🔒 **使用 API 钱包**而非主钱包私钥
- 🔒 **定期检查持仓和风险敞口**
- 🔒 **验证所有计算结果**再下单

---

### 快速参考

**开仓流程**:
```python
# 1. 转换美元
calc = await calculate_token_amount_from_dollars("BTC", 100.0)
# 2. 开仓
result = await market_open_position("BTC", "buy", calc["token_amount"])
# 3. 设置止盈止损
await set_take_profit_stop_loss("BTC", tp_price=50000, sl_price=40000)
```

**查询流程**:
```python
# 获取完整账户信息
summary = await get_account_summary()
# 获取市场数据
market = await get_market_data("BTC")
```

**平仓流程**:
```python
# 全部平仓
await market_close_position("BTC")
# 部分平仓 - 使用限价单 + reduce_only=True
await place_limit_order("BTC", "sell", 0.5, price, reduce_only=True)
```
