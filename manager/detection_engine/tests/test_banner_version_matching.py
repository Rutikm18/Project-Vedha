"""
Banner versions against Debian package bounds (matcher revision 2).

A network banner shows the UPSTREAM version; the OSV snapshot's bounds are Debian
package versions with an epoch, a revision and sometimes a "+dfsg" tag. These tests
pin the three ways the matcher now reads a banner (plain upstream build, Debian build
with its package revision, other backporting distro build) and the two field bugs that
motivated it: vsftpd 2.3.4 / 3.0.5 reported for CVEs fixed in that very release, and
OpenSSH 9.6p1 never matched against regreSSHion because every OpenSSH bound has an
epoch.
"""
from __future__ import annotations

import pytest

from cpe_normalizer import CPECandidate, detect_build, normalize_banner
from matcher import MATCHER_REVISION, match_candidate
from models import Fact, FindingState, SourceConfidence
from vuln_db import SnapshotMeta, VulnDB, _content_hash, load_snapshot


def _db(records):
    meta = SnapshotMeta(fetched_at="2026-01-01T00:00:00Z", ecosystem="Debian:12",
                        products=list(records), content_hash=_content_hash(records),
                        path="test.json")
    return VulnDB(records, meta)


def _rec(cve, pkg, *ranges):
    """One OSV record; each range is (ecosystem, events)."""
    return {"id": f"DEBIAN-{cve}", "upstream": [cve],
            "affected": [{"package": {"name": pkg, "ecosystem": eco},
                          "ranges": [{"type": "ECOSYSTEM", "events": events}]}
                         for eco, events in ranges]}


def _cand(version, pkg="vsftpd", distro=None, revision=None,
          source=SourceConfidence.inferred):
    return CPECandidate(vendor="v", product=pkg, lookup_key=pkg,
                        version_raw=version, version_normalized=version,
                        confidence="low", source_confidence=source,
                        basis="banner", source_ref="t.jsonl:1",
                        distro=distro, distro_revision=revision)


def _cves(findings):
    return {f.cve_id: f for f in findings}


# ── plain upstream build ──────────────────────────────────────────────────────

