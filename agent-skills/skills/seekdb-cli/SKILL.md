---
name: seekdb-cli
description: "Use seekdb-cli to interact with seekdb/OceanBase databases via shell commands. seekdb-cli is an AI-Agent-friendly database CLI with JSON-structured output, automatic row protection, write safety guards, and sensitive field masking. Use when: (1) querying databases with SQL, (2) exploring table schemas and structure, (3) profiling table data distributions, (4) inferring table relationships, (5) managing vector collections and semantic search, (6) importing/exporting data, (7) managing AI models, (8) checking database connection status, or (9) performing any database operation via command line. Triggers on: SQL queries, database schema inspection, table exploration, data lookup, vector search, collection management, seekdb operations."
license: MIT
---

# seekdb-cli — AI-Agent Database CLI

A command-line client designed for AI Agents. All output is JSON-structured, stateless, with built-in safety guardrails.

## Prerequisites

Check if seekdb-cli is installed:

```bash
seekdb --version
```

If not installed:

```bash
pip install seekdb-cli            # core (SQL + schema)
pip install seekdb-cli[vector]    # + collection / query support (pyseekdb)
pip install seekdb-cli[ai]        # + AI completion support (openai)
pip install seekdb-cli[all]       # everything
```

## Connection Setup

Set the `SEEKDB_DSN` environment variable before running any command:

```bash
export SEEKDB_DSN="seekdb://user:password@host:port/database"
```

Or pass `--dsn` on each call (overrides env var):

```bash
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" status
```

Verify connectivity:

```bash
seekdb status
# → {"ok": true, "data": {"cli_version": "0.1.0", "server_version": "...", "database": "test", "connected": true}}
```

## Self-Description for AI Agents

Run `seekdb ai-guide` to get a structured JSON guide of all commands, recommended workflow, safety features, and output format. Execute this once to learn the full CLI.

```bash
seekdb ai-guide
```

## Recommended Workflow

### SQL Database Exploration

```
1. seekdb schema tables              → list all tables (name, column count, row count)
2. seekdb schema describe <table>    → get column names, types, indexes, comments
3. seekdb table profile <table>      → get data statistics (null ratios, distinct, min/max, top values)
4. seekdb relations infer            → infer JOIN relationships between tables
5. seekdb sql "SELECT ... LIMIT N"   → execute SQL with explicit LIMIT
```

### Vector Collection Workflow

```
1. seekdb collection list            → list all collections
2. seekdb collection info <name>     → get collection details and preview
3. seekdb query <collection> --text "..." → search by semantic similarity
```

## Command Reference

### seekdb sql

Execute SQL statements. Default is read-only mode.

```bash
# Read query
seekdb sql "SELECT id, name FROM users LIMIT 10"

# Read from file
seekdb sql --file query.sql

# Read from stdin
echo "SELECT 1" | seekdb sql --stdin

# Include table schema in output
seekdb sql "SELECT * FROM orders LIMIT 5" --with-schema

# Disable large-field truncation
seekdb sql "SELECT content FROM articles LIMIT 1" --no-truncate

# Write operation (requires --write flag)
seekdb sql --write "INSERT INTO users (name) VALUES ('Alice')"
seekdb sql --write "UPDATE users SET name = 'Bob' WHERE id = 1"
seekdb sql --write "DELETE FROM users WHERE id = 3"
```

**Output format:**

```json
{"ok": true, "columns": ["id", "name"], "rows": [{"id": 1, "name": "Alice"}], "affected": 0, "time_ms": 12}
```

### seekdb schema tables

```bash
seekdb schema tables
```

```json
{"ok": true, "data": [{"name": "users", "columns": 5, "rows": 1200}, {"name": "orders", "columns": 8, "rows": 50000}]}
```

### seekdb schema describe

```bash
seekdb schema describe orders
```

```json
{"ok": true, "data": {"table": "orders", "comment": "Order table", "columns": [{"name": "id", "type": "int", "comment": "Order ID"}, {"name": "status", "type": "varchar(20)", "comment": "0=pending, 1=paid"}], "indexes": ["PRIMARY(id)", "idx_status(status)"]}}
```

