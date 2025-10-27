#!/usr/bin/env python3
"""
测试 HyperLiquid 配置和连接
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import logging

import main

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_configuration():
    """测试配置和连接"""
    print("=" * 60)
    print("HyperLiquid MCP 配置测试")
    print("=" * 60)

    # 1. 检查配置
    try:
        config = main.get_config()
        print("\n✅ 配置加载成功")
        print(f"   网络: {'测试网 (Testnet)' if config.testnet else '主网 (Mainnet)'}")
        print(f"   账户地址: {config.account_address}")
        print(f"   私钥已配置: {'是' if config.private_key else '否'}")
    except Exception as e:
        print(f"\n❌ 配置加载失败: {e}")
        return False

    # 2. 初始化服务
    try:
        main.initialize_service()
        print("\n✅ 服务初始化成功")
        print(f"   服务对象: {main.hyperliquid_service}")
    except Exception as e:
        print(f"\n❌ 服务初始化失败: {e}")
        return False

    # 3. 测试获取账户余额
    print("\n" + "-" * 60)
    print("测试 1: 获取账户余额")
    print("-" * 60)
    try:
        balance = await main.hyperliquid_service.get_account_balance()
        if balance.get("success"):
            data = balance.get("data", {})
            print(f"✅ 账户余额:")
            print(f"   总权益: ${data.get('account_value', 'N/A')}")
            print(f"   可用余额: ${data.get('withdrawable', 'N/A')}")
            print(f"   保证金使用: ${data.get('margin_used', 'N/A')}")
        else:
            print(f"❌ 获取余额失败: {balance.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 获取余额异常: {e}")
        return False

    # 4. 测试获取持仓
    print("\n" + "-" * 60)
    print("测试 2: 获取持仓信息")
    print("-" * 60)
    try:
        positions = await main.hyperliquid_service.get_open_positions()
        if positions.get("success"):
            pos_list = positions.get("positions", [])
            total = positions.get("total_positions", 0)
            print(f"✅ 持仓数量: {total}")
            if pos_list:
                for pos in pos_list:
                    print(
                        f"   - {pos.get('coin')}: 数量={pos.get('position_value')}, PnL={pos.get('unrealized_pnl')}"
                    )
            else:
                print("   (当前无持仓)")
        else:
            print(f"❌ 获取持仓失败: {positions.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 获取持仓异常: {e}")
        return False

    # 5. 测试获取未平仓订单
    print("\n" + "-" * 60)
    print("测试 3: 获取未平仓订单")
    print("-" * 60)
    try:
        orders = await main.hyperliquid_service.get_open_orders()
        if orders.get("success"):
            order_list = orders.get("orders", [])
            total = orders.get("total_orders", 0)
            print(f"✅ 订单数量: {total}")
            if order_list:
                for order in order_list:
                    print(
                        f"   - {order.get('coin')}: {order.get('side')} {order.get('sz')} @ {order.get('limitPx')}"
                    )
            else:
                print("   (当前无未平仓订单)")
        else:
            print(f"❌ 获取订单失败: {orders.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 获取订单异常: {e}")
        return False

    # 6. 测试获取市场数据
    print("\n" + "-" * 60)
    print("测试 4: 获取 BTC 市场数据")
    print("-" * 60)
    try:
        market_data = await main.hyperliquid_service.get_market_data("BTC")
        if market_data.get("success"):
            data = market_data.get("market_data", {})
            print(f"✅ BTC 市场数据:")
            print(f"   当前价格: ${data.get('mid_price', 'N/A')}")
            print(f"   24h成交量: ${data.get('day_ntl_vlm', 'N/A')}")
            print(f"   资金费率: {data.get('funding', 'N/A')}")
        else:
            print(f"❌ 获取市场数据失败: {market_data.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 获取市场数据异常: {e}")
        return False

    # 7. 测试完整账户摘要
    print("\n" + "-" * 60)
    print("测试 5: 获取完整账户摘要")
    print("-" * 60)
    try:
        # 直接调用服务方法
        balance = await main.hyperliquid_service.get_account_balance()
        positions = await main.hyperliquid_service.get_open_positions()
        orders = await main.hyperliquid_service.get_open_orders()

        summary = {
            "success": True,
            "summary": {
                "balance": balance.get("data") if balance.get("success") else None,
                "positions": (
                    positions.get("positions", []) if positions.get("success") else []
                ),
                "orders": orders.get("orders", []) if orders.get("success") else [],
                "total_positions": (
                    positions.get("total_positions", 0)
                    if positions.get("success")
                    else 0
                ),
                "total_orders": (
                    orders.get("total_orders", 0) if orders.get("success") else 0
                ),
            },
        }

        if summary.get("success"):
            print(f"✅ 账户摘要:")
            print(
                f"   账户价值: ${summary['summary']['balance'].get('account_value', 'N/A')}"
            )
            print(f"   持仓数: {summary['summary']['total_positions']}")
            print(f"   订单数: {summary['summary']['total_orders']}")
        else:
            print(f"❌ 获取账户摘要失败")
            return False
    except Exception as e:
        print(f"❌ 获取账户摘要异常: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ 所有测试通过！配置正确，连接正常")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = asyncio.run(test_configuration())
    sys.exit(0 if success else 1)