class TestUpstreamBuild:
    def test_release_that_carries_the_fix_is_not_vulnerable(self):
        # vsftpd field FP: Debian fixed it by packaging upstream 3.0.5 ("-0.1").
        db = _db({"vsftpd": [_rec("CVE-2021-3618", "vsftpd",
                                  ("Debian:13", [{"introduced": "0"}, {"fixed": "3.0.5-0.1"}]))]})
        assert match_candidate("10.0.0.1", _cand("3.0.5"), db) == []
        assert set(_cves(match_candidate("10.0.0.1", _cand("3.0.4"), db))) == {"CVE-2021-3618"}

    def test_first_packaging_revision_one(self):
        db = _db({"vsftpd": [_rec("CVE-2011-0762", "vsftpd",
                                  ("Debian:11", [{"introduced": "0"}, {"fixed": "2.3.4-1"}]))]})
        assert match_candidate("10.0.0.1", _cand("2.3.4"), db) == []
        assert match_candidate("10.0.0.1", _cand("2.3.2"), db)

    def test_stable_backport_of_a_new_upstream_counts_as_first_packaging(self):
        db = _db({"apache2": [_rec("CVE-2024-40725", "apache2",
                                   ("Debian:11", [{"introduced": "0"},
                                                  {"fixed": "2.4.62-1~deb11u1"}]))]})
        assert match_candidate("10.0.0.1", _cand("2.4.62", "apache2"), db) == []
        assert match_candidate("10.0.0.1", _cand("2.4.61", "apache2"), db)

    def test_debian_patch_revision_keeps_the_upstream_release_vulnerable(self):
        # Fixed by Debian's own patch on 3.0.3: upstream 3.0.3 is still vulnerable.
        db = _db({"vsftpd": [_rec("CVE-2099-0001", "vsftpd",
                                  ("Debian:11", [{"introduced": "0"},
                                                 {"fixed": "3.0.3-12+deb11u1"}]))]})
        f = _cves(match_candidate("10.0.0.1", _cand("3.0.3"), db))["CVE-2099-0001"]
        assert f.state == FindingState.suspected and f.match_basis == "range"
        assert any("backport-possible" in n for n in f.notes)

    def test_epoch_bound_is_compared_not_skipped(self):
        # regreSSHion shape: every OpenSSH bound carries epoch 1.
        db = _db({"openssh": [_rec("CVE-2024-6387", "openssh",
                                   ("Debian:13", [{"introduced": "1:8.5p1-1"},
                                                  {"fixed": "1:9.8p1-1"}]))]})
        assert set(_cves(match_candidate("10.0.0.1", _cand("9.6p1", "openssh"), db))) \
            == {"CVE-2024-6387"}
        assert match_candidate("10.0.0.1", _cand("9.8p1", "openssh"), db) == []
        assert match_candidate("10.0.0.1", _cand("8.4p1", "openssh"), db) == []

    def test_repack_suffix_is_ignored(self):
        db = _db({"proftpd-dfsg": [_rec("CVE-2099-0002", "proftpd-dfsg",
                                        ("Debian:12", [{"introduced": "0"},
                                                       {"fixed": "1.3.8+dfsg-1"}]))]})
        assert match_candidate("10.0.0.1", _cand("1.3.8", "proftpd-dfsg"), db) == []
        assert match_candidate("10.0.0.1", _cand("1.3.7", "proftpd-dfsg"), db)

    def test_open_range_in_one_release_ignored_once_past_another_releases_fix(self):
        # Debian 11 never shipped a fix; Debian 13 fixed it by packaging 3.0.5.
        db = _db({"vsftpd": [_rec("CVE-2021-3618", "vsftpd",
                                  ("Debian:11", [{"introduced": "0"}]),
                                  ("Debian:13", [{"introduced": "0"}, {"fixed": "3.0.5-0.1"}]))]})
        assert match_candidate("10.0.0.1", _cand("3.0.5"), db) == []

    def test_regressed_range_is_not_a_fix(self):
        # fixed at 2.0 then re-introduced at 3.0: 3.5 is still vulnerable.
        db = _db({"vsftpd": [_rec("CVE-2099-0003", "vsftpd",
                                  ("Debian:12", [{"introduced": "0"}, {"fixed": "2.0-1"},
                                                 {"introduced": "3.0-1"}]))]})
        f = _cves(match_candidate("10.0.0.1", _cand("3.5"), db))["CVE-2099-0003"]
        assert f.match_basis == "range-open"

    def test_matcher_revision_is_stamped(self):
        db = _db({"vsftpd": [_rec("CVE-2099-0004", "vsftpd",
                                  ("Debian:12", [{"introduced": "0"}, {"fixed": "9.0-1"}]))]})
        (f,) = match_candidate("10.0.0.1", _cand("1.0"), db)
        assert f.matcher_revision == MATCHER_REVISION == "4"

    def test_authoritative_dpkg_order_is_unchanged(self):
        # The host's own package version keeps exact dpkg semantics.
        db = _db({"vsftpd": [_rec("CVE-2099-0005", "vsftpd",
                                  ("Debian:12", [{"introduced": "0"}, {"fixed": "3.0.3-13+deb12u1"}]))]})
        auth = SourceConfidence.authoritative
        assert match_candidate("10.0.0.1", _cand("3.0.3-13", source=auth), db)
        assert match_candidate("10.0.0.1", _cand("3.0.3-13+deb12u1", source=auth), db) == []


# ── Debian build with its package revision in the banner ──────────────────────

_REGRESSHION_DEBIAN = {"openssh": [_rec(
    "CVE-2024-6387", "openssh",
    ("Debian:12", [{"introduced": "1:8.5p1-1"}, {"fixed": "1:9.2p1-2+deb12u3"}]),
    ("Debian:13", [{"introduced": "1:8.5p1-1"}, {"fixed": "1:9.7p1-7"}]),
)]}


