# 账户管理

本页面介绍如何管理 HyperLiquid 账户、仓位和资金。

## 账户信息

### 查看余额

```python
balance = get_account_balance()

if balance["success"]:
    data = balance["data"]
    print(f"账户总值: ${data['account_value']}")
    print(f"可用余额: ${data['withdrawable']}")
    print(f"已用保证金: ${data['total_margin_used']}")
```

**字段说明**:

- `account_value`: 账户总价值（USD）
- `withdrawable`: 可提取金额
- `total_margin_used`: 已使用的保证金
- `total_ntl_pos`: 仓位名义价值
- `total_raw_usd`: 原始 USD 余额

### 账户概览

一次性获取所有信息：

```python
summary = get_account_summary()

if summary["success"]:
    s = summary["summary"]

    # 余额信息
    balance = s["balance"]
    print(f"账户总值: ${balance['account_value']}")

    # 仓位信息
    print(f"开仓数量: {s['total_positions']}")
    for pos in s["positions"]:
        print(f"  {pos['coin']}: {pos['szi']} @ ${pos['entry_px']}")

    # 订单信息
    print(f"未成交订单: {s['total_orders']}")
```

## 仓位管理

### 查看所有仓位

```python
positions = get_open_positions()

if positions["success"]:
    for pos in positions["positions"]:
        coin = pos["coin"]
        size = pos["szi"]
        entry = pos["entry_px"]
        pnl = pos["unrealized_pnl"]

        direction = "多" if float(size) > 0 else "空"
        print(f"{coin} {direction}仓: {abs(float(size))} @ ${entry}")
        print(f"  未实现盈亏: ${pnl}")
```

### 仓位详细信息

```python
positions = get_open_positions()

if positions["success"]:
    for pos in positions["positions"]:
        print(f"""
仓位: {pos['coin']}
方向: {'做多' if float(pos['szi']) > 0 else '做空'}
数量: {abs(float(pos['szi']))}
开仓均价: ${pos['entry_px']}
仓位价值: ${pos['position_value']}
未实现盈亏: ${pos['unrealized_pnl']}
回报率: {pos['return_on_equity']}
杠杆: {pos['leverage']}
强平价: ${pos['liquidation_px']}
        """)
```

### 检查特定仓位

```python
def get_position(coin):
    """获取特定币种的仓位"""
    positions = get_open_positions()

    if positions["success"]:
        return next(
            (p for p in positions["positions"] if p["coin"] == coin),
            None
        )
    return None

# 使用
btc_pos = get_position("BTC")
if btc_pos:
    print(f"BTC 仓位大小: {btc_pos['szi']}")
else:
    print("没有 BTC 仓位")
```

### 计算仓位盈亏

```python
def calculate_pnl(coin):
    """计算仓位盈亏详情"""
    pos = get_position(coin)
    if not pos:
        return None

    size = abs(float(pos["szi"]))
    entry_price = float(pos["entry_px"])

    # 获取当前价格
    market = get_market_data(coin)
    current_price = float(market["data"]["mark_px"])

    # 计算盈亏
    is_long = float(pos["szi"]) > 0
    if is_long:
        pnl = (current_price - entry_price) * size
        pnl_pct = (current_price / entry_price - 1) * 100
    else:
        pnl = (entry_price - current_price) * size
        pnl_pct = (entry_price / current_price - 1) * 100

    return {
        "unrealized_pnl": pnl,
        "pnl_percentage": pnl_pct,
        "entry_price": entry_price,
        "current_price": current_price
    }

# 使用
pnl = calculate_pnl("BTC")
if pnl:
    print(f"盈亏: ${pnl['unrealized_pnl']:.2f} ({pnl['pnl_percentage']:.2f}%)")
```

## 杠杆管理

### 更新杠杆

```python
# 设置 BTC 为 10x 全仓杠杆
result = update_leverage("BTC", leverage=10, cross_margin=True)

# 设置 ETH 为 5x 逐仓杠杆
result = update_leverage("ETH", leverage=5, cross_margin=False)
```

