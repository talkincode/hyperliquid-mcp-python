"""输入验证工具"""
from typing import Optional

class ValidationError(ValueError):
    """验证错误"""
    pass

def validate_coin(coin: str) -> None:
    """验证币种参数"""
    if not coin or not isinstance(coin, str):
        raise ValidationError("coin must be non-empty string")
    if not coin.replace("-", "").replace("_", "").isalnum():
        raise ValidationError(f"invalid coin format: {coin}")

def validate_side(side: str, is_buy: Optional[bool] = None) -> bool:
    """验证订单方向
    
    Returns:
        bool: True for buy, False for sell
    """
    if is_buy is not None:
        return is_buy
    
    side_lower = side.lower().strip()
    if side_lower not in ("buy", "sell"):
        raise ValidationError(
            f"side must be 'buy' or 'sell', got: '{side}'"
        )
    return side_lower == "buy"

def validate_size(size: float, min_size: float = 0.0) -> None:
    """验证订单大小（代币数量，非美元金额）"""
    if not isinstance(size, (int, float)):
        raise ValidationError(
            f"size must be numeric, got: {type(size).__name__}"
        )
    if size <= min_size:
        raise ValidationError(
            f"size must be > {min_size} (token amount, not dollar value), got: {size}"
        )

def validate_price(price: float) -> None:
    """验证价格"""
    if not isinstance(price, (int, float)):
        raise ValidationError(
            f"price must be numeric, got: {type(price).__name__}"
        )
    if price <= 0:
        raise ValidationError(f"price must be > 0, got: {price}")

def validate_order_inputs(
    coin: str,
    side: str,
    size: float,
    price: Optional[float] = None
) -> dict:
    """综合验证订单输入
    
    Returns:
        dict: {"coin": str, "is_buy": bool, "size": float, "price": float (optional)}
    """
    validate_coin(coin)
    is_buy = validate_side(side)
    validate_size(size)
    
    result = {
        "coin": coin,
        "is_buy": is_buy,
        "size": float(size)
    }
    
    if price is not None:
        validate_price(price)
        result["price"] = float(price)
    
    return result
