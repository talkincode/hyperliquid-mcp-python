# 错误处理

本页面介绍如何正确处理 HyperLiquid MCP Server 中的错误。

## 错误类型

### 1. 验证错误 (VALIDATION_ERROR)

输入参数不符合要求。

**常见原因**:

- 币种符号无效
- 价格或数量为负数或零
- 订单方向无效（不是 "buy" 或 "sell"）
- 客户端订单 ID 格式错误

**示例**:

```json
{
  "success": false,
  "error": "Invalid coin symbol: INVALID",
  "error_code": "VALIDATION_ERROR"
}
```

**解决方案**:

```python
# ❌ 错误
order = place_limit_order("INVALID", "buy", 1.0, 3000)

# ✅ 正确
order = place_limit_order("BTC", "buy", 0.1, 45000)
```

---

### 2. 余额不足 (INSUFFICIENT_BALANCE)

账户余额不足以完成操作。

**示例**:

```json
{
  "success": false,
  "error": "Insufficient balance to place order",
  "error_code": "INSUFFICIENT_BALANCE",
  "required": "1000.00",
  "available": "500.00"
}
```

**解决方案**:

```python
# 先检查余额
balance = get_account_balance()
if balance["success"]:
    available = float(balance["data"]["withdrawable"])

    # 只下能承受的订单
    if available >= required_amount:
        order = place_limit_order(...)
    else:
        print(f"余额不足: 需要 ${required_amount}, 可用 ${available}")
```

---

### 3. 仓位未找到 (POSITION_NOT_FOUND)

尝试操作不存在的仓位。

**示例**:

```json
{
  "success": false,
  "error": "No position found for BTC",
  "error_code": "POSITION_NOT_FOUND",
  "coin": "BTC"
}
```

**解决方案**:

```python
# 先检查仓位是否存在
positions = get_open_positions()
if positions["success"]:
    btc_position = next(
        (p for p in positions["positions"] if p["coin"] == "BTC"),
        None
    )

    if btc_position:
        # 仓位存在，可以设置 TP/SL
        set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)
    else:
        print("BTC 仓位不存在，请先开仓")
```

---

### 4. 订单未找到 (ORDER_NOT_FOUND)

尝试操作不存在的订单。

**示例**:

```json
{
  "success": false,
  "error": "Order not found: 123456",
  "error_code": "ORDER_NOT_FOUND",
  "order_id": 123456
}
```

**解决方案**:

```python
# 先获取开放订单列表
orders = get_open_orders()
if orders["success"]:
    order_ids = [o["order_id"] for o in orders["orders"]]

    if order_id in order_ids:
        cancel_order("BTC", order_id)
    else:
        print(f"订单 {order_id} 不存在或已完成")
```

---

### 5. API 错误 (API_ERROR)

与 HyperLiquid API 通信失败。

**常见原因**:

- 网络连接问题
- API 限流
- HyperLiquid 服务问题
- 认证失败

**示例**:

```json
{
  "success": false,
  "error": "API request failed: Rate limit exceeded",
  "error_code": "API_ERROR",
  "details": "Please wait before making more requests"
}
```

**解决方案**:

```python
import time

def retry_with_backoff(func, max_retries=3):
    """带退避的重试机制"""
    for i in range(max_retries):
        result = func()

        if result["success"]:
            return result

        if result.get("error_code") == "API_ERROR":
            if i < max_retries - 1:
                wait_time = 2 ** i  # 指数退避
                print(f"API 错误，{wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print("达到最大重试次数")
                return result
        else:
            # 其他错误不重试
            return result

    return result

# 使用重试机制
result = retry_with_backoff(
    lambda: get_market_data("BTC")
)
```

---

### 6. 价格/数量无效

价格或数量不符合要求。

**示例**:

```json
{
  "success": false,
  "error": "Price must be greater than 0",
  "error_code": "INVALID_PRICE"
}
```

**解决方案**:

```python
# 验证输入
def validate_trade_params(size, price):
    if size <= 0:
        raise ValueError("Size must be greater than 0")
    if price <= 0:
        raise ValueError("Price must be greater than 0")
    return True

try:
    validate_trade_params(0.1, 45000)
    order = place_limit_order("BTC", "buy", 0.1, 45000)
except ValueError as e:
    print(f"参数错误: {e}")
```

