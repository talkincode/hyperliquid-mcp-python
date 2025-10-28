#!/usr/bin/env python3
"""测试 OCO 分组常量修复"""

from services.constants import OCO_GROUP_EXISTING_POSITION, OCO_GROUP_NEW_POSITION

print("=" * 60)
print("OCO 分组常量验证")
print("=" * 60)

print(f"\nOCO_GROUP_NEW_POSITION = {repr(OCO_GROUP_NEW_POSITION)}")
print(f"OCO_GROUP_EXISTING_POSITION = {repr(OCO_GROUP_EXISTING_POSITION)}")

# 验证与 SDK 定义一致
assert OCO_GROUP_NEW_POSITION == "normalTpsl", f"错误: {OCO_GROUP_NEW_POSITION}"
assert OCO_GROUP_EXISTING_POSITION == "positionTpsl", (
    f"错误: {OCO_GROUP_EXISTING_POSITION}"
)

print("\n✅ 所有常量值正确!")
print("✅ 与 HyperLiquid SDK Grouping 类型定义一致 (小写 's')")
print("\n修复说明:")
print("- 之前: normalTpSl, positionTpSl (大写 S - 错误)")
print("- 现在: normalTpsl, positionTpsl (小写 s - 正确)")
print("\n这个修复解决了 '422 Failed to deserialize the JSON body' 错误")
