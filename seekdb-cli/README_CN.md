[English](README.md) | 简体中文
# seekdb-cli

面向 AI Agent 的 seekdb / OceanBase 命令行客户端。默认 JSON 输出、无状态调用、统一错误格式，便于 Agent 可靠地执行 SQL、查看 schema、管理向量集合与数据库内 AI 模型。

## 为什么选择 seekdb-cli

- **面向 Agent**：任何能执行 Shell 的 Agent 均可通过 `seekdb` 命令使用 seekdb-cli；同时提供同名入口 `seekdb-cli`（与 `seekdb` 等价，便于 `which seekdb-cli` 等探测）。默认输出 JSON 格式，`seekdb ai-guide` 命令给 Agent 提供 seekdb-cli 用法的自描述。
- **安全可控**：行数限制、写操作保护与敏感字段脱敏，降低 Agent 或脚本操作生产数据的风险。
- **统一入口**：远程与嵌入式、SQL 与向量集合、数据库内 AI 共用一套 CLI，无需交互式提示或会话状态。

## 特性

- **默认 JSON**：所有命令输出结构化 JSON，`--format table|csv|jsonl` 可切换人类可读格式
- **行数保护**：超过 100 行要求补充 LIMIT
- **写操作保护**：写操作需 `--write`；禁止无 WHERE 的 DELETE/UPDATE
- **敏感字段脱敏**：列名匹配常见敏感模式（如 phone/mobile、email、password/secret/api key、证件号/SSN 等）时自动掩码
- **操作历史**：所有命令的操作记录到 `~/.seekdb/sql-history.jsonl`；其中 **SQL 执行** 会记录 SQL 文本，并对 SQL 中敏感字面量脱敏
- **数据库 AI**：通过 DBMS_AI_SERVICE 管理模型与 endpoint，通过 AI_COMPLETE 做补全

## 环境要求

- Python 3.11+
- **远程**：可通过 `seekdb://...` 访问的 seekdb / OceanBase（或兼容 MySQL 协议的服务）
- **嵌入式**（默认本地存储）：Linux（glibc ≥ 2.28）或 macOS 15+，且需 `pyseekdb`；其他平台请改用远程 DSN

## 安装

```bash
pip install seekdb-cli
```

安装后可使用 `seekdb` 命令；亦提供 `seekdb-cli` 作为同一程序的别名（例如与 PyPI 包名一致、供脚本或工具探测）。

## 连接

无需任何配置即可使用——默认使用 `~/.seekdb/seekdb.db` 嵌入式存储。

**嵌入式路径**表示**数据目录**（不存在时会创建），不是单个 SQLite 文件。可选逻辑库名：`embedded:/path/to/dir?database=mydb`。

如需连接远程服务器或指定其他嵌入式目录，创建全局配置文件：

```bash
mkdir -p ~/.seekdb
# 远程
echo 'SEEKDB_DSN="seekdb://user:pass@host:port/database"' > ~/.seekdb/config.env

# 或嵌入式自定义数据目录
echo 'SEEKDB_DSN="embedded:/path/to/data"' > ~/.seekdb/config.env
```

**DSN 解析顺序**（前者覆盖后者）：

1. 命令行 `--dsn`  
2. 环境变量 `SEEKDB_DSN`  
3. **当前工作目录**下的 `.env`（含 `SEEKDB_DSN=...` 行）  
4. `~/.seekdb/config.env`  
5. 默认 `embedded:~/.seekdb/seekdb.db`

**TLS（仅远程 DSN）：** 写在 URL 查询串即可，例如 `seekdb://user:pass@host:2881/db?tls=skip-verify`（加密且不校验证书，常见于自签名）或 `?tls=required`（加密并按系统 CA 校验）。`tls=` 与 MySQL 风格 `sslmode=` 等价，例如 `REQUIRED`、`VERIFY_CA`、`VERIFY_IDENTITY`、`skip-verify`。PEM：`ssl_ca`、`ssl_cert`、`ssl_key`，可选 `ssl_key_password`。仅此即可确定 TLS，不必再设单独 TLS 环境变量。

## 常用命令

| 命令 | 说明 |
|------|------|
| `seekdb status` | 连接状态与版本 |
| `seekdb schema tables` | 列出所有表 |
| `seekdb schema describe <table>` | 表结构（列、类型、索引） |
| `seekdb schema dump` | 输出所有表的 DDL |
| `seekdb table profile <table>` | 表数据画像（行数、空值、distinct、min/max、候选 JOIN 键与时间列） |
| `seekdb sql "<stmt>"` | 执行 SQL（只读默认；`--write` 允许写；`--with-schema` / `--no-truncate`；`--file` / `--stdin` 或**管道 stdin** 输入） |
| `seekdb relations infer [--table <t>]` | 推断表间 JOIN 关系 |
| `seekdb collection list \| create \| delete \| info` | 向量集合管理 |
| `seekdb query <coll> --text "<query>" [--mode semantic\|fulltext\|hybrid]` | 集合检索（默认 **hybrid** 混合检索） |
| `seekdb get <coll> [--ids ...] [--limit n]` | 按 ID 或条件取文档 |
| `seekdb add <coll> (--file \| --stdin \| --data)` | 向集合写入数据 |
| `seekdb export <coll> --output <path>` | 导出集合数据 |
| `seekdb ai model list \| create \| delete` | AI 模型管理（DBMS_AI_SERVICE） |
| `seekdb ai model endpoint create \| delete` | `create <endpoint> <ai_model> --url <url> --access-key <key>` [`--provider` …]；`delete <endpoint>` |
| `seekdb ai complete "<prompt>" --model <name>` | 数据库内 AI 补全（AI_COMPLETE） |
| `seekdb ai-guide` | 输出 AI Agent 用结构化指南（JSON） |

## 选项顺序

`--dsn`、`--format` 为主命令的全局选项，必须写在子命令**之前**：

```bash
seekdb --format table sql "SELECT * FROM t LIMIT 5"
seekdb --dsn "seekdb://root:@127.0.0.1:2881/test" schema tables
```
