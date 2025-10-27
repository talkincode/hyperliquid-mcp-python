# HyperLiquid MCP 优化任务计划

## 📋 MVP 优化方案 (1-2天完成)

本计划专注于最高优先级的安全和功能修复，采用最小可行方案快速提升代码质量。

---

## 🎯 阶段 1: 核心安全修复 (4-6小时)

### ✅ 任务 1.1: 修复 account_address 回退逻辑
**优先级**: 🔴 P0 - 严重  
**文件**: `services/hyperliquid_services.py`  
**问题**: 当未提供 `account_address` 时可能传递 `None` 导致运行时错误

**修改内容**:
```python
# 第 48-53 行修改
# 原代码:
self.account_address = account_address
print(self.account_address)

# 修改为:
self.account_address = account_address or self.wallet.address
self.logger.info(
    f"Account initialized: {self.account_address[:6]}...{self.account_address[-4:]}"
)
```

**验证**:
- [ ] 运行服务初始化，不提供 `account_address` 参数
- [ ] 检查日志输出是否包含掩码后的地址
- [ ] 确认 `self.account_address` 不为 `None`

---

### ✅ 任务 1.2: 创建 OCO 分组常量
**优先级**: 🔴 P0 - 严重  
**文件**: `services/constants.py` (新建)

**创建内容**:
```python
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
```

**验证**:
- [ ] 文件创建成功
- [ ] 可以成功导入常量

---

### ✅ 任务 1.3: 修复 place_bracket_order OCO 分组
**优先级**: 🔴 P0 - 严重  
**文件**: `services/hyperliquid_services.py`

**修改位置 1** - 导入常量 (第 1 行后添加):
```python
from .constants import (
    OCO_GROUP_NEW_POSITION,
    OCO_GROUP_EXISTING_POSITION,
    ORDER_TYPE_LIMIT_GTC,
    ADDRESS_PREFIX_LEN,
    ADDRESS_SUFFIX_LEN
)
```

**修改位置 2** - `place_bracket_order` 方法 (约第 334 行):
```python
# 原代码:
bulk_result = self._bulk_orders_with_grouping(order_requests, grouping="normalTpsl")

# 修改为:
bulk_result = self._bulk_orders_with_grouping(
    order_requests, 
    grouping=OCO_GROUP_NEW_POSITION
)
```

**修改位置 3** - 返回值 (约第 345 行):
```python
# 原代码:
"grouping": "normalTpSl"

# 修改为:
"grouping": OCO_GROUP_NEW_POSITION
```

**验证**:
- [ ] 代码编译通过
- [ ] 运行 `place_bracket_order` 测试
- [ ] 检查日志确认分组参数为 `normalTpSl`

---

### ✅ 任务 1.4: 修复 set_position_tpsl 未定义变量问题
**优先级**: 🔴 P0 - 严重  
**文件**: `services/hyperliquid_services.py`

**修改位置** - `set_position_tpsl` 方法 (约第 737-750 行):
```python
# 原代码:
try:
    # First, let's try the standard bulk_orders approach
    bulk_result = self.exchange.bulk_orders(order_requests)
    self.logger.info(f"Standard bulk_orders result: {bulk_result}")
except Exception as e:
    self.logger.error(f"Standard bulk_orders failed with exception: {e}")
    # Fall back to custom method

# 修改为:
try:
    # 直接使用自定义方法确保分组正确
    bulk_result = self._bulk_orders_with_grouping(
        order_requests, 
        grouping=OCO_GROUP_EXISTING_POSITION
    )
    self.logger.info(f"Position TP/SL set successfully: {bulk_result}")
except Exception as e:
    self.logger.error(
        f"Failed to set position TP/SL for {coin}: {e}", 
        exc_info=True
    )
    return {
        "success": False,
        "error": f"Failed to submit OCO TP/SL orders: {str(e)}",
        "coin": coin
    }
```

**修改位置 2** - 返回值中的分组 (约第 758 行):
```python
# 原代码:
"grouping": "positionTpSl"

# 修改为:
"grouping": OCO_GROUP_EXISTING_POSITION
```

**验证**:
- [ ] 代码编译通过
- [ ] 模拟测试设置止盈止损
- [ ] 确认异常情况下不会出现 `UnboundLocalError`

---

## 🎯 阶段 2: 输入验证层 (3-4小时)

