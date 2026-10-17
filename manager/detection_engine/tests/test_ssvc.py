"""CISA SSVC decision for CVE findings (BOD 26-04 prioritisation, roadmap item 7)."""
from __future__ import annotations

import json

import pytest

import ssvc as S
from update_snapshot import parse_vulnrichment, vulnrichment_path

RCE = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"          # automatable, total
LOCAL = "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N"         # not automatable, partial


@pytest.mark.parametrize("e,t,a,m,want", [
    ("active", "total", "yes", "high", "Act"),
    ("active", "total", "yes", "low", "Attend"),
    ("active", "total", "no", "medium", "Attend"),
    ("active", "partial", "no", "low", "Track"),
    ("poc", "total", "yes", "high", "Attend"),
    ("poc", "total", "no", "medium", "Track*"),
    ("none", "total", "no", "high", "Track*"),
    ("none", "partial", "no", "high", "Track"),
])
def test_tree_cells(e, t, a, m, want):
    assert S.decide(e, t, a, m) == want


def test_every_cell_is_a_known_decision():
    for e in ("none", "poc", "active"):
        for t in ("partial", "total"):
            for a in ("no", "yes"):
                for m in ("low", "medium", "high"):
                    assert S.decide(e, t, a, m) in S.DECISIONS


def test_urgency_never_drops_as_inputs_get_worse():
    order = {d: i for i, d in enumerate(S.DECISIONS)}
    for t in ("partial", "total"):
        for a in ("no", "yes"):
            for m in ("low", "medium", "high"):
                ranks = [order[S.decide(e, t, a, m)] for e in ("none", "poc", "active")]
                assert ranks == sorted(ranks), (t, a, m)


def test_unknown_values_fall_back_to_least_urgent():
    assert S.decide("bogus", "bogus", "bogus", "bogus") == "Track"


def test_kev_overrides_published_exploitation():
    db = S.SsvcDB({"CVE-2099-1": {"exploitation": "poc", "automatable": "yes",
                                  "technical_impact": "total"}}, "t")
    r = S.assess("CVE-2099-1", RCE, kev=True, internet_facing=True, db=db)
    assert (r["exploitation"], r["exploitation_source"]) == ("active", "CISA KEV")
    assert r["decision"] == "Act" and r["automatable_source"] == "CISA Vulnrichment"


def test_published_values_beat_the_cvss_derivation():
    # regreSSHion: CISA says automatable "no" although the vector reads network/no-auth.
    db = S.SsvcDB({"CVE-2024-6387": {"exploitation": "poc", "automatable": "no",
                                     "technical_impact": "total"}}, "t")
    r = S.assess("CVE-2024-6387", "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
                 kev=False, internet_facing=False, db=db)
    assert (r["automatable"], r["decision"]) == ("no", "Track*")


def test_without_published_data_the_points_are_derived_and_labelled():
    r = S.assess("CVE-2099-2", LOCAL, kev=False, internet_facing=None, db=S.SsvcDB({}, None))
    assert (r["automatable"], r["technical_impact"]) == ("no", "partial")
    assert r["automatable_source"] == "derived from CVSS vector"
    assert r["exploitation_source"] == "no exploitation data published"
    assert r["decision"] == "Track"


def test_no_vector_no_data_is_unknown_not_invented():
    r = S.assess("CVE-2099-3", None, kev=None, internet_facing=None, db=None)
    assert r["automatable"] is None and r["technical_impact"] is None
    assert r["decision"] == "Track"


def test_missing_snapshot_is_an_empty_db(tmp_path):
    assert S.load_ssvc(tmp_path / "absent.json").get("CVE-2024-6387") is None


def test_vulnrichment_parsing_and_paths():
    doc = {"containers": {"adp": [{"metrics": [{"other": {"type": "ssvc", "content": {
        "timestamp": "2024-07-01T00:00:00Z",
        "options": [{"Exploitation": "poc"}, {"Automatable": "no"},
                    {"Technical Impact": "total"}]}}}]}]}}
    assert parse_vulnrichment(doc) == {"exploitation": "poc", "automatable": "no",
                                       "technical_impact": "total",
                                       "timestamp": "2024-07-01T00:00:00Z"}
    bad = json.loads(json.dumps(doc))
    bad["containers"]["adp"][0]["metrics"][0]["other"]["content"]["options"][0] = {
        "Exploitation": "<script>"}
    assert parse_vulnrichment(bad) is None             # outside the SSVC vocabulary
    assert vulnrichment_path("CVE-2021-44228") == "2021/44xxx/CVE-2021-44228.json"
    assert vulnrichment_path("../../etc/passwd") is None
