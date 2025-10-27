# 分支保护配置指南

## 为什么需要分支保护?

分支保护可以:

- ✅ 防止直接推送到主分支
- ✅ 确保所有更改都经过 PR 审查
- ✅ 强制 CI 测试必须通过
- ✅ 要求代码审查
- ✅ 保持代码质量和稳定性

## 推荐的分支保护规则

### 🔒 Main 分支保护 (强烈推荐)

#### 基础保护

1. **Require a pull request before merging** (合并前需要 PR)

   - ✅ 启用此选项
   - Require approvals: 1 (至少 1 人审查)
   - ✅ Dismiss stale pull request approvals when new commits are pushed (新提交时清除旧审查)
   - ✅ Require review from Code Owners (如果有 CODEOWNERS 文件)

2. **Require status checks to pass before merging** (合并前需要状态检查通过)

   - ✅ 启用此选项
   - ✅ Require branches to be up to date before merging (合并前需要更新分支)
   - 必需的状态检查:
     - `test (3.10)` - Python 3.10 测试
     - `test (3.11)` - Python 3.11 测试
     - `test (3.12)` - Python 3.12 测试
     - `test (3.13)` - Python 3.13 测试
     - `lint` - 代码质量检查
     - `build` - 包构建

3. **Require conversation resolution before merging** (合并前需要解决所有对话)

   - ✅ 启用此选项

4. **Require signed commits** (需要签名提交)

   - ⚠️ 可选 - 如果团队使用 GPG 签名

5. **Require linear history** (需要线性历史)

   - ⚠️ 可选 - 防止合并提交,保持历史清晰

6. **Do not allow bypassing the above settings** (不允许绕过以上设置)
   - ✅ 启用此选项 (管理员也需遵守规则)

#### 其他规则

- ✅ **Restrict who can push to matching branches** - 限制谁可以推送
  - 只允许维护者推送
- ✅ **Allow force pushes** - 关闭 (防止强制推送)
- ✅ **Allow deletions** - 关闭 (防止删除主分支)

## 📋 配置步骤

### 方式 1: 通过 GitHub 网页配置 (推荐)

1. 访问仓库设置

   ```
   https://github.com/talkincode/hyperliquid-mcp-python/settings/branches
   ```

2. 点击 "Add branch protection rule"

3. 在 "Branch name pattern" 中输入: `main`

4. 启用以下选项:

   - ✅ Require a pull request before merging

     - Required number of approvals: 1
     - ✅ Dismiss stale pull request approvals when new commits are pushed

   - ✅ Require status checks to pass before merging

     - ✅ Require branches to be up to date before merging
     - 添加必需的检查:
       - `test (3.10)`
       - `test (3.11)`
       - `test (3.12)`
       - `test (3.13)`
       - `lint`
       - `build`

   - ✅ Require conversation resolution before merging

   - ✅ Do not allow bypassing the above settings

5. 点击 "Create" 保存

### 方式 2: 通过 GitHub CLI 配置

```bash
# 安装 GitHub CLI (如果未安装)
brew install gh

# 登录
gh auth login

# 创建分支保护规则
gh api repos/talkincode/hyperliquid-mcp-python/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test (3.10)","test (3.11)","test (3.12)","test (3.13)","lint","build"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1}' \
  --field restrictions=null
```

### 方式 3: 使用 Terraform (Infrastructure as Code)

创建 `terraform/github.tf`:

```hcl
resource "github_branch_protection" "main" {
  repository_id = "hyperliquid-mcp-python"
  pattern       = "main"

  required_status_checks {
    strict   = true
    contexts = [
      "test (3.10)",
      "test (3.11)",
      "test (3.12)",
      "test (3.13)",
      "lint",
      "build"
    ]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 1
  }

  enforce_admins                  = true
  require_conversation_resolution = true
  require_signed_commits          = false
  allow_force_pushes              = false
  allow_deletions                 = false
}
```

## 🎯 不同场景的推荐配置

### 个人项目 (轻量级)

