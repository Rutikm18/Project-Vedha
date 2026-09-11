"""Phase 2 — config loader: single precedence chain + effective source map.
Pure logic — no IO."""
from __future__ import annotations

from agent import config_model as cm


def test_parse_env_file_ignores_comments_and_blanks():
    text = "# comment\n\nPLATFORM_URL=https://m.example.com\nPROBE_NAME=host-1\n"
    d = cm.parse_env_file(text)
    assert d == {"PLATFORM_URL": "https://m.example.com", "PROBE_NAME": "host-1"}


def test_precedence_cli_beats_env_beats_probe_env_beats_default():
    values, sources = cm.resolve(
        cli={"manager_url": "https://cli"},
        env={"PLATFORM_URL": "https://env"},
        probe_env={"PLATFORM_URL": "https://file", "PROBE_NAME": "file-name"},
        pushed={},
    )
    assert values["manager_url"] == "https://cli"
    assert sources["manager_url"] == "cli"
    # name only in probe.env → wins there
    assert values["name"] == "file-name"
    assert sources["name"] == "probe.env"
    # nothing set → default with source 'default'
    assert sources["heartbeat_interval"] == "default"
    assert values["heartbeat_interval"] == 30


def test_verify_tls_is_coerced_to_bool():
    values, _ = cm.resolve(cli={}, env={"VERIFY_TLS": "false"}, probe_env={}, pushed={})
    assert values["verify_tls"] is False
    values2, _ = cm.resolve(cli={}, env={"VERIFY_TLS": "true"}, probe_env={}, pushed={})
    assert values2["verify_tls"] is True


def test_int_fields_are_coerced():
    values, _ = cm.resolve(cli={}, env={"HEARTBEAT_INTERVAL": "45"}, probe_env={}, pushed={})
    assert values["heartbeat_interval"] == 45 and isinstance(values["heartbeat_interval"], int)


def test_render_effective_lists_value_and_source():
    values, sources = cm.resolve(cli={"name": "cli-name"}, env={}, probe_env={}, pushed={})
    rows = cm.render_effective(values, sources)
    row = {r[0]: r for r in rows}["name"]
    assert row[1] == "cli-name" and row[2] == "cli"
