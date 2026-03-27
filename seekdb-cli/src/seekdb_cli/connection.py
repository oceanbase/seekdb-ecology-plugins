"""DSN parsing and connection management for seekdb-cli.

Supports two connection modes:
  - Remote:   seekdb://user:pass@host:port/db   → pymysql
  - Embedded: embedded:./path[/database]         → pylibseekdb

Remote DSNs: if the username contains ``@`` (e.g. ``u@sys``), use
``seekdb://u@sys:password@host:port/db``.  The parser takes the *rightmost*
``@`` whose suffix is ``host[:port]``, then splits the credential prefix on
the *first* ``:`` into user and password.  Usernames containing ``:`` must
still be percent-encoded.

TLS for remote DSNs: append a query string, e.g.
``seekdb://user:pass@host:2881/db?tls=skip-verify`` or ``?sslmode=REQUIRED``.
See ``_parse_seekdb_ssl_query``.
"""

from __future__ import annotations

import os
import re
import ssl as ssl_module
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl, unquote

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
    # TLS: ssl_mode None = plain TCP (default). See _normalize_seekdb_ssl_mode.
    ssl_mode: str | None = None
    ssl_ca: str | None = None
    ssl_cert: str | None = None
    ssl_key: str | None = None
    ssl_key_password: str | None = None


@dataclass
class EmbeddedDSNConfig:
    path: str = "./seekdb.db"
    database: str = "test"


# ---------------------------------------------------------------------------
# DSN parsing
# ---------------------------------------------------------------------------

# Tail after the last "@" that separates credentials from host must look like host[:port].
_SEEKDB_HOST_PORT_RE = re.compile(r"^(?P<host>[^@/:]+)(?::(?P<port>\d+))?$")

_EMBEDDED_RE = re.compile(
    r"^embedded:(?P<path>[^?]+?)(?:\?database=(?P<database>[^&]+))?$"
)


def _parse_seekdb_remote_body(body: str) -> DSNConfig | None:
    """Parse ``[user[:password]@]host[:port][/database]`` (no scheme, no ``?``)."""
    database = ""
    if "/" in body:
        slash = body.index("/")
        database = unquote(body[slash + 1 :])
        body = body[:slash]

    cfg = DSNConfig()
    if database:
        cfg.database = database

    def apply_host_port(hostpart: str) -> bool:
        m = _SEEKDB_HOST_PORT_RE.match(hostpart)
        if not m:
            return False
        cfg.host = m.group("host")
        if m.group("port"):
            cfg.port = int(m.group("port"))
        return True

    if "@" not in body:
        if not apply_host_port(body):
            return None
        return cfg

    for at_idx in range(len(body) - 1, -1, -1):
        if body[at_idx] != "@":
            continue
        userinfo, hostpart = body[:at_idx], body[at_idx + 1 :]
        if not apply_host_port(hostpart):
            continue
        if ":" in userinfo:
            c = userinfo.index(":")
            cfg.user = unquote(userinfo[:c])
            cfg.password = unquote(userinfo[c + 1 :])
        else:
            cfg.user = unquote(userinfo)
        return cfg

    return None


def _parse_seekdb_ssl_query(query: str, cfg: DSNConfig) -> None:
    """Apply ``?tls=...`` / ``?sslmode=...`` / PEM paths from a DSN query string."""
    if not query.strip():
        return
    merged: dict[str, str] = {}
    for k, v in parse_qsl(query, keep_blank_values=False, strict_parsing=False):
        merged[k.lower()] = unquote(v)

    def take(*names: str) -> str | None:
        for n in names:
            if n in merged and merged[n].strip() != "":
                return merged[n].strip()
        return None

    mode = take("tls", "sslmode", "ssl_mode")
    if mode is not None:
        cfg.ssl_mode = _normalize_seekdb_ssl_mode(mode)
    ca = take("ssl_ca")
    if ca is not None:
        cfg.ssl_ca = ca
    cert = take("ssl_cert")
    if cert is not None:
        cfg.ssl_cert = cert
    key = take("ssl_key")
    if key is not None:
        cfg.ssl_key = key
    kpw = take("ssl_key_password", "ssl-key-password")
    if kpw is not None:
        cfg.ssl_key_password = kpw


