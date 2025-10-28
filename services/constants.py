"""HyperLiquid MCP 常量定义"""

# OCO 订单分组类型
# 注意: 必须与 HyperLiquid SDK 中的 Grouping 类型定义一致
# SDK 定义: Literal["na"], Literal["normalTpsl"], Literal["positionTpsl"]
OCO_GROUP_NEW_POSITION = "normalTpsl"  # 新仓位的括号订单 (小写 s)
OCO_GROUP_EXISTING_POSITION = "positionTpsl"  # 现有仓位的止盈止损 (小写 s)

# 订单类型常量
ORDER_TYPE_LIMIT_GTC = {"limit": {"tif": "Gtc"}}
ORDER_TYPE_LIMIT_IOC = {"limit": {"tif": "Ioc"}}

# 滑点配置
DEFAULT_SLIPPAGE = 0.001  # 0.1%
AGGRESSIVE_SLIPPAGE = 0.5  # 50%

# 地址掩码配置
ADDRESS_PREFIX_LEN = 6
ADDRESS_SUFFIX_LEN = 4
