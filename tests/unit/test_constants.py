"""常量测试"""

from services.constants import (
    ADDRESS_PREFIX_LEN,
    ADDRESS_SUFFIX_LEN,
    AGGRESSIVE_SLIPPAGE,
    DEFAULT_SLIPPAGE,
    OCO_GROUP_EXISTING_POSITION,
    OCO_GROUP_NEW_POSITION,
    ORDER_TYPE_LIMIT_GTC,
    ORDER_TYPE_LIMIT_IOC,
)


def test_oco_grouping_constants():
    """测试 OCO 分组常量与 SDK 定义一致"""
    # 必须与 HyperLiquid SDK 中的 Grouping 类型定义完全一致
    assert OCO_GROUP_NEW_POSITION == "normalTpsl"  # 注意小写 's'
    assert OCO_GROUP_EXISTING_POSITION == "positionTpsl"  # 注意小写 's'


def test_order_type_constants():
    """测试订单类型常量"""
    assert ORDER_TYPE_LIMIT_GTC == {"limit": {"tif": "Gtc"}}
    assert ORDER_TYPE_LIMIT_IOC == {"limit": {"tif": "Ioc"}}


def test_slippage_constants():
    """测试滑点常量"""
    assert DEFAULT_SLIPPAGE == 0.001
    assert AGGRESSIVE_SLIPPAGE == 0.5


def test_address_mask_constants():
    """测试地址掩码常量"""
    assert ADDRESS_PREFIX_LEN == 6
    assert ADDRESS_SUFFIX_LEN == 4
