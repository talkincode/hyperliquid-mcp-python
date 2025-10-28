# 贡献指南

欢迎为 HyperLiquid MCP Server 做出贡献！本页概述开发流程、代码规范与提交要求。更多细节请参考仓库根目录的 `CONTRIBUTING.md`。

## 准备工作

### Fork 与克隆

```bash
git clone https://github.com/<你的用户名>/hyperliquid-mcp-python.git
cd hyperliquid-mcp-python
```

### 安装依赖

```bash
uv sync --all-extras --dev
```

### 创建分支

```bash
git checkout -b feature/<你的功能>
# 或
git checkout -b fix/<你的修复>
```

## 开发流程

1. **实现功能**：遵循既有架构约定，保持异步接口和服务层分离。
2. **补充测试**：新增或修改功能必须附带相应测试。
3. **自检**：运行格式化和静态检查工具，保持代码整洁。
4. **提交 PR**：填写 Pull Request 模板，说明变更动机及测试情况。

### 常用命令

```bash
# 运行全部测试
uv run pytest

# 运行指定测试
uv run pytest tests/unit/test_validators.py

# 运行格式化
uv run black .
uv run isort .
```

## 提交信息规范

项目采用 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 仅格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具变动

示例：

```
feat: 支持批量撤单工具
fix: 修复 size 合法性校验
```

## 代码规范

- 使用 Black / isort 统一代码风格。
- 遵循 PEP 8，必要时补充类型注解。
- 为公共 API 编写 docstring，说明参数与返回值。
- 捕获并整理 HyperLiquid SDK 抛出的异常，统一返回格式。

## 测试要求

- 为新功能添加单元测试，必要时补充集成测试。
- 确保 `uv run pytest` 全部通过。
- 如需真实 API，请使用测试网 (`HYPERLIQUID_TESTNET=true`) 并提供 mock 方案。

## 文档同步

- 功能变更需更新 `docs/api/*.md` 或 `docs/guides/*.md`。
- 文档站点使用 MkDocs，可通过 `mkdocs serve` 本地预览。
- 提交前运行 `mkdocs build`，确保无损坏链接或缺失文件。

## 提交 PR 前检查清单

- [ ] 单元测试与集成测试全部通过。
- [ ] 关键逻辑添加或更新测试用例。
- [ ] 已运行 `uv run black .` 与 `uv run isort .`。
- [ ] 文档已更新并通过构建。
- [ ] PR 模板填写完整，包含测试结果。

## 获取帮助

- 阅读仓库根目录的 `README.md` 与 `CONTRIBUTING.md`。
- 在 GitHub Issues 中提问或参考既有讨论。
- 通过 PR 评论交流实现细节。

感谢你的贡献，祝编码愉快！🚀

---

**相关文档**

- [项目 README](../../README.md)
