# HyperLiquid MCP Agent 架构指南

## 📋 概述

HyperLiquid MCP Server 是一个基于 **Model Context Protocol (MCP)** 的 AI Agent 系统，为 AI 助手提供 HyperLiquid 交易平台的完整功能访问。本文档描述了 Agent 的架构、工作流程和最佳实践。

## 🏗️ 架构设计

### 三层架构模式

```
┌─────────────────────────────────────────────────────┐
│              AI Assistant / Client                   │
│           (Claude Desktop, Cline, etc.)              │
└────────────────────┬────────────────────────────────┘
                     │ MCP Protocol
                     │ (JSON-RPC)
┌────────────────────▼────────────────────────────────┐
│             MCP Server Layer (main.py)               │
│  - Tool Definitions (@mcp.tool)                      │
│  - Configuration Management                          │
│  - Request/Response Handling                         │
│  - Global Service Instance                           │
└────────────────────┬────────────────────────────────┘
                     │ Service API
                     │
┌────────────────────▼────────────────────────────────┐
│     Service Layer (services/)                        │
│  - HyperliquidServices (交易逻辑)                    │
│  - Validators (输入验证)                             │
│  - Constants (配置常量)                              │
└────────────────────┬────────────────────────────────┘
                     │ SDK API
                     │
┌────────────────────▼────────────────────────────────┐
│         HyperLiquid Python SDK                       │
│  - Info Client (只读操作)                            │
│  - Exchange Client (交易操作)                        │
└─────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. MCP Server (`main.py`)

- **角色**: 协议层，处理 MCP 请求
- **职责**:
  - 定义和暴露工具 (tools)
  - 管理配置加载 (环境变量 → .env → config.json)
  - 初始化全局服务实例
  - 处理错误和返回格式
- **关键模式**:
  - 全局单例: `hyperliquid_service` 实例复用
  - 异步优先: 所有工具都是 async 函数
  - 懒加载: 服务在首次调用时初始化

#### 2. Service Layer (`services/`)

- **HyperliquidServices**: 核心业务逻辑
  - 封装 HyperLiquid SDK 调用
  - 实现自定义批量订单逻辑
  - 处理 OCO 订单分组
  - 统一错误处理和日志
- **Validators**: 输入验证

  - 参数类型和范围检查
  - 交易对和方向验证
  - 订单大小和价格验证
  - 自定义 ValidationError 异常

- **Constants**: 配置常量
  - OCO 订单分组常量
  - 订单类型定义
  - 默认配置值

#### 3. HyperLiquid SDK

- **Info Client**: 只读操作 (市场数据、账户信息)
- **Exchange Client**: 交易操作 (下单、撤单、转账)
- **钱包集成**: eth-account 签名

## 🔧 Agent 工作流程

### 1. 配置加载流程

```python
环境变量 (HYPERLIQUID_*)
    ↓ (如果不存在)
.env 文件
    ↓ (如果不存在)
config.json
    ↓ (如果都不存在)
抛出配置错误 + 帮助信息
```

### 2. 工具调用流程

```
AI 请求 → MCP Tool
    ↓
initialize_service() (如需要)
    ↓
参数验证 (validators)
    ↓
HyperliquidServices 方法调用
    ↓
HyperLiquid SDK API
    ↓
