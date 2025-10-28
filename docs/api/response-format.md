# 返回格式

所有 HyperLiquid MCP Server 工具都遵循统一的返回格式规范。

## 标准响应格式

### 成功响应

所有成功的 API 调用都会返回包含 `success: true` 的 JSON 对象：

```json
{
  "success": true,
  "data": {
    /* 具体数据内容 */
  }
}
```

### 错误响应

所有失败的 API 调用都会返回包含 `success: false` 的 JSON 对象：

```json
{
  "success": false,
  "error": "错误描述信息",
  "error_code": "ERROR_CODE"
}
```

## 常见返回类型

### 账户信息

#### get_account_balance

```json
{
  "success": true,
  "data": {
    "account_value": "12345.67",
    "total_margin_used": "2345.67",
    "total_ntl_pos": "10000.00",
    "total_raw_usd": "12345.67",
    "withdrawable": "10000.00"
  }
}
```

#### get_open_positions

```json
{
  "success": true,
  "positions": [
    {
      "coin": "BTC",
      "szi": "0.1",
      "entry_px": "45000.00",
      "position_value": "4512.30",
      "unrealized_pnl": "12.30",
      "return_on_equity": "0.27",
      "leverage": "10x",
      "liquidation_px": "40500.00"
    }
  ],
  "total_positions": 1
}
```

#### get_open_orders

```json
{
  "success": true,
  "orders": [
    {
      "order_id": 123456789,
      "coin": "ETH",
      "side": "buy",
      "limit_px": "3000.00",
      "sz": "1.0",
      "timestamp": 1704067200000,
      "order_type": "Limit"
    }
  ],
  "total_orders": 1
}
```

### 交易操作

#### place_limit_order / market_open_position

```json
{
  "success": true,
  "order_result": {
    "status": {
      "filled": {
        "totalSz": "0.1",
        "avgPx": "45123.45",
        "oid": 123456789
      }
    }
  },
  "order_id": 123456789,
  "filled": true,
  "average_price": "45123.45"
}
```

#### market_close_position

```json
{
  "success": true,
  "order_result": {
    "status": "closed",
    "closed_size": "0.1",
    "avg_close_price": "45678.90"
  },
  "message": "Position closed successfully"
}
```

#### place_bracket_order

```json
{
  "success": true,
  "bulk_result": {
    "entry_order": {
      "order_id": 123456,
      "status": "placed"
    },
    "take_profit_order": {
      "order_id": 123457,
      "status": "placed",
      "trigger_price": "47000.00"
    },
    "stop_loss_order": {
      "order_id": 123458,
      "status": "placed",
      "trigger_price": "43000.00"
    }
  },
  "message": "Bracket order placed successfully"
}
```

### 订单管理

#### cancel_order

```json
{
  "success": true,
  "cancelled_order_id": 123456789,
  "message": "Order cancelled successfully"
}
```

#### cancel_all_orders

```json
{
  "success": true,
  "cancelled_count": 5,
  "message": "Cancelled 5 orders for BTC"
}
```

或（全部取消）：

```json
{
  "success": true,
  "cancelled_count": 12,
  "message": "Cancelled all 12 orders"
}
```

#### modify_order

```json
{
  "success": true,
  "order_result": {
    "order_id": 123456789,
    "new_size": "2.0",
    "new_price": "3100.00",
    "status": "modified"
  },
  "message": "Order modified successfully"
}
```

### 市场数据

#### get_market_data

```json
{
  "success": true,
  "data": {
    "coin": "BTC",
    "mark_px": "45123.45",
    "mid_px": "45122.50",
    "premium": "0.0001",
    "funding": "0.0001",
    "open_interest": "123456.78",
    "prev_day_px": "44500.00",
    "day_ntl_vlm": "1234567890.00"
  }
}
```

#### get_orderbook

```json
{
  "success": true,
  "orderbook": {
    "coin": "BTC",
    "time": 1704067200000,
    "levels": [
      [
        {
          "px": "45125.00",
          "sz": "1.5",
          "n": 3
        },
        {
          "px": "45120.00",
          "sz": "2.0",
          "n": 5
        }
      ],
      [
        {
          "px": "45115.00",
          "sz": "1.2",
          "n": 2
        },
        {
          "px": "45110.00",
          "sz": "1.8",
          "n": 4
        }
      ]
    ]
  }
}
```

#### get_funding_history

```json
{
  "success": true,
  "funding_history": [
    {
      "coin": "BTC",
      "fundingRate": "0.0001",
      "premium": "0.00005",
      "time": 1704067200000
    }
  ],
  "days": 7
}
```

### 账户设置

#### update_leverage

```json
{
  "success": true,
  "leverage": 10,
  "leverage_type": "cross",
  "coin": "BTC",
  "message": "Leverage updated to 10x cross margin"
}
```

#### transfer_between_spot_and_perp

```json
{
  "success": true,
  "amount": 1000.0,
  "from": "spot",
  "to": "perp",
  "message": "Transferred $1000.00 from spot to perpetual account"
}
```

### 止盈止损

#### set_take_profit_stop_loss

```json
{
  "success": true,
  "tp_order": {
    "order_id": 123457,
    "trigger_price": "47000.00",
    "size": "0.1"
  },
  "sl_order": {
    "order_id": 123458,
    "trigger_price": "43000.00",
    "size": "0.1"
  },
  "message": "TP/SL orders placed successfully (OCO group)"
}
```

### 实用工具

#### calculate_token_amount_from_dollars

```json
{
  "success": true,
  "coin": "SOL",
  "dollar_amount": 20.0,
  "current_price": 150.0,
  "token_amount": 0.133333,
  "calculation": "$20.00 ÷ $150.00 = 0.133333 SOL"
}
```

