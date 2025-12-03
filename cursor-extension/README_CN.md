[English](README.md) | 简体中文
# Seekdb Extension for Cursor

将 seekdb 数据库文档添加到 `.cursor/rules` 目录，使 Cursor AI 助手能够理解 Seekdb 数据库知识。

## 功能

- 将 seekdb 官方文档复制到当前工作区的 `.cursor/rules/seekdb-docs` 目录
- 将 `seekdb.mdc` 规则文件复制到当前工作区的 `.cursor/rules` 目录
- 支持版本管理，仅在文档版本更新时重新复制
- 支持手动移除已复制的文档（会同时移除 `.cursor/rules/seekdb-docs` 和 `.cursor/rules/seekdb.mdc`）

## 使用方法

### 复制文档到当前项目

1. 打开命令面板：
   - Windows/Linux: 按 `Ctrl+Shift+P`
   - macOS: 按 `Cmd+Shift+P`

2. 输入并选择命令：
   - 输入 "Seekdb Docs" 或 "Add Seekdb Docs"
   - 选择 `Add Seekdb Docs` 命令

3. 文档将自动添加到：
   - `.cursor/rules/seekdb-docs` 目录（官方文档）
   - `.cursor/rules/seekdb.mdc` 文件（规则文件）

### 从当前项目移除文档

1. 打开命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）

2. 输入并选择命令：
   - 输入 "Remove Seekdb Docs"
   - 选择 `Remove Seekdb Docs` 命令

3. 文档将从以下位置移除：
   - `.cursor/rules/seekdb-docs` 目录
   - `.cursor/rules/seekdb.mdc` 文件

## 注意事项

- 扩展不会自动添加文档，需要手动执行命令
- 如果文档已存在且版本相同，将跳过添加
