# GitHub 工作流启用检查清单

## ✅ 已完成的配置

### 核心工作流

- [x] **CI 工作流** (`.github/workflows/ci.yml`)

  - 多版本 Python 测试 (3.10-3.13)
  - 单元测试执行
  - Black/isort 代码质量检查
  - 包构建验证

- [x] **发布工作流** (`.github/workflows/publish.yml`)

  - 自动发布到 PyPI
  - 基于 GitHub Release 触发
  - 支持手动触发

- [x] **Dependabot** (`.github/dependabot.yml`)
  - 自动检查 GitHub Actions 更新
  - 自动检查 Python 依赖更新

### 协作模板

- [x] **Pull Request 模板** (`.github/pull_request_template.md`)
- [x] **Bug 报告模板** (`.github/ISSUE_TEMPLATE/bug_report.md`)
- [x] **功能请求模板** (`.github/ISSUE_TEMPLATE/feature_request.md`)

### 文档

- [x] **贡献指南** (`CONTRIBUTING.md`)
- [x] **工作流文档** (`.github/WORKFLOWS.md`)
- [x] **设置总结** (`.github/SETUP_SUMMARY.md`)
- [x] **README 徽章** (已添加 4 个状态徽章)
- [x] **Markdown Lint 配置** (`.markdownlint.json`)

## 🔧 需要手动配置的项目

### 1. PyPI Token 配置 (发布到 PyPI 需要)

**选项 A: API Token (简单)**

1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token (选择 "Entire account" 或特定项目)
3. 复制 token
4. 在 GitHub 仓库:
   - Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: 粘贴你的 token
   - 点击 "Add secret"

**选项 B: Trusted Publishing (推荐,更安全)**

1. 在 PyPI 上进入项目设置
2. 找到 "Publishing" 部分
3. 添加 GitHub Actions 为 Trusted Publisher:
   - Owner: `talkincode`
   - Repository: `hyperliquid-mcp-python`
   - Workflow: `publish.yml`
   - Environment: 留空
4. 修改 `.github/workflows/publish.yml`:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     # 不需要 password,使用 OIDC
   ```

### 2. 测试工作流

**首次运行 CI:**

```bash
# 提交所有变更
git add .
git commit -m "feat: enable GitHub workflows with CI/CD"
git push origin main

# 查看工作流运行状态
open https://github.com/talkincode/hyperliquid-mcp-python/actions
```

**预期结果:**

- CI 工作流应该自动触发
- 所有测试应该通过 ✅
- 代码质量检查应该通过 ✅
- 包构建应该成功 ✅

### 3. 配置分支保护 (强烈推荐) 🔒

**为什么需要?**

- 防止直接推送到主分支
- 确保 CI 测试通过才能合并
- 保持代码质量和稳定性

**快速配置:**

1. 访问 https://github.com/talkincode/hyperliquid-mcp-python/settings/branches
2. 点击 "Add branch protection rule"
3. Branch name pattern: `main`
4. 启用以下选项:
   - ✅ Require a pull request before merging
     - Required approvals: 1
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date
     - 添加必需检查: `test (3.10)`, `test (3.11)`, `test (3.12)`, `test (3.13)`, `lint`, `build`
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings
5. 点击 "Create"

**详细指南:** 查看 `.github/BRANCH_PROTECTION.md`

### 4. 测试发布流程 (可选)

**创建测试 Release:**

```bash
# 1. 更新版本号 (如果需要)
# 编辑 pyproject.toml: version = "0.1.5"

# 2. 提交变更
git add pyproject.toml
git commit -m "chore: bump version to 0.1.5"

# 3. 创建并推送标签
git tag v0.1.5
git push origin v0.1.5

# 4. 在 GitHub 创建 Release
# 访问: https://github.com/talkincode/hyperliquid-mcp-python/releases/new
# - Tag: v0.1.5
# - Release title: v0.1.5
# - Description: 简要说明本次发布的内容
# - 点击 "Publish release"
```

**预期结果:**

- 发布工作流应该自动触发
- 包应该构建成功
- 包应该发布到 PyPI ✅

## 📊 验证步骤

### 1. 检查 CI 状态

```bash
# 在终端中查看最近的工作流运行
gh run list --limit 5

# 或访问网页
open https://github.com/talkincode/hyperliquid-mcp-python/actions
```

### 2. 验证徽章显示

- 查看 README.md
- CI 徽章应显示为绿色 (passing)
- PyPI 版本徽章应显示最新版本

### 3. 测试 Dependabot

- 等待 Dependabot 创建第一个更新 PR (通常在启用后 1-7 天内)
- 检查 PR 的格式和标签是否正确

## 🚨 常见问题

### CI 失败?

1. 检查测试是否在本地通过: `uv run pytest`
2. 检查代码格式: `uv run black --check .`
3. 检查导入排序: `uv run isort --check-only .`

### 发布失败?

1. 确认已配置 `PYPI_API_TOKEN`
2. 确认 token 有效且有发布权限
3. 检查版本号是否已存在于 PyPI

### Dependabot 没有创建 PR?

1. 检查 `.github/dependabot.yml` 配置
2. 可能需要等待一周 (schedule: weekly)
3. 在仓库的 Insights → Dependency graph → Dependabot 查看状态

## 🎯 后续优化建议

1. **代码覆盖率**: 添加 Codecov 集成
2. **性能测试**: 添加基准测试工作流
3. **安全扫描**: 启用 CodeQL
4. **预提交钩子**: 配置 pre-commit
5. **文档部署**: 自动部署文档到 GitHub Pages

## 📞 获取帮助

如遇问题:

1. 查看 `.github/WORKFLOWS.md` 详细文档
2. 查看 GitHub Actions 日志
3. 参考 [GitHub Actions 文档](https://docs.github.com/actions)
4. 在项目中创建 Issue

---

**快速开始**: 只需配置 PyPI Token 并 push 代码,其他都已自动配置好! 🚀
