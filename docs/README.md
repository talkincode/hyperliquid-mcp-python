# 文档网站

本项目使用 **MkDocs Material** 构建文档网站。

## 本地开发

### 安装依赖

```bash
pip install -r docs-requirements.txt
```

### 本地预览

```bash
# 启动开发服务器
mkdocs serve

# 或使用 Makefile
make -f Makefile.docs docs-serve
```

访问 http://127.0.0.1:8000 查看文档。

### 构建静态文件

```bash
# 构建文档
mkdocs build

# 或使用 Makefile
make -f Makefile.docs docs-build
```

生成的静态文件位于 `site/` 目录。

## 部署

### 自动部署

推送到 `main` 分支时，GitHub Actions 会自动构建并部署到 GitHub Pages。

### 手动部署

```bash
# 部署到 GitHub Pages
mkdocs gh-deploy --force

# 或使用 Makefile
make -f Makefile.docs docs-deploy
```

## 文档结构

```
docs/
├── index.md                    # 首页
├── getting-started/            # 快速开始
│   ├── installation.md         # 安装指南
│   ├── configuration.md        # 配置指南
│   └── quick-start.md          # 快速验证
├── guides/                     # 使用指南
│   ├── mcp-integration.md      # MCP 客户端集成
│   ├── trading-tools.md        # 交易工具
│   ├── account-management.md   # 账户管理
│   ├── market-data.md          # 市场数据
│   └── use-cases.md            # 常见用例
├── api/                        # API 参考
│   ├── tools-reference.md      # 工具列表
│   ├── response-format.md      # 返回格式
│   └── error-handling.md       # 错误处理
├── developers/                 # 开发者文档
│   ├── architecture.md         # 架构设计
│   ├── testing.md              # 测试工具
│   └── contributing.md         # 贡献指南
├── troubleshooting.md          # 故障排除
└── changelog.md                # 更新日志
```

## 编写指南

### Markdown 扩展

MkDocs Material 支持丰富的 Markdown 扩展：

#### 告示块

```markdown
!!! note "标题"
这是一个提示信息

!!! warning "警告"
这是一个警告信息

!!! danger "危险"
这是一个危险警告
```

#### 代码高亮

````markdown
​`python
def hello():
    print("Hello, World!")
​`
````

#### 标签页

```markdown
=== "Tab 1"
内容 1

=== "Tab 2"
内容 2
```

#### 卡片网格

```markdown
<div class="grid cards" markdown>

- :material-rocket: **快速开始**

  快速上手指南

- :material-book: **文档**

  完整文档

</div>
```

### 文档规范

1. **文件命名**：使用小写字母和连字符，如 `quick-start.md`
2. **标题层级**：每个文件只有一个 `#` 标题
3. **代码示例**：包含完整的代码示例和输出
4. **链接**：使用相对路径链接其他文档
5. **图片**：放在 `docs/assets/images/` 目录

## 配置

主配置文件：`mkdocs.yml`

### 主题配置

```yaml
theme:
  name: material
  language: zh
  palette:
    - scheme: default
      primary: indigo
```

### 导航配置

```yaml
nav:
  - 首页: index.md
  - 快速开始:
      - 安装: getting-started/installation.md
```

### 插件配置

```yaml
plugins:
  - search
  - minify
```

## 相关资源

- [MkDocs 官方文档](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown 扩展](https://squidfunk.github.io/mkdocs-material/reference/)
