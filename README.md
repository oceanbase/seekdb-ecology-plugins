English | [简体中文](README_CN.md)

# seekdb Ecosystem Plugins Collection

This repository includes multiple plugins designed to enhance **seekdb** integration with various frameworks and tools. Each plugin is optimized for specific scenarios to ensure stable and efficient database operations.

---

## 🧩 Project Overview

seekdb is a high-performance vector database that provides powerful capabilities for AI applications, including vector search, hybrid search, and AI functions. This repository provides the following plugins to help developers integrate seekdb seamlessly into their development workflows:

| Plugin Name                                                                             | Use Case                  | Key Features                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| [seekdb Agent Skills](./agent-skills/README.md)                             | Development Tools/Data Analysis         | This plugin contains seekdb skill that is designed specifically for Claude Code, aimed at enhancing Claude's capabilities in seekdb database scenarios. data import (CSV/Excel with vectorization), and hybrid search with export |
| [seekdb Cursor Extension](./cursor-extension/README.md)                            | Development Tools         | Adds seekdb database documentation to Cursor's `.cursor/rules` directory for AI assistant integration |

---

## 📁 Plugin Details

### ✅ seekdb Claude Code Plugin

- **Function**: Provides comprehensive seekdb capabilities for Claude Code through three integrated skills:
  - **seekdb**: Complete official documentation knowledge base with semantic search
  - **importing-to-seekdb**: Import CSV/Excel files with automatic column vectorization for semantic search
  - **querying-from-seekdb**: Hybrid search (fulltext + semantic) with metadata filtering and CSV/Excel export

- **Use Case**: 
  - Query seekdb technical documentation and best practices
  - Import product catalogs, documents, or any tabular data into seekdb with vector embeddings
  - Perform semantic search with metadata filters and export results

- **Example Workflow**:
  ```
  1. "How to create a vector collection in seekdb?" → Documentation query
  2. "Import sample_products.xlsx, vectorize the Details column" → Data import
  3. "Find phones with rating >= 4.3 and AMOLED screen, export to Excel" → Hybrid search + export
  ```

- **Documentation**: [seekdb Claude Code Plugin](./agent-skills/README.md)

### ✅ seekdb Cursor Extension

- **Function**: Adds seekdb database documentation to the `.cursor/rules` directory in your workspace, enabling the Cursor AI assistant to understand seekdb database knowledge. Supports version management and manual removal of documentation.

- **Use Case**: When developing with seekdb database in Cursor editor, need the AI assistant to have access to seekdb documentation for better code suggestions and assistance.

- **Documentation**: [seekdb Cursor Extension](./cursor-extension/README.md)

---

## 📚 Full Documentation Links

| Plugin Name                           | Documentation Link                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| seekdb Claude Code Plugin             | [seekdb Claude Code Plugin](./agent-skills/README.md)                             |
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