def _normalize_seekdb_ssl_mode(raw: str) -> str | None:
    """Return internal mode label or None if TLS is disabled."""
    s = raw.strip().lower().replace("_", "-")
    if s in ("", "disabled", "off", "false", "0", "no"):
        return None
    if s in ("skip-verify", "skipverify", "insecure"):
        return "skip_verify"
    if s in ("required", "require", "true", "1", "on", "yes", "preferred"):
        return "required"
    if s in ("verify-ca", "verifyca"):
        return "verify_ca"
    if s in ("verify-identity", "verifyidentity"):
        return "verify_identity"
    raise ValueError(
        f"Invalid tls / sslmode value: {raw!r}. "
        "Use: disabled, required, skip-verify, verify-ca, verify-identity "
        "(or MySQL-style DISABLED, REQUIRED, VERIFY_CA, VERIFY_IDENTITY)."
    )


def pymysql_ssl_kwargs(cfg: DSNConfig) -> dict[str, Any]:
    """Keyword arguments for ``pymysql.connect`` TLS (``ssl``, ``ssl_ca``, …)."""
    mode = (cfg.ssl_mode or "").strip().lower() if cfg.ssl_mode else None
    out: dict[str, Any] = {}

    if cfg.ssl_ca:
        out["ssl_ca"] = cfg.ssl_ca
    if cfg.ssl_cert:
        out["ssl_cert"] = cfg.ssl_cert
    if cfg.ssl_key:
        out["ssl_key"] = cfg.ssl_key
    if cfg.ssl_key_password:
        out["ssl_key_password"] = cfg.ssl_key_password

    # PEM-based TLS (pymysql enables SSL when ssl_ca/ssl_cert/ssl_key are set).
    if out.get("ssl_ca") or out.get("ssl_cert") or out.get("ssl_key"):
        if mode == "skip_verify":
            out["ssl_verify_cert"] = False
            out["ssl_verify_identity"] = False
        elif mode == "verify_identity":
            out["ssl_verify_identity"] = True
        elif mode == "verify_ca":
            out["ssl_verify_cert"] = True
        return out

    if not mode or mode == "disabled":
        return {}

    if mode == "skip_verify":
        ctx = ssl_module.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl_module.CERT_NONE
        return {"ssl": ctx}

    if mode == "required":
        return {"ssl": ssl_module.create_default_context()}

    if mode == "verify_ca":
        ctx = ssl_module.create_default_context()
        return {"ssl": ctx}

    if mode == "verify_identity":
        ctx = ssl_module.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl_module.CERT_REQUIRED
        return {"ssl": ctx}

    return {}


def _parse_seekdb_remote_dsn(dsn: str) -> DSNConfig | None:
    """Parse ``seekdb://[user[:password]@]host[:port][/database][?query]``.

    The ``@`` before *host* may be ambiguous when the username contains ``@``
    (e.g. ``u@sys:secret@10.0.0.1:2881/db``).  We pick the **rightmost** ``@``
    whose suffix matches ``host:port``; credentials are the prefix, split on
    the **first** ``:`` into user and password (password may contain ``:`` and
    ``@``).  Usernames containing an unencoded ``:`` are not supported.
    """
    prefix = "seekdb://"
    if not dsn.startswith(prefix):
        return None
    rest = dsn[len(prefix) :]
    query = ""
    if "?" in rest:
        main_part, query = rest.split("?", 1)
    else:
        main_part = rest

    cfg = _parse_seekdb_remote_body(main_part)
    if cfg is None:
        return None
    _parse_seekdb_ssl_query(query, cfg)
    return cfg


def parse_dsn(dsn: str) -> DSNConfig:
    """Parse ``seekdb://user:pass@host:port/db`` into a DSNConfig."""
    cfg = _parse_seekdb_remote_dsn(dsn)
    if cfg is None:
        hint = ""
        if not dsn.startswith("embedded:") and not dsn.startswith("seekdb://"):
            if dsn.startswith("/") or dsn.startswith("./") or ".db" in dsn:
                hint = f" For a local DB file use: embedded:{dsn}"
        raise ValueError(
            f"Invalid DSN format: {dsn!r}. "
            "Remote: seekdb://user:pass@host:port/db ; "
            f"Embedded: embedded:<path>[?database=<db>] e.g. embedded:~/.seekdb/seekdb.db.{hint}"
        )
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
    cfg.path = os.path.expanduser(m.group("path"))
    if m.group("database"):
        cfg.database = m.group("database")
    return cfg


