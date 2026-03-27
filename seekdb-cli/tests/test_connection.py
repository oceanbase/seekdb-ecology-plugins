"""Tests for DSN parsing."""

import pytest
from seekdb_cli.connection import parse_dsn, DSNConfig, pymysql_ssl_kwargs


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

    def test_dsn_at_in_username_before_sys_password(self):
        """Usernames like u@sys:secret@host — use rightmost @ before host."""
        cfg = parse_dsn(
            "seekdb://u_b0d763c7@sys:xxxx@6.12.233.85:2881/db_b0d763c7"
        )
        assert cfg.user == "u_b0d763c7@sys"
        assert cfg.password == "xxxx"
        assert cfg.host == "6.12.233.85"
        assert cfg.port == 2881
        assert cfg.database == "db_b0d763c7"

    def test_dsn_at_in_username_no_password(self):
        cfg = parse_dsn("seekdb://u@sys@10.0.0.2:2881/db")
        assert cfg.user == "u@sys"
        assert cfg.password == ""
        assert cfg.host == "10.0.0.2"

    def test_invalid_dsn(self):
        with pytest.raises(ValueError, match="Invalid DSN format"):
            parse_dsn("mysql://user:pass@host/db")

    def test_invalid_dsn_no_scheme(self):
        with pytest.raises(ValueError, match="Invalid DSN format"):
            parse_dsn("user:pass@host:3306/db")

    def test_dsn_tls_skip_verify(self):
        cfg = parse_dsn(
            "seekdb://root:pw@10.0.0.1:2881/mydb?tls=skip-verify"
        )
        assert cfg.ssl_mode == "skip_verify"
        sk = pymysql_ssl_kwargs(cfg)
        assert "ssl" in sk
        assert sk["ssl"].verify_mode.name == "CERT_NONE"

    def test_dsn_sslmode_required(self):
        cfg = parse_dsn("seekdb://root@host:3306/db?sslmode=REQUIRED")
        assert cfg.ssl_mode == "required"
        sk = pymysql_ssl_kwargs(cfg)
        assert "ssl" in sk

    def test_dsn_tls_alias(self):
        cfg = parse_dsn("seekdb://h/db?tls=require")
        assert cfg.ssl_mode == "required"

    def test_dsn_ssl_pem_paths(self):
        cfg = parse_dsn(
            "seekdb://u:p@h:1/db?ssl_ca=/tmp/ca.pem&ssl_cert=/c.pem&ssl_key=/k.pem"
        )
        assert cfg.ssl_ca == "/tmp/ca.pem"
        sk = pymysql_ssl_kwargs(cfg)
        assert sk["ssl_ca"] == "/tmp/ca.pem"
        assert sk["ssl_cert"] == "/c.pem"
        assert sk["ssl_key"] == "/k.pem"

    def test_invalid_tls_value(self):
        with pytest.raises(ValueError, match="Invalid tls"):
            parse_dsn("seekdb://h/db?tls=not-a-mode")
