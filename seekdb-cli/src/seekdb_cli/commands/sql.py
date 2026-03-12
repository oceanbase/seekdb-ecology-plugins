"""seekdb sql command — execute SQL with safety guardrails."""

from __future__ import annotations

import re
import sys
from typing import Any

import click
import pymysql

from seekdb_cli import output
from seekdb_cli.connection import get_connection
from seekdb_cli.logger import log_operation
from seekdb_cli.masking import mask_rows

_LARGE_FIELD_TYPES = frozenset({
    pymysql.constants.FIELD_TYPE.BLOB,
    pymysql.constants.FIELD_TYPE.LONG_BLOB,
    pymysql.constants.FIELD_TYPE.MEDIUM_BLOB,
    pymysql.constants.FIELD_TYPE.TINY_BLOB,
    pymysql.constants.FIELD_TYPE.VAR_STRING,
    pymysql.constants.FIELD_TYPE.STRING,
})

_WRITE_RE = re.compile(
    r"^\s*(INSERT|UPDATE|DELETE|REPLACE|ALTER|CREATE|DROP|TRUNCATE|RENAME)\b",
    re.I,
)
_SELECT_RE = re.compile(r"^\s*SELECT\b", re.I)
_LIMIT_RE = re.compile(r"\bLIMIT\s+\d+", re.I)
_DANGEROUS_DELETE_RE = re.compile(
    r"^\s*DELETE\s+FROM\s+\S+\s*$", re.I
)
_DANGEROUS_UPDATE_RE = re.compile(
    r"^\s*UPDATE\s+\S+\s+SET\s+.+$", re.I
)
_DROP_TRUNCATE_RE = re.compile(r"^\s*(DROP|TRUNCATE)\b", re.I)

_TABLE_NOT_FOUND_RE = re.compile(r"Table '.*?\.(\w+)' doesn't exist", re.I)
_COLUMN_NOT_FOUND_RE = re.compile(r"Unknown column '(\w+)'", re.I)
_TABLE_FROM_SQL_RE = re.compile(
    r"\b(?:FROM|INTO|UPDATE|TABLE)\s+`?(\w+)`?", re.I
)

ROW_PROBE_LIMIT = 101
DEFAULT_TRUNCATE_LEN = 200


def _is_write(sql: str) -> bool:
    return bool(_WRITE_RE.match(sql))


def _is_select(sql: str) -> bool:
    return bool(_SELECT_RE.match(sql))


def _has_limit(sql: str) -> bool:
    return bool(_LIMIT_RE.search(sql))


def _has_where(sql: str) -> bool:
    return bool(re.search(r"\bWHERE\b", sql, re.I))


def _check_dangerous_write(sql: str, fmt: str) -> None:
    """Reject DELETE/UPDATE without WHERE, and DROP/TRUNCATE entirely."""
    if _DROP_TRUNCATE_RE.match(sql):
        output.error(
            "DANGEROUS_WRITE",
            "DROP/TRUNCATE operations are not allowed.",
            fmt=fmt,
        )
    stripped = sql.strip().rstrip(";")
    if re.match(r"^\s*DELETE\b", stripped, re.I) and not _has_where(stripped):
        output.error(
            "DANGEROUS_WRITE",
            "DELETE without WHERE clause is not allowed.",
            fmt=fmt,
        )
    if re.match(r"^\s*UPDATE\b", stripped, re.I) and not _has_where(stripped):
        output.error(
            "DANGEROUS_WRITE",
            "UPDATE without WHERE clause is not allowed.",
            fmt=fmt,
        )


def _truncate_large_fields(
    rows: list[dict[str, Any]],
    description: tuple,
    max_len: int,
) -> list[dict[str, Any]]:
    """Truncate TEXT/BLOB columns exceeding max_len characters."""
    large_cols: set[str] = set()
    for desc in description:
        col_name = desc[0]
        col_type = desc[1]
        if col_type in _LARGE_FIELD_TYPES:
            large_cols.add(col_name)

    if not large_cols:
        return rows

    for row in rows:
        for col in large_cols:
            val = row.get(col)
            if isinstance(val, (str, bytes)):
                s = val if isinstance(val, str) else val.decode("utf-8", errors="replace")
                if len(s) > max_len:
                    row[col] = s[:max_len] + f"...(truncated, {len(s)} chars)"
    return rows


