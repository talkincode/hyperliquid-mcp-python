# MCP 客户端集成

本页面介绍如何将 HyperLiquid MCP Server 集成到 MCP 客户端（如 Claude Desktop）。

## Claude Desktop 集成

### 前提条件

1. 已安装 Claude Desktop
2. 已完成 [HyperLiquid MCP Server 配置](../getting-started/configuration.md)
3. 已验证服务器可以正常运行

### 配置文件位置

Claude Desktop 的配置文件位于：

**macOS**:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:

```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:

```
~/.config/Claude/claude_desktop_config.json
```

## 配置方式

### 方式 1: 本地开发版本（推荐）

如果你克隆了仓库并在本地开发：

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uv",
      "args": [
        "--directory",
        "/完整/绝对/路径/hyperliquid-mcp",
        "run",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x你的私钥",
        "HYPERLIQUID_TESTNET": "true",
        "HYPERLIQUID_ACCOUNT_ADDRESS": "0x你的账户地址（如使用API钱包）"
      }
    }
  }
}
```

**重要提示**:

- ✅ 使用**完整的绝对路径**（不要用 `~`）
- ✅ macOS/Linux 示例: `/Users/yourname/projects/hyperliquid-mcp`
- ✅ Windows 示例: `C:\\Users\\yourname\\projects\\hyperliquid-mcp`

### 方式 2: 使用 uvx（无需安装）

最简单的方式，无需克隆仓库：

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
        "--from",
        "hyperliquid-mcp-python",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x你的私钥",
        "HYPERLIQUID_TESTNET": "true",
        "HYPERLIQUID_ACCOUNT_ADDRESS": "0x你的账户地址（可选）"
      }
    }
  }
}
```

!!! tip "为什么指定 Python 3.13?"
依赖包 `ckzg` 目前只提供到 Python 3.13 的预编译包。

### 方式 3: 全局安装版本

如果已经通过 pip 全局安装：

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "hyperliquid-mcp",
      "args": ["stdio"],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x你的私钥",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

## 环境变量配置

### 必需变量

| 变量                      | 说明               | 示例        |
| ------------------------- | ------------------ | ----------- |
| `HYPERLIQUID_PRIVATE_KEY` | 私钥（以 0x 开头） | `0x1234...` |

### 可选变量

| 变量                          | 默认值   | 说明                             |
| ----------------------------- | -------- | -------------------------------- |
| `HYPERLIQUID_TESTNET`         | `false`  | 使用测试网（强烈建议先用测试网） |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | 自动派生 | 使用 API 钱包时必需              |

### 配置示例

#### 测试网配置（推荐用于学习）

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
        "--from",
        "hyperliquid-mcp-python",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x1234567890abcdef...",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

#### 主网配置（用于实际交易）

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
        "--from",
        "hyperliquid-mcp-python",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x1234567890abcdef...",
        "HYPERLIQUID_TESTNET": "false"
      }
    }
  }
}
```

#### API 钱包配置

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
        "--from",
        "hyperliquid-mcp-python",
        "hyperliquid-mcp",
        "stdio"
      ],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0xAPI钱包私钥",
        "HYPERLIQUID_ACCOUNT_ADDRESS": "0x主账户地址",
        "HYPERLIQUID_TESTNET": "true"
      }
    }
  }
}
```

!!! warning "API 钱包重要提示"
使用 API 钱包时，`HYPERLIQUID_ACCOUNT_ADDRESS` **必须设置为主账户地址**，而非 API 钱包地址。

## 应用配置

### 1. 编辑配置文件

```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 或使用文本编辑器
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 2. 粘贴配置

选择上面的一种配置方式，复制到文件中。

### 3. 保存并重启 Claude Desktop

配置文件保存后，**完全退出并重启 Claude Desktop**。

### 4. 验证连接

重启后，Claude Desktop 会自动连接 MCP 服务器。

你可以在 Claude 中询问：

```
你能看到 HyperLiquid 相关的工具吗？
```

或直接测试：

```
帮我查看一下 HyperLiquid 账户余额
```

## 验证配置

### 检查服务器状态

在 Claude Desktop 中，服务器状态会显示在界面上：

- ✅ **绿色点**：已连接
- 🟡 **黄色点**：连接中
- ❌ **红色点**：连接失败

### 测试基本功能

```
# 1. 查看余额
帮我查看账户余额

# 2. 获取市场数据
BTC 现在的价格是多少？

# 3. 查看仓位
我有哪些开仓？
```

## 日志查看

### Claude Desktop 日志

查看 Claude Desktop 的 MCP 日志：

**macOS**:

