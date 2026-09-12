# VA Maturity Gap Closure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the seven verified maturity gaps in Vedha's VA pipeline — default-credential detection, EOL/EOS detection, delta surfacing, MTTR/ownership, checkpointed scanning, continuous scheduling, and ServiceNow ticketing — without weakening the accuracy discipline the detection engine already enforces.

**Architecture:** Vedha is a two-part system. The **probe** (`probe/`, Python) is FACTS-ONLY by design: it observes and emits `Fact` records, never verdicts. The **manager** (`manager/`) runs detection: `manager/detection_engine/posture_rules.py` is a data-driven rule catalog (39 rules today) that turns facts into findings, and `manager/backend/app/` is the FastAPI service that stores, prioritizes, and reports them. Every gap is closed at the layer that owns it: detection rules in `detection_engine/`, new observations in `probe/main_scripts/`, workflow/state in `manager/backend/app/`. The probe's `main_scripts/` and `scanner/` trees are kept BYTE-IDENTICAL (drift-guarded) — every probe change lands in `main_scripts/` then is copied to `scanner/`.

**Tech Stack:** Python 3.11+ (probe: stdlib-only scanners; manager: FastAPI, SQLAlchemy async, Alembic, Postgres/JSONB), pytest.

## Global Constraints

- **Two-tree parity (probe):** any change to `probe/main_scripts/<mod>.py` MUST be mirrored to `probe/scanner/<mod>.py` (`cp main_scripts/<mod>.py scanner/<mod>.py`); `tests/test_two_tree_parity.py` fails otherwise. Manager code has no such mirror.
- **Facts-only probe:** the probe emits observations, never findings/severity/verdicts. Detection stays in the manager. A new probe capability adds FACTS; a new detection adds a `PostureRule`.
- **Evidence invariant:** no evidence → no finding. A `PostureRule.detect(fact)` returns `None` (not a low-confidence finding) when its inputs are absent.
- **Trust tier:** a finding from a scanner NOT in `posture_rules.VALIDATED_SCANNERS` is `SUSPECTED`, not `CONFIRMED`. New rules on unvalidated scanners state this in `fp_notes`.
- **`requires` contract:** every `PostureRule` declares the minimal `fact.data` paths that gate assessability, so a missing input reports `MISSING_INPUT` (drift) instead of looking clean.
- **Migrations:** new Alembic revisions chain from `0038` (current head); revision ids are zero-padded (`0039`, `0040`…). Postgres enum values are added with `ALTER TYPE ... ADD VALUE IF NOT EXISTS`; they cannot be dropped (downgrade rewrites rows).
- **Timestamps:** use `app/services/project_time.py::project_now()` (manager) / `scanner_base.project_timestamp()` (probe) — aware, IST-rendered, never naive `datetime.now()`.
- **No secrets in scan params:** the probe and manager reject credential material in job params. Default-credential CHECKS must use a curated built-in list, never operator-supplied secrets.
- **Deploy reality:** manager code is baked into `vedha-backend:local` (not mounted); the detection engine is baked at `/opt/detection_engine`. A change is live only after image rebuild + `docker compose up -d`. The probe loads code at process start — restart required after a probe change.
- **Test command (manager):** `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`. **Test command (probe):** `cd probe && .venv/bin/python -m pytest tests/ -q -p no:cacheprovider`.
- **Detection-engine tests** live in `manager/detection_engine/tests/`; import modules as top-level (`from posture_rules import ...`) — the engine runs with its own directory on `sys.path`, not as `app.detection_engine`.

---

## Workstream A — Detection rules (no schema, no probe changes)

*Shippable alone. Pure additions to `posture_rules.py` + fixtures. Highest security value, lowest risk.*

### Task A1: EOL/EOS operating-system detection rule

**Files:**
- Create: `manager/detection_engine/eol_catalog.py`
- Modify: `manager/detection_engine/posture_rules.py` (add one detector + one `PostureRule` to the `RULES` tuple)
- Test: `manager/detection_engine/tests/test_eol_detection.py`

**Interfaces:**
- Consumes: `Fact` with `scanner="os_fingerprint"`, `data.os_release` (e.g. `"Windows 10 22H2"`), `data.os_version` (e.g. `"10.0.19045"`), `data.os_build` (int).
- Produces: `eol_catalog.lookup_eol(os_release: str, os_version: str | None) -> dict | None` returning `{"product","eol_date","days_past_eol","source"}` or `None`; a `PostureRule` with id `POSTURE-OS-END-OF-LIFE`.

- [ ] **Step 1: Write the failing test for the catalog lookup**

```python
# manager/detection_engine/tests/test_eol_detection.py
import datetime as dt
from eol_catalog import lookup_eol

def test_windows_10_22h2_is_past_eol():
    hit = lookup_eol("Windows 10 22H2", "10.0.19045")
    assert hit is not None
    assert hit["product"] == "Windows 10 22H2"
    assert hit["eol_date"] == "2025-10-14"
    assert hit["days_past_eol"] > 0
    assert hit["source"]

def test_supported_os_returns_none():
    assert lookup_eol("Windows 11 24H2", "10.0.26100") is None

def test_unknown_os_returns_none():
    assert lookup_eol("SomeAppliance 1.0", None) is None
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/detection_engine && python -m pytest tests/test_eol_detection.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'eol_catalog'`.

- [ ] **Step 3: Write the EOL catalog**

```python
# manager/detection_engine/eol_catalog.py
"""
eol_catalog.py — curated end-of-life / end-of-support dates for OSes Vedha
fingerprints. DATA, not logic: a table an analyst maintains, matched against the
os_release string os_fingerprint already emits. Dates are vendor-published EOS
dates (the point after which security patches stop). Keep entries specific —
match the release+edition string, never a fuzzy prefix, so "Windows 11 24H2"
(supported) is never swept up by a "Windows 11" entry.
"""
from __future__ import annotations
from datetime import date, datetime, timezone

# product-match substring (case-insensitive, exact token match preferred) -> EOS date
_EOL: dict[str, str] = {
    "windows 7":            "2020-01-14",
    "windows 8":            "2016-01-12",
    "windows 8.1":          "2023-01-10",
    "windows 10 1507":      "2017-05-09",
    "windows 10 1809":      "2020-11-10",
    "windows 10 20h2":      "2023-05-09",
    "windows 10 21h2":      "2024-06-11",
    "windows 10 22h2":      "2025-10-14",   # final Windows 10 servicing
    "windows server 2008":  "2020-01-14",
    "windows server 2012":  "2023-10-10",
    "windows server 2012 r2": "2023-10-10",
    "ubuntu 16.04":         "2021-04-30",
    "ubuntu 18.04":         "2023-05-31",
    "centos 7":             "2024-06-30",
    "centos 8":             "2021-12-31",
    "debian 9":             "2022-06-30",
    "debian 10":            "2024-06-30",
}


def lookup_eol(os_release: str | None, os_version: str | None = None) -> dict | None:
    """Return EOL info for a fingerprinted OS, or None if supported/unknown.

    Matches the LONGEST catalog key contained in the normalized os_release, so
    'windows 10 22h2' wins over a hypothetical 'windows 10' entry and a
    still-supported release matches nothing.
    """
    if not os_release:
        return None
    hay = os_release.strip().lower()
    best_key = None
    for key in _EOL:
        if key in hay and (best_key is None or len(key) > len(best_key)):
            best_key = key
    if best_key is None:
        return None
    eol = date.fromisoformat(_EOL[best_key])
    today = datetime.now(timezone.utc).date()
    return {
        "product": os_release.strip(),
        "eol_date": _EOL[best_key],
        "days_past_eol": (today - eol).days,
        "source": "vendor_published_eos",
    }
```

- [ ] **Step 4: Run the catalog test to confirm it passes**

Run: `cd manager/detection_engine && python -m pytest tests/test_eol_detection.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Write the failing rule test**

```python
# append to tests/test_eol_detection.py
from posture_rules import RULES
from models import Fact

