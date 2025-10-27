#!/usr/bin/env python3
"""
测试账户信息获取
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


async def test_account_info():
    """测试账户信息"""
    print("=" * 70)
    print("👤 账户信息测试")
    print("=" * 70)

    # 初始化服务
    main.initialize_service()
    config = main.get_config()

    print(f"\n📍 配置信息")
    print("-" * 70)
    print(f"网络: {'测试网 (Testnet)' if config.testnet else '主网 (Mainnet)'}")
    print(f"账户地址: {config.account_address}")

    # 1. 获取账户余额
    print(f"\n{'=' * 70}")
    print("💰 账户余额")
    print(f"{'=' * 70}")

    balance = await main.hyperliquid_service.get_account_balance()

    if balance.get("success"):
        data = balance.get("data", {})
        print(f"\n总权益: ${data.get('account_value', 'N/A')}")
        print(f"可用余额: ${data.get('withdrawable', 'N/A')}")
        print(f"保证金使用: ${data.get('margin_used', 'N/A')}")
    else:
        print(f"❌ 获取失败: {balance.get('error')}")

    # 2. 获取持仓
    print(f"\n{'=' * 70}")
    print("📊 持仓信息")
    print(f"{'=' * 70}")

    positions = await main.hyperliquid_service.get_open_positions()

    if positions.get("success"):
        pos_list = positions.get("positions", [])
        total = positions.get("total_positions", 0)

        print(f"\n持仓数量: {total}")

        if pos_list:
            print(
                f"\n{'币种':<8} {'方向':<8} {'数量':<15} {'入场价':<15} {'未实现盈亏':<15}"
            )
            print("-" * 70)

            for pos in pos_list:
                coin = pos.get("coin", "N/A")
                side = pos.get("side", "N/A")
                size = pos.get("size", "N/A")
                entry_price = pos.get("entry_price", "N/A")
                pnl = pos.get("unrealized_pnl", "N/A")

                print(f"{coin:<8} {side:<8} {size:<15} {entry_price:<15} {pnl:<15}")
        else:
            print("\n(当前无持仓)")
    else:
        print(f"❌ 获取失败: {positions.get('error')}")

    # 3. 获取未平仓订单
    print(f"\n{'=' * 70}")
    print("📋 未平仓订单")
    print(f"{'=' * 70}")

    orders = await main.hyperliquid_service.get_open_orders()

    if orders.get("success"):
        order_list = orders.get("orders", [])
        total = orders.get("total_orders", 0)

        print(f"\n订单数量: {total}")

        if order_list:
            print(f"\n{'币种':<8} {'方向':<8} {'数量':<15} {'价格':<15} {'订单ID':<12}")
            print("-" * 70)

            for order in order_list[:10]:  # 只显示前10个
                coin = order.get("coin", "N/A")
                side = order.get("side", "N/A")
                size = order.get("sz", "N/A")
                price = order.get("limitPx", "N/A")
                oid = order.get("oid", "N/A")

                print(f"{coin:<8} {side:<8} {size:<15} {price:<15} {oid:<12}")

            if total > 10:
                print(f"\n... 还有 {total - 10} 个订单未显示")
        else:
            print("\n(当前无未平仓订单)")
    else:
        print(f"❌ 获取失败: {orders.get('error')}")

    # 4. 获取交易历史（最近7天）
    print(f"\n{'=' * 70}")
    print("📜 交易历史（最近7天）")
    print(f"{'=' * 70}")

    trades = await main.hyperliquid_service.get_trade_history(7)

    if trades.get("success"):
        trade_list = trades.get("trades", [])
        total = trades.get("total_trades", 0)

        print(f"\n交易数量: {total}")

        if trade_list:
            print(f"\n显示最近 10 笔交易:")
            print(f"\n{'币种':<8} {'方向':<8} {'数量':<15} {'价格':<15} {'时间':<20}")
            print("-" * 70)

            for trade in trade_list[:10]:
                coin = trade.get("coin", "N/A")
                side = trade.get("side", "N/A")
                size = trade.get("sz", "N/A")
                price = trade.get("px", "N/A")
                time = trade.get("time", "N/A")

                # 格式化时间
                if time != "N/A" and isinstance(time, (int, float)):
                    from datetime import datetime

                    dt = datetime.fromtimestamp(time / 1000)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = str(time)

                print(f"{coin:<8} {side:<8} {size:<15} {price:<15} {time_str:<20}")

            if total > 10:
                print(f"\n... 还有 {total - 10} 笔交易未显示")
        else:
            print("\n(最近7天无交易)")
    else:
        print(f"❌ 获取失败: {trades.get('error')}")

    print("\n" + "=" * 70)
    print("✅ 账户信息测试完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_account_info())
