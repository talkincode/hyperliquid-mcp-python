# 交易工具使用指南

本页面详细介绍如何使用 HyperLiquid MCP Server 的各种交易工具。

## 基础交易流程

### 1. 查看市场信息

在交易前，先获取市场数据：

```python
# 获取 BTC 市场数据
market_data = get_market_data("BTC")

if market_data["success"]:
    data = market_data["data"]
    print(f"当前价格: ${data['mark_px']}")
    print(f"24h 成交量: ${data['day_ntl_vlm']}")
```

### 2. 计算订单大小

**关键步骤**：将美元金额转换为代币数量

```python
# 想用 $100 买 BTC
calc = calculate_token_amount_from_dollars("BTC", 100.0)

if calc["success"]:
    token_amount = calc["token_amount"]
    print(f"$100 = {token_amount} BTC")
```

### 3. 下单交易

```python
# 使用计算的代币数量下单
order = market_open_position("BTC", "buy", token_amount)

if order["success"]:
    print(f"订单成功: {order['order_id']}")
```

## 市价交易

### 开仓

使用 `market_open_position()` 快速开仓：

```python
# 计算代币数量
calc = calculate_token_amount_from_dollars("ETH", 200.0)

# 做多（买入）
long_order = market_open_position(
    coin="ETH",
    side="buy",  # 做多
    size=calc["token_amount"]
)

# 做空（卖出）
short_order = market_open_position(
    coin="ETH",
    side="sell",  # 做空
    size=calc["token_amount"]
)
```

### 平仓

使用 `market_close_position()` 快速平仓：

```python
# 关闭所有 BTC 仓位
result = market_close_position("BTC")

if result["success"]:
    print(f"仓位已平: {result['message']}")
```

### 部分平仓

```python
# 平仓 50%
result = close_position("BTC", percentage=50.0)

# 平仓 25%
result = close_position("ETH", percentage=25.0)
```

## 限价交易

### 基础限价单

```python
# 在 $45000 买入 0.1 BTC
order = place_limit_order(
    coin="BTC",
    side="buy",
    size=0.1,
    price=45000.0
)
```

### Reduce-Only 订单

只减仓，不增加仓位：

```python
# 只平仓的限价单
order = place_limit_order(
    coin="BTC",
    side="sell",
    size=0.05,
    price=47000.0,
    reduce_only=True  # 只减仓
)
```

### 带客户端 ID 的订单

用于追踪特定订单：

```python
import secrets

# 生成 128 位十六进制 ID
client_id = "0x" + secrets.token_hex(16)

order = place_limit_order(
    coin="ETH",
    side="buy",
    size=1.0,
    price=3000.0,
    client_order_id=client_id
)

# 保存 client_id 用于后续追踪
print(f"客户端订单 ID: {client_id}")
```

## 括号订单

一次性设置入场、止盈、止损：

### 基础括号订单

```python
# 计算代币数量
calc = calculate_token_amount_from_dollars("SOL", 100.0)

# 入场 $150, 止盈 $160, 止损 $140
order = place_bracket_order(
    coin="SOL",
    side="buy",
    size=calc["token_amount"],
    entry_price=150.0,      # 入场价
    take_profit_price=160.0,  # 止盈价
    stop_loss_price=140.0     # 止损价
)

if order["success"]:
    result = order["bulk_result"]
    print(f"入场订单: {result['entry_order']['order_id']}")
    print(f"止盈订单: {result['take_profit_order']['order_id']}")
    print(f"止损订单: {result['stop_loss_order']['order_id']}")
```

### 适用场景

括号订单适合：

- ✅ 新开仓位
- ✅ 一次性设置完整的交易计划
- ✅ 自动化风险管理

不适合：

- ❌ 现有仓位（使用 `set_take_profit_stop_loss`）
- ❌ 只想设置止盈或止损之一

## 止盈止损管理

### 为现有仓位设置 TP/SL

```python
# 同时设置止盈和止损
result = set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=47000.0,
    stop_loss_price=43000.0
)
```

### 只设置止盈

```python
result = set_take_profit("BTC", take_profit_price=47000.0)

# 或
result = set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=47000.0,
    stop_loss_price=None
)
```

### 只设置止损

```python
result = set_stop_loss("BTC", stop_loss_price=43000.0)

# 或
result = set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=None,
    stop_loss_price=43000.0
)
```

### 修改 TP/SL

要修改现有的止盈止损，需要先取消旧订单，再设置新的：