def _rule(rid):
    return next(r for r in RULES if r.rule_id == rid)

def _fact(**data):
    return Fact(scanner="os_fingerprint", target="10.0.0.5", port=None,
                status="open", data=data)

def test_eol_rule_fires_on_past_eol_os():
    rule = _rule("POSTURE-OS-END-OF-LIFE")
    ev = rule.detect(_fact(os_release="Windows 10 22H2", os_version="10.0.19045"))
    assert ev is not None
    assert ev["eol_date"] == "2025-10-14"
    assert "days_past_eol" in ev

def test_eol_rule_silent_on_supported_os():
    rule = _rule("POSTURE-OS-END-OF-LIFE")
    assert rule.detect(_fact(os_release="Windows 11 24H2")) is None

def test_eol_rule_silent_without_os_release():
    rule = _rule("POSTURE-OS-END-OF-LIFE")
    assert rule.detect(_fact(os_guess="Windows")) is None   # evidence invariant
```

- [ ] **Step 6: Run it to confirm it fails**

Run: `cd manager/detection_engine && python -m pytest tests/test_eol_detection.py -q`
Expected: FAIL, `StopIteration` (rule not registered yet).

- [ ] **Step 7: Add the detector and rule to `posture_rules.py`**

Add near the other detectors (after `_d`), importing the catalog at the top of the file (`from eol_catalog import lookup_eol`):

```python
def _os_eol(f: Fact) -> Optional[dict]:
    d = _d(f)
    hit = lookup_eol(d.get("os_release"), d.get("os_version"))
    if hit is None:
        return None
    return {
        "product": hit["product"],
        "eol_date": hit["eol_date"],
        "days_past_eol": hit["days_past_eol"],
        "detail": f"{hit['product']} reached end-of-support on {hit['eol_date']} "
                  f"({hit['days_past_eol']} days ago); no security patches are issued.",
    }
```

Add to the `RULES` tuple:

```python
    PostureRule(
        "POSTURE-OS-END-OF-LIFE", "Operating system is end-of-life / unsupported",
        "high", "CWE-1104", "T1190", "eol_software", ("os_fingerprint",), _os_eol,
        "Upgrade to a vendor-supported OS release; unsupported OSes receive no "
        "security patches and accumulate unfixable vulnerabilities.",
        fp_notes="Fires only when os_fingerprint reports a specific release string "
                 "present in the curated EOL catalog. A build not in the catalog "
                 "(unknown or still-supported) never fires — no false positives, "
                 "at the cost of catalog freshness.",
        requires=("os_release",)),
```

- [ ] **Step 8: Run the full EOL test file to confirm it passes**

Run: `cd manager/detection_engine && python -m pytest tests/test_eol_detection.py -q`
Expected: PASS (6 tests).

- [ ] **Step 9: Run the full detection-engine suite (no regressions)**

Run: `cd manager/detection_engine && python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add manager/detection_engine/eol_catalog.py manager/detection_engine/posture_rules.py manager/detection_engine/tests/test_eol_detection.py
git commit -m "feat(detection): flag end-of-life operating systems (POSTURE-OS-END-OF-LIFE)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task A2: Grouped/deduplicated fleet findings (noise reduction)

**Files:**
- Modify: `manager/detection_engine/posture_rules.py` — extend the evidence dict of existing device-class rules with a stable `group_key` (no new rule).
- Test: `manager/detection_engine/tests/test_finding_grouping.py`

**Interfaces:**
- Consumes: existing rule evidence dicts.
- Produces: every posture evidence dict carries `group_key: str` — a stable hash of `(rule_id, product-or-service-signature)` so the UI/report layer can collapse N identical device findings (12 identical cameras) into one grouped row while preserving per-asset detail.

- [ ] **Step 1: Write the failing test**

```python
# manager/detection_engine/tests/test_finding_grouping.py
from posture_rules import group_key_for

def test_identical_devices_share_a_group_key():
    a = group_key_for("POSTURE-SVC-RDP-EXPOSED", {"product": "Hikvision DS-2CD"})
    b = group_key_for("POSTURE-SVC-RDP-EXPOSED", {"product": "Hikvision DS-2CD"})
    assert a == b

def test_different_products_differ():
    a = group_key_for("POSTURE-SVC-RDP-EXPOSED", {"product": "Hikvision DS-2CD"})
    b = group_key_for("POSTURE-SVC-RDP-EXPOSED", {"product": "Axis M3045"})
    assert a != b

def test_different_rules_differ():
    a = group_key_for("RULE-A", {"product": "X"})
    b = group_key_for("RULE-B", {"product": "X"})
    assert a != b

def test_missing_product_falls_back_to_rule_only():
    assert group_key_for("RULE-A", {}) == group_key_for("RULE-A", {})
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/detection_engine && python -m pytest tests/test_finding_grouping.py -q`
Expected: FAIL, `ImportError: cannot import name 'group_key_for'`.

- [ ] **Step 3: Add `group_key_for` to `posture_rules.py`**

```python
def group_key_for(rule_id: str, evidence: dict) -> str:
    """Stable key for collapsing identical findings across a fleet.

    A flat network with 12 identical cameras should read as ONE grouped finding
    with an asset count, not 12 rows that bury the real issues. The key is the
    rule plus the strongest device signature available in the evidence; when no
    product/service signature exists it degrades to rule-only (still groups, just
    coarser). Grouping is a PRESENTATION concern — each per-asset finding is still
    stored individually; this only tells the UI what may be folded together.
    """
    sig = (evidence or {}).get("product") or (evidence or {}).get("service") or ""
    raw = f"{rule_id}|{str(sig).strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/detection_engine && python -m pytest tests/test_finding_grouping.py -q`
Expected: PASS (4 tests).

- [ ] **Step 5: Run the full detection-engine suite**

Run: `cd manager/detection_engine && python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add manager/detection_engine/posture_rules.py manager/detection_engine/tests/test_finding_grouping.py
git commit -m "feat(detection): stable group_key for fleet finding deduplication

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream B — Default-credential detection (probe FACT + manager RULE)

*Two commits: the probe emits a login-surface fact; the manager rule reads it. Highest real-world IoT value. Ships after Workstream A but is independent of it.*

### Task B1: Probe emits an auth-surface fact (no credential guessing on the probe)

**Files:**
- Modify: `probe/main_scripts/iot_scanner.py` — add HTTP auth-realm observation to the existing device probe.
- Mirror: `cp probe/main_scripts/iot_scanner.py probe/scanner/iot_scanner.py`
- Test: `probe/tests/test_iot_auth_surface.py`

**Interfaces:**
- Produces: `iot_scanner` facts gain `data.auth_surface = {"scheme": "basic|digest|form|none", "realm": str|None, "vendor": str|None}` when an HTTP(S) management port responds with a `WWW-Authenticate` header or a recognizable login form. This is an OBSERVATION (what auth the device advertises), NOT a credential attempt.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_iot_auth_surface.py
from scanner.iot_scanner import parse_auth_surface

def test_basic_auth_realm_is_parsed():
    headers = {"WWW-Authenticate": 'Basic realm="Hikvision"'}
    s = parse_auth_surface(headers, body="")
    assert s == {"scheme": "basic", "realm": "Hikvision", "vendor": "hikvision"}

def test_digest_auth_is_parsed():
    headers = {"WWW-Authenticate": 'Digest realm="NETGEAR", nonce="x"'}
    s = parse_auth_surface(headers, body="")
    assert s["scheme"] == "digest" and s["realm"] == "NETGEAR"

def test_no_auth_header_and_no_form_is_none_scheme():
    s = parse_auth_surface({}, body="<html>welcome</html>")
    assert s["scheme"] == "none"

def test_login_form_without_header_is_detected():
    body = '<form action="/login"><input type="password" name="pass"></form>'
    s = parse_auth_surface({}, body=body)
    assert s["scheme"] == "form"
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_iot_auth_surface.py -q`
Expected: FAIL, `ImportError: cannot import name 'parse_auth_surface'`.