class TestDebianRevision:
    def test_patched_package_is_not_vulnerable(self):
        db = _db(_REGRESSHION_DEBIAN)
        c = _cand("9.2p1", "openssh", distro="debian", revision="2+deb12u3")
        assert match_candidate("10.0.0.1", c, db) == []

    def test_other_release_bound_does_not_leak_in(self):
        # Debian 13's fix (9.7p1-7) must not judge a Debian 12 package.
        db = _db(_REGRESSHION_DEBIAN)
        c = _cand("9.2p1", "openssh", distro="debian", revision="2+deb12u4")
        assert match_candidate("10.0.0.1", c, db) == []

    def test_unpatched_package_is_suspected_without_backport_caveat(self):
        db = _db(_REGRESSHION_DEBIAN)
        c = _cand("9.2p1", "openssh", distro="debian", revision="2+deb12u2")
        f = _cves(match_candidate("10.0.0.1", c, db))["CVE-2024-6387"]
        assert f.state == FindingState.suspected and f.match_basis == "range"
        assert not any("backport-possible" in n for n in f.notes)
        assert any("Debian 12" in n for n in f.notes)

    def test_release_not_named_needs_every_release_to_agree(self):
        db = _db(_REGRESSHION_DEBIAN)
        # "Debian-2": 9.2p1-2 is below both releases' fixes -> vulnerable in both.
        assert match_candidate("10.0.0.1", _cand("9.2p1", "openssh", "debian", "2"), db)
        # "Debian-1" on 9.3p1: past Debian 12's fix, below Debian 13's -> the
        # releases disagree, so no finding (one release already ships it fixed).
        assert match_candidate("10.0.0.1", _cand("9.3p1", "openssh", "debian", "1"), db) == []

    def test_release_without_a_record_is_not_affected(self):
        db = _db({"openssh": [_rec("CVE-2099-0006", "openssh",
                                   ("Debian:11", [{"introduced": "0"}, {"fixed": "1:8.4p1-6"}]))]})
        c = _cand("9.2p1", "openssh", distro="debian", revision="2+deb12u3")
        assert match_candidate("10.0.0.1", c, db) == []


# ── other backporting distro builds ───────────────────────────────────────────

class TestDistroBuild:
    def test_ubuntu_build_is_product_presence(self):
        db = _db(_REGRESSHION_DEBIAN)
        (f,) = match_candidate("10.0.0.1", _cand("8.9p1", "openssh", distro="ubuntu"), db)
        assert f.state == FindingState.potential and f.match_basis == "range-distro"
        assert any("ubuntu build" in n for n in f.notes)

    def test_pipeline_keeps_distro_matches_out_of_the_customer_set(self, tmp_path):
        import json
        from pipeline import run_full_detection
        from enrichment_db import EpssDB, KevDB
        rec = {"scanner": "service_banner", "target": "10.0.0.7",
               "timestamp": "2026-01-01T00:00:00Z", "port": 22, "proto": "tcp",
               "status": "open", "evidence": None, "error": None,
               "data": {"first_line": "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10",
                        "service": "ssh", "product": "OpenSSH", "version": "8.9p1"}}
        p = tmp_path / "f.jsonl"
        p.write_text(json.dumps(rec) + "\n")
        res = run_full_detection([str(p)], vuln_db=_db(_REGRESSHION_DEBIAN),
                                 kev_db=KevDB(cve_ids=set(), fetched_at="x"),
                                 epss_db=EpssDB(scores={}, fetched_at="x"))
        assert res["cve"] == []
        assert [f.cve_id for f in res["cve_product_presence"]] == ["CVE-2024-6387"]
        assert res["matcher_revision"] == MATCHER_REVISION


# ── banner parsing ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text,expected", [
    ("SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3", ("debian", "2+deb12u3")),
    ("SSH-2.0-OpenSSH_9.2p1 Raspbian-2+deb12u3", ("debian", "2+deb12u3")),
    ("SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10", ("ubuntu", None)),
    ("SSH-2.0-OpenSSH_for_Windows_9.5", ("windows", None)),
    ("SSH-2.0-OpenSSH_9.6 FreeBSD-20240104", ("freebsd", None)),
    ("Apache/2.4.57 (Debian)", ("debian", None)),
    ("Apache/2.4.37 (Red Hat Enterprise Linux)", ("rhel", None)),
    ("nginx/1.18.0 (Ubuntu)", ("ubuntu", None)),
    ("10.11.6-MariaDB-0+deb12u1", ("debian", "0+deb12u1")),
    ("10.6.18-MariaDB-0ubuntu0.22.04.1", ("ubuntu", None)),
    # upstream builds: no backporting distro
    ("SSH-2.0-OpenSSH_7.4", (None, None)),
    ("220 (vsFTPd 3.0.3)", (None, None)),
    ("Apache/2.4.58 (Win64) OpenSSL/3.1.3", (None, None)),
    ("10.6.12-MariaDB-1:10.6.12+maria~ubu2004", (None, None)),
])
def test_detect_build(text, expected):
    assert detect_build(text) == expected


def test_openssh_for_windows_version_is_parsed():
    fact = Fact(scanner="service_banner", target="10.0.0.9", timestamp="", port=22,
                proto="tcp", status="open",
                data={"first_line": "SSH-2.0-OpenSSH_for_Windows_9.5", "service": "ssh",
                      "product": "OpenSSH", "version": "for_Windows_9.5"},
                evidence=None, error=None, source_confidence=SourceConfidence.inferred,
                source_file="f", source_line=1)
    (c,) = normalize_banner(fact)
    assert c.version_raw == "9.5" and c.distro == "windows"


