#!/usr/bin/env python3
"""
测试价格计算器 - 美元转代币数量
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


async def test_price_calculator():
    """测试价格计算器"""
    print("=" * 70)
    print("💵 价格计算器测试")
    print("=" * 70)
    
    # 初始化服务
    main.initialize_service()
    
    # 测试不同金额和币种的转换
    test_cases = [
        {"coin": "BTC", "dollars": [10, 50, 100, 500, 1000]},
        {"coin": "ETH", "dollars": [10, 50, 100, 500]},
        {"coin": "SOL", "dollars": [10, 20, 50, 100]},
    ]
    
    for test_case in test_cases:
        coin = test_case["coin"]
        dollar_amounts = test_case["dollars"]
        
        print(f"\n{'=' * 70}")
        print(f"💰 {coin} 价格计算")
        print(f"{'=' * 70}")
        
        # 先获取当前价格（只调用一次）
        market_data = await main.hyperliquid_service.get_market_data(coin)
        
        if not market_data.get("success"):
            print(f"❌ 获取市场数据失败: {market_data.get('error')}\n")
            continue
        
        current_price = market_data["market_data"]["mid_price"]
        
        if current_price == "N/A":
            print(f"❌ 无法获取 {coin} 当前价格\n")
            continue
        
        price = float(current_price)
        print(f"\n当前价格: ${price:,.2f}\n")
        
        print(f"{'美元金额':<15} {'代币数量':<25} {'精确价值':<15}")
        print("-" * 70)
        
        # 使用同一个价格计算所有金额，避免重复调用 API
        for dollar_amount in dollar_amounts:
            token_amount = dollar_amount / price
            exact_value = token_amount * price
            
            print(f"${dollar_amount:<14.2f} {token_amount:<24.8f} ${exact_value:<14.2f}")
        
        print()
    
    print("=" * 70)
    print("✅ 价格计算器测试完成")
    print("=" * 70)
    print("\n💡 提示: 使用 calculate_token_amount_from_dollars() 工具进行实时转换")


if __name__ == "__main__":
    asyncio.run(test_price_calculator())
