"""账户地址回退测试"""

from unittest.mock import MagicMock, patch

import pytest

from services.hyperliquid_services import HyperliquidServices


@pytest.mark.asyncio
async def test_account_address_fallback_to_wallet():
    """测试未提供 account_address 时回退到 wallet.address"""
    with (
        patch("services.hyperliquid_services.Info"),
        patch("services.hyperliquid_services.Exchange"),
        patch("eth_account.Account") as mock_account_class,
    ):

        # Mock wallet
        mock_wallet = MagicMock()
        mock_wallet.address = "0xWALLET_ADDRESS_12345"
        mock_account_class.from_key.return_value = mock_wallet

        # 不提供 account_address
        service = HyperliquidServices(
            private_key="0x" + "1" * 64,
            testnet=True,
            account_address=None,  # 关键：传入 None
        )

        # 应该回退到 wallet.address
        assert service.account_address == "0xWALLET_ADDRESS_12345"
        assert service.account_address is not None


@pytest.mark.asyncio
async def test_account_address_uses_provided():
    """测试提供 account_address 时使用提供的地址"""
    with (
        patch("services.hyperliquid_services.Info"),
        patch("services.hyperliquid_services.Exchange"),
        patch("eth_account.Account") as mock_account_class,
    ):

        # Mock wallet
        mock_wallet = MagicMock()
        mock_wallet.address = "0xWALLET_ADDRESS_12345"
        mock_account_class.from_key.return_value = mock_wallet

        # 提供 account_address
        custom_address = "0xCUSTOM_ADDRESS_67890"
        service = HyperliquidServices(
            private_key="0x" + "1" * 64, testnet=True, account_address=custom_address
        )

        # 应该使用提供的地址
        assert service.account_address == custom_address
        assert service.account_address != mock_wallet.address


@pytest.mark.asyncio
async def test_account_address_not_none():
    """测试 account_address 永远不会是 None"""
    with (
        patch("services.hyperliquid_services.Info"),
        patch("services.hyperliquid_services.Exchange"),
        patch("eth_account.Account") as mock_account_class,
    ):

        # Mock wallet
        mock_wallet = MagicMock()
        mock_wallet.address = "0xWALLET_ADDRESS_12345"
        mock_account_class.from_key.return_value = mock_wallet

        # 测试各种情况
        for account_addr in [None, "", "0xTEST"]:
            service = HyperliquidServices(
                private_key="0x" + "1" * 64, testnet=True, account_address=account_addr
            )

            # account_address 应该永远不为 None
            assert service.account_address is not None
            assert len(service.account_address) > 0