def test_debian_banner_fact_carries_the_revision():
    fact = Fact(scanner="service_banner", target="10.0.0.9", timestamp="", port=22,
                proto="tcp", status="open",
                data={"first_line": "SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3",
                      "service": "ssh", "product": "OpenSSH", "version": "9.2p1"},
                evidence=None, error=None, source_confidence=SourceConfidence.inferred,
                source_file="f", source_line=1)
    (c,) = normalize_banner(fact)
    assert (c.distro, c.distro_revision) == ("debian", "2+deb12u3")


# ── the shipped snapshot (the field cases) ────────────────────────────────────

@pytest.fixture(scope="module")
def db():
    return load_snapshot()


class TestShippedSnapshot:
    def _match(self, db, pkg, version, **kw):
        return {f.cve_id: f for f in match_candidate("10.0.0.1", _cand(version, pkg, **kw), db)}

    def test_vsftpd_305_has_no_cve(self, db):
        assert self._match(db, "vsftpd", "3.0.5") == {}

    def test_vsftpd_234_keeps_only_the_cves_after_it(self, db):
        assert set(self._match(db, "vsftpd", "2.3.4")) == {"CVE-2015-1419", "CVE-2021-3618"}

    def test_openssh_96_matches_regresshion_98_does_not(self, db):
        assert self._match(db, "openssh", "9.6p1")["CVE-2024-6387"].match_basis == "range"
        assert "CVE-2024-6387" not in self._match(db, "openssh", "9.8p1")

    def test_patched_debian_12_openssh_has_no_regresshion(self, db):
        got = self._match(db, "openssh", "9.2p1", distro="debian", revision="2+deb12u3")
        assert "CVE-2024-6387" not in got


def test_build_is_read_from_the_identifying_line_only():
    # An upstream nginx whose page body and Location mention Ubuntu is still an
    # upstream build: its CVEs must not be hidden as distro product presence.
    fact = Fact(scanner="service_banner", target="10.0.0.9", timestamp="", port=80,
                proto="tcp", status="open",
                data={"first_line": "HTTP/1.1 200 OK", "http_status": 200,
                      "http_server": "nginx/1.25.3", "product": "nginx", "version": "1.25.3",
                      "banner": "HTTP/1.1 200 OK\r\nServer: nginx/1.25.3\r\n"
                                "Location: http://ubuntu-web01/\r\n\r\nWelcome to Ubuntu"},
                evidence=None, error=None, source_confidence=SourceConfidence.inferred,
                source_file="f", source_line=1)
    (c,) = normalize_banner(fact)
    assert c.distro is None
    fact.data["http_server"] = "nginx/1.18.0 (Ubuntu)"
    (c,) = normalize_banner(fact)
    assert c.distro == "ubuntu"


@pytest.mark.parametrize("garbage", ["", "-rc1", "unknown", "x9.6"])
def test_non_numeric_banner_version_matches_nothing(garbage):
    db = _db({"vsftpd": [_rec("CVE-2099-0007", "vsftpd",
                              ("Debian:12", [{"introduced": "0"}, {"fixed": "3.0.5-1"}]))]})
    c = _cand(garbage)
    c.version_raw = c.version_normalized = garbage or "-"
    assert match_candidate("10.0.0.1", c, db) == []


# ── finding fields a client reads first (gap: CVE finding quality) ────────────

