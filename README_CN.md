[English](README.md) | 简体中文

# Seekdb 生态插件集合

本仓库包含多个插件，旨在增强 **seekdb** 与各种框架和工具的集成。每个插件都针对特定场景进行了优化，以确保稳定高效的数据库操作。

---

## 🧩 项目概述

SeekDB 是一个高性能向量数据库，为 AI 应用提供强大的能力，包括向量搜索、混合搜索和 AI 函数。本仓库提供以下插件，帮助开发者将 SeekDB 无缝集成到开发工作流中：

| 插件名称                                                                             | 使用场景                  | 核心功能                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| [Seekdb Claude Code Plugin](./claudecode-plugin/README_CN.md)                             | 开发工具         | 为 Claude Code 提供 seekdb 数据库相关文档支持                 |
| [Seekdb Cursor Extension](./cursor-extension/README_CN.md)                            | 开发工具         | 将 seekdb 数据库文档添加到 Cursor 的 `.cursor/rules` 目录，实现 AI 助手集成 |

---

## 📁 插件详情

### ✅ Seekdb Claude Code Plugin

- **功能**：为 Claude Code 提供 seekdb 数据库相关文档支持，内置完整的 seekdb 官方文档知识库，支持文档查询和检索。

- **使用场景**：在 Claude Code 中使用 seekdb 数据库时，需要查询技术文档和获取最佳实践。

- **文档**：[Seekdb Claude Code Plugin](./claudecode-plugin/README_CN.md)

### ✅ Seekdb Cursor Extension

- **功能**：将 seekdb 数据库文档添加到工作区的 `.cursor/rules` 目录，使 Cursor AI 助手能够理解 Seekdb 数据库知识。支持版本管理和手动移除文档。

- **使用场景**：在 Cursor 编辑器中使用 seekdb 数据库进行开发时，需要 AI 助手访问 seekdb 文档以提供更好的代码建议和帮助。

- **文档**：[Seekdb Cursor Extension ](./cursor-extension/README_CN.md)

---

## 📚 完整文档链接

| 插件名称                           | 文档链接                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| Seekdb Claude Code Plugin             | [Seekdb Claude Code Plugin](./claudecode-plugin/README_CN.md)                             |
| Seekdb Cursor Extension          | [Seekdb Cursor Extension](./cursor-extension/README_CN.md)                            |

---

## 🛠️ 贡献与反馈

我们欢迎通过 **Issues** 或 **Pull Requests** 进行贡献。

如有问题或建议，请访问 [GitHub Issues](https://github.com/oceanbase/seekdb-ecology-plugins/issues)。

---

## 📄 许可证

本项目采用 [Apache License 2.0](./LICENSE) 许可证。

---

## 📌 注意事项

- 详细的配置和使用说明，请参考相应插件的文档。

