---
mode: 'agent'
model: GPT-5
tools: ['search', 'usages', 'problems', 'changes', 'githubRepo', 'todos']
description: 'HyperLiquid MCP 项目代码质量自动检测与分析'
---

# HyperLiquid MCP 代码审查指南

## 审查目标
对 HyperLiquid MCP 服务器项目进行全面的代码质量检查，确保交易功能的安全性、可靠性和最佳实践。

## 核心审查领域

### 1. 安全性审查 🔒
**重点关注：**
- ✅ 私钥处理：确保私钥永不泄露、正确加密存储
- ✅ 环境变量配置：检查 `.env` 文件是否正确添加到 `.gitignore`
- ✅ API 认证：验证所有交易操作的身份验证机制
- ✅ 输入验证：所有用户输入必须经过严格验证（订单大小、价格、币种等）
- ✅ 错误信息：确保错误信息不暴露敏感数据
- ✅ 测试网/主网隔离：验证网络切换逻辑正确无误

**检查清单：**
```python
# ❌ 错误示例
print(f"Private key: {private_key}")  # 永不打印私钥

# ✅ 正确示例  
logger.info(f"Account initialized: {account_address[:6]}...{account_address[-4:]}")
```

### 2. 交易逻辑审查 💰
**关键模式验证：**
- ✅ **订单大小 vs 美元金额**：确保 `size` 参数代表代币数量，非美元价值
  ```python
  # ❌ 常见错误：用户想买 $20 的 SOL
  place_limit_order(coin="SOL", size=20.0)  # 错误！这是 20 个 SOL
  
  # ✅ 正确做法
  token_amount = calculate_token_amount_from_dollars("SOL", 20.0)
  place_limit_order(coin="SOL", size=token_amount["token_amount"])
  ```

- ✅ **OCO 订单分组**：验证不同场景使用正确的分组类型
  - `normalTpSl`：新仓位的止盈止损（`place_bracket_order`）
  - `positionTpSl`：现有仓位的止盈止损（`set_position_tpsl`）

- ✅ **仓位管理**：区分新仓位操作 vs 现有仓位操作
  - 新仓位：`market_open_position()`, `place_bracket_order()`
  - 现有仓位：`set_take_profit_stop_loss()`, `market_close_position()`

- ✅ **滑点计算**：检查 `_slippage_price()` 方法的正确性

### 3. 异步模式审查 ⚡
**FastMCP 架构要求：**
- ✅ 所有 `@mcp.tool` 装饰的函数必须是 `async def`
- ✅ 服务层调用使用 `await` 关键字
- ✅ 全局服务实例的正确初始化（单例模式）
- ✅ 避免阻塞操作影响异步性能

```python
# ✅ 正确的异步工具实现
@mcp.tool
async def get_account_balance() -> Dict[str, Any]:
    initialize_service()  # 确保服务已初始化
    return await hyperliquid_service.get_account_balance()
```

### 4. 错误处理审查 🛡️
**标准化返回格式：**
```python
# ✅ 成功响应
{
    "success": True,
    "data": {...},
    "order_result": {...}
}

# ✅ 失败响应
{
    "success": False,
    "error": "详细错误描述"
}
```

**检查要点：**
- ✅ 所有 API 调用都有 try-except 包裹
- ✅ 错误日志包含足够的上下文信息
- ✅ 用户友好的错误提示
- ✅ 关键操作失败时的回滚机制

### 5. 日志与监控审查 📊
**日志策略：**
- ✅ 结构化日志：包含时间戳、级别、上下文
- ✅ 文件日志：写入 `hyperliquid_mcp.log`
- ✅ 敏感信息过滤：订单 ID 可记录，私钥绝不记录
- ✅ API 交互日志：记录请求参数和响应（排除敏感数据）

```python
# ✅ 良好的日志实践
self.logger.info(f"Placing order: {coin} {side} {sz} @ {limit_px}")
self.logger.error(f"Failed to place order for {coin}: {e}", exc_info=True)
```

### 6. 配置管理审查 ⚙️
**三层配置系统：**
1. 环境变量（优先级最高）
2. `.env` 文件
3. `config.json` 文件

**验证要点：**
- ✅ 配置加载顺序正确
- ✅ 必需配置缺失时提供清晰的错误提示
- ✅ 配置验证使用 Pydantic 模型
- ✅ 测试网/主网配置清晰标识

