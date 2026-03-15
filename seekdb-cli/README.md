English | [简体中文](README_CN.md)
# seekdb-cli

Command-line client for seekdb / OceanBase, built for AI agents. Default JSON output, stateless invocations, and a consistent error format make it easy for agents to run SQL, inspect schema, manage vector collections, and use in-database AI models reliably.

## Features

- **JSON by default**: All commands emit structured JSON; use `--format table|csv|jsonl` for human-readable output.
- **Row limits**: SELECTs without LIMIT are probed with 101 rows; if more than 100 rows are returned, the CLI asks for an explicit LIMIT.
- **Write safeguards**: Writes require `--write`; DELETE/UPDATE without WHERE and DROP/TRUNCATE are disallowed.
- **Sensitive-field masking**: Columns such as phone, email, password, id_card are auto-masked in query results.
- **SQL history**: Operations are logged to `~/.seekdb/sql-history.jsonl` (sensitive literals in SQL are redacted when logged).
- **Database AI**: Manage models and endpoints via DBMS_AI_SERVICE; use AI_COMPLETE for completion.

## Requirements

- Python 3.11+
- seekdb / OceanBase (or any MySQL-protocol–compatible server)

## Installation

```bash
# With uv (recommended)
cd seekdb-cli && uv sync

# Or with pip
pip install -e .
```

After installation, the `seekdb` command is available.

## Connection

Set the DSN via environment variable or global option (**global options must appear before the subcommand**):

```bash
# Remote
export SEEKDB_DSN="seekdb://user:pass@host:port/database"

# Embedded (local directory, no separate server)
export SEEKDB_DSN="embedded:./seekdb.db"
export SEEKDB_DSN="embedded:./data?database=mydb"

# Or pass per invocation
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" status
```

## Common commands

| Command | Description |
|--------|-------------|
| `seekdb status` | Connection status and version |
| `seekdb schema tables` | List all tables |
| `seekdb schema describe <table>` | Table structure (columns, types, indexes) |
| `seekdb schema dump` | Output DDL for all tables (to stdout) |
| `seekdb table profile <table>` | Table data profile (row count, nulls, distinct, min/max, candidate JOIN keys and time columns) |
| `seekdb sql "<stmt>"` | Execute SQL (read-only by default; use `--write` for writes; `--with-schema` adds table schema; `--no-truncate` keeps large fields intact) |
| `seekdb relations infer [--table <t>]` | Infer JOIN relationships between tables |
| `seekdb collection list \| create \| delete \| info` | Vector collection management |
| `seekdb query <coll> --text "<query>" [--mode semantic\|fulltext\|hybrid]` | Search a collection |
| `seekdb get <coll> [--ids ...] [--limit n]` | Get documents by ID or condition |
| `seekdb add <coll> (--file \| --stdin \| --data)` | Add data to a collection |
| `seekdb export <coll> --output <path>` | Export collection data |
| `seekdb ai model list \| create \| delete` | AI model management (DBMS_AI_SERVICE) |
| `seekdb ai model endpoint create \| delete` | Create or delete AI model endpoints |
| `seekdb ai complete "<prompt>" --model <name>` | In-database AI completion (AI_COMPLETE) |
| `seekdb ai-guide` | Print structured guide for AI agents (JSON) |

## Option order

`--dsn` and `--format` are global options and must appear **before** the subcommand:

```bash
seekdb --format table sql "SELECT * FROM t LIMIT 5"
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" schema tables
```

## License

MIT