def is_embedded_dsn(dsn: str) -> bool:
    return dsn.startswith("embedded:")


def resolve_dsn(cli_dsn: str | None) -> DSNConfig:
    """Resolve DSN from CLI arg, env var, or config files.

    Only handles remote (seekdb://) DSNs.  For embedded DSNs, callers
    should check ``is_embedded_dsn()`` first.
    """
    raw = resolve_raw_dsn(cli_dsn)
    if is_embedded_dsn(raw):
        raise ValueError(
            "resolve_dsn() does not handle embedded DSNs. Use resolve_raw_dsn() instead."
        )
    return parse_dsn(raw)


def _resolve_embedded_path(dsn: str, base_dir: str) -> str:
    """Resolve relative embedded paths to absolute, relative to *base_dir*."""
    if not is_embedded_dsn(dsn):
        return dsn
    m = _EMBEDDED_RE.match(dsn)
    if not m:
        return dsn
    path = os.path.expanduser(m.group("path"))
    if os.path.isabs(path):
        return f"embedded:{path}" + (f"?database={m.group('database')}" if m.group("database") else "")
    abs_path = os.path.normpath(os.path.join(base_dir, path))
    result = f"embedded:{abs_path}"
    if m.group("database"):
        result += f"?database={m.group('database')}"
    return result


def _read_dsn_from_env_file(filepath: str) -> str | None:
    """Extract SEEKDB_DSN value from a .env-style file."""
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("SEEKDB_DSN="):
                    val = line[len("SEEKDB_DSN="):]
                    return val.strip().strip("\"'")
    except OSError:
        pass
    return None


def _discover_dsn() -> str | None:
    """Auto-discover DSN from config files.

    Search order:
      1. .env            in cwd   (SEEKDB_DSN=... line)
      2. ~/.seekdb/config          (SEEKDB_DSN=... line)
    Relative embedded paths are resolved relative to the config file's
    directory so the DSN works from any working directory.
    """
    cwd = os.getcwd()

    env_file = os.path.join(cwd, ".env")
    dsn = _read_dsn_from_env_file(env_file)
    if dsn:
        return _resolve_embedded_path(dsn, cwd)

    config_file = os.path.expanduser("~/.seekdb/config.env")
    dsn = _read_dsn_from_env_file(config_file)
    if dsn:
        return _resolve_embedded_path(dsn, os.path.dirname(config_file))

    return None


_DEFAULT_EMBEDDED_DSN = "embedded:" + os.path.join(
    os.path.expanduser("~"), ".seekdb", "seekdb.db"
)


def resolve_raw_dsn(cli_dsn: str | None) -> str:
    """Return the raw DSN string.

    Resolution order:
      1. ``--dsn`` CLI argument
      2. ``SEEKDB_DSN`` environment variable
      3. Auto-discover from config files (see ``_discover_dsn``)
      4. Default embedded database at ``~/.seekdb/seekdb.db``
    """
    return (
        cli_dsn
        or os.environ.get("SEEKDB_DSN")
        or _discover_dsn()
        or _DEFAULT_EMBEDDED_DSN
    )


# ---------------------------------------------------------------------------
# Remote pymysql connection
# ---------------------------------------------------------------------------

def connect(cfg: DSNConfig) -> pymysql.connections.Connection:
    """Open a pymysql connection from a DSNConfig."""
    kw: dict[str, Any] = {
        "host": cfg.host,
        "port": cfg.port,
        "user": cfg.user,
        "password": cfg.password,
        "database": cfg.database,
        "cursorclass": pymysql.cursors.DictCursor,
        "charset": "utf8mb4",
        "connect_timeout": 10,
        "read_timeout": 30,
    }
    kw.update(pymysql_ssl_kwargs(cfg))
    return pymysql.connect(**kw)


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
                "Embedded mode is only supported on Linux (glibc >= 2.28) and macOS 15+. "
                "On other systems, please use Server Mode instead: "
                "deploy seekdb via Docker or OceanBase Desktop, then connect with "
                "--dsn seekdb://user:pass@host:port/db"
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