返回标准化响应格式
```

### 3. 标准响应格式

所有工具返回统一格式：

```python
{
    "success": bool,              # 操作是否成功
    "data" / "order_result": {},  # 成功时的数据
    "error": str,                 # 失败时的错误描述
    # ... 其他上下文字段
}
```

## 🛠️ 可用工具 (Tools)

### 市场数据工具

| 工具名                | 功能         | 类型 |
| --------------------- | ------------ | ---- |
| `get_market_overview` | 获取市场概览 | 只读 |
| `get_orderbook`       | 获取订单簿   | 只读 |
| `get_l2_snapshot`     | L2 市场快照  | 只读 |
| `get_candles`         | K 线数据     | 只读 |
| `get_funding_history` | 资金费率历史 | 只读 |

### 账户管理工具

| 工具名                | 功能       | 类型 |
| --------------------- | ---------- | ---- |
| `get_user_state`      | 账户状态   | 只读 |
| `get_account_balance` | 账户余额   | 只读 |
| `get_positions`       | 持仓信息   | 只读 |
| `get_open_orders`     | 未成交订单 | 只读 |

### 交易执行工具

| 工具名                      | 功能                  | OCO 分组       |
| --------------------------- | --------------------- | -------------- |
| `place_limit_order`         | 限价单                | -              |
| `market_open_position`      | 市价开仓              | -              |
| `market_close_position`     | 市价平仓              | -              |
| `place_bracket_order`       | Bracket 订单 (新仓位) | `normalTpSl`   |
| `set_take_profit_stop_loss` | 止盈止损 (现有仓位)   | `positionTpSl` |
| `cancel_order`              | 撤单                  | -              |
| `cancel_all_orders`         | 撤销所有订单          | -              |

### 工具函数工具

| 工具名                                | 功能           | 类型 |
| ------------------------------------- | -------------- | ---- |
| `calculate_token_amount_from_dollars` | 美元转代币数量 | 计算 |
| `calculate_slippage_price`            | 滑点价格计算   | 计算 |

## 🎯 Agent 提示模式

项目包含专门的 Agent 提示模板：

### Planner Agent (`planner.prompt.md`)

**用途**: 项目规划和需求分析

**核心职责**:

1. 深度分析项目结构
2. 精准理解用户意图
3. MVP 最小化原则
4. 单一焦点规划
5. 协助创建 Issues 和 PR

**工作流程**:

```
项目结构分析 → 理解用户意图 → MVP 规划
    ↓
优先级评估 → 技术方案设计 → 工作量评估
    ↓
