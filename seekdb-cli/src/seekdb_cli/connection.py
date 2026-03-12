"""DSN parsing and pymysql connection management for seekdb-cli."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote

import pymysql
import pymysql.cursors


@dataclass
class DSNConfig:
    host: str = "127.0.0.1"
    port: int = 2881
    user: str = "root"
    password: str = ""
    database: str = "test"


_DSN_RE = re.compile(
    r"^seekdb://"
    r"(?:(?P<user>[^:@]+)(?::(?P<password>[^@]*))?@)?"
    r"(?P<host>[^:/?]+)"
    r"(?::(?P<port>\d+))?"
    r"(?:/(?P<database>[^?]*))?"
    r"$"
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


def resolve_dsn(cli_dsn: str | None) -> DSNConfig:
    """Resolve DSN from CLI arg (highest priority) or SEEKDB_DSN env var."""
    raw = cli_dsn or os.environ.get("SEEKDB_DSN")
    if not raw:
        raise ValueError(
            "No connection info. Set SEEKDB_DSN env var or pass --dsn.\n"
            "  Example: export SEEKDB_DSN=\"seekdb://root:pass@127.0.0.1:2881/test\""
        )
    return parse_dsn(raw)


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


def get_connection(cli_dsn: str | None) -> pymysql.connections.Connection:
    """Resolve DSN and return an open connection."""
    cfg = resolve_dsn(cli_dsn)
    return connect(cfg)