#### get_account_summary

```json
{
  "success": true,
  "summary": {
    "balance": {
      "account_value": "12345.67",
      "withdrawable": "10000.00"
    },
    "positions": [
      {
        "coin": "BTC",
        "szi": "0.1",
        "unrealized_pnl": "12.30"
      }
    ],
    "orders": [
      {
        "order_id": 123456,
        "coin": "ETH",
        "side": "buy"
      }
    ],
    "total_positions": 1,
    "total_orders": 1
  }
}
```

## 错误响应格式

### 验证错误

```json
{
  "success": false,
  "error": "Invalid coin symbol: INVALID",
  "error_code": "VALIDATION_ERROR"
}
```

### 余额不足

```json
{
  "success": false,
  "error": "Insufficient balance to place order",
  "error_code": "INSUFFICIENT_BALANCE",
  "required": "1000.00",
  "available": "500.00"
}
```

### 仓位未找到

```json
{
  "success": false,
  "error": "No position found for BTC",
  "error_code": "POSITION_NOT_FOUND",
  "coin": "BTC"
}
```

### 订单未找到

```json
{
  "success": false,
  "error": "Order not found: 123456",
  "error_code": "ORDER_NOT_FOUND",
  "order_id": 123456
}
```

### API 错误

```json
{
  "success": false,
  "error": "API request failed: Rate limit exceeded",
  "error_code": "API_ERROR",
  "details": "Please wait before making more requests"
}
```

## 错误代码列表

| 错误代码               | 说明             | 解决方案                               |
| ---------------------- | ---------------- | -------------------------------------- |
| `VALIDATION_ERROR`     | 输入参数验证失败 | 检查参数格式和取值范围                 |
| `INSUFFICIENT_BALANCE` | 账户余额不足     | 充值或减少订单大小                     |
| `POSITION_NOT_FOUND`   | 未找到仓位       | 确认仓位存在后再操作                   |
| `ORDER_NOT_FOUND`      | 未找到订单       | 检查订单 ID 是否正确                   |
| `API_ERROR`            | API 调用失败     | 查看详细错误信息，可能是网络或限流问题 |
| `INVALID_PRICE`        | 价格无效         | 价格必须大于 0                         |
| `INVALID_SIZE`         | 数量无效         | 数量必须大于 0                         |
| `RATE_LIMIT_EXCEEDED`  | 超过 API 限流    | 降低请求频率                           |

## 字段说明

### 通用字段

| 字段         | 类型    | 说明                 |
| ------------ | ------- | -------------------- |
| `success`    | boolean | 是否成功             |
| `error`      | string  | 错误描述（仅失败时） |
| `error_code` | string  | 错误代码（仅失败时） |
| `message`    | string  | 操作消息             |

### 仓位字段

| 字段               | 类型   | 说明                           |
| ------------------ | ------ | ------------------------------ |
| `coin`             | string | 交易对                         |
| `szi`              | string | 仓位大小（正数为多，负数为空） |
| `entry_px`         | string | 开仓均价                       |
| `position_value`   | string | 仓位价值                       |
| `unrealized_pnl`   | string | 未实现盈亏                     |
| `return_on_equity` | string | 回报率                         |
| `leverage`         | string | 杠杆倍数                       |
| `liquidation_px`   | string | 强平价格                       |

### 订单字段

| 字段         | 类型    | 说明                 |
| ------------ | ------- | -------------------- |
| `order_id`   | integer | 订单 ID              |
| `coin`       | string  | 交易对               |
| `side`       | string  | 订单方向（buy/sell） |
| `limit_px`   | string  | 限价价格             |
| `sz`         | string  | 订单大小             |
| `timestamp`  | integer | 时间戳（毫秒）       |
| `order_type` | string  | 订单类型             |

### 成交字段

| 字段      | 类型    | 说明     |
| --------- | ------- | -------- |
| `totalSz` | string  | 成交总量 |
| `avgPx`   | string  | 成交均价 |
| `oid`     | integer | 订单 ID  |

## 最佳实践

### 1. 始终检查 success 字段

```python
result = get_account_balance()
if result["success"]:
    balance = result["data"]
    print(f"余额: {balance['account_value']}")
else:
    print(f"错误: {result['error']}")
```

### 2. 处理不同的返回结构

不同的工具可能使用不同的数据键：

```python
# 账户数据使用 "data"
balance = get_account_balance()
if balance["success"]:
    data = balance["data"]

# 订单结果使用 "order_result"
order = place_limit_order(...)
if order["success"]:
    result = order["order_result"]

# 列表数据使用特定键名
positions = get_open_positions()
if positions["success"]:
    pos_list = positions["positions"]
```

### 3. 错误处理

```python
try:
    result = market_open_position("BTC", "buy", 0.1)
    if not result["success"]:
        error_code = result.get("error_code")
        if error_code == "INSUFFICIENT_BALANCE":
            print("余额不足，请充值")
        elif error_code == "VALIDATION_ERROR":
            print(f"参数错误: {result['error']}")
        else:
            print(f"操作失败: {result['error']}")
except Exception as e:
    print(f"异常: {str(e)}")
```

### 4. 提取关键信息

```python
# 获取订单 ID
order = place_limit_order("ETH", "buy", 1.0, 3000)
if order["success"]:
    order_id = order.get("order_id") or order["order_result"]["status"]["filled"]["oid"]
    print(f"订单 ID: {order_id}")
```

## 相关文档

- [工具 API 参考](tools-reference.md) - 完整的工具列表
- [错误处理](error-handling.md) - 错误处理最佳实践
- [故障排除](../troubleshooting.md) - 常见问题解决