- [ ] **Step 3: Add `parse_auth_surface` to `iot_scanner.py`**

```python
_VENDOR_HINTS = ("hikvision", "dahua", "axis", "netgear", "ubiquiti", "tp-link",
                 "d-link", "hp", "canon", "epson", "brother", "zyxel", "mikrotik")

def parse_auth_surface(headers: dict, body: str = "") -> dict:
    """Classify the AUTH SURFACE a web management port advertises.

    Pure observation, never a login attempt: we read what the device asks for
    (an HTTP auth challenge or a password form) so the MANAGER can flag it as a
    default-credential CANDIDATE. The probe stays facts-only; it never sends a
    username or password.
    """
    www = ""
    for k, v in (headers or {}).items():
        if k.lower() == "www-authenticate":
            www = str(v)
            break
    realm = None
    scheme = "none"
    if www:
        low = www.lower()
        scheme = "digest" if low.startswith("digest") else "basic" if low.startswith("basic") else "other"
        m = __import__("re").search(r'realm="([^"]*)"', www)
        realm = m.group(1) if m else None
    elif body and ("type=\"password\"" in body.lower() or "type='password'" in body.lower()):
        scheme = "form"
    blob = f"{realm or ''} {body[:2000]}".lower()
    vendor = next((v for v in _VENDOR_HINTS if v in blob), None)
    return {"scheme": scheme, "realm": realm, "vendor": vendor}
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_iot_auth_surface.py -q`
Expected: PASS (4 tests).

- [ ] **Step 5: Wire `parse_auth_surface` into the scanner's HTTP probe**

In `iot_scanner.py`, where the device HTTP response is available, add its result to the emitted `data` dict as `"auth_surface": parse_auth_surface(resp_headers, resp_body)`. (Locate the existing `data={...}` construction in the HTTP branch; add the one key.)

- [ ] **Step 6: Mirror to the scanner/ tree and confirm parity**

```bash
cp probe/main_scripts/iot_scanner.py probe/scanner/iot_scanner.py
cd probe && .venv/bin/python -m pytest tests/test_two_tree_parity.py tests/test_iot_auth_surface.py -q
```
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add probe/main_scripts/iot_scanner.py probe/scanner/iot_scanner.py probe/tests/test_iot_auth_surface.py
git commit -m "feat(probe): observe device web auth surface (facts-only, no credential attempts)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task B2: Manager rule — default-credential exposure candidate

**Files:**
- Create: `manager/detection_engine/default_creds_catalog.py`
- Modify: `manager/detection_engine/posture_rules.py`
- Test: `manager/detection_engine/tests/test_default_cred_rule.py`

**Interfaces:**
- Consumes: `iot_scanner`/`printer_scanner` facts with `data.auth_surface` (from B1) and `data.vendor`/`data.model`.
- Produces: `default_creds_catalog.has_known_defaults(vendor: str | None) -> dict | None`; a `PostureRule` `POSTURE-DEFAULT-CRED-CANDIDATE`.

- [ ] **Step 1: Write the failing catalog test**

```python
# manager/detection_engine/tests/test_default_cred_rule.py
from default_creds_catalog import has_known_defaults

def test_known_vendor_has_defaults():
    hit = has_known_defaults("hikvision")
    assert hit and hit["default_login"] and hit["reference"]

def test_unknown_vendor_returns_none():
    assert has_known_defaults("acme-nonexistent") is None

def test_none_vendor_returns_none():
    assert has_known_defaults(None) is None
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/detection_engine && python -m pytest tests/test_default_cred_rule.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the catalog**

```python
# manager/detection_engine/default_creds_catalog.py
"""
default_creds_catalog.py — vendors with WIDELY-DOCUMENTED default credentials.

DATA only, and deliberately NOT a credential list to try: this maps a fingerprinted
vendor to the PUBLIC FACT that it ships default creds plus a reference, so the
manager can raise a "change the default password" finding from the auth-surface
observation alone. Vedha never attempts a login (no brute force, no spray) —
confirming the credential is a separate, RoE-gated active-validation step.
"""
from __future__ import annotations

_DEFAULTS: dict[str, dict] = {
    "hikvision": {"default_login": "admin/12345", "reference": "vendor default; CVE-2017-7921 era"},
    "dahua":     {"default_login": "admin/admin", "reference": "vendor default"},
    "axis":      {"default_login": "root/pass",   "reference": "vendor default (pre-2020 firmware)"},
    "netgear":   {"default_login": "admin/password", "reference": "vendor default"},
    "tp-link":   {"default_login": "admin/admin", "reference": "vendor default"},
    "d-link":    {"default_login": "admin/(blank)", "reference": "vendor default"},
    "ubiquiti":  {"default_login": "ubnt/ubnt",   "reference": "vendor default"},
    "zyxel":     {"default_login": "admin/1234",  "reference": "vendor default"},
    "mikrotik":  {"default_login": "admin/(blank)", "reference": "vendor default"},
}


def has_known_defaults(vendor: str | None) -> dict | None:
    if not vendor:
        return None
    return _DEFAULTS.get(vendor.strip().lower())
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/detection_engine && python -m pytest tests/test_default_cred_rule.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Write the failing rule test**

```python
# append to tests/test_default_cred_rule.py
from posture_rules import RULES
from models import Fact

def _rule(rid):
    return next(r for r in RULES if r.rule_id == rid)

def test_default_cred_rule_fires_on_known_vendor_with_auth():
    rule = _rule("POSTURE-DEFAULT-CRED-CANDIDATE")
    f = Fact(scanner="iot_scan", target="10.0.0.9", port=80, status="open",
             data={"vendor": "hikvision",
                   "auth_surface": {"scheme": "basic", "realm": "Hikvision", "vendor": "hikvision"}})
    ev = rule.detect(f)
    assert ev is not None and ev["default_login"] == "admin/12345"

def test_default_cred_rule_silent_when_no_auth_surface():
    rule = _rule("POSTURE-DEFAULT-CRED-CANDIDATE")
    f = Fact(scanner="iot_scan", target="10.0.0.9", port=80, status="open",
             data={"vendor": "hikvision"})   # no auth_surface -> evidence invariant
    assert rule.detect(f) is None

def test_default_cred_rule_silent_on_unknown_vendor():
    rule = _rule("POSTURE-DEFAULT-CRED-CANDIDATE")
    f = Fact(scanner="iot_scan", target="10.0.0.9", port=80, status="open",
             data={"vendor": "acme", "auth_surface": {"scheme": "basic", "realm": "x"}})
    assert rule.detect(f) is None
```

- [ ] **Step 6: Run it to confirm it fails**

Run: `cd manager/detection_engine && python -m pytest tests/test_default_cred_rule.py -q`
Expected: FAIL, `StopIteration`.

- [ ] **Step 7: Add the detector and rule**

Import at top: `from default_creds_catalog import has_known_defaults`. Add detector:

```python
def _default_cred_candidate(f: Fact) -> Optional[dict]:
    d = _d(f)
    surface = d.get("auth_surface") or {}
    if not isinstance(surface, dict) or surface.get("scheme") in (None, "none"):
        return None                       # no login surface observed -> no finding
    vendor = surface.get("vendor") or d.get("vendor")
    hit = has_known_defaults(vendor)
    if hit is None:
        return None
    return {
        "vendor": vendor,
        "auth_scheme": surface.get("scheme"),
        "default_login": hit["default_login"],
        "reference": hit["reference"],
        "product": d.get("model") or vendor,
        "detail": f"{vendor} devices ship documented default credentials "
                  f"({hit['default_login']}); this host exposes a "
                  f"{surface.get('scheme')} login. Confirm the default was changed.",
    }
```

Add to `RULES`:

