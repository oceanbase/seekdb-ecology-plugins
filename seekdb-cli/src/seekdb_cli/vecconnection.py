"""pyseekdb client connection management for seekdb-cli vector/collection operations."""

from __future__ import annotations

from typing import Any

from seekdb_cli.connection import resolve_dsn, DSNConfig


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
    """Resolve DSN and return a pyseekdb Client."""
    _check_pyseekdb()
    import pyseekdb

    cfg = resolve_dsn(cli_dsn)
    return pyseekdb.Client(
        host=cfg.host,
        port=cfg.port,
        database=cfg.database,
        user=cfg.user,
        password=cfg.password,
    )
