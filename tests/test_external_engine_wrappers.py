from __future__ import annotations

import subprocess

import pytest

from scanner.mass_scan import (
    _parse_masscan_json_detailed,
    _run_masscan,
    _spec_in_scope,
)
from scanner.nmap_wrapper import (
    NmapExecutionError,
    _parse_nmap_xml,
    _run_nmap,
    _validated_extra_args,
)
from scanner.scanner_base import ScopeGuard


def test_nmap_extra_args_cannot_replace_validated_targets() -> None:
    with pytest.raises(ValueError, match="intentionally blocked"):
        _validated_extra_args("-iL /tmp/unvalidated-targets")

    with pytest.raises(ValueError, match="intentionally blocked"):
        _validated_extra_args("--script intrusive")


def test_nmap_extra_args_accept_bounded_tuning() -> None:
    assert _validated_extra_args(
        "-T3 --max-retries 2 --host-timeout 30s --reason"
    ) == [
        "-T3",
        "--max-retries",
        "2",
        "--host-timeout",
        "30s",
        "--reason",
    ]


def test_nmap_empty_failure_is_not_zero_findings(monkeypatch) -> None:
    monkeypatch.setattr(
        "scanner.nmap_wrapper.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0],
            returncode=1,
            stdout="",
            stderr="requires root privileges",
        ),
    )

    with pytest.raises(NmapExecutionError) as raised:
        _run_nmap(["10.0.0.1"], ["-O"], 30)

    assert raised.value.code == "nonzero_exit"
    assert "requires root" in raised.value.stderr


def test_nmap_malformed_xml_is_an_explicit_parse_error() -> None:
    with pytest.raises(NmapExecutionError) as raised:
        _parse_nmap_xml("<nmaprun><host>", "version")

    assert raised.value.code == "parse_error"


def test_nmap_xml_error_state_is_preserved_as_result() -> None:
    xml = """
    <nmaprun>
      <runstats>
        <finished exit="error" errormsg="failed to open device"/>
      </runstats>
    </nmaprun>
    """

    results = _parse_nmap_xml(xml, "version")
    assert len(results) == 1
    assert results[0].status == "error"
    assert results[0].data["error_code"] == "nonzero_exit"


def test_masscan_tolerates_partial_json_and_counts_bad_records() -> None:
    records, parse_errors = _parse_masscan_json_detailed(
        '[\n{"ip":"10.0.0.1","ports":[]},\nnot-json,\n'
    )

    assert [record["ip"] for record in records] == ["10.0.0.1"]
    assert parse_errors == 1


def test_masscan_timeout_is_not_zero_findings(monkeypatch) -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], timeout=5)

    monkeypatch.setattr("scanner.mass_scan.subprocess.run", timeout)
    run = _run_masscan(["10.0.0.1"], "80", 100, 5, [])

    assert run.outcome == "failed"
    assert run.error_code == "timeout"
    assert run.records == []


def test_masscan_nonzero_with_valid_output_is_degraded(monkeypatch) -> None:
    def partial(cmd, **kwargs):
        output_path = cmd[cmd.index("-oJ") + 1]
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write('[{"ip":"10.0.0.1","ports":[]}]')
        return subprocess.CompletedProcess(
            cmd,
            returncode=1,
            stdout="",
            stderr="adapter stopped",
        )

    monkeypatch.setattr("scanner.mass_scan.subprocess.run", partial)
    run = _run_masscan(["10.0.0.1"], "80", 100, 5, [])

    assert run.outcome == "degraded"
    assert run.error_code == "nonzero_exit"
    assert len(run.records) == 1


def test_masscan_range_must_be_fully_in_scope() -> None:
    scope = ScopeGuard.from_list(
        ["10.0.0.0/24"],
        excludes=["10.0.0.5/32"],
    )

    assert _spec_in_scope("10.0.0.1-10.0.0.4", scope) is True
    assert _spec_in_scope("10.0.0.1-10.0.0.6", scope) is False