```python
    PostureRule(
        "POSTURE-DEFAULT-CRED-CANDIDATE", "Device may still use default credentials",
        "high", "CWE-1392", "T1078.001", "default_credentials",
        ("iot_scan", "printer_scan"), _default_cred_candidate,
        "Change the device's default administrator password; where supported, "
        "disable the default account and enforce a password policy.",
        fp_notes="A CANDIDATE, not a confirmation: fires when a device from a "
                 "known-default vendor exposes a login surface. Vedha never "
                 "attempts the credential — confirmation is a separate RoE-gated "
                 "active-validation step. iot_scan/printer_scan are not in the "
                 "validated trust tier, so this is SUSPECTED.",
        requires=("auth_surface",)),
```

- [ ] **Step 8: Run the full file to confirm it passes**

Run: `cd manager/detection_engine && python -m pytest tests/test_default_cred_rule.py -q`
Expected: PASS (6 tests).

- [ ] **Step 9: Run the full detection-engine suite**

Run: `cd manager/detection_engine && python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add manager/detection_engine/default_creds_catalog.py manager/detection_engine/posture_rules.py manager/detection_engine/tests/test_default_cred_rule.py
git commit -m "feat(detection): flag default-credential candidates from device auth surface

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream C — Findings lifecycle: MTTR + ownership (manager schema + API)

*Adds two columns and a metrics endpoint. Independent of A and B.*

### Task C1: Add `assigned_to` and `resolved_at` to the Finding model

**Files:**
- Modify: `manager/backend/app/models/finding.py`
- Create: `manager/backend/alembic/versions/0039_finding_owner_resolved.py`
- Test: `manager/backend/tests/test_finding_owner_schema.py`

**Interfaces:**
- Produces: `Finding.assigned_to: uuid | None` (FK users.id, nullable), `Finding.resolved_at: datetime | None`. `first_seen`/`last_seen`/`resolution_run_id`/`resolution_method` already exist (verified) — MTTR reuses them; `resolved_at` is the explicit close timestamp for manual resolutions that have no run.

- [ ] **Step 1: Write the failing migration-presence test**

```python
# manager/backend/tests/test_finding_owner_schema.py
from app.models.finding import Finding

def test_finding_has_owner_and_resolved_columns():
    cols = set(Finding.__table__.columns.keys())
    assert "assigned_to" in cols
    assert "resolved_at" in cols
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_owner_schema.py -q`
Expected: FAIL, `AssertionError`.

- [ ] **Step 3: Add the columns to the model**

In `manager/backend/app/models/finding.py`, after the resolution-lifecycle block:

```python
    # ── Ownership + explicit close time (mobilization) ─────────────────────────
    # assigned_to: the user responsible for remediating this finding (nullable —
    #   unassigned is the default). resolved_at: when it was closed, whether by the
    #   coverage-gated auto-resolver or a manual status change. MTTR = resolved_at
    #   - first_seen; ownership drives the "who" of remediation tracking.
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
```

- [ ] **Step 4: Write the Alembic migration**

```python
# manager/backend/alembic/versions/0039_finding_owner_resolved.py
"""finding ownership + explicit resolved_at

Revision ID: 0039
Revises: 0038
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0039"
down_revision: Union[str, None] = "0038"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("assigned_to", sa.dialects.postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("findings", sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_findings_assigned_to", "findings", ["assigned_to"])
    op.create_foreign_key("fk_findings_assigned_to_users", "findings", "users",
                          ["assigned_to"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    op.drop_constraint("fk_findings_assigned_to_users", "findings", type_="foreignkey")
    op.drop_index("ix_findings_assigned_to", table_name="findings")
    op.drop_column("findings", "resolved_at")
    op.drop_column("findings", "assigned_to")
```

- [ ] **Step 5: Run the schema test to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_owner_schema.py -q`
Expected: PASS.

- [ ] **Step 6: Run the full backend suite (no model-import regressions)**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/finding.py manager/backend/alembic/versions/0039_finding_owner_resolved.py manager/backend/tests/test_finding_owner_schema.py
git commit -m "feat(findings): add assigned_to + resolved_at for ownership and MTTR

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task C2: MTTR + ownership metrics service and endpoint

**Files:**
- Create: `manager/backend/app/services/finding_metrics.py`
- Modify: `manager/backend/app/routers/findings.py` (add a `GET /findings/metrics` route)
- Test: `manager/backend/tests/test_finding_metrics.py`

**Interfaces:**
- Consumes: `Finding.first_seen`, `Finding.resolved_at`, `Finding.status`, `Finding.assigned_to`.
- Produces: `finding_metrics.compute_mttr(resolved: list[tuple[datetime, datetime]]) -> dict` returning `{"count","mttr_hours","mttr_days"}`; endpoint `GET /agents-independent /findings/metrics?engagement_id=` returning `{"mttr": {...}, "open_by_owner": {...}, "open_count": int, "resolved_count": int}`.

- [ ] **Step 1: Write the failing pure-function test**

```python
# manager/backend/tests/test_finding_metrics.py
from datetime import datetime, timedelta, timezone
from app.services.finding_metrics import compute_mttr

def _pair(hours):
    seen = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return (seen, seen + timedelta(hours=hours))

def test_mttr_of_two_findings():
    m = compute_mttr([_pair(10), _pair(20)])
    assert m["count"] == 2
    assert m["mttr_hours"] == 15.0
    assert round(m["mttr_days"], 3) == 0.625

def test_mttr_empty_is_zero_not_crash():
    m = compute_mttr([])
    assert m["count"] == 0 and m["mttr_hours"] == 0.0

def test_mttr_ignores_negative_durations():
    # resolved_at before first_seen is dirty data; must not skew or go negative
    seen = datetime(2026, 1, 1, tzinfo=timezone.utc)
    m = compute_mttr([(seen, seen - timedelta(hours=5)), _pair(10)])
    assert m["count"] == 1 and m["mttr_hours"] == 10.0
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_metrics.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the metrics service**

```python
# manager/backend/app/services/finding_metrics.py
"""
finding_metrics.py — mobilization metrics over the findings lifecycle.

