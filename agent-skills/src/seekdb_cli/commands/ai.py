"""seekdb ai command — manage AI models and run completions."""

from __future__ import annotations

from typing import Any

import click
import pymysql

from seekdb_cli import output
from seekdb_cli.connection import get_connection
from seekdb_cli.logger import log_operation


@click.group("ai")
@click.pass_context
def ai_cmd(ctx: click.Context) -> None:
    """AI model management and completion."""


# ---------------------------------------------------------------------------
# seekdb ai model ...
# ---------------------------------------------------------------------------

@ai_cmd.group("model")
@click.pass_context
def model_group(ctx: click.Context) -> None:
    """Manage AI models registered in seekdb."""


@model_group.command("list")
@click.pass_context
def model_list(ctx: click.Context) -> None:
    """List all registered AI models."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model list", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "SELECT model_name, provider, model, created_at "
                "FROM __seekdb_ai_models ORDER BY created_at"
            )
            rows = cur.fetchall()
            result = [
                {
                    "name": r["model_name"],
                    "provider": r["provider"],
                    "model": r["model"],
                    "created_at": str(r.get("created_at", "")),
                }
                for r in rows
            ]

        log_operation("ai model list", ok=True, time_ms=timer.elapsed_ms)
        output.success(result, time_ms=timer.elapsed_ms, fmt=fmt)
    except pymysql.err.ProgrammingError:
        log_operation("ai model list", ok=True, time_ms=timer.elapsed_ms)
        output.success([], time_ms=timer.elapsed_ms, fmt=fmt)
    except pymysql.err.Error as exc:
        log_operation("ai model list", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


@model_group.command("create")
@click.argument("name")
@click.option("--provider", required=True, help="Model provider (openai, ollama, qwen, etc.).")
@click.option("--model", "model_id", required=True, help="Model identifier at the provider.")
@click.option("--api-key", default=None, help="API key (stored encrypted). Can also use SEEKDB_AI_API_KEY env var.")
@click.option("--base-url", default=None, help="Custom API base URL.")
@click.pass_context
def model_create(
    ctx: click.Context,
    name: str,
    provider: str,
    model_id: str,
    api_key: str | None,
    base_url: str | None,
) -> None:
    """Register a new AI model."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model create", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS __seekdb_ai_models ("
                "  model_name VARCHAR(128) PRIMARY KEY,"
                "  provider VARCHAR(64) NOT NULL,"
                "  model VARCHAR(128) NOT NULL,"
                "  api_key VARCHAR(512) DEFAULT '',"
                "  base_url VARCHAR(512) DEFAULT '',"
                "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
                ")"
            )
            cur.execute(
                "REPLACE INTO __seekdb_ai_models (model_name, provider, model, api_key, base_url) "
                "VALUES (%s, %s, %s, %s, %s)",
                (name, provider, model_id, api_key or "", base_url or ""),
            )
            conn.commit()

        log_operation("ai model create", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"name": name, "provider": provider, "model": model_id},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except pymysql.err.Error as exc:
        log_operation("ai model create", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


@model_group.command("delete")
@click.argument("name")
@click.pass_context
def model_delete(ctx: click.Context, name: str) -> None:
    """Delete a registered AI model."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model delete", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM __seekdb_ai_models WHERE model_name = %s", (name,)
            )
            conn.commit()
            if cur.rowcount == 0:
                log_operation("ai model delete", ok=False, error_code="MODEL_NOT_FOUND")
                output.error("MODEL_NOT_FOUND", f"Model '{name}' does not exist", fmt=fmt)
                return

        log_operation("ai model delete", ok=True, time_ms=timer.elapsed_ms)
        output.success({"deleted": name}, time_ms=timer.elapsed_ms, fmt=fmt)
    except SystemExit:
        raise
    except pymysql.err.Error as exc:
        log_operation("ai model delete", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# seekdb ai complete ...
# ---------------------------------------------------------------------------

@ai_cmd.command("complete")
@click.argument("prompt")
@click.option("--model", "model_name", required=True, help="Registered model name.")
@click.pass_context
def ai_complete(ctx: click.Context, prompt: str, model_name: str) -> None:
    """Run a text completion using a registered AI model."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai complete", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "SELECT provider, model, api_key, base_url "
                "FROM __seekdb_ai_models WHERE model_name = %s",
                (model_name,),
            )
            model_cfg = cur.fetchone()
            if not model_cfg:
                log_operation("ai complete", ok=False, error_code="MODEL_NOT_FOUND")
                output.error("MODEL_NOT_FOUND", f"Model '{model_name}' not registered. Run: seekdb ai model list", fmt=fmt)
                return

        conn.close()

        import os
        provider = model_cfg["provider"]
        model_id = model_cfg["model"]
        api_key = model_cfg["api_key"] or os.environ.get("SEEKDB_AI_API_KEY", "")
        base_url = model_cfg["base_url"] or None

        with timer:
            response_text = _call_provider(provider, model_id, api_key, base_url, prompt)

        log_operation("ai complete", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"model": model_name, "response": response_text},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("ai complete", ok=False, error_code="AI_ERROR")
        output.error("AI_ERROR", str(exc), fmt=fmt)
    finally:
        try:
            conn.close()
        except Exception:
            pass


def _call_provider(provider: str, model: str, api_key: str, base_url: str | None, prompt: str) -> str:
    """Dispatch to the appropriate LLM provider. Uses OpenAI-compatible API by default."""
    try:
        import openai
    except ImportError:
        raise ImportError("openai package is required for AI completions. Install it with: pip install openai")

    kwargs: dict[str, Any] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    elif provider == "ollama":
        kwargs["base_url"] = "http://localhost:11434/v1"

    client = openai.OpenAI(**kwargs)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or ""
