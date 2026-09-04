"""
Run-scoped facts must not be scope-checked as if they were hosts.

THE BUG THIS LOCKS OUT (observed in production 2026-09-03):
  A `network_va` job completed normally, the probe submitted its results, and the
  manager rejected the ENTIRE payload with 422:

      job.result_scope_rejected
        rejected=[{'path': 'facts[0].target', 'value': 'auto'}]
      POST /agents/{id}/jobs/{job}/result -> 422 Unprocessable Entity

  `ipv6_discovery` describes the SCAN RUN, not a host: its `target` is the local
  interface that was swept, or the literal string "auto" when none resolved. The
  scope gate treated that as a network identity, found it wasn't inside the
  engagement CIDRs, and permanently rejected the whole result — including every
  legitimate finding in it. The job then sat `running` until its lease expired,
  was requeued, exhausted max_attempts, and finally failed. From the dashboard
  that looks exactly like "stuck in scanning phase, no results".

  The probe already knows these records aren't hosts — agent/engine.py skips
  `_RUN_SCOPED_SCANNERS` during asset promotion precisely so a phantom asset
  named "auto" isn't invented. The manager simply lacked the same exemption.

The gate itself must keep working: a genuinely out-of-scope HOST is still a
hard rejection. That is the security control and these tests pin it down.
"""
from __future__ import annotations

import pytest

from app.services.job_result_service import (
    _result_network_identities,
    validate_result_scope,
)

SCOPE = ["192.168.1.65/32"]


def _fact(scanner: str, target: str, **extra):
    return {"scanner": scanner, "target": target, "status": "observed", **extra}


class TestRunScopedFactsAreExempt:
    def test_ipv6_discovery_auto_target_is_not_rejected(self):
        """The exact payload that caused the 422."""
        result = {"facts": [_fact("ipv6_discovery", "auto")]}
        assert validate_result_scope(result, SCOPE) == []

    def test_ipv6_discovery_interface_name_is_not_rejected(self):
        """Same record, but an interface actually resolved — still not a host."""
        result = {"facts": [_fact("ipv6_discovery", "en0")]}
        assert validate_result_scope(result, SCOPE) == []

    def test_run_scoped_fact_is_not_collected_as_an_identity(self):
        ids = _result_network_identities({"facts": [_fact("ipv6_discovery", "auto")]})
        assert ids == []

    def test_a_real_result_with_one_run_scoped_fact_is_accepted_whole(self):
        """The damage was collateral: one non-host descriptor discarded every
        legitimate finding alongside it."""
        result = {
            "facts": [
                _fact("ipv6_discovery", "auto"),
                _fact("port_scan", "192.168.1.65", status="open", port=445),
            ],
            "findings": [{"rule_id": "SMB-V1-ENABLED", "target": "192.168.1.65"}],
            "hosts": [{"ip": "192.168.1.65"}],
        }
        assert validate_result_scope(result, SCOPE) == []


class TestTheScopeGateStillWorks:
    """The exemption must be narrow. These are the security assertions."""

    def test_out_of_scope_host_fact_is_still_rejected(self):
        result = {"facts": [_fact("port_scan", "10.9.9.9", status="open")]}
        rejected = validate_result_scope(result, SCOPE)
        assert [r["value"] for r in rejected] == ["10.9.9.9"]

    def test_out_of_scope_host_row_is_still_rejected(self):
        result = {"hosts": [{"ip": "8.8.8.8"}]}
        assert validate_result_scope(result, SCOPE) != []

    def test_out_of_scope_finding_is_still_rejected(self):
        result = {"findings": [{"rule_id": "X", "target": "172.16.0.1"}]}
        assert validate_result_scope(result, SCOPE) != []

    def test_an_unknown_scanner_gets_no_exemption(self):
        """Only the documented run-scoped scanners are exempt — a scanner name
        the manager doesn't recognise must not become a scope bypass."""
        result = {"facts": [_fact("totally_made_up_scanner", "10.9.9.9")]}
        assert validate_result_scope(result, SCOPE) != []

    def test_run_scoped_name_does_not_launder_an_out_of_scope_host(self):
        """The exemption skips the record entirely rather than trusting its
        target, so labelling a fact `ipv6_discovery` cannot smuggle a host into
        the asset inventory — it contributes no identity at all."""
        ids = _result_network_identities(
            {"facts": [_fact("ipv6_discovery", "10.9.9.9")]})
        assert ids == []

    def test_hostname_target_is_still_refused(self):
        """Authorization is IP/CIDR-only; a hostname must not pass."""
        result = {"facts": [_fact("port_scan", "evil.example.com")]}
        assert validate_result_scope(result, SCOPE) != []

    def test_excluded_cidr_still_wins(self):
        result = {"facts": [_fact("port_scan", "192.168.1.65", status="open")]}
        assert validate_result_scope(result, SCOPE, ["192.168.1.65/32"]) != []

    def test_scanner_control_record_exemption_is_unchanged(self):
        """The pre-existing <nmap-run> exemption this fix is modelled on."""
        assert validate_result_scope(
            {"facts": [_fact("nmap", "<nmap-run>")]}, SCOPE) == []
