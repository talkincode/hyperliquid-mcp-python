#!/usr/bin/env python3
"""
检查所有账户余额（现货 + 合约）
"""
import asyncio
import json
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


async def check_all_balances():
    """检查所有账户余额"""
    print("=" * 70)
    print("HyperLiquid 完整余额检查（现货 + 合约）")
    print("=" * 70)

    # 初始化服务
    main.initialize_service()
    config = main.get_config()

    from hyperliquid.info import Info

    # 创建 Info 客户端
    base_url = "https://api.hyperliquid-testnet.xyz" if config.testnet else None
    info = Info(skip_ws=True, base_url=base_url)

    print(f"\n📍 网络: {'测试网 (Testnet)' if config.testnet else '主网 (Mainnet)'}")
    print(f"📍 账户: {config.account_address}")

    # 1. 检查合约账户（Perpetual）
    print("\n" + "=" * 70)
    print("📊 合约账户（Perpetual Account）余额")
    print("=" * 70)

    try:
        user_state = info.user_state(config.account_address)

        if "marginSummary" in user_state:
            margin = user_state["marginSummary"]
            account_value = float(margin.get("accountValue", "0"))
            withdrawable = float(user_state.get("withdrawable", "0"))
            margin_used = float(margin.get("totalMarginUsed", "0"))

            print(f"\n💰 账户价值: ${account_value:,.2f}")
            print(f"💵 可提取: ${withdrawable:,.2f}")
            print(f"📌 保证金使用: ${margin_used:,.2f}")

            if account_value == 0:
                print("\n⚠️  合约账户余额为 $0")
        else:
            print("\n❌ 无法获取合约账户信息")

    except Exception as e:
        print(f"\n❌ 获取合约账户失败: {e}")

    # 2. 检查现货账户（Spot）
    print("\n" + "=" * 70)
    print("📊 现货账户（Spot Account）余额")
    print("=" * 70)

    try:
        spot_state = info.spot_user_state(config.account_address)

        if "balances" in spot_state:
            balances = spot_state["balances"]

            if balances:
                print(f"\n✅ 找到 {len(balances)} 种代币:\n")

                total_value_usd = 0

                for balance in balances:
                    coin = balance.get("coin", "Unknown")
                    total = float(balance.get("total", "0"))
                    hold = float(balance.get("hold", "0"))
                    available = total - hold

                    # 尝试获取 USD 价值（如果是稳定币，直接计算）
                    if coin in ["USDC", "USDT", "USD"]:
                        usd_value = total
                        total_value_usd += usd_value
                        print(f"   💵 {coin}:")
                        print(f"      总计: {total:,.2f} (≈ ${usd_value:,.2f})")
                        print(f"      冻结: {hold:,.2f}")
                        print(f"      可用: {available:,.2f}")
                    else:
                        print(f"   🪙 {coin}:")
                        print(f"      总计: {total:,.8f}")
                        print(f"      冻结: {hold:,.8f}")
                        print(f"      可用: {available:,.8f}")
                    print()

                if total_value_usd > 0:
                    print(f"💰 现货账户总价值（估算）: ${total_value_usd:,.2f}\n")

                print("=" * 70)
                print("🔄 如何将现货余额转入合约账户进行交易？")
                print("=" * 70)
                print("\n使用我们的 MCP 工具:")
                print("   工具名: transfer_between_spot_and_perp")
                print(f"   参数: amount={total_value_usd}, to_perp=True")
                print("\n或运行命令:")
                print(f"   uv run python -c 'import asyncio; import main; ")
                print(f"   main.initialize_service(); ")
                print(
                    f"   asyncio.run(main.hyperliquid_service.transfer_between_spot_and_perp({total_value_usd}, True))'"
                )

            else:
                print("\n⚠️  现货账户余额为空")
        else:
            print("\n❌ 无法获取现货账户信息")

    except Exception as e:
        print(f"\n❌ 获取现货账户失败: {e}")
        import traceback

        traceback.print_exc()

    # 3. 总结
    print("\n" + "=" * 70)
    print("📋 总结")
    print("=" * 70)
    print(
        """
HyperLiquid 有两个独立的账户：
1. 📊 合约账户（Perpetual）- 用于合约交易（我们的 MCP 工具主要操作这个）
2. 🪙 现货账户（Spot）- 用于现货交易

如果你的 999 余额在现货账户，需要先转入合约账户才能进行合约交易。
    """
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(check_all_balances())
