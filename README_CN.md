[English](README.md) | 简体中文

# seekdb 生态插件集合

本仓库包含多个插件，旨在增强 **seekdb** 与各种框架和工具的集成。每个插件都针对特定场景进行了优化，以确保稳定高效的数据库操作。

---

## 🧩 项目概述

seekdb 是一个高性能向量数据库，为 AI 应用提供强大的能力，包括向量搜索、混合搜索和 AI 函数。本仓库提供以下插件，帮助开发者将 seekdb 无缝集成到开发工作流中：

| 插件名称                                                                             | 使用场景                  | 核心功能                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| [seekdb Agent Skills](./agent-skills/README_CN.md)                             | 开发工具、数据分析         | 为 AI 智能体提供 seekdb 技能：文档知识库、数据导入（CSV/Excel 向量化）、混合搜索与导出、seekdb-cli 命令行技能 |
| [seekdb Cursor Extension](./cursor-extension/README_CN.md)                            | 开发工具         | 将 seekdb 数据库文档添加到 Cursor 的 `.cursor/rules` 目录，实现 AI 助手集成 |
| [seekdb-cli](./seekdb-cli/README_CN.md)                                                | 命令行、AI Agent          | 面向 AI Agent 的 CLI：默认 JSON、无状态、SQL/schema/向量集合/数据库 AI 管理 |

---

## 📁 插件详情

### ✅ seekdb Agent Skills

- **技能**：
  - **seekdb**：完整的官方文档知识库，支持语义搜索
  - **importing-to-seekdb**：导入 CSV/Excel 文件，自动向量化指定列以支持语义搜索
  - **querying-from-seekdb**：混合搜索（全文 + 语义），支持元数据过滤和 CSV/Excel 导出
  - **seekdb-cli**：通过 seekdb-cli 命令行与 seekdb/OceanBase 交互：执行 SQL、查看 schema/表画像、关系推断、向量集合与 AI 模型管理（JSON 输出、无状态，适合 AI Agent 调用）

- **使用场景**：
  - 查询 seekdb 技术文档和最佳实践
  - 将产品目录、文档或任何表格数据导入 seekdb 并生成向量嵌入
  - 执行带元数据过滤的语义搜索并导出结果
  - 通过 Shell 执行 SQL、查看表结构、管理向量集合或使用数据库内 AI（seekdb-cli 技能）

- **示例工作流程**：
  ```
  1. "如何在 seekdb 中创建向量集合？" → 文档查询
  2. "将 sample_products.xlsx 导入，向量化 Details 列" → 数据导入
  3. "找出评分 >= 4.3 且有 AMOLED 屏幕的手机，导出为 Excel" → 混合搜索 + 导出
  4. "用 seekdb-cli 查 test 表前 10 行" 或 "列出所有表 / 看某表结构" → seekdb-cli 技能
  ```

- **文档**：[seekdb Agent Skills](./agent-skills/README_CN.md)

### ✅ seekdb Cursor Extension

- **功能**：将 seekdb 数据库文档添加到工作区的 `.cursor/rules` 目录，使 Cursor AI 助手能够理解 seekdb 数据库知识。支持版本管理和手动移除文档。

- **使用场景**：在 Cursor 编辑器中使用 seekdb 数据库进行开发时，需要 AI 助手访问 seekdb 文档以提供更好的代码建议和帮助。

- **文档**：[seekdb Cursor Extension ](./cursor-extension/README_CN.md)

### ✅ seekdb-cli

- **功能**：面向 AI Agent 的 seekdb / OceanBase 命令行客户端。默认 JSON 输出、无状态调用、统一错误格式；支持 SQL 执行（含行数/写操作保护）、schema 查看与 dump、表画像、关系推断、向量集合管理与检索、数据库内 AI 模型与补全。

- **使用场景**：在终端或由 AI Agent 通过 Shell 调用，执行 SQL、查看表结构、管理向量集合、使用 DBMS_AI_SERVICE / AI_COMPLETE；支持远程连接与嵌入式本地模式。

- **文档**：[seekdb-cli](./seekdb-cli/README_CN.md)

---

## 📚 完整文档链接

| 插件名称                           | 文档链接                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| seekdb Agent Skills             | [seekdb Agent Skills](./agent-skills/README_CN.md)                             |
| seekdb Cursor Extension          | [seekdb Cursor Extension](./cursor-extension/README_CN.md)                            |
| seekdb-cli                        | [seekdb-cli](./seekdb-cli/README_CN.md)                                                |

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

