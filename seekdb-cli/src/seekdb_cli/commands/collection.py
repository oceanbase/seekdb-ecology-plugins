"""seekdb collection command — manage vector collections."""

from __future__ import annotations

from typing import Any

import click

from seekdb_cli import output
from seekdb_cli.logger import log_operation
from seekdb_cli.vecconnection import get_vec_client


@click.group("collection")
@click.pass_context
def collection_cmd(ctx: click.Context) -> None:
    """Manage vector collections."""


@collection_cmd.command("list")
@click.pass_context
def list_collections(ctx: click.Context) -> None:
    """List all collections in the current database."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("collection list", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            collections = client.list_collections()
            result = []
            for col in collections:
                info: dict[str, Any] = {"name": col.name}
                try:
                    info["count"] = col.count()
                except Exception:
                    info["count"] = None
                result.append(info)

        log_operation("collection list", ok=True, time_ms=timer.elapsed_ms)
        output.success(result, time_ms=timer.elapsed_ms, fmt=fmt)
    except Exception as exc:
        log_operation("collection list", ok=False, error_code="COLLECTION_ERROR")
        output.error("COLLECTION_ERROR", str(exc), fmt=fmt)


@collection_cmd.command("create")
@click.argument("name")
@click.option("--dimension", "-d", type=int, default=384, help="Vector dimension (default: 384).")
@click.option("--distance", type=click.Choice(["cosine", "l2", "ip"]), default="cosine", help="Distance metric.")
@click.pass_context
def create_collection(ctx: click.Context, name: str, dimension: int, distance: str) -> None:
    """Create a new collection."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("collection create", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        from pyseekdb import HNSWConfiguration

        with timer:
            config = HNSWConfiguration(dimension=dimension, distance=distance)
            client.create_collection(
                name=name,
                configuration=config,
                embedding_function=None,
            )

        log_operation("collection create", ok=True, time_ms=timer.elapsed_ms)
        output.success(
            {"name": name, "dimension": dimension, "distance": distance},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except Exception as exc:
        log_operation("collection create", ok=False, error_code="COLLECTION_ERROR")
        output.error("COLLECTION_ERROR", str(exc), fmt=fmt)


@collection_cmd.command("delete")
@click.argument("name")
@click.pass_context
def delete_collection(ctx: click.Context, name: str) -> None:
    """Delete a collection."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("collection delete", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            if not client.has_collection(name):
                log_operation("collection delete", ok=False, error_code="COLLECTION_NOT_FOUND")
                output.error(
                    "COLLECTION_NOT_FOUND",
                    f"Collection '{name}' does not exist",
                    fmt=fmt,
                    extra={"collections": [c.name for c in client.list_collections()]},
                )
                return
            client.delete_collection(name)

        log_operation("collection delete", ok=True, time_ms=timer.elapsed_ms)
        output.success({"deleted": name}, time_ms=timer.elapsed_ms, fmt=fmt)
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("collection delete", ok=False, error_code="COLLECTION_ERROR")
        output.error("COLLECTION_ERROR", str(exc), fmt=fmt)


@collection_cmd.command("info")
@click.argument("name")
@click.pass_context
def info_collection(ctx: click.Context, name: str) -> None:
    """Show collection details (count, peek)."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("collection info", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            if not client.has_collection(name):
                log_operation("collection info", ok=False, error_code="COLLECTION_NOT_FOUND")
                output.error(
                    "COLLECTION_NOT_FOUND",
                    f"Collection '{name}' does not exist",
                    fmt=fmt,
                    extra={"collections": [c.name for c in client.list_collections()]},
                )
                return

            col = client.get_collection(name, embedding_function=None)
            count = col.count()
            preview = col.peek(limit=3)

            data: dict[str, Any] = {
                "name": name,
                "count": count,
                "preview": {
                    "ids": preview.get("ids", []),
                    "documents": preview.get("documents", []),
                    "metadatas": preview.get("metadatas", []),
                },
            }
            # Dimension and distance come from list_collections() metadata (pyseekdb API)
            for coll in client.list_collections():
                if getattr(coll, "name", None) == name:
                    if getattr(coll, "dimension", None) is not None:
                        data["dimension"] = coll.dimension
                    if getattr(coll, "distance", None) is not None:
                        data["distance"] = coll.distance
                    break

        log_operation("collection info", ok=True, time_ms=timer.elapsed_ms)
        output.success(data, time_ms=timer.elapsed_ms, fmt=fmt)
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("collection info", ok=False, error_code="COLLECTION_ERROR")
        output.error("COLLECTION_ERROR", str(exc), fmt=fmt)