```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows**:

```
%LOCALAPPDATA%\Claude\logs\mcp*.log
```

### 服务器日志

HyperLiquid MCP Server 的日志：

```bash
# 在项目目录
tail -f hyperliquid_mcp.log
```

## 常见问题

### 服务器无法连接

**问题**: Claude Desktop 显示服务器离线

**检查清单**:

1. **路径是否正确**

   ```bash
   # 验证路径存在
   ls /完整/路径/hyperliquid-mcp
   ```

2. **命令是否可用**

   ```bash
   # 测试 uv 命令
   which uv

   # 测试 hyperliquid-mcp 命令
   which hyperliquid-mcp
   ```

3. **环境变量是否正确**

   ```json
   {
     "env": {
       "HYPERLIQUID_PRIVATE_KEY": "0x...", // 必须以 0x 开头
       "HYPERLIQUID_TESTNET": "true" // 注意是字符串 "true"
     }
   }
   ```

4. **重启 Claude Desktop**
   - 完全退出应用
   - 重新启动

### 私钥格式错误

**问题**: 认证失败

**解决方案**:

```json
{
  "env": {
    // ❌ 错误
    "HYPERLIQUID_PRIVATE_KEY": "1234567890abcdef...",

    // ✅ 正确
    "HYPERLIQUID_PRIVATE_KEY": "0x1234567890abcdef..."
  }
}
```

### 找不到命令

**问题**: `command not found: hyperliquid-mcp`

**解决方案**:

使用 uvx 方式（推荐）：

```json
{
  "command": "uvx",
  "args": ["--from", "hyperliquid-mcp-python", "hyperliquid-mcp", "stdio"]
}
```

或使用本地开发版本：

```json
{
  "command": "uv",
  "args": ["--directory", "/完整/路径", "run", "hyperliquid-mcp", "stdio"]
}
```

### API 钱包无法使用

**问题**: 使用 API 钱包时操作失败

**解决方案**:

必须同时设置账户地址：

```json
{
  "env": {
    "HYPERLIQUID_PRIVATE_KEY": "0xAPI钱包私钥",
    "HYPERLIQUID_ACCOUNT_ADDRESS": "0x主账户地址" // 必需！
  }
}
```

## 高级配置

### 多网络配置

可以同时配置测试网和主网：

```json
{
  "mcpServers": {
    "hyperliquid-testnet": {
      "command": "uvx",
      "args": ["--from", "hyperliquid-mcp-python", "hyperliquid-mcp", "stdio"],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x测试网私钥",
        "HYPERLIQUID_TESTNET": "true"
      }
    },
    "hyperliquid-mainnet": {
      "command": "uvx",
      "args": ["--from", "hyperliquid-mcp-python", "hyperliquid-mcp", "stdio"],
      "env": {
        "HYPERLIQUID_PRIVATE_KEY": "0x主网私钥",
        "HYPERLIQUID_TESTNET": "false"
      }
    }
  }
}
```

### 使用配置文件

除了环境变量，也可以使用 `.env` 文件：

1. 在项目目录创建 `.env`：

   ```bash
   HYPERLIQUID_PRIVATE_KEY=0x...
   HYPERLIQUID_TESTNET=true
   ```

2. 配置 Claude Desktop：
   ```json
   {
     "mcpServers": {
       "hyperliquid": {
         "command": "uv",
         "args": [
           "--directory",
           "/完整/路径/hyperliquid-mcp",
           "run",
           "hyperliquid-mcp",
           "stdio"
         ]
       }
     }
   }
   ```

## 安全最佳实践

1. **使用测试网**

   ```json
   "HYPERLIQUID_TESTNET": "true"
   ```

2. **使用 API 钱包**

   - 访问 https://app.hyperliquid.xyz/API
   - 生成专用 API 钱包
   - 权限受限，更安全

3. **定期轮换密钥**

   - 定期更换 API 钱包
   - 删除旧的配置

4. **保护配置文件**
   ```bash
   # 设置适当的文件权限
   chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

## 使用示例

### 查看账户信息

```
你: 帮我查看账户余额和仓位

Claude: 我来帮您查看...
[调用 get_account_balance 和 get_open_positions]
```

### 下单交易

```
你: 用 $100 买入 BTC

Claude: 我来帮您计算并下单...
[调用 calculate_token_amount_from_dollars]
[调用 market_open_position]
```

### 设置止盈止损

```
你: 为我的 BTC 仓位设置止盈 47000，止损 43000

Claude: 我来设置...
[调用 set_take_profit_stop_loss]
```

## 下一步

- [交易工具使用](trading-tools.md) - 学习如何使用各种交易工具
- [账户管理](account-management.md) - 管理账户和仓位
- [故障排除](../troubleshooting.md) - 解决常见问题

## 相关资源

- [Claude Desktop 文档](https://claude.ai/desktop)
- [MCP 协议规范](https://github.com/anthropics/mcp)
- [FastMCP 文档](https://fastmcp.com)
