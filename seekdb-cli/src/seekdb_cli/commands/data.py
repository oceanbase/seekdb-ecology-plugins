"""seekdb add / export commands — data transfer for collections."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

import click

from seekdb_cli import output
from seekdb_cli.logger import log_operation
from seekdb_cli.vecconnection import get_vec_client


def _read_records_from_file(path: str) -> list[dict[str, Any]]:
    """Read records from a JSON array file, JSONL file, or CSV file."""
    p = Path(path)
    suffix = p.suffix.lower()

    if suffix == ".jsonl":
        records = []
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    if suffix == ".csv":
        with open(p, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    raise ValueError(f"Expected a JSON array in {path}, got {type(data).__name__}")


def _parse_json_text(text: str) -> list[dict[str, Any]]:
    """Parse a string as either a JSON array or one-per-line JSONL."""
    text = text.strip()
    if not text:
        return []

    if text.startswith("["):
        data = json.loads(text)
        if isinstance(data, list):
            return data
        raise ValueError(f"Expected a JSON array, got {type(data).__name__}")

    records: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


@click.command("add")
@click.argument("collection")
@click.option("--file", "filepath", type=click.Path(exists=True), default=None, help="Path to data file (JSON/JSONL/CSV).")
@click.option("--stdin", "use_stdin", is_flag=True, help="Read JSON/JSONL from stdin.")
@click.option("--data", "inline_data", default=None, help="Inline JSON object or array.")
@click.option("--vectorize-column", default=None, help="Column to auto-vectorize via collection embedding function.")
@click.pass_context
def add_cmd(
    ctx: click.Context,
    collection: str,
    filepath: str | None,
    use_stdin: bool,
    inline_data: str | None,
    vectorize_column: str | None,
) -> None:
    """Add data to a collection.

    Data source (exactly one required): --file, --stdin, or --data.
    """
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    sources = sum([filepath is not None, use_stdin, inline_data is not None])
    if sources == 0:
        output.error(
            "MISSING_INPUT",
            "No data source. Pass --file <path>, --stdin, or --data '<json>'.",
            fmt=fmt,
            exit_code=output.EXIT_USAGE_ERROR,
        )
        return
    if sources > 1:
        output.error(
            "CONFLICTING_INPUT",
            "Specify only one of --file, --stdin, or --data.",
            fmt=fmt,
            exit_code=output.EXIT_USAGE_ERROR,
        )
        return

    try:
        if filepath:
            records = _read_records_from_file(filepath)
        elif use_stdin:
            records = _parse_json_text(sys.stdin.read())
        else:
            text = inline_data or ""
            if text.startswith("{"):
                records = [json.loads(text)]
            else:
                records = _parse_json_text(text)
    except Exception as exc:
        log_operation("add", ok=False, error_code="INPUT_ERROR")
        output.error("INPUT_ERROR", f"Cannot parse input: {exc}", fmt=fmt)
        return

    if not records:
        output.error("INPUT_ERROR", "No records found in input.", fmt=fmt)
        return

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("add", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            col = client.get_or_create_collection(collection)

            ids: list[str] = []
            documents: list[str] = []
            metadatas: list[dict[str, Any]] = []
            embeddings: list[list[float]] | None = None

            for i, rec in enumerate(records):
                doc_id = str(rec.pop("id", str(i)))
                ids.append(doc_id)

                doc_text = ""
                if vectorize_column and vectorize_column in rec:
                    doc_text = str(rec.pop(vectorize_column))
                elif "document" in rec:
                    doc_text = str(rec.pop("document"))
                elif "text" in rec:
                    doc_text = str(rec.pop("text"))
                elif "content" in rec:
                    doc_text = str(rec.pop("content"))
                documents.append(doc_text)

                if "embedding" in rec:
                    emb = rec.pop("embedding")
                    if embeddings is None:
                        embeddings = []
                    embeddings.append(emb)

                meta = rec.pop("metadata", None)
                if isinstance(meta, dict):
                    metadatas.append(meta)
                else:
                    metadatas.append({k: v for k, v in rec.items() if k not in ("embedding",)})

            kwargs: dict[str, Any] = {
                "ids": ids,
                "documents": documents,
                "metadatas": metadatas,
            }
            if embeddings and len(embeddings) == len(ids):
                kwargs["embeddings"] = embeddings

            BATCH_SIZE = 500
            imported = 0
            for start in range(0, len(ids), BATCH_SIZE):
                end = start + BATCH_SIZE
                batch: dict[str, Any] = {}
                for k, v in kwargs.items():
                    batch[k] = v[start:end] if isinstance(v, list) else v
                col.add(**batch)
                imported += len(batch["ids"])

        log_operation("add", ok=True, rows=imported, time_ms=timer.elapsed_ms)
        output.success(
            {"collection": collection, "added": imported},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("add", ok=False, error_code="IMPORT_ERROR")
        output.error("ADD_ERROR", str(exc), fmt=fmt)


@click.command("export")
@click.argument("collection")
@click.option("--output", "outpath", required=True, type=click.Path(), help="Output file path (JSON/JSONL).")
@click.option("--limit", "-n", type=int, default=10000, help="Max records to export.")
@click.pass_context
def export_cmd(ctx: click.Context, collection: str, outpath: str, limit: int) -> None:
    """Export collection data to a file."""
    fmt: str = ctx.obj["format"]
    dsn: str | None = ctx.obj["dsn"]

    try:
        client = get_vec_client(dsn)
    except (ImportError, ValueError) as exc:
        log_operation("export", ok=False, error_code="CONNECTION_ERROR")
        output.error("CONNECTION_ERROR", str(exc), fmt=fmt)
        return

    timer = output.Timer()
    try:
        with timer:
            col = client.get_collection(collection, embedding_function=None)
            results = col.get(
                include=["documents", "metadatas", "embeddings"],
                limit=limit,
            )

            doc_ids = results.get("ids", [])
            docs = results.get("documents", [])
            metas = results.get("metadatas", [])
            embs = results.get("embeddings", [])

            records: list[dict[str, Any]] = []
            for i, doc_id in enumerate(doc_ids):
                rec: dict[str, Any] = {"id": doc_id}
                if docs and i < len(docs) and docs[i]:
                    rec["document"] = docs[i]
                if metas and i < len(metas) and metas[i]:
                    rec["metadata"] = metas[i]
                if embs and i < len(embs) and embs[i]:
                    rec["embedding"] = embs[i]
                records.append(rec)

            p = Path(outpath)
            p.parent.mkdir(parents=True, exist_ok=True)

            if p.suffix.lower() == ".jsonl":
                with open(p, "w", encoding="utf-8") as f:
                    for rec in records:
                        f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            else:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(records, f, ensure_ascii=False, indent=2, default=str)

        log_operation("export", ok=True, rows=len(records), time_ms=timer.elapsed_ms)
        output.success(
            {"collection": collection, "exported": len(records), "file": str(p)},
            time_ms=timer.elapsed_ms,
            fmt=fmt,
        )
    except SystemExit:
        raise
    except Exception as exc:
        log_operation("export", ok=False, error_code="EXPORT_ERROR")
        output.error("EXPORT_ERROR", str(exc), fmt=fmt)
