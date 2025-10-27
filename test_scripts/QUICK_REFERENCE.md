# 测试脚本快速参考

## 🚀 一键运行所有测试

```bash
./test_scripts/run_tests.sh all
```

## 📝 单独运行特定测试

### 基础测试
```bash
# 连接测试
./test_scripts/run_tests.sh connection
uv run python test_scripts/test_connection.py

# 地址验证
./test_scripts/run_tests.sh address
uv run python test_scripts/check_address.py
```

### 账户相关
```bash
# 账户信息
./test_scripts/run_tests.sh account
uv run python test_scripts/test_account_info.py

# 余额检查
./test_scripts/run_tests.sh balance
uv run python test_scripts/check_all_balances.py
```

### 市场数据
```bash
# 市场数据
./test_scripts/run_tests.sh market
uv run python test_scripts/test_market_data.py

# 订单簿
./test_scripts/run_tests.sh orderbook
uv run python test_scripts/test_orderbook.py

# 资金费率
./test_scripts/run_tests.sh funding
uv run python test_scripts/test_funding_history.py

# 价格计算器
./test_scripts/run_tests.sh calculator
uv run python test_scripts/test_price_calculator.py
```

### 交互式工具
```bash
# 交互式测试菜单
uv run python test_scripts/interactive_test.py
```

## 📊 测试脚本说明

| 脚本 | 功能 | 快捷命令 |
|------|------|----------|
| `test_connection.py` | 基础连接测试 | `./test_scripts/run_tests.sh connection` |
| `test_account_info.py` | 完整账户信息 | `./test_scripts/run_tests.sh account` |
| `check_all_balances.py` | 账户余额（现货+合约） | `./test_scripts/run_tests.sh balance` |
| `test_market_data.py` | 多币种市场数据 | `./test_scripts/run_tests.sh market` |
| `test_orderbook.py` | 订单簿深度 | `./test_scripts/run_tests.sh orderbook` |
| `test_funding_history.py` | 资金费率历史 | `./test_scripts/run_tests.sh funding` |
| `test_price_calculator.py` | 美元转代币计算 | `./test_scripts/run_tests.sh calculator` |
| `check_address.py` | 地址验证 | `./test_scripts/run_tests.sh address` |
| `interactive_test.py` | 交互式菜单 | `uv run python test_scripts/interactive_test.py` |

## 🎯 推荐测试流程

### 首次配置
```bash
# 1. 验证配置
./test_scripts/run_tests.sh connection

# 2. 检查地址
./test_scripts/run_tests.sh address

# 3. 检查余额
./test_scripts/run_tests.sh balance
```

### 日常使用
```bash
# 快速检查账户
./test_scripts/run_tests.sh account

# 查看市场数据
./test_scripts/run_tests.sh market

# 交互式探索
uv run python test_scripts/interactive_test.py
```

### 全面测试
```bash
# 运行所有只读测试
./test_scripts/run_tests.sh all
```

## 💡 提示

- 所有测试都是**只读**的，不会修改账户状态
- 使用 `run_tests.sh` 脚本可以获得彩色输出和更好的格式
- 测试脚本会自动从 `.env` 文件加载配置
- 首次使用建议在测试网环境下进行 (`HYPERLIQUID_TESTNET=true`)
