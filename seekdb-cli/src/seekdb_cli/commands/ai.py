"""seekdb ai command — use database AI (DBMS_AI_SERVICE, AI_COMPLETE)."""

from __future__ import annotations

import json

import click
import pymysql

from seekdb_cli import output
from seekdb_cli.connection import get_connection
from seekdb_cli.logger import log_operation

# OceanBase AI model types (for CREATE_AI_MODEL)
AI_MODEL_TYPES = ("dense_embedding", "completion", "rerank")


@click.group("ai")
@click.pass_context
def ai_cmd(ctx: click.Context) -> None:
    """AI model management and completion (via database DBMS_AI_SERVICE)."""


# ---------------------------------------------------------------------------
# seekdb ai model ...
# ---------------------------------------------------------------------------

@ai_cmd.group("model")
@click.pass_context
def model_group(ctx: click.Context) -> None:
    """Manage AI models registered in the database (DBMS_AI_SERVICE)."""


@model_group.command("list")
@click.pass_context
def model_list(ctx: click.Context) -> None:
    """List all registered AI models (from oceanbase.DBA_OB_AI_MODELS)."""
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
                "SELECT MODEL_ID, NAME, TYPE, MODEL_NAME "
                "FROM oceanbase.DBA_OB_AI_MODELS ORDER BY NAME"
            )
            rows = cur.fetchall()
            # DictCursor: keys may be uppercase from view
            result = []
            for r in rows:
                row = dict(r)
                result.append({
                    "name": row.get("NAME") or row.get("name"),
                    "type": row.get("TYPE") or row.get("type"),
                    "model_name": row.get("MODEL_NAME") or row.get("model_name"),
                    "model_id": row.get("MODEL_ID") or row.get("model_id"),
                })

        log_operation("ai model list", ok=True, time_ms=timer.elapsed_ms)
        output.success(result, time_ms=timer.elapsed_ms, fmt=fmt)
    except pymysql.err.ProgrammingError as exc:
        log_operation("ai model list", ok=False, error_code="SQL_ERROR")
        output.error(
            "SQL_ERROR",
            str(exc) + ". Ensure the database supports DBA_OB_AI_MODELS (OceanBase AI).",
            fmt=fmt,
        )
    except pymysql.err.Error as exc:
        log_operation("ai model list", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


@model_group.command("create")
@click.argument("name")
@click.option(
    "--type",
    "model_type",
    type=click.Choice(AI_MODEL_TYPES),
    required=True,
    help="Model type: dense_embedding, completion, or rerank.",
)
@click.option(
    "--model",
    "provider_model_name",
    required=True,
    help="Provider model name (e.g. BAAI/bge-m3, THUDM/GLM-4-9B-0414).",
)
@click.pass_context
def model_create(
    ctx: click.Context,
    name: str,
    model_type: str,
    provider_model_name: str,
) -> None:
    """Register an AI model via DBMS_AI_SERVICE.CREATE_AI_MODEL. Create an endpoint separately to use it."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model create", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    config = json.dumps({"type": model_type, "model_name": provider_model_name})
    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "CALL DBMS_AI_SERVICE.CREATE_AI_MODEL(%s, %s)",
                (name, config),
            )
            conn.commit()

        log_operation("ai model create", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"name": name, "type": model_type, "model_name": provider_model_name},
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
    """Drop an AI model via DBMS_AI_SERVICE.DROP_AI_MODEL. Drop endpoints first if any."""
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
            cur.execute("CALL DBMS_AI_SERVICE.DROP_AI_MODEL(%s)", (name,))
            conn.commit()

        log_operation("ai model delete", ok=True, time_ms=timer.elapsed_ms)
        output.success({"deleted": name}, time_ms=timer.elapsed_ms, fmt=fmt)
    except pymysql.err.Error as exc:
        log_operation("ai model delete", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# seekdb ai model endpoint ...
# ---------------------------------------------------------------------------

@model_group.group("endpoint")
@click.pass_context
def endpoint_group(ctx: click.Context) -> None:
    """Create or delete AI model endpoints (DBMS_AI_SERVICE)."""


@endpoint_group.command("create")
@click.argument("endpoint_name")
@click.argument("ai_model_name")
@click.option("--url", required=True, help="API URL (e.g. https://api.siliconflow.cn/v1/chat/completions).")
@click.option("--access-key", required=True, help="API key for the service.")
@click.option(
    "--provider",
    default="siliconflow",
    help="Provider identifier. See supported providers and URLs below.",
)
@click.pass_context
def endpoint_create(
    ctx: click.Context,
    endpoint_name: str,
    ai_model_name: str,
    url: str,
    access_key: str,
    provider: str,
) -> None:
    """Create an AI model endpoint via DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT.

    Supported providers (--provider value):
      aliyun-openAI     Alibaba Cloud (OpenAI-compatible)
      aliyun-dashscope  Alibaba Cloud DashScope
      deepseek          DeepSeek
      siliconflow       SiliconFlow
      hunyuan-openAI    Tencent Hunyuan (OpenAI-compatible)
      openAI            OpenAI

    Provider endpoint URLs (use the specific interface URL for chat/embedding/rerank, not the base URL):
      Alibaba Cloud (OpenAI-compatible):
        completion  https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
        embedding   https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings
      Alibaba Cloud DashScope (native):
        completion  https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
        embedding   https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding
        rerank     https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank
      DeepSeek (OpenAI-compatible):
        completion  https://api.deepseek.com/chat/completions
      SiliconFlow (OpenAI-compatible):
        completion  https://api.siliconflow.cn/v1/chat/completions
        embedding   https://api.siliconflow.cn/v1/embeddings
        rerank     https://api.siliconflow.cn/v1/rerank
      Tencent Hunyuan (OpenAI-compatible):
        completion  https://api.hunyuan.cloud.tencent.com/v1/chat/completions
        embedding   https://api.hunyuan.cloud.tencent.com/v1/embeddings
    """
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model endpoint create", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    config = json.dumps({
        "ai_model_name": ai_model_name,
        "url": url,
        "access_key": access_key,
        "provider": provider,
    })
    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "CALL DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT(%s, %s)",
                (endpoint_name, config),
            )
            conn.commit()

        log_operation("ai model endpoint create", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"endpoint": endpoint_name, "ai_model": ai_model_name, "provider": provider},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except pymysql.err.Error as exc:
        log_operation("ai model endpoint create", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


@endpoint_group.command("delete")
@click.argument("endpoint_name")
@click.pass_context
def endpoint_delete(ctx: click.Context, endpoint_name: str) -> None:
    """Drop an AI model endpoint via DBMS_AI_SERVICE.DROP_AI_MODEL_ENDPOINT."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        conn = get_connection(dsn)
    except Exception as exc:
        log_operation("ai model endpoint delete", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer, conn.cursor() as cur:
            cur.execute(
                "CALL DBMS_AI_SERVICE.DROP_AI_MODEL_ENDPOINT(%s)",
                (endpoint_name,),
            )
            conn.commit()

        log_operation("ai model endpoint delete", ok=True, time_ms=timer.elapsed_ms)
        output.success({"deleted": endpoint_name}, time_ms=timer.elapsed_ms, fmt=fmt)
    except pymysql.err.Error as exc:
        log_operation("ai model endpoint delete", ok=False, error_code="SQL_ERROR")
        output.error("SQL_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# seekdb ai complete ...
# ---------------------------------------------------------------------------

@ai_cmd.command("complete")
@click.argument("prompt")
@click.option("--model", "model_name", required=True, help="Registered completion model name (from ai model list).")
@click.pass_context
def ai_complete(ctx: click.Context, prompt: str, model_name: str) -> None:
    """Run text completion using the database AI_COMPLETE function."""
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
                "SELECT AI_COMPLETE(%s, %s) AS response",
                (model_name, prompt),
            )
            row = cur.fetchone()
        response_text = (row.get("response") or row.get("RESPONSE") or "") if row else ""

        log_operation("ai complete", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"model": model_name, "response": response_text},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except pymysql.err.Error as exc:
        log_operation("ai complete", ok=False, error_code="AI_ERROR")
        output.error("AI_ERROR", str(exc), fmt=fmt)
    finally:
        conn.close()