class TestFixVersionAndLocation:
    def test_banner_finding_names_the_upstream_fix(self):
        db = _db({"openssh": [_rec("CVE-2024-6387", "openssh",
                                   ("Debian:13", [{"introduced": "1:8.5p1-1"},
                                                  {"fixed": "1:9.8p1-1"}]))]})
        (f,) = match_candidate("10.0.0.1", _cand("9.6p1", "openssh"), db)
        assert (f.fixed_version, f.fixed_version_raw, f.version_scheme) == \
            ("9.8p1", "1:9.8p1-1", "upstream")

    def test_debian_patch_only_fix_has_no_upstream_target(self):
        db = _db({"vsftpd": [_rec("CVE-2099-0008", "vsftpd",
                                  ("Debian:11", [{"introduced": "0"},
                                                 {"fixed": "3.0.3-12+deb11u1"}]))]})
        (f,) = match_candidate("10.0.0.1", _cand("3.0.3"), db)
        assert f.fixed_version is None and f.fixed_version_raw == "3.0.3-12+deb11u1"

    def test_package_version_keeps_the_package_fix(self):
        db = _db(_REGRESSHION_DEBIAN)
        (f,) = match_candidate("10.0.0.1", _cand("9.2p1", "openssh", "debian", "2+deb12u2"), db)
        assert (f.fixed_version, f.version_scheme) == ("1:9.2p1-2+deb12u3", "package")

    def test_port_and_product_reach_the_finding_through_the_pipeline(self, tmp_path):
        import json
        from pipeline import run_full_detection
        from enrichment_db import EpssDB, KevDB
        rows = [{"scanner": "service_banner", "target": "10.0.0.8", "port": port,
                 "timestamp": "2026-01-01T00:00:00Z", "proto": "tcp", "status": "open",
                 "evidence": None, "error": None,
                 "data": {"first_line": "220 (vsFTPd 3.0.3)", "service": "ftp",
                          "product": "vsftpd", "version": "3.0.3"}} for port in (21, 2121)]
        p = tmp_path / "f.jsonl"
        p.write_text("".join(json.dumps(r) + "\n" for r in rows))
        db = _db({"vsftpd": [_rec("CVE-2021-3618", "vsftpd",
                                  ("Debian:13", [{"introduced": "0"}, {"fixed": "3.0.5-0.1"}]))]})
        res = run_full_detection([str(p)], vuln_db=db,
                                 kev_db=KevDB(cve_ids=set(), fetched_at="x"),
                                 epss_db=EpssDB(scores={}, fetched_at="x"))
        (f,) = res["cve"]
        d = f.to_dict()
        assert (d["port"], d["proto"], d["product"]) == (21, "tcp", "vsftpd")
        assert d["ports"] == [21, 2121]
        assert d["fixed_version"] == "3.0.5"


# ── OpenSSH builds that omit the portable suffix (lab finding, 17 Oct) ────────
# Alpine, macOS and Microsoft's port announce "OpenSSH_10.3", not "OpenSSH_10.3p1".
# The accuracy lab's current OpenSSH 10.3 showed five CVEs "fixed in 10.3p1".

class TestPortableSuffix:
    def _db(self, fixed):
        return _db({"openssh": [_rec("CVE-2099-0100", "openssh",
                                     ("Debian:13", [{"introduced": "0"}, {"fixed": fixed}]))]})

    def test_p1_fix_is_already_in_any_build_of_that_release(self):
        assert match_candidate("10.0.0.1", _cand("10.3", "openssh"), self._db("1:10.3p1-1")) == []

    def test_older_release_still_matches(self):
        assert match_candidate("10.0.0.1", _cand("10.2", "openssh"), self._db("1:10.3p1-1"))

    def test_p2_fix_cannot_be_judged_from_a_suffixless_banner(self):
        # "9.3" may be 9.3p1 (vulnerable) or 9.3p2 (fixed): no claim either way.
        assert match_candidate("10.0.0.1", _cand("9.3", "openssh"), self._db("1:9.3p2-1")) == []

    def test_suffixed_banner_is_unchanged(self):
        assert match_candidate("10.0.0.1", _cand("9.3p1", "openssh"), self._db("1:9.3p2-1"))
        assert match_candidate("10.0.0.1", _cand("9.3p2", "openssh"), self._db("1:9.3p2-1")) == []


# ── matcher revision 4: lab findings on Redis / MariaDB (17 Oct) ──────────────

class TestRevisionShapes:
    @pytest.mark.parametrize("rev,first", [
        ("1", True), ("0", True), ("0.1", True), (None, True),
        ("1~deb11u1", True), ("1~bpo11+1", True),
        ("1+deb12u1", False),      # stable/security update: Debian's own patch
        ("1~deb12u4", False),      # 4th update of a stable rebuild
        ("1~bpo11+2", False),
        ("3", False), ("12+deb11u1", False), ("0.2", False),
    ])
    def test_first_packaging(self, rev, first):
        from matcher import _revision_is_first_packaging
        assert _revision_is_first_packaging(rev) is first

    def test_patched_rebuild_does_not_clear_the_upstream_release(self):
        db = _db({"redis": [_rec("CVE-2099-0200", "redis",
                                 ("Debian:12", [{"introduced": "0"}, {"fixed": "5:7.0.15-1~deb12u4"}]))]})
        f = _cves(match_candidate("10.0.0.1", _cand("7.0.15", "redis"), db))
        assert f["CVE-2099-0200"].match_basis == "range"


