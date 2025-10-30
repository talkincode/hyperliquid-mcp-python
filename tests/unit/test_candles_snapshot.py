"""批量 K 线快照服务测试"""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from services.hyperliquid_services import HyperliquidServices


@pytest.fixture
def service_with_mocks(monkeypatch):
    """创建带有 Info/Exchange mock 的服务实例"""
    with (
        patch("services.hyperliquid_services.Info") as mock_info_class,
        patch("services.hyperliquid_services.Exchange") as mock_exchange_class,
        patch("eth_account.Account") as mock_account_class,
    ):
        mock_wallet = MagicMock()
        mock_wallet.address = "0xFAKE_WALLET"
        mock_account_class.from_key.return_value = mock_wallet

        info_instance = MagicMock()
        mock_info_class.return_value = info_instance
        mock_exchange_class.return_value = MagicMock()

        service = HyperliquidServices(
            private_key="0x" + "1" * 64,
            testnet=True,
            account_address="0xACCOUNT",
        )

    # 使用实际构造出的 info instance 以便校验调用
    service.info = info_instance
    yield service, info_instance


def test_get_candles_snapshot_bulk_days_success(service_with_mocks, monkeypatch):
    """验证 days 参数路径可正确获取并整理数据"""
    service, info_instance = service_with_mocks

    fixed_time = 1_700_000_000.0
    monkeypatch.setattr("services.hyperliquid_services.time.time", lambda: fixed_time)

    info_instance.candles_snapshot.return_value = [
        {
            "t": 1_699_913_600_000,
            "o": "1",
            "h": "2",
            "l": "0.5",
            "c": "1.5",
            "v": "10",
            "n": 5,
        },
        {
            "t": 1_699_917_600_000,
            "o": "1.5",
            "h": "2.5",
            "l": "1",
            "c": "2",
            "v": "12",
            "n": 6,
        },
    ]

    result = asyncio.run(
        service.get_candles_snapshot_bulk(["BTC", "BTC"], "1h", days=1)
    )

    assert result["success"] is True
    assert list(result["data"].keys()) == ["BTC"]
    assert len(result["data"]["BTC"]) == 2

    expected_end = int(fixed_time * 1000)
    expected_start = expected_end - 86_400_000

    info_instance.candles_snapshot.assert_called_once_with(
        "BTC", "1h", expected_start, expected_end
    )


def test_get_candles_snapshot_bulk_coin_error(service_with_mocks):
    """当部分币种失败时依然返回成功并附带错误信息"""
    service, info_instance = service_with_mocks

    def side_effect(coin, interval, start, end):
        if coin == "BTC":
            return [{"t": 1, "o": "1", "h": "2", "l": "0.5", "c": "1.5", "v": "10"}]
        raise RuntimeError("coin not supported")

    info_instance.candles_snapshot.side_effect = side_effect

    result = asyncio.run(
        service.get_candles_snapshot_bulk(
            ["BTC", "ETH"],
            "1h",
            start_time=1,
            end_time=2,
        )
    )

    assert result["success"] is True
    assert "BTC" in result["data"]
    assert "coin_errors" in result
    assert result["coin_errors"].get("ETH") == "coin not supported"


def test_get_candles_snapshot_bulk_invalid_params(service_with_mocks):
    """非法参数组合应返回失败"""
    service, _ = service_with_mocks

    result = asyncio.run(
        service.get_candles_snapshot_bulk(
            ["BTC"],
            "1h",
            start_time=1,
            end_time=2,
            days=1,
        )
    )

    assert result["success"] is False
    assert "days cannot be used" in result["error"]
