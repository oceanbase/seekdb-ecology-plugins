"""Tests for internal table filtering in schema commands."""

import pytest

from seekdb_cli.commands.schema import _is_hidden_schema_table


@pytest.mark.parametrize(
    "name,hidden",
    [
        ("sdk_collections", True),
        ("SDK_COLLECTIONS", True),
        ("c$v_foo", True),
        ("C$V_bar", True),
        ("my_table", False),
        ("c$other", False),
        ("cv_nope", False),
    ],
)
def test_is_hidden_schema_table(name: str, hidden: bool) -> None:
    assert _is_hidden_schema_table(name) is hidden