生成规划 → 询问创建 Issue → 询问创建 PR
```

**使用场景**:

- 新功能开发规划
- Bug 修复任务分解
- 代码优化方案设计
- 文档完善计划

## 💡 开发最佳实践

### 1. 添加新工具

```python
@mcp.tool()
async def new_trading_tool(
    coin: str,
    size: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    工具描述 (AI 会读取这个文档字符串)

    Args:
        coin: 交易对 (如 "BTC")
        size: 代币数量 (不是美元金额!)
        price: 限价 (可选)

    Returns:
        标准化响应格式
    """
    try:
        # 1. 初始化服务
        initialize_service()

        # 2. 验证输入
        validated = validate_order_inputs(coin, "buy", size, price)

        # 3. 调用服务层
        result = hyperliquid_service.your_method(
            coin=validated["coin"],
            is_buy=validated["is_buy"],
            size=validated["size"],
            price=validated.get("price")
        )

        # 4. 返回标准格式
        return {
            "success": True,
            "data": result
        }
    except ValidationError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
```

### 2. 订单大小处理

**关键**: `size` 参数表示**代币数量**，不是美元金额！

```python
# ✅ 正确
size = 0.1  # 0.1 个 BTC

# ❌ 错误
size = 100  # 用户想要 $100，但会被理解为 100 个 BTC
```

**解决方案**: 使用 `calculate_token_amount_from_dollars`

```python
# 用户想用 $100 买 BTC
token_amount = calculate_token_amount_from_dollars(
    coin="BTC",
    dollar_amount=100
)
# 返回: {"success": True, "token_amount": 0.00105, ...}
```

### 3. OCO 订单分组

不同场景使用不同分组：

```python
# 新仓位的止盈止损
place_bracket_order()  # 使用 normalTpSl

# 现有仓位的止盈止损
set_take_profit_stop_loss()  # 使用 positionTpSl

# 自定义批量订单
_bulk_orders_with_grouping()  # 自定义分组
```

### 4. 错误处理模式

```python
# 服务层方法
def trading_method(self):
    try:
        result = self.exchange.some_action()
        logger.info(f"Success: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in trading_method: {e}", exc_info=True)
        raise

# 工具层捕获
async def tool():
    try:
        result = service.trading_method()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 5. 日志策略

```python
import logging

logger = logging.getLogger(__name__)

# 操作日志
logger.info(f"Placing order: {coin} {side} {size}")

# 调试信息
logger.debug(f"Order params: {params}")

# 错误日志 (带堆栈)
logger.error(f"Order failed: {e}", exc_info=True)

# 警告
logger.warning(f"High slippage detected: {slippage}%")
```

## 🔐 安全考虑

### 1. 私钥管理

```python
# ✅ 从环境变量加载
private_key = os.getenv("HYPERLIQUID_PRIVATE_KEY")

# ✅ 从 .env 文件
load_dotenv()

# ❌ 绝不硬编码
private_key = "0x123..."  # 危险！
```

### 2. 测试网优先

```python
# 开发时使用测试网
testnet = True

# 生产环境
testnet = False
```

### 3. API 钱包

推荐使用 HyperLiquid 控制面板生成的 **API 钱包**：

- 权限可控
- 资金隔离
- 易于撤销

## 📊 监控和调试

### 日志文件

```bash
# 查看日志
tail -f hyperliquid_mcp.log

# 或使用 Makefile
make logs
```

### 测试工具

```bash
# 快速验证
make test-quick

# 完整测试
make test-all

# 交互式测试
make test-interactive
```

### 调试模式

```python
# 在 main.py 中启用调试
logging.basicConfig(
    level=logging.DEBUG,  # 显示所有日志
    ...
)
```

## 🚀 部署模式

### 1. HTTP 模式 (开发)

```bash
make run-http
# 访问: http://127.0.0.1:8080
```

**用途**:

- 开发调试
- API 测试
- 健康检查

### 2. Stdio 模式 (生产)

```bash
make run-stdio
```

**用途**:

- MCP 客户端集成 (Claude Desktop)
- 进程间通信
- 生产环境

### 3. Claude Desktop 配置

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uvx",
      "args": ["--from", "hyperliquid-mcp-python", "hyperliquid-mcp", "stdio"],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "your_key",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

## 📚 学习路径

### 初学者

1. 阅读 `README.md` - 基础使用
2. 运行 `make test-connection` - 验证配置
3. 尝试只读工具 - 查询市场数据
4. 查看 `test_scripts/` - 学习示例

### 进阶

1. 阅读 `.github/copilot-instructions.md` - 架构细节
2. 研究 `services/hyperliquid_services.py` - 核心逻辑
3. 理解 OCO 订单分组 - 复杂交易场景
4. 自定义工具 - 扩展功能

### 高级

1. 研究 MCP 协议 - 底层通信
2. 优化性能 - 异步和缓存
3. 扩展 SDK - 新功能集成
4. 贡献代码 - 提交 PR

## 🔗 相关资源

- **MCP 官方文档**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **FastMCP 框架**: [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **HyperLiquid SDK**: [github.com/hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
- **HyperLiquid API**: [hyperliquid.gitbook.io](https://hyperliquid.gitbook.io)

## 🎓 常见问题

### Q: Agent 如何知道用户想用多少钱交易？

A: Agent 需要主动询问或使用 `calculate_token_amount_from_dollars` 工具转换。`size` 参数永远是代币数量，不是美元金额。

### Q: 什么时候使用 bracket order vs set TP/SL？

A:

- **Bracket Order**: 开新仓位时同时设置止盈止损
- **Set TP/SL**: 为现有仓位添加或修改止盈止损

### Q: 如何处理滑点？

A: 使用 `calculate_slippage_price` 工具计算合理的限价，或使用市价单时接受市场价格。

### Q: 测试网和主网的区别？

A: 测试网使用测试资金，主网使用真实资金。API 端点相同，通过 `testnet` 参数区分。

### Q: 如何调试 MCP 通信问题？

A:

1. 查看 `hyperliquid_mcp.log`
2. 设置 `logging.DEBUG` 级别
3. 使用 HTTP 模式测试工具

## 🤝 贡献指南

在开发新功能时：

1. **使用 Planner Agent**: 先用 `planner.prompt.md` 规划
2. **遵循架构**: 保持三层架构分离
3. **编写测试**: 单元测试 + 集成测试
4. **更新文档**: 代码和文档同步更新
5. **代码质量**: 运行 `make format` 和 `make lint`
6. **文档克制**: 代码和适当的注解已经足够，不要为每次新的修改创建说明文档。

参考 `CONTRIBUTING.md` 了解详细流程。

---

**最后更新**: 2025-10-28
**维护者**: @talkincode
**许可证**: MIT
