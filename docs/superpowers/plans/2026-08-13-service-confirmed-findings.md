# Service-Confirmed Findings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the probe's findings key on the *confirmed* service (from `service_banner` behavior) instead of the port number, raising confidence when confirmed and catching services on non-standard ports.

**Architecture:** A pure service index `(target, port) → {service, product, version}` is built from `service_banner` facts; the exposure/cleartext findings rule consults it first (confidence `high`, "confirmed") and falls back to the port-number hint (confidence `medium/low`, "port-based, unconfirmed") only when no behavior confirmed the service. Pure functions over facts — no network.

**Tech Stack:** Python 3, pytest. Files in `probe/main_scripts/` + `probe/tests/`.

## Global Constraints (verbatim from the source spec)

- **"Never treat `445 == SMB`, `3389 == RDP`, `22 == SSH`, `443 == HTTPS` as confirmed service identification. Port number should only influence probe priority."** (26-phase spec, Phase 16.)
- **Confidence ≠ severity.** An exposed datastore is high *severity* but only high *confidence* once the service is behaviorally confirmed; port-only is `medium`.
- **`open|filtered` never raises an exposure finding** — only definitively `open`.
- **No CVE claims** on the probe. Findings stay config/hygiene/exposure.
- **`main_scripts/` is untracked** (local hardening tree) — so a task's "commit" gate is *"full `main_scripts` test suite green"*, not a git commit. Run: `python3 -m pytest tests/test_main_scripts_*.py -q`.

---

## Product framing (PM lens)

**North Star:** *verified, evidence-backed findings an operator can act on without re-checking* — accuracy is the moat (incumbents lose to false positives).

**Success metrics for this milestone:**
- Exposure/cleartext findings carry `confidence=high` **only** when a service was behaviorally confirmed; port-only findings are explicitly `confidence≤medium` and labeled "unconfirmed".
- A confirmed service on a **non-standard port** (e.g. Redis on 7000) is now flagged (previously missed — port map only).
- Zero regressions across the 92-test suite.

**Prioritized roadmap (RICE-ranked epics; this plan = Epic 1):**

| # | Epic | Reach | Impact | Confidence | Effort | Why now |
|---|------|-------|--------|-----------|--------|---------|
| **1** | **Service-confirmed findings** *(this plan)* | every scan | high | high | S | Fixes a self-identified accuracy weakness (port==service); offline-testable |
| 2 | Correlation findings (SMBv1+no-signing+exposed → relay path) | Windows nets | high | med | S | High-signal, pure over existing findings |
| 3 | Anonymous-access proofs (FTP anon / SMB null / Redis unauth) | many | high | med | M | Upgrades exposure med→high *confidence* with a real proof (needs small collector reads) |
| 4 | Scan completeness invariant (Phase 3) | every scan | med | high | S | Trust: prove no silent port drops |
| 5 | JA4S + JA4 similarity (arXiv 2410.03817) | TLS hosts | med | med | M | Extends JA4X; infra correlation |
| 6 | Accuracy harness vs nmap (Phase 26) | — | high | med | L | Turns anti-FP claim into a published number |

Epics 2–6 are sequenced after this; each is an independent, testable increment.

---

## File Structure

- **Modify:** `probe/main_scripts/findings.py` — add `build_service_index()`; rewrite `_rule_cleartext_and_exposure` to consult it. One responsibility: fact→finding interpretation (unchanged).
- **Modify:** `probe/tests/test_main_scripts_findings.py` — add service-confirmation tests.

No new files — this deepens the existing findings module.

---

### Task 1: Pure service index from `service_banner` facts

**Files:**
- Modify: `probe/main_scripts/findings.py`
- Test: `probe/tests/test_main_scripts_findings.py`

**Interfaces:**
- Produces: `build_service_index(facts) -> dict[tuple[str, int], dict]` mapping `(target, port)` → `{"service": str, "product": str | None, "version": str | None}` for every fact whose `scanner == "service_banner"` (or `data.service` present) and `status == "open"`.

- [ ] **Step 1: Write the failing test**

