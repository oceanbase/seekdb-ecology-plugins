"""seekdb-cli — AI-Agent-friendly database CLI for seekdb / OceanBase."""

from __future__ import annotations

import json

import click
import pymysql

from seekdb_cli import __version__, output
from seekdb_cli.connection import get_connection
from seekdb_cli.logger import log_operation


@click.group(invoke_without_command=True)
@click.option("--dsn", envvar="SEEKDB_DSN", default=None, help="Connection string (seekdb://user:pass@host:port/db).")
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

    info = {"cli_version": __version__}

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
        with timer, conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS version")
            row = cur.fetchone()
            info["server_version"] = row["version"] if row else "unknown"
            cur.execute("SELECT DATABASE() AS db")
            row = cur.fetchone()
            info["database"] = row["db"] if row else "unknown"
            info["connected"] = True
    except pymysql.err.Error as exc:
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
        "examples": [
            "seekdb --format table sql \"SELECT * FROM t LIMIT 5\"",
            "seekdb --dsn \"seekdb://root:@127.0.0.1:2881/test\" status",
            "seekdb --dsn \"...\" --format csv sql \"SELECT id, name FROM users LIMIT 10\"",
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
            "name": "import",
            "usage": "seekdb import <collection> --file <path> [--vectorize-column <col>]",
            "description": "Import data into a collection from a JSON/JSONL/CSV file.",
        },
        {
            "name": "export",
            "usage": "seekdb export <collection> --output <path> [--limit <n>]",
            "description": "Export collection data to a JSON or JSONL file.",
        },
        {
            "name": "ai model list",
            "usage": "seekdb ai model list",
            "description": "List all registered AI models.",
        },
        {
            "name": "ai model create",
            "usage": "seekdb ai model create <name> --provider <provider> --model <model> [--api-key <key>] [--base-url <url>]",
            "description": "Register a new AI model (openai, ollama, qwen, etc.).",
        },
        {
            "name": "ai model delete",
            "usage": "seekdb ai model delete <name>",
            "description": "Delete a registered AI model.",
        },
        {
            "name": "ai complete",
            "usage": "seekdb ai complete \"<prompt>\" --model <name>",
            "description": "Run a text completion using a registered AI model.",
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
from seekdb_cli.commands.data import import_cmd, export_cmd  # noqa: E402
from seekdb_cli.commands.ai import ai_cmd  # noqa: E402
from seekdb_cli.commands.profile import table_cmd  # noqa: E402
from seekdb_cli.commands.relations import relations_cmd  # noqa: E402

cli.add_command(sql_cmd)
cli.add_command(schema_cmd)
cli.add_command(collection_cmd)
cli.add_command(query_cmd)
cli.add_command(get_cmd)
cli.add_command(import_cmd)
cli.add_command(export_cmd)
cli.add_command(ai_cmd)
cli.add_command(table_cmd)
cli.add_command(relations_cmd)