```
- ✅ Require status checks (CI must pass)
- ⚠️ Require PR (可选,个人项目可以直接推送)
- ⚠️ Require reviews (可选,个人项目不需要)
```

### 小团队项目 (2-5 人)

```
- ✅ Require status checks (CI must pass)
- ✅ Require pull request before merging
- ✅ Require 1 approval
- ✅ Require conversation resolution
```

### 开源项目 (推荐配置)

```
- ✅ Require status checks (CI must pass)
- ✅ Require pull request before merging
- ✅ Require 1-2 approvals
- ✅ Require conversation resolution
- ✅ Require Code Owner reviews
- ⚠️ Allow force pushes for maintainers only
```

### 企业项目 (严格)

```
- ✅ Require status checks (CI must pass)
- ✅ Require pull request before merging
- ✅ Require 2+ approvals
- ✅ Require conversation resolution
- ✅ Require Code Owner reviews
- ✅ Require signed commits
- ✅ Require linear history
- ✅ Enforce for administrators
```

## 📝 CODEOWNERS 文件 (可选)

创建 `.github/CODEOWNERS` 文件来指定代码所有者:

```
# 默认所有者
* @talkincode

# 核心服务代码
/services/ @talkincode

# 工作流配置
/.github/workflows/ @talkincode

# 文档
*.md @talkincode
```

## 🚨 常见问题

### Q: 如果我是唯一的维护者,还需要分支保护吗?

A: 是的!至少启用 "Require status checks",确保 CI 通过才能合并。这可以防止意外破坏主分支。

### Q: 分支保护后如何提交代码?

A: 通过创建 PR:

```bash
# 1. 创建功能分支
git checkout -b feature/my-feature

# 2. 进行修改并提交
git add .
git commit -m "feat: add new feature"

# 3. 推送分支
git push origin feature/my-feature

# 4. 在 GitHub 创建 PR
# 5. 等待 CI 通过并合并
```

### Q: 紧急修复怎么办?

A: 即使是紧急修复,也应该:

1. 创建 hotfix 分支
2. 快速修复并测试
3. 创建 PR (可以自己审查)
4. 等待 CI 通过
5. 合并

### Q: 可以临时禁用分支保护吗?

A: 不推荐,但管理员可以在设置中临时关闭 "Enforce for administrators"。

## ✅ 验证配置

配置完成后,测试:

```bash
# 尝试直接推送到 main (应该失败)
git checkout main
git commit --allow-empty -m "test"
git push origin main
# 预期: remote: error: GH006: Protected branch update failed

# 正确方式:通过 PR
git checkout -b test-branch-protection
git commit --allow-empty -m "test branch protection"
git push origin test-branch-protection
# 然后在 GitHub 创建 PR
```

## 📊 推荐的分支策略

### Git Flow (推荐用于发布周期的项目)

```
main          - 生产环境,受保护
develop       - 开发分支,受保护
feature/*     - 功能分支
hotfix/*      - 紧急修复分支
release/*     - 发布分支
```

### GitHub Flow (推荐用于持续部署)

```
main          - 生产环境,受保护
feature/*     - 功能分支
fix/*         - 修复分支
```

### Trunk-Based (推荐用于小团队)

```
main          - 主分支,受保护
feature/*     - 短期功能分支 (< 2 天)
```

## 🎉 最佳实践

1. **始终通过 PR 合并** - 即使是小改动
2. **保持 PR 小而专注** - 更容易审查
3. **及时审查 PR** - 不要让 PR 积压
4. **使用自动化** - 让 CI 做繁重的工作
5. **编写清晰的 PR 描述** - 使用提供的模板
6. **要求 CI 通过** - 这是最低要求
7. **定期更新保护规则** - 随着项目发展调整

## 📚 相关资源

- [GitHub 分支保护文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Git Flow 工作流](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)

---

**快速开始**: 访问 https://github.com/talkincode/hyperliquid-mcp-python/settings/branches 立即配置! 🔒
