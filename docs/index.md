# HyperLiquid MCP Server

[![CI](https://github.com/talkincode/hyperliquid-mcp-python/actions/workflows/ci.yml/badge.svg)](https://github.com/talkincode/hyperliquid-mcp-python/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/hyperliquid-mcp-python.svg)](https://badge.fury.io/py/hyperliquid-mcp-python)
[![Python Versions](https://img.shields.io/pypi/pyversions/hyperliquid-mcp-python.svg)](https://pypi.org/project/hyperliquid-mcp-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 FastMCP 的 HyperLiquid 交易 MCP 服务器。为 AI 助手提供与 HyperLiquid 永续合约和现货交易平台交互的工具。

!!! success "致谢"
本项目 Fork 自 [GigabrainGG/hyperliquid-mcp](https://github.com/GigabrainGG/hyperliquid-mcp)，感谢原作者的出色工作！

## ✨ 主要功能

### 🚀 交易工具

- **市价订单**：使用 HyperLiquid 原生函数优化的开仓和平仓
- **限价订单**：支持 reduce-only 和自定义订单 ID 追踪
- **括号订单**：一键创建带止盈止损的新仓位（OCO 行为）
- **订单管理**：按 ID 或客户端 ID 取消订单、批量取消、修改订单
- **仓位管理**：查看仓位、平仓（全部或部分）、获取盈亏信息
- **高级止盈止损**：为现有仓位设置 OCO 止盈止损

### 📊 账户管理

- **余额信息**：获取账户余额和保证金详情
- **仓位跟踪**：监控所有开仓及未实现盈亏
- **交易历史**：查询成交记录和交易历史
- **杠杆控制**：为不同资产更新杠杆设置
- **资金划转**：在现货和合约账户间转移资金

### 📈 市场数据

- **实时价格**：获取当前市场数据，包括买卖价差
- **订单簿**：获取可配置深度的实时订单簿数据
- **资金费率**：访问历史资金费率信息

### 🛠️ 实用工具

- **账户总览**：获取账户综合概览
- **美元转换**：根据当前价格计算代币数量
- **仓位管理**：专用的现有仓位管理工具

## 🎯 快速开始

=== "使用 uvx（推荐）"

    **最简单的方式** - 无需安装，直接运行：

    ```bash
    # 查看帮助
    uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp --help

    # 启动 HTTP 服务器
    uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp start

    # 启动 stdio 服务器（用于 MCP 客户端）
    uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp stdio
    ```

    !!! info "为什么指定 Python 3.13?"
        依赖包 `ckzg` 目前只提供到 Python 3.13 的预编译包，Python 3.14 还不支持。

=== "本地开发"

    ```bash
    # 克隆仓库
    git clone https://github.com/talkincode/hyperliquid-mcp-python.git
    cd hyperliquid-mcp-python

    # 安装依赖
    uv sync

    # 配置
    cp .env.example .env  # 然后编辑 .env 文件

    # 运行
    uv run hyperliquid-mcp              # HTTP 模式
    uv run hyperliquid-mcp stdio        # stdio 模式
    ```

=== "pip 安装"

    ```bash
    # 使用 pip（需要 Python 3.10-3.13）
    pip install hyperliquid-mcp-python

    # 运行
    hyperliquid-mcp --help
    ```

## 📚 文档导航

<div class="grid cards" markdown>

- :material-rocket-launch:{ .lg .middle } **快速开始**

  ***

  了解如何安装、配置和运行 HyperLiquid MCP Server

  [:octicons-arrow-right-24: 开始使用](getting-started/installation.md)

- :material-book-open-variant:{ .lg .middle } **使用指南**

  ***

  学习如何使用各种交易工具、管理账户和获取市场数据

  [:octicons-arrow-right-24: 查看指南](guides/trading-tools.md)

- :material-code-braces:{ .lg .middle } **API 参考**

  ***

  完整的工具列表、参数说明和返回格式文档

  [:octicons-arrow-right-24: API 文档](api/tools-reference.md)

- :material-wrench:{ .lg .middle } **开发者文档**

  ***

  了解架构设计、测试工具和如何贡献代码

  [:octicons-arrow-right-24: 开发文档](developers/architecture.md)

</div>

## ⚠️ 重要提示

!!! warning "安全建议" - 绝不提交包含私钥的 `.env` 文件 - **强烈建议先使用测试网**进行测试 - 建议使用 API 钱包：https://app.hyperliquid.xyz/API

!!! danger "交易风险"
加密货币交易涉及重大风险。本项目仅供学习使用，请谨慎使用真实资金。

## 🔗 相关链接

- [HyperLiquid 文档](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [FastMCP](https://fastmcp.com)
- [MCP 协议](https://github.com/anthropics/mcp)
- [GitHub 仓库](https://github.com/talkincode/hyperliquid-mcp-python)
- [PyPI 包](https://pypi.org/project/hyperliquid-mcp-python/)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](https://github.com/talkincode/hyperliquid-mcp-python/blob/main/LICENSE) 文件了解详情。
