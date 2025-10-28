#!/usr/bin/env python3
"""
调试止盈止损订单的 JSON 格式
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hyperliquid.utils.signing import order_type_to_wire

# 模拟一个止盈订单
tp_order = {
    "coin": "BTC",
    "is_buy": False,  # 平多仓
    "sz": 0.001,
    "limit_px": 95000.0,
    "order_type": {
        "trigger": {
            "triggerPx": 95000.0,
            "isMarket": False,
            "tpsl": "tp",
        }
    },
    "reduce_only": True,
}

# 模拟一个止损订单
sl_order = {
    "coin": "BTC",
    "is_buy": False,  # 平多仓
    "sz": 0.001,
    "limit_px": 90000.0,
    "order_type": {
        "trigger": {
            "triggerPx": 90000.0,
            "isMarket": True,
            "tpsl": "sl",
        }
    },
    "reduce_only": True,
}

print("=" * 60)
print("止盈订单 (TP Order):")
print("=" * 60)
print(json.dumps(tp_order, indent=2))

print("\n" + "=" * 60)
print("止损订单 (SL Order):")
print("=" * 60)
print(json.dumps(sl_order, indent=2))

# 测试 order_type 转换
print("\n" + "=" * 60)
print("TP Order Type Wire:")
print("=" * 60)
tp_wire_type = order_type_to_wire(tp_order["order_type"])
print(json.dumps(tp_wire_type, indent=2))

print("\n" + "=" * 60)
print("SL Order Type Wire:")
print("=" * 60)
sl_wire_type = order_type_to_wire(sl_order["order_type"])
print(json.dumps(sl_wire_type, indent=2))

print("\n✅ 订单类型格式验证通过!")
