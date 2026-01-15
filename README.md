English | [简体中文](README_CN.md)

# seekdb Ecosystem Plugins Collection

This repository includes multiple plugins designed to enhance **seekdb** integration with various frameworks and tools. Each plugin is optimized for specific scenarios to ensure stable and efficient database operations.

---

## 🧩 Project Overview

seekdb is a high-performance vector database that provides powerful capabilities for AI applications, including vector search, hybrid search, and AI functions. This repository provides the following plugins to help developers integrate seekdb seamlessly into their development workflows:

| Plugin Name                                                                             | Use Case                  | Key Features                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| [seekdb Claude Code Plugin](./claudecode-plugin/README.md)                             | Development Tools         | This plugin contains seekdb skill that is designed specifically for Claude Code, aimed at enhancing Claude's capabilities in seekdb database scenarios.                 |
| [seekdb Cursor Extension](./cursor-extension/README.md)                            | Development Tools         | Adds seekdb database documentation to Cursor's `.cursor/rules` directory for AI assistant integration |

---

## 📁 Plugin Details

### ✅ seekdb Claude Code Plugin

- **Function**: Provides seekdb database-related documentation support for Claude Code, with built-in complete seekdb official documentation knowledge base supporting document query and retrieval.

- **Use Case**: When using seekdb database in Claude Code, need to query technical documentation and obtain best practices.

- **Documentation**: [seekdb Claude Code Plugin](./claudecode-plugin/README.md)

### ✅ seekdb Cursor Extension

- **Function**: Adds seekdb database documentation to the `.cursor/rules` directory in your workspace, enabling the Cursor AI assistant to understand seekdb database knowledge. Supports version management and manual removal of documentation.

- **Use Case**: When developing with seekdb database in Cursor editor, need the AI assistant to have access to seekdb documentation for better code suggestions and assistance.

- **Documentation**: [seekdb Cursor Extension](./cursor-extension/README.md)

---

## 📚 Full Documentation Links

| Plugin Name                           | Documentation Link                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| seekdb Claude Code Plugin             | [seekdb Claude Code Plugin](./claudecode-plugin/README.md)                             |
| seekdb Cursor Extension          | [seekdb Cursor Extension](./cursor-extension/README.md)                            |

---

## 🛠️ Contributing & Feedback

We welcome contributions via **Issues** or **Pull Requests**.

For questions or suggestions, visit [GitHub Issues](https://github.com/oceanbase/seekdb-ecology-plugins/issues).

---

## 📄 License

This project is licensed under the [Apache License 2.0](./LICENSE).

---

## 📌 Notes

- For detailed configuration and usage instructions, refer to the respective plugin documentation.

