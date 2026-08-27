"""
test_cve_correlation.py — the offline CVE-correlation layer (cve/ package).

This layer is the SEPARATE manager-side interpretation step: the probe emits
facts + a CPE identity and NEVER a CVE claim; `cve/` owns the offline mirror and
maps (vendor, product, version) -> prioritized CVE findings. Tests cover the four
accuracy-critical seams end-to-end without touching the network:

  * version.py   — loose version parsing/comparison for real banner strings
  * cpe.py       — product -> CPE 2.3 identity (probe-side enrichment)
  * vulndb.py    — SQLite range-membership query (versionStart*/versionEnd*)
  * correlator.py— match + enrich (CVSS/KEV/EPSS) + confidence + risk score
  * ingest.py    — NVD/KEV/EPSS parse, pagination, resume (monkeypatched _get)
  * cli.py       — ingest + correlate verbs, clean-stdout contract
"""

from __future__ import annotations

import gzip
import json

import pytest

from cve import version as ver
from cve.vulndb import VulnDB
from cve.correlator import (correlate, summarize, risk_score, risk_band,
                            CVEFinding, mirror_age_note)
from scanner.cpe import to_cpe
import cve.ingest as ing
import cve.cli as cli


# ── version.py ────────────────────────────────────────────────────────────────
class TestVersion:
    def test_parse_openssh_portable(self):
        assert ver.parse_version("8.2p1") == (8, 2, 1)

    def test_parse_openssl_letter_suffix(self):
        assert ver.parse_version("1.1.1k") == (1, 1, 1, 11)

    def test_parse_debian_epoch_and_distro_suffix(self):
        # epoch dropped, first token only
        assert ver.parse_version("1:2.4.41") == (2, 4, 41)
        assert ver.parse_version("8.2p1 Ubuntu-4ubuntu0.5") == (8, 2, 1)

    def test_parse_leading_v_and_empty(self):
        assert ver.parse_version("v1.20.0") == (1, 20, 0)
        assert ver.parse_version("") == (0,)
        assert ver.parse_version(None) == (0,)

    def test_compare(self):
        assert ver.compare("8.2p1", "8.2") == 1       # p1 is later
        assert ver.compare("1.1.1k", "1.1.1t") == -1  # k < t
        assert ver.compare("2.4.41", "2.4.41") == 0

    def test_in_range_end_exclusive(self):
        assert ver.in_range("8.2", end_excl="8.3") is True
        assert ver.in_range("8.3", end_excl="8.3") is False   # exclusive
        assert ver.in_range("8.4", end_excl="8.3") is False

    def test_in_range_start_inclusive(self):
        assert ver.in_range("8.0", start_incl="8.0", end_excl="8.3") is True
        assert ver.in_range("7.9", start_incl="8.0", end_excl="8.3") is False

    def test_in_range_exact(self):
        assert ver.in_range("8.1", exact="8.1") is True
        assert ver.in_range("8.2", exact="8.1") is False

    def test_in_range_unconstrained_is_false(self):
        # nothing constrains -> must not match everything
        assert ver.in_range("8.2") is False


# ── cpe.py (probe-side) ───────────────────────────────────────────────────────
class TestCpe:
    def test_openssh(self):
        c = to_cpe("ssh", "OpenSSH", "8.2p1")
        assert c["cpe23"] == "cpe:2.3:a:openbsd:openssh:8.2p1:*:*:*:*:*:*:*"
        assert (c["vendor"], c["product"], c["version"]) == ("openbsd", "openssh", "8.2p1")

    def test_version_pulled_from_product_string(self):
        c = to_cpe("http", "nginx/1.18.0", None)
        assert c["vendor"] == "nginx" and c["version"] == "1.18.0"

    def test_mysql_vs_mariadb_vendor(self):
        assert to_cpe("mysql", "MySQL", "5.7.0")["vendor"] == "oracle"
        assert to_cpe("mysql", "MariaDB", "10.5.0")["vendor"] == "mariadb"

    def test_unknown_product_returns_none(self):
        assert to_cpe("x", "TotallyUnknownServer", "1.0") is None

    def test_no_version_returns_none(self):
        assert to_cpe("ssh", "OpenSSH", None) is None

    def test_datastore_map_entries(self):
        # FIX-3: conservative expansion — exact NVD vendor:product identities.
        assert to_cpe("es", "Elasticsearch", "7.10.2")["cpe23"] == \
            "cpe:2.3:a:elastic:elasticsearch:7.10.2:*:*:*:*:*:*:*"
        assert to_cpe("db", "CouchDB", "3.1.1")["vendor"] == "apache"
        assert to_cpe("cache", "memcached", "1.6.9")["vendor"] == "memcached"
        assert to_cpe("cache", "Redis", "6.0.9")["cpe23"] == \
            "cpe:2.3:a:redis:redis:6.0.9:*:*:*:*:*:*:*"


