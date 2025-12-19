[English](README.md) | 简体中文
# seekdb extension for cursor

将 seekdb 数据库文档添加到 `.cursor/rules` 目录，使 Cursor AI 助手能够理解 seekdb 数据库知识。

## 使用方法

### 复制文档到当前项目

1. 打开命令面板：
   - Windows/Linux: 按 `Ctrl+Shift+P`
   - macOS: 按 `Cmd+Shift+P`

2. 输入并选择命令：
   - 输入 "seekdb Docs" 或 "Add seekdb Docs"
   - 选择 `Add seekdb Docs` 命令

3. 文档将自动添加到：
   - `.cursor/rules/seekdb-docs` 目录（官方文档）
   - `.cursor/rules/seekdb.mdc` 文件（规则文件）

### 从当前项目移除文档

1. 打开命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）

2. 输入并选择命令：
   - 输入 "Remove seekdb Docs"
   - 选择 `Remove seekdb Docs` 命令

3. 文档将从以下位置移除：
   - `.cursor/rules/seekdb-docs` 目录
   - `.cursor/rules/seekdb.mdc` 文件

## 工作模式

本扩展支持**两种工作模式**，并具有自动切换功能：

- **远程模式（主要）**：通过 GitHub Raw 获取文档，始终访问最新文档
- **本地模式（备用）**：当 GitHub 不可访问时，从本地 `.cursor/rules/seekdb-docs/` 读取

AI 助手会检测网络可用性并无缝切换模式。

## 功能

- 将 seekdb 官方文档复制到当前工作区的 `.cursor/rules/seekdb-docs` 目录
- 将 `seekdb.mdc` 规则文件复制到当前工作区的 `.cursor/rules` 目录
- 支持版本管理，仅在文档版本更新时重新复制
- 支持手动移除已复制的文档（会同时移除 `.cursor/rules/seekdb-docs` 和 `.cursor/rules/seekdb.mdc`）

## 注意事项

- 扩展不会自动添加文档，需要手动执行命令
- 如果文档已存在且版本相同，将跳过添加
