# 快速验证

完成配置后，运行测试确保一切正常工作。

## 方式 1：使用 Makefile（推荐）⭐

最简单的方式：

```bash
# 快速验证（连接 + 余额 + 地址）
make test-quick

# 查看所有可用测试
make list-tests

# 运行所有只读测试
make test-all
```

## 方式 2：手动运行测试

### 1. 测试连接

验证能否连接到 HyperLiquid API：

```bash
uv run python test_scripts/test_connection.py
```

成功输出示例：

```
✅ Connection test passed!
Network: Testnet
Account: 0x1234567890abcdef1234567890abcdef12345678
```

### 2. 检查余额

查看账户余额：

```bash
# 检查所有余额（现货 + 合约）
uv run python test_scripts/check_all_balances.py

# 查看详细余额
uv run python test_scripts/check_detailed_balance.py
```

输出示例：

```
📊 HyperLiquid Account Balance

Perpetual Account:
  Total Value: $1,234.56
  Available: $1,000.00
  Margin Used: $234.56

Spot Account:
  USDC: 500.00
  BTC: 0.05
```

### 3. 验证地址

确认账户地址配置正确：

```bash
uv run python test_scripts/test_account_address.py
```

### 4. 测试市场数据

获取实时市场数据：

```bash
uv run python test_scripts/test_market_data.py
```

## 交互式测试工具

推荐使用交互式测试工具，可以方便地测试各种功能：

```bash
uv run python test_scripts/interactive_test.py
```

功能菜单：

```
HyperLiquid MCP Interactive Test

1. Get Account Balance
2. Get Open Positions
3. Get Market Data
4. Get Order Book
5. Calculate Token Amount from Dollars
6. Place Test Order (Testnet Only)
7. Exit

Enter your choice:
```

## 运行测试套件

运行完整的测试套件：

```bash
# 使用测试脚本
./test_scripts/run_tests.sh all

# 或使用 Makefile
make test-all
```

## 验证清单

确保以下测试都通过：

- [ ] ✅ 连接测试通过
- [ ] ✅ 能获取账户余额
- [ ] ✅ 账户地址正确
- [ ] ✅ 能获取市场数据
- [ ] ✅ 能获取订单簿数据

## 常见问题排查

### 连接失败

**错误信息**：`Connection error` 或 `timeout`

**解决方案**：

1. 检查网络连接
2. 确认 `HYPERLIQUID_TESTNET` 设置正确
3. 检查防火墙设置

### 认证失败

**错误信息**：`Authentication failed` 或 `Invalid signature`

**解决方案**：

1. 检查私钥格式（必须以 `0x` 开头）
2. 确认私钥正确
3. 如使用 API 钱包，确认 `ACCOUNT_ADDRESS` 已设置

### 余额为 0

**测试网**：

- 访问 HyperLiquid 测试网水龙头获取测试币
- 确认使用的是测试网地址

**主网**：

- 确认账户已充值
- 检查是否使用了正确的账户地址

### 找不到测试脚本

确保在项目根目录运行：

```bash
cd /path/to/hyperliquid-mcp-python
pwd  # 确认当前目录
ls test_scripts/  # 确认测试脚本存在
```

## 下一步

验证通过后，可以：

1. **学习使用工具**

   - [交易工具](../guides/trading-tools.md)
   - [账户管理](../guides/account-management.md)
   - [市场数据](../guides/market-data.md)

2. **集成到 MCP 客户端**

   - [MCP 客户端集成](../guides/mcp-integration.md)

3. **了解架构**
   - [架构设计](../developers/architecture.md)
   - [测试工具](../developers/testing.md)

## 测试环境建议

### 测试网优先

!!! tip "强烈建议"
**务必先在测试网充分测试**，再考虑使用主网！

测试网优势：

- ✅ 无真实资金风险
- ✅ 可以放心测试各种功能
- ✅ 可以测试错误处理
- ✅ 学习成本低

### 测试流程

1. **配置测试网**

   ```bash
   HYPERLIQUID_TESTNET=true
   ```

2. **获取测试币**

   - 访问 HyperLiquid 测试网
   - 申请测试 USDC

3. **运行所有测试**

   ```bash
   make test-all
   ```

4. **尝试小额交易**

   ```bash
   uv run python test_scripts/test_small_order.py
   ```

5. **验证功能完整性**
   ```bash
   uv run python test_scripts/verify_completion.py
   ```

## 更多测试

查看完整的测试文档：

- [测试工具文档](../developers/testing.md)
- [测试脚本 README](https://github.com/talkincode/hyperliquid-mcp-python/tree/main/test_scripts)
