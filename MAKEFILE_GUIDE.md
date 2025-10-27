# Makefile 使用指南

## 🚀 快速开始

```bash
# 1. 安装依赖
make install

# 2. 查看配置
make config

# 3. 快速验证
make test-quick

# 4. 运行服务器
make run-http
```

## 📋 所有命令

### 开发命令

| 命令 | 说明 |
|------|------|
| `make install` | 安装依赖（uv sync） |
| `make dev` | 开发模式安装 |
| `make run-http` | 启动 HTTP 服务器 (http://127.0.0.1:8080) |
| `make run-stdio` | 启动 stdio 服务器（用于 MCP 客户端） |
| `make config` | 查看当前配置（隐藏私钥） |
| `make logs` | 查看日志文件 |

### 测试命令

| 命令 | 说明 |
|------|------|
| `make test-all` | 运行所有只读测试 ⭐ |
| `make test-quick` | 快速验证（连接+余额+地址） |
| `make test-connection` | 基础连接测试 |
| `make test-account` | 账户信息测试 |
| `make test-balance` | 账户余额检查（现货+合约） |
| `make test-market` | 市场数据测试 |
| `make test-orderbook` | 订单簿测试 |
| `make test-funding` | 资金费率历史测试 |
| `make test-calculator` | 价格计算器测试 |
| `make test-address` | 地址验证测试 |
| `make test-interactive` | 交互式测试工具 |
| `make list-tests` | 列出所有可用测试脚本 |

### 代码质量

| 命令 | 说明 |
|------|------|
| `make format` | 格式化代码（black + isort） |
| `make check` | 检查代码但不修改 |
| `make lint` | 运行代码检查 |
| `make test` | 运行单元测试 |

### 构建和发布

| 命令 | 说明 |
|------|------|
| `make clean` | 清理构建文件 |
| `make build` | 构建发布包 |
| `make publish` | 发布到 PyPI |
| `make test-pypi` | 发布到测试 PyPI |
| `make all` | clean + build |
| `make release` | clean + build + publish |

### 文档和帮助

| 命令 | 说明 |
|------|------|
| `make help` | 显示所有可用命令 |
| `make test-help` | 显示测试快速参考 |
| `make docs` | 显示完整 README |
| `make test-docs` | 显示测试文档 |
| `make list-tests` | 列出所有测试脚本 |

## 🎯 常用工作流

### 首次配置

```bash
# 1. 克隆仓库
git clone https://github.com/jamiesun/hyperliquid-mcp.git
cd hyperliquid-mcp

# 2. 安装依赖
make install

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的配置

# 4. 验证配置
make test-quick

# 5. 运行所有测试
make test-all
```

### 日常开发

```bash
# 查看配置
make config

# 测试连接
make test-connection

# 启动服务器
make run-http

# 查看日志
make logs
```

### 测试新功能

```bash
# 测试市场数据
make test-market

# 测试账户信息
make test-account

# 交互式测试
make test-interactive
```

### 发布新版本

```bash
# 清理
make clean

# 构建
make build

# 发布到测试 PyPI
make test-pypi

# 发布到正式 PyPI
make publish
```

## 💡 提示

- 所有测试命令都是**只读**的，不会修改账户状态
- 使用 `make test-quick` 可以快速验证配置是否正确
- `make test-all` 会运行所有测试，适合全面检查
- `make config` 会隐藏私钥，可以安全地查看配置
- 首次使用建议在测试网环境下进行 (`HYPERLIQUID_TESTNET=true`)

## 🔗 相关文档

- [主 README](../README.md)
- [测试脚本文档](test_scripts/README.md)
- [测试快速参考](test_scripts/QUICK_REFERENCE.md)
