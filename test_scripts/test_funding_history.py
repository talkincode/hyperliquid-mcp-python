#!/usr/bin/env python3
"""
测试资金费率历史获取
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


async def test_funding_history():
    """测试资金费率历史"""
    print("=" * 70)
    print("💰 资金费率历史测试")
    print("=" * 70)

    # 初始化服务
    main.initialize_service()

    # 测试币种
    test_coins = ["BTC", "ETH", "SOL"]
    days = 7

    print(f"\n获取过去 {days} 天的资金费率...\n")

    for coin in test_coins:
        print(f"{'=' * 70}")
        print(f"📊 {coin} 资金费率（过去 {days} 天）")
        print(f"{'=' * 70}")

        result = await main.hyperliquid_service.get_funding_history(coin, days)

        if not result.get("success"):
            print(f"❌ 获取失败: {result.get('error')}\n")
            continue

        funding_data = result.get("funding_history", [])

        if not funding_data:
            print(f"⚠️  未找到资金费率数据\n")
            continue

        # 显示最近的资金费率记录
        print(f"\n最近 10 条记录:\n")
        print(f"{'时间':<20} {'费率 (%)':<15} {'年化 (%)':<15}")
        print("-" * 70)

        # 显示最近10条
        recent_data = funding_data[:10] if len(funding_data) >= 10 else funding_data

        for record in recent_data:
            time = record.get("time", "N/A")
            funding_rate = record.get("funding", "N/A")

            # 将时间戳转换为可读格式
            if time != "N/A" and isinstance(time, (int, float)):
                from datetime import datetime

                dt = datetime.fromtimestamp(time / 1000)  # 毫秒转秒
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                time_str = str(time)

            # 计算年化（假设每8小时一次，即一天3次）
            if funding_rate != "N/A":
                try:
                    rate = float(funding_rate)
                    rate_pct = rate * 100
                    annualized = rate * 3 * 365 * 100  # 年化百分比
                    print(f"{time_str:<20} {rate_pct:>12.6f}% {annualized:>12.2f}%")
                except:
                    print(f"{time_str:<20} {funding_rate:<15} {'N/A':<15}")
            else:
                print(f"{time_str:<20} {'N/A':<15} {'N/A':<15}")

        # 计算平均资金费率
        try:
            valid_rates = [
                float(r.get("funding", 0))
                for r in funding_data
                if r.get("funding") != "N/A"
            ]
            if valid_rates:
                avg_rate = sum(valid_rates) / len(valid_rates)
                avg_pct = avg_rate * 100
                avg_annualized = avg_rate * 3 * 365 * 100

                print("\n" + "-" * 70)
                print(f"平均资金费率: {avg_pct:.6f}% (年化: {avg_annualized:.2f}%)")
                print(f"记录数量: {len(funding_data)}")
        except Exception as e:
            print(f"\n⚠️  无法计算平均值: {e}")

        print()

    print("=" * 70)
    print("✅ 资金费率历史测试完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_funding_history())
