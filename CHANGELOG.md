# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2025-10-28

### Fixed

- **关键修复**: 修正 OCO 分组常量大小写,解决止盈止损订单 422 错误
  - 修改 `normalTpSl` -> `normalTpsl` (小写 s)
  - 修改 `positionTpSl` -> `positionTpsl` (小写 s)
  - 与 HyperLiquid SDK `Grouping` 类型定义保持完全一致
  - 修复设置止盈止损时的 "Failed to deserialize the JSON body" 错误

### Added

- 新增调试脚本 `test_scripts/debug_tpsl.py` 用于验证订单格式
- 新增验证脚本 `test_scripts/test_grouping_fix.py` 用于测试修复

### Changed

- 更新相关测试和验证脚本以匹配新的常量值
- 改进订单结构注释说明

## [0.1.6] - 2025-10-27

### Fixed

- 清理错误的 v0.2.0 标签，恢复正确的版本历史
- 维护版本一致性

## [0.1.5] - 2025-10-27

### Added

- 自动格式化代码（black 和 isort）
- 优化 release.prompt 支持自动版本号递增

### Changed

- 清理冗余文档和重组文件

## [0.1.4] - Previous Release

Initial release with core HyperLiquid MCP functionality.
