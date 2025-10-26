# PyPI 发布指南

本文档说明如何将 hyperliquid-mcp-python 发布到 PyPI。

## 前置要求

1. **注册 PyPI 账号**
   - 主站：https://pypi.org/account/register/
   - 测试站（建议先用这个）：https://test.pypi.org/account/register/

2. **生成 API Token**
   - 主站：https://pypi.org/manage/account/token/
   - 测试站：https://test.pypi.org/manage/account/token/
   - 选择 "Scope: Entire account" 或指定项目
   - 保存生成的 token（格式：`pypi-...`）

3. **安装发布工具**
   ```bash
   uv pip install build twine
   ```

## 发布步骤

### 步骤 1: 清理旧构建文件

```bash
# 删除之前的构建产物
rm -rf dist/ build/ *.egg-info
```

### 步骤 2: 构建分发包

```bash
# 使用 uv 构建
uv build

# 或使用 python -m build
python -m build
```

这会在 `dist/` 目录生成两个文件：
- `.tar.gz` (源码分发)
- `.whl` (wheel 分发)

### 步骤 3: 检查构建产物

```bash
# 检查包的完整性
twine check dist/*
```

### 步骤 4: 先发布到测试 PyPI（推荐）

```bash
# 使用 token 上传到测试服务器
twine upload --repository testpypi dist/*

# 会提示输入：
# Username: __token__
# Password: pypi-... (粘贴你的 token)
```

### 步骤 5: 从测试 PyPI 安装验证

```bash
# 从测试 PyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperliquid-mcp-python

# 测试安装的包
hyperliquid-mcp --help
```

### 步骤 6: 发布到正式 PyPI

如果测试没问题，发布到正式 PyPI：

```bash
twine upload dist/*

# 会提示输入：
# Username: __token__
# Password: pypi-... (粘贴你的正式 PyPI token)
```

### 步骤 7: 验证安装

```bash
# 从正式 PyPI 安装
pip install hyperliquid-mcp-python

# 或使用 uv
uv pip install hyperliquid-mcp-python
```

## 使用 ~/.pypirc 简化流程（可选）

创建 `~/.pypirc` 文件保存 token：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-你的正式token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-你的测试token
```

设置文件权限：
```bash
chmod 600 ~/.pypirc
```

有了这个配置后，上传时不需要输入密码：
```bash
# 测试服务器
twine upload -r testpypi dist/*

# 正式服务器
twine upload dist/*
```

## 发布新版本

1. 更新版本号（`pyproject.toml` 中的 `version`）
2. 更新 README 或 CHANGELOG
3. 提交并打 tag：
   ```bash
   git add -A
   git commit -m "chore: bump version to 0.1.1"
   git tag v0.1.1
   git push origin main --tags
   ```
4. 清理并重新构建：
   ```bash
   rm -rf dist/
   uv build
   ```
5. 上传新版本：
   ```bash
   twine upload dist/*
   ```

## 自动化发布（GitHub Actions）

可以创建 `.github/workflows/publish.yml` 实现自动发布：

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

需要在 GitHub 仓库设置中添加 Secret: `PYPI_API_TOKEN`

## 常见问题

### 错误：文件已存在
如果上传时提示文件已存在，说明该版本号已发布过。需要：
1. 更新版本号
2. 重新构建
3. 再次上传

### 错误：包名已被占用
如果包名被占用，需要修改 `pyproject.toml` 中的 `name` 字段。

### 包大小问题
确保 `.gitignore` 中排除了不需要的文件：
- `__pycache__/`
- `*.pyc`
- `.env`
- `hyperliquid_mcp.log`

## 验证清单

发布前检查：
- [ ] LICENSE 文件存在
- [ ] README.md 完整且格式正确
- [ ] version 号正确
- [ ] dependencies 版本号合理
- [ ] 在测试 PyPI 上验证通过
- [ ] 本地可以正常 import 和运行

## 参考资源

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)