### ✅ 任务 2.1: 创建验证器模块
**优先级**: 🔴 P0 - 严重  
**文件**: `services/validators.py` (新建)

**创建内容**:
```python
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
```

**验证**:
- [ ] 文件创建成功
- [ ] 导入测试通过

---

### ✅ 任务 2.2: 集成验证器到工具函数
**优先级**: 🔴 P0 - 严重  
**文件**: `main.py`

**修改位置 1** - 导入 (第 1 行后添加):
```python
from services.validators import validate_order_inputs, ValidationError
```

**修改位置 2** - `place_limit_order` 工具 (约第 97 行):
```python
@mcp.tool
async def place_limit_order(
    coin: str,
    side: str,
    size: float,
    price: float,
    reduce_only: bool = False,
    client_order_id: Optional[str] = None
) -> Dict[str, Any]:
    """..."""
    initialize_service()
    
    try:
        # 验证输入
        validated = validate_order_inputs(coin, side, size, price)
        
        return await hyperliquid_service.place_order(
            coin=validated["coin"],
            is_buy=validated["is_buy"],
            sz=validated["size"],
            limit_px=validated["price"],
            reduce_only=reduce_only,
            cloid=client_order_id
        )
    except ValidationError as e:
        return {
            "success": False,
            "error": f"Invalid input: {str(e)}",
            "error_code": "VALIDATION_ERROR"
        }
```

**类似修改** - 应用到以下工具:
- [ ] `market_open_position` (约第 136 行)
- [ ] `place_bracket_order` (约第 165 行)
- [ ] `set_take_profit_stop_loss` (约第 441 行)

**验证**:
- [ ] 传入非法参数测试 (size=0, side="invalid", coin="")
- [ ] 检查返回错误格式包含 `error_code`

---

## 🎯 阶段 3: 最小测试覆盖 (3-4小时)

### ✅ 任务 3.1: 创建测试目录结构
**优先级**: 🟡 P1 - 重要

**创建目录**:
```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_constants.py
└── integration/
    ├── __init__.py
    ├── test_oco_grouping.py
    └── test_account_address.py
```

**验证**:
- [ ] 目录创建成功
- [ ] `__init__.py` 文件存在

---

### ✅ 任务 3.2: 编写验证器单元测试
**优先级**: 🟡 P1 - 重要  
**文件**: `tests/unit/test_validators.py`

**测试内容** (关键测试):
```python
"""验证器测试"""
import pytest
from services.validators import (
    validate_coin, validate_side, validate_size, 
    validate_price, ValidationError
)

def test_validate_size_zero():
    """测试 size=0 抛出错误"""
    with pytest.raises(ValidationError, match="must be >"):
        validate_size(0)

def test_validate_size_negative():
    """测试负数 size 抛出错误"""
    with pytest.raises(ValidationError, match="must be >"):
        validate_size(-1)

def test_validate_side_invalid():
    """测试非法 side 抛出错误"""
    with pytest.raises(ValidationError, match="must be 'buy' or 'sell'"):
        validate_side("long")

def test_validate_coin_empty():
    """测试空币种抛出错误"""
    with pytest.raises(ValidationError, match="non-empty"):
        validate_coin("")
```

**验证**:
- [ ] `pytest tests/unit/test_validators.py -v` 通过

---

### ✅ 任务 3.3: 编写 OCO 分组集成测试
**优先级**: 🟡 P1 - 重要  
**文件**: `tests/integration/test_oco_grouping.py`

**测试内容**:
```python
"""OCO 分组测试"""
import pytest
from unittest.mock import MagicMock, patch
from services.hyperliquid_services import HyperliquidServices
from services.constants import OCO_GROUP_NEW_POSITION, OCO_GROUP_EXISTING_POSITION

@pytest.fixture
def mock_service():
    """创建 mock 服务实例"""
    with patch('services.hyperliquid_services.Info'), \
         patch('services.hyperliquid_services.Exchange'), \
         patch('services.hyperliquid_services.Account'):
        service = HyperliquidServices(
            private_key="0x" + "1" * 64,
            testnet=True,
            account_address="0xTEST"
        )
        return service

@pytest.mark.asyncio
async def test_bracket_order_uses_correct_grouping(mock_service, monkeypatch):
    """测试 place_bracket_order 使用 normalTpSl 分组"""
    captured_grouping = None
    
    def mock_bulk_orders(order_requests, grouping="na"):
        nonlocal captured_grouping
        captured_grouping = grouping
        return {"status": "ok"}
    
    monkeypatch.setattr(
        mock_service, 
        "_bulk_orders_with_grouping",
        mock_bulk_orders
    )
    
    await mock_service.place_bracket_order(
        coin="BTC",
        is_buy=True,
        sz=0.1,
        limit_px=45000,
        take_profit_px=47000,
        stop_loss_px=43000
    )
    
    assert captured_grouping == OCO_GROUP_NEW_POSITION
```

