#!/bin/bash

# 文档网站快速设置脚本

set -e

echo "📚 HyperLiquid MCP - 文档网站设置"
echo "=================================="
echo ""

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "请先安装 Python 3.10 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"
echo ""

# 安装文档依赖
echo "📦 安装文档依赖..."
pip install -r docs-requirements.txt

echo ""
echo "✅ 文档依赖安装完成！"
echo ""
echo "下一步："
echo ""
echo "1. 本地预览文档："
echo "   make docs-serve"
echo "   或: mkdocs serve"
echo ""
echo "2. 构建文档："
echo "   make docs-build"
echo "   或: mkdocs build"
echo ""
echo "3. 部署到 GitHub Pages："
echo "   make docs-deploy"
echo "   或: mkdocs gh-deploy --force"
echo ""
echo "📖 访问 http://127.0.0.1:8000 查看文档"