### seekdb schema dump

```bash
seekdb schema dump
```

Returns all `CREATE TABLE` DDL statements.

### seekdb table profile

Generate statistical summary of a table without returning raw data. Helps understand data distribution before writing SQL.

```bash
seekdb table profile <table>
```

```json
{"ok": true, "data": {
  "table": "orders",
  "row_count": 50000,
  "columns": [
    {"name": "id", "type": "int", "null_ratio": 0, "distinct": 50000, "min": 1, "max": 50000},
    {"name": "user_id", "type": "int", "null_ratio": 0, "distinct": 1200, "min": 1, "max": 1500},
    {"name": "amount", "type": "decimal(10,2)", "null_ratio": 0.02, "min": 0.5, "max": 9999.99},
    {"name": "status", "type": "varchar(20)", "null_ratio": 0, "distinct": 4, "top_values": ["paid", "pending", "refunded", "cancelled"]},
    {"name": "created_at", "type": "datetime", "null_ratio": 0, "min": "2024-01-01", "max": "2026-03-10"}
  ],
  "candidate_join_keys": ["user_id"],
  "candidate_time_columns": ["created_at"]
}}
```

### seekdb relations infer

Infer JOIN relationships between tables by analyzing column name patterns (e.g., `user_id` → `users.id`) and type compatibility.

```bash
# Infer all table relationships
seekdb relations infer

# Infer for a specific table only
seekdb relations infer --table orders
```

```json
{"ok": true, "data": [
  {"from": "orders.user_id", "to": "users.id", "confidence": "high"},
  {"from": "orders.product_id", "to": "products.id", "confidence": "high"},
  {"from": "order_items.order_id", "to": "orders.id", "confidence": "high"}
]}
```

### seekdb collection list

```bash
seekdb collection list
```

```json
{"ok": true, "data": [{"name": "docs", "count": 1500}, {"name": "faq", "count": 200}]}
```

### seekdb collection create

```bash
seekdb collection create my_docs --dimension 384 --distance cosine
```

### seekdb collection delete

```bash
seekdb collection delete my_docs
```

### seekdb collection info

```bash
seekdb collection info my_docs
```

```json
{"ok": true, "data": {"name": "my_docs", "count": 1500, "preview": {"ids": ["doc1", "doc2"], "documents": ["Hello world", "Test doc"], "metadatas": [{"category": "test"}, {}]}}}
```

### seekdb query

Search a collection using semantic (vector), fulltext, or hybrid mode.

```bash
# Semantic search (default)
seekdb query my_docs --text "how to deploy seekdb"

# Fulltext search
seekdb query my_docs --text "deployment guide" --mode fulltext

# Hybrid search (semantic + fulltext, RRF ranking)
seekdb query my_docs --text "deploy seekdb" --mode hybrid

# With metadata filter
seekdb query my_docs --text "performance tuning" --where '{"category": "tech"}'

# Limit results
seekdb query my_docs --text "seekdb" --limit 5
```

```json
{"ok": true, "data": {"results": [
  {"id": "doc1", "score": 0.92, "document": "How to deploy seekdb...", "metadata": {"category": "tech"}},
  {"id": "doc2", "score": 0.85, "document": "seekdb performance tuning...", "metadata": {"category": "tech"}}
], "count": 2}, "time_ms": 35}
```

### seekdb get

Retrieve documents from a collection by IDs or metadata filter.

```bash
# Get by IDs
seekdb get my_docs --ids "doc1,doc2"

# Get by metadata filter
seekdb get my_docs --where '{"category": "tech"}' --limit 20
```

### seekdb import

Import data into a collection from a JSON, JSONL, or CSV file.

```bash
seekdb import my_docs --file data.jsonl
seekdb import my_docs --file articles.csv --vectorize-column content
```

**File format**: Each record should have `id` (optional), `document`/`text`/`content` (text to vectorize), and any other fields become metadata. If `embedding` field is present, it is used directly.

### seekdb export

Export collection data to a file.