# ── vulndb.py range query ─────────────────────────────────────────────────────
@pytest.fixture()
def db():
    d = VulnDB(":memory:", create=True)
    d.upsert_cve("CVE-2020-1000", 7.5, "HIGH", "", "OpenSSH < 8.3", "2020", "2020")
    d.add_cpe_match("CVE-2020-1000", "openbsd", "openssh", end_excl="8.3")
    d.upsert_kev("CVE-2020-1000", "openbsd", "openssh", "RCE", "2022-05-01")
    d.upsert_epss("CVE-2020-1000", 0.42, 0.97)
    d.upsert_cve("CVE-2019-0001", 4.0, "MEDIUM", "", "minor", "2019", "2019")
    d.add_cpe_match("CVE-2019-0001", "openbsd", "openssh", end_excl="9.0")
    d.commit()
    return d


class TestVulnDB:
    def test_cves_for_cpe_in_range(self, db):
        hits = db.cves_for_cpe("openbsd", "openssh", "8.2p1")
        ids = {h["cve_id"] for h in hits}
        assert ids == {"CVE-2020-1000", "CVE-2019-0001"}

    def test_kev_sorts_first(self, db):
        hits = db.cves_for_cpe("openbsd", "openssh", "8.2p1")
        assert hits[0]["cve_id"] == "CVE-2020-1000"   # KEV outranks
        assert hits[0]["kev"] is True and hits[0]["epss"] == 0.42

    def test_out_of_range_excluded(self, db):
        # 9.5 is above both end bounds
        assert db.cves_for_cpe("openbsd", "openssh", "9.5") == []

    def test_vendor_norm(self, db):
        assert db.cves_for_cpe("OpenBSD", "OpenSSH", "8.2p1")   # case-insensitive

    def test_counts(self, db):
        c = db.counts()
        assert c["cve"] == 2 and c["kev"] == 1 and c["epss"] == 1


# ── correlator.py ─────────────────────────────────────────────────────────────
SSH_FACT = {
    "scanner": "service_banner", "target": "10.0.0.5", "port": 22, "status": "open",
    "data": {"service": "ssh", "product": "OpenSSH", "version": "8.2p1",
             "cpe": "cpe:2.3:a:openbsd:openssh:8.2p1:*:*:*:*:*:*:*",
             "cpe_vendor": "openbsd", "cpe_product": "openssh", "cpe_version": "8.2p1"}}


class TestRiskScore:
    def test_bands(self):
        assert risk_band(80) == "critical"
        assert risk_band(60) == "high"
        assert risk_band(40) == "medium"
        assert risk_band(0) == "low"

    def test_kev_and_exposure_weight(self):
        # 0.5*7.5*10=37.5 +30(kev) +20*0.42=8.4 +15(exposed) = 90.9 -> 91
        assert risk_score(7.5, True, 0.42, True) == 91
        # not exposed -> 76
        assert risk_score(7.5, True, 0.42, False) == 76

    def test_capped_at_100(self):
        assert risk_score(10, True, 1.0, True) == 100


