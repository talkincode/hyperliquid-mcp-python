# GitHub 工作流配置

本项目已启用以下 GitHub Actions 工作流:

## 📋 工作流列表

### 1. CI 工作流 (`.github/workflows/ci.yml`)

**触发条件:**

- Push 到 `main` 或 `develop` 分支
- Pull Request 到 `main` 或 `develop` 分支

**功能:**

- **多版本测试**: 在 Python 3.10, 3.11, 3.12, 3.13 上运行测试
- **代码质量检查**: 使用 Black 和 isort 检查代码格式
- **包构建**: 验证包可以成功构建
- **测试覆盖**: 运行单元测试和验证测试

**任务:**

1. `test` - 运行所有单元测试
2. `lint` - 代码格式和导入检查
3. `build` - 构建发布包

### 2. 发布工作流 (`.github/workflows/publish.yml`)

**触发条件:**

- 创建新的 GitHub Release
- 手动触发 (workflow_dispatch)

**功能:**

- 自动构建包
- 发布到 PyPI

**配置要求:**
需要在 GitHub 仓库设置中添加以下 Secret:

- `PYPI_API_TOKEN`: PyPI API token

### 3. Dependabot (`.github/dependabot.yml`)

**功能:**

- 每周自动检查 GitHub Actions 更新
- 每周自动检查 Python 依赖更新
- 自动创建 PR 以更新依赖

## 🔒 分支保护

为确保代码质量,强烈建议启用分支保护。详细配置指南请查看 `.github/BRANCH_PROTECTION.md`。

**快速配置:**

```bash
# 使用提供的脚本一键配置
./scripts/setup-branch-protection.sh

# 或手动配置
# 访问: https://github.com/talkincode/hyperliquid-mcp-python/settings/branches
```

**推荐的保护规则:**

- ✅ 合并前需要 PR
- ✅ 需要 1 人审查批准
- ✅ 必需通过所有 CI 检查
- ✅ 合并前需要解决所有对话
- ✅ 管理员也需遵守规则

## 🎯 状态徽章

在 README.md 中已添加以下徽章:

- CI 工作流状态
- PyPI 版本
- Python 版本支持
- 许可证

## 📝 模板

### Pull Request 模板

位于 `.github/pull_request_template.md`

提供了标准化的 PR 描述格式,包括:

- 变更描述
- 变更类型
- 测试说明
- 检查清单

### Issue 模板

位于 `.github/ISSUE_TEMPLATE/`

提供了两种模板:

1. **Bug 报告** (`bug_report.md`): 标准化的 bug 报告格式
2. **功能请求** (`feature_request.md`): 新功能建议格式

## 🚀 使用指南

### 本地开发

1. Fork 并克隆仓库
2. 安装依赖: `uv sync --all-extras --dev`
3. 创建功能分支: `git checkout -b feature/your-feature`
4. 运行测试: `uv run pytest`
5. 格式化代码: `uv run black . && uv run isort .`
6. 提交并推送
7. 创建 Pull Request

### 发布新版本

1. 更新 `pyproject.toml` 中的版本号
2. 提交变更: `git commit -am "chore: bump version to x.x.x"`
3. 创建标签: `git tag vx.x.x`
4. 推送标签: `git push origin vx.x.x`
5. 在 GitHub 上创建 Release
6. 发布工作流将自动运行并发布到 PyPI

### 配置 PyPI Token

1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token
3. 在 GitHub 仓库设置中:
   - Settings → Secrets and variables → Actions
   - 添加新 Secret: `PYPI_API_TOKEN`

## ⚙️ 工作流优化

当前配置是精简模式,包含核心功能:

- ✅ 自动化测试
- ✅ 代码质量检查
- ✅ 自动发布
- ✅ 依赖更新

### 可选增强

如需要,可添加:

- 代码覆盖率报告 (Codecov)
- 安全扫描 (Snyk, Dependabot Security)
- 自动化 Changelog 生成
- Docker 镜像构建

## 📚 参考资源

- [GitHub Actions 文档](https://docs.github.com/actions)
- [PyPI 发布指南](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Dependabot 文档](https://docs.github.com/code-security/dependabot)
