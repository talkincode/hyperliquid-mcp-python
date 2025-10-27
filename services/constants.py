"""HyperLiquid MCP 常量定义"""

# OCO 订单分组类型
OCO_GROUP_NEW_POSITION = "normalTpSl"        # 新仓位的括号订单
OCO_GROUP_EXISTING_POSITION = "positionTpSl" # 现有仓位的止盈止损

# 订单类型常量
ORDER_TYPE_LIMIT_GTC = {"limit": {"tif": "Gtc"}}
ORDER_TYPE_LIMIT_IOC = {"limit": {"tif": "Ioc"}}

# 滑点配置
DEFAULT_SLIPPAGE = 0.001      # 0.1%
AGGRESSIVE_SLIPPAGE = 0.5     # 50%

# 地址掩码配置
ADDRESS_PREFIX_LEN = 6
ADDRESS_SUFFIX_LEN = 4
