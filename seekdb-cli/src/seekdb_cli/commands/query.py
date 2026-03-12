"""seekdb query / get commands — search and retrieve documents from collections."""

from __future__ import annotations

import json
from typing import Any

import click

from seekdb_cli import output
from seekdb_cli.logger import log_operation
from seekdb_cli.vecconnection import get_vec_client


def _parse_where(where_json: str | None) -> dict[str, Any] | None:
    if not where_json:
        return None
    try:
        return json.loads(where_json)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"Invalid JSON for --where: {exc}") from exc


def _flatten_results(results: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert pyseekdb nested list results into flat list of dicts."""
    ids_lists = results.get("ids", [[]])
    docs_lists = results.get("documents", [[]])
    meta_lists = results.get("metadatas", [[]])
    dist_lists = results.get("distances", [[]])

    ids = ids_lists[0] if ids_lists else []
    docs = docs_lists[0] if docs_lists else []
    metas = meta_lists[0] if meta_lists else []
    dists = dist_lists[0] if dist_lists else []

    out: list[dict[str, Any]] = []
    for i, doc_id in enumerate(ids):
        item: dict[str, Any] = {"id": doc_id}
        if dists and i < len(dists):
            item["score"] = round(1.0 - dists[i], 4) if dists[i] is not None else None
        if docs and i < len(docs):
            item["document"] = docs[i]
        if metas and i < len(metas):
            item["metadata"] = metas[i]
        out.append(item)
    return out


@click.command("query")
@click.argument("collection")
@click.option("--text", required=True, help="Query text for semantic/fulltext search.")
@click.option("--mode", type=click.Choice(["semantic", "fulltext", "hybrid"]), default="semantic", help="Search mode.")
@click.option("--limit", "-n", type=int, default=10, help="Max results to return.")
@click.option("--where", "where_json", default=None, help="Metadata filter as JSON.")
@click.pass_context
def query_cmd(ctx: click.Context, collection: str, text: str, mode: str, limit: int, where_json: str | None) -> None:
    """Search a collection using semantic, fulltext, or hybrid mode."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]
    where = _parse_where(where_json)

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("query", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            col = client.get_collection(collection)

            if mode == "semantic":
                results = col.query(
                    query_texts=[text],
                    n_results=limit,
                    where=where,
                    include=["documents", "metadatas"],
                )
            elif mode == "fulltext":
                results = col.query(
                    query_texts=[text],
                    n_results=limit,
                    where=where,
                    where_document={"$contains": text},
                    include=["documents", "metadatas"],
                )
            else:  # hybrid
                results = col.hybrid_search(
                    query={
                        "where_document": {"$contains": text},
                        "where": where,
                        "n_results": limit,
                    },
                    knn={
                        "query_texts": [text],
                        "where": where,
                        "n_results": limit,
                    },
                    rank={"rrf": {}},
                    n_results=limit,
                    include=["documents", "metadatas"],
                )

        flat = _flatten_results(results)
        log_operation("query", ok=True, rows=len(flat), time_ms=timer.elapsed_ms)
        output.success(
            {"results": flat, "count": len(flat)},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("query", ok=False, error_code="QUERY_ERROR")
        output.error("QUERY_ERROR", str(exc), fmt=fmt)


@click.command("get")
@click.argument("collection")
@click.option("--ids", default=None, help="Comma-separated document IDs.")
@click.option("--limit", "-n", type=int, default=10, help="Max results to return.")
@click.option("--where", "where_json", default=None, help="Metadata filter as JSON.")
@click.pass_context
def get_cmd(ctx: click.Context, collection: str, ids: str | None, limit: int, where_json: str | None) -> None:
    """Retrieve documents from a collection by IDs or filter."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]
    where = _parse_where(where_json)

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("get", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            col = client.get_collection(collection, embedding_function=None)

            kwargs: dict[str, Any] = {
                "include": ["documents", "metadatas"],
                "limit": limit,
            }
            if ids:
                kwargs["ids"] = [i.strip() for i in ids.split(",")]
            if where:
                kwargs["where"] = where

            results = col.get(**kwargs)

        doc_ids = results.get("ids", [])
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])

        flat: list[dict[str, Any]] = []
        for i, doc_id in enumerate(doc_ids):
            item: dict[str, Any] = {"id": doc_id}
            if docs and i < len(docs):
                item["document"] = docs[i]
            if metas and i < len(metas):
                item["metadata"] = metas[i]
            flat.append(item)

        log_operation("get", ok=True, rows=len(flat), time_ms=timer.elapsed_ms)
        output.success(
            {"results": flat, "count": len(flat)},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("get", ok=False, error_code="GET_ERROR")
        output.error("GET_ERROR", str(exc), fmt=fmt)
