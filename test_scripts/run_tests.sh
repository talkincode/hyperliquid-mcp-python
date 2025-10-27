#!/bin/bash

# HyperLiquid MCP 测试套件
# 运行所有只读测试

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         HyperLiquid MCP 只读测试套件                               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查是否在项目根目录
cd "$PROJECT_DIR"

# 函数：运行测试并显示结果
run_test() {
    local test_name=$1
    local test_file=$2
    
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}▶ 运行测试: ${test_name}${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if uv run python "$test_file"; then
        echo ""
        echo -e "${GREEN}✅ ${test_name} - 通过${NC}"
    else
        echo ""
        echo -e "${RED}❌ ${test_name} - 失败${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 函数：显示菜单
show_menu() {
    echo -e "${BLUE}请选择要运行的测试:${NC}"
    echo ""
    echo "  1. 基础连接测试"
    echo "  2. 账户信息测试"
    echo "  3. 账户余额检查（现货 + 合约）"
    echo "  4. 市场数据测试"
    echo "  5. 订单簿测试"
    echo "  6. 资金费率历史测试"
    echo "  7. 价格计算器测试"
    echo ""
    echo "  9. 运行所有只读测试（推荐）"
    echo "  0. 退出"
    echo ""
}

# 主测试函数
run_all_readonly_tests() {
    local failed=0
    
    run_test "基础连接测试" "test_scripts/test_connection.py" || ((failed++))
    run_test "账户信息测试" "test_scripts/test_account_info.py" || ((failed++))
    run_test "账户余额检查" "test_scripts/check_all_balances.py" || ((failed++))
    run_test "市场数据测试" "test_scripts/test_market_data.py" || ((failed++))
    run_test "订单簿测试" "test_scripts/test_orderbook.py" || ((failed++))
    run_test "资金费率历史测试" "test_scripts/test_funding_history.py" || ((failed++))
    run_test "价格计算器测试" "test_scripts/test_price_calculator.py" || ((failed++))
    
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                        测试总结                                    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✅ 所有测试通过！${NC}"
    else
        echo -e "${RED}❌ $failed 个测试失败${NC}"
    fi
    
    echo ""
}

# 如果提供了命令行参数，直接运行对应测试
if [ $# -gt 0 ]; then
    case $1 in
        1|connection)
            run_test "基础连接测试" "test_scripts/test_connection.py"
            ;;
        2|account)
            run_test "账户信息测试" "test_scripts/test_account_info.py"
            ;;
        3|balance)
            run_test "账户余额检查" "test_scripts/check_all_balances.py"
            ;;
        4|market)
            run_test "市场数据测试" "test_scripts/test_market_data.py"
            ;;
        5|orderbook)
            run_test "订单簿测试" "test_scripts/test_orderbook.py"
            ;;
        6|funding)
            run_test "资金费率历史测试" "test_scripts/test_funding_history.py"
            ;;
        7|calculator)
            run_test "价格计算器测试" "test_scripts/test_price_calculator.py"
            ;;
        9|all)
            run_all_readonly_tests
            ;;
        *)
            echo -e "${RED}错误: 无效的选项 '$1'${NC}"
            echo ""
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  1|connection   - 基础连接测试"
            echo "  2|account      - 账户信息测试"
            echo "  3|balance      - 账户余额检查"
            echo "  4|market       - 市场数据测试"
            echo "  5|orderbook    - 订单簿测试"
            echo "  6|funding      - 资金费率历史测试"
            echo "  7|calculator   - 价格计算器测试"
            echo "  9|all          - 运行所有只读测试"
            echo ""
            exit 1
            ;;
    esac
    exit 0
fi

# 交互式菜单
while true; do
    show_menu
    read -p "请输入选项 (0-9): " choice
    
    case $choice in
        1)
            run_test "基础连接测试" "test_scripts/test_connection.py"
            ;;
        2)
            run_test "账户信息测试" "test_scripts/test_account_info.py"
            ;;
        3)
            run_test "账户余额检查" "test_scripts/check_all_balances.py"
            ;;
        4)
            run_test "市场数据测试" "test_scripts/test_market_data.py"
            ;;
        5)
            run_test "订单簿测试" "test_scripts/test_orderbook.py"
            ;;
        6)
            run_test "资金费率历史测试" "test_scripts/test_funding_history.py"
            ;;
        7)
            run_test "价格计算器测试" "test_scripts/test_price_calculator.py"
            ;;
        9)
            run_all_readonly_tests
            ;;
        0)
            echo ""
            echo -e "${GREEN}再见！${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED}无效的选项，请输入 0-7 或 9${NC}"
            echo ""
            ;;
    esac
    
    # 等待用户按键继续
    echo ""
    read -p "按 Enter 继续..." 
    clear
done
