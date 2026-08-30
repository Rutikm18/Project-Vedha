"""
Tests for the evidence store, and a demo that puts numbers on the strategic claims.

Run:   python3 -m unittest test_evidence_store -v
Demo:  python3 test_evidence_store.py demo
"""

from __future__ import annotations

import re
import sys
import unittest
from datetime import timedelta

from evidence_store import (
    ANSWER_CANNOT_ANSWER, ANSWER_NOT_VULNERABLE, ANSWER_VULNERABLE,
    PROV_IMPORTED, Rule, connect, coverage_summary, exposure_timeline,
    naive_ip_identity, record_observation, resolve_identity, retroactive_detect,
    time_travel, utcnow, _iso,
)

TENANT = "t1"

# Three real machines. Ordinary DHCP behaviour over 30 days:
#   HOST_A  keeps one SSH host key, moves 10.0.0.5 -> 10.0.0.9 -> 10.0.0.5
#   HOST_B  later picks up 10.0.0.9, the address HOST_A used to hold
#   HOST_C  runs an agent, so it has a machine_id
KEY_A = "SHA256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
KEY_B = "SHA256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def ssh_obs(conn, *, ip, host_key, banner, day, hostname=None, machine_id=None):
    ident = {"ssh_host_key": host_key}
    if hostname:
        ident["hostname"] = hostname
    if machine_id:
        ident["machine_id"] = machine_id
    return record_observation(
        conn, tenant_id=TENANT, collector="ssh_probe", collector_ver="1.4.0",
        ip=ip, observed_at=utcnow() - timedelta(days=day),
        facts={"identity": ident, "ssh": {"banner": banner, "port": 22}},
    )


def smb_obs(conn, *, ip, host_key, smbv1, day):
    return record_observation(
        conn, tenant_id=TENANT, collector="smb_probe", collector_ver="1.4.0",
        ip=ip, observed_at=utcnow() - timedelta(days=day),
        facts={"identity": {"ssh_host_key": host_key},
               "smb": {"data": {"smbv1_enabled": smbv1, "dialect": "0x0311"}}},
    )


def openssh_below(major: int, minor: int) -> Rule:
    def pred(f):
        b = f["ssh"]["banner"]
        if not isinstance(b, str):
            raise TypeError("banner not a string")
        m = re.search(r"OpenSSH[_ ](\d+)\.(\d+)", b)
        if not m:
            return False
        return (int(m.group(1)), int(m.group(2))) < (major, minor)
    return Rule("SSH-NEW", f"OpenSSH below {major}.{minor}", "ssh_probe",
                ("ssh.banner",), pred, cve_id="CVE-2026-99999")


SMBV1 = Rule("SMB-001", "SMBv1 enabled", "smb_probe",
             ("smb.data.smbv1_enabled",),
             lambda f: f["smb"]["data"]["smbv1_enabled"] is True)


def build_fleet(conn):
    """30 days of history. HOST_A is patched on day 10."""
    for day in range(30, 20, -1):                       # A at .5, vulnerable
        ssh_obs(conn, ip="10.0.0.5", host_key=KEY_A, banner="SSH-2.0-OpenSSH_7.4",
                day=day, hostname="web01")
    for day in range(20, 10, -1):                       # A moves to .9, still vulnerable
        ssh_obs(conn, ip="10.0.0.9", host_key=KEY_A, banner="SSH-2.0-OpenSSH_7.4",
                day=day, hostname="web01")
    for day in range(10, 0, -1):                        # A back to .5, patched
        ssh_obs(conn, ip="10.0.0.5", host_key=KEY_A, banner="SSH-2.0-OpenSSH_9.6",
                day=day, hostname="web01")
    for day in range(8, 0, -1):                         # B takes over .9
        ssh_obs(conn, ip="10.0.0.9", host_key=KEY_B, banner="SSH-2.0-OpenSSH_8.9",
                day=day, hostname="db01")
    for day in range(5, 0, -1):                         # C, agent-managed
        ssh_obs(conn, ip="10.0.0.20", host_key="SHA256:cccc", banner="SSH-2.0-OpenSSH_9.6",
                day=day, hostname="app01", machine_id="mid-c-0001")
    # SMB evidence exists for A only. C is never SMB-scanned -> unanswerable, honestly.
    for day in (30, 20, 10, 2):
        smb_obs(conn, ip="10.0.0.5", host_key=KEY_A, smbv1=True, day=day)
    return resolve_identity(conn, TENANT)