```python
# 1. 取消现有的 TP/SL 订单
cancel_all_orders("BTC")

# 2. 设置新的 TP/SL
set_take_profit_stop_loss(
    coin="BTC",
    take_profit_price=48000.0,  # 新止盈价
    stop_loss_price=42000.0     # 新止损价
)
```

## 订单管理

### 查看开放订单

```python
orders = get_open_orders()

if orders["success"]:
    for order in orders["orders"]:
        print(f"{order['coin']}: {order['side']} {order['sz']} @ ${order['limit_px']}")
```

### 取消单个订单

```python
# 按订单 ID 取消
cancel_order("BTC", order_id=123456)

# 按客户端订单 ID 取消
cancel_order_by_client_id("BTC", client_order_id="0x1234...")
```

### 批量取消

```python
# 取消 BTC 的所有订单
cancel_all_orders("BTC")

# 取消所有币种的订单
cancel_all_orders()
```

### 修改订单

```python
# 修改订单的价格和数量
modify_order(
    coin="ETH",
    order_id=123456,
    new_size=2.0,
    new_price=3100.0
)
```

## 实战示例

### 示例 1: 简单的市价买入

```python
# 1. 获取当前价格
market = get_market_data("BTC")
current_price = float(market["data"]["mark_px"])
print(f"BTC 当前价格: ${current_price}")

# 2. 计算代币数量（用 $500）
calc = calculate_token_amount_from_dollars("BTC", 500.0)
token_amount = calc["token_amount"]
print(f"将买入: {token_amount} BTC")

# 3. 市价开仓
order = market_open_position("BTC", "buy", token_amount)

if order["success"]:
    print(f"✅ 订单成功")
    print(f"成交均价: ${order['order_result']['avgPx']}")
else:
    print(f"❌ 订单失败: {order['error']}")
```

### 示例 2: 带止盈止损的限价单

```python
# 1. 计算代币数量
calc = calculate_token_amount_from_dollars("ETH", 300.0)

# 2. 下括号订单
order = place_bracket_order(
    coin="ETH",
    side="buy",
    size=calc["token_amount"],
    entry_price=3000.0,      # 在 $3000 入场
    take_profit_price=3300.0,  # 止盈 $3300 (+10%)
    stop_loss_price=2850.0     # 止损 $2850 (-5%)
)

if order["success"]:
    print("✅ 括号订单已设置")
    print(f"入场: $3000")
    print(f"止盈: $3300 (+10%)")
    print(f"止损: $2850 (-5%)")
```

### 示例 3: 追踪止损

手动实现追踪止损逻辑：

```python
import time

def trailing_stop_loss(coin, initial_stop_distance_pct=5.0, trail_distance_pct=3.0):
    """
    简单的追踪止损实现

    Args:
        coin: 交易对
        initial_stop_distance_pct: 初始止损距离百分比
        trail_distance_pct: 追踪距离百分比
    """
    # 获取当前仓位
    positions = get_open_positions()
    position = next((p for p in positions["positions"] if p["coin"] == coin), None)

    if not position:
        print(f"没有 {coin} 仓位")
        return

    entry_price = float(position["entry_px"])
    position_size = abs(float(position["szi"]))
    is_long = float(position["szi"]) > 0

    # 计算初始止损价
    if is_long:
        stop_loss = entry_price * (1 - initial_stop_distance_pct / 100)
    else:
        stop_loss = entry_price * (1 + initial_stop_distance_pct / 100)

    print(f"开始追踪止损 - 入场价: ${entry_price}, 初始止损: ${stop_loss}")

    highest_price = entry_price

    while True:
        # 获取当前价格
        market = get_market_data(coin)
        current_price = float(market["data"]["mark_px"])

        if is_long:
            # 做多：价格创新高，提升止损
            if current_price > highest_price:
                highest_price = current_price
                new_stop = highest_price * (1 - trail_distance_pct / 100)

                if new_stop > stop_loss:
                    stop_loss = new_stop
                    print(f"提升止损到: ${stop_loss:.2f}")

                    # 更新止损订单
                    set_stop_loss(coin, stop_loss_price=stop_loss)

            # 触发止损
            if current_price <= stop_loss:
                print(f"触发止损！平仓价: ${current_price}")
                market_close_position(coin)
                break

        time.sleep(5)  # 每 5 秒检查一次
```

### 示例 4: 分批建仓

