# HyperLiquid MCP Server - AI 编程指南

## 项目概述

这是一个**模型上下文协议 (MCP) 服务器**，为AI助手提供HyperLiquid交易功能。架构采用**服务层模式**，FastMCP处理MCP协议，专门的服务层负责HyperLiquid API交互。

**核心架构：**
- `main.py`: FastMCP服务器，包含工具定义和配置管理
- `services/hyperliquid_services.py`: 核心交易逻辑和HyperLiquid SDK集成
- **全局单例模式**: 服务实例初始化一次，在所有工具调用中重复使用
- **异步优先**: 所有工具都是异步的，尽管底层SDK是同步的

## 关键实现模式

### 配置管理
应用使用**三模式配置系统**：
1. 环境变量 (`HYPERLIQUID_PRIVATE_KEY`, `HYPERLIQUID_TESTNET`, `HYPERLIQUID_ACCOUNT_ADDRESS`)
2. `.env` 文件（相同变量名）
3. `config.json` 文件，使用snake_case键名 (`private_key`, `testnet`, `account_address`)

**模式：** 始终先检查环境变量，然后检查配置文件，最后抛出带有有用设置说明的错误。

### 订单大小 vs 美元价值
**关键：** 所有交易函数中的 `size` 参数代表**代币数量**，而非美元价值。
- ✅ `0.1` 表示 0.1 个 SOL 代币
- ❌ `20.0` 误认为是 $20

使用 `calculate_token_amount_from_dollars()` 进行转换。这是最常见的用户错误。

### OCO（一取消其他）订单分组
不同场景使用不同的订单分组：
- **新仓位的止盈止损**: `place_bracket_order()` 使用 `normalTpSl` 分组
- **现有仓位的止盈止损**: `set_position_tpsl()` 使用 `positionTpSl` 分组
- **自定义批量订单**: 重写 `_bulk_orders_with_grouping()` 方法设置适当分组

### 市场操作
- **开仓**: 使用 `market_open_position()` → 调用 `exchange.market_open()`
- **平仓**: 使用 `market_close_position()` → 激进的IOC订单，设置 `reduce_only=True`
- **常规交易**: 使用 `place_limit_order()` 进行标准限价订单

## 服务层架构

### 服务初始化模式
```python
global hyperliquid_service: Optional[HyperliquidServices] = None

def initialize_service():
    global hyperliquid_service
    if hyperliquid_service is None:
        config = get_config()
        hyperliquid_service = HyperliquidServices(
            private_key=config.private_key,
            testnet=config.testnet,
            account_address=config.account_address
        )
```

**在工具函数中使用服务前，始终调用 `initialize_service()`**。

### 自定义SDK扩展
`HyperliquidServices` 类扩展了官方SDK：
- **自定义批量订单**: `_bulk_orders_with_grouping()` 正确设置OCO分组
- **仓位检测**: 自动检测TP/SL订单的仓位大小和方向
- **滑点定价**: `_slippage_price()` 用于激进市场订单
- **统一错误处理**: 所有方法的一致返回格式

## 工具设计模式

### 返回格式标准化
所有工具返回：
```python
{
    "success": bool,
    "data"/"order_result"/"bulk_result": Any,  # 成功数据
    "error": str,  # 失败时的错误描述
    # 其他上下文字段
}
```

### 仓位 vs 新订单管理
- **新仓位**: `market_open_position()`, `place_limit_order()`, `place_bracket_order()`
- **现有仓位**: `set_take_profit_stop_loss()`, `market_close_position()`

不要混合使用这些 - 新仓位工具创建仓位，现有仓位工具修改仓位。

## 开发工作流

### 依赖管理
使用 **Poetry** 进行依赖管理：
- `poetry install` - 安装依赖
- `poetry start` - HTTP服务器模式（生产环境）
- `poetry stdio` - stdio模式（MCP客户端集成）
- `poetry run python main.py` - 直接执行

### 服务器模式
1. **HTTP模式**: `start_server()` → 运行在 `127.0.0.1:8080`
2. **Stdio模式**: `stdio_server()` → 用于MCP客户端连接
3. **直接模式**: `__main__` 块 → 回退到HTTP

## 安全与配置

### 私钥处理
- **绝不提交私钥** 到版本控制
- 支持 **API钱包** （在HyperLiquid仪表板生成）
- 推荐 **测试网优先** 开发
- 如果未提供，账户地址从私钥自动派生

### 网络配置
- `testnet: false` → 主网（默认）
- `testnet: true` → 测试网
- 两个网络使用相同的API URL结构 (`https://api.hyperliquid.xyz`)

## 错误处理模式

### 常见用户错误
1. **大小混淆**: 用户提供美元金额而不是代币数量
2. **客户端订单ID格式**: 必须是128位十六进制字符串 (`0x1234...`)
3. **找不到仓位**: 尝试在不存在的仓位上设置TP/SL
4. **错误的OCO分组**: 对现有仓位使用bracket订单

### 日志策略
- **结构化日志** 包含上下文信息
- **文件日志** 写入 `hyperliquid_mcp.log`
- **错误详情** 包含调试堆栈跟踪
- **API交互日志** 用于故障排除

## 集成点

### HyperLiquid SDK
- 使用官方 `hyperliquid-python-sdk`
- **Info客户端**: 只读操作（余额、仓位、市场数据）
- **Exchange客户端**: 交易操作（订单、取消、转账）
- **钱包集成**: 使用 `eth-account` 进行交易签名

### FastMCP框架
- **工具装饰器**: `@mcp.tool` 用于暴露函数
- **异步工具**: 所有工具都是异步的，保持一致性
- **参数验证**: 使用Pydantic模型进行配置
- **传输选项**: HTTP和stdio传输

修改现有工具时，维护已建立的错误处理、日志记录和返回格式模式。添加新交易功能时，遵循服务层抽象并考虑订单管理的OCO行为。