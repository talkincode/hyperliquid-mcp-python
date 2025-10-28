# 工具 API 参考

本页面列出了 HyperLiquid MCP Server 提供的所有工具及其详细说明。

## 📊 账户管理

### get_account_balance

获取账户余额和保证金信息。

**参数**: 无

**返回**:

```json
{
  "success": true,
  "data": {
    "total_value": "1234.56",
    "available_balance": "1000.00",
    "margin_used": "234.56",
    ...
  }
}
```

**示例**:

```python
balance = get_account_balance()
```

---

### get_open_positions

获取所有开仓及盈亏信息。

**参数**: 无

**返回**:

```json
{
  "success": true,
  "positions": [
    {
      "coin": "BTC",
      "size": "0.1",
      "entry_price": "45000",
      "unrealized_pnl": "250.00",
      ...
    }
  ],
  "total_positions": 1
}
```

**示例**:

```python
positions = get_open_positions()
```

---

### get_open_orders

获取所有未成交订单。

**参数**: 无

**返回**:

```json
{
  "success": true,
  "orders": [
    {
      "order_id": 123456,
      "coin": "ETH",
      "side": "buy",
      "size": "1.0",
      "price": "3000",
      ...
    }
  ],
  "total_orders": 1
}
```

---

### get_trade_history

获取账户交易历史。

**参数**:

- `days` (int, 可选): 回溯天数，默认 7 天

**返回**:

```json
{
  "success": true,
  "trades": [
    {
      "time": "2024-01-01T12:00:00Z",
      "coin": "BTC",
      "side": "buy",
      "size": "0.1",
      "price": "45000",
      ...
    }
  ]
}
```

**示例**:

```python
# 获取最近 7 天的交易
history = get_trade_history()

# 获取最近 30 天的交易
history = get_trade_history(days=30)
```

---

### get_account_summary

获取账户综合概览（余额 + 仓位 + 订单）。

**参数**: 无

**返回**:

```json
{
  "success": true,
  "summary": {
    "balance": {...},
    "positions": [...],
    "orders": [...],
    "total_positions": 1,
    "total_orders": 2
  }
}
```

## 📈 交易工具

### place_limit_order

下限价订单（开仓或平仓）。

**参数**:

- `coin` (str): 交易对，如 "BTC"、"ETH"
- `side` (str): 订单方向，"buy" 或 "sell"
- `size` (float): **代币数量**（不是美元金额！）
- `price` (float): 限价价格
- `reduce_only` (bool, 可选): 是否只减仓，默认 false
- `client_order_id` (str, 可选): 客户端订单 ID（128 位十六进制）

**返回**:

```json
{
  "success": true,
  "order_result": {
    "order_id": 123456,
    "status": "placed",
    ...
  }
}
```

**示例**:

```python
# ❌ 错误：size 不是美元金额
order = place_limit_order("SOL", "buy", 20.0, 150.0)  # 会买 20 个 SOL！

# ✅ 正确：先计算代币数量
calc = calculate_token_amount_from_dollars("SOL", 20.0)  # $20
order = place_limit_order("SOL", "buy", calc["token_amount"], 150.0)
```

!!! warning "重要提示"
`size` 参数是**代币数量**，不是美元金额！ - `0.1` 表示 0.1 个 BTC/ETH/SOL 代币 - 如需按美元金额下单，请先使用 `calculate_token_amount_from_dollars()` 转换

---

### market_open_position

使用市价单开仓（最优执行）。

**参数**:

- `coin` (str): 交易对
- `side` (str): "buy" 做多 或 "sell" 做空
- `size` (float): **代币数量**（不是美元金额！）
- `client_order_id` (str, 可选): 客户端订单 ID

**返回**:

```json
{
  "success": true,
  "order_result": {
    "status": "filled",
    "avg_price": "45123.45",
    ...
  }
}
```

**示例**:

```python
# 先计算代币数量
calc = calculate_token_amount_from_dollars("BTC", 100.0)  # $100 worth

# 开多仓
order = market_open_position("BTC", "buy", calc["token_amount"])

# 开空仓
order = market_open_position("BTC", "sell", calc["token_amount"])
```

---

### market_close_position

使用市价单平仓（关闭所有仓位）。

**参数**:

- `coin` (str): 交易对
- `client_order_id` (str, 可选): 客户端订单 ID

**返回**:

```json
{
  "success": true,
  "order_result": {
    "status": "closed",
    "closed_size": "0.1",
    ...
  }
}
```

**示例**:

```python
# 关闭 BTC 的所有仓位
result = market_close_position("BTC")
```

!!! note "说明"
此方法会关闭指定币种的**所有仓位**，HyperLiquid 会自动确定正确的方向和数量。

---

### place_bracket_order

下括号订单（入场 + 止盈 + 止损一体）。

**参数**:

- `coin` (str): 交易对
- `side` (str): "buy" 或 "sell"
- `size` (float): **代币数量**
- `entry_price` (float): 入场价格
- `take_profit_price` (float): 止盈价格
- `stop_loss_price` (float): 止损价格
- `client_order_id` (str, 可选): 客户端订单 ID

**返回**:

```json
{
  "success": true,
  "bulk_result": {
    "entry_order": {...},
    "take_profit_order": {...},
    "stop_loss_order": {...}
  }
}
```

**示例**:

```python
# 计算代币数量
calc = calculate_token_amount_from_dollars("ETH", 200.0)  # $200

# 下括号订单：入场 $3000，止盈 $3200，止损 $2900
order = place_bracket_order(
    coin="ETH",
    side="buy",
    size=calc["token_amount"],
    entry_price=3000,
    take_profit_price=3200,
    stop_loss_price=2900
)
```

!!! tip "使用场景"
适合**新开仓位**，一次性设置入场、止盈、止损。

    止盈止损订单使用 OCO（一取消另一个）行为。

---

### close_position

关闭仓位（全部或部分）。

**参数**:

- `coin` (str): 交易对
- `percentage` (float, 可选): 平仓百分比，默认 100.0（全部）

**返回**:

```json
{
  "success": true,
  "closed_percentage": 100.0,
  "order_result": {...}
}
```

**示例**:

```python
# 全部平仓
close_position("BTC")

# 平仓 50%
close_position("BTC", percentage=50.0)
```

## 🎯 止盈止损管理

### set_take_profit_stop_loss

为**现有仓位**设置止盈止损（OCO 订单）。

**参数**:

- `coin` (str): 交易对（必须有现有仓位）
- `take_profit_price` (float, 可选): 止盈价格
- `stop_loss_price` (float, 可选): 止损价格
- `position_size` (float, 可选): 仓位大小（自动检测）

**返回**:

```json
{
  "success": true,
  "tp_order": {...},
  "sl_order": {...}
}
```

**示例**:

```python
# 为现有 BTC 仓位设置止盈止损
set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=47000,
    stop_loss_price=43000
)

# 只设置止盈
set_take_profit_stop_loss(coin="BTC", take_profit_price=47000)

# 只设置止损
set_take_profit_stop_loss(coin="BTC", stop_loss_price=43000)
```

!!! warning "注意"
此方法仅适用于**已有仓位**。

    新开仓位请使用 `place_bracket_order()`。

---

### set_take_profit

为现有仓位**只设置**止盈。

**参数**:

- `coin` (str): 交易对
- `take_profit_price` (float): 止盈价格
- `position_size` (float, 可选): 仓位大小

**示例**:

```python
set_take_profit("ETH", take_profit_price=3200)
```

---

### set_stop_loss

为现有仓位**只设置**止损。

**参数**:

- `coin` (str): 交易对
- `stop_loss_price` (float): 止损价格
- `position_size` (float, 可选): 仓位大小

**示例**:

```python
set_stop_loss("ETH", stop_loss_price=2900)
```

## 📝 订单管理

### cancel_order

根据订单 ID 取消订单。

**参数**:

- `coin` (str): 交易对
- `order_id` (int): 订单 ID

**示例**:

```python
cancel_order("BTC", order_id=123456)
```

---

### cancel_order_by_client_id

根据客户端订单 ID 取消订单。

**参数**:

- `coin` (str): 交易对
- `client_order_id` (str): 客户端订单 ID

**示例**:

```python
cancel_order_by_client_id("BTC", client_order_id="0x1234...")
```

---

### cancel_all_orders

取消所有订单或指定币种的订单。

**参数**:

- `coin` (str, 可选): 交易对（不指定则取消所有）

**示例**:

```python
# 取消 BTC 的所有订单
cancel_all_orders("BTC")

# 取消所有币种的订单
cancel_all_orders()
```

---

### modify_order

修改现有订单。

**参数**:

- `coin` (str): 交易对
- `order_id` (int): 订单 ID
- `new_size` (float): 新订单大小
- `new_price` (float): 新订单价格

**示例**:

```python
modify_order("ETH", order_id=123456, new_size=2.0, new_price=3100)
```

## 💹 市场数据

### get_market_data

获取指定币种的市场数据。

**参数**:

- `coin` (str): 交易对

**返回**:

```json
{
  "success": true,
  "data": {
    "coin": "BTC",
    "mark_price": "45123.45",
    "bid": "45120.00",
    "ask": "45125.00",
    "24h_volume": "1234567.89",
    ...
  }
}
```

**示例**:

```python
data = get_market_data("BTC")
```

---

### get_orderbook

获取订单簿数据。

**参数**:

- `coin` (str): 交易对
- `depth` (int, 可选): 深度，默认 20

**返回**:

