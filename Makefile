.PHONY: help install dev clean build publish test run-http run-stdio lint format check

# 默认目标
help:
	@echo "HyperLiquid MCP - 可用命令:"
	@echo ""
	@echo "开发命令:"
	@echo "  make install     - 安装依赖（uv sync）"
	@echo "  make dev         - 开发模式安装"
	@echo "  make run-http    - 启动 HTTP 服务器"
	@echo "  make run-stdio   - 启动 stdio 服务器"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint        - 运行代码检查"
	@echo "  make format      - 格式化代码"
	@echo "  make check       - 检查代码但不修改"
	@echo "  make test        - 运行测试"
	@echo ""
	@echo "构建和发布:"
	@echo "  make clean       - 清理构建文件"
	@echo "  make build       - 构建发布包"
	@echo "  make publish     - 发布到 PyPI"
	@echo "  make test-pypi   - 发布到测试 PyPI"
	@echo ""
	@echo "快捷命令:"
	@echo "  make all         - clean + build"
	@echo "  make release     - clean + build + publish"

# 安装依赖
install:
	uv sync

# 开发模式
dev:
	uv sync --all-extras

# 运行 HTTP 服务器
run-http:
	uv run hyperliquid-mcp start

# 运行 stdio 服务器
run-stdio:
	uv run hyperliquid-mcp stdio

# 代码格式化
format:
	uv run black .
	uv run isort .

# 代码检查（不修改）
check:
	uv run black --check .
	uv run isort --check-only .

# 代码检查（带 lint）
lint: check
	@echo "✅ 代码检查通过"

# 运行测试
test:
	@echo "⚠️  暂无测试，跳过"
	@# uv run pytest

# 清理构建文件
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ 清理完成"

# 构建发布包
build: clean
	uv run python -m build
	uv run twine check dist/*
	@echo "✅ 构建完成"
	@ls -lh dist/

# 发布到测试 PyPI
test-pypi: build
	uv run twine upload --repository testpypi dist/*
	@echo "✅ 已发布到测试 PyPI"
	@echo "查看: https://test.pypi.org/project/hyperliquid-mcp-python/"

# 发布到正式 PyPI
publish: build
	@echo "⚠️  即将发布到正式 PyPI，请确认："
	@echo "   1. 版本号已更新"
	@echo "   2. CHANGELOG 已更新"
	@echo "   3. 代码已提交到 git"
	@read -p "继续？(y/N) " confirm && [ "$$confirm" = "y" ] || (echo "已取消" && exit 1)
	uv run twine upload dist/*
	@echo "✅ 已发布到 PyPI"
	@echo "查看: https://pypi.org/project/hyperliquid-mcp-python/"

# 快捷命令：清理 + 构建
all: clean build

# 快捷命令：完整发布流程
release: clean build publish

# 检查 uv 是否安装
check-uv:
	@which uv > /dev/null || (echo "❌ uv 未安装，请访问: https://github.com/astral-sh/uv" && exit 1)

# 显示版本信息
version:
	@grep '^version = ' pyproject.toml | cut -d'"' -f2

# 缓存清理
cache-clean:
	uv cache clean
	@echo "✅ UV 缓存已清理"

# 测试 uvx 安装
test-uvx:
	@echo "测试 uvx 安装..."
	uvx --python 3.13 --from hyperliquid-mcp-python hyperliquid-mcp --version

# 本地测试安装
test-install: build
	@echo "创建测试虚拟环境..."
	python3 -m venv /tmp/test-hyperliquid-mcp
	/tmp/test-hyperliquid-mcp/bin/pip install dist/*.whl
	/tmp/test-hyperliquid-mcp/bin/hyperliquid-mcp --version
	rm -rf /tmp/test-hyperliquid-mcp
	@echo "✅ 本地安装测试通过"

# Git 标签和推送
tag:
	@VERSION=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2) && \
	git tag -a "v$$VERSION" -m "Release v$$VERSION" && \
	echo "✅ 已创建标签: v$$VERSION" && \
	echo "推送标签: git push origin v$$VERSION"

# 完整发布流程（包含 git）
full-release: check-uv
	@echo "🚀 开始完整发布流程..."
	@$(MAKE) clean
	@$(MAKE) build
	@$(MAKE) test-install
	@VERSION=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2) && \
	echo "" && \
	echo "准备发布 v$$VERSION" && \
	echo "请确认所有更改已提交到 git" && \
	read -p "继续？(y/N) " confirm && [ "$$confirm" = "y" ] || (echo "已取消" && exit 1)
	@$(MAKE) publish
	@$(MAKE) tag
	@echo ""
	@echo "🎉 发布完成！别忘了："
	@echo "   git push origin main"
	@echo "   git push origin v$$(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