class TestCorrelate:
    def test_exposed_top_finding(self, db):
        fnds = correlate([SSH_FACT], db, exposed_targets={"10.0.0.5"})
        top = fnds[0]
        assert top.cve_id == "CVE-2020-1000"
        assert top.kev is True and top.confidence == "medium"
        assert top.risk_band == "critical" and top.risk_score == 91
        assert "verify against the" in top.evidence

    def test_never_asserts_confidence_is_medium(self, db):
        # banner-derived version is medium at most; correlator must not assert
        for f in correlate([SSH_FACT], db):
            assert f.confidence == "medium"

    def test_sorted_by_risk_desc(self, db):
        fnds = correlate([SSH_FACT], db)
        assert [f.risk_score for f in fnds] == sorted(
            (f.risk_score for f in fnds), reverse=True)

    def test_facts_without_cpe_ignored(self, db):
        plain = {"scanner": "x", "target": "1.2.3.4", "port": 80, "data": {"banner": "hi"}}
        assert correlate([plain], db) == []

    def test_dedup_by_cve_target_port(self, db):
        # same fact twice -> not duplicated
        fnds = correlate([SSH_FACT, dict(SSH_FACT)], db)
        assert len({(f.cve_id, f.target, f.port) for f in fnds}) == len(fnds)

    def test_to_dict_tags_type(self, db):
        d = correlate([SSH_FACT], db)[0].to_dict()
        assert d["type"] == "cve_finding" and d["cve_id"] == "CVE-2020-1000"

    def test_summarize(self, db):
        s = summarize(correlate([SSH_FACT], db, exposed_targets={"10.0.0.5"}))
        assert s["total"] == 2 and s["kev"] == 1 and s["top_cve"] == "CVE-2020-1000"

    def test_backport_banner_downgrades_confidence(self, db):
        # FIX-4: a distro-backport marker means the version can't be trusted for
        # matching -> confidence drops to "low" and the evidence says why.
        fact = {**SSH_FACT, "data": {**SSH_FACT["data"],
                "banner": "SSH-2.0-OpenSSH_8.2p1 Debian-4+deb11u1"}}
        fnds = correlate([fact], db)
        assert fnds and all(f.confidence == "low" for f in fnds)
        assert "distro-backport marker" in fnds[0].evidence

    def test_clean_banner_stays_medium(self, db):
        fact = {**SSH_FACT, "data": {**SSH_FACT["data"],
                "banner": "SSH-2.0-OpenSSH_8.2p1"}}
        fnds = correlate([fact], db)
        assert fnds and all(f.confidence == "medium" for f in fnds)


# ── ingest.py (offline, monkeypatched _get) ──────────────────────────────────
NVD_CVE = {
    "id": "CVE-2020-1000",
    "published": "2020-01-01T00:00Z", "lastModified": "2020-06-01T00:00Z",
    "descriptions": [{"lang": "es", "value": "x"}, {"lang": "en", "value": "OpenSSH < 8.3"}],
    "metrics": {"cvssMetricV31": [{"cvssData": {
        "baseScore": 7.5, "baseSeverity": "HIGH", "vectorString": "CVSS:3.1/AV:N"}}]},
    "configurations": [{"nodes": [{"cpeMatch": [
        {"vulnerable": True, "criteria": "cpe:2.3:a:openbsd:openssh:*:*:*:*:*:*:*:*",
         "versionEndExcluding": "8.3"},
        {"vulnerable": True, "criteria": "cpe:2.3:h:some:hw:*:*:*:*:*:*:*:*"},
        {"vulnerable": True, "criteria": "cpe:2.3:a:openbsd:openssh:8.1:*:*:*:*:*:*:*"}]}]}]}


