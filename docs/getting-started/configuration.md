# 配置指南

在使用 HyperLiquid MCP Server 之前，需要配置必要的参数。

## 配置方式

支持三种配置方式（按优先级排序）：

1. **环境变量**（最高优先级）
2. **`.env` 文件**
3. **`config.json` 文件**

## 方式 1：环境变量（推荐）

直接设置环境变量：

```bash
export HYPERLIQUID_PRIVATE_KEY="0x..."
export HYPERLIQUID_TESTNET="true"
export HYPERLIQUID_ACCOUNT_ADDRESS="0x..."  # 可选
```

## 方式 2：.env 文件

创建 `.env` 文件：

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
nano .env
```

`.env` 文件内容：

```bash
# 必填：你的私钥
HYPERLIQUID_PRIVATE_KEY=0x1234567890abcdef...

# 可选：是否使用测试网（默认：false）
HYPERLIQUID_TESTNET=true

# 可选：账户地址（如果不设置，会从私钥自动派生）
HYPERLIQUID_ACCOUNT_ADDRESS=0xabcdef...
```

## 方式 3：config.json 文件

创建 `config.json` 文件：

```json
{
  "private_key": "0x1234567890abcdef...",
  "testnet": true,
  "account_address": "0xabcdef..."
}
```

!!! note "键名格式"
注意 `config.json` 使用 **snake_case** 格式（`private_key`），而环境变量使用 **UPPER_CASE** 格式（`HYPERLIQUID_PRIVATE_KEY`）。

## 配置参数说明

### HYPERLIQUID_PRIVATE_KEY

- **必填**
- **格式**：以 `0x` 开头的十六进制字符串
- **说明**：你的 HyperLiquid 账户私钥

!!! danger "安全警告" - **绝不要**将私钥提交到版本控制 - **绝不要**在公开场合分享私钥 - 建议使用 **API 钱包**而非主钱包

### HYPERLIQUID_TESTNET

- **可选**（默认：`false`）
- **格式**：`true` 或 `false`
- **说明**：是否使用测试网

!!! tip "强烈建议"
在正式使用前，**务必先在测试网**进行充分测试！

### HYPERLIQUID_ACCOUNT_ADDRESS

- **可选**
- **格式**：以 `0x` 开头的以太坊地址
- **说明**：账户地址

!!! info "何时需要设置" - 使用 **API 钱包**时，必须设置为主账户地址 - 使用普通钱包时，会自动从私钥派生，无需设置

## 获取私钥

### 方式 1：使用 API 钱包（推荐）✅

API 钱包是 HyperLiquid 提供的专用交易密钥，权限受限，更安全。

1. 访问 [HyperLiquid API 页面](https://app.hyperliquid.xyz/API)
2. 点击 "Create API Wallet"
3. 保存生成的私钥
4. 设置配置：

```bash
HYPERLIQUID_PRIVATE_KEY=0x...          # API 钱包私钥
HYPERLIQUID_ACCOUNT_ADDRESS=0x...      # 你的主账户地址
```

### 方式 2：使用主钱包私钥

!!! warning "不推荐"
使用主钱包私钥风险较高，仅建议在测试网使用。

1. 从 MetaMask 或其他钱包导出私钥
2. 设置配置：

```bash
HYPERLIQUID_PRIVATE_KEY=0x...          # 主钱包私钥
# 无需设置 ACCOUNT_ADDRESS，会自动派生
```

## 网络选择

### 测试网

```bash
HYPERLIQUID_TESTNET=true
```

- **优点**：安全测试，无真实资金风险
- **缺点**：需要申请测试币
- **适用场景**：开发、测试、学习

### 主网

```bash
HYPERLIQUID_TESTNET=false  # 或不设置
```

- **优点**：真实交易
- **缺点**：涉及真实资金
- **适用场景**：生产环境

!!! danger "主网使用前"
确保已在测试网充分测试，理解所有风险！

## 验证配置

运行配置验证：

```bash
# 使用 Makefile
make config

# 或直接运行
uv run python -c "from main import get_config; print(get_config())"
```

输出示例：

```
Network: Testnet
Account: 0x1234567890abcdef1234567890abcdef12345678
Private Key: 0x**** (hidden)
```

## 快速测试

验证配置是否正确：

```bash
# 快速验证（连接 + 余额 + 地址）
make test-quick

# 或手动运行
uv run python test_scripts/test_connection.py
```

## 安全最佳实践

### ✅ 推荐做法

- 使用 **API 钱包**
- 先在**测试网**测试
- 将 `.env` 添加到 `.gitignore`
- 使用**环境变量**而非配置文件
- 定期**轮换** API 密钥

### ❌ 避免做法

- 提交私钥到 Git
- 在主网直接测试
- 使用主钱包私钥
- 在公共场合分享配置
- 硬编码私钥到代码

## 多环境配置

### 开发环境

```bash
# .env.development
HYPERLIQUID_PRIVATE_KEY=0x...
HYPERLIQUID_TESTNET=true
```

### 生产环境

```bash
# .env.production
HYPERLIQUID_PRIVATE_KEY=0x...
HYPERLIQUID_TESTNET=false
```

### 使用不同配置

```bash
# 加载开发环境
cp .env.development .env

# 加载生产环境
cp .env.production .env
```

## 常见问题

### 私钥格式错误

确保私钥：

- 以 `0x` 开头
- 包含 64 个十六进制字符（不含 `0x` 前缀）
- 示例：`0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`

### 找不到配置文件

确保 `.env` 或 `config.json` 在项目根目录：

```bash
# 检查文件位置
ls -la .env
ls -la config.json
```

### API 钱包地址未设置

使用 API 钱包时必须设置主账户地址：

```bash
HYPERLIQUID_ACCOUNT_ADDRESS=0x...  # 你的主账户地址，不是 API 钱包地址
```

## 下一步

- [快速验证](quick-start.md) - 运行测试确保配置正确
- [MCP 客户端集成](../guides/mcp-integration.md) - 与 Claude Desktop 集成
- [交易工具](../guides/trading-tools.md) - 开始使用交易功能
