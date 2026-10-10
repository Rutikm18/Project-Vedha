"""
Gap #2 — duplicate findings.

Several producers (the detection-engine posture track, the probe self-assessment,
the legacy service_vuln bridge) each raised a finding for the SAME cleartext
service with a DIFFERENT title, and the dedup key was (asset, title), so one
Telnet service became 3 rows. The fix:

  1. The legacy service_vuln cleartext rule is RETIRED (posture is authoritative).
  2. Exposed-service producers stamp a per-port CONDITION key into evidence, and
     dedup matches on (asset, condition) across producers regardless of title.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from app.detection import engine_bridge
from app.discovery.finding_translator import (
    condition_index_key, exposed_service_condition, probe_finding_condition,
)
from app.discovery.service_vuln import create_service_vuln_findings
from app.models.asset import Asset
from app.models.enums import FindingStatus
from app.models.finding import Finding

ENGAGEMENT = uuid.uuid4()
RUN = uuid.uuid4()


class _FakeSession:
    def __init__(self):
        self.added: list = []

    async def execute(self, stmt):
        class _R:
            def scalars(self):
                class _S:
                    def all(self_inner):
                        return []
                return _S()

            def scalar_one_or_none(self):
                return None
        return _R()

    def add(self, obj):
        self.added.append(obj)
        if getattr(obj, "id", None) is None:
            obj.id = uuid.uuid4()

    async def flush(self):
        pass


async def _persist(db, posture, *, open_index=None, cache=None):
    touched: list = []
    return await engine_bridge._persist_posture_findings(
        db, ENGAGEMENT, RUN, datetime.now(timezone.utc), posture, touched,
        "vulndb-1", cache={} if cache is None else cache,
        open_index={} if open_index is None else open_index,
        remediated_index={},
    )


def _exposed_cleartext(asset_ip="10.0.0.5", port=23):
    return {
        "rule_id": "POSTURE-EXPOSED-CLEARTEXT",
        "title": f"Cleartext protocol exposed on {port} (Telnet)",
        "asset_ip": asset_ip, "severity": "high", "state": "confirmed",
        "category": "exposure", "port": port, "remediation": "Disable it.",
        "mitre": "T1040",
    }


# ── unit: the condition helpers ──────────────────────────────────────────────

def test_exposed_service_condition_is_per_port():
    assert exposed_service_condition(23) == "exposed:23"
    assert exposed_service_condition(None) is None


def test_probe_finding_condition_only_for_exposed_classes():
    assert probe_finding_condition({"category": "cleartext_protocol", "port": 23}) == "exposed:23"
    assert probe_finding_condition({"category": "exposure", "port": 3389}) == "exposed:3389"
    # NOT an exposed-service class → no per-port key (so weak-crypto/web on a
    # shared port never wrongly merge).
    assert probe_finding_condition({"category": "weak_crypto", "port": 443}) is None
    assert probe_finding_condition({"category": "cleartext_protocol"}) is None


# ── posture stamps + dedups by the condition key ─────────────────────────────

@pytest.mark.asyncio
async def test_posture_merges_onto_another_producers_finding_by_condition():
    """A probe finding already exists for Telnet/23 under its own title; the
    posture run for the same service must REAFFIRM it (merge), not add a second
    row under the posture title."""
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.5")
    asset.id = uuid.uuid4()
    probe_f = Finding(
        engagement_id=ENGAGEMENT, asset_id=asset.id,
        title="Telnet exposed (cleartext credentials)",
        status=FindingStatus.open, evidence={"dedup_key": "exposed:23"})
    index = {
        (asset.id, probe_f.title): probe_f,
        condition_index_key(asset.id, "exposed:23"): probe_f,
    }

    created, reaffirmed = await _persist(
        db, [_exposed_cleartext()], open_index=index,
        cache={"10.0.0.5": asset})

    assert (created, reaffirmed) == (0, 1)              # merged, no new row
    assert [o for o in db.added if isinstance(o, Finding)] == []
    assert probe_f.detection_run_id == RUN


@pytest.mark.asyncio
async def test_posture_exposed_finding_is_stamped_with_condition():
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.5")
    asset.id = uuid.uuid4()
    created, _ = await _persist(db, [_exposed_cleartext()],
                               cache={"10.0.0.5": asset})
    assert created == 1
    f = next(o for o in db.added if isinstance(o, Finding))
    assert f.evidence.get("dedup_key") == "exposed:23"


@pytest.mark.asyncio
async def test_non_exposed_posture_finding_is_not_port_keyed():
    """A dedicated-scanner finding (RDP-NO-NLA) must NOT get a per-port condition
    key — two distinct real findings can share a port and must stay separate."""
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.6")
    asset.id = uuid.uuid4()
    rdp = {"rule_id": "POSTURE-RDP-NO-NLA", "title": "RDP without NLA",
           "asset_ip": "10.0.0.6", "severity": "high", "state": "confirmed",
           "category": "misconfiguration", "port": 3389, "remediation": "x",
           "mitre": "T1210"}
    created, _ = await _persist(db, [rdp], cache={"10.0.0.6": asset})
    assert created == 1
    f = next(o for o in db.added if isinstance(o, Finding))
    assert "dedup_key" not in (f.evidence or {})


# ── the legacy cleartext producer is retired ─────────────────────────────────

@pytest.mark.asyncio
async def test_service_vuln_no_longer_emits_cleartext():
    db = _FakeSession()
    telnet = {"scan_type": "port_scan", "engine": "nmap",
              "facts": [{"status": "open", "target": "10.0.0.5", "port": 23,
                         "data": {"service": "telnet"}}]}
    with (patch("app.discovery.service_vuln._resolve_asset", AsyncMock(return_value=None)),
          patch("app.discovery.service_vuln._find_open_duplicate", AsyncMock(return_value=None))):
        created = await create_service_vuln_findings(db, ENGAGEMENT, telnet)
    assert created == 0
    assert [o for o in db.added if isinstance(o, Finding)] == []


@pytest.mark.asyncio
async def test_service_vuln_still_emits_ssh_weak_crypto():
    db = _FakeSession()
    ssh = {"scan_type": "port_scan", "engine": "nmap",
           "facts": [{"status": "open", "target": "10.0.0.5", "port": 22,
                      "data": {"service": "ssh", "banner": "SSH-2.0-OpenSSH_7.4\nssh-dss"}}]}
    with (patch("app.discovery.service_vuln._resolve_asset", AsyncMock(return_value=None)),
          patch("app.discovery.service_vuln._find_open_duplicate", AsyncMock(return_value=None))):
        created = await create_service_vuln_findings(db, ENGAGEMENT, ssh)
    assert created == 1


# ── M1: canonical condition key from the rule definition ─────────────────────

def _nfs_dedicated(asset_ip="10.0.0.9"):
    return {
        "rule_id": "POSTURE-NFS-WORLD-READABLE-EXPORT", "title": "NFS export world-readable",
        "asset_ip": asset_ip, "severity": "high", "state": "confirmed",
        "category": "misconfiguration", "port": 2049, "remediation": "Restrict the export.",
        "evidence": {"dedup_key": "exposed:2049"},
    }


def test_probe_udp_exposed_condition_is_distinct_from_tcp():
    assert exposed_service_condition(161, "udp") == "exposed:161/udp"
    assert probe_finding_condition({"category": "amplification", "port": 161, "proto": "udp"}) == "exposed:161/udp"


@pytest.mark.asyncio
async def test_dedicated_scanner_merges_with_port_intel_row_and_keeps_strongest_severity():
    from app.models.enums import FindingSeverity
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.9")
    asset.id = uuid.uuid4()
    port_intel = Finding(
        engagement_id=ENGAGEMENT, asset_id=asset.id,
        title="Network file service exposed on 2049 (NFS) (port 2049)",
        severity=FindingSeverity.medium, status=FindingStatus.open,
        evidence={"dedup_key": "exposed:2049", "rule_id": "POSTURE-EXPOSED-FILESHARE"})
    index = {(asset.id, port_intel.title): port_intel,
             condition_index_key(asset.id, "exposed:2049"): port_intel}

    created, reaffirmed = await _persist(db, [_nfs_dedicated()], open_index=index,
                                         cache={"10.0.0.9": asset})

    assert (created, reaffirmed) == (0, 1)
    assert port_intel.severity == FindingSeverity.high            # strongest signal wins
    rules = {s["rule_id"] for s in port_intel.evidence["signals"]}
    assert rules == {"POSTURE-EXPOSED-FILESHARE", "POSTURE-NFS-WORLD-READABLE-EXPORT"}


@pytest.mark.asyncio
async def test_different_weakness_on_one_port_stays_a_separate_finding():
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.7")
    asset.id = uuid.uuid4()
    base = {"asset_ip": "10.0.0.7", "state": "confirmed", "category": "weak_crypto",
            "port": 443, "remediation": "x", "severity": "medium"}
    cipher = {**base, "rule_id": "POSTURE-TLS-WEAK-CIPHER", "title": "Weak TLS cipher",
              "evidence": {"dedup_key": "tls-weak-cipher:443"}}
    version = {**base, "rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "title": "Deprecated TLS",
               "evidence": {"dedup_key": "tls-deprecated-version:443"}}
    created, reaffirmed = await _persist(db, [cipher, version], cache={"10.0.0.7": asset})
    assert (created, reaffirmed) == (2, 0)