MTTR = mean(resolved_at - first_seen) over findings that actually closed. The
inputs already exist on the Finding model (first_seen from the detection run that
first produced it, resolved_at from auto/manual close); this only aggregates them.
Dirty pairs (resolved before first seen) are dropped, never allowed to produce a
negative MTTR.
"""
from __future__ import annotations
from datetime import datetime


def compute_mttr(pairs: list[tuple[datetime, datetime]]) -> dict:
    durations = [
        (resolved - seen).total_seconds() / 3600.0
        for seen, resolved in pairs
        if seen and resolved and resolved >= seen
    ]
    if not durations:
        return {"count": 0, "mttr_hours": 0.0, "mttr_days": 0.0}
    mean_h = sum(durations) / len(durations)
    return {
        "count": len(durations),
        "mttr_hours": round(mean_h, 2),
        "mttr_days": round(mean_h / 24.0, 3),
    }
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_metrics.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Write the failing endpoint test**

```python
# append to tests/test_finding_metrics.py — mirror the direct-call style used by
# tests/test_fleet_jobs.py (SimpleNamespace user, mocked AsyncSession)
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.routers import findings as fr

@pytest.mark.asyncio
async def test_metrics_endpoint_shape():
    user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")
    db = MagicMock()
    # resolved pairs query, then open-by-owner query, then counts
    db.execute = AsyncMock(side_effect=[
        MagicMock(all=lambda: []),               # resolved (first_seen, resolved_at) pairs
        MagicMock(all=lambda: []),               # open by owner rows
        MagicMock(scalar_one=lambda: 0),         # open count
        MagicMock(scalar_one=lambda: 0),         # resolved count
    ])
    out = await fr.finding_metrics(uuid.uuid4(), db, user)
    assert set(out.keys()) == {"mttr", "open_by_owner", "open_count", "resolved_count"}
    assert out["mttr"]["count"] == 0
```

- [ ] **Step 6: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_metrics.py -q`
Expected: FAIL, `AttributeError: module 'app.routers.findings' has no attribute 'finding_metrics'`.

- [ ] **Step 7: Add the endpoint to `findings.py`**

```python
from app.services.finding_metrics import compute_mttr

@router.get("/metrics", summary="MTTR + ownership metrics for an engagement")
async def finding_metrics(engagement_id: uuid.UUID, db: DB, current_user: AuthUser):
    # tenant-scoped via the engagement join, same pattern as the other routes here
    pairs = (await db.execute(
        select(Finding.first_seen, Finding.resolved_at)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.engagement_id == engagement_id,
               Engagement.tenant_id == current_user.tenant_id,
               Finding.resolved_at.is_not(None))
    )).all()
    by_owner_rows = (await db.execute(
        select(Finding.assigned_to, func.count())
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.engagement_id == engagement_id,
               Engagement.tenant_id == current_user.tenant_id,
               Finding.status == FindingStatus.open)
        .group_by(Finding.assigned_to)
    )).all()
    open_count = (await db.execute(
        select(func.count()).select_from(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.engagement_id == engagement_id,
               Engagement.tenant_id == current_user.tenant_id,
               Finding.status == FindingStatus.open)
    )).scalar_one()
    resolved_count = (await db.execute(
        select(func.count()).select_from(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.engagement_id == engagement_id,
               Engagement.tenant_id == current_user.tenant_id,
               Finding.resolved_at.is_not(None))
    )).scalar_one()
    return {
        "mttr": compute_mttr([(s, r) for s, r in pairs]),
        "open_by_owner": {str(owner) if owner else "unassigned": n for owner, n in by_owner_rows},
        "open_count": int(open_count),
        "resolved_count": int(resolved_count),
    }
```

Verify `func`, `select`, `Engagement`, `Finding`, `FindingStatus`, `DB`, `AuthUser` are imported at the top of `findings.py`; add any missing (they follow the existing import block's style).

- [ ] **Step 8: Run the full metrics test file**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_finding_metrics.py -q`
Expected: PASS (4 tests).

- [ ] **Step 9: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add manager/backend/app/services/finding_metrics.py manager/backend/app/routers/findings.py manager/backend/tests/test_finding_metrics.py
git commit -m "feat(findings): MTTR + open-by-owner metrics endpoint

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream D — Delta surfacing (manager reads existing probe delta capability)

*The probe already has `delta_scanner.py` and a `uc_rescan_delta` use case. This exposes run-to-run change at the manager so an operator sees "3 new ports, 1 new host" without re-deriving it. Independent workstream.*

### Task D1: Run-to-run delta service

**Files:**
- Create: `manager/backend/app/services/run_delta.py`
- Modify: `manager/backend/app/routers/detection_runs.py` (add `GET /detection-runs/{run_id}/delta`)
- Test: `manager/backend/tests/test_run_delta.py`

**Interfaces:**
- Consumes: two runs' finding sets (current run's findings vs the previous run's for the same engagement), keyed by `(rule_id_or_cve, asset, port)`.
- Produces: `run_delta.diff_findings(current: list[dict], previous: list[dict]) -> dict` → `{"new": [...], "resolved": [...], "unchanged_count": int}`; endpoint returning the same over the two most recent runs.

- [ ] **Step 1: Write the failing pure-diff test**

```python
# manager/backend/tests/test_run_delta.py
from app.services.run_delta import diff_findings

def _f(key, sev="high"):
    return {"key": key, "severity": sev, "title": key}

def test_new_findings_are_detected():
    d = diff_findings(current=[_f("a"), _f("b")], previous=[_f("a")])
    assert [x["key"] for x in d["new"]] == ["b"]
    assert d["resolved"] == []
    assert d["unchanged_count"] == 1

def test_resolved_findings_are_detected():
    d = diff_findings(current=[_f("a")], previous=[_f("a"), _f("c")])
    assert [x["key"] for x in d["resolved"]] == ["c"]

def test_no_previous_run_marks_all_new():
    d = diff_findings(current=[_f("a"), _f("b")], previous=[])
    assert len(d["new"]) == 2 and d["resolved"] == []
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_run_delta.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the diff service**

```python
# manager/backend/app/services/run_delta.py
"""
run_delta.py — what changed between two detection runs.

