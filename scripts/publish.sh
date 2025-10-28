#!/bin/bash
# 快速发布脚本 - 发布到 PyPI

set -e  # 遇到错误立即退出

echo "🚀 HyperLiquid MCP - PyPI 发布脚本"
echo "=================================="
echo ""

# 检查是否安装了必要工具
if ! command -v twine &> /dev/null; then
    echo "❌ twine 未安装，正在安装..."
    uv pip install twine build
fi

# 1. 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info 2>/dev/null || true

# 2. 构建包
echo "📦 构建分发包..."
uv run python -m build

# 3. 检查构建产物
echo "✅ 检查包的完整性..."
uv run twine check dist/*

echo ""
echo "构建完成！以下是构建的文件："
ls -lh dist/

echo ""
echo "请选择发布目标："
echo "1) 测试 PyPI (test.pypi.org) - 推荐先测试"
echo "2) 正式 PyPI (pypi.org)"
echo "3) 取消"
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "📤 上传到测试 PyPI..."
        echo "用户名: __token__"
        echo "密码: 粘贴你的测试 PyPI token"
        uv run twine upload --repository testpypi dist/*
        echo ""
        echo "✅ 上传成功！"
        echo "测试安装命令："
        echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperliquid-mcp-python"
        ;;
    2)
        echo ""
        echo "📤 上传到正式 PyPI..."
        echo "用户名: __token__"
        echo "密码: 粘贴你的正式 PyPI token"
        uv run twine upload dist/*
        echo ""
        echo "✅ 上传成功！"
        echo "安装命令："
        echo "  pip install hyperliquid-mcp-python"
        echo "  uv pip install hyperliquid-mcp-python"
        ;;
    3)
        echo "❌ 取消发布"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "🎉 完成！"
