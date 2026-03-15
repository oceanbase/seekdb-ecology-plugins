"""DSN parsing and connection management for seekdb-cli.

Supports two connection modes:
  - Remote:   seekdb://user:pass@host:port/db   → pymysql
  - Embedded: embedded:./path[/database]         → pylibseekdb
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote

import pymysql
import pymysql.cursors
import pymysql.err


# ---------------------------------------------------------------------------
# DSN configs
# ---------------------------------------------------------------------------

@dataclass
class DSNConfig:
    host: str = "127.0.0.1"
    port: int = 2881
    user: str = "root"
    password: str = ""
    database: str = "test"


@dataclass
class EmbeddedDSNConfig:
    path: str = "./seekdb.db"
    database: str = "test"


# ---------------------------------------------------------------------------
# DSN parsing
# ---------------------------------------------------------------------------

_DSN_RE = re.compile(
    r"^seekdb://"
    r"(?:(?P<user>[^:@]+)(?::(?P<password>[^@]*))?@)?"
    r"(?P<host>[^:/?]+)"
    r"(?::(?P<port>\d+))?"
    r"(?:/(?P<database>[^?]*))?"
    r"$"
)

_EMBEDDED_RE = re.compile(
    r"^embedded:(?P<path>[^?]+?)(?:\?database=(?P<database>[^&]+))?$"
)


def parse_dsn(dsn: str) -> DSNConfig:
    """Parse ``seekdb://user:pass@host:port/db`` into a DSNConfig."""
    m = _DSN_RE.match(dsn)
    if not m:
        raise ValueError(f"Invalid DSN format: {dsn!r}. Expected: seekdb://user:pass@host:port/db")

    cfg = DSNConfig()
    if m.group("host"):
        cfg.host = m.group("host")
    if m.group("port"):
        cfg.port = int(m.group("port"))
    if m.group("user"):
        cfg.user = unquote(m.group("user"))
    if m.group("password") is not None:
        cfg.password = unquote(m.group("password"))
    if m.group("database"):
        cfg.database = unquote(m.group("database"))
    return cfg


def parse_embedded_dsn(dsn: str) -> EmbeddedDSNConfig:
    """Parse ``embedded:./path[/database]`` into an EmbeddedDSNConfig."""
    m = _EMBEDDED_RE.match(dsn)
    if not m:
        raise ValueError(
            f"Invalid embedded DSN format: {dsn!r}. "
            "Expected: embedded:<path>[?database=<db>]  e.g. embedded:./seekdb.db"
        )
    cfg = EmbeddedDSNConfig()
    cfg.path = m.group("path")
    if m.group("database"):
        cfg.database = m.group("database")
    return cfg


def is_embedded_dsn(dsn: str) -> bool:
    return dsn.startswith("embedded:")


def resolve_dsn(cli_dsn: str | None) -> DSNConfig:
    """Resolve DSN from CLI arg (highest priority) or SEEKDB_DSN env var.

    Only handles remote (seekdb://) DSNs.  For embedded DSNs, callers
    should check ``is_embedded_dsn()`` first.
    """
    raw = cli_dsn or os.environ.get("SEEKDB_DSN")
    if not raw:
        raise ValueError(
            "No connection info. Set SEEKDB_DSN env var or pass --dsn.\n"
            "  Example: export SEEKDB_DSN=\"seekdb://root:pass@127.0.0.1:2881/test\"\n"
            "  Embedded: export SEEKDB_DSN=\"embedded:./seekdb.db\""
        )
    if is_embedded_dsn(raw):
        raise ValueError(
            "resolve_dsn() does not handle embedded DSNs. Use resolve_raw_dsn() instead."
        )
    return parse_dsn(raw)


def resolve_raw_dsn(cli_dsn: str | None) -> str:
    """Return the raw DSN string from CLI arg or env var."""
    raw = cli_dsn or os.environ.get("SEEKDB_DSN")
    if not raw:
        raise ValueError(
            "No connection info. Set SEEKDB_DSN env var or pass --dsn.\n"
            "  Example: export SEEKDB_DSN=\"seekdb://root:pass@127.0.0.1:2881/test\"\n"
            "  Embedded: export SEEKDB_DSN=\"embedded:./seekdb.db\""
        )
    return raw


# ---------------------------------------------------------------------------
# Remote pymysql connection
# ---------------------------------------------------------------------------

def connect(cfg: DSNConfig) -> pymysql.connections.Connection:
    """Open a pymysql connection from a DSNConfig."""
    return pymysql.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        database=cfg.database,
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        connect_timeout=10,
        read_timeout=30,
    )


# ---------------------------------------------------------------------------
# Embedded connection — pylibseekdb adapter
# ---------------------------------------------------------------------------