The probe already computes fact-level deltas (delta_scanner + uc_rescan_delta);
this is the MANAGER-side, finding-level view an operator actually reads: which
findings are NEW since the last run, which are gone (RESOLVED), and how many
persist. Keyed on a stable identity so re-running the same scan on an unchanged
network shows an empty delta, not churn.
"""
from __future__ import annotations


def _key(f: dict) -> str:
    return str(f.get("key") or f"{f.get('rule_id') or f.get('cve')}|{f.get('asset')}|{f.get('port')}")


def diff_findings(current: list[dict], previous: list[dict]) -> dict:
    cur = {_key(f): f for f in current}
    prev = {_key(f): f for f in previous}
    new = [cur[k] for k in cur if k not in prev]
    resolved = [prev[k] for k in prev if k not in cur]
    unchanged = sum(1 for k in cur if k in prev)
    return {"new": new, "resolved": resolved, "unchanged_count": unchanged}
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_run_delta.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Write the failing endpoint test**

```python
# append to tests/test_run_delta.py
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.routers import detection_runs as dr

@pytest.mark.asyncio
async def test_delta_endpoint_new_and_resolved():
    user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")
    run_id = uuid.uuid4()
    # _load_run_findings returns (current_list, previous_list); patch it
    dr._load_run_findings = AsyncMock(return_value=(
        [{"key": "a"}, {"key": "b"}], [{"key": "a"}]))
    db = MagicMock()
    out = await dr.run_delta_endpoint(run_id, db, user)
    assert [x["key"] for x in out["new"]] == ["b"]
    assert out["unchanged_count"] == 1
```

- [ ] **Step 6: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_run_delta.py -q`
Expected: FAIL, `AttributeError` (endpoint + helper not defined).

- [ ] **Step 7: Add the loader helper and endpoint to `detection_runs.py`**

```python
from app.services.run_delta import diff_findings

async def _load_run_findings(db, run_id, tenant_id):
    """(current run's findings, the previous run's findings) as diff-ready dicts.

    Current = findings whose detection_run_id == run_id. Previous = findings from
    the run immediately before it for the same engagement. Returns ([], []) shapes
    the diff handles. Tenant-scoped via the run->engagement join.
    """
    run = (await db.execute(
        select(DetectionRun).join(Engagement, DetectionRun.engagement_id == Engagement.id)
        .where(DetectionRun.id == run_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if run is None:
        return None, None
    prev = (await db.execute(
        select(DetectionRun).where(
            DetectionRun.engagement_id == run.engagement_id,
            DetectionRun.created_at < run.created_at,
        ).order_by(DetectionRun.created_at.desc()).limit(1)
    )).scalar_one_or_none()

    def _shape(rows):
        return [{"key": f"{f.cve_ids[0] if f.cve_ids else f.title}|{f.asset_id}",
                 "title": f.title, "severity": f.severity.value if hasattr(f.severity, 'value') else str(f.severity)}
                for f in rows]

    cur_rows = (await db.execute(
        select(Finding).where(Finding.detection_run_id == run_id))).scalars().all()
    prev_rows = [] if prev is None else (await db.execute(
        select(Finding).where(Finding.detection_run_id == prev.id))).scalars().all()
    return _shape(cur_rows), _shape(prev_rows)


@router.get("/{run_id}/delta", summary="Findings that changed since the previous run")
async def run_delta_endpoint(run_id: uuid.UUID, db: DB, current_user: AuthUser):
    current, previous = await _load_run_findings(db, run_id, current_user.tenant_id)
    if current is None:
        raise HTTPException(404, "Detection run not found")
    return diff_findings(current, previous or [])
```

Verify imports (`select`, `DetectionRun`, `Finding`, `Engagement`, `HTTPException`, `DB`, `AuthUser`) exist at the top of `detection_runs.py`; add any missing.

- [ ] **Step 8: Run the full delta test file**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_run_delta.py -q`
Expected: PASS (4 tests).

- [ ] **Step 9: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add manager/backend/app/services/run_delta.py manager/backend/app/routers/detection_runs.py manager/backend/tests/test_run_delta.py
git commit -m "feat(detection): run-to-run finding delta (new/resolved/unchanged)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream E — Checkpointed port scanning + partial results (probe)

*The port scanner already reports a complete/degraded summary; this adds a per-host WALL-CLOCK budget so a deep scan of a huge, silent host returns partial-but-honest results instead of running for hours. Independent workstream. Builds on the AIMD/delivery work already in `port_scanner.py`.*

### Task E1: Per-host time budget with honest partial-result reporting

**Files:**
- Modify: `probe/main_scripts/port_scanner.py` (add a `deadline_seconds` knob to `PortScanner` + `--max-seconds` CLI flag)
- Mirror: `cp probe/main_scripts/port_scanner.py probe/scanner/port_scanner.py`
- Test: `probe/tests/test_port_scan_budget.py`

**Interfaces:**
- Consumes: `PortScanner(..., deadline_seconds: float | None = None)`.
- Produces: when the wall-clock budget elapses, the scan stops dequeuing new ports, records unreached ports as `not_scanned` (NOT `filtered` — they were never probed), and the `scan_summary.data` gains `budget_exhausted: bool`, `ports_not_scanned: int`, and `complete: False`. An honest partial result, never a fabricated one.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_port_scan_budget.py
import asyncio
from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard

def _sc(ports, **kw):
    return PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                       ports=ports, timeout=0.01, concurrency=4,
                       rate=10_000, reprobe=False, **kw)

def test_budget_stops_the_scan_and_reports_partial():
    sc = _sc(list(range(1, 2001)), deadline_seconds=0.2)

    async def _slow(target, port, est=None, min_timeout=None):
        await asyncio.sleep(0.05)   # each probe is slow; budget must cut in
        return sc._build(target, port, "filtered", "no_response", "silence")
    sc._attempt = _slow
    out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 20))
    summ = [r for r in out if r.status == "scan_summary"][0].data
    assert summ["budget_exhausted"] is True
    assert summ["complete"] is False
    assert summ["ports_not_scanned"] > 0
    # attempted + not_scanned must account for every requested port (honesty)
    assert summ["ports_attempted"] + summ["ports_not_scanned"] == summ["ports_requested"]

def test_no_budget_scans_everything():
    sc = _sc([80, 443], deadline_seconds=None)

    async def _fast(target, port, est=None, min_timeout=None):
        return sc._build(target, port, "closed", "connection_refused", "rst")
    sc._attempt = _fast
    out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 20))
    summ = [r for r in out if r.status == "scan_summary"][0].data
    assert summ["budget_exhausted"] is False
    assert summ["complete"] is True
    assert summ["ports_not_scanned"] == 0
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_port_scan_budget.py -q`
Expected: FAIL, `TypeError: __init__() got an unexpected keyword argument 'deadline_seconds'`.

- [ ] **Step 3: Add the budget to `PortScanner`**

In `__init__`, accept and store the knob:

```python
        # Wall-clock budget for THIS host. None = scan to completion. When set,
        # the worker pool stops dequeuing once the deadline passes and every
        # un-dequeued port is recorded not_scanned (never filtered — it was never
        # probed). Turns an hours-long deep scan of a silent host into an honest
        # partial result. Complements the accuracy floors: those keep throughput
        # up; this bounds total time when even a healthy scan is simply huge.
        self.deadline_seconds = deadline_seconds
```

In `scan_target`, compute the deadline once after `t0` is set:

```python
        _deadline = (t0 + self.deadline_seconds) if self.deadline_seconds else None
```

In the worker loop, before dequeuing the next port, stop if the budget is spent:

```python
        async def _worker() -> None:
            while True:
                if _deadline is not None and time.monotonic() >= _deadline:
                    return                     # budget spent: leave the rest in the queue
                try:
                    port = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                ...
```

After the workers finish, before recording, capture the not-scanned ports (whatever is still queued):

```python
        not_scanned = []
        while not queue.empty():
            try:
                not_scanned.append(queue.get_nowait())
            except asyncio.QueueEmpty:
                break
        budget_exhausted = bool(not_scanned) and _deadline is not None
```

In the `scan_summary` data dict, add:

```python
            "budget_exhausted": budget_exhausted,
            "ports_not_scanned": len(not_scanned),
```

And make `complete` reflect it — the summary's `complete` must be False when ports were left unscanned. (The existing `complete` is derived from metrics; AND it with `not not_scanned`.)

- [ ] **Step 4: Run to confirm it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_port_scan_budget.py -q`
Expected: PASS (2 tests).

- [ ] **Step 5: Add the `--max-seconds` CLI flag**

Where `port_scanner` builds its argparser and constructs the scanner:

```python
    parser.add_argument("--max-seconds", type=float, default=None,
                        help="per-host wall-clock budget; unreached ports are "
                             "reported not_scanned and the run is marked incomplete")
```
and pass `deadline_seconds=args.max_seconds` into the `PortScanner(...)` call.

- [ ] **Step 6: Mirror to scanner/ and confirm parity + no regressions**

```bash
cp probe/main_scripts/port_scanner.py probe/scanner/port_scanner.py
cd probe && .venv/bin/python -m pytest tests/test_two_tree_parity.py tests/test_port_scan_budget.py tests/test_scanner_congestion.py tests/test_main_scripts_completeness.py -q
```
Expected: PASS. (`test_main_scripts_completeness` proves attempted+not_scanned still accounts for every requested port.)

- [ ] **Step 7: Commit**

```bash
git add probe/main_scripts/port_scanner.py probe/scanner/port_scanner.py probe/tests/test_port_scan_budget.py
git commit -m "feat(probe): per-host wall-clock budget with honest partial results

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task E2: Thread the budget through intensity presets

**Files:**
- Modify: `probe/workflow/intensity.py` (add `max_host_seconds` to each preset)
- Modify: `probe/workflow/workflow_engine.py` (pass it into the `PortScanner` at the port_scan stage)
- Mirror: `cp` both to `probe/scanner/` counterparts IF they exist there (workflow/ is not mirrored — verify with `ls probe/scanner/workflow` ; if absent, skip the mirror for these two files).
- Test: `probe/tests/test_intensity_budget.py`

**Interfaces:**
- Consumes: `INTENSITY_PRESETS[name]["max_host_seconds"]`.
- Produces: `deep` intensity carries a finite `max_host_seconds` (default 1800 = 30 min/host) so an operator-launched deep `network_va` can never run for hours per host; `light`/`standard` keep `None` (they are already bounded by port breadth).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_intensity_budget.py
from workflow.intensity import INTENSITY_PRESETS

def test_deep_has_a_finite_host_budget():
    assert INTENSITY_PRESETS["deep"]["max_host_seconds"] == 1800

def test_light_and_standard_are_unbounded():
    assert INTENSITY_PRESETS["light"]["max_host_seconds"] is None
    assert INTENSITY_PRESETS["standard"]["max_host_seconds"] is None
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_intensity_budget.py -q`
Expected: FAIL, `KeyError: 'max_host_seconds'`.

- [ ] **Step 3: Add `max_host_seconds` to each preset in `intensity.py`**

Add the key to all three dicts: `light` → `None`, `standard` → `None`, `deep` → `1800`. Add a comment on the `deep` entry explaining that a full 65,535-port sweep of a silent host would otherwise run ~21+ min even at healthy throughput, and unreachable hosts can be far worse; the budget makes the ceiling explicit and the partial result honest.

- [ ] **Step 4: Run to confirm it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_intensity_budget.py -q`
Expected: PASS.

- [ ] **Step 5: Pass the budget into the scanner at the port_scan stage**

In `workflow_engine.py`, at the `port_scan` stage where `PortScanner(...)` is constructed (near line 513, inside `with _timed(trace, "port_scan")`), pass `deadline_seconds=intensity_preset.get("max_host_seconds")` using whatever variable already holds the resolved intensity preset. If the preset dict isn't in scope there, thread it from where `resolve_intensity`/`INTENSITY_PRESETS` is consulted.

- [ ] **Step 6: Run the workflow tests + full probe suite**

Run: `cd probe && .venv/bin/python -m pytest tests/test_intensity_budget.py tests/test_workflow_execution.py -q`
Expected: PASS. Then the full suite: `cd probe && .venv/bin/python -m pytest tests/ -q -p no:cacheprovider` → PASS.

- [ ] **Step 7: Commit**

```bash
git add probe/workflow/intensity.py probe/workflow/workflow_engine.py probe/tests/test_intensity_budget.py
git commit -m "feat(probe): deep intensity gets a 30-min per-host scan budget

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream F — Continuous scheduling (manager)

*Recurring, incremental rescans instead of every run starting from scratch. Independent workstream; benefits most from Workstream D (delta) but does not require it.*

### Task F1: ScanSchedule model + migration

**Files:**
- Create: `manager/backend/app/models/scan_schedule.py`
- Create: `manager/backend/alembic/versions/0040_scan_schedule.py`
- Modify: `manager/backend/app/models/__init__.py` (register the model if that file aggregates model imports — verify)
- Test: `manager/backend/tests/test_scan_schedule_model.py`

**Interfaces:**
- Produces: `ScanSchedule` table — `id`, `tenant_id`, `engagement_id`, `use_case_id: str`, `intensity: int`, `interval_hours: int`, `enabled: bool`, `last_run_at: datetime|None`, `next_run_at: datetime`, `created_by`, timestamps.

- [ ] **Step 1: Write the failing model test**

```python
# manager/backend/tests/test_scan_schedule_model.py
def test_scan_schedule_model_columns():
    from app.models.scan_schedule import ScanSchedule
    cols = set(ScanSchedule.__table__.columns.keys())
    for c in ("id", "tenant_id", "engagement_id", "use_case_id", "intensity",
              "interval_hours", "enabled", "last_run_at", "next_run_at"):
        assert c in cols, c
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scan_schedule_model.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the model** (follow `app/models/scan_job.py` conventions — `TimestampMixin`, `Mapped`, `mapped_column`, server defaults).

```python
# manager/backend/app/models/scan_schedule.py
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin   # match scan_job.py's import


class ScanSchedule(Base, TimestampMixin):
    __tablename__ = "scan_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), index=True, nullable=False)
    use_case_id: Mapped[str] = mapped_column(String(64), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="2")
    interval_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
```

Confirm `app/models/base.py` exports `Base` and `TimestampMixin` the way `scan_job.py` imports them; match that import exactly.

- [ ] **Step 4: Write the migration** (chain from `0039`; create `scan_schedules` with all columns, the FK, and indexes on `tenant_id`, `engagement_id`, `next_run_at`).

```python
# manager/backend/alembic/versions/0040_scan_schedule.py
"""scan schedules for continuous rescanning

