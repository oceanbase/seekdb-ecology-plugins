# seekdb Documentation Examples

Complete workflow examples for common seekdb documentation queries.

## Example 1: Keyword Search (Normal Flow)

**User Query**: "How do I use vector search in seekdb?"

**Process**:

1. **Resolve skill directory**
   ```
   Read SKILL.md → extract parent directory as <skill_dir>
   ```

2. **Grep catalog**
   ```bash
   grep -i "vector search" <skill_dir>references/seekdb-docs-catalog.jsonl
   ```
   Found matches:
   ```json
   {"path": "200.develop/600.search/300.vector-search/100.vector-search-intro.md",
    "description": "This document provides an overview of vector search in seekdb, covering core concepts, supported vector data types, indexing methods, and search operations."}
   {"path": "200.develop/600.search/300.vector-search/300.vector-similarity-search.md",
    "description": "This document explains vector similarity search methods in seekdb..."}
   ```

3. **Read documents (local-first)**
   - Try: `<skill_dir>seekdb-docs/200.develop/600.search/300.vector-search/100.vector-search-intro.md`
   - Success → provide answer

---

## Example 2: Remote Fallback Scenario

**User Query**: "How do I deploy seekdb on macOS?"

**Process**:

1. **Resolve skill directory** → `<skill_dir>`

2. **Grep catalog**
   ```bash
   grep -i "mac" <skill_dir>references/seekdb-docs-catalog.jsonl
   ```
   Found:
   ```json
   {"path": "400.guides/400.deploy/700.server-mode/100.deploy-by-systemd.md",
    "description": "This document provides instructions for deploying and managing the seekdb database using systemd on RPM-based, DEB-based, and macOS systems..."}
   ```

3. **Read document**
   - Try local: `<skill_dir>seekdb-docs/400.guides/400.deploy/700.server-mode/100.deploy-by-systemd.md`
   - Local missing → fallback: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.1.0/en-US/400.guides/400.deploy/700.server-mode/100.deploy-by-systemd.md`

---

## Example 3: Multiple Matches

**User Query**: "Tell me about seekdb indexes"

**Process**:

1. **Resolve skill directory** → `<skill_dir>`

2. **Grep catalog**
   ```bash
   grep -i "index" <skill_dir>references/seekdb-docs-catalog.jsonl
   ```
   Found multiple matches:
   ```json
   {"path": "200.develop/600.search/300.vector-search/200.vector-index/100.vector-index-overview.md", "description": "...vector index types..."}
   {"path": "200.develop/200.design-database-schema/35.multi-model/300.char-and-text/300.full-text-index.md", "description": "...full-text indexes..."}
   {"path": "200.develop/200.design-database-schema/40.create-index-in-develop.md", "description": "...creating indexes..."}
   ```

3. **Read all relevant documents** (local-first for each)

4. **Provide comprehensive answer** covering vector indexes, full-text indexes, and index creation syntax