class TestIdentity(unittest.TestCase):
    def setUp(self):
        self.conn = connect()
        self.ident = build_fleet(self.conn)

    def test_fingerprint_identity_finds_exactly_three_machines(self):
        self.assertEqual(self.ident.asset_count(), 3)
        self.assertEqual(self.ident.conflicts, [])

    def test_ip_identity_is_wrong_in_both_directions(self):
        """Not merely coarse -- wrong. It splits one machine and merges two."""
        naive = naive_ip_identity(self.conn, TENANT)
        self.assertEqual(len(set(naive.values())), 3)   # coincidentally same count...

        # ...but the groupings are incorrect. HOST_A is split across two IP buckets:
        a_obs = set(self.ident.observations_for(self.ident.assignments[1]))
        a_ips = {naive[o] for o in a_obs}
        self.assertGreater(len(a_ips), 1, "HOST_A should be split by IP identity")

        # And 10.0.0.9 wrongly merges HOST_A with HOST_B.
        merged = {o for o, k in naive.items() if k == "ip-10.0.0.9"}
        real = {self.ident.assignments[o] for o in merged}
        self.assertGreater(len(real), 1, "IP bucket .9 should merge two real machines")

    def test_hostname_never_overrides_a_fingerprint(self):
        c = connect()
        ssh_obs(c, ip="10.1.1.1", host_key="SHA256:x", banner="b", day=1,
                hostname="shared-name")
        ssh_obs(c, ip="10.1.1.2", host_key="SHA256:y", banner="b", day=1,
                hostname="shared-name")
        self.assertEqual(resolve_identity(c, TENANT).asset_count(), 2)

    def test_observations_without_any_fingerprint_fall_back_to_hostname(self):
        c = connect()
        for ip in ("10.2.2.1", "10.2.2.2"):
            record_observation(c, tenant_id=TENANT, collector="ssh_probe",
                               collector_ver="1", ip=ip, observed_at=utcnow(),
                               facts={"identity": {"hostname": "legacy01"}})
        r = resolve_identity(c, TENANT)
        self.assertEqual(r.asset_count(), 1)
        self.assertEqual(set(r.method.values()), {"hostname"})
        self.assertTrue(all(v < 0.6 for v in r.confidence.values()),
                        "hostname-only identity must be marked low confidence")


class TestRetroactiveDetection(unittest.TestCase):
    def setUp(self):
        self.conn = connect()
        self.ident = build_fleet(self.conn)

    def test_a_brand_new_rule_answers_against_stored_evidence(self):
        """No rescan. The whole point."""
        v = retroactive_detect(self.conn, TENANT, openssh_below(8, 5))
        answers = sorted(x.answer for x in v.values())
        self.assertEqual(answers.count(ANSWER_NOT_VULNERABLE), 3)

    def test_time_travel_recovers_the_historical_answer(self):
        rule = openssh_below(8, 5)
        asset_a = self.ident.assignments[1]

        past = time_travel(self.conn, TENANT, rule, asset_a,
                           utcnow() - timedelta(days=15))
        now = time_travel(self.conn, TENANT, rule, asset_a, utcnow())

        self.assertEqual(past.answer, ANSWER_VULNERABLE)
        self.assertEqual(now.answer, ANSWER_NOT_VULNERABLE)

    def test_remediation_is_verified_by_evidence_not_by_a_ticket(self):
        asset_a = self.ident.assignments[1]
        tl = exposure_timeline(self.conn, TENANT, openssh_below(8, 5), asset_a)
        self.assertEqual([a for _, a in tl],
                         [ANSWER_VULNERABLE, ANSWER_NOT_VULNERABLE])

    def test_current_state_comes_from_latest_evidence_not_a_union_over_history(self):
        """Regression guard. An OR over history means a patched host stays vulnerable
        forever and no finding ever closes -- a defect that looks like diligence."""
        rule = openssh_below(8, 5)
        asset_a = self.ident.assignments[1]
        v = retroactive_detect(self.conn, TENANT, rule)[asset_a]
        self.assertEqual(v.answer, ANSWER_NOT_VULNERABLE, "patched host must close")
        self.assertIsNotNone(v.first_seen_vulnerable,
                             "history must still record it WAS vulnerable")

    def test_cannot_answer_is_reported_rather_than_assumed_clean(self):
        v = retroactive_detect(self.conn, TENANT, SMBV1)
        by_answer = {}
        for k, x in v.items():
            by_answer.setdefault(x.answer, []).append(x)

        self.assertEqual(len(by_answer[ANSWER_VULNERABLE]), 1)
        self.assertEqual(len(by_answer[ANSWER_CANNOT_ANSWER]), 2)
        for x in by_answer[ANSWER_CANNOT_ANSWER]:
            self.assertIn("no smb_probe evidence", x.reason)

        s = coverage_summary(v)
        self.assertEqual(s["assets_total"], 3)
        self.assertEqual(s["cannot_answer"], 2)
        self.assertAlmostEqual(s["coverage_pct"], 33.3, places=1)

    def test_collected_but_unusable_evidence_is_distinguished_from_absent(self):
        """Drifted payload: the probe ran, the field moved."""
        c = connect()
        record_observation(c, tenant_id=TENANT, collector="smb_probe",
                           collector_ver="2.0.0", ip="10.9.9.9", observed_at=utcnow(),
                           facts={"identity": {"ssh_host_key": "SHA256:z"},
                                  "smb": {"smbv1": True}})
        resolve_identity(c, TENANT)
        v = list(retroactive_detect(c, TENANT, SMBV1).values())[0]
        self.assertEqual(v.answer, ANSWER_CANNOT_ANSWER)
        self.assertIn("lacks smb.data.smbv1_enabled", v.reason)

    def test_third_party_conclusions_are_kept_separate_from_first_party_evidence(self):
        c = connect()
        ssh_obs(c, ip="10.3.3.1", host_key="SHA256:q", banner="SSH-2.0-OpenSSH_7.4",
                day=1)
        record_observation(c, tenant_id=TENANT, collector="nuclei", collector_ver="3.1",
                           ip="10.3.3.1", observed_at=utcnow(),
                           provenance=PROV_IMPORTED,
                           facts={"identity": {"ssh_host_key": "SHA256:q"},
                                  "template": "CVE-2026-1234", "matched": True})
        resolve_identity(c, TENANT)
        rows = c.execute("SELECT provenance, COUNT(*) n FROM observations"
                         " GROUP BY provenance").fetchall()
        self.assertEqual({r["provenance"]: r["n"] for r in rows},
                         {"observation": 1, "imported": 1})