def _extract_tables_from_sql(sql: str) -> list[str]:
    return _TABLE_FROM_SQL_RE.findall(sql)


def _fetch_error_schema(
    conn: pymysql.connections.Connection,
    error_msg: str,
    sql: str,
) -> dict[str, Any] | None:
    """Build a schema hint dict based on the SQL error type."""
    try:
        table_match = _TABLE_NOT_FOUND_RE.search(error_msg)
        if table_match:
            with conn.cursor() as cur:
                cur.execute("SHOW TABLES")
                tables = [list(r.values())[0] for r in cur.fetchall()]
            return {"tables": tables}

        col_match = _COLUMN_NOT_FOUND_RE.search(error_msg)
        if col_match:
            table_names = _extract_tables_from_sql(sql)
            if table_names:
                table = table_names[0]
                with conn.cursor() as cur:
                    cur.execute(f"SHOW FULL COLUMNS FROM `{table}`")
                    cols = [r["Field"] for r in cur.fetchall()]
                    cur.execute(f"SHOW INDEX FROM `{table}`")
                    indexes = []
                    seen: set[str] = set()
                    for idx in cur.fetchall():
                        key = idx["Key_name"]
                        if key not in seen:
                            seen.add(key)
                            indexes.append(f"{key}({idx['Column_name']})")
                return {"table": table, "columns": cols, "indexes": indexes}
    except Exception:
        pass
    return None


def _fetch_table_schema(
    conn: pymysql.connections.Connection,
    table: str,
) -> dict[str, Any] | None:
    """Fetch schema for --with-schema."""
    try:
        with conn.cursor() as cur:
            cur.execute(f"SHOW FULL COLUMNS FROM `{table}`")
            columns = [
                {"name": r["Field"], "type": r["Type"], "comment": r.get("Comment", "")}
                for r in cur.fetchall()
            ]
            cur.execute(f"SHOW INDEX FROM `{table}`")
            indexes = []
            seen: set[str] = set()
            for idx in cur.fetchall():
                key = idx["Key_name"]
                if key not in seen:
                    seen.add(key)
                    indexes.append(f"{key}({idx['Column_name']})")
        return {"table": table, "columns": columns, "indexes": indexes}
    except Exception:
        return None


