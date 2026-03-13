# seekdb-cli

面向 AI Agent 的 seekdb / OceanBase 命令行客户端。默认 JSON 输出、无状态调用、统一错误格式，便于 Agent 可靠地执行 SQL、查看 schema、管理向量集合与数据库内 AI 模型。

## 特性

- **默认 JSON**：所有命令输出结构化 JSON，`--format table|csv|jsonl` 可切换人类可读格式
- **行数保护**：无 LIMIT 的 SELECT 先试探 101 行，超过 100 行则要求补充 LIMIT
- **写操作保护**：写操作需 `--write`；禁止无 WHERE 的 DELETE/UPDATE 及 DROP/TRUNCATE
- **敏感字段脱敏**：查询结果中 phone、email、password、id_card 等自动掩码
- **SQL 历史**：操作记录到 `~/.seekdb/sql-history.jsonl`（写入时 SQL 中敏感字面量会脱敏）
- **数据库 AI**：通过 DBMS_AI_SERVICE 管理模型与 endpoint，通过 AI_COMPLETE 做补全

## 环境要求

- Python 3.11+
- seekdb / OceanBase 服务（或兼容 MySQL 协议）

## 安装

```bash
# 使用 uv（推荐）
cd seekdb-cli && uv sync

# 或 pip
pip install -e .
```

安装后可使用 `seekdb` 命令。

## 连接

通过环境变量或全局选项指定 DSN（**全局选项须写在子命令前**）：

```bash
export SEEKDB_DSN="seekdb://user:pass@host:port/database"

# 或每次指定
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" status
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `seekdb status` | 连接状态与版本 |
| `seekdb schema tables` | 列出所有表 |
| `seekdb schema describe <table>` | 表结构（列、类型、索引） |
| `seekdb table profile <table>` | 表数据画像（行数、空值、distinct、min/max、候选 JOIN 键与时间列） |
| `seekdb sql "<stmt>"` | 执行 SQL（只读默认；加 `--write` 允许写；`--with-schema` 附带表 schema；`--no-truncate` 不截断大字段） |
| `seekdb relations infer [--table <t>]` | 推断表间 JOIN 关系 |
| `seekdb collection list \| create \| delete \| info` | 向量集合管理 |
| `seekdb query <coll> --text "<query>" [--mode semantic\|fulltext\|hybrid]` | 集合检索 |
| `seekdb get <coll> [--ids ...] [--limit n]` | 按 ID 或条件取文档 |
| `seekdb add <coll> (--file \| --stdin \| --data)` | 向集合写入数据 |
| `seekdb export <coll> --output <path>` | 导出集合数据 |
| `seekdb ai model list \| create \| delete` | AI 模型管理（DBMS_AI_SERVICE） |
| `seekdb ai model endpoint create \| delete` | AI 模型 endpoint 创建/删除 |
| `seekdb ai complete "<prompt>" --model <name>` | 数据库内 AI 补全（AI_COMPLETE） |
| `seekdb ai-guide` | 输出 AI Agent 用结构化指南（JSON） |

## 选项顺序

`--dsn`、`--format` 为主命令的全局选项，必须写在子命令**之前**：

```bash
seekdb --format table sql "SELECT * FROM t LIMIT 5"
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" schema tables
```

## 文档与设计

完整设计与约定见仓库根目录下的 [design.md](../design.md)。

## License

MIT
