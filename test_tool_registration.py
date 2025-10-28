#!/usr/bin/env python3
"""
测试MCP工具注册情况
"""

import sys

sys.path.insert(0, "/Volumes/ExtDISK/github/hyperliquid-mcp")

from main import mcp

print("\n" + "=" * 60)
print("MCP Tools Registration Test")
print("=" * 60)

# 访问 _tool_manager._tools
if hasattr(mcp, "_tool_manager") and hasattr(mcp._tool_manager, "_tools"):
    tools_dict = mcp._tool_manager._tools
    tool_names = sorted(tools_dict.keys())

    print(f"\n✅ Found {len(tool_names)} registered tools:\n")

    for i, tool_name in enumerate(tool_names, 1):
        marker = "🆕" if tool_name == "get_candles_snapshot" else "  "
        print(f"{marker} {i:2d}. {tool_name}")

    # 检查 get_candles_snapshot
    print("\n" + "=" * 60)
    if "get_candles_snapshot" in tools_dict:
        print("✅✅✅ get_candles_snapshot IS REGISTERED!")
        tool_def = tools_dict["get_candles_snapshot"]
        print(f"   Type: {type(tool_def)}")
        if hasattr(tool_def, "description"):
            print(f"   Description: {tool_def.description[:100]}...")
    else:
        print("❌ get_candles_snapshot NOT FOUND")
else:
    print("❌ Cannot access tool manager")

print("=" * 60 + "\n")