```python
def test_build_service_index_extracts_confirmed_services():
    idx = F.build_service_index([
        {"scanner": "service_banner", "target": "t", "port": 7000, "status": "open",
         "data": {"service": "redis", "product": "Redis", "version": "7.0.1"}},
        {"scanner": "service_banner", "target": "t", "port": 80, "status": "open",
         "data": {"service": "http", "product": "nginx"}},
        {"scanner": "service_banner", "target": "t", "port": 9, "status": "open",
         "data": {}},                         # no service -> ignored
        {"scanner": "port_scan", "target": "t", "port": 22, "status": "open"},  # not a banner
    ])
    assert idx[("t", 7000)]["service"] == "redis"
    assert idx[("t", 7000)]["version"] == "7.0.1"
    assert idx[("t", 80)]["service"] == "http"
    assert ("t", 9) not in idx and ("t", 22) not in idx
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_main_scripts_findings.py::test_build_service_index_extracts_confirmed_services -q`
Expected: FAIL — `AttributeError: module 'main_scripts.findings' has no attribute 'build_service_index'`.

- [ ] **Step 3: Implement `build_service_index`** (add near the rule helpers in `findings.py`)

```python
def build_service_index(facts) -> dict:
    """Map (target, port) -> confirmed-service info from service_banner facts.
    Only behavior-confirmed services (data.service present, port open) are indexed."""
    idx: dict = {}
    for raw in facts:
        f = _as_dict(raw)
        if _scanner(f) != "service_banner" or f.get("status") != "open":
            continue
        svc = (_data(f).get("service") or "").lower()
        if not svc:
            continue
        idx[(f.get("target"), f.get("port"))] = {
            "service": svc,
            "product": _data(f).get("product"),
            "version": _data(f).get("version"),
        }
    return idx
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_main_scripts_findings.py::test_build_service_index_extracts_confirmed_services -q`
Expected: PASS.

- [ ] **Step 5: Gate — full suite green**

Run: `python3 -m pytest tests/test_main_scripts_*.py -q` → all pass (main_scripts is untracked; no git commit).

---

### Task 2: Confirmed-service exposure/cleartext rule (port as fallback hint)

**Files:**
- Modify: `probe/main_scripts/findings.py` (`_rule_cleartext_and_exposure`)
- Test: `probe/tests/test_main_scripts_findings.py`

**Interfaces:**
- Consumes: `build_service_index` (Task 1); `_DATASTORE_PORTS`, `Finding`, severity/category/confidence constants (existing).
- Produces: exposure/cleartext findings with `confidence="high"` + evidence `"service confirmed by banner"` when the `(target,port)` service is confirmed; `confidence="medium"` (datastore/rdp) or unchanged cleartext with evidence `"port-based (service not confirmed)"` otherwise. A confirmed datastore service (`redis/mysql/mongodb/...`) on ANY port is flagged, not just its default port.

- [ ] **Step 1: Write the failing tests**

```python
def test_confirmed_redis_is_high_confidence_even_on_nonstandard_port():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 7000, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 7000, "status": "open",
         "data": {"service": "redis", "product": "Redis"}},
    )
    hit = next(f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED" and f.port == 7000)
    assert hit.severity == F.SEV_HIGH and hit.confidence == F.CONF_HIGH
    assert "confirm" in hit.evidence.lower()

def test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp", "status": "open"})
    hit = next(f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED")
    assert hit.confidence == F.CONF_MEDIUM and "unconfirmed" in hit.evidence.lower()

def test_confirmed_ftp_cleartext_is_high_confidence():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 21, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 21, "status": "open",
         "data": {"service": "ftp", "product": "vsftpd"}},
    )
    hit = next(f for f in fs if f.rule_id == "SVC-FTP-CLEARTEXT")
    assert hit.confidence == F.CONF_HIGH
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_main_scripts_findings.py -q -k "confirmed or unconfirmed"`
Expected: FAIL (rule still keys on port number; Redis on 7000 not flagged; 6379 is high-not-medium via old CONF_MEDIUM but no "unconfirmed" text).