Revision ID: 0040
Revises: 0039
"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision = "0040"
down_revision: Union[str, None] = "0039"
branch_labels = depends_on = None


def upgrade() -> None:
    op.create_table(
        "scan_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("use_case_id", sa.String(64), nullable=False),
        sa.Column("intensity", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("interval_hours", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_scan_schedules_tenant_id", "scan_schedules", ["tenant_id"])
    op.create_index("ix_scan_schedules_engagement_id", "scan_schedules", ["engagement_id"])
    op.create_index("ix_scan_schedules_next_run_at", "scan_schedules", ["next_run_at"])


def downgrade() -> None:
    op.drop_table("scan_schedules")
```

- [ ] **Step 5: Run the model test to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scan_schedule_model.py -q`
Expected: PASS.

- [ ] **Step 6: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/scan_schedule.py manager/backend/alembic/versions/0040_scan_schedule.py manager/backend/app/models/__init__.py
git commit -m "feat(scheduling): ScanSchedule model + migration

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task F2: Due-schedule computation + worker tick

**Files:**
- Create: `manager/backend/app/services/scheduler.py`
- Modify: `manager/backend/app/workers/reaper.py` (or the existing periodic worker loop — verify which worker already ticks on an interval and add the schedule check there)
- Test: `manager/backend/tests/test_scheduler.py`

**Interfaces:**
- Consumes: `ScanSchedule` rows.
- Produces: `scheduler.due_schedules(rows, now) -> list[ScanSchedule]` (enabled and `next_run_at <= now`); `scheduler.advance(schedule, now) -> None` (sets `last_run_at=now`, `next_run_at=now+interval`). Enqueues one `ScanJob` per due schedule via the existing enqueue path, then advances it.

- [ ] **Step 1: Write the failing pure-logic test**

```python
# manager/backend/tests/test_scheduler.py
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from app.services.scheduler import due_schedules, advance

def _s(enabled, next_run_offset_h, interval=24):
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return SimpleNamespace(enabled=enabled, interval_hours=interval,
                           next_run_at=now + timedelta(hours=next_run_offset_h),
                           last_run_at=None)

def test_only_enabled_and_due_are_returned():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    due = _s(True, -1)        # past due
    future = _s(True, +5)     # not yet
    disabled = _s(False, -1)  # due but off
    got = due_schedules([due, future, disabled], now)
    assert got == [due]

def test_advance_sets_next_run_by_interval():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    s = _s(True, -1, interval=12)
    advance(s, now)
    assert s.last_run_at == now
    assert s.next_run_at == now + timedelta(hours=12)
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scheduler.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the scheduler logic**

```python
# manager/backend/app/services/scheduler.py
"""
scheduler.py — decide which scan schedules are due, and advance them.

Pure functions kept apart from the worker that calls them, so the "is it due?"
and "when next?" logic is unit-testable without a database or a clock. The worker
loads enabled schedules, enqueues one job per due schedule through the SAME
enqueue path an operator uses (so scope, capability and queue-cap checks all
apply), then advances each. Incremental by construction: each run targets the
engagement's current scope, and Workstream D surfaces what changed.
"""
from __future__ import annotations
from datetime import datetime, timedelta


def due_schedules(rows, now: datetime) -> list:
    return [s for s in rows if s.enabled and s.next_run_at <= now]


def advance(schedule, now: datetime) -> None:
    schedule.last_run_at = now
    schedule.next_run_at = now + timedelta(hours=schedule.interval_hours)
```

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scheduler.py -q`
Expected: PASS (2 tests).

- [ ] **Step 5: Wire the tick into the periodic worker**

Identify the worker that already runs on an interval (`app/workers/reaper.py` runs every 60s per its own logs). Add a `scheduler_tick(session_factory)` coroutine that: opens a session, selects enabled `ScanSchedule` rows with `next_run_at <= project_now()`, and for each calls the existing job-enqueue routine (the same one `POST /agents/jobs` uses — import and reuse it, do NOT duplicate the enqueue logic) with the schedule's `engagement_id`, `use_case_id`, `intensity`, then `advance()` and commit. Guard the whole tick in try/except so one bad schedule can't kill the worker loop.

- [ ] **Step 6: Write a tick integration test** (mock the session + enqueue; assert a due schedule enqueues once and is advanced, a not-due one does neither).

```python
# append to tests/test_scheduler.py
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_tick_enqueues_due_and_advances(monkeypatch):
    from app.services import scheduler as sch
    now = __import__("datetime").datetime(2026, 1, 1, tzinfo=__import__("datetime").timezone.utc)
    due = SimpleNamespace(enabled=True, interval_hours=24,
                          next_run_at=now - __import__("datetime").timedelta(hours=1),
                          last_run_at=None, engagement_id=uuid.uuid4(),
                          use_case_id="uc_network_va", intensity=2, tenant_id=uuid.uuid4())
    enqueue = AsyncMock()
    await sch.run_due(rows=[due], now=now, enqueue=enqueue)
    enqueue.assert_awaited_once()
    assert due.next_run_at == now + __import__("datetime").timedelta(hours=24)
```

Add the thin orchestrator `run_due(rows, now, enqueue)` to `scheduler.py` that loops `due_schedules`, awaits `enqueue(schedule)`, then `advance(schedule, now)` — this is the unit-testable core the worker calls with a real enqueue closure.

- [ ] **Step 7: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scheduler.py -q`
Expected: PASS (3 tests).

- [ ] **Step 8: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add manager/backend/app/services/scheduler.py manager/backend/app/workers/reaper.py manager/backend/tests/test_scheduler.py
git commit -m "feat(scheduling): due-schedule tick enqueues recurring rescans

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task F3: Schedule CRUD endpoints

**Files:**
- Create: `manager/backend/app/routers/scan_schedules.py`
- Modify: `manager/backend/app/main.py` (register the router)
- Test: `manager/backend/tests/test_scan_schedule_api.py`

**Interfaces:**
- Produces: `POST /scan-schedules` (create), `GET /scan-schedules?engagement_id=`, `PATCH /scan-schedules/{id}` (enable/disable, change interval), `DELETE /scan-schedules/{id}` — all tenant-scoped, RBAC `["admin","manager"]`, following `routers/sla_policy.py` as the CRUD template.

- [ ] **Step 1: Write the failing create-validation test**

```python
# manager/backend/tests/test_scan_schedule_api.py
import uuid, pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.routers import scan_schedules as ss

def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")

@pytest.mark.asyncio
async def test_interval_below_one_hour_is_rejected():
    body = SimpleNamespace(engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
                           intensity=2, interval_hours=0)
    with pytest.raises(HTTPException) as e:
        await ss.create_schedule(body, MagicMock(), _user())
    assert e.value.status_code == 422
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scan_schedule_api.py -q`
Expected: FAIL, `ModuleNotFoundError`.

- [ ] **Step 3: Write the router** — Pydantic `ScheduleIn` (`interval_hours: int = Field(ge=1, le=8760)`, `intensity: int = Field(ge=1, le=3)`), the four handlers, tenant scoping via the engagement join, `next_run_at = project_now() + interval` on create. Register in `main.py` next to the other `app.include_router(...)` calls.

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_scan_schedule_api.py -q`
Expected: PASS.

- [ ] **Step 5: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/routers/scan_schedules.py manager/backend/app/main.py manager/backend/tests/test_scan_schedule_api.py
git commit -m "feat(scheduling): scan-schedule CRUD endpoints

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Workstream G — ServiceNow ticketing (manager)

*Extends the existing integration framework (`email|slack|jira`) with ServiceNow. Smallest workstream; independent. Follows the Jira integration as a template.*

### Task G1: Add ServiceNow as an integration kind

**Files:**
- Modify: `manager/backend/app/routers/integrations.py` (`_KINDS`)
- Modify: `manager/backend/app/services/notifications.py` (add `_send_servicenow`)
- Test: `manager/backend/tests/test_servicenow_integration.py`

**Interfaces:**
- Consumes: integration config `{url, username, table, ...}` + secret (API token/password) via the existing integration storage.
- Produces: `notifications._send_servicenow(config, secret, subject, body)` creates an incident via the ServiceNow Table API; `_KINDS` includes `"servicenow"`.

- [ ] **Step 1: Write the failing test**

```python
# manager/backend/tests/test_servicenow_integration.py
from app.routers.integrations import _KINDS

def test_servicenow_is_an_accepted_kind():
    assert "servicenow" in _KINDS

def test_send_servicenow_requires_config(monkeypatch):
    from app.services import notifications as n
    import pytest
    with pytest.raises(ValueError):
        n._send_servicenow({}, None, "subj", "body")   # missing url/table
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_servicenow_integration.py -q`
Expected: FAIL, `assert 'servicenow' in {...}`.

- [ ] **Step 3: Add ServiceNow support**

In `integrations.py`: `_KINDS = {"email", "slack", "jira", "servicenow"}` (and update the endpoint summary/docstrings that enumerate kinds). In `notifications.py`, add `_send_servicenow` mirroring `_send_jira`'s validation-and-post shape:

```python
def _send_servicenow(config: dict, secret: str | None, subject: str, body: str) -> None:
    """Create a ServiceNow incident via the Table API.

    Mirrors _send_jira: validate required config, POST a minimal incident. The
    secret is the API password/token; never logged. Fails loud on missing config
    so a misconfigured integration is caught at test time, not silently dropped.
    """
    url = (config or {}).get("URL")
    table = (config or {}).get("TABLE", "incident")
    user = (config or {}).get("USERNAME")
    if not url or not user or not secret:
        raise ValueError("servicenow integration missing URL/USERNAME/token")
    import httpx
    resp = httpx.post(
        f"{url.rstrip('/')}/api/now/table/{table}",
        auth=(user, secret),
        json={"short_description": subject, "description": body},
        timeout=15.0,
    )
    resp.raise_for_status()
```

Wire it into the same dispatch switch that routes `jira`/`slack`/`email` (find where `_send_jira` is called and add the `servicenow` branch).

- [ ] **Step 4: Run to confirm it passes**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/test_servicenow_integration.py -q`
Expected: PASS.

- [ ] **Step 5: Run the full backend suite**

Run: `cd manager/backend && ./.venv/bin/python -m pytest tests/ -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/routers/integrations.py manager/backend/app/services/notifications.py manager/backend/tests/test_servicenow_integration.py
git commit -m "feat(integrations): ServiceNow incident creation

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Deferred / explicitly out of scope

- **Probe self-exposure (ports 7070/9092) and raw-evidence redaction/retention** — real operational hardening, but infra/policy work, not a feature slice; track separately.
- **`skip_reason` / null `devices` schema consistency on timed-out runs** — Workstream E's honest partial-result reporting addresses the port-scan case; a broader schema-consistency pass across all scanners is a separate cleanup.
- **UI wiring** — every workstream above ends at an API/fact/rule. Surfacing group_key, MTTR, delta, and schedules in the Next.js dashboard is a follow-on frontend plan.
- **Attack-path expansion** — `detection/attack_paths.py` already exists; deepening it (the "19 cameras next to unsigned-SMB PCs → one risk story") is an enhancement to existing code, not a gap, and deserves its own plan.

## Rollout note (all workstreams)

Manager code is baked into `vedha-backend:local` and the detection engine into `/opt/detection_engine`; probe code loads at process start. After merging, each affected component needs: **rebuild image → `docker compose up -d` (manager) / restart probe**. Migrations (`0039`, `0040`) run via the `migrate` service on `docker compose up`. Verify with `alembic current` = `0040` after F1.

## Self-review

- **Coverage:** the 7 gaps map to A1 (EOL) + A2/B1/B2 (default-cred + grouping) + C1/C2 (MTTR/owner) + D1 (delta) + E1/E2 (checkpointing) + F1/F2/F3 (scheduling) + G1 (ServiceNow). All covered.
- **Correction folded in:** MTTR data (`first_seen`/`resolved_at`) largely pre-exists — C1 adds only `assigned_to` + `resolved_at`, C2 only computes. Stated in C1's interfaces.
- **Type consistency:** `parse_auth_surface` returns `{scheme,realm,vendor}` in B1 and is read by `_default_cred_candidate` in B2; `lookup_eol` shape consistent A1; `group_key_for` signature consistent A2; `due_schedules`/`advance`/`run_due` consistent across F2.
- **Verify-before-code flags:** three tasks say "verify" an import/scope point (C2 imports, E2 workflow mirror + preset var in scope, F2 which worker ticks, F1 models/__init__). These are real unknowns the implementer must confirm against the file, not placeholders in the deliverable.
