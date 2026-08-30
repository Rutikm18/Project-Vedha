"""
vedha_ref.evidence_store -- the layer the whole strategy rests on.

Thesis under test: a network VA platform's durable advantage is not its scanner. It is
an immutable, provenance-tagged observation store with identity resolution on top,
because that combination buys three things nobody else can retrofit:

  1. RETROACTIVE DETECTION. A CVE drops today; you answer for the last 90 days in
     milliseconds, without touching the customer network.
  2. HONEST COVERAGE. You can state which assets you CANNOT answer for, and why.
  3. TIME TRAVEL. "Was this host vulnerable on the 14th?" -- an audit-grade answer.

None of that is possible if you store conclusions instead of evidence.

The second thing proved here is that IP-keyed asset identity is actively wrong, not
merely imprecise: under ordinary DHCP churn it both splits one machine into several
and merges several machines into one. Every trend line, SLA clock and remediation
verification built on it is measuring noise.

Zero dependencies. Runs with stdlib Python 3.12.
"""

from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Iterable, Sequence

# --------------------------------------------------------------------------------------
# Provenance classes. Conflating these is why nobody can debug a VA platform.
#
#   OBSERVATION -- raw bytes a collector saw at a moment in time. Never edited.
#   ASSERTION   -- a normalized belief derived from observations ("this is OpenSSH 7.4"),
#                  carrying confidence and a pointer back to its evidence.
#   IMPORTED    -- a third-party tool's conclusion (Nuclei, an EDR export). It is someone
#                  else's opinion, not our evidence, and must never be laundered into
#                  first-party fact.
#   FINDING     -- our conclusion. Derived, reproducible, and always traceable to the
#                  observations that produced it.
# --------------------------------------------------------------------------------------

PROV_OBSERVATION = "observation"
PROV_ASSERTION = "assertion"
PROV_IMPORTED = "imported"
PROV_FINDING = "finding"

# Identity keys, strongest first. A strong key does two jobs: it MERGES observations
# that share it, and it SEPARATES observations that disagree on it. The second job is
# the one naive identity models forget, and it is why they silently merge two machines
# that happened to reuse a DHCP lease.
STRONG_IDENTITY_KEYS = ("machine_id", "ssh_host_key", "tls_cert_sha256", "mac")
WEAK_IDENTITY_KEYS = ("hostname",)
# `ip` is deliberately absent. It is a location, not an identity.

SCHEMA = """
CREATE TABLE observations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id     TEXT NOT NULL,
    observed_at   TEXT NOT NULL,
    collector     TEXT NOT NULL,
    collector_ver TEXT NOT NULL,
    provenance    TEXT NOT NULL,
    ip            TEXT,
    facts         TEXT NOT NULL
);
CREATE INDEX ix_obs_tenant_time ON observations(tenant_id, observed_at);

CREATE TABLE asset_identity (
    observation_id INTEGER PRIMARY KEY,
    asset_key      TEXT NOT NULL,
    confidence     REAL NOT NULL,
    method         TEXT NOT NULL
);
CREATE INDEX ix_identity_asset ON asset_identity(asset_key);
"""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


_MISSING = object()


def get_path(doc: Any, dotted: str) -> Any:
    cur = doc
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur


# ======================================================================================
# Ingest -- observations only, never conclusions
# ======================================================================================

def record_observation(
    conn: sqlite3.Connection, *, tenant_id: str, collector: str, collector_ver: str,
    facts: dict, observed_at: datetime, ip: str | None = None,
    provenance: str = PROV_OBSERVATION,
) -> int:
    cur = conn.execute(
        "INSERT INTO observations"
        " (tenant_id, observed_at, collector, collector_ver, provenance, ip, facts)"
        " VALUES (?,?,?,?,?,?,?)",
        (tenant_id, _iso(observed_at), collector, collector_ver, provenance,
         ip, json.dumps(facts)),
    )
    return cur.lastrowid


# ======================================================================================
# Identity resolution
# ======================================================================================

@dataclass
class IdentityResult:
    assignments: dict[int, str]                 # observation_id -> asset_key
    method: dict[int, str]
    confidence: dict[int, float]
    conflicts: list[str] = field(default_factory=list)

    def asset_count(self) -> int:
        return len(set(self.assignments.values()))

    def observations_for(self, asset_key: str) -> list[int]:
        return sorted(o for o, a in self.assignments.items() if a == asset_key)


class _UnionFind:
    def __init__(self):
        self.parent: dict[int, int] = {}

    def find(self, x: int) -> int:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def _identity_keys(facts: dict) -> dict[str, str]:
    out = {}
    for k in STRONG_IDENTITY_KEYS + WEAK_IDENTITY_KEYS:
        v = get_path(facts, f"identity.{k}")
        if v is _MISSING:
            v = get_path(facts, k)
        if v is not _MISSING and isinstance(v, str) and v:
            out[k] = v
    return out