### 全仓 vs 逐仓

**全仓模式** (`cross_margin=True`):

- ✅ 使用账户全部可用余额作为保证金
- ✅ 降低强平风险
- ❌ 一个仓位爆仓可能影响其他仓位

**逐仓模式** (`cross_margin=False`):

- ✅ 每个仓位独立，风险隔离
- ✅ 最大损失仅为该仓位保证金
- ❌ 更容易触发强平

### 批量设置杠杆

```python
def set_leverage_for_all(leverage, cross_margin=True):
    """为所有仓位设置相同杠杆"""
    positions = get_open_positions()

    if positions["success"]:
        for pos in positions["positions"]:
            coin = pos["coin"]
            result = update_leverage(coin, leverage, cross_margin)

            if result["success"]:
                print(f"✅ {coin}: {leverage}x")
            else:
                print(f"❌ {coin}: {result['error']}")

# 使用：所有仓位设置为 5x 全仓
set_leverage_for_all(5, cross_margin=True)
```

## 资金划转

### 现货和合约间转账

```python
# 从现货转 1000 到合约账户
result = transfer_between_spot_and_perp(
    amount=1000.0,
    to_perp=True
)

# 从合约转 500 到现货账户
result = transfer_between_spot_and_perp(
    amount=500.0,
    to_perp=False
)

if result["success"]:
    print(f"✅ 转账成功: {result['message']}")
```

### 检查余额后转账

```python
def safe_transfer_to_perp(amount):
    """安全地从现货转到合约"""
    # TODO: 需要先实现获取现货余额的功能
    # 这里假设有足够余额

    result = transfer_between_spot_and_perp(amount, to_perp=True)

    if result["success"]:
        print(f"✅ 已转入 ${amount} 到合约账户")
    else:
        print(f"❌ 转账失败: {result['error']}")
```

## 交易历史

### 查看最近交易

```python
# 最近 7 天的交易
history = get_trade_history(days=7)

if history["success"]:
    for trade in history["trades"]:
        print(f"""
时间: {trade['time']}
币种: {trade['coin']}
方向: {trade['side']}
数量: {trade['size']}
价格: ${trade['price']}
        """)
```

### 查看特定币种的交易

```python
def get_coin_trades(coin, days=7):
    """获取特定币种的交易历史"""
    history = get_trade_history(days=days)

    if history["success"]:
        coin_trades = [
            t for t in history["trades"]
            if t["coin"] == coin
        ]
        return coin_trades
    return []

# 使用
btc_trades = get_coin_trades("BTC", days=30)
print(f"BTC 最近 30 天交易: {len(btc_trades)} 笔")
```

### 计算交易统计

```python
def calculate_trade_stats(coin, days=30):
    """计算交易统计数据"""
    trades = get_coin_trades(coin, days)

    if not trades:
        return None

    total_volume = sum(float(t["size"]) * float(t["price"]) for t in trades)
    avg_price = sum(float(t["price"]) for t in trades) / len(trades)

    buys = [t for t in trades if t["side"] == "buy"]
    sells = [t for t in trades if t["side"] == "sell"]

    return {
        "total_trades": len(trades),
        "total_volume": total_volume,
        "average_price": avg_price,
        "buy_count": len(buys),
        "sell_count": len(sells),
        "days": days
    }

# 使用
stats = calculate_trade_stats("BTC", days=30)
if stats:
    print(f"""
BTC 交易统计 (最近 {stats['days']} 天):
总交易次数: {stats['total_trades']}
总交易量: ${stats['total_volume']:.2f}
平均价格: ${stats['average_price']:.2f}
买入: {stats['buy_count']} | 卖出: {stats['sell_count']}
    """)
```

## 订单管理

### 查看未成交订单