_SHOW_TABLE_STATUS_COLS = [
    "Name", "Engine", "Version", "Row_format", "Rows",
    "Avg_row_length", "Data_length", "Max_data_length",
    "Index_length", "Data_free", "Auto_increment",
    "Create_time", "Update_time", "Check_time",
    "Collation", "Checksum", "Create_options", "Comment",
]

_SHOW_FULL_COLUMNS_COLS = [
    "Field", "Type", "Collation", "Null", "Key",
    "Default", "Extra", "Privileges", "Comment",
]

_SHOW_COLUMNS_COLS = ["Field", "Type", "Null", "Key", "Default", "Extra"]

_SHOW_INDEX_COLS = [
    "Table", "Non_unique", "Key_name", "Seq_in_index",
    "Column_name", "Collation", "Cardinality", "Sub_part",
    "Packed", "Null", "Index_type", "Comment",
    "Index_comment", "Visible", "Expression",
]

_SHOW_CREATE_TABLE_COLS = ["Table", "Create Table"]

_SHOW_TABLES_COLS = ["Tables_in_db"]


_SELECT_RE_TOP = re.compile(r"^\s*SELECT\b", re.I)
_SHOW_RE = re.compile(r"^\s*SHOW\b", re.I)
_DML_RE = re.compile(
    r"^\s*(INSERT|UPDATE|DELETE|REPLACE|ALTER|CREATE|DROP|TRUNCATE|RENAME|SET)\b",
    re.I,
)

_VIEW_NAME = "__seekdb_cli_colinfo"