def resolve_identity(conn: sqlite3.Connection, tenant_id: str) -> IdentityResult:
    """Cluster observations into assets using fingerprint keys.

    Strong keys merge AND separate. Two observations sharing an IP but disagreeing on a
    strong key are different machines. Two observations with different IPs but the same
    strong key are one machine. Both cases are routine on any DHCP network, and both are
    handled backwards by IP-keyed identity.
    """
    rows = conn.execute(
        "SELECT id, ip, facts FROM observations WHERE tenant_id=? ORDER BY id",
        (tenant_id,),
    ).fetchall()

    uf = _UnionFind()
    by_key: dict[tuple[str, str], list[int]] = defaultdict(list)
    keys_of: dict[int, dict[str, str]] = {}

    for r in rows:
        oid = r["id"]
        uf.find(oid)
        ks = _identity_keys(json.loads(r["facts"]))
        keys_of[oid] = ks
        for name in STRONG_IDENTITY_KEYS:
            if name in ks:
                by_key[(name, ks[name])].append(oid)

    for (_name, _val), members in by_key.items():
        for other in members[1:]:
            uf.union(members[0], other)

    # Weak keys only link observations that have no strong key at all. A hostname is
    # a label people reuse; it must never override a fingerprint.
    weak_groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for oid, ks in keys_of.items():
        if not any(k in ks for k in STRONG_IDENTITY_KEYS):
            for name in WEAK_IDENTITY_KEYS:
                if name in ks:
                    weak_groups[(name, ks[name])].append(oid)
    for members in weak_groups.values():
        for other in members[1:]:
            uf.union(members[0], other)

    # Verify no cluster holds two different values of the same strong key.
    cluster_keys: dict[int, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for oid, ks in keys_of.items():
        root = uf.find(oid)
        for name in STRONG_IDENTITY_KEYS:
            if name in ks:
                cluster_keys[root][name].add(ks[name])

    conflicts = [
        f"cluster {root} holds {len(vals)} distinct {name} values"
        for root, names in cluster_keys.items()
        for name, vals in names.items() if len(vals) > 1
    ]

    assignments, method, confidence = {}, {}, {}
    for r in rows:
        oid = r["id"]
        root = uf.find(oid)
        ks = keys_of[oid]
        for name in STRONG_IDENTITY_KEYS:
            if name in ks:
                m, c = name, 0.99 if name in ("machine_id", "ssh_host_key") else 0.9
                break
        else:
            if any(k in ks for k in WEAK_IDENTITY_KEYS):
                m, c = "hostname", 0.5
            else:
                m, c = "unresolved", 0.1
        assignments[oid] = f"asset-{root}"
        method[oid] = m
        confidence[oid] = c

    conn.execute("DELETE FROM asset_identity")
    conn.executemany(
        "INSERT INTO asset_identity (observation_id, asset_key, confidence, method)"
        " VALUES (?,?,?,?)",
        [(o, assignments[o], confidence[o], method[o]) for o in assignments],
    )
    return IdentityResult(assignments, method, confidence, conflicts)


def naive_ip_identity(conn: sqlite3.Connection, tenant_id: str) -> dict[int, str]:
    """The industry default, for comparison. Included so the cost is measurable."""
    return {
        r["id"]: f"ip-{r['ip']}"
        for r in conn.execute(
            "SELECT id, ip FROM observations WHERE tenant_id=?", (tenant_id,))
    }


# ======================================================================================
# Retroactive detection
# ======================================================================================

@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    collector: str
    requires: tuple[str, ...]
    predicate: Callable[[dict], bool]
    severity: str = "high"
    cve_id: str | None = None


ANSWER_VULNERABLE = "vulnerable"
ANSWER_NOT_VULNERABLE = "not_vulnerable"
ANSWER_CANNOT_ANSWER = "cannot_answer"   # the honest third option nobody ships


@dataclass
class AssetVerdict:
    asset_key: str
    answer: str
    reason: str | None = None
    first_seen_vulnerable: str | None = None
    last_evidence_at: str | None = None
    evidence_observation_ids: list[int] = field(default_factory=list)


def retroactive_detect(
    conn: sqlite3.Connection, tenant_id: str, rule: Rule, *,
    as_of: datetime | None = None, since: datetime | None = None,
) -> dict[str, AssetVerdict]:
    """Answer a brand-new rule against evidence already on disk.

    No network traffic, no rescan, no customer coordination. This is the capability
    that makes the observation store a moat rather than a storage cost.
    """
    q = ("SELECT o.id, o.observed_at, o.collector, o.facts, a.asset_key"
         " FROM observations o JOIN asset_identity a ON a.observation_id = o.id"
         " WHERE o.tenant_id=?")
    params: list[Any] = [tenant_id]
    if as_of:
        q += " AND o.observed_at <= ?"
        params.append(_iso(as_of))
    if since:
        q += " AND o.observed_at >= ?"
        params.append(_iso(since))
    q += " ORDER BY o.observed_at"

    # Group first, evaluate after. The current answer must come from the LATEST
    # qualifying observation, never from a disjunction over history -- otherwise a
    # host patched last week stays "vulnerable" forever and no finding ever closes.
    # History is preserved separately as first_seen_vulnerable and the timeline.
    rows_by_asset: dict[str, list[Any]] = defaultdict(list)
    for r in conn.execute(q, params):
        if r["collector"] == rule.collector:
            rows_by_asset[r["asset_key"]].append(r)

    def _eval(row) -> tuple[str, str | None]:
        facts = json.loads(row["facts"])
        missing = [p for p in rule.requires if get_path(facts, p) is _MISSING]
        if missing:
            return ANSWER_CANNOT_ANSWER, (
                f"collected {rule.collector} data lacks {missing[0]}")
        try:
            return (ANSWER_VULNERABLE if rule.predicate(facts)
                    else ANSWER_NOT_VULNERABLE), None
        except Exception as exc:
            return ANSWER_CANNOT_ANSWER, f"rule could not evaluate: {type(exc).__name__}"

    per_asset: dict[str, AssetVerdict] = {}
    all_assets = {r["asset_key"] for r in
                  conn.execute("SELECT DISTINCT asset_key FROM asset_identity")}

    for asset_key, rows in rows_by_asset.items():
        rows.sort(key=lambda r: r["observed_at"])
        answer, reason = _eval(rows[-1])                      # latest wins
        v = AssetVerdict(asset_key, answer, reason)
        v.last_evidence_at = rows[-1]["observed_at"]
        for row in rows:
            a, _ = _eval(row)
            if a != ANSWER_CANNOT_ANSWER:
                v.evidence_observation_ids.append(row["id"])
            if a == ANSWER_VULNERABLE and v.first_seen_vulnerable is None:
                v.first_seen_vulnerable = row["observed_at"]
        per_asset[asset_key] = v

    for a in all_assets - set(per_asset):
        per_asset[a] = AssetVerdict(
            a, ANSWER_CANNOT_ANSWER,
            reason=f"no {rule.collector} evidence collected for this asset")
    return per_asset


def coverage_summary(verdicts: dict[str, AssetVerdict]) -> dict:
    """What a customer should actually be shown: three numbers, not one."""
    c = defaultdict(int)
    for v in verdicts.values():
        c[v.answer] += 1
    total = len(verdicts)
    answerable = c[ANSWER_VULNERABLE] + c[ANSWER_NOT_VULNERABLE]
    return {
        "assets_total": total,
        "vulnerable": c[ANSWER_VULNERABLE],
        "not_vulnerable": c[ANSWER_NOT_VULNERABLE],
        "cannot_answer": c[ANSWER_CANNOT_ANSWER],
        "coverage_pct": round(100.0 * answerable / total, 1) if total else 0.0,
    }


def time_travel(
    conn: sqlite3.Connection, tenant_id: str, rule: Rule, asset_key: str,
    as_of: datetime,
) -> AssetVerdict:
    """Audit-grade: what did the evidence support on a specific date?"""
    return retroactive_detect(conn, tenant_id, rule, as_of=as_of).get(
        asset_key, AssetVerdict(asset_key, ANSWER_CANNOT_ANSWER,
                                reason="no evidence at that time"))


def exposure_timeline(
    conn: sqlite3.Connection, tenant_id: str, rule: Rule, asset_key: str,
) -> list[tuple[str, str]]:
    """(observed_at, answer) transitions -- the real remediation-verification signal.

    A ticket marked 'done' is a claim. A transition from vulnerable to not_vulnerable,
    backed by evidence, is a fact.
    """
    out: list[tuple[str, str]] = []
    for r in conn.execute(
        "SELECT o.observed_at, o.facts, o.collector FROM observations o"
        " JOIN asset_identity a ON a.observation_id=o.id"
        " WHERE o.tenant_id=? AND a.asset_key=? ORDER BY o.observed_at",
        (tenant_id, asset_key),
    ):
        if r["collector"] != rule.collector:
            continue
        facts = json.loads(r["facts"])
        if any(get_path(facts, p) is _MISSING for p in rule.requires):
            ans = ANSWER_CANNOT_ANSWER
        else:
            try:
                ans = ANSWER_VULNERABLE if rule.predicate(facts) else ANSWER_NOT_VULNERABLE
            except Exception:
                ans = ANSWER_CANNOT_ANSWER
        if not out or out[-1][1] != ans:
            out.append((r["observed_at"], ans))
    return out
