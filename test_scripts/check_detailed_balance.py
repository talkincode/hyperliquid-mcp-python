#!/usr/bin/env python3
"""
检查详细余额信息
"""
import asyncio
import sys
from pathlib import Path
import json

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import main
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def check_detailed_balance():
    """检查详细余额"""
    print("=" * 60)
    print("HyperLiquid 详细余额检查")
    print("=" * 60)
    
    # 初始化服务
    main.initialize_service()
    
    # 获取原始的用户状态信息
    print("\n获取原始用户状态...")
    try:
        from hyperliquid.info import Info
        config = main.get_config()
        info = Info(skip_ws=True, base_url="https://api.hyperliquid-testnet.xyz" if config.testnet else None)
        
        # 获取用户状态
        user_state = info.user_state(config.account_address)
        
        print("\n完整用户状态:")
        print(json.dumps(user_state, indent=2))
        
        # 检查余额
        if 'marginSummary' in user_state:
            margin = user_state['marginSummary']
            print("\n保证金摘要:")
            print(f"  账户价值: ${margin.get('accountValue', 'N/A')}")
            print(f"  总原始USD: ${margin.get('totalRawUsd', 'N/A')}")
            print(f"  总保证金使用: ${margin.get('totalMarginUsed', 'N/A')}")
            print(f"  可提取: ${margin.get('withdrawable', 'N/A')}")
        
        # 检查资产持仓
        if 'assetPositions' in user_state:
            assets = user_state['assetPositions']
            print(f"\n资产持仓 ({len(assets)} 个):")
            for asset in assets:
                position = asset.get('position', {})
                coin = position.get('coin', 'Unknown')
                entry_px = position.get('entryPx')
                position_value = position.get('positionValue')
                unrealized_pnl = position.get('unrealizedPnl')
                print(f"  {coin}:")
                print(f"    入场价: {entry_px}")
                print(f"    仓位价值: {position_value}")
                print(f"    未实现盈亏: {unrealized_pnl}")
        
        # 检查余额 - 查找代币余额
        if 'withdrawable' in user_state:
            print(f"\n可提取余额: ${user_state['withdrawable']}")
            
        # 获取现货余额
        print("\n获取现货余额...")
        spot_state = info.spot_user_state(config.account_address)
        print("\n现货账户状态:")
        print(json.dumps(spot_state, indent=2))
        
        if 'balances' in spot_state:
            balances = spot_state['balances']
            print(f"\n现货余额 ({len(balances)} 种代币):")
            for balance in balances:
                coin = balance.get('coin', 'Unknown')
                total = balance.get('total', '0')
                hold = balance.get('hold', '0')
                print(f"  {coin}: 总计={total}, 冻结={hold}, 可用={float(total) - float(hold)}")
        
    except Exception as e:
        print(f"\n❌ 获取详细信息失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(check_detailed_balance())
