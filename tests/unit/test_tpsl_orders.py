"""止盈止损订单结构测试

测试止盈止损订单的正确构建，确保：
1. 止盈订单使用限价单 (isMarket: False)
2. 止损订单使用市价单 (isMarket: True)
3. limit_px 设置正确
4. OCO 分组正确
"""

from unittest.mock import MagicMock, patch

import pytest

from services.constants import OCO_GROUP_EXISTING_POSITION
from services.hyperliquid_services import HyperliquidServices


@pytest.fixture
def mock_service():
    """创建 mock 服务实例"""
    with (
        patch("services.hyperliquid_services.Info"),
        patch("services.hyperliquid_services.Exchange"),
        patch("eth_account.Account") as mock_account_class,
    ):
        # Mock wallet
        mock_wallet = MagicMock()
        mock_wallet.address = "0xTEST_WALLET_ADDRESS"
        mock_account_class.from_key.return_value = mock_wallet

        service = HyperliquidServices(
            private_key="0x" + "1" * 64, testnet=True, account_address="0xTEST"
        )
        return service


@pytest.mark.asyncio
async def test_take_profit_order_structure(mock_service, monkeypatch):
    """测试止盈订单结构: 应该使用限价单"""
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回多头仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "0.1"}}  # 多头仓位
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 只设置止盈
    await mock_service.set_position_tpsl(coin="BTC", tp_px=50000, sl_px=None)

    assert captured_orders is not None
    assert len(captured_orders) == 1

    tp_order = captured_orders[0]

    # 验证止盈订单结构
    assert tp_order["coin"] == "BTC"
    assert tp_order["is_buy"] is False  # 平多头，应该是卖单
    assert tp_order["sz"] == 0.1
    assert tp_order["limit_px"] == 50000.0  # 限价应该等于触发价
    assert tp_order["reduce_only"] is True
    assert tp_order["order_type"]["trigger"]["triggerPx"] == 50000.0
    assert tp_order["order_type"]["trigger"]["isMarket"] is False  # 止盈使用限价单
    assert tp_order["order_type"]["trigger"]["tpsl"] == "tp"


@pytest.mark.asyncio
async def test_stop_loss_order_structure(mock_service, monkeypatch):
    """测试止损订单结构: 应该使用市价单"""
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回多头仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "0.1"}}  # 多头仓位
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 只设置止损
    await mock_service.set_position_tpsl(coin="BTC", tp_px=None, sl_px=40000)

    assert captured_orders is not None
    assert len(captured_orders) == 1

    sl_order = captured_orders[0]

    # 验证止损订单结构
    assert sl_order["coin"] == "BTC"
    assert sl_order["is_buy"] is False  # 平多头，应该是卖单
    assert sl_order["sz"] == 0.1
    assert sl_order["limit_px"] == 40000.0  # 止损也用触发价作为限价
    assert sl_order["reduce_only"] is True
    assert sl_order["order_type"]["trigger"]["triggerPx"] == 40000.0
    assert sl_order["order_type"]["trigger"]["isMarket"] is True  # 止损使用市价单
    assert sl_order["order_type"]["trigger"]["tpsl"] == "sl"


@pytest.mark.asyncio
async def test_combined_tpsl_order_structure(mock_service, monkeypatch):
    """测试同时设置止盈止损: 应该创建两个订单"""
    captured_orders = None
    captured_grouping = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders, captured_grouping
        captured_orders = order_requests
        captured_grouping = grouping
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回多头仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "0.1"}}  # 多头仓位
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 同时设置止盈止损
    result = await mock_service.set_position_tpsl(
        coin="BTC", tp_px=50000, sl_px=40000, position_size=0.1
    )

    # 验证返回结果
    assert result["success"] is True
    assert result["position_details"]["take_profit_price"] == 50000
    assert result["position_details"]["stop_loss_price"] == 40000

    # 验证订单数量
    assert captured_orders is not None
    assert len(captured_orders) == 2

    # 验证 OCO 分组
    assert captured_grouping == OCO_GROUP_EXISTING_POSITION

    # 找到止盈和止损订单
    tp_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "tp"
    )
    sl_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "sl"
    )

    # 验证止盈订单
    assert tp_order["limit_px"] == 50000.0
    assert tp_order["order_type"]["trigger"]["isMarket"] is False

    # 验证止损订单
    assert sl_order["limit_px"] == 40000.0
    assert sl_order["order_type"]["trigger"]["isMarket"] is True


@pytest.mark.asyncio
async def test_short_position_tpsl_direction(mock_service, monkeypatch):
    """测试空头仓位的止盈止损方向: 应该使用买单平仓"""
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回空头仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "ETH", "szi": "-1.5"}}  # 负数表示空头
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 设置止盈止损
    result = await mock_service.set_position_tpsl(coin="ETH", tp_px=2000, sl_px=2200)

    assert result["success"] is True
    assert result["position_details"]["is_long"] is False

    # 验证订单方向
    tp_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "tp"
    )
    sl_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "sl"
    )

    # 空头平仓应该是买单
    assert tp_order["is_buy"] is True
    assert sl_order["is_buy"] is True

    # 仓位大小应该是绝对值
    assert tp_order["sz"] == 1.5
    assert sl_order["sz"] == 1.5


@pytest.mark.asyncio
async def test_tpsl_without_position_fails(mock_service, monkeypatch):
    """测试没有仓位时设置止盈止损应该失败"""

    # Mock info.user_state 返回空仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "0"}}  # 空仓
            ]
        }

    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    result = await mock_service.set_position_tpsl(coin="BTC", tp_px=50000, sl_px=40000)

    assert result["success"] is False
    assert "No position found" in result["error"]


@pytest.mark.asyncio
async def test_tpsl_price_validation(mock_service, monkeypatch):
    """测试止盈止损价格验证"""

    # Mock info.user_state 返回多头仓位
    def mock_user_state(address):
        return {"assetPositions": [{"position": {"coin": "BTC", "szi": "0.1"}}]}

    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 测试至少需要设置一个价格
    result = await mock_service.set_position_tpsl(coin="BTC", tp_px=None, sl_px=None)

    assert result["success"] is False
    assert "At least one of tp_px or sl_px must be specified" in result["error"]


@pytest.mark.asyncio
async def test_auto_detect_position_size(mock_service, monkeypatch):
    """测试自动检测仓位大小"""
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "SOL", "szi": "5.25"}}  # 5.25 SOL 多头
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    # 不提供 position_size，应该自动检测
    result = await mock_service.set_position_tpsl(coin="SOL", tp_px=200, sl_px=180)

    assert result["success"] is True
    assert result["position_details"]["position_size"] == 5.25

    # 验证订单大小
    for order in captured_orders:
        assert order["sz"] == 5.25


@pytest.mark.asyncio
async def test_limit_px_equals_trigger_px(mock_service, monkeypatch):
    """测试 limit_px 应该等于 trigger_px（而不是使用激进价格）"""
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_orders
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    def mock_user_state(address):
        return {"assetPositions": [{"position": {"coin": "BTC", "szi": "0.1"}}]}

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    tp_price = 50000.0
    sl_price = 40000.0

    await mock_service.set_position_tpsl(coin="BTC", tp_px=tp_price, sl_px=sl_price)

    tp_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "tp"
    )
    sl_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "sl"
    )

    # 验证 limit_px 等于用户指定的价格，不是激进价格
    assert tp_order["limit_px"] == tp_price
    assert tp_order["order_type"]["trigger"]["triggerPx"] == tp_price

    assert sl_order["limit_px"] == sl_price
    assert sl_order["order_type"]["trigger"]["triggerPx"] == sl_price
