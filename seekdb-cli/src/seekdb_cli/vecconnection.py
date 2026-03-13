"""pyseekdb client connection management for seekdb-cli vector/collection operations."""

from __future__ import annotations

from typing import Any

from seekdb_cli.connection import (
    resolve_raw_dsn,
    is_embedded_dsn,
    parse_embedded_dsn,
    parse_dsn,
)


def _check_pyseekdb() -> None:
    """Raise ImportError with install instructions if pyseekdb is missing."""
    try:
        import pyseekdb  # noqa: F401
    except ImportError:
        raise ImportError(
            "pyseekdb is required for collection/query operations. "
            "Install it with: pip install pyseekdb"
        )


def get_vec_client(cli_dsn: str | None) -> Any:
    """Resolve DSN and return a pyseekdb Client.

    For remote DSNs, connects via host/port.
    For embedded DSNs, connects via local path.
    """
    _check_pyseekdb()
    import pyseekdb

    raw = resolve_raw_dsn(cli_dsn)

    if is_embedded_dsn(raw):
        cfg = parse_embedded_dsn(raw)
        return pyseekdb.Client(
            path=cfg.path,
            database=cfg.database,
        )

    cfg = parse_dsn(raw)
    return pyseekdb.Client(
        host=cfg.host,
        port=cfg.port,
        database=cfg.database,
        user=cfg.user,
        password=cfg.password,
    )
