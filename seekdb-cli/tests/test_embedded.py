"""Tests for embedded mode: DSN parsing, EmbeddedConnection, and EmbeddedCursor."""

from __future__ import annotations

import os
import shutil
import tempfile

import pymysql.err
import pytest

from seekdb_cli.connection import (
    EmbeddedConnection,
    EmbeddedDSNConfig,
    is_embedded_dsn,
    parse_embedded_dsn,
    get_connection,
    _sql_escape,
    _interpolate_sql,
)


# ---------------------------------------------------------------------------
# DSN parsing
# ---------------------------------------------------------------------------

class TestEmbeddedDSNParsing:
    def test_basic_path(self):
        cfg = parse_embedded_dsn("embedded:./seekdb.db")
        assert cfg.path == "./seekdb.db"
        assert cfg.database == "test"

    def test_path_with_database(self):
        cfg = parse_embedded_dsn("embedded:./data?database=mydb")
        assert cfg.path == "./data"
        assert cfg.database == "mydb"

    def test_absolute_path(self):
        cfg = parse_embedded_dsn("embedded:/opt/seekdb/data")
        assert cfg.path == "/opt/seekdb/data"
        assert cfg.database == "test"

    def test_absolute_path_with_database(self):
        cfg = parse_embedded_dsn("embedded:/opt/seekdb/data?database=prod")
        assert cfg.path == "/opt/seekdb/data"
        assert cfg.database == "prod"

    def test_simple_dir(self):
        cfg = parse_embedded_dsn("embedded:seekdb_data")
        assert cfg.path == "seekdb_data"
        assert cfg.database == "test"

    def test_is_embedded(self):
        assert is_embedded_dsn("embedded:./seekdb.db") is True
        assert is_embedded_dsn("seekdb://host/db") is False

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid embedded DSN"):
            parse_embedded_dsn("seekdb://host/db")


class TestSqlEscape:
    def test_string(self):
        assert _sql_escape("hello") == "'hello'"

    def test_string_with_quotes(self):
        assert _sql_escape("it's") == "'it\\'s'"

    def test_none(self):
        assert _sql_escape(None) == "NULL"

    def test_int(self):
        assert _sql_escape(42) == "42"

    def test_float(self):
        assert _sql_escape(3.14) == "3.14"


class TestInterpolateSql:
    def test_single_param(self):
        result = _interpolate_sql("SELECT * FROM t WHERE id = %s", (1,))
        assert result == "SELECT * FROM t WHERE id = 1"

    def test_string_param(self):
        result = _interpolate_sql("SELECT * FROM t WHERE name = %s", ("Alice",))
        assert result == "SELECT * FROM t WHERE name = 'Alice'"

    def test_multiple_params(self):
        result = _interpolate_sql("SELECT * FROM t WHERE a = %s AND b = %s", (1, "x"))
        assert result == "SELECT * FROM t WHERE a = 1 AND b = 'x'"

    def test_literal_percent(self):
        result = _interpolate_sql("SELECT 100 %% done", ())
        assert result == "SELECT 100 % done"


# ---------------------------------------------------------------------------
# Embedded connection and cursor (requires pylibseekdb, Linux only)
# ---------------------------------------------------------------------------

def _find_non_tmpfs_dir() -> str:
    """Return a temporary directory NOT on tmpfs (pylibseekdb rejects tmpfs)."""
    candidates = [os.path.expanduser("~"), "/var/tmp", "/opt"]
    for base in candidates:
        if os.path.isdir(base) and os.access(base, os.W_OK):
            path = os.path.join(base, ".seekdb_cli_test")
            os.makedirs(path, exist_ok=True)
            return path
    pytest.skip("No writable non-tmpfs directory found")
    return ""


_pylibseekdb_available = False
try:
    import pylibseekdb  # noqa: F401
    _pylibseekdb_available = True
except ImportError:
    pass