class TestIngestParse:
    def test_ingest_one_cve(self):
        d = VulnDB(":memory:", create=True)
        ing.ingest_one_cve(d, NVD_CVE)
        d.commit()
        row = d.conn.execute("SELECT * FROM cve WHERE cve_id='CVE-2020-1000'").fetchone()
        assert row["cvss_score"] == 7.5 and row["cvss_severity"] == "HIGH"
        assert row["description"] == "OpenSSH < 8.3"
        cm = d.conn.execute("SELECT * FROM cpe_match WHERE cve_id='CVE-2020-1000'").fetchall()
        assert len(cm) == 2   # hardware (part 'h') skipped
        assert {r["exact_version"] for r in cm} == {None, "8.1"}

    def test_ingest_idempotent(self):
        d = VulnDB(":memory:", create=True)
        ing.ingest_one_cve(d, NVD_CVE)
        ing.ingest_one_cve(d, NVD_CVE)
        d.commit()
        n = d.conn.execute("SELECT COUNT(*) n FROM cpe_match").fetchone()["n"]
        assert n == 2   # replace_cpe_matches prevents duplication

    def test_cvss_fallback(self):
        assert ing._cvss({"cvssMetricV30": [{"cvssData": {
            "baseScore": 5.0, "baseSeverity": "medium"}}]}) == (5.0, "MEDIUM", None)
        assert ing._cvss({"cvssMetricV2": [{"baseSeverity": "LOW",
            "cvssData": {"baseScore": 3.3}}]}) == (3.3, "LOW", None)
        assert ing._cvss({}) == (None, None, None)

    def test_parse_criteria(self):
        assert ing._parse_criteria("cpe:2.3:a:v:p:1.0:*:*:*:*:*:*:*") == ("a", "v", "p", "1.0")
        assert ing._parse_criteria("garbage") is None


class TestIngestPagination:
    def _pages(self):
        return {
            0: {"totalResults": 3, "vulnerabilities": [
                {"cve": {"id": "CVE-0001", "descriptions": [], "metrics": {}, "configurations": []}},
                {"cve": {"id": "CVE-0002", "descriptions": [], "metrics": {}, "configurations": []}}]},
            2: {"totalResults": 3, "vulnerabilities": [
                {"cve": {"id": "CVE-0003", "descriptions": [], "metrics": {}, "configurations": []}}]}}

    def test_resume(self, monkeypatch):
        pages, calls = self._pages(), []

        def fake_get(url, *, params=None, headers=None, timeout=60.0, retries=4, ctx=None):
            calls.append(params["startIndex"])
            return json.dumps(pages[params["startIndex"]]).encode()
        monkeypatch.setattr(ing, "_get", fake_get)

        d = VulnDB(":memory:", create=True)
        # page 1 only -> resumable, next_index persisted
        n1 = ing.ingest_nvd(d, resume=True, max_pages=1, page_size=2, log=lambda *_: None)
        assert n1 == 2 and d.get_meta("nvd_next_index") == "2"
        assert d.get_meta("nvd_complete") is None
        # resume -> finishes, resets
        n2 = ing.ingest_nvd(d, resume=True, page_size=2, log=lambda *_: None)
        assert n2 == 1 and calls == [0, 2]
        assert d.get_meta("nvd_complete") == "1" and d.get_meta("nvd_next_index") == "0"
        assert d.counts()["cve"] == 3


class TestIngestFeeds:
    def test_kev_and_epss(self, monkeypatch):
        def fake_get(url, *, params=None, headers=None, timeout=60.0, retries=4, ctx=None):
            if "known_exploited" in url:
                return json.dumps({"vulnerabilities": [
                    {"cveID": "CVE-0001", "vendorProject": "OpenBSD", "product": "OpenSSH",
                     "vulnerabilityName": "RCE", "dateAdded": "2022-01-01"}]}).encode()
            if url.endswith(".gz"):
                return gzip.compress(
                    b"#model\ncve,epss,percentile\nCVE-0001,0.42,0.97\nbad,line\n")
            raise AssertionError(url)
        monkeypatch.setattr(ing, "_get", fake_get)

        d = VulnDB(":memory:", create=True)
        assert ing.ingest_kev(d, log=lambda *_: None) == 1
        assert ing.ingest_epss(d, log=lambda *_: None) == 1   # bad line skipped
        k = d.conn.execute("SELECT * FROM kev WHERE cve_id='CVE-0001'").fetchone()
        assert k["vendor"] == "openbsd" and k["product"] == "openssh"

    def test_epss_tolerates_plain_csv(self, monkeypatch):
        monkeypatch.setattr(ing, "_get", lambda *a, **k: b"cve,epss,percentile\nCVE-9,0.5,0.5\n")
        d = VulnDB(":memory:", create=True)
        assert ing.ingest_epss(d, log=lambda *_: None) == 1

    def test_ingest_all_stamps_last_ingest(self, monkeypatch):
        # FIX-5: a completed refresh cycle stamps meta.last_ingest_utc.
        monkeypatch.setattr(ing, "_get",
                            lambda *a, **k: b"cve,epss,percentile\nCVE-1,0.1,0.1\n")
        d = VulnDB(":memory:", create=True)
        ing.ingest_all(d, nvd=False, kev=False, epss=True, log=lambda *_: None)
        stamp = d.get_meta("last_ingest_utc")
        assert stamp and stamp.endswith("Z") and "T" in stamp


