"""Phase 3 — exit-state protocol (0b contract): 5 classes, reason->class map,
exit-state.json + structured stderr line. Pure."""
from __future__ import annotations

from agent import exit_state as es


def test_reason_maps_to_class_and_code():
    assert es.class_for_reason("manager-unreachable") == "retryable"
    assert es.class_for_reason("empty-scope") == "fatal-config"
    assert es.class_for_reason("cert-expired") == "fatal-identity"
    assert es.class_for_reason("pairing-pending") == "awaiting-approval"
    assert es.class_for_reason("clean-shutdown") == "success"
    assert es.code_for_reason("empty-scope") == 20


def test_unknown_reason_defaults_to_retryable():
    # An unknown reason must not hard-stop; it's bounded by the supervisor's cap.
    assert es.class_for_reason("some-new-thing") == "retryable"


def test_class_for_code_roundtrip():
    for cls, code in es.CLASSES.items():
        assert es.class_for_code(code) == cls
    assert es.class_for_code(999) == "retryable"   # unknown code → retryable


def test_json_roundtrip(tmp_path):
    st = es.make("cert-expired", "renew the client certificate", at_monotonic=12.5)
    text = es.to_json(st)
    back = es.from_json(text)
    assert back.reason == "cert-expired"
    assert back.cls == "fatal-identity" and back.code == 30
    assert back.contract_version == es.CONTRACT_VERSION
    # write/read on disk
    p = tmp_path / "exit-state.json"
    es.write(str(p), st)
    assert es.read(str(p)).reason == "cert-expired"


def test_stderr_line_emit_and_parse():
    st = es.make("manager-unreachable", "check egress 443")
    line = es.stderr_line(st)
    assert line.startswith("VEDHA-EXIT retryable manager-unreachable")
    cls, reason, rem = es.parse_stderr_line(line)
    assert cls == "retryable" and reason == "manager-unreachable" and "egress" in rem


def test_parse_stderr_line_ignores_noise():
    assert es.parse_stderr_line("some unrelated log line") is None
