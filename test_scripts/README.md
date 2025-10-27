# HyperLiquid MCP 测试脚本

这个文件夹包含用于测试 HyperLiquid MCP 服务器的各种测试脚本。

## 📁 测试脚本列表

### 1. `test_connection.py` - 基础连接测试
快速验证配置和基本功能是否正常。

**用途**：
- 验证配置文件是否正确
- 测试与 HyperLiquid API 的连接
- 检查基本功能（余额、持仓、订单、市场数据）

**运行**：
```bash
uv run python test_scripts/test_connection.py
```

**输出**：显示 5 个基础测试的结果

---

### 2. `check_all_balances.py` - 完整余额检查
检查现货和合约账户的详细余额。

**用途**：
- 查看合约账户（Perpetual）余额
- 查看现货账户（Spot）余额
- 了解账户间转账方法

**运行**：
```bash
uv run python test_scripts/check_all_balances.py
```

**输出**：
- 合约账户余额详情
- 现货账户代币列表
- 转账指南（如需要）

---

### 3. `check_address.py` - 地址验证
验证配置的账户地址是否正确。

**用途**：
- 检查 `.env` 中配置的地址
- 从私钥派生地址并验证
- 对比 UI 中显示的地址

**运行**：
```bash
uv run python test_scripts/check_address.py
```

**输出**：
- 配置的地址
- 从私钥派生的地址
- 地址匹配状态

---

### 4. `check_detailed_balance.py` - 详细余额信息
获取原始 API 返回的完整用户状态。

**用途**：
- 查看完整的 API 响应
- 调试余额问题
- 查看资产持仓详情

**运行**：
```bash
uv run python test_scripts/check_detailed_balance.py
```

**输出**：完整的 JSON 格式用户状态

---

### 5. `test_small_order.py` - 小额订单测试
通过下一个小额测试订单来验证账户余额和交易功能。

**用途**：
- 验证账户是否真的有余额
- 测试下单功能
- 验证 API 权限

**运行**：
```bash
uv run python test_scripts/test_small_order.py
```

**功能**：
- 获取当前市价
- 下一个低于市价 5% 的限价单（不会成交）
- 确认后自动取消订单

**注意**：会提示确认后才下单

---

### 6. `interactive_test.py` - 交互式测试工具 ⭐ 推荐
提供交互式菜单，方便测试各种功能。

**用途**：
- 交互式测试所有功能
- 无需编写代码
- 适合快速验证和学习

**运行**：
```bash
uv run python test_scripts/interactive_test.py
```

**功能菜单**：
1. 查看账户余额
2. 查看持仓
3. 查看未平仓订单
4. 查看市场数据 (BTC)
5. 查看市场数据 (ETH)
6. 查看市场数据 (SOL)
7. 查看账户摘要
8. 计算美元转代币数量
9. 获取订单簿 (BTC)
0. 退出

---

### 7. `test_market_data.py` - 市场数据测试

获取多个币种的市场数据并显示汇总表格。

**用途**：
- 批量获取多个币种的市场数据
- 查看价格、成交量、资金费率
- 对比不同币种的市场状况

**运行**：
```bash
uv run python test_scripts/test_market_data.py
```

**输出**：显示 BTC, ETH, SOL, ARB, OP 的市场数据表格

---

### 8. `test_orderbook.py` - 订单簿测试

获取并显示订单簿的买卖盘数据。

**用途**：
- 查看实时订单簿
- 分析买卖价差
- 了解市场深度

**运行**：
```bash
uv run python test_scripts/test_orderbook.py
```

**输出**：
- 最佳 5 档买卖盘
- 买卖价差统计
- 订单簿深度信息

---

### 9. `test_funding_history.py` - 资金费率历史

获取并分析过去几天的资金费率数据。

**用途**：
- 查看历史资金费率
- 计算平均资金费率和年化
- 分析资金费率趋势

**运行**：
```bash
uv run python test_scripts/test_funding_history.py
```

**输出**：
- 最近 10 条资金费率记录
- 平均资金费率和年化
- 多个币种对比

---

### 10. `test_price_calculator.py` - 价格计算器

