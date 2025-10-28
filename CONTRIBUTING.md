# 贡献指南

感谢你对 HyperLiquid MCP Server 项目的关注!我们欢迎各种形式的贡献。

## 开发流程

### 1. Fork 和克隆

```bash
git clone https://github.com/你的用户名/hyperliquid-mcp-python.git
cd hyperliquid-mcp-python
```

### 2. 安装开发依赖

```bash
# 使用 uv 安装依赖
uv sync --all-extras --dev
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 4. 开发和测试

#### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/unit/test_validators.py

# 运行单元测试
uv run pytest tests/unit -v

# 运行集成测试 (需要配置 .env)
uv run pytest tests/integration -v
```

#### 代码格式化

```bash
# 格式化代码
uv run black .

# 排序导入
uv run isort .
```

### 5. 提交变更

```bash
git add .
git commit -m "feat: 添加新功能" # 或 "fix: 修复bug"
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

在 GitHub 上创建 PR,并填写 PR 模板中的信息。

## 提交信息规范

我们使用约定式提交 (Conventional Commits):

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具的变动

示例:

```
feat: 添加获取资金费率历史的工具
fix: 修复订单簿数据解析错误
docs: 更新 README 安装说明
```

## 代码规范

- 遵循 PEP 8 风格指南
- 使用 Black 进行代码格式化
- 使用 isort 排序导入语句
- 为新功能编写测试
- 为公共 API 添加文档字符串

## 测试要求

- 所有新功能必须包含单元测试
- PR 必须通过所有现有测试
- 尽可能添加集成测试
- 测试覆盖率应保持或提高

## 文档

- 更新 README.md (如果添加了新功能)
- 在 EXAMPLES.md 中添加使用示例
- 为复杂功能添加注释

## 获取帮助

如有问题,请:

- 查看 [README.md](README.md)
- 在 GitHub Issues 中提问
- 查看现有的 Pull Requests

再次感谢你的贡献! 🚀