```json
{
  "success": true,
  "orderbook": {
    "bids": [[45120.0, 1.5], [45110.0, 2.0], ...],
    "asks": [[45125.0, 1.2], [45130.0, 1.8], ...]
  }
}
```

**示例**:

```python
# 默认深度 20
book = get_orderbook("BTC")

# 深度 50
book = get_orderbook("BTC", depth=50)
```

---

### get_funding_history

获取资金费率历史。

**参数**:

- `coin` (str): 交易对
- `days` (int, 可选): 回溯天数，默认 7

**返回**:

```json
{
  "success": true,
  "funding_history": [
    {
      "time": "2024-01-01T12:00:00Z",
      "rate": "0.0001",
      ...
    }
  ]
}
```

**示例**:

```python
history = get_funding_history("BTC", days=30)
```

## ⚙️ 账户设置

### update_leverage

更新杠杆倍数。

**参数**:

- `coin` (str): 交易对
- `leverage` (int): 杠杆倍数（如 10 表示 10x）
- `cross_margin` (bool, 可选): 全仓模式（true）或逐仓模式（false），默认 true

**返回**:

```json
{
  "success": true,
  "leverage": 10,
  "mode": "cross"
}
```

**示例**:

```python
# 设置 BTC 为 10x 全仓杠杆
update_leverage("BTC", leverage=10, cross_margin=True)

# 设置 ETH 为 5x 逐仓杠杆
update_leverage("ETH", leverage=5, cross_margin=False)
```

---

### transfer_between_spot_and_perp

在现货和合约账户间转账。

**参数**:

- `amount` (float): 转账金额
- `to_perp` (bool, 可选): 转到合约账户（true）或现货账户（false），默认 true

**返回**:

```json
{
  "success": true,
  "transferred": 1000.0,
  "direction": "to_perp"
}
```

**示例**:

```python
# 从现货转 1000 到合约
transfer_between_spot_and_perp(amount=1000.0, to_perp=True)

# 从合约转 500 到现货
transfer_between_spot_and_perp(amount=500.0, to_perp=False)
```

## 🧮 实用工具

### calculate_token_amount_from_dollars

根据当前价格将美元金额转换为代币数量。

**参数**:

- `coin` (str): 交易对
- `dollar_amount` (float): 美元金额

**返回**:

```json
{
  "success": true,
  "coin": "SOL",
  "dollar_amount": 20.0,
  "current_price": 150.0,
  "token_amount": 0.133,
  "calculation": "$20.00 ÷ $150.00 = 0.133 SOL"
}
```

**示例**:

```python
# 计算 $20 能买多少 SOL
calc = calculate_token_amount_from_dollars("SOL", 20.0)
print(f"Token amount: {calc['token_amount']}")  # 0.133

# 用于下单
order = market_open_position("SOL", "buy", calc["token_amount"])
```

!!! tip "最佳实践"
这是**最常用的工具**之一！

    在下单前使用此工具将美元金额转换为代币数量，避免下单错误。

---

## 📋 返回格式

所有工具都返回标准化的 JSON 格式：

### 成功响应

```json
{
  "success": true,
  "data": {
    /* 具体数据 */
  }
}
```

或

```json
{
  "success": true,
  "order_result": {
    /* 订单结果 */
  },
  "order_id": 123456
}
```

### 错误响应

```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "ERROR_CODE"
}
```

常见错误代码：

- `VALIDATION_ERROR` - 输入验证失败
- `INSUFFICIENT_BALANCE` - 余额不足
- `POSITION_NOT_FOUND` - 仓位不存在
- `ORDER_NOT_FOUND` - 订单不存在
- `API_ERROR` - API 调用失败

## 🔑 关键概念

### Size 参数

!!! danger "重要"
**所有交易函数中的 `size` 参数代表代币数量，不是美元金额！**

    - ✅ `0.1` = 0.1 个 BTC/ETH/SOL 代币
    - ❌ `20.0` ≠ $20 美元

    使用 `calculate_token_amount_from_dollars()` 进行转换。

### OCO 订单组

**括号订单** vs **现有仓位 TP/SL**：

| 场景             | 使用工具                      | 订单组类型     |
| ---------------- | ----------------------------- | -------------- |
| 新仓位 + TP/SL   | `place_bracket_order()`       | `normalTpSl`   |
| 现有仓位 + TP/SL | `set_take_profit_stop_loss()` | `positionTpSl` |

### 客户端订单 ID

格式要求：**128 位十六进制字符串**

- ✅ `0x1234567890abcdef1234567890abcdef`
- ❌ `my-order-123`

## 📚 相关文档

- [使用指南](../guides/trading-tools.md) - 详细的使用教程
- [常见用例](../guides/use-cases.md) - 实际应用示例
- [错误处理](error-handling.md) - 错误处理最佳实践
- [故障排除](../troubleshooting.md) - 常见问题解决
