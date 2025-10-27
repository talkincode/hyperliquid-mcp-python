# 代码质量和自动格式化指南

本项目使用多种工具来保证代码质量和一致性。

## 🎯 快速开始

### 1. 安装 Pre-commit Hooks (推荐)

这是**最简单的方式**,可以在每次 `git commit` 时自动格式化代码:

```bash
# 安装 hooks
make pre-commit-install

# 或直接使用
uv run pre-commit install
```

**安装后,每次提交时会自动:**

- ✅ 格式化代码 (black)
- ✅ 排序 imports (isort)
- ✅ 删除行尾空格
- ✅ 检查 YAML/TOML 语法
- ✅ 运行 ruff linter

### 2. 手动格式化代码

```bash
# 格式化所有代码
make format

# 或单独运行
uv run black .
uv run isort .
```

### 3. 检查代码(不修改)

```bash
# 检查格式但不修改
make check

# 或
uv run black --check .
uv run isort --check-only .
```

## 🔧 工具说明

### Black - 代码格式化器

配置在 `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py310', 'py311', 'py312', 'py313']
```

使用:

```bash
# 格式化所有文件
uv run black .

# 检查但不修改
uv run black --check .

# 格式化特定文件
uv run black services/hyperliquid_services.py
```

### isort - Import 排序

配置在 `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
line_length = 88
```

使用:

```bash
# 排序所有文件
uv run isort .

# 检查但不修改
uv run isort --check-only .
```

### Ruff - 快速 Linter

配置在 `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
```

使用:

```bash
# 运行 linter
uv run ruff check .

# 自动修复
uv run ruff check . --fix
```

### Pre-commit - Git Hooks

配置在 `.pre-commit-config.yaml`

使用:

```bash
# 安装 hooks
uv run pre-commit install

# 手动运行所有文件
uv run pre-commit run --all-files

# 更新 hooks 到最新版本
uv run pre-commit autoupdate

# 跳过 hooks 提交(不推荐)
git commit --no-verify -m "message"
```

## 🤖 自动化流程

### GitHub Actions - 自动格式化

PR 提交后,会自动运行 `.github/workflows/auto-format.yml`:

1. 自动格式化代码
2. 如果有变更,自动提交并推送
3. 在 PR 中添加评论通知

### GitHub Actions - CI 检查

PR 必须通过 `.github/workflows/ci.yml` 的所有检查:

- ✅ `test (3.10)` - Python 3.10 测试
- ✅ `test (3.11)` - Python 3.11 测试
- ✅ `test (3.12)` - Python 3.12 测试
- ✅ `test (3.13)` - Python 3.13 测试
- ✅ `lint` - 代码质量检查
- ✅ `build` - 包构建

## 📋 开发工作流

### 推荐流程

```bash
# 1. 安装 pre-commit (只需一次)
make pre-commit-install

# 2. 开发代码
# ... 编写代码 ...

# 3. 提交代码 (会自动格式化)
git add .
git commit -m "feat: add new feature"

# 4. 如果 pre-commit 修改了文件
git add .
git commit -m "feat: add new feature"

# 5. 推送到 GitHub
git push origin feature-branch

# 6. 创建 PR - CI 会自动检查
```

### 手动流程(如果不使用 pre-commit)

```bash
# 1. 开发代码
# ... 编写代码 ...

# 2. 格式化代码
make format

# 3. 检查是否通过
make check

# 4. 提交
git add .
git commit -m "feat: add new feature"
git push
```

## 🚨 常见问题

### Q: Pre-commit 失败怎么办?

A: Pre-commit 失败后会自动修复文件,只需重新添加并提交:

```bash
# 1. pre-commit 运行并修复文件
git add .

# 2. 再次提交
git commit -m "your message"
```

### Q: 如何跳过 pre-commit 检查?

A: 不推荐,但紧急情况下可以:

```bash
git commit --no-verify -m "emergency fix"
```

### Q: CI 失败说代码格式不对?

A: 运行格式化并重新提交:

```bash
make format
git add .
git commit -m "style: format code"
git push
```

### Q: 如何在 VS Code 中自动格式化?

A: 安装扩展并配置:

1. 安装扩展:

   - Black Formatter
   - isort

2. 在 `.vscode/settings.json` 中:

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### Q: 如何更新 pre-commit hooks?

A: 定期运行:

```bash
make pre-commit-update
```

## 📚 相关资源

- [Black 文档](https://black.readthedocs.io/)
- [isort 文档](https://pycqa.github.io/isort/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [Pre-commit 文档](https://pre-commit.com/)

## 🎯 最佳实践

1. ✅ **始终使用 pre-commit** - 最简单的方式
2. ✅ **提交前检查** - `make check`
3. ✅ **保持工具更新** - `make pre-commit-update`
4. ✅ **不要跳过检查** - 除非紧急情况
5. ✅ **配置 IDE** - 保存时自动格式化

---

**快速命令参考:**

```bash
make pre-commit-install  # 安装 pre-commit hooks
make format              # 格式化代码
make check               # 检查代码
make pre-commit-all      # 运行所有 pre-commit 检查
```
