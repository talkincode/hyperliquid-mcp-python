# PyPI 发布前检查清单

## ✅ 发布前必须完成的检查项

### 1. 项目元数据
- [x] LICENSE 文件已创建 (MIT)
- [x] README.md 完整且格式正确
- [x] pyproject.toml 包含所有必需字段
- [x] version 号正确 (当前: 0.1.0)
- [ ] CHANGELOG.md 已更新（如果有）

### 2. 代码质量
- [ ] 所有测试通过
- [ ] 代码已格式化 (black, isort)
- [ ] 没有明显的 bug
- [ ] 文档字符串完整
- [ ] 示例代码可运行

### 3. 依赖项
- [x] dependencies 列表完整
- [x] version 约束合理
- [x] 没有不必要的依赖

### 4. 安全检查
- [ ] 确保 .env 文件在 .gitignore 中
- [ ] 确保私钥不在代码中
- [ ] 敏感信息已移除
- [x] .gitignore 配置正确

### 5. 文件结构
```
hyperliquid-mcp/
├── LICENSE              ✅
├── README.md            ✅
├── PUBLISHING.md        ✅
├── EXAMPLES.md          ✅
├── pyproject.toml       ✅
├── cli.py               ✅
├── main.py              ✅
├── services/
│   └── hyperliquid_services.py  ✅
└── .gitignore           ✅
```

### 6. PyPI 账号准备
- [ ] 注册 https://test.pypi.org 账号
- [ ] 注册 https://pypi.org 账号
- [ ] 生成测试 PyPI API token
- [ ] 生成正式 PyPI API token
- [ ] (可选) 配置 ~/.pypirc 文件

### 7. 本地测试
- [ ] 在虚拟环境中安装依赖
- [ ] 运行 `hyperliquid-mcp --help`
- [ ] 测试 HTTP 模式
- [ ] 测试 stdio 模式
- [ ] 验证所有 MCP 工具可用

## 🚀 快速发布流程

### 方式 1: 使用自动脚本（推荐）

```bash
# 一键发布
./publish.sh
```

### 方式 2: 手动发布

```bash
# 1. 安装工具
uv pip install build twine

# 2. 清理
rm -rf dist/ build/ *.egg-info

# 3. 构建
uv build

# 4. 检查
twine check dist/*

# 5. 测试发布
twine upload --repository testpypi dist/*

# 6. 测试安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperliquid-mcp-python

# 7. 正式发布
twine upload dist/*
```

## 📝 发布后验证

```bash
# 从 PyPI 安装
pip install hyperliquid-mcp-python

# 验证命令可用
hyperliquid-mcp --help

# 验证版本
hyperliquid-mcp --version

# 测试运行
export HYPERLIQUID_PRIVATE_KEY="0x..."
export HYPERLIQUID_TESTNET="true"
hyperliquid-mcp
```

## 🔄 发布新版本流程

1. **更新版本号**
   ```bash
   # 编辑 pyproject.toml
   version = "0.1.1"  # 或 0.2.0, 1.0.0
   
   # 同步更新 cli.py 中的版本号
   version='HyperLiquid MCP v0.1.1'
   ```

2. **更新文档**
   - 更新 README.md
   - 更新 CHANGELOG.md（如果有）
   - 更新 EXAMPLES.md（如果有变化）

3. **提交并打标签**
   ```bash
   git add -A
   git commit -m "chore: bump version to 0.1.1"
   git tag v0.1.1
   git push origin main --tags
   ```

4. **发布新版本**
   ```bash
   ./publish.sh
   ```

## 📊 版本号规范 (Semantic Versioning)

- **0.1.0 → 0.1.1**: Bug 修复、小改进（Patch）
- **0.1.0 → 0.2.0**: 新功能、向后兼容（Minor）
- **0.1.0 → 1.0.0**: 重大变更、API 变化（Major）

## ⚠️ 常见错误及解决

### 错误: HTTPError: 400 Bad Request
原因: 元数据不完整或格式错误
解决: 检查 pyproject.toml，确保所有必需字段存在

### 错误: File already exists
原因: 该版本已发布
解决: 更新版本号后重新构建

### 错误: Invalid distribution filename
原因: 包名格式不正确
解决: 检查 pyproject.toml 中的 name 字段

### 警告: 包太大
解决: 检查 .gitignore，排除不必要的文件
```bash
# 查看包内容
tar -tzf dist/*.tar.gz
```

## 📚 参考资源

- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)

## 🎯 首次发布建议

对于首次发布，强烈建议：

1. ✅ 先发布到测试 PyPI
2. ✅ 测试安装和基本功能
3. ✅ 确认无问题后发布到正式 PyPI
4. ✅ 准备好回滚计划（删除版本需要联系 PyPI 管理员）

## 🔐 安全提示

- ⚠️ 绝不在代码中硬编码 API tokens
- ⚠️ 使用 ~/.pypirc 时设置权限: `chmod 600 ~/.pypirc`
- ⚠️ 定期轮换 PyPI API tokens
- ⚠️ 使用项目范围的 tokens 而非账户范围
