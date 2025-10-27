#!/usr/bin/env python3
"""
HyperLiquid 测试工具 - 交互式测试各种功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import main


async def test_menu():
    """显示测试菜单"""
    print("\n" + "=" * 60)
    print("HyperLiquid MCP 测试工具")
    print("=" * 60)
    print("1. 查看账户余额")
    print("2. 查看持仓")
    print("3. 查看未平仓订单")
    print("4. 查看市场数据 (BTC)")
    print("5. 查看市场数据 (ETH)")
    print("6. 查看市场数据 (SOL)")
    print("7. 查看账户摘要")
    print("8. 计算美元转代币数量 (示例: $20 买 SOL)")
    print("9. 获取订单簿 (BTC)")
    print("0. 退出")
    print("=" * 60)


async def main_loop():
    """主循环"""
    # 初始化服务
    print("正在初始化 HyperLiquid 服务...")
    main.initialize_service()
    config = main.get_config()
    network = "测试网 (Testnet)" if config.testnet else "主网 (Mainnet)"
    print(f"✅ 已连接到 {network}")
    print(f"   账户地址: {config.account_address}")
    
    while True:
        await test_menu()
        choice = input("\n请选择操作 (0-9): ").strip()
        
        if choice == "0":
            print("\n再见！")
            break
        
        elif choice == "1":
            print("\n正在获取账户余额...")
            result = await main.hyperliquid_service.get_account_balance()
            if result.get("success"):
                data = result.get("data", {})
                print(f"\n✅ 账户余额:")
                print(f"   总权益: ${data.get('account_value', 'N/A')}")
                print(f"   可用余额: ${data.get('withdrawable', 'N/A')}")
                print(f"   保证金使用: ${data.get('margin_used', 'N/A')}")
            else:
                print(f"\n❌ 失败: {result.get('error')}")
        
        elif choice == "2":
            print("\n正在获取持仓...")
            result = await main.hyperliquid_service.get_open_positions()
            if result.get("success"):
                positions = result.get("positions", [])
                total = result.get("total_positions", 0)
                print(f"\n✅ 持仓数量: {total}")
                if positions:
                    for pos in positions:
                        print(f"\n   币种: {pos.get('coin')}")
                        print(f"   方向: {pos.get('side')}")
                        print(f"   数量: {pos.get('size')}")
                        print(f"   入场价: {pos.get('entry_price')}")
                        print(f"   仓位价值: {pos.get('position_value')}")
                        print(f"   未实现盈亏: {pos.get('unrealized_pnl')}")
                else:
                    print("   (当前无持仓)")
            else:
                print(f"\n❌ 失败: {result.get('error')}")
        
        elif choice == "3":
            print("\n正在获取未平仓订单...")
            result = await main.hyperliquid_service.get_open_orders()
            if result.get("success"):
                orders = result.get("orders", [])
                total = result.get("total_orders", 0)
                print(f"\n✅ 订单数量: {total}")
                if orders:
                    for order in orders:
                        print(f"\n   币种: {order.get('coin')}")
                        print(f"   方向: {order.get('side')}")
                        print(f"   数量: {order.get('sz')}")
                        print(f"   价格: {order.get('limitPx')}")
                        print(f"   订单ID: {order.get('oid')}")
                else:
                    print("   (当前无未平仓订单)")
            else:
                print(f"\n❌ 失败: {result.get('error')}")
        
        elif choice in ["4", "5", "6"]:
            coins = {"4": "BTC", "5": "ETH", "6": "SOL"}
            coin = coins[choice]
            print(f"\n正在获取 {coin} 市场数据...")
            result = await main.hyperliquid_service.get_market_data(coin)
            if result.get("success"):
                data = result.get("market_data", {})
                print(f"\n✅ {coin} 市场数据:")
                print(f"   当前价格: ${data.get('mid_price', 'N/A')}")
                print(f"   24h成交量: ${data.get('day_ntl_vlm', 'N/A')}")
                print(f"   资金费率: {data.get('funding', 'N/A')}")
                print(f"   未平仓合约: {data.get('open_interest', 'N/A')}")
            else:
                print(f"\n❌ 失败: {result.get('error')}")
        
        elif choice == "7":
            print("\n正在获取账户摘要...")
            balance = await main.hyperliquid_service.get_account_balance()
            positions = await main.hyperliquid_service.get_open_positions()
            orders = await main.hyperliquid_service.get_open_orders()
            
            print(f"\n✅ 账户摘要:")
            if balance.get("success"):
                data = balance.get("data", {})
                print(f"\n   余额:")
                print(f"     总权益: ${data.get('account_value', 'N/A')}")
                print(f"     可用: ${data.get('withdrawable', 'N/A')}")
            
            if positions.get("success"):
                total_pos = positions.get("total_positions", 0)
                print(f"\n   持仓: {total_pos} 个")
            
            if orders.get("success"):
                total_orders = orders.get("total_orders", 0)
                print(f"   订单: {total_orders} 个")
        
        elif choice == "8":
            coin = input("   输入币种 (如 SOL, BTC, ETH): ").strip().upper()
            dollar_str = input("   输入美元金额 (如 20): $").strip()
            try:
                dollar_amount = float(dollar_str)
                print(f"\n正在计算 ${dollar_amount} 可以买多少 {coin}...")
                
                # 获取市场价格
                market_data = await main.hyperliquid_service.get_market_data(coin)
                if market_data.get("success"):
                    price = market_data["market_data"]["mid_price"]
                    if price != "N/A":
                        price = float(price)
                        token_amount = dollar_amount / price
                        print(f"\n✅ 计算结果:")
                        print(f"   当前价格: ${price}")
                        print(f"   美元金额: ${dollar_amount}")
                        print(f"   代币数量: {token_amount:.8f} {coin}")
                        print(f"   公式: ${dollar_amount} ÷ ${price} = {token_amount:.8f}")
                    else:
                        print(f"\n❌ 无法获取 {coin} 的价格")
                else:
                    print(f"\n❌ 失败: {market_data.get('error')}")
            except ValueError:
                print("\n❌ 无效的金额格式")
        
        elif choice == "9":
            print("\n正在获取 BTC 订单簿...")
            result = await main.hyperliquid_service.get_orderbook("BTC", depth=10)
            if result.get("success"):
                data = result.get("orderbook", {})
                print(f"\n✅ BTC 订单簿 (前10档):")
                
                bids = data.get("bids", [])
                asks = data.get("asks", [])
                
                print("\n   卖盘 (Asks):")
                for ask in reversed(asks[-5:]):  # 显示最低5个卖单
                    print(f"     价格: ${ask.get('px')}, 数量: {ask.get('sz')}")
                
                print("\n   ----------------------")
                
                print("\n   买盘 (Bids):")
                for bid in bids[:5]:  # 显示最高5个买单
                    print(f"     价格: ${bid.get('px')}, 数量: {bid.get('sz')}")
            else:
                print(f"\n❌ 失败: {result.get('error')}")
        
        else:
            print("\n❌ 无效的选择，请输入 0-9")
        
        input("\n按 Enter 继续...")


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n\n程序已中断，再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