**验证**:
- [ ] `pytest tests/integration/test_oco_grouping.py -v` 通过

---

### ✅ 任务 3.4: 编写 account_address 回退测试
**优先级**: 🟡 P1 - 重要  
**文件**: `tests/integration/test_account_address.py`

**测试内容**:
```python
"""账户地址回退测试"""
import pytest
from unittest.mock import patch, MagicMock
from services.hyperliquid_services import HyperliquidServices

@pytest.mark.asyncio
async def test_account_address_fallback_to_wallet():
    """测试未提供 account_address 时回退到 wallet.address"""
    with patch('services.hyperliquid_services.Info'), \
         patch('services.hyperliquid_services.Exchange'), \
         patch('services.hyperliquid_services.Account') as mock_account_class:
        
        # Mock wallet
        mock_wallet = MagicMock()
        mock_wallet.address = "0xWALLET_ADDRESS_12345"
        mock_account_class.from_key.return_value = mock_wallet
        
        # 不提供 account_address
        service = HyperliquidServices(
            private_key="0x" + "1" * 64,
            testnet=True,
            account_address=None  # 关键：传入 None
        )
        
        # 应该回退到 wallet.address
        assert service.account_address == "0xWALLET_ADDRESS_12345"
        assert service.account_address is not None
```

**验证**:
- [ ] `pytest tests/integration/test_account_address.py -v` 通过

---

### ✅ 任务 3.5: 配置 pytest
**优先级**: 🟡 P1 - 重要  
**文件**: `tests/conftest.py`

**创建内容**:
```python
"""pytest 配置"""
import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

**文件**: `pyproject.toml` (添加配置)

**添加内容**:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

**验证**:
- [ ] `uv run pytest tests/ -v` 运行所有测试

---

## 📝 完成标准

### 阶段 1 完成标准:
- [x] `account_address` 回退逻辑修复
- [x] 常量文件创建并导入成功
- [x] `place_bracket_order` 使用常量
- [x] `set_position_tpsl` 无未定义变量错误
- [x] 日志输出地址已掩码

### 阶段 2 完成标准:
- [x] 验证器模块创建
- [x] 至少 4 个工具集成验证器
- [x] 非法输入返回 `VALIDATION_ERROR`

### 阶段 3 完成标准:
- [x] 测试目录结构创建
- [x] 验证器单元测试 100% 通过
- [x] OCO 分组测试通过
- [x] account_address 回退测试通过
- [x] `pytest tests/ -v` 全绿

---

## 🚀 执行顺序

1. **先做阶段 1** (最高优先级，解决严重 bug)
2. **再做阶段 2** (防止新 bug 引入)
3. **最后做阶段 3** (锁定改进成果)

每完成一个任务立即验证，确保通过后再进行下一个。

---

## ⏱️ 预估时间

| 阶段 | 预计时间 | 累计时间 |
|------|---------|---------|
| 阶段 1 | 4-6 小时 | 4-6 小时 |
| 阶段 2 | 3-4 小时 | 7-10 小时 |
| 阶段 3 | 3-4 小时 | 10-14 小时 |

**总计**: 10-14 小时 (约 1.5-2 个工作日)

---

## 📞 后续可选增强 (不在 MVP 范围)

- [ ] 异步 SDK 包装 (asyncio.to_thread)
- [ ] 结构化日志 (JSON 格式)
- [ ] 响应格式 Pydantic 模型
- [ ] CI/CD GitHub Actions
- [ ] 测试覆盖率 > 60%

**建议**: 完成 MVP 后评估实际需求再决定是否实施。

---

**状态更新**: 📋 计划已创建，待开始执行
**最后更新**: 2025-01-27
