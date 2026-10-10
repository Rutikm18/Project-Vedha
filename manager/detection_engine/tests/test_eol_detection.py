"""
End-of-life / end-of-support OS detection.

An unsupported OS receives no security patches, so its vulnerability count only
grows and no amount of scanning will ever find a fix to apply. That makes EOL a
first-class posture finding, not a footnote — and it was a verified gap: nothing
in the engine flagged Windows 10 22H2 or Server 2012 as out of support.

Design constraint these tests enforce: the catalog matches a SPECIFIC release
string, never a fuzzy prefix. "Windows 11 24H2" (supported) must never be swept
up by a hypothetical "Windows 11" entry, and an OS absent from the catalog must
stay silent rather than guess. False positives here are expensive: telling a
customer to rebuild a supported fleet destroys trust faster than a missed finding.
"""
from __future__ import annotations

from eol_catalog import lookup_eol


class TestCatalogLookup:
    def test_windows_10_22h2_is_past_eol(self):
        hit = lookup_eol("Windows 10 22H2", "10.0.19045")
        assert hit is not None
        assert hit["product"] == "Windows 10 22H2"
        assert hit["eol_date"] == "2025-10-14"
        assert hit["days_past_eol"] > 0
        assert hit["source"]

    def test_supported_os_returns_none(self):
        assert lookup_eol("Windows 11 24H2", "10.0.26100") is None

    def test_unknown_os_returns_none(self):
        assert lookup_eol("SomeAppliance 1.0", None) is None

    def test_missing_os_release_returns_none(self):
        """Evidence invariant: no input, no verdict."""
        assert lookup_eol(None) is None
        assert lookup_eol("") is None

    def test_longest_match_wins(self):
        """'windows server 2012 r2' must not be shadowed by 'windows server 2012'."""
        hit = lookup_eol("Windows Server 2012 R2 Standard")
        assert hit is not None
        assert hit["eol_date"] == "2023-10-10"

    def test_match_is_case_insensitive(self):
        assert lookup_eol("WINDOWS 7 PROFESSIONAL") is not None

    def test_days_past_eol_is_positive_for_long_dead_os(self):
        """Windows 7 died in 2020; the number must be large and positive, not a
        signed artefact of date maths."""
        hit = lookup_eol("Windows 7")
        assert hit["days_past_eol"] > 2000


# ── the POSTURE-OS-END-OF-LIFE rule ──────────────────────────────────────────
from models import Fact, SourceConfidence          # noqa: E402
import posture_rules as P                          # noqa: E402


def _fact(data, scanner="os_fingerprint", port=None, status="open",
          target="192.168.1.77"):
    """Same shape the other posture-rule tests use (tests/test_posture_rules.py)."""
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _rule(rule_id):
    return next(r for r in P.RULES if r.rule_id == rule_id)


class TestEolRule:
    RULE_ID = "POSTURE-OS-END-OF-LIFE"

    def test_rule_is_registered(self):
        assert _rule(self.RULE_ID) is not None

    def test_fires_on_past_eol_os(self):
        ev = _rule(self.RULE_ID).detect(
            _fact({"os_release": "Windows 10 22H2", "os_version": "10.0.19045"}))
        assert ev is not None
        assert ev["eol_date"] == "2025-10-14"
        assert ev["days_past_eol"] > 0
        assert "end-of-support" in ev["detail"]

    def test_silent_on_supported_os(self):
        assert _rule(self.RULE_ID).detect(
            _fact({"os_release": "Windows 11 24H2"})) is None

    def test_silent_without_os_release(self):
        """Evidence invariant: os_guess alone is not enough to claim EOL. It is
        Undetermined (falsy, never a finding), not clean."""
        ev = _rule(self.RULE_ID).detect(_fact({"os_guess": "Windows"}))
        assert not ev
        assert isinstance(ev, P.Undetermined)

    def test_has_no_single_required_input(self):
        """Two alternative inputs (os_release on os_fingerprint, the banner on
        ssh_scan), so no single `requires` path: an unidentified release must not
        read as agent drift."""
        assert _rule(self.RULE_ID).requires == ()
        assert _rule(self.RULE_ID).host_level is True

    def test_reads_os_fingerprint_and_ssh_facts(self):
        assert set(_rule(self.RULE_ID).scanners) == {"os_fingerprint", "ssh_scan"}

    def test_is_high_severity_with_attack_surface_mapping(self):
        r = _rule(self.RULE_ID)
        assert r.severity == "high"
        assert r.cwe and r.mitre and r.category == "eol_software"


