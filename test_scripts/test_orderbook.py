#!/usr/bin/env python3
"""
测试订单簿数据获取
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


async def test_orderbook():
    """测试订单簿获取"""
    print("=" * 70)
    print("📖 订单簿测试")
    print("=" * 70)

    # 初始化服务
    main.initialize_service()

    # 测试币种
    coin = "BTC"
    depth = 10

    print(f"\n正在获取 {coin} 订单簿（深度 {depth}）...")

    result = await main.hyperliquid_service.get_orderbook(coin, depth)

    if not result.get("success"):
        print(f"❌ 获取失败: {result.get('error')}")
        return

    orderbook = result.get("orderbook", {})
    bids = orderbook.get("bids", [])
    asks = orderbook.get("asks", [])

    print("\n" + "=" * 70)
    print(f"📖 {coin} 订单簿")
    print("=" * 70)

    # 显示卖盘（从高到低）
    print(f"\n{'卖盘 (Asks)':<30} {'价格':<20} {'数量':<15}")
    print("-" * 70)

    # 显示最低的5个卖单（价格从高到低）
    display_asks = list(reversed(asks[-5:])) if len(asks) >= 5 else list(reversed(asks))
    for ask in display_asks:
        price = float(ask.get("px", 0))
        size = float(ask.get("sz", 0))
        print(f"{'🔴 SELL':<30} ${price:>15,.2f} {size:>12.6f} BTC")

    print("-" * 70)
    print(f"{'💰 市场价格区间':<30}")
    print("-" * 70)

    # 显示买盘（从高到低）
    print(f"\n{'买盘 (Bids)':<30} {'价格':<20} {'数量':<15}")
    print("-" * 70)

    # 显示最高的5个买单
    display_bids = bids[:5] if len(bids) >= 5 else bids
    for bid in display_bids:
        price = float(bid.get("px", 0))
        size = float(bid.get("sz", 0))
        print(f"{'🟢 BUY':<30} ${price:>15,.2f} {size:>12.6f} BTC")

    # 计算买卖价差
    if bids and asks:
        best_bid = float(bids[0].get("px", 0))
        best_ask = float(asks[0].get("px", 0))
        spread = best_ask - best_bid
        spread_pct = (spread / best_bid) * 100 if best_bid > 0 else 0

        print("\n" + "=" * 70)
        print("📊 市场统计")
        print("=" * 70)
        print(f"最佳买价: ${best_bid:,.2f}")
        print(f"最佳卖价: ${best_ask:,.2f}")
        print(f"买卖价差: ${spread:,.2f} ({spread_pct:.4f}%)")

    print("\n" + "=" * 70)
    print(f"✅ 成功获取 {coin} 订单簿数据")
    print(f"   买单: {len(bids)} 档")
    print(f"   卖单: {len(asks)} 档")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_orderbook())