@click.command("sql")
@click.argument("statement", required=False)
@click.option("--write", is_flag=True, help="Allow write operations (INSERT/UPDATE/DELETE).")
@click.option("--with-schema", is_flag=True, help="Include related table schema in output.")
@click.option("--no-truncate", is_flag=True, help="Do not truncate large fields.")
@click.option("--file", "sql_file", type=click.Path(exists=True), help="Read SQL from file.")
@click.option("--stdin", "use_stdin", is_flag=True, help="Read SQL from stdin.")
@click.pass_context
def sql_cmd(
    ctx: click.Context,
    statement: str | None,
    write: bool,
    with_schema: bool,
    no_truncate: bool,
    sql_file: str | None,
    use_stdin: bool,
) -> None:
    """Execute a SQL statement."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    sql_text = _resolve_sql(statement, sql_file, use_stdin, fmt)

    if _is_write(sql_text) and not write:
        log_operation("sql", sql=sql_text, ok=False, error_code="WRITE_NOT_ALLOWED")
        output.error(
            "WRITE_NOT_ALLOWED",
            "Write operations require --write flag.",
            fmt=fmt,
        )

    if write and _is_write(sql_text):
        _check_dangerous_write(sql_text, fmt)

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("sql", sql=sql_text, ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return  # unreachable, output.error calls sys.exit

    timer = output.Timer()
    try:
        with timer:
            _execute(conn, sql_text, fmt, no_truncate, with_schema, timer)
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("sql", sql=sql_text, ok=False, error_code="INTERNAL_ERROR")
        output.error("INTERNAL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


def _resolve_sql(
    statement: str | None,
    sql_file: str | None,
    use_stdin: bool,
    fmt: str,
) -> str:
    if sql_file:
        with open(sql_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    if use_stdin:
        return sys.stdin.read().strip()
    if statement:
        return statement.strip()
    output.error(
        "MISSING_SQL",
        "No SQL provided. Pass a statement, --file, or --stdin.",
        fmt=fmt,
        exit_code=output.EXIT_USAGE_ERROR,
    )
    return ""  # unreachable


def _execute(
    conn: pymysql.connections.Connection,
    sql_text: str,
    fmt: str,
    no_truncate: bool,
    with_schema: bool,
    timer: output.Timer,
) -> None:
    is_select = _is_select(sql_text)
    needs_probe = is_select and not _has_limit(sql_text)

    exec_sql = sql_text
    if needs_probe:
        exec_sql = sql_text.rstrip(";") + f" LIMIT {ROW_PROBE_LIMIT}"

    try:
        with conn.cursor() as cur:
            cur.execute(exec_sql)

            if is_select:
                rows_raw = cur.fetchall()
                description = cur.description or ()

                if needs_probe and len(rows_raw) > ROW_PROBE_LIMIT - 1:
                    tables = _extract_tables_from_sql(sql_text)
                    extra: dict[str, Any] = {}
                    if tables:
                        schema = _fetch_table_schema(conn, tables[0])
                        if schema:
                            extra["schema"] = schema
                    log_operation(
                        "sql", sql=sql_text, ok=False, error_code="LIMIT_REQUIRED",
                        time_ms=timer.elapsed_ms,
                    )
                    output.error(
                        "LIMIT_REQUIRED",
                        "Query returns more than 100 rows. Please add LIMIT to your SQL.",
                        fmt=fmt,
                        extra=extra or None,
                    )

                columns = [d[0] for d in description]
                rows = list(rows_raw)

                if not no_truncate and description:
                    rows = _truncate_large_fields(rows, description, DEFAULT_TRUNCATE_LEN)

                rows = mask_rows(columns, rows)

                extra_out: dict[str, Any] = {}
                if with_schema:
                    tables = _extract_tables_from_sql(sql_text)
                    if tables:
                        schema = _fetch_table_schema(conn, tables[0])
                        if schema:
                            extra_out["schema"] = schema

                log_operation(
                    "sql", sql=sql_text, ok=True, rows=len(rows),
                    time_ms=timer.elapsed_ms,
                )
                output.success_rows(
                    columns, rows,
                    time_ms=timer.elapsed_ms,
                    fmt=fmt,
                    extra=extra_out or None,
                )
            else:
                conn.commit()
                affected = cur.rowcount
                log_operation(
                    "sql", sql=sql_text, ok=True, affected=affected,
                    time_ms=timer.elapsed_ms,
                )
                output.success(
                    {"affected": affected},
                    time_ms=timer.elapsed_ms,
                    fmt=fmt,
                )

    except pymysql.err.ProgrammingError as exc:
        err_msg = str(exc)
        schema_hint = _fetch_error_schema(conn, err_msg, sql_text)
        extra_err: dict[str, Any] = {}
        if schema_hint:
            extra_err["schema"] = schema_hint
        log_operation(
            "sql", sql=sql_text, ok=False, error_code="SQL_ERROR",
            time_ms=timer.elapsed_ms,
        )
        output.error("SQL_ERROR", err_msg, fmt=fmt, extra=extra_err or None)

    except pymysql.err.OperationalError as exc:
        err_msg = str(exc)
        schema_hint = _fetch_error_schema(conn, err_msg, sql_text)
        extra_err = {}
        if schema_hint:
            extra_err["schema"] = schema_hint
        log_operation(
            "sql", sql=sql_text, ok=False, error_code="SQL_ERROR",
            time_ms=timer.elapsed_ms,
        )
        output.error("SQL_ERROR", err_msg, fmt=fmt, extra=extra_err or None)
