"""seekdb-cli — AI-Agent-friendly database CLI for seekdb / OceanBase."""

from __future__ import annotations

import json

import click
import pymysql

from seekdb_cli import __version__, output
from seekdb_cli.connection import get_connection, is_embedded_dsn, resolve_raw_dsn
from seekdb_cli.logger import log_operation


@click.group(invoke_without_command=True)
@click.option(
    "--dsn", envvar="SEEKDB_DSN", default=None,
    help="Connection string. Remote: seekdb://user:pass@host:port/db  Embedded: embedded:<path>[?database=<db>]",
)
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv", "jsonl"]), default="json", help="Output format.")
@click.version_option(__version__, message="version %(version)s")
@click.pass_context
def cli(ctx: click.Context, dsn: str | None, fmt: str) -> None:
    """seekdb-cli — AI-Agent-friendly database CLI."""
    ctx.ensure_object(dict)
    ctx.obj["dsn"] = dsn
    ctx.obj["format"] = fmt

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command("status")
@click.pass_context
def status_cmd(ctx: click.Context) -> None:
    """Show connection status and version info."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    info: dict = {"cli_version": __version__}

    try:
        raw_dsn = resolve_raw_dsn(dsn)
        info["mode"] = "embedded" if is_embedded_dsn(raw_dsn) else "remote"
    except ValueError:
        info["mode"] = "unknown"

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        info["connected"] = False
        info["error"] = str(exc)
        log_operation("status", ok=False, error_code="CONNECTION_ERROR")
        output.success(info, fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            cur = conn.cursor()
            try:
                cur.execute("SELECT VERSION() AS version")
                row = cur.fetchone()
                info["server_version"] = row["version"] if row else "unknown"
                cur.execute("SELECT DATABASE() AS db")
                row = cur.fetchone()
                info["database"] = row["db"] if row else "unknown"
                info["connected"] = True
            finally:
                cur.close()
    except (pymysql.err.Error, RuntimeError) as exc:
        info["connected"] = False
        info["error"] = str(exc)
    finally:
        conn.close()

    log_operation("status", ok=info.get("connected", False), time_ms=timer.elapsed_ms)
    output.success(info, time_ms=timer.elapsed_ms, fmt=fmt)


# ---------------------------------------------------------------------------
# ai-guide — structured self-description for AI Agents
# ---------------------------------------------------------------------------

_AI_GUIDE = {
    "name": "seekdb-cli",
    "version": __version__,
    "description": "AI-Agent-friendly database CLI for seekdb / OceanBase",
    "global_options": {
        "order": "Global options --dsn and --format must appear before the subcommand.",
        "usage_pattern": "seekdb [--dsn DSN] [--format json|table|csv|jsonl] <subcommand> [args]",
        "dsn_formats": {
            "remote": "seekdb://user:pass@host:port/db",
            "embedded": "embedded:<path>[?database=<db>]",
        },
        "examples": [
            "seekdb --format table sql \"SELECT * FROM t LIMIT 5\"",
            "seekdb --dsn \"seekdb://root:@127.0.0.1:2881/test\" status",
            "seekdb --dsn \"embedded:./seekdb.db\" status",
            "seekdb --dsn \"embedded:./data?database=mydb\" sql \"SELECT 1\"",
        ],
    },
    "recommended_workflow": [
        "seekdb schema tables",
        "seekdb schema describe <table>",
        "seekdb table profile <table>",
        "seekdb sql \"SELECT ... LIMIT N\"",
    ],
    "commands": [
        {
            "name": "status",
            "usage": "seekdb status",
            "description": "Show connection status, server version, and database name.",
        },
        {
            "name": "sql",
            "usage": "seekdb sql \"<statement>\" [--write] [--with-schema] [--no-truncate] [--file <path>] [--stdin]",
            "description": "Execute SQL. Read-only by default; add --write for mutations. Row protection auto-enforces LIMIT.",
        },
        {
            "name": "schema tables",
            "usage": "seekdb schema tables",
            "description": "List all tables with column count and row estimate.",
        },
        {
            "name": "schema describe",
            "usage": "seekdb schema describe <table>",
            "description": "Show table columns, types, indexes, and comments.",
        },
        {
            "name": "schema dump",
            "usage": "seekdb schema dump",
            "description": "Output CREATE TABLE DDL for all tables.",
        },
        {
            "name": "table profile",
            "usage": "seekdb table profile <table>",
            "description": "Statistical summary of a table: row count, null ratios, distinct counts, min/max, top values.",
        },
        {
            "name": "relations infer",
            "usage": "seekdb relations infer [--table <table>]",
            "description": "Infer JOIN relationships between tables using column name patterns.",
        },
        {
            "name": "collection list",
            "usage": "seekdb collection list",
            "description": "List all vector collections.",
        },
        {
            "name": "collection create",
            "usage": "seekdb collection create <name> [--dimension <n>] [--distance cosine|l2|ip]",
            "description": "Create a new vector collection.",
        },
        {
            "name": "collection delete",
            "usage": "seekdb collection delete <name>",
            "description": "Delete a vector collection.",
        },
        {
            "name": "collection info",
            "usage": "seekdb collection info <name>",
            "description": "Show collection details: document count and preview.",
        },
        {
            "name": "query",
            "usage": "seekdb query <collection> --text \"<query>\" [--mode semantic|fulltext|hybrid] [--limit <n>] [--where '<json>']",
            "description": "Search a collection using semantic, fulltext, or hybrid mode.",
        },
        {
            "name": "get",
            "usage": "seekdb get <collection> [--ids <id1,id2>] [--limit <n>] [--where '<json>']",
            "description": "Retrieve documents from a collection by IDs or metadata filter.",
        },
        {
            "name": "add",
            "usage": "seekdb add <collection> (--file <path> | --stdin | --data '<json>') [--vectorize-column <col>]",
            "description": "Add data to a collection. Source: file, stdin (JSON/JSONL), or inline JSON.",
        },
        {
            "name": "export",
            "usage": "seekdb export <collection> --output <path> [--limit <n>]",
            "description": "Export collection data to a JSON or JSONL file.",
        },
        {
            "name": "ai model list",
            "usage": "seekdb ai model list",
            "description": "List AI models from database (oceanbase.DBA_OB_AI_MODELS).",
        },
        {
            "name": "ai model create",
            "usage": "seekdb ai model create <name> --type completion|dense_embedding|rerank --model <provider_model_name>",
            "description": "Register an AI model via DBMS_AI_SERVICE.CREATE_AI_MODEL. Create endpoint in DB separately to use it.",
        },
        {
            "name": "ai model delete",
            "usage": "seekdb ai model delete <name>",
            "description": "Drop an AI model via DBMS_AI_SERVICE.DROP_AI_MODEL. Drop endpoints first if any.",
        },
        {
            "name": "ai model endpoint create",
            "usage": "seekdb ai model endpoint create <endpoint_name> <ai_model_name> --url <url> --access-key <key> [--provider siliconflow]",
            "description": "Create an AI model endpoint via DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT.",
        },
        {
            "name": "ai model endpoint delete",
            "usage": "seekdb ai model endpoint delete <endpoint_name>",
            "description": "Drop an AI model endpoint via DBMS_AI_SERVICE.DROP_AI_MODEL_ENDPOINT.",
        },
        {
            "name": "ai complete",
            "usage": "seekdb ai complete \"<prompt>\" --model <name>",
            "description": "Run text completion using database AI_COMPLETE function (requires registered completion model + endpoint).",
        },
        {
            "name": "ai-guide",
            "usage": "seekdb ai-guide",
            "description": "Output this structured guide for AI Agents (JSON).",
        },
    ],
    "output_format": {
        "success": {"ok": True, "data": "...", "time_ms": "N"},
        "error": {"ok": False, "error": {"code": "...", "message": "..."}},
    },
    "safety": {
        "row_protection": "Queries without LIMIT are probed at 101 rows; if exceeded, LIMIT_REQUIRED error is returned.",
        "write_protection": "Write operations require --write flag. DELETE/UPDATE without WHERE and DROP/TRUNCATE are always blocked.",
        "masking": "Sensitive fields (phone, email, password, id_card) are auto-masked in output.",
    },
    "exit_codes": {"0": "success", "1": "business error", "2": "usage error"},
    "tips": {
        "detailed_help": "Run 'seekdb <subcommand> --help' for detailed options. Examples: seekdb sql --help | seekdb schema describe --help | seekdb table profile --help | seekdb ai complete --help | seekdb ai model create --help | seekdb ai model endpoint create --help",
    },
}


@cli.command("ai-guide")
@click.pass_context
def ai_guide_cmd(ctx: click.Context) -> None:
    """Output structured AI Agent usage guide (JSON)."""
    fmt: str = ctx.obj["format"]
    log_operation("ai-guide", ok=True)
    print(json.dumps(_AI_GUIDE, ensure_ascii=False, indent=2))
    raise SystemExit(0)


# ---------------------------------------------------------------------------
# Register all sub-commands
# ---------------------------------------------------------------------------

from seekdb_cli.commands.sql import sql_cmd  # noqa: E402
from seekdb_cli.commands.schema import schema_cmd  # noqa: E402
from seekdb_cli.commands.collection import collection_cmd  # noqa: E402
from seekdb_cli.commands.query import query_cmd, get_cmd  # noqa: E402
from seekdb_cli.commands.data import add_cmd, export_cmd  # noqa: E402
from seekdb_cli.commands.ai import ai_cmd  # noqa: E402
from seekdb_cli.commands.profile import table_cmd  # noqa: E402
from seekdb_cli.commands.relations import relations_cmd  # noqa: E402

cli.add_command(sql_cmd)
cli.add_command(schema_cmd)
cli.add_command(collection_cmd)
cli.add_command(query_cmd)
cli.add_command(get_cmd)
cli.add_command(add_cmd)
cli.add_command(export_cmd)
cli.add_command(ai_cmd)
cli.add_command(table_cmd)
cli.add_command(relations_cmd)