## 错误处理模式

### 模式 1: 基础错误检查

最简单的错误处理方式：

```python
result = place_limit_order("BTC", "buy", 0.1, 45000)

if result["success"]:
    print(f"订单成功: {result['order_id']}")
else:
    print(f"订单失败: {result['error']}")
```

### 模式 2: 详细错误处理

根据错误类型采取不同行动：

```python
result = place_limit_order("BTC", "buy", 0.1, 45000)

if not result["success"]:
    error_code = result.get("error_code")
    error_msg = result.get("error")

    if error_code == "INSUFFICIENT_BALANCE":
        print("余额不足，请充值或减少订单大小")
        # 可以尝试减少订单大小

    elif error_code == "VALIDATION_ERROR":
        print(f"参数错误: {error_msg}")
        # 修正参数

    elif error_code == "API_ERROR":
        print("API 错误，稍后重试")
        # 实施重试机制

    else:
        print(f"未知错误: {error_msg}")
```

### 模式 3: 异常处理

结合 try-except 处理：

```python
try:
    # 获取市场数据
    market_data = get_market_data("BTC")

    if not market_data["success"]:
        raise Exception(market_data["error"])

    current_price = float(market_data["data"]["mark_px"])

    # 计算代币数量
    calc = calculate_token_amount_from_dollars("BTC", 100.0)

    if not calc["success"]:
        raise Exception(calc["error"])

    token_amount = calc["token_amount"]

    # 下单
    order = market_open_position("BTC", "buy", token_amount)

    if not order["success"]:
        raise Exception(order["error"])

    print(f"订单成功: {order['order_id']}")

except Exception as e:
    print(f"操作失败: {str(e)}")
    # 记录日志或通知用户
```

### 模式 4: 防御性编程

在操作前进行检查：

```python
def safe_place_order(coin, side, dollar_amount):
    """安全下单函数，包含所有检查"""

    # 1. 检查余额
    balance = get_account_balance()
    if not balance["success"]:
        return {"success": False, "error": "无法获取余额"}

    available = float(balance["data"]["withdrawable"])
    if available < dollar_amount:
        return {
            "success": False,
            "error": f"余额不足: 需要 ${dollar_amount}, 可用 ${available}"
        }

    # 2. 获取当前价格并计算代币数量
    calc = calculate_token_amount_from_dollars(coin, dollar_amount)
    if not calc["success"]:
        return {"success": False, "error": calc["error"]}

    token_amount = calc["token_amount"]

    # 3. 下单
    order = market_open_position(coin, side, token_amount)

    return order

# 使用
result = safe_place_order("BTC", "buy", 100.0)
if result["success"]:
    print("订单成功")
else:
    print(f"订单失败: {result['error']}")
```

## 常见错误场景

### 场景 1: Size 参数误用

**问题**: 用户想买 $20 的 SOL，但直接传 20.0 作为 size

```python
# ❌ 错误 - 会尝试买 20 个 SOL（约 $3000）！
order = market_open_position("SOL", "buy", 20.0)
```

**解决方案**:

```python
# ✅ 正确 - 先计算代币数量
calc = calculate_token_amount_from_dollars("SOL", 20.0)

if calc["success"]:
    order = market_open_position("SOL", "buy", calc["token_amount"])
else:
    print(f"计算失败: {calc['error']}")
```

---

### 场景 2: 为不存在的仓位设置 TP/SL

**问题**: 在没有仓位的情况下设置止盈止损

```python
# ❌ 错误 - 如果没有 BTC 仓位会失败
result = set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)
# 返回: {"success": false, "error": "No position found for BTC"}
```

**解决方案**:

```python
# ✅ 正确 - 先检查仓位
positions = get_open_positions()

if positions["success"]:
    btc_pos = next((p for p in positions["positions"] if p["coin"] == "BTC"), None)

    if btc_pos:
        result = set_take_profit_stop_loss("BTC", tp_price=47000, sl_price=43000)
    else:
        # 如果要新开仓位 + TP/SL，使用 bracket 订单
        calc = calculate_token_amount_from_dollars("BTC", 100.0)
        result = place_bracket_order(
            coin="BTC",
            side="buy",
            size=calc["token_amount"],
            entry_price=45000,
            take_profit_price=47000,
            stop_loss_price=43000
        )
```