### 7. SDK 集成审查 🔌
**HyperLiquid SDK 使用：**
- ✅ Info 客户端：只读操作（余额、持仓、市场数据）
- ✅ Exchange 客户端：交易操作（订单、取消、转账）
- ✅ 自定义扩展：`_bulk_orders_with_grouping()` 正确设置 OCO 分组
- ✅ 钱包集成：`eth-account` 正确签名交易

### 8. 代码质量审查 ✨
**Python 最佳实践：**
- ✅ 类型注解：使用 `typing` 模块标注参数和返回值
- ✅ 文档字符串：所有公共方法包含清晰的 docstring
- ✅ 命名规范：遵循 PEP 8（snake_case 函数，CamelCase 类）
- ✅ 代码复用：避免重复代码，提取通用函数
- ✅ 依赖管理：使用 `uv` 管理依赖，保持 `pyproject.toml` 整洁

## 自动化检查流程

### 步骤 1：问题诊断 🔍
```bash
# 使用 'problems' 工具检查编译和 lint 错误
- 检查类型错误
- 检查未使用的导入
- 检查潜在的 bug
```

### 步骤 2：代码变更分析 📝
```bash
# 使用 'changes' 工具查看最近修改
- 识别新增或修改的交易功能
- 检查是否影响核心安全逻辑
- 验证测试覆盖
```

### 步骤 3：代码搜索 🔎
```bash
# 使用 'search' 工具查找特定模式
- 搜索硬编码的敏感信息（API 密钥、私钥等）
- 查找未处理的异常
- 识别同步代码在异步环境中的使用
```

### 步骤 4：使用情况分析 📈
```bash
# 使用 'usages' 工具分析函数调用
- 验证服务层函数被正确调用
- 检查已弃用的 API 使用
- 识别未使用的代码
```

### 步骤 5：待办事项检查 ✅
```bash
# 使用 'todos' 工具查找未完成工作
- 检查 TODO 注释
- 识别 FIXME 标记
- 查找临时解决方案
```

## 特定场景审查清单

### 新增交易工具函数
- [ ] 函数名清晰描述功能
- [ ] 包含完整的 docstring（参数、返回值、示例）
- [ ] 使用 `@mcp.tool` 装饰器
- [ ] 函数声明为 `async def`
- [ ] 调用 `initialize_service()` 初始化服务
- [ ] 参数验证完整（类型、范围、格式）
- [ ] 错误处理遵循标准返回格式
- [ ] 日志记录关键操作
- [ ] 添加使用示例或测试用例

### 修改核心服务层
- [ ] 保持向后兼容性
- [ ] 更新相关文档
- [ ] 验证所有调用点
- [ ] 添加或更新单元测试
- [ ] 考虑性能影响
- [ ] 审查错误处理路径

### 配置变更
- [ ] 更新 `.env.example` 文件
- [ ] 文档化新配置项
- [ ] 提供默认值或验证逻辑
- [ ] 测试配置缺失场景
- [ ] 更新 README.md

## 输出格式

### 审查报告结构
```markdown
# HyperLiquid MCP 代码审查报告

## 📊 总体评分
- 安全性：X/10
- 代码质量：X/10  
- 文档完整性：X/10
- 测试覆盖率：X/10

## 🔴 严重问题（必须修复）
1. [问题描述]
   - 位置：文件名:行号
   - 影响：安全性/功能性
   - 建议：具体修复方案

## 🟡 警告（建议修复）
1. [问题描述]
   - 位置：文件名:行号
   - 建议：改进方案

## 🟢 最佳实践建议
1. [建议内容]
   - 位置：文件名:行号
   - 优化：具体建议

## 📝 详细分析
[按审查领域组织的详细发现]

## ✅ 操作项
- [ ] 修复严重安全问题
- [ ] 改进错误处理
- [ ] 补充文档
- [ ] 添加测试用例
```

## 参考文档
- **项目文档**：`AGENT.md` - AI 编程指南
- **FastMCP 文档**：https://github.com/jlowin/fastmcp
- **HyperLiquid SDK**：https://github.com/hyperliquid-dex/hyperliquid-python-sdk
- **Python 异步编程**：PEP 492

---

**执行建议**：
1. 优先审查涉及资金操作的代码
2. 关注最近变更的文件
3. 验证所有错误路径的处理
4. 确保文档与代码同步
5. 定期运行自动化检查工具