```python
orders = get_open_orders()

if orders["success"]:
    print(f"未成交订单: {orders['total_orders']}")

    for order in orders["orders"]:
        print(f"""
订单 ID: {order['order_id']}
币种: {order['coin']}
方向: {order['side']}
数量: {order['sz']}
价格: ${order['limit_px']}
类型: {order['order_type']}
        """)
```

### 按币种分组订单

```python
from collections import defaultdict

def group_orders_by_coin():
    """按币种分组订单"""
    orders = get_open_orders()

    if not orders["success"]:
        return {}

    grouped = defaultdict(list)
    for order in orders["orders"]:
        grouped[order["coin"]].append(order)

    return dict(grouped)

# 使用
grouped = group_orders_by_coin()
for coin, coin_orders in grouped.items():
    print(f"{coin}: {len(coin_orders)} 个订单")
```

### 清理所有订单

```python
def cleanup_all_orders():
    """取消所有未成交订单"""
    result = cancel_all_orders()

    if result["success"]:
        print(f"✅ 已取消 {result['cancelled_count']} 个订单")
    else:
        print(f"❌ 取消失败: {result['error']}")

# 使用
cleanup_all_orders()
```

## 风险管理

### 计算账户风险

```python
def calculate_account_risk():
    """计算账户风险指标"""
    summary = get_account_summary()

    if not summary["success"]:
        return None

    balance = summary["summary"]["balance"]
    account_value = float(balance["account_value"])
    margin_used = float(balance["total_margin_used"])

    # 保证金使用率
    margin_ratio = (margin_used / account_value) * 100 if account_value > 0 else 0

    # 计算总未实现盈亏
    positions = summary["summary"]["positions"]
    total_unrealized_pnl = sum(float(p["unrealized_pnl"]) for p in positions)

    # 风险等级
    if margin_ratio > 80:
        risk_level = "高风险"
    elif margin_ratio > 50:
        risk_level = "中风险"
    else:
        risk_level = "低风险"

    return {
        "account_value": account_value,
        "margin_used": margin_used,
        "margin_ratio": margin_ratio,
        "risk_level": risk_level,
        "total_unrealized_pnl": total_unrealized_pnl,
        "free_margin": account_value - margin_used
    }

# 使用
risk = calculate_account_risk()
if risk:
    print(f"""
账户风险分析:
账户总值: ${risk['account_value']:.2f}
已用保证金: ${risk['margin_used']:.2f}
保证金使用率: {risk['margin_ratio']:.1f}%
风险等级: {risk['risk_level']}
未实现盈亏: ${risk['total_unrealized_pnl']:.2f}
可用保证金: ${risk['free_margin']:.2f}
    """)
```

### 设置仓位限制

```python
def check_position_limit(coin, new_size_usd, max_position_pct=20.0):
    """检查是否超过仓位限制

    Args:
        coin: 币种
        new_size_usd: 新增仓位美元价值
        max_position_pct: 单个仓位最大占比（默认20%）
    """
    balance = get_account_balance()
    if not balance["success"]:
        return False

    account_value = float(balance["data"]["account_value"])
    max_size = account_value * (max_position_pct / 100)

    # 检查现有仓位
    pos = get_position(coin)
    current_size = 0
    if pos:
        current_size = float(pos["position_value"])

    total_size = current_size + new_size_usd

    if total_size > max_size:
        print(f"❌ 超过仓位限制!")
        print(f"当前: ${current_size:.2f}")
        print(f"新增: ${new_size_usd:.2f}")
        print(f"总计: ${total_size:.2f}")
        print(f"限制: ${max_size:.2f} ({max_position_pct}%)")
        return False

    return True

# 使用
if check_position_limit("BTC", 5000.0, max_position_pct=25.0):
    print("✅ 未超过仓位限制，可以开仓")
```

## 资金费率

### 查看资金费率历史

