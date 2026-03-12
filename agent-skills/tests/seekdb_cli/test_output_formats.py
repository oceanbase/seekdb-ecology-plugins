"""Tests for improved output formatting (CSV, JSONL, table for non-row data)."""

import io
import json
import sys
from unittest.mock import patch

from seekdb_cli.output import _write_csv, _print_jsonl, _print_table_from_data, _json_dumps


class TestWriteCsv:
    def test_basic_csv(self, capsys):
        columns = ["id", "name"]
        rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        _write_csv(columns, rows)
        out = capsys.readouterr().out
        lines = [l.rstrip("\r") for l in out.strip().split("\n")]
        assert lines[0] == "id,name"
        assert lines[1] == "1,Alice"
        assert lines[2] == "2,Bob"

    def test_nested_values_serialized(self, capsys):
        columns = ["id", "meta"]
        rows = [{"id": 1, "meta": {"key": "val"}}]
        _write_csv(columns, rows)
        out = capsys.readouterr().out
        assert "key" in out and "val" in out

    def test_none_values(self, capsys):
        columns = ["id", "name"]
        rows = [{"id": 1, "name": None}]
        _write_csv(columns, rows)
        out = capsys.readouterr().out
        lines = out.strip().split("\n")
        assert lines[1] == "1,"


class TestPrintJsonl:
    def test_rows_mode(self, capsys):
        payload = {"ok": True}
        rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        _print_jsonl(payload, rows)
        out = capsys.readouterr().out
        lines = out.strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["id"] == 1

    def test_data_list_fallback(self, capsys):
        payload = {"ok": True, "data": [{"name": "t1"}, {"name": "t2"}]}
        _print_jsonl(payload, None)
        out = capsys.readouterr().out
        lines = out.strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["name"] == "t1"

    def test_non_list_data_fallback(self, capsys):
        payload = {"ok": True, "data": {"key": "val"}}
        _print_jsonl(payload, None)
        out = capsys.readouterr().out
        parsed = json.loads(out.strip())
        assert parsed["ok"] is True


class TestPrintTableFromData:
    def test_list_of_dicts(self, capsys):
        payload = {"ok": True, "data": [{"name": "users", "rows": 100}, {"name": "orders", "rows": 500}]}
        _print_table_from_data(payload)
        out = capsys.readouterr().out
        assert "name" in out
        assert "users" in out
        assert "orders" in out

    def test_non_list_data(self, capsys):
        payload = {"ok": True, "data": "simple string"}
        _print_table_from_data(payload)
        out = capsys.readouterr().out
        parsed = json.loads(out.strip())
        assert parsed["ok"] is True
