# 🚀 自动代码格式化 - 快速设置指南

## 一次性设置 (推荐)

```bash
# 1. 安装 pre-commit hooks
make pre-commit-install

# 完成! 现在每次 git commit 都会自动格式化代码
```

## 它做了什么?

安装后,**每次 `git commit` 时会自动:**

✅ 使用 black 格式化 Python 代码  
✅ 使用 isort 排序 imports  
✅ 删除行尾空格  
✅ 修复文件结尾换行  
✅ 检查 YAML/TOML 语法  
✅ 运行 ruff linter

## 提交流程示例

```bash
# 1. 修改代码
vim main.py

# 2. 正常提交 (pre-commit 会自动运行)
git add main.py
git commit -m "feat: add new feature"

# 如果 pre-commit 修复了格式,你会看到:
# black....................................Failed
# - hook id: black
# - files were modified by this hook
#
# 只需重新添加并提交:
git add main.py
git commit -m "feat: add new feature"

# 3. 推送
git push
```

## GitHub Actions 自动格式化

PR 提交后,如果代码格式不对:

1. **自动格式化 workflow** 会运行
2. 自动修复并提交到你的 PR 分支
3. 在 PR 中添加评论: "✨ Code has been automatically formatted"

**你不需要做任何事!** 机器人会自动修复。

## 手动格式化 (可选)

如果你想手动格式化:

```bash
# 格式化所有文件
make format

# 检查格式 (不修改)
make check

# 运行所有 pre-commit 检查
make pre-commit-all
```

## VS Code 集成 (可选)

在 VS Code 中保存时自动格式化:

1. 安装扩展:

   - **Black Formatter** (ms-python.black-formatter)
   - **isort** (ms-python.isort)

2. 在项目中创建 `.vscode/settings.json`:

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

## 常见问题

### Q: 如何跳过 pre-commit?

不推荐,但紧急时可以:

```bash
git commit --no-verify -m "emergency fix"
```

### Q: Pre-commit 太慢怎么办?

只检查修改的文件:

```bash
# pre-commit 默认只检查 staged 的文件
# 如果想检查所有文件:
uv run pre-commit run --all-files
```

### Q: 如何更新 hooks?

```bash
make pre-commit-update
```

## 更多信息

- 📖 完整文档: `.github/CODE_QUALITY.md`
- 🔧 配置文件: `.pre-commit-config.yaml`
- ⚙️ 工具配置: `pyproject.toml`

---

**记住: 只需运行一次 `make pre-commit-install`,之后一切自动化!** ✨
