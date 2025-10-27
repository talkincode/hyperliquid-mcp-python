#!/usr/bin/env python3
"""
HyperLiquid MCP CLI 入口

用法:
    hyperliquid-mcp              # 启动 HTTP 服务器（默认）
    hyperliquid-mcp start        # 启动 HTTP 服务器
    hyperliquid-mcp stdio        # 启动 stdio 服务器
    hyperliquid-mcp --help       # 显示帮助
"""
import argparse
import sys

from main import start_server, stdio_server


def main():
    """HyperLiquid MCP 服务器的主 CLI 入口"""
    parser = argparse.ArgumentParser(
        description="HyperLiquid MCP 服务器 - 交易工具和账户管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 启动 HTTP 服务器（默认在 127.0.0.1:8080）
    hyperliquid-mcp
    hyperliquid-mcp start

    # 启动 stdio 服务器（用于 MCP 客户端）
    hyperliquid-mcp stdio

配置:
    设置环境变量或创建 config.json：
    - HYPERLIQUID_PRIVATE_KEY      (必填)
    - HYPERLIQUID_TESTNET          (可选，默认: false)
    - HYPERLIQUID_ACCOUNT_ADDRESS  (可选，从私钥派生)

更多信息，访问: https://github.com/jamiesun/hyperliquid-mcp
        """,
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="start",
        choices=["start", "stdio"],
        help="服务器模式: start (HTTP) 或 stdio (MCP 客户端)",
    )

    parser.add_argument("--version", action="version", version="HyperLiquid MCP v0.1.3")

    args = parser.parse_args()

    # 根据模式执行
    if args.mode == "stdio":
        print("🚀 启动 HyperLiquid MCP 服务器（stdio 模式）...")
        stdio_server()
    else:
        print("🚀 启动 HyperLiquid MCP 服务器（HTTP 模式）...")
        start_server()


if __name__ == "__main__":
    main()