```bash
seekdb export my_docs --output backup.json
seekdb export my_docs --output backup.jsonl --limit 5000
```

### seekdb ai model list

```bash
seekdb ai model list
```

```json
{"ok": true, "data": [{"name": "gpt4", "provider": "openai", "model": "gpt-4o", "created_at": "2026-03-12"}]}
```

### seekdb ai model create

```bash
seekdb ai model create gpt4 --provider openai --model gpt-4o --api-key sk-...
seekdb ai model create local-llm --provider ollama --model llama3
seekdb ai model create qwen --provider qwen --model qwen-max --base-url https://dashscope.aliyuncs.com/compatible-mode/v1
```

### seekdb ai model delete

```bash
seekdb ai model delete gpt4
```

### seekdb ai complete

```bash
seekdb ai complete "Summarize this table structure" --model gpt4
```

```json
{"ok": true, "data": {"model": "gpt4", "response": "The table has..."}, "time_ms": 1200}
```

### seekdb ai-guide

Output a structured JSON guide for AI Agents containing all commands, parameters, workflow, and safety rules. Execute once to learn the full CLI.

```bash
seekdb ai-guide
```

### seekdb status

```bash
seekdb status
```

Returns CLI version, server version, database name, and connectivity.

## Safety Features

### Row Protection

Queries without `LIMIT` are automatically probed. If result exceeds 100 rows, execution is blocked:

```json
{"ok": false, "error": {"code": "LIMIT_REQUIRED", "message": "Query returns more than 100 rows. Please add LIMIT to your SQL."}}
```

**Action**: Add an explicit `LIMIT` clause and retry.

### Write Protection

Write operations (INSERT/UPDATE/DELETE) are blocked by default:

```json
{"ok": false, "error": {"code": "WRITE_NOT_ALLOWED", "message": "Write operations require --write flag."}}
```

**Action**: Add `--write` flag to enable write operations.

Even with `--write`, these are always blocked:
- `DELETE` / `UPDATE` without `WHERE` clause
- `DROP` / `TRUNCATE` statements

### Error Auto-Correction

On SQL errors, the CLI automatically attaches schema hints:

**Column not found** → returns the table's column list and indexes:
```json
{"ok": false, "error": {"code": "SQL_ERROR", "message": "Unknown column 'username'"}, "schema": {"table": "users", "columns": ["id", "name", "email"], "indexes": ["PRIMARY(id)"]}}
```

**Table not found** → returns available table names:
```json
{"ok": false, "error": {"code": "SQL_ERROR", "message": "Table 'user' does not exist"}, "schema": {"tables": ["users", "orders", "products"]}}
```

**Action**: Use the schema info to correct the SQL and retry.

### Large Field Truncation

TEXT/BLOB fields are truncated to 200 characters by default, with original length noted:

```json
{"content": "First 200 characters of content...(truncated, 8520 chars)"}
```

Use `--no-truncate` to get full content when needed.

### Sensitive Field Masking

Columns matching sensitive patterns are automatically masked:

| Pattern | Example Output |
|---------|---------------|
| phone/mobile/tel | `138****5678` |
| email | `z***@gmail.com` |
| password/secret/token | `******` |
| id_card/ssn | `110***********1234` |

## Output Formats

Default is JSON. Switch with `--format`:

```bash
seekdb --format table sql "SELECT id, name FROM users LIMIT 5"
seekdb --format csv sql "SELECT id, name FROM users LIMIT 5"
seekdb --format jsonl sql "SELECT id, name FROM users LIMIT 5"
```

All formats now work with non-row data (e.g., `schema tables`, `collection list`). CSV and JSONL will auto-detect list-of-dict data in the `data` field.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Business error (SQL error, connection error, etc.) |
| 2 | Usage error (missing arguments, invalid options) |

## Operation Logging

All commands are logged to `~/.seekdb/history.jsonl` for audit:

```json
{"ts": "2026-03-12T14:23:01", "command": "sql", "sql": "SELECT id FROM users LIMIT 10", "ok": true, "rows": 10, "time_ms": 12}
```