```python
# 查看 BTC 最近 7 天的资金费率
funding = get_funding_history("BTC", days=7)

if funding["success"]:
    for rate in funding["funding_history"]:
        print(f"时间: {rate['time']}")
        print(f"费率: {rate['fundingRate']}")
        print(f"溢价: {rate['premium']}")
        print("---")
```

### 计算资金费用

```python
def estimate_funding_cost(coin, days=30):
    """估算资金费用"""
    # 获取仓位
    pos = get_position(coin)
    if not pos:
        return None

    position_value = float(pos["position_value"])

    # 获取资金费率历史
    funding = get_funding_history(coin, days=days)
    if not funding["success"]:
        return None

    # 计算平均费率
    rates = [float(r["fundingRate"]) for r in funding["funding_history"]]
    avg_rate = sum(rates) / len(rates) if rates else 0

    # 估算费用（每8小时收取一次）
    funding_periods = days * 3  # 每天3次
    estimated_cost = position_value * avg_rate * funding_periods

    return {
        "avg_funding_rate": avg_rate,
        "estimated_cost": estimated_cost,
        "days": days,
        "position_value": position_value
    }

# 使用
cost = estimate_funding_cost("BTC", days=30)
if cost:
    print(f"""
资金费用估算 (30天):
仓位价值: ${cost['position_value']:.2f}
平均费率: {cost['avg_funding_rate']:.6f}
估算费用: ${cost['estimated_cost']:.2f}
    """)
```

## 最佳实践

### 1. 定期检查账户状态

```python
def daily_account_check():
    """每日账户检查"""
    print("=== 每日账户检查 ===\n")

    # 1. 余额
    balance = get_account_balance()
    if balance["success"]:
        print(f"账户总值: ${balance['data']['account_value']}")

    # 2. 仓位
    positions = get_open_positions()
    if positions["success"]:
        print(f"开仓数: {positions['total_positions']}")
        for pos in positions["positions"]:
            pnl = float(pos["unrealized_pnl"])
            emoji = "📈" if pnl > 0 else "📉"
            print(f"  {emoji} {pos['coin']}: ${pnl:.2f}")

    # 3. 风险
    risk = calculate_account_risk()
    if risk:
        print(f"保证金使用率: {risk['margin_ratio']:.1f}%")
        print(f"风险等级: {risk['risk_level']}")

# 每天运行一次
daily_account_check()
```

### 2. 自动止损检查

```python
def check_stop_loss_coverage():
    """检查所有仓位是否设置了止损"""
    positions = get_open_positions()
    orders = get_open_orders()

    if not positions["success"] or not orders["success"]:
        return

    for pos in positions["positions"]:
        coin = pos["coin"]

        # 检查是否有止损订单
        has_stop_loss = any(
            o["coin"] == coin and o["order_type"] == "Stop"
            for o in orders["orders"]
        )

        if not has_stop_loss:
            print(f"⚠️  {coin} 没有设置止损!")

check_stop_loss_coverage()
```

### 3. 仓位再平衡

```python
def rebalance_portfolio(target_allocations):
    """按目标比例重新平衡仓位

    Args:
        target_allocations: {"BTC": 50, "ETH": 30, "SOL": 20}
    """
    balance = get_account_balance()
    total_value = float(balance["data"]["account_value"])

    for coin, target_pct in target_allocations.items():
        target_value = total_value * (target_pct / 100)

        pos = get_position(coin)
        current_value = float(pos["position_value"]) if pos else 0

        diff = target_value - current_value

        if abs(diff) > total_value * 0.01:  # 超过1%才调整
            print(f"{coin}: 调整 ${diff:.2f}")
            # TODO: 实现调整逻辑

# 使用
rebalance_portfolio({"BTC": 50, "ETH": 30, "SOL": 20})
```

## 相关文档

- [交易工具](trading-tools.md) - 交易工具使用
- [市场数据](market-data.md) - 获取市场数据
- [API 参考](../api/tools-reference.md) - 完整 API 文档
- [故障排除](../troubleshooting.md) - 常见问题
