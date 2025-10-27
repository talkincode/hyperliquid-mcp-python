"""验证器测试"""

import pytest

from services.validators import (ValidationError, validate_coin,
                                 validate_order_inputs, validate_price,
                                 validate_side, validate_size)


def test_validate_size_zero():
    """测试 size=0 抛出错误"""
    with pytest.raises(ValidationError, match="must be >"):
        validate_size(0)


def test_validate_size_negative():
    """测试负数 size 抛出错误"""
    with pytest.raises(ValidationError, match="must be >"):
        validate_size(-1)


def test_validate_size_valid():
    """测试有效的 size"""
    validate_size(0.1)  # 应该不抛出错误
    validate_size(100)  # 应该不抛出错误


def test_validate_side_invalid():
    """测试非法 side 抛出错误"""
    with pytest.raises(ValidationError, match="must be 'buy' or 'sell'"):
        validate_side("long")

    with pytest.raises(ValidationError, match="must be 'buy' or 'sell'"):
        validate_side("short")


def test_validate_side_valid():
    """测试有效的 side"""
    assert validate_side("buy") == True
    assert validate_side("BUY") == True
    assert validate_side("sell") == False
    assert validate_side("SELL") == False


def test_validate_coin_empty():
    """测试空币种抛出错误"""
    with pytest.raises(ValidationError, match="non-empty"):
        validate_coin("")


def test_validate_coin_none():
    """测试 None 币种抛出错误"""
    with pytest.raises(ValidationError, match="non-empty"):
        validate_coin(None)


def test_validate_coin_valid():
    """测试有效的币种"""
    validate_coin("BTC")
    validate_coin("ETH")
    validate_coin("SOL")
    validate_coin("BTC-USD")


def test_validate_price_zero():
    """测试 price=0 抛出错误"""
    with pytest.raises(ValidationError, match="must be > 0"):
        validate_price(0)


def test_validate_price_negative():
    """测试负价格抛出错误"""
    with pytest.raises(ValidationError, match="must be > 0"):
        validate_price(-100)


def test_validate_price_valid():
    """测试有效价格"""
    validate_price(100.5)
    validate_price(0.001)


def test_validate_order_inputs_valid():
    """测试综合验证 - 有效输入"""
    result = validate_order_inputs("BTC", "buy", 0.1, 45000)
    assert result["coin"] == "BTC"
    assert result["is_buy"] == True
    assert result["size"] == 0.1
    assert result["price"] == 45000


def test_validate_order_inputs_no_price():
    """测试综合验证 - 无价格"""
    result = validate_order_inputs("ETH", "sell", 1.5)
    assert result["coin"] == "ETH"
    assert result["is_buy"] == False
    assert result["size"] == 1.5
    assert "price" not in result


def test_validate_order_inputs_invalid_coin():
    """测试综合验证 - 无效币种"""
    with pytest.raises(ValidationError, match="non-empty"):
        validate_order_inputs("", "buy", 1.0, 100)


def test_validate_order_inputs_invalid_side():
    """测试综合验证 - 无效方向"""
    with pytest.raises(ValidationError, match="must be 'buy' or 'sell'"):
        validate_order_inputs("BTC", "long", 1.0, 100)


def test_validate_order_inputs_invalid_size():
    """测试综合验证 - 无效大小"""
    with pytest.raises(ValidationError, match="must be >"):
        validate_order_inputs("BTC", "buy", 0, 100)


def test_validate_order_inputs_invalid_price():
    """测试综合验证 - 无效价格"""
    with pytest.raises(ValidationError, match="must be > 0"):
        validate_order_inputs("BTC", "buy", 1.0, -100)