# ── an unknown release is UNASSESSED, never BLIND (the operator's warning) ──────
class TestUnidentifiedReleaseIsUnassessed:
    """Seen on a real campaign: '1 of 41 checks could not be assessed … blind
    checks: POSTURE-OS-END-OF-LIFE'. A TTL guess never carries os_release, so
    every Linux host and every Windows host without SMB reported the rule as
    agent drift. The scanner did not drift; it cannot know the release."""

    RULE = "POSTURE-OS-END-OF-LIFE"

    def _outcome(self, fact):
        return P.evaluate_rule(_rule(self.RULE), fact)

    def test_ttl_only_guess_is_unassessed_with_a_reason(self):
        row = self._outcome(_fact({"alive": True, "os_guess": "Linux/Unix/macOS"}))
        assert row.outcome == P.OUTCOME_NO_EVIDENCE
        assert row.outcome not in P.BLIND_OUTCOMES
        assert "SSH banner" in row.reason and "SMB" in row.reason

    def test_icmp_unavailable_is_unassessed(self):
        row = self._outcome(_fact({"icmp": "unavailable"}, status="observed"))
        assert row.outcome == P.OUTCOME_NO_EVIDENCE

    def test_campaign_rollup_no_longer_counts_it_blind(self):
        from models import Asset
        a = Asset(ip="192.168.1.70")
        a.facts.append(_fact({"alive": True, "os_guess": "Linux/Unix/macOS"},
                             target="192.168.1.70"))
        _, traces = P.detect_posture_traced(a)
        summary = P.summarize_traces(traces)
        assert self.RULE not in summary["blind_rule_ids"]


# ── the release a distribution's SSH banner announces ──────────────────────────
from os_release_intel import release_from_ssh_banner, release_from_ssh_fact  # noqa: E402


def _ssh(raw, port=22, target="192.168.1.70"):
    software, _, comments = raw.split("-", 2)[2].partition(" ")
    banner = {"protocol": "2.0", "software": software,
              "comments": comments or None, "raw": raw}
    return _fact({"ssh": True, "ssh_confirmed": True, "banner": banner,
                  "software": software}, scanner="ssh_scan", port=port, target=target)


class TestSshBannerRelease:
    def test_ubuntu_lts_releases(self):
        cases = {
            ("OpenSSH_7.6p1", "Ubuntu-4ubuntu0.7"): "Ubuntu 18.04",
            ("OpenSSH_8.2p1", "Ubuntu-4ubuntu0.13"): "Ubuntu 20.04",
            ("OpenSSH_8.9p1", "Ubuntu-3ubuntu0.10"): "Ubuntu 22.04",
            ("OpenSSH_9.6p1", "Ubuntu-3ubuntu13.5"): "Ubuntu 24.04",
            ("OpenSSH_6.6.1p1", "Ubuntu-2ubuntu2.13"): "Ubuntu 14.04",
        }
        for (sw, c), want in cases.items():
            assert release_from_ssh_banner(sw, c) == want, (sw, c)

    def test_debian_suffix_names_the_release(self):
        assert release_from_ssh_banner("OpenSSH_7.4p1", "Debian-10+deb9u7") == "Debian 9"
        assert release_from_ssh_banner("OpenSSH_9.2p1", "Debian-2+deb12u3") == "Debian 12"
        assert release_from_ssh_banner("OpenSSH_7.9p1", "Raspbian-10+deb10u2") == "Debian 10"

    def test_debian_without_suffix_uses_the_upstream_version(self):
        assert release_from_ssh_banner("OpenSSH_8.4p1", "Debian-5") == "Debian 11"

    def test_unknown_or_unpackaged_banners_name_nothing(self):
        assert release_from_ssh_banner("OpenSSH_9.0p1", "Ubuntu-1ubuntu8.7") is None  # non-LTS
        assert release_from_ssh_banner("OpenSSH_9.8", None) is None                   # self-built
        assert release_from_ssh_banner("OpenSSH_for_Windows_8.1", None) is None
        assert release_from_ssh_banner("dropbear_2022.83", None) is None
        assert release_from_ssh_fact({"ssh": False, "banner": "HTTP/1.1 400"}) is None