- [ ] **Step 3: Rewrite `_rule_cleartext_and_exposure`** to consult the service index

```python
# Confirmed service name -> (rule_id, title-noun, severity, category)
_DATASTORE_SERVICES = {
    "redis": ("Redis", SEV_HIGH), "mongodb": ("MongoDB", SEV_HIGH),
    "elasticsearch": ("Elasticsearch", SEV_HIGH), "couchdb": ("CouchDB", SEV_HIGH),
    "memcached": ("Memcached", SEV_MEDIUM), "mysql": ("MySQL/MariaDB", SEV_MEDIUM),
    "postgresql": ("PostgreSQL", SEV_MEDIUM), "mssql": ("Microsoft SQL Server", SEV_MEDIUM),
}


def _rule_cleartext_and_exposure(facts: list[dict]) -> Iterable[Finding]:
    index = build_service_index(facts)
    for f in facts:
        if _scanner(f) not in ("port_scan", "syn_scan", "mass_scan", "service_banner"):
            continue
        if f.get("proto") not in ("tcp", None) or not _is_open(f):
            continue
        port = f.get("port")
        target = f.get("target")
        confirmed = index.get((target, port), {})
        svc = confirmed.get("service")

        # 1) Confirmed datastore on ANY port -> high-confidence exposure.
        if svc in _DATASTORE_SERVICES:
            name, sev = _DATASTORE_SERVICES[svc]
            yield Finding(
                "SVC-DATASTORE-EXPOSED", f"{name} reachable from the scan vantage",
                sev, CONF_HIGH, CAT_EXPOSURE, target, port, "tcp",
                f"{name} confirmed by banner on port {port}. Reachable from the scan "
                "position; bind to localhost/management network and require auth.",
                f"Bind {name} to localhost/management network and require authentication.",
                {"service": name, "port": port, "confirmed": True,
                 "version": confirmed.get("version")}, "service_banner")
            continue
        # 2) Confirmed FTP (cleartext) on any port.
        if svc == "ftp":
            yield Finding(
                "SVC-FTP-CLEARTEXT", "FTP exposed (cleartext control channel)",
                SEV_MEDIUM, CONF_HIGH, CAT_CLEARTEXT, target, port, "tcp",
                f"FTP confirmed by banner on port {port}; credentials travel in cleartext. "
                "Verify anonymous access is disabled.",
                "Use FTPS/SFTP; disable anonymous FTP.",
                {"port": port, "confirmed": True}, "service_banner")
            continue
        if svc == "telnet":
            yield Finding(
                "SVC-TELNET-CLEARTEXT", "Telnet exposed (cleartext credentials)",
                SEV_HIGH, CONF_HIGH, CAT_CLEARTEXT, target, port, "tcp",
                f"Telnet confirmed on port {port} — credentials and session in cleartext.",
                "Disable Telnet; use SSH.", {"port": port, "confirmed": True}, "service_banner")
            continue

        # 3) No behavioral confirmation -> port-number HINT only (lower confidence).
        if port == 23:
            yield Finding(
                "SVC-TELNET-CLEARTEXT", "Telnet exposed (cleartext credentials)",
                SEV_HIGH, CONF_MEDIUM, CAT_CLEARTEXT, target, port, "tcp",
                "Port 23 open — Telnet by convention (port-based, service not confirmed); "
                "Telnet transmits credentials in cleartext.",
                "Disable Telnet; use SSH.", {"port": 23, "confirmed": False}, _scanner(f))
        elif port == 21:
            yield Finding(
                "SVC-FTP-CLEARTEXT", "FTP exposed (cleartext control channel)",
                SEV_MEDIUM, CONF_MEDIUM, CAT_CLEARTEXT, target, port, "tcp",
                "Port 21 open — FTP by convention (port-based, service not confirmed); "
                "FTP transmits credentials in cleartext.",
                "Use FTPS/SFTP; disable anonymous FTP.", {"port": 21, "confirmed": False}, _scanner(f))
        elif port == 3389:
            yield Finding(
                "SVC-RDP-EXPOSED", "RDP exposed to the scan vantage",
                SEV_MEDIUM, CONF_MEDIUM, CAT_EXPOSURE, target, port, "tcp",
                "Port 3389 open — RDP by convention (port-based, service not confirmed); "
                "a common brute-force / exploit target.",
                "Restrict RDP to VPN/jump hosts; enforce NLA + MFA.",
                {"port": 3389, "confirmed": False}, _scanner(f))
        elif port in _DATASTORE_PORTS:
            name, sev, why = _DATASTORE_PORTS[port]
            yield Finding(
                "SVC-DATASTORE-EXPOSED", f"{name} reachable from the scan vantage",
                sev, CONF_MEDIUM, CAT_EXPOSURE, target, port, "tcp",
                f"Port {port} open — {name} by convention (port-based, service not "
                f"confirmed). {why}",
                f"Bind {name} to localhost/management network and require authentication.",
                {"service": name, "port": port, "confirmed": False}, _scanner(f))
```