测试美元金额转代币数量的计算功能。

**用途**：
- 计算不同金额可以购买多少代币
- 验证价格转换的准确性
- 学习如何使用价格计算工具

**运行**：
```bash
uv run python test_scripts/test_price_calculator.py
```

**输出**：不同美元金额对应的代币数量表格

---

### 11. `test_account_info.py` - 完整账户信息

获取账户的完整信息概览。

**用途**：
- 一次性查看所有账户信息
- 包含余额、持仓、订单、交易历史
- 适合快速了解账户状态

**运行**：
```bash
uv run python test_scripts/test_account_info.py
```

**输出**：
- 账户余额
- 当前持仓
- 未平仓订单
- 最近 7 天交易历史

---

### 🎯 `run_tests.sh` - 测试套件脚本（推荐）⭐

一键运行所有测试或选择性运行特定测试。

**用途**：
- 自动化测试流程
- 交互式菜单选择测试
- 批量运行所有只读测试

**运行方式 1 - 交互式菜单**：
```bash
./test_scripts/run_tests.sh
```

**运行方式 2 - 命令行参数**：
```bash
# 运行所有测试
./test_scripts/run_tests.sh all

# 运行特定测试
./test_scripts/run_tests.sh market        # 市场数据测试
./test_scripts/run_tests.sh orderbook    # 订单簿测试
./test_scripts/run_tests.sh account      # 账户信息测试
./test_scripts/run_tests.sh connection   # 基础连接测试
```

**可用选项**：
- `1` 或 `connection` - 基础连接测试
- `2` 或 `account` - 账户信息测试
- `3` 或 `balance` - 账户余额检查
- `4` 或 `market` - 市场数据测试
- `5` 或 `orderbook` - 订单簿测试
- `6` 或 `funding` - 资金费率历史测试
- `7` 或 `calculator` - 价格计算器测试
- `8` 或 `address` - 地址验证测试
- `9` 或 `all` - 运行所有测试

---

## 🚀 快速开始

### 第一次使用？

**推荐方式 - 使用测试套件脚本**：
```bash
# 运行所有只读测试
./test_scripts/run_tests.sh all

# 或使用交互式菜单
./test_scripts/run_tests.sh
```

**手动运行单个测试**：
1. **验证配置**：
   ```bash
   uv run python test_scripts/test_connection.py
   ```

2. **检查余额**：
   ```bash
   uv run python test_scripts/check_all_balances.py
   ```

3. **查看市场数据**：
   ```bash
   uv run python test_scripts/test_market_data.py
   ```

4. **交互式探索**：
   ```bash
   uv run python test_scripts/interactive_test.py
   ```

---

## 🔧 故障排查

### 问题：显示余额为 $0

运行以下脚本诊断：
```bash
# 1. 检查地址是否匹配
uv run python test_scripts/check_address.py

# 2. 检查现货和合约账户
uv run python test_scripts/check_all_balances.py

# 3. 查看详细状态
uv run python test_scripts/check_detailed_balance.py
```

### 问题：地址不匹配

如果 UI 中显示的地址和 API 使用的地址不同：
- 使用 API 钱包：在 `.env` 中设置 `HYPERLIQUID_ACCOUNT_ADDRESS` 为主账号地址
- 使用主账号：更新 `.env` 中的 `HYPERLIQUID_PRIVATE_KEY`

---

## 📝 注意事项

1. **测试网优先**：所有测试建议先在测试网进行
2. **小额测试**：首次使用建议使用小额资金测试
3. **私钥安全**：永远不要分享或提交私钥到版本控制
4. **API 钱包**：推荐使用 API 钱包代理主账号进行操作

---

## 🔗 相关文档

- [主 README](../README.md)
- [示例文档](../EXAMPLES.md)
- [HyperLiquid 官方文档](https://hyperliquid.gitbook.io/)
- [HyperLiquid API 文档](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api)

---

## 💡 提示

- 使用 `interactive_test.py` 可以快速熟悉所有功能
- 每个脚本都可以独立运行，无需额外配置
- 所有脚本都会自动加载 `.env` 配置文件