def _sql_escape(value: Any) -> str:
    """Escape a Python value for safe SQL interpolation."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def _interpolate_sql(sql: str, args: tuple | list) -> str:
    """Replace ``%s`` placeholders with escaped literal values."""
    parts: list[str] = []
    arg_iter = iter(args)
    i = 0
    while i < len(sql):
        if sql[i] == "%" and i + 1 < len(sql):
            if sql[i + 1] == "s":
                try:
                    parts.append(_sql_escape(next(arg_iter)))
                except StopIteration:
                    raise ValueError("Not enough arguments for SQL placeholders")
                i += 2
                continue
            elif sql[i + 1] == "%":
                parts.append("%")
                i += 2
                continue
        parts.append(sql[i])
        i += 1
    return "".join(parts)


def _is_result_returning(sql: str) -> bool:
    """Return True if the SQL is expected to return a result set."""
    s = sql.strip()
    upper = s.upper()
    if upper.startswith("SELECT") or upper.startswith("SHOW"):
        return True
    if upper.startswith("DESCRIBE") or upper.startswith("DESC "):
        return True
    if upper.startswith("EXPLAIN"):
        return True
    return False


def _determine_show_columns(sql: str, row_width: int) -> list[str]:
    """Return column names for a SHOW command based on pattern matching."""
    upper = sql.strip().upper()

    if "SHOW TABLE STATUS" in upper:
        return _SHOW_TABLE_STATUS_COLS[:row_width]
    if "SHOW FULL COLUMNS" in upper:
        return _SHOW_FULL_COLUMNS_COLS[:row_width]
    if "SHOW COLUMNS" in upper:
        return _SHOW_COLUMNS_COLS[:row_width]
    if "SHOW INDEX" in upper:
        return _SHOW_INDEX_COLS[:row_width]
    if "SHOW CREATE TABLE" in upper:
        return _SHOW_CREATE_TABLE_COLS[:row_width]
    if "SHOW TABLES" in upper:
        return _SHOW_TABLES_COLS[:row_width]
    return [f"col_{i}" for i in range(row_width)]


class EmbeddedCursor:
    """Adapter that gives pylibseekdb cursors a pymysql DictCursor interface.

    Key differences bridged:
      - pylibseekdb returns tuples → we return dicts
      - pylibseekdb has no ``description`` / ``rowcount`` → we synthesize them
      - pylibseekdb execute() takes only raw SQL → we interpolate %s params
    """

    def __init__(self, embedded_conn: "EmbeddedConnection") -> None:
        self._econn = embedded_conn
        self._cursor = embedded_conn._raw_conn.cursor()
        self._columns: list[str] = []
        self._rows: list[tuple] = []
        self._description: tuple | None = None
        self._rowcount: int = 0

    # -- pymysql cursor interface -----------------------------------------

    @property
    def description(self) -> tuple | None:
        return self._description

    @property
    def rowcount(self) -> int:
        return self._rowcount

    def execute(self, sql: str, args: tuple | list | None = None) -> int:
        if args:
            sql = _interpolate_sql(sql, args)

        try:
            rc = self._cursor.execute(sql)
        except RuntimeError as exc:
            raise pymysql.err.ProgrammingError(str(exc)) from exc

        self._rowcount = rc if rc != 0xFFFFFFFFFFFFFFFF else 0

        if _is_result_returning(sql):
            try:
                self._rows = list(self._cursor.fetchall())
            except RuntimeError:
                self._rows = []

            if self._rows:
                row_width = len(self._rows[0])
                self._columns = self._resolve_columns(sql, row_width)
                self._description = tuple(
                    (col, None, None, None, None, None, None)
                    for col in self._columns
                )
            else:
                self._columns = self._resolve_columns_empty(sql)
                self._description = tuple(
                    (col, None, None, None, None, None, None)
                    for col in self._columns
                ) if self._columns else None
        else:
            self._rows = []
            self._columns = []
            self._description = None

        return self._rowcount

    def fetchall(self) -> list[dict[str, Any]]:
        result = [dict(zip(self._columns, row)) for row in self._rows]
        self._rows = []
        return result

    def fetchone(self) -> dict[str, Any] | None:
        if not self._rows:
            return None
        row = self._rows.pop(0)
        return dict(zip(self._columns, row))

    def close(self) -> None:
        try:
            self._cursor.close()
        except Exception:
            pass

    def __enter__(self) -> "EmbeddedCursor":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    # -- Column name resolution -------------------------------------------

    def _resolve_columns(self, sql: str, row_width: int) -> list[str]:
        """Determine column names for a result-returning SQL statement."""
        if _SHOW_RE.match(sql):
            return _determine_show_columns(sql, row_width)

        cols = self._columns_via_view(sql, row_width)
        if cols:
            return cols

        return [f"col_{i}" for i in range(row_width)]

    def _resolve_columns_empty(self, sql: str) -> list[str]:
        if _SHOW_RE.match(sql):
            return _determine_show_columns(sql, 0)
        return self._columns_via_view(sql, 0) or []

    def _columns_via_view(self, sql: str, expected_width: int) -> list[str] | None:
        """Create a temporary view to extract column names from a SELECT."""
        try:
            clean_sql = sql.rstrip().rstrip(";")
            self._cursor.execute(f"DROP VIEW IF EXISTS `{_VIEW_NAME}`")
            self._cursor.execute(f"CREATE VIEW `{_VIEW_NAME}` AS {clean_sql}")
            self._cursor.execute(f"SHOW COLUMNS FROM `{_VIEW_NAME}`")
            col_rows = self._cursor.fetchall()
            self._cursor.execute(f"DROP VIEW IF EXISTS `{_VIEW_NAME}`")
            cols = [row[0] for row in col_rows]
            if expected_width and len(cols) != expected_width:
                return None
            return cols
        except (RuntimeError, Exception):
            try:
                self._cursor.execute(f"DROP VIEW IF EXISTS `{_VIEW_NAME}`")
            except Exception:
                pass
            return None


class EmbeddedConnection:
    """Adapter wrapping pylibseekdb to provide a pymysql-compatible interface.

    Usage is identical to pymysql::

        conn = EmbeddedConnection("./seekdb.db", "test")
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS val")
            rows = cur.fetchall()   # [{"val": 1}]
        conn.close()
    """

    def __init__(self, path: str, database: str = "test") -> None:
        try:
            import pylibseekdb
        except ImportError:
            raise ImportError(
                "pylibseekdb is required for embedded mode. "
                "Install it with: pip install pyseekdb   (Linux only)"
            )

        abs_path = os.path.abspath(path)
        os.makedirs(abs_path, exist_ok=True)

        try:
            pylibseekdb.open(db_dir=abs_path)
        except RuntimeError as exc:
            if "initialized twice" not in str(exc):
                raise

        self._raw_conn = pylibseekdb.connect(database=database, autocommit=True)
        self._database = database
        self._path = abs_path

    def cursor(self) -> EmbeddedCursor:
        return EmbeddedCursor(self)

    def commit(self) -> None:
        self._raw_conn.commit()

    def rollback(self) -> None:
        self._raw_conn.rollback()

    def close(self) -> None:
        try:
            self._raw_conn.close()
        except Exception:
            pass

    @property
    def open(self) -> bool:
        return True


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

def get_connection(cli_dsn: str | None) -> Any:
    """Resolve DSN and return an open connection.

    Returns a ``pymysql.Connection`` for remote DSNs or an
    ``EmbeddedConnection`` for ``embedded:`` DSNs.  Both expose the same
    cursor interface (DictCursor-compatible).
    """
    raw = resolve_raw_dsn(cli_dsn)

    if is_embedded_dsn(raw):
        cfg = parse_embedded_dsn(raw)
        return EmbeddedConnection(cfg.path, cfg.database)

    cfg = parse_dsn(raw)
    return connect(cfg)