# ── mirror staleness (FIX-5) ─────────────────────────────────────────────────
class TestMirrorAge:
    def test_unknown_when_no_stamp(self, db):
        assert "unknown" in mirror_age_note(db)

    def test_fresh_has_no_warning(self, db):
        from datetime import datetime, timezone
        db.set_meta("last_ingest_utc",
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        note = mirror_age_note(db)
        assert "WARNING" not in note and "days ago" in note

    def test_stale_warns(self, db):
        db.set_meta("last_ingest_utc", "2000-01-01T00:00:00Z")
        assert mirror_age_note(db).startswith("WARNING: STALE")

    def test_unparseable_stamp_is_graceful(self, db):
        db.set_meta("last_ingest_utc", "garbage")
        assert "unparseable" in mirror_age_note(db)


# ── cli.py ────────────────────────────────────────────────────────────────────
class TestCli:
    def test_correlate_writes_findings(self, tmp_path, db):
        dbp = tmp_path / "vuln.db"
        # persist the fixture DB to disk for the CLI to open
        disk = VulnDB(str(dbp), create=True)
        disk.upsert_cve("CVE-2020-1000", 7.5, "HIGH", "", "OpenSSH < 8.3", "2020", "2020")
        disk.add_cpe_match("CVE-2020-1000", "openbsd", "openssh", end_excl="8.3")
        disk.upsert_kev("CVE-2020-1000", "openbsd", "openssh", "RCE", "2022-05-01")
        disk.commit(); disk.close()

        facts = tmp_path / "facts.jsonl"
        facts.write_text(json.dumps(SSH_FACT) + "\n# comment\n\n{ bad json\n")
        out = tmp_path / "cve_findings.jsonl"
        rc = cli.main(["correlate", "--db", str(dbp), "--facts", str(facts),
                       "--out", str(out), "--exposed", "10.0.0.5"])
        assert rc == 0
        lines = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
        assert len(lines) == 1
        assert lines[0]["cve_id"] == "CVE-2020-1000" and lines[0]["type"] == "cve_finding"
        assert lines[0]["risk_band"] == "critical"

    def test_ingest_stdout_is_clean_json(self, tmp_path, monkeypatch, capsys):
        def fake_get(url, *, params=None, headers=None, timeout=60.0, retries=4, ctx=None):
            if "known_exploited" in url:
                return json.dumps({"vulnerabilities": [
                    {"cveID": "CVE-1", "vendorProject": "v", "product": "p",
                     "vulnerabilityName": "n", "dateAdded": "2022"}]}).encode()
            if url.endswith(".gz"):
                return b"cve,epss,percentile\nCVE-1,0.9,0.99\n"
            raise AssertionError("nvd must not be called with --kev --epss")
        monkeypatch.setattr(ing, "_get", fake_get)

        dbp = tmp_path / "v.db"
        rc = cli.main(["ingest", "--db", str(dbp), "--kev", "--epss"])
        assert rc == 0
        captured = capsys.readouterr()
        # stdout must be a single clean JSON line (progress went to stderr)
        res = json.loads(captured.out.strip())
        assert res["ingested"] == {"kev": 1, "epss": 1}
        assert "kev:" in captured.err