def demo():
    conn = connect()
    ident = build_fleet(conn)
    naive = naive_ip_identity(conn, TENANT)

    print("=" * 84)
    print("1. ASSET IDENTITY -- 3 real machines, 30 days, ordinary DHCP churn")
    print("=" * 84)
    print(f"  fingerprint identity : {ident.asset_count()} assets, "
          f"{len(ident.conflicts)} conflicts")
    print(f"  IP-keyed identity    : {len(set(naive.values()))} buckets")
    a_key = ident.assignments[1]
    a_obs = ident.observations_for(a_key)
    print(f"  ...but HOST_A's {len(a_obs)} observations land in "
          f"{len({naive[o] for o in a_obs})} different IP buckets (one machine, split)")
    nine = {o for o, k in naive.items() if k == "ip-10.0.0.9"}
    print(f"  ...and IP bucket 10.0.0.9 contains "
          f"{len({ident.assignments[o] for o in nine})} different real machines (merged)")
    print("  Every SLA clock and trend line built on IP identity is measuring noise.")

    print()
    print("=" * 84)
    print("2. RETROACTIVE DETECTION -- a CVE drops today, no rescan")
    print("=" * 84)
    rule = openssh_below(8, 5)
    for label, days in (("today", 0), ("15 days ago", 15), ("25 days ago", 25)):
        v = retroactive_detect(conn, TENANT, rule, as_of=utcnow() - timedelta(days=days))
        s = coverage_summary(v)
        print(f"  as of {label:12s}: vulnerable={s['vulnerable']}  "
              f"clean={s['not_vulnerable']}  unknown={s['cannot_answer']}")
    print("  Answered from evidence already on disk. Zero packets sent.")

    print()
    print("=" * 84)
    print("3. HONEST COVERAGE -- the number nobody reports")
    print("=" * 84)
    s = coverage_summary(retroactive_detect(conn, TENANT, SMBV1))
    print(f"  SMBv1 check: {s['vulnerable']} vulnerable, {s['not_vulnerable']} clean, "
          f"{s['cannot_answer']} UNANSWERABLE")
    print(f"  Honest coverage: {s['coverage_pct']}% of assets")
    print("  A dashboard reporting '1 finding' here is technically true and")
    print("  operationally a lie: two thirds of the fleet was never assessed.")

    print()
    print("=" * 84)
    print("4. REMEDIATION VERIFIED BY EVIDENCE, NOT BY A CLOSED TICKET")
    print("=" * 84)
    for ts, ans in exposure_timeline(conn, TENANT, rule, a_key):
        print(f"  {ts[:10]}  {ans}")
    print("=" * 84)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        unittest.main(verbosity=2)