@pytest.fixture(scope="module")
def embedded_dir():
    d = _find_non_tmpfs_dir()
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.mark.skipif(not _pylibseekdb_available, reason="pylibseekdb not installed")
class TestEmbeddedConnection:

    def test_connect_and_select(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("SELECT 1 AS val, 'hello' AS msg")
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0]["val"] == 1
        assert rows[0]["msg"] == "hello"
        cur.close()
        conn.close()

    def test_create_table_and_query(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS cli_test (id INT PRIMARY KEY, name VARCHAR(64))")
        cur.execute("INSERT INTO cli_test VALUES (1, 'Alice') ON DUPLICATE KEY UPDATE name='Alice'")
        cur.execute("INSERT INTO cli_test VALUES (2, 'Bob') ON DUPLICATE KEY UPDATE name='Bob'")

        cur.execute("SELECT * FROM cli_test ORDER BY id")
        rows = cur.fetchall()
        assert len(rows) == 2
        assert rows[0]["id"] == 1
        assert rows[0]["name"] == "Alice"

        cur.execute("DROP TABLE IF EXISTS cli_test")
        cur.close()
        conn.close()

    def test_show_tables(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS show_test (id INT PRIMARY KEY)")
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        tables = [list(r.values())[0] for r in rows]
        assert "show_test" in tables

        cur.execute("DROP TABLE IF EXISTS show_test")
        cur.close()
        conn.close()

    def test_show_full_columns(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS col_test (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL)")
        cur.execute("SHOW FULL COLUMNS FROM col_test")
        rows = cur.fetchall()
        assert len(rows) == 2
        assert rows[0]["Field"] == "id"
        assert rows[1]["Field"] == "name"
        assert "Type" in rows[0]

        cur.execute("DROP TABLE IF EXISTS col_test")
        cur.close()
        conn.close()

    def test_show_index(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS idx_test (id INT PRIMARY KEY, val INT)")
        cur.execute("SHOW INDEX FROM idx_test")
        rows = cur.fetchall()
        assert len(rows) >= 1
        assert rows[0]["Key_name"] == "PRIMARY"
        assert rows[0]["Column_name"] == "id"

        cur.execute("DROP TABLE IF EXISTS idx_test")
        cur.close()
        conn.close()

    def test_show_table_status(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS status_test (id INT PRIMARY KEY)")
        cur.execute("SHOW TABLE STATUS")
        rows = cur.fetchall()
        assert len(rows) >= 1
        names = [r["Name"] for r in rows]
        assert "status_test" in names

        cur.execute("DROP TABLE IF EXISTS status_test")
        cur.close()
        conn.close()

    def test_show_create_table(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ddl_test (id INT PRIMARY KEY)")
        cur.execute("SHOW CREATE TABLE ddl_test")
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0]["Table"] == "ddl_test"
        assert "CREATE TABLE" in rows[0]["Create Table"]

        cur.execute("DROP TABLE IF EXISTS ddl_test")
        cur.close()
        conn.close()

    def test_parameterized_query(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS param_test (id INT PRIMARY KEY, name VARCHAR(64))")
        cur.execute("INSERT INTO param_test VALUES (1, 'Alice') ON DUPLICATE KEY UPDATE name='Alice'")

        cur.execute(
            "SELECT * FROM param_test WHERE name = %s",
            ("Alice",),
        )
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0]["name"] == "Alice"

        cur.execute("DROP TABLE IF EXISTS param_test")
        cur.close()
        conn.close()

    def test_fetchone(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("SELECT 1 AS a UNION ALL SELECT 2")
        row1 = cur.fetchone()
        assert row1 is not None
        row2 = cur.fetchone()
        assert row2 is not None
        row3 = cur.fetchone()
        assert row3 is None
        cur.close()
        conn.close()

    def test_dml_rowcount(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS rc_test (id INT PRIMARY KEY, val INT)")
        cur.execute("DELETE FROM rc_test")
        cur.execute("INSERT INTO rc_test VALUES (1, 10)")
        cur.execute("INSERT INTO rc_test VALUES (2, 20)")
        cur.execute("UPDATE rc_test SET val = 99 WHERE id = 1")
        assert cur.rowcount == 1

        cur.execute("DROP TABLE IF EXISTS rc_test")
        cur.close()
        conn.close()

    def test_description_populated(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("SELECT 1 AS x, 'hi' AS y")
        assert cur.description is not None
        col_names = [d[0] for d in cur.description]
        assert "x" in col_names
        assert "y" in col_names
        cur.close()
        conn.close()

    def test_cursor_context_manager(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        with conn.cursor() as cur:
            cur.execute("SELECT 42 AS answer")
            rows = cur.fetchall()
            assert rows[0]["answer"] == 42
        conn.close()

    def test_sql_error_raises_pymysql_error(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        with pytest.raises(pymysql.err.ProgrammingError):
            cur.execute("SELECT * FROM nonexistent_table_xyz_123")
        cur.close()
        conn.close()

    def test_get_connection_embedded(self, embedded_dir):
        dsn = f"embedded:{embedded_dir}"
        conn = get_connection(dsn)
        cur = conn.cursor()
        cur.execute("SELECT 1 AS v")
        rows = cur.fetchall()
        assert rows[0]["v"] == 1
        cur.close()
        conn.close()

    def test_information_schema(self, embedded_dir):
        conn = EmbeddedConnection(embedded_dir, "test")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS info_test (id INT PRIMARY KEY)")
        cur.execute(
            "SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
            ("info_test",),
        )
        rows = cur.fetchall()
        assert len(rows) >= 1
        assert "TABLE_COMMENT" in rows[0]

        cur.execute("DROP TABLE IF EXISTS info_test")
        cur.close()
        conn.close()
