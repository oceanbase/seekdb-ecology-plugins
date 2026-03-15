English | [简体中文](README_CN.md)

# seekdb Ecosystem Plugins Collection

This repository includes multiple plugins designed to enhance **seekdb** integration with various frameworks and tools. Each plugin is optimized for specific scenarios to ensure stable and efficient database operations.

---

## 🧩 Project Overview

seekdb is a high-performance vector database that provides powerful capabilities for AI applications, including vector search, hybrid search, and AI functions. This repository provides the following plugins to help developers integrate seekdb seamlessly into their development workflows:

| Plugin Name                                                                             | Use Case                  | Key Features                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| [seekdb Agent Skills](./agent-skills/README.md)                             | Development Tools/Data Analysis         | Agent skills for seekdb: documentation knowledge base, data import (CSV/Excel with vectorization), hybrid search with export, seekdb-cli command-line skill |
| [seekdb Cursor Extension](./cursor-extension/README.md)                            | Development Tools         | Adds seekdb database documentation to Cursor's `.cursor/rules` directory for AI assistant integration |
| [seekdb-cli](./seekdb-cli/README.md)                                                | CLI / AI Agent            | AI-Agent-friendly CLI: default JSON, stateless, SQL/schema/vector collections/database AI management |

---

## 📁 Plugin Details

### ✅ seekdb Agent Skills

- **Skills**:
  - **seekdb**: Complete official documentation knowledge base with semantic search
  - **importing-to-seekdb**: Import CSV/Excel files with automatic column vectorization for semantic search
  - **querying-from-seekdb**: Hybrid search (fulltext + semantic) with metadata filtering and CSV/Excel export
  - **seekdb-cli**: Interact with seekdb/OceanBase via the seekdb-cli command line: run SQL, inspect schema/table profile, infer relations, manage vector collections and AI models (JSON output, stateless, for AI Agent invocation)

- **Use Case**: 
  - Query seekdb technical documentation and best practices
  - Import product catalogs, documents, or any tabular data into seekdb with vector embeddings
  - Perform semantic search with metadata filters and export results
  - Run SQL, inspect table structure, manage vector collections, or use in-database AI via Shell (seekdb-cli skill)

- **Example Workflow**:
  ```
  1. "How to create a vector collection in seekdb?" → Documentation query
  2. "Import sample_products.xlsx, vectorize the Details column" → Data import
  3. "Find phones with rating >= 4.3 and AMOLED screen, export to Excel" → Hybrid search + export
  4. "Query first 10 rows of test table with seekdb-cli" or "List all tables / describe a table" → seekdb-cli skill
  ```

- **Documentation**: [seekdb Agent Skills](./agent-skills/README.md)

### ✅ seekdb Cursor Extension

- **Function**: Adds seekdb database documentation to the `.cursor/rules` directory in your workspace, enabling the Cursor AI assistant to understand seekdb database knowledge. Supports version management and manual removal of documentation.

- **Use Case**: When developing with seekdb database in Cursor editor, need the AI assistant to have access to seekdb documentation for better code suggestions and assistance.

- **Documentation**: [seekdb Cursor Extension](./cursor-extension/README.md)

### ✅ seekdb-cli

- **Function**: AI-Agent-friendly command-line client for seekdb / OceanBase. Default JSON output, stateless calls, unified error format; supports SQL execution (with row/write safeguards), schema inspection and dump, table profile, relation inference, vector collection management and search, and in-database AI models and completion.

- **Use Case**: Invoked from the terminal or by an AI Agent via Shell to run SQL, inspect table structure, manage vector collections, or use DBMS_AI_SERVICE / AI_COMPLETE; supports remote and embedded local mode.

- **Documentation**: [seekdb-cli](./seekdb-cli/README.md)

---

## 📚 Full Documentation Links

| Plugin Name                           | Documentation Link                                                                      |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| seekdb Agent Skills             | [seekdb Agent Skills](./agent-skills/README.md)                             |
| seekdb Cursor Extension          | [seekdb Cursor Extension](./cursor-extension/README.md)                            |
| seekdb-cli                        | [seekdb-cli](./seekdb-cli/README.md)                                                |

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

