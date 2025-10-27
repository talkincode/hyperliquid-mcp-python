#!/usr/bin/env python3
"""
测试市场数据获取功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


async def test_market_data():
    """测试市场数据获取"""
    print("=" * 70)
    print("📊 市场数据测试")
    print("=" * 70)
    
    # 初始化服务
    main.initialize_service()
    
    # 测试的币种列表
    test_coins = ["BTC", "ETH", "SOL", "ARB", "OP"]
    
    print(f"\n测试 {len(test_coins)} 个币种的市场数据...\n")
    
    results = []
    
    for coin in test_coins:
        print(f"正在获取 {coin} 市场数据...")
        result = await main.hyperliquid_service.get_market_data(coin)
        
        if result.get("success"):
            data = result.get("market_data", {})
            results.append({
                "coin": coin,
                "price": data.get("mid_price", "N/A"),
                "volume": data.get("day_ntl_vlm", "N/A"),
                "funding": data.get("funding", "N/A"),
                "oi": data.get("open_interest", "N/A")
            })
        else:
            print(f"  ⚠️  获取失败: {result.get('error')}")
    
    # 显示汇总表格
    print("\n" + "=" * 70)
    print("📊 市场数据汇总")
    print("=" * 70)
    print(f"\n{'币种':<8} {'当前价格':<15} {'24h成交量':<15} {'资金费率':<12} {'未平仓':<12}")
    print("-" * 70)
    
    for r in results:
        price = f"${r['price']}" if r['price'] != "N/A" else "N/A"
        volume = f"${r['volume']}" if r['volume'] != "N/A" else "N/A"
        print(f"{r['coin']:<8} {price:<15} {volume:<15} {r['funding']:<12} {r['oi']:<12}")
    
    print("\n" + "=" * 70)
    print(f"✅ 成功获取 {len(results)}/{len(test_coins)} 个币种的市场数据")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_market_data())
