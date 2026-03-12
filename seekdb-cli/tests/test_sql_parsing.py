"""Tests for SQL parsing utilities in the sql command."""

from seekdb_cli.commands.sql import (
    _is_write,
    _is_select,
    _has_limit,
    _has_where,
    _extract_tables_from_sql,
)


class TestIsWrite:
    def test_insert(self):
        assert _is_write("INSERT INTO users (name) VALUES ('Alice')")

    def test_update(self):
        assert _is_write("UPDATE users SET name = 'Bob' WHERE id = 1")

    def test_delete(self):
        assert _is_write("DELETE FROM users WHERE id = 1")

    def test_drop(self):
        assert _is_write("DROP TABLE users")

    def test_truncate(self):
        assert _is_write("TRUNCATE TABLE users")

    def test_select_is_not_write(self):
        assert not _is_write("SELECT * FROM users")

    def test_show_is_not_write(self):
        assert not _is_write("SHOW TABLES")

    def test_case_insensitive(self):
        assert _is_write("insert into users values (1)")
        assert _is_write("  DELETE FROM t")


class TestIsSelect:
    def test_select(self):
        assert _is_select("SELECT id, name FROM users")

    def test_select_with_whitespace(self):
        assert _is_select("  SELECT 1")

    def test_insert_is_not_select(self):
        assert not _is_select("INSERT INTO t VALUES (1)")


class TestHasLimit:
    def test_with_limit(self):
        assert _has_limit("SELECT * FROM users LIMIT 10")

    def test_without_limit(self):
        assert not _has_limit("SELECT * FROM users")

    def test_limit_case_insensitive(self):
        assert _has_limit("select * from t limit 50")


class TestHasWhere:
    def test_with_where(self):
        assert _has_where("DELETE FROM users WHERE id = 1")

    def test_without_where(self):
        assert not _has_where("DELETE FROM users")


class TestExtractTables:
    def test_select_from(self):
        tables = _extract_tables_from_sql("SELECT * FROM users WHERE id = 1")
        assert "users" in tables

    def test_insert_into(self):
        tables = _extract_tables_from_sql("INSERT INTO orders (id) VALUES (1)")
        assert "orders" in tables

    def test_update(self):
        tables = _extract_tables_from_sql("UPDATE products SET price = 10 WHERE id = 1")
        assert "products" in tables

    def test_backtick_table(self):
        tables = _extract_tables_from_sql("SELECT * FROM `my_table`")
        assert "my_table" in tables