```python
def scale_in_position(coin, total_usd, num_orders=3):
    """
    分批建仓

    Args:
        coin: 交易对
        total_usd: 总投资金额
        num_orders: 分几批
    """
    # 获取当前价格
    market = get_market_data(coin)
    current_price = float(market["data"]["mark_px"])

    # 每批金额
    amount_per_order = total_usd / num_orders

    # 价格梯度（每次降低 1%）
    price_step = 0.01

    for i in range(num_orders):
        # 计算每批的入场价
        entry_price = current_price * (1 - price_step * i)

        # 计算代币数量
        calc = calculate_token_amount_from_dollars(coin, amount_per_order)

        # 下限价单
        order = place_limit_order(
            coin=coin,
            side="buy",
            size=calc["token_amount"],
            price=entry_price
        )

        if order["success"]:
            print(f"✅ 批次 {i+1}: ${amount_per_order} @ ${entry_price:.2f}")
        else:
            print(f"❌ 批次 {i+1} 失败: {order['error']}")

# 使用: $1000 分 3 批买入 BTC
scale_in_position("BTC", 1000.0, num_orders=3)
```

### 示例 5: 网格交易

```python
def grid_trading(coin, grid_size=5, price_range_pct=5.0, amount_per_grid=100.0):
    """
    简单的网格交易策略

    Args:
        coin: 交易对
        grid_size: 网格数量
        price_range_pct: 价格范围百分比
        amount_per_grid: 每个网格的金额
    """
    # 获取当前价格
    market = get_market_data(coin)
    mid_price = float(market["data"]["mark_px"])

    # 计算价格范围
    upper_price = mid_price * (1 + price_range_pct / 100)
    lower_price = mid_price * (1 - price_range_pct / 100)
    price_step = (upper_price - lower_price) / grid_size

    print(f"设置网格交易:")
    print(f"中间价: ${mid_price:.2f}")
    print(f"范围: ${lower_price:.2f} - ${upper_price:.2f}")

    # 在中间价下方设置买单
    for i in range(grid_size // 2):
        buy_price = mid_price - (i + 1) * price_step
        calc = calculate_token_amount_from_dollars(coin, amount_per_grid)

        order = place_limit_order(
            coin=coin,
            side="buy",
            size=calc["token_amount"],
            price=buy_price
        )
        print(f"买单 @ ${buy_price:.2f}")

    # 在中间价上方设置卖单
    for i in range(grid_size // 2):
        sell_price = mid_price + (i + 1) * price_step
        calc = calculate_token_amount_from_dollars(coin, amount_per_grid)

        order = place_limit_order(
            coin=coin,
            side="sell",
            size=calc["token_amount"],
            price=sell_price
        )
        print(f"卖单 @ ${sell_price:.2f}")

# 使用
grid_trading("ETH", grid_size=6, price_range_pct=3.0, amount_per_grid=50.0)
```

## 最佳实践

### 1. 始终先计算代币数量

```python
# ❌ 错误
order = market_open_position("SOL", "buy", 20.0)  # 会买 20 个 SOL！

# ✅ 正确
calc = calculate_token_amount_from_dollars("SOL", 20.0)
order = market_open_position("SOL", "buy", calc["token_amount"])
```

### 2. 操作前检查状态

```python
# 检查余额
balance = get_account_balance()
if balance["success"]:
    available = float(balance["data"]["withdrawable"])
    if available < required_amount:
        print("余额不足")
        return

# 检查仓位
positions = get_open_positions()
# ...
```

### 3. 错误处理

```python
order = market_open_position("BTC", "buy", 0.1)

if not order["success"]:
    error_code = order.get("error_code")

    if error_code == "INSUFFICIENT_BALANCE":
        print("余额不足，请充值")
    elif error_code == "API_ERROR":
        print("API 错误，稍后重试")
    else:
        print(f"错误: {order['error']}")
```

### 4. 使用止盈止损

```python
# 开仓时设置
order = place_bracket_order(...)

# 或开仓后立即设置
order = market_open_position("BTC", "buy", 0.1)
if order["success"]:
    set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)
```

### 5. 记录交易

```python
import logging

logging.basicConfig(filename='trading.log', level=logging.INFO)

# 记录每笔交易
order = market_open_position("BTC", "buy", 0.1)
if order["success"]:
    logging.info(f"开仓成功: BTC, size=0.1, id={order['order_id']}")
```

## 相关文档

- [API 参考](../api/tools-reference.md) - 完整的工具列表
- [账户管理](account-management.md) - 管理账户和仓位
- [错误处理](../api/error-handling.md) - 错误处理指南
- [故障排除](../troubleshooting.md) - 常见问题解决
