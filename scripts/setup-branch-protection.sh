#!/bin/bash

# 分支保护快速配置脚本
# 使用 GitHub CLI 配置分支保护规则

set -e

echo "🔒 HyperLiquid MCP - 分支保护配置脚本"
echo "========================================"
echo ""

# 检查 gh CLI 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) 未安装"
    echo ""
    echo "请先安装 GitHub CLI:"
    echo "  macOS:   brew install gh"
    echo "  Linux:   https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo "  Windows: https://github.com/cli/cli/releases"
    echo ""
    exit 1
fi

echo "✅ GitHub CLI 已安装"

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 未登录 GitHub"
    echo ""
    echo "请先登录:"
    echo "  gh auth login"
    echo ""
    exit 1
fi

echo "✅ 已登录 GitHub"
echo ""

# 仓库信息
OWNER="talkincode"
REPO="hyperliquid-mcp-python"
BRANCH="main"

echo "📋 配置信息:"
echo "  仓库: $OWNER/$REPO"
echo "  分支: $BRANCH"
echo ""

# 询问用户确认
read -p "是否继续配置分支保护? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 0
fi

echo ""
echo "🔧 正在配置分支保护..."

# 配置分支保护
# 注意: 这个 API 调用需要适当的权限
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  repos/$OWNER/$REPO/branches/$BRANCH/protection \
  --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      {"context": "test (3.10)"},
      {"context": "test (3.11)"},
      {"context": "test (3.12)"},
      {"context": "test (3.13)"},
      {"context": "lint"},
      {"context": "build"}
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 分支保护配置成功!"
    echo ""
    echo "📋 已启用的保护规则:"
    echo "  ✅ 合并前需要 PR"
    echo "  ✅ 需要 1 人审查批准"
    echo "  ✅ 新提交时清除旧审查"
    echo "  ✅ 必需通过 CI 检查:"
    echo "     - test (3.10)"
    echo "     - test (3.11)"
    echo "     - test (3.12)"
    echo "     - test (3.13)"
    echo "     - lint"
    echo "     - build"
    echo "  ✅ 合并前需要解决所有对话"
    echo "  ✅ 管理员也需遵守规则"
    echo "  ✅ 禁止强制推送"
    echo "  ✅ 禁止删除分支"
    echo ""
    echo "🎉 配置完成!"
    echo ""
    echo "📚 查看配置:"
    echo "  https://github.com/$OWNER/$REPO/settings/branches"
    echo ""
    echo "💡 下次提交代码时,请使用 PR 流程:"
    echo "  1. git checkout -b feature/your-feature"
    echo "  2. git commit -m 'feat: your changes'"
    echo "  3. git push origin feature/your-feature"
    echo "  4. 在 GitHub 创建 PR 并等待 CI 通过"
else
    echo ""
    echo "❌ 配置失败"
    echo ""
    echo "可能的原因:"
    echo "  1. 没有仓库管理员权限"
    echo "  2. GitHub token 权限不足"
    echo "  3. 网络连接问题"
    echo ""
    echo "请访问以下链接手动配置:"
    echo "  https://github.com/$OWNER/$REPO/settings/branches"
    echo ""
    echo "详细指南:"
    echo "  .github/BRANCH_PROTECTION.md"
    exit 1
fi
