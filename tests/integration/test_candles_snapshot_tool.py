"""批量 K 线工具集成测试"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import main


def test_get_candles_snapshot_tool_limit(monkeypatch):
    """验证工具能调用服务并应用 limit"""
    mock_service = MagicMock()
    mock_service.get_candles_snapshot_bulk = AsyncMock(
        return_value={
            "success": True,
            "data": {
                "BTC": [
                    {
                        "timestamp": 1,
                        "open": 1,
                        "high": 2,
                        "low": 0.5,
                        "close": 1.5,
                        "volume": 10,
                        "trade_count": 5,
                    },
                    {
                        "timestamp": 2,
                        "open": 1.5,
                        "high": 2.5,
                        "low": 1,
                        "close": 2,
                        "volume": 12,
                        "trade_count": 6,
                    },
                ],
                "ETH": [
                    {
                        "timestamp": 3,
                        "open": 3,
                        "high": 4,
                        "low": 2.5,
                        "close": 3.5,
                        "volume": 15,
                        "trade_count": 7,
                    },
                ],
            },
            "interval": "1h",
            "start_time": 1,
            "end_time": 2,
        }
    )

    monkeypatch.setattr(main, "initialize_service", lambda: None)
    monkeypatch.setattr(main, "hyperliquid_service", mock_service)

    response = asyncio.run(
        main.get_candles_snapshot(
            coins=["BTC", "ETH"],
            interval="1h",
            days=1,
            limit=1,
        )
    )

    assert response["success"] is True
    assert response["limit_per_coin"] == 1
    assert len(response["data"]["BTC"]) == 1
    assert response["data"]["BTC"][0]["timestamp"] == 2

    mock_service.get_candles_snapshot_bulk.assert_awaited_once()


def test_get_candles_snapshot_tool_validation_error(monkeypatch):
    """非法输入参数返回结构化错误"""
    monkeypatch.setattr(main, "initialize_service", lambda: None)
    monkeypatch.setattr(main, "hyperliquid_service", MagicMock())

    response = asyncio.run(
        main.get_candles_snapshot(
            coins=["BTC"],
            interval="1h",
            start_time=None,
            end_time=None,
            days=None,
        )
    )

    assert response["success"] is False
    assert response.get("error_code") == "VALIDATION_ERROR"