class TestReleaseLines:
    # RediShell-shaped: Debian 12 patched 7.0.15; Debian 13 fixed it by moving to 8.0.
    _REDIS = {"redis": [_rec("CVE-2025-49844", "redis",
                             ("Debian:12", [{"introduced": "0"}, {"fixed": "5:7.0.15-1~deb12u6"}]),
                             ("Debian:13", [{"introduced": "0"}, {"fixed": "5:8.0.2-3+deb13u1"}]))]}

    def test_fix_only_on_a_newer_line_is_product_presence(self):
        (f,) = match_candidate("10.0.0.1", _cand("7.2.16", "redis"), _db(self._REDIS))
        assert f.match_basis == "range-branch" and f.state == FindingState.potential
        assert any("another redis release line" in n for n in f.notes)

    def test_fix_on_the_banners_own_line_is_a_finding(self):
        (f,) = match_candidate("10.0.0.1", _cand("7.0.11", "redis"), _db(self._REDIS))
        assert f.match_basis == "range"

    def test_single_line_product_is_unaffected(self):
        # OpenSSH: 9.6p1 vs a fix in 9.8p1 is a real version signal.
        db = _db(_REGRESSHION_DEBIAN)
        (f,) = match_candidate("10.0.0.1", _cand("9.5p1", "openssh"), db)
        assert f.match_basis == "range"

    def test_debian_cve_ids_merge(self):
        db = _db({"redis": [
            {"id": "DEBIAN-CVE-2025-46817",
             "affected": [{"package": {"name": "redis", "ecosystem": "Debian:12"},
                           "ranges": [{"type": "ECOSYSTEM",
                                       "events": [{"introduced": "0"}, {"fixed": "5:7.0.15-1~deb12u9"}]}]}]},
            _rec("CVE-2025-46817", "redis",
                 ("Debian:12", [{"introduced": "0"}, {"fixed": "5:7.0.15-1~deb12u9"}]))]})
        found = match_candidate("10.0.0.1", _cand("7.0.11", "redis"), db)
        assert [f.cve_id for f in found] == ["CVE-2025-46817"]


def test_mariadb_wire_compat_prefix_is_not_the_version():
    # MariaDB's handshake says "5.5.5-10.11.19-MariaDB-ubu2204" (a replication
    # compatibility prefix). Read as 5.5.5 it matched every MariaDB CVE since 2012.
    from cpe_normalizer import normalize_db
    fact = Fact(scanner="db_scan", target="10.0.0.9", timestamp="", port=3306, proto="tcp",
                status="open",
                data={"engine": "mysql/mariadb",
                      "server_version": "5.5.5-10.11.19-MariaDB-ubu2204"},
                evidence=None, error=None, source_confidence=SourceConfidence.inferred,
                source_file="f", source_line=1)
    (c,) = normalize_db(fact)
    assert c.version_raw == "10.11.19-MariaDB-ubu2204"
    assert c.distro is None          # MariaDB's own repository build: upstream versions


# ── host OS summary (testing-round gap 7: asset table said "not recorded") ────

def test_host_os_prefers_the_ssh_banner_release(tmp_path):
    import json
    from ingest import ingest_files
    from pipeline import host_os_summary
    rows = [
        {"scanner": "os_fingerprint", "target": "10.0.0.30", "timestamp": "t", "port": None,
         "proto": None, "status": "observed", "evidence": None, "error": None,
         "data": {"os_guess": "Linux/Unix/macOS", "confidence": 0.7}},
        {"scanner": "ssh_scan", "target": "10.0.0.30", "timestamp": "t", "port": 22,
         "proto": "tcp", "status": "open", "evidence": None, "error": None,
         "data": {"ssh_confirmed": True, "software": "OpenSSH_7.2p2",
                  "banner": {"software": "OpenSSH_7.2p2", "comments": "Ubuntu-4ubuntu2.10",
                             "raw": "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10"}}},
        {"scanner": "os_fingerprint", "target": "10.0.0.31", "timestamp": "t", "port": None,
         "proto": None, "status": "observed", "evidence": None, "error": None,
         "data": {"os_guess": "unknown", "confidence": 0.0}},
    ]
    p = tmp_path / "f.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    got = host_os_summary(ingest_files([str(p)]))
    assert got["10.0.0.30"] == {"os": "Ubuntu", "os_version": "16.04", "source": "ssh_banner"}
    assert "10.0.0.31" not in got                       # "unknown" is not an OS
