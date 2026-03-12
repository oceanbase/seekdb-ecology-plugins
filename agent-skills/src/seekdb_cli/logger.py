"""Operation logging to ~/.seekdb/history.jsonl."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_LOG_DIR = Path.home() / ".seekdb"
_LOG_FILE = _LOG_DIR / "history.jsonl"


def log_operation(
    command: str,
    *,
    sql: str | None = None,
    ok: bool = True,
    rows: int | None = None,
    affected: int | None = None,
    time_ms: int = 0,
    error_code: str | None = None,
) -> None:
    """Append one JSONL entry to the history log. Failures are silently ignored."""
    entry: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "command": command,
    }
    if sql is not None:
        entry["sql"] = sql
    entry["ok"] = ok
    if rows is not None:
        entry["rows"] = rows
    if affected is not None:
        entry["affected"] = affected
    if time_ms:
        entry["time_ms"] = time_ms
    if error_code:
        entry["error_code"] = error_code

    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass
