#!/usr/bin/env python3
"""
测试小额订单 - 验证账户是否真的有余额
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import main


async def test_small_order():
    """测试一个非常小的订单"""
    print("=" * 70)
    print("测试小额订单 - 验证账户余额")
    print("=" * 70)
    
    # 初始化服务
    main.initialize_service()
    
    print("\n📊 步骤 1: 获取 BTC 当前价格")
    print("-" * 70)
    
    market_data = await main.hyperliquid_service.get_market_data("BTC")
    if not market_data.get("success"):
        print(f"❌ 获取市场数据失败: {market_data.get('error')}")
        return
    
    current_price = float(market_data["market_data"]["mid_price"])
    print(f"✅ BTC 当前价格: ${current_price:,.2f}")
    
    # 计算一个非常小的订单 - 大约 $5 的 BTC
    test_size = 5.0 / current_price  # $5 worth of BTC
    # 设置一个偏离市价的限价单，这样不会立即成交
    limit_price = current_price * 0.95  # 比市价低 5%
    
    print(f"\n📊 步骤 2: 尝试下一个测试订单")
    print("-" * 70)
    print(f"   币种: BTC")
    print(f"   方向: 买入 (做多)")
    print(f"   数量: {test_size:.8f} BTC (约 $5)")
    print(f"   限价: ${limit_price:,.2f} (比市价低 5%，不会立即成交)")
    print(f"\n这个订单不会立即成交，只是测试账户是否有足够余额...")
    
    confirm = input("\n是否继续测试下单？(yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("\n已取消测试")
        return
    
    print("\n正在下单...")
    result = await main.hyperliquid_service.place_order(
        coin="BTC",
        is_buy=True,
        sz=test_size,
        limit_px=limit_price,
        reduce_only=False
    )
    
    print("\n" + "=" * 70)
    print("📊 订单结果")
    print("=" * 70)
    
    if result.get("success"):
        print("✅ 订单下单成功！")
        print("\n这意味着：")
        print("  1. ✅ 账户有足够的余额")
        print("  2. ✅ API 连接正常")
        print("  3. ✅ 配置正确")
        
        order_data = result.get("order_result", {})
        print(f"\n订单详情:")
        print(f"  状态: {order_data.get('status', 'Unknown')}")
        
        if 'response' in order_data and 'data' in order_data['response']:
            response_data = order_data['response']['data']
            if 'statuses' in response_data:
                for status in response_data['statuses']:
                    print(f"  订单状态: {status}")
        
        # 现在取消这个订单
        print(f"\n现在取消这个测试订单...")
        cancel_result = await main.hyperliquid_service.cancel_all_orders("BTC")
        
        if cancel_result.get("success"):
            print("✅ 测试订单已取消")
        else:
            print(f"⚠️ 取消订单失败: {cancel_result.get('error')}")
            print("   请手动在 UI 中取消订单")
    else:
        error = result.get("error", "Unknown error")
        print(f"❌ 订单失败: {error}")
        
        if "insufficient" in error.lower() or "balance" in error.lower():
            print("\n这确认了账户余额不足。")
            print("UI 显示的 999.00 可能是：")
            print("  - 旧的缓存数据")
            print("  - 不同账户的余额")
            print("  - 不同网络的余额")
        else:
            print("\n失败原因可能是其他问题，不一定是余额不足")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(test_small_order())
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