- [ ] **Step 4: Run the new tests + the existing exposure tests**

Run: `python3 -m pytest tests/test_main_scripts_findings.py -q`
Expected: PASS. (Note: `test_exposed_redis_is_high_exposure_medium_confidence` and `test_telnet_is_high_cleartext` may need their confidence/evidence assertions updated to the new port-based `medium`/"unconfirmed" wording — update them in this step to match the corrected behavior, since port-only is now medium-confidence by design.)

- [ ] **Step 5: Gate — full suite green**

Run: `python3 -m pytest tests/test_main_scripts_*.py -q` → all pass.

---

### Task 3: Dedup a confirmed + port-hint collision on the same (target, port)

**Files:**
- Modify: `probe/tests/test_main_scripts_findings.py` (assertion only — dedup already exists in `run_findings`).

**Interfaces:** Consumes existing `run_findings` dedup by `(rule_id, target, port)`.

- [ ] **Step 1: Write the test**

```python
def test_confirmed_and_port_hint_do_not_double_report():
    # 6379 open AND service_banner confirms redis on 6379 -> exactly one finding.
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 6379, "status": "open",
         "data": {"service": "redis"}},
    )
    hits = [f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED" and f.port == 6379]
    assert len(hits) == 1 and hits[0].confidence == F.CONF_HIGH   # the confirmed one wins
```

- [ ] **Step 2: Run it**

Run: `python3 -m pytest tests/test_main_scripts_findings.py::test_confirmed_and_port_hint_do_not_double_report -q`
Expected: PASS (the `service_banner` fact is iterated first via index-confirm; `run_findings` dedup keeps one). If the port-hint (CONF_MEDIUM) wins the dedup instead of the confirmed one, reorder so the confirmed branch is emitted first (the `service_banner` fact row itself carries the confirmation) — verify and adjust.

- [ ] **Step 3: Gate — full suite green**

Run: `python3 -m pytest tests/test_main_scripts_*.py -q` → all pass.

---

## Self-Review

**1. Spec coverage:** Phase-16 principle ("port is only a hint; behavior confirms service") → Tasks 1–2. Confidence≠severity → Task 2 (confirmed=high, port-only=medium). Non-standard-port detection → Task 2 datastore-service branch. Dedup → Task 3. ✅

**2. Placeholder scan:** every step has runnable code + exact commands. The one judgment note (Task 2 Step 4 / Task 3 Step 2) tells the engineer exactly which existing assertions to update and why. ✅

**3. Type consistency:** `build_service_index(facts) -> dict[(target,port)->{service,product,version}]` used identically in Tasks 1–3. `_DATASTORE_SERVICES` (service→(name,sev)) is new; `_DATASTORE_PORTS` (port→(name,sev,why)) is the existing fallback — distinct names, no collision. Confidence constants `CONF_HIGH/CONF_MEDIUM` match `findings.py`. ✅

---

## Execution Handoff

Milestone 1 of the roadmap. Executing inline (Tasks 1–3) in `main_scripts`, verifying the full suite green after each — no git commits (untracked tree).
