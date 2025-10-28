# 安装指南

HyperLiquid MCP Server 提供多种安装方式，选择最适合你的方式开始使用。

## 方式 1：使用 uvx（推荐）🚀

这是**最简单的方式** - 无需安装，直接运行！

### 前提条件

确保已安装 [uv](https://github.com/astral-sh/uv)：

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 运行服务器

```bash
# 查看帮助
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp --help

# 启动 HTTP 服务器（默认 127.0.0.1:8080）
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp start

# 启动 stdio 服务器（用于 MCP 客户端）
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp stdio
```

!!! info "为什么要指定 `--python 3.13`?"
依赖包 `ckzg` 目前只提供到 Python 3.13 的预编译包，Python 3.14 还不支持。指定版本可以避免编译错误。

## 方式 2：本地开发安装

适合需要修改代码或深度定制的开发者。

### 克隆仓库

```bash
git clone https://github.com/talkincode/hyperliquid-mcp-python.git
cd hyperliquid-mcp-python
```

### 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 运行

```bash
# 使用 Makefile（最简单）
make run-http        # HTTP 服务器
make run-stdio       # stdio 服务器

# 或直接使用 uv
uv run hyperliquid-mcp              # HTTP 模式
uv run hyperliquid-mcp stdio        # stdio 模式

# 或使用已安装的命令
hyperliquid-mcp                     # HTTP 模式
hyperliquid-mcp stdio               # stdio 模式
```

## 方式 3：pip 安装

适合在现有 Python 环境中使用。

### 要求

- Python 3.10-3.13（不支持 3.14）

### 安装

```bash
pip install hyperliquid-mcp-python
```

### 运行

```bash
hyperliquid-mcp --help              # 查看帮助
hyperliquid-mcp                     # HTTP 服务器
hyperliquid-mcp stdio               # stdio 服务器
```

## Python 版本说明

!!! warning "重要提示" - **支持版本**：Python 3.10, 3.11, 3.12, 3.13 - **不支持**：Python 3.14（依赖包 `ckzg` 尚未提供预编译包） - **推荐版本**：Python 3.13

### 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

## 验证安装

安装完成后，验证是否正常工作：

```bash
# 查看版本
hyperliquid-mcp --version

# 查看帮助
hyperliquid-mcp --help

# 测试连接（需要先配置）
uv run python test_scripts/test_connection.py
```

## 下一步

- [配置服务器](configuration.md) - 设置私钥和网络
- [快速验证](quick-start.md) - 运行测试确保一切正常
- [MCP 客户端集成](../guides/mcp-integration.md) - 与 Claude Desktop 集成

## 常见问题

### 编译错误

如果遇到 `ckzg` 编译错误：

```bash
# 指定 Python 3.13
uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp
```

### 命令未找到

如果 `hyperliquid-mcp` 命令未找到：

```bash
# 确保已安装
pip show hyperliquid-mcp-python

# 使用完整路径
python -m cli

# 或使用 uv
uv run hyperliquid-mcp
```

### 权限问题

在 macOS/Linux 上，可能需要添加执行权限：

```bash
chmod +x /path/to/hyperliquid-mcp
```

## 卸载

```bash
# pip 安装
pip uninstall hyperliquid-mcp-python

# 本地开发
rm -rf .venv
```
