# ============================================================================
# HyperLiquid MCP Makefile
# ============================================================================
#
# 快速开始:
#   make install        # 安装依赖
#   make config         # 查看配置
#   make test-quick     # 快速验证（连接+余额+地址）
#   make test-all       # 运行所有只读测试
#   make run-http       # 启动 HTTP 服务器
#
# 测试:
#   make test-market    # 市场数据测试
#   make test-account   # 账户信息测试
#   make test-balance   # 余额检查
#
# 帮助:
#   make help           # 显示所有可用命令
#   make test-help      # 显示测试快速参考
#   make list-tests     # 列出所有测试脚本
#
# ============================================================================

.PHONY: help install dev clean build publish test run-http run-stdio lint format check \
        test-connection test-account test-balance test-market test-orderbook \
        test-funding test-calculator test-all test-interactive config logs

# 默认目标
help:
	@echo "HyperLiquid MCP - 可用命令:"
	@echo ""
	@echo "开发命令:"
	@echo "  make install          - 安装依赖（uv sync）"
	@echo "  make dev              - 开发模式安装"
	@echo "  make run-http         - 启动 HTTP 服务器"
	@echo "  make run-stdio        - 启动 stdio 服务器"
	@echo ""
	@echo "测试命令:"
	@echo "  make test-all         - 运行所有只读测试 ⭐"
	@echo "  make test-connection  - 基础连接测试"
	@echo "  make test-account     - 账户信息测试"
	@echo "  make test-balance     - 账户余额检查"
	@echo "  make test-market      - 市场数据测试"
	@echo "  make test-orderbook   - 订单簿测试"
	@echo "  make test-funding     - 资金费率历史测试"
	@echo "  make test-calculator  - 价格计算器测试"
	@echo "  make test-interactive - 交互式测试工具"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint             - 运行代码检查"
	@echo "  make format           - 格式化代码"
	@echo "  make check            - 检查代码但不修改"
	@echo "  make test             - 运行单元测试"
	@echo ""
	@echo "构建和发布:"
	@echo "  make clean            - 清理构建文件"
	@echo "  make build            - 构建发布包"
	@echo "  make publish          - 发布到 PyPI"
	@echo "  make test-pypi        - 发布到测试 PyPI"
	@echo ""
	@echo "快捷命令:"
	@echo "  make all              - clean + build"
	@echo "  make release          - clean + build + publish"

# ============================================================================
# 运行服务器
# ============================================================================

# 安装依赖
install:
	uv sync

# 开发模式
dev:
	uv sync --all-extras

# 运行 HTTP 服务器
run-http:
	@echo "🚀 启动 HTTP 服务器 (http://127.0.0.1:8080)..."
	uv run hyperliquid-mcp start

# 运行 stdio 服务器
run-stdio:
	@echo "🚀 启动 stdio 服务器..."
	uv run hyperliquid-mcp stdio

# 查看日志
logs:
	@if [ -f hyperliquid_mcp.log ]; then \
		tail -f hyperliquid_mcp.log; \
	else \
		echo "⚠️  日志文件不存在"; \
	fi

# 查看配置
config:
	@echo "📋 当前配置:"
	@echo ""
	@if [ -f .env ]; then \
		echo "从 .env 文件:"; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		grep -v '^#' .env | grep -v '^$$' | sed 's/HYPERLIQUID_PRIVATE_KEY=.*/HYPERLIQUID_PRIVATE_KEY=***隐藏***/'; \
	else \
		echo "⚠️  .env 文件不存在"; \
	fi
	@echo ""
	@echo "提示: 复制 .env.example 到 .env 并填入你的配置"

# ============================================================================
# 代码质量
# ============================================================================

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

# ============================================================================
# 文档和帮助
# ============================================================================

# 显示测试脚本帮助
test-help:
	@cat test_scripts/QUICK_REFERENCE.md

# 显示完整 README
docs:
	@cat README.md

# 显示测试文档
test-docs:
	@cat test_scripts/README.md

# 列出所有可用的测试脚本
list-tests:
	@echo "📝 可用的测试脚本:"
	@echo ""
	@ls -1 test_scripts/*.py | xargs -I {} basename {} | sort | nl
	@echo ""
	@echo "运行: make test-<名称> 或 uv run python test_scripts/<脚本名>"

# ============================================================================
# 清理和构建
# ============================================================================

# ============================================================================
# 测试命令
# ============================================================================

# 运行单元测试
test:
	@echo "⚠️  暂无单元测试，跳过"
	@# uv run pytest

# 运行所有只读测试
test-all:
	@echo "🧪 运行所有只读测试..."
	@./test_scripts/run_tests.sh all

# 基础连接测试
test-connection:
	@echo "🔗 运行基础连接测试..."
	@uv run python test_scripts/test_connection.py

# 账户信息测试
test-account:
	@echo "👤 运行账户信息测试..."
	@uv run python test_scripts/test_account_info.py

# 账户余额检查
test-balance:
	@echo "💰 运行账户余额检查..."
	@uv run python test_scripts/check_all_balances.py

# 市场数据测试
test-market:
	@echo "📊 运行市场数据测试..."
	@uv run python test_scripts/test_market_data.py

# 订单簿测试
test-orderbook:
	@echo "📖 运行订单簿测试..."
	@uv run python test_scripts/test_orderbook.py

# 资金费率历史测试
test-funding:
	@echo "💵 运行资金费率历史测试..."
	@uv run python test_scripts/test_funding_history.py

# 价格计算器测试
test-calculator:
	@echo "🧮 运行价格计算器测试..."
	@uv run python test_scripts/test_price_calculator.py

# 交互式测试工具
test-interactive:
	@echo "🎮 启动交互式测试工具..."
	@uv run python test_scripts/interactive_test.py

# 快速验证（连接 + 余额）
test-quick:
	@echo "⚡ 快速验证..."
	@$(MAKE) test-connection
	@echo ""
	@$(MAKE) test-balance

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
