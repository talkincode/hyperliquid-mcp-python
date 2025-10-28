"""OCO 分组测试"""

from unittest.mock import MagicMock, patch

import pytest

from services.constants import OCO_GROUP_EXISTING_POSITION, OCO_GROUP_NEW_POSITION
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
async def test_bracket_order_uses_correct_grouping(mock_service, monkeypatch):
    """测试 place_bracket_order 使用 normalTpSl 分组"""
    captured_grouping = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_grouping
        captured_grouping = grouping
        return {"status": "ok", "response": {"type": "default"}}

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)

    result = await mock_service.place_bracket_order(
        coin="BTC",
        is_buy=True,
        sz=0.1,
        limit_px=45000,
        take_profit_px=47000,
        stop_loss_px=43000,
    )

    assert captured_grouping == OCO_GROUP_NEW_POSITION
    assert result["success"]
    assert result["order_details"]["grouping"] == OCO_GROUP_NEW_POSITION


@pytest.mark.asyncio
async def test_set_position_tpsl_uses_correct_grouping(mock_service, monkeypatch):
    """测试 set_position_tpsl 使用 positionTpSl 分组"""
    captured_grouping = None
    captured_orders = None

    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_grouping, captured_orders
        captured_grouping = grouping
        captured_orders = order_requests
        return {"status": "ok", "response": {"type": "default"}}

    # Mock info.user_state 返回一个仓位
    def mock_user_state(address):
        return {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "0.1"}}  # 正数表示多头
            ]
        }

    monkeypatch.setattr(mock_service, "_bulk_orders_with_grouping", mock_bulk_orders)
    monkeypatch.setattr(mock_service.info, "user_state", mock_user_state)

    result = await mock_service.set_position_tpsl(coin="BTC", tp_px=47000, sl_px=43000)

    assert captured_grouping == OCO_GROUP_EXISTING_POSITION
    assert result["success"]
    assert result["position_details"]["grouping"] == OCO_GROUP_EXISTING_POSITION

    # 验证订单结构正确性
    assert len(captured_orders) == 2
    tp_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "tp"
    )
    sl_order = next(
        o for o in captured_orders if o["order_type"]["trigger"]["tpsl"] == "sl"
    )

    # 验证止盈使用限价单
    assert tp_order["order_type"]["trigger"]["isMarket"] is False
    assert tp_order["limit_px"] == 47000.0

    # 验证止损使用市价单
    assert sl_order["order_type"]["trigger"]["isMarket"] is True
    assert sl_order["limit_px"] == 43000.0
