"""Tests for DSN parsing."""

import pytest
from seekdb_cli.connection import parse_dsn, DSNConfig


class TestParseDSN:
    def test_full_dsn(self):
        cfg = parse_dsn("seekdb://root:mypass@10.0.0.1:2881/testdb")
        assert cfg.host == "10.0.0.1"
        assert cfg.port == 2881
        assert cfg.user == "root"
        assert cfg.password == "mypass"
        assert cfg.database == "testdb"

    def test_minimal_dsn(self):
        cfg = parse_dsn("seekdb://localhost")
        assert cfg.host == "localhost"
        assert cfg.port == 2881
        assert cfg.user == "root"
        assert cfg.password == ""
        assert cfg.database == "test"

    def test_dsn_with_user_no_password(self):
        cfg = parse_dsn("seekdb://admin@db.example.com:3306/prod")
        assert cfg.user == "admin"
        assert cfg.password == ""
        assert cfg.host == "db.example.com"
        assert cfg.port == 3306
        assert cfg.database == "prod"

    def test_dsn_with_empty_password(self):
        cfg = parse_dsn("seekdb://root:@127.0.0.1:2881/test")
        assert cfg.user == "root"
        assert cfg.password == ""

    def test_dsn_url_encoded_password(self):
        cfg = parse_dsn("seekdb://root:p%40ss%3Aword@host:2881/db")
        assert cfg.password == "p@ss:word"

    def test_invalid_dsn(self):
        with pytest.raises(ValueError, match="Invalid DSN format"):
            parse_dsn("mysql://user:pass@host/db")

    def test_invalid_dsn_no_scheme(self):
        with pytest.raises(ValueError, match="Invalid DSN format"):
            parse_dsn("user:pass@host:3306/db")