class TestEolFromSshBanner:
    RULE = "POSTURE-OS-END-OF-LIFE"

    def test_eol_ubuntu_fires_from_the_banner(self):
        ev = _rule(self.RULE).detect(_ssh("SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7"))
        assert ev and ev["eol_date"] == "2023-05-31"
        assert ev["os_release_source"] == "ssh_banner"
        assert "SSH banner" in ev["detail"]

    def test_supported_ubuntu_is_assessed_clean(self):
        row = P.evaluate_rule(_rule(self.RULE), _ssh("SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10"))
        assert row.outcome == P.OUTCOME_NO_MATCH

    def test_unrecognised_banner_is_unassessed(self):
        row = P.evaluate_rule(_rule(self.RULE), _ssh("SSH-2.0-OpenSSH_9.8"))
        assert row.outcome == P.OUTCOME_NO_EVIDENCE

    def test_linux_host_ttl_guess_plus_banner_is_assessed(self):
        """The weak-lab shape: TTL says Linux, the banner names the release."""
        from models import Asset
        a = Asset(ip="192.168.1.70")
        a.facts += [_fact({"alive": True, "os_guess": "Linux/Unix/macOS"}, target=a.ip),
                    _ssh("SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.10", target=a.ip)]
        findings, traces = P.detect_posture_traced(a)
        assert not [f for f in findings if f.rule_id == self.RULE]
        assert P.verdict_for_rule(traces, self.RULE)[0] == P.VERDICT_CLEAN

    def test_one_finding_per_host_even_with_two_ssh_ports(self):
        from models import Asset
        a = Asset(ip="192.168.1.71")
        a.facts += [_ssh("SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7", port=22, target=a.ip),
                    _ssh("SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7", port=2222, target=a.ip)]
        findings, _ = P.detect_posture_traced(a)
        eol = [f for f in findings if f.rule_id == self.RULE]
        assert len(eol) == 1
        assert eol[0].port is None                    # host property, not a port's
        assert eol[0].finding_id == P.make_posture_id(a.ip, self.RULE, None)


# ── a build two editions share is never called end-of-life ───────────────────
class TestSharedBuildIsNotAccused:
    """smb_scanner maps build 17763 to 'Windows 10 1809' and records
    'Windows Server 2019' as os_release_alt. Server 2019 is supported until 2029,
    so calling every Server 2019 host end-of-life was a false finding."""

    RULE = "POSTURE-OS-END-OF-LIFE"

    def test_17763_with_supported_alternative_is_unassessed(self):
        f = _fact({"os_guess": "Windows", "os_release": "Windows 10 1809",
                   "os_release_alt": "Windows Server 2019", "os_build": 17763})
        row = P.evaluate_rule(_rule(self.RULE), f)
        assert row.outcome == P.OUTCOME_NO_EVIDENCE
        assert "Windows Server 2019" in row.reason

    def test_unambiguous_eol_build_still_fires(self):
        f = _fact({"os_guess": "Windows", "os_release": "Windows 10 22H2",
                   "os_build": 19045})
        assert P.evaluate_rule(_rule(self.RULE), f).outcome == P.OUTCOME_MATCH


class TestNewCatalogRows:
    def test_ubuntu_20_04_and_debian_11_are_past_eol(self):
        assert lookup_eol("Ubuntu 20.04")["eol_date"] == "2025-05-31"
        assert lookup_eol("Debian 11")["eol_date"] == "2026-08-31"

    def test_supported_successors_stay_silent(self):
        assert lookup_eol("Ubuntu 22.04") is None
        assert lookup_eol("Ubuntu 24.04") is None
        assert lookup_eol("Debian 12") is None
