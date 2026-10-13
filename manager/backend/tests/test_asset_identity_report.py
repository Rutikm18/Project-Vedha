"""
test_asset_identity_report.py — P1b-5: GET /engagements/{id}/asset-identity.

The operator-facing evidence for choosing per-site identity. The report must make
the merge visible (conflicting names for one private IP, overlapping ranges), must
not cry wolf (same name from two vantages is consistent; overlapping ranges alone
only suggest), and must show the dual-homed machines the graph linked.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.services.asset_identity_report import build_report, load_report, observation_names

NOW = datetime(2026, 10, 8, tzinfo=timezone.utc)
SITE_A, SITE_B = str(uuid.uuid4()), str(uuid.uuid4())


def _asset(ip, host=None, site=None, seen=NOW, fqdn=None):
    return SimpleNamespace(id=uuid.uuid4(), ip_address=ip, hostname=host, fqdn=fqdn, site_id=site, last_seen=seen)


def _fact(ip, **data):
    return {"scanner": "device_inventory", "target": ip, "data": data}


# ── extracting host names from facts ─────────────────────────────────────────

def test_names_are_taken_from_the_usual_keys_and_attributed_to_the_site():
    rows = [(SITE_A, [_fact("10.0.0.5", hostname="FILESRV01"), _fact("10.0.0.6", dns_name="db01.corp")]),
            (SITE_B, [_fact("10.0.0.5:445", netbios_name="NAS-BRANCH")])]
    assert observation_names(rows) == [(SITE_A, "10.0.0.5", "FILESRV01"), (SITE_A, "10.0.0.6", "db01.corp"),
                                       (SITE_B, "10.0.0.5", "NAS-BRANCH")]


def test_facts_without_a_name_or_target_are_ignored():
    rows = [(SITE_A, [{"target": "10.0.0.5"}, _fact("", hostname="x"), _fact("10.0.0.5", hostname="  "),
                      "junk", None, {"target": "10.0.0.5", "data": "str"}])]
    assert observation_names(rows) == []


# ── the report ───────────────────────────────────────────────────────────────

def _sites():
    return [{"site_id": SITE_A, "name": "HQ", "authorized_cidrs": ["10.0.0.0/16"], "assets": 1},
            {"site_id": SITE_B, "name": "Branch", "authorized_cidrs": ["10.0.5.0/24"], "assets": 1}]


def test_merged_machines_are_a_strong_recommendation_to_switch():
    obs = [(SITE_A, "10.0.5.7", "FILESRV01"), (SITE_B, "10.0.5.7", "nas-branch")]
    r = build_report(mode="global", sites=_sites(), observations=obs, assets=[], now=NOW)
    assert r["recommendation"]["action"] == "switch_to_per_site"
    assert r["identity_conflicts"][0]["ip"] == "10.0.5.7"
    assert r["overlapping_private_ranges"][0]["overlap"] == ["10.0.5.0/24"]


def test_overlapping_ranges_alone_only_suggest():
    r = build_report(mode="global", sites=_sites(), observations=[], assets=[], now=NOW)
    assert r["recommendation"]["action"] == "consider_per_site" and r["identity_conflicts"] == []


def test_the_same_name_from_two_sites_is_not_a_conflict():
    obs = [(SITE_A, "10.0.5.7", "FILESRV01"), (SITE_B, "10.0.5.7", "filesrv01.corp")]
    r = build_report(mode="global", sites=_sites(), observations=obs, assets=[], now=NOW)
    assert r["identity_conflicts"] == []


def test_already_per_site_says_so():
    r = build_report(mode="per_site", sites=_sites(), observations=[], assets=[], now=NOW)
    assert r["recommendation"]["action"] == "none" and r["mode"] == "per_site"


def test_no_evidence_keeps_global():
    r = build_report(mode="global", sites=[], observations=[], assets=[_asset("10.0.0.5")], now=NOW)
    assert r["recommendation"]["action"] == "keep_global" and r["assets"] == 1


def test_addresses_already_split_into_several_assets_are_listed():
    a, b = _asset("10.0.0.5", site=SITE_A), _asset("10.0.0.5", site=SITE_B)
    r = build_report(mode="per_site", sites=_sites(), observations=[], assets=[a, b, _asset("10.0.0.6")], now=NOW)
    assert r["addresses_with_several_assets"] == ["10.0.0.5"]


def test_multi_homed_machines_are_shown_with_readable_labels():
    x = _asset("10.0.1.5", host="gateway-app")
    y = _asset("10.0.2.5", host="gateway-app")
    (m,) = build_report(mode="global", sites=[], observations=[], assets=[x, y], now=NOW)["linked_machines"]
    assert m["name"] == "gateway-app" and m["labels"] == ["gateway-app", "gateway-app"] and len(m["members"]) == 2


def test_stale_assets_are_counted_and_the_window_is_reported():
    old = _asset("10.0.0.5", seen=NOW - timedelta(days=90))
    r = build_report(mode="global", sites=[], observations=[], assets=[old, _asset("10.0.0.6")], now=NOW,
                     freshness_days=30)
    assert r["stale_assets"] == {"count": 1, "window_days": 30, "asset_ids": [str(old.id)]}


def test_the_report_says_how_much_evidence_it_looked_at():
    assert build_report(mode="global", sites=[], observations=[], assets=[], now=NOW,
                        sampled_results=500)["evidence_sampled_from"] == 500


# ── the DB adapter ───────────────────────────────────────────────────────────

class _Result:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows

    def scalars(self):
        return SimpleNamespace(all=lambda: self._rows)


class FakeDB:
    def __init__(self, assets, scan_rows, sites):
        self.assets, self.scan_rows, self.sites = assets, scan_rows, sites

    async def execute(self, stmt):
        sql = str(stmt).lower()
        if "from scan_results" in sql:
            return _Result(self.scan_rows)
        if "from assets" in sql:
            return _Result(self.assets)
        if "from probe_sites" in sql:
            return _Result(self.sites)
        raise AssertionError(sql)


def test_load_report_assembles_sites_assets_and_evidence():
    a = _asset("10.0.5.7", host="filesrv01", site=SITE_A)
    sites = [SimpleNamespace(id=uuid.UUID(SITE_A), name="HQ", authorized_cidrs=["10.0.0.0/16"]),
             SimpleNamespace(id=uuid.UUID(SITE_B), name="Branch", authorized_cidrs=["10.0.5.0/24"])]
    scan_rows = [(uuid.UUID(SITE_A), [_fact("10.0.5.7", hostname="FILESRV01")]),
                 (uuid.UUID(SITE_B), [_fact("10.0.5.7", hostname="nas-branch")])]
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement={"attack_path_freshness_days": 7})
    report = asyncio.run(load_report(FakeDB([a], scan_rows, sites), eng, now=NOW))
    assert report["mode"] == "global" and report["recommendation"]["action"] == "switch_to_per_site"
    assert [s["name"] for s in report["sites"]] == ["Branch", "HQ"]
    assert next(s for s in report["sites"] if s["name"] == "HQ")["assets"] == 1
    assert report["stale_assets"]["window_days"] == 7 and report["evidence_sampled_from"] == 2


def test_load_report_with_no_sites_or_scans_is_a_calm_empty_report():
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement=None)
    report = asyncio.run(load_report(FakeDB([], [], []), eng, now=NOW))
    assert report["sites"] == [] and report["recommendation"]["action"] == "keep_global"