---

### 场景 3: 客户端订单 ID 格式错误

**问题**: 客户端订单 ID 格式不正确

```python
# ❌ 错误 - 格式不正确
order = place_limit_order(
    "BTC", "buy", 0.1, 45000,
    client_order_id="my-order-123"  # 应该是 128 位十六进制
)
```

**解决方案**:

```python
# ✅ 正确 - 使用正确的格式
import secrets

# 生成 128 位十六进制 ID
client_order_id = "0x" + secrets.token_hex(16)

order = place_limit_order(
    "BTC", "buy", 0.1, 45000,
    client_order_id=client_order_id
)
```

---

### 场景 4: API 限流

**问题**: 请求过于频繁被限流

```python
# ❌ 错误 - 快速连续请求可能触发限流
for coin in ["BTC", "ETH", "SOL", "AVAX", "MATIC"]:
    data = get_market_data(coin)  # 可能触发限流
```

**解决方案**:

```python
# ✅ 正确 - 添加延迟
import time

for coin in ["BTC", "ETH", "SOL", "AVAX", "MATIC"]:
    data = get_market_data(coin)

    if data["success"]:
        print(f"{coin}: {data['data']['mark_px']}")
    else:
        if data.get("error_code") == "API_ERROR":
            print(f"API 错误，等待重试...")
            time.sleep(2)
            # 重试一次
            data = get_market_data(coin)

    time.sleep(0.5)  # 每次请求间隔 500ms
```

## 日志记录

记录错误以便调试：

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    filename='trading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(operation, result):
    """记录错误信息"""
    if not result["success"]:
        logging.error(
            f"Operation: {operation} | "
            f"Error: {result.get('error')} | "
            f"Code: {result.get('error_code')}"
        )

# 使用
result = place_limit_order("BTC", "buy", 0.1, 45000)
if not result["success"]:
    log_error("place_limit_order", result)
```

## 错误恢复策略

### 自动重试

```python
def auto_retry(func, max_attempts=3, delay=1):
    """自动重试机制"""
    for attempt in range(max_attempts):
        result = func()

        if result["success"]:
            return result

        error_code = result.get("error_code")

        # 可重试的错误
        if error_code in ["API_ERROR"]:
            if attempt < max_attempts - 1:
                print(f"重试 {attempt + 1}/{max_attempts}...")
                time.sleep(delay * (attempt + 1))
                continue

        # 不可重试的错误
        return result

    return result
```

### 降级策略

```python
def get_price_with_fallback(coin):
    """获取价格，失败时使用缓存"""
    result = get_market_data(coin)

    if result["success"]:
        price = float(result["data"]["mark_px"])
        # 缓存价格
        cache[coin] = price
        return price
    else:
        # 使用缓存的价格
        if coin in cache:
            print(f"使用缓存价格 for {coin}")
            return cache[coin]
        else:
            raise Exception(f"无法获取 {coin} 价格且无缓存")
```

## 最佳实践总结

1. **始终检查 `success` 字段**

   ```python
   if result["success"]:
       # 处理成功
   else:
       # 处理错误
   ```

2. **根据错误代码采取行动**

   ```python
   error_code = result.get("error_code")
   if error_code == "INSUFFICIENT_BALANCE":
       # 特定处理
   ```

3. **操作前验证状态**

   ```python
   # 检查仓位存在
   # 检查余额充足
   # 验证参数有效
   ```

4. **使用重试机制**

   ```python
   # API 错误时重试
   # 使用指数退避
   ```

5. **记录所有错误**

   ```python
   logging.error(f"Error: {result['error']}")
   ```

6. **提供友好的错误消息**
   ```python
   if error_code == "INSUFFICIENT_BALANCE":
       print("余额不足，请充值后再试")
   ```

## 相关文档

- [工具 API 参考](tools-reference.md) - 完整的工具列表
- [返回格式](response-format.md) - 返回数据格式说明
- [故障排除](../troubleshooting.md) - 常见问题解决
