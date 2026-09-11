"""Phase 8 — observability: redacted structured logs, low-cardinality heartbeat
metrics, IP masking, redacted diagnostics bundle. Pure."""
from __future__ import annotations

import json

from agent import obs


def test_redact_masks_sensitive_keys_only():
    r = obs.redact({"manager_url": "https://m", "PROBE_PAT": "vpat_x", "authorization": "Bearer y"})
    assert r["manager_url"] == "https://m"
    assert r["PROBE_PAT"] == "[REDACTED]"
    assert r["authorization"] == "[REDACTED]"


def test_log_line_is_json_and_redacts():
    line = obs.log_line("info", "enroll", {"token": "vet_secret", "mode": "pairing"},
                        ts=1700.0, corr_id="abc")
    rec = json.loads(line)
    assert rec["level"] == "info" and rec["event"] == "enroll" and rec["corr_id"] == "abc"
    assert rec["mode"] == "pairing"
    assert rec["token"] == "[REDACTED]"
    assert "vet_secret" not in line


def test_mask_ip_hides_host_octet():
    assert obs.mask_ip("10.20.30.40") == "10.20.30.x"
    assert obs.mask_ip("not-an-ip") == "not-an-ip"


def test_heartbeat_metrics_are_low_cardinality():
    m = obs.heartbeat_metrics(
        version="1.0.0", os_name="linux", artifact_hash="deadbeef",
        since_last_contact_s=12, queue_depth=3, oldest_unsent_age_s=40.0,
        job_outcomes={"success": 5, "fatal": 1}, restart_count=2,
        last_exit_class="retryable", rss_bytes=1024, cpu_pct=1.5, privileged=False)
    # bounded key set — NO per-target / per-host labels (they'd melt a TSDB)
    for k in m:
        low = k.lower()
        assert "ip" not in low and "host" not in low and "target" not in low, k
    assert m["queue_depth"] == 3 and m["last_exit_class"] == "retryable"


def test_diagnostics_bundle_is_redacted():
    from agent.doctor import Check
    bundle = obs.build_diagnostics(
        config_values={"manager_url": "https://m", "VEDHA_PAT": "vpat_secret"},
        doctor_checks=[Check("python", "pass", "3.12")],
        interfaces=[{"name": "eth0", "kind": "physical", "addresses": ["10.20.0.5/24"]}],
        recent_logs=["line1"], clock_offset_s=2.0)
    text = json.dumps(bundle)
    assert "vpat_secret" not in text                 # config secret redacted
    assert "10.20.0.5" not in text                   # own IP masked in the bundle
    assert bundle["doctor"][0]["name"] == "python"
    assert bundle["clock_offset_s"] == 2.0
