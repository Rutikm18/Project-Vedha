# Probe Use-Case Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise the probe's real behavior to match what each use-case *claims* — closing every overclaim found in the capability audit — without ever leaving the read-only, OT-safe collection philosophy.

**Architecture:** Additive-only changes. Wire I/O stays in the existing scanner classes; all new *interpretation* logic is factored into pure functions so it can be unit-tested against crafted byte fixtures with zero network. Descriptions are corrected FIRST (liability), then each capability is built and its claim re-added with a test — docs are never ahead of code.

**Tech Stack:** Python 3.13, stdlib only (`struct`, `socket`, `asyncio`, `urllib`, `re`), pytest. Run the probe suite with the explicit venv Python: `cd probe && .venv/bin/python -m pytest`.

## Global Constraints

- **Read-only / collection-only.** No authentication with guessed creds, no writes, no exploitation. Every new probe is a standard read request the protocol offers publicly.
- **OT profile stays passive-only, structurally.** No task in this plan adds any active probe to the `ot` profile. Active protocol probes (Modbus etc.) are out of scope here — Phase 2, gated on a product decision.
- **Scanners are extended additively, never rewritten.** New facts are added to existing `ScanResult.data`; existing fields and their meanings are unchanged so the manager's ingest and the accuracy tests keep passing.
- **Pure interpretation, mocked I/O.** New parsing logic goes in module-level pure functions (`bytes -> dict`), tested directly. No test may open a socket.
- **Docs never ahead of code.** A use-case description may only claim a capability once the task that builds it lands.
- Probe test command: `cd probe && .venv/bin/python -m pytest -q` (a bare `pytest` is intercepted by the RTK shell hook).

---

## Phase 1 — Truth alignment + read-only capability (no philosophy fork)

### Task 1: Correct the overclaiming use-case descriptions (liability fix, first)

Do this before any capability work so the shipped library never claims more than the code does. Each claim removed here is re-added by its capability task later.

**Files:**
- Modify: `probe/agent/use_cases.py` (the `USE_CASES` dict entries)
- Test: `probe/tests/test_use_cases.py` (create)

**Interfaces:**
- Produces: unchanged `USE_CASES` keys and `scan_type`/`profile` values — only `description` text changes in this task.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_use_cases.py
from agent.use_cases import USE_CASES

# Phrases that describe capabilities the probe does NOT have yet. A description
# must not contain them until the task that builds that capability updates it.
FORBIDDEN = {
    "uc_windows_estate": ["shares exposed", "shares are exposed"],
    "uc_udp_service_exposure": ["monlist", "amplification"],
    "uc_web_app_triage": ["HTTP methods"],
    "uc_iot_device_survey": ["Modbus", "banner"],
}

def test_descriptions_do_not_overclaim():
    for uc_id, banned in FORBIDDEN.items():
        desc = USE_CASES[uc_id]["description"].lower()
        for phrase in banned:
            assert phrase.lower() not in desc, f"{uc_id} still claims '{phrase}'"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py::test_descriptions_do_not_overclaim -v`
Expected: FAIL — current descriptions contain "shares exposed", "monlist", "HTTP methods", "Modbus", "banner".

- [ ] **Step 3: Rewrite the four descriptions to match today's reality**

In `probe/agent/use_cases.py` replace the four `description` values:

```python
# uc_windows_estate
"description": "SMB dialect + signing detection. Is SMBv1 enabled? Is SMB signing required?",
# uc_udp_service_exposure
"description": (
    "Probe UDP services: DNS (53), SNMP public community (161), "
    "NTP (123), NetBIOS-NS (137). Confirms which UDP services answer."
),
# uc_web_app_triage
"description": (
    "Web-layer fingerprint: response headers, server tech stack, security-header "
    "posture on all web ports. Use before a dedicated web application pentest."
),
# uc_iot_device_survey
"description": (
    "Inventory IoT/embedded devices on the IoT port set "
    "(MQTT, RTSP, CoAP, Telnet, printer/DVR ports): discovery + service banner."
),
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "docs(probe): correct overclaiming use-case descriptions to match current behavior"
```

---

### Task 2: SMB signing detection (parse the NEGOTIATE response)

**Files:**
- Modify: `probe/scanner/smb_scanner.py` (add pure parser + call it in `scan_target`)
- Test: `probe/tests/test_smb_scanner.py` (create)

**Interfaces:**
- Produces: `parse_smb2_security_mode(response: bytes) -> dict` with keys `signing_parsed: bool`, `signing_enabled: bool`, `signing_required: bool`, `negotiated_dialect: str | None`. Merged into the SMB `ScanResult.data`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_smb_scanner.py
import struct
from scanner.smb_scanner import parse_smb2_security_mode

def _smb2_negotiate_response(security_mode: int, dialect: int) -> bytes:
    # 4-byte Direct-TCP transport header + 64-byte SMB2 header + NEGOTIATE body.
    nbt = b"\x00\x00\x00\x80"
    header = b"\xfeSMB" + b"\x00" * 60            # 64-byte SMB2 header
    body = struct.pack("<HHH", 65, security_mode, dialect)  # StructSize, SecMode, Dialect
    return nbt + header + body

def test_signing_required_smb311():
    resp = _smb2_negotiate_response(0x0003, 0x0311)  # enabled + required
    out = parse_smb2_security_mode(resp)
    assert out["signing_parsed"] is True
    assert out["signing_enabled"] is True
    assert out["signing_required"] is True
    assert out["negotiated_dialect"] == "0x0311"

def test_signing_not_required():
    resp = _smb2_negotiate_response(0x0001, 0x0210)  # enabled, NOT required
    out = parse_smb2_security_mode(resp)
    assert out["signing_required"] is False

def test_garbage_response():
    assert parse_smb2_security_mode(b"nope")["signing_parsed"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_smb_scanner.py -v`
Expected: FAIL — `parse_smb2_security_mode` not defined.

- [ ] **Step 3: Add the pure parser and call it**

Add to `probe/scanner/smb_scanner.py` (module level, after imports):

```python
def parse_smb2_security_mode(response: bytes | None) -> dict:
    """Read signing posture from an SMB2 NEGOTIATE response.

    The response carries a 4-byte Direct-TCP/NBT transport header, so the SMB2
    header starts at offset 4 and the NEGOTIATE body at offset 68. Within the
    body: StructureSize[0:2], SecurityMode[2:4], DialectRevision[4:6]. Read-only.
    """
    if not response or len(response) < 72 or response[4:8] != b"\xfeSMB":
        return {"signing_parsed": False}
    security_mode = struct.unpack_from("<H", response, 70)[0]
    dialect = (struct.unpack_from("<H", response, 72)[0]
               if len(response) >= 74 else None)
    return {
        "signing_parsed": True,
        "signing_enabled": bool(security_mode & 0x0001),
        "signing_required": bool(security_mode & 0x0002),
        "negotiated_dialect": f"0x{dialect:04x}" if dialect is not None else None,
    }
```

In `scan_target`, extend the returned `data` (keep every existing field):

```python
        data = {
            "smbv1_enabled": smb1_enabled,
            "smb2_supported": smb2_supported,
        }
        data.update(parse_smb2_security_mode(smb2))
        return [ScanResult(
            self.name, target, port=self.port, proto="tcp", status="open",
            data=data,
            evidence=(f"SMBv1={'on' if smb1_enabled else 'off'}, "
                      f"SMB2={'on' if smb2_supported else 'off'}, "
                      f"signing_required={data.get('signing_required')}"),
        )]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_smb_scanner.py -v`
Expected: PASS

- [ ] **Step 5: Update the use-case claim + commit**

In `use_cases.py`, `uc_windows_estate` description now truthfully includes signing (already set in Task 1). Add a `test_use_cases.py` assertion that it mentions signing:

```python
def test_windows_estate_claims_signing():
    assert "signing" in USE_CASES["uc_windows_estate"]["description"].lower()
```

```bash
git add probe/scanner/smb_scanner.py probe/tests/test_smb_scanner.py probe/tests/test_use_cases.py
git commit -m "feat(probe): detect SMB signing-required from negotiate response"
```

---

### Task 3: DB unauthenticated-read honesty fact

**Files:**
- Modify: `probe/scanner/db_scanner.py` (factor Redis interpretation into a pure fn; add `unauthenticated_read`)
- Test: `probe/tests/test_db_unauth.py` (create)

**Interfaces:**
- Produces: `interpret_redis_info(text: str) -> dict` with keys `engine`, `auth_required`, `unauthenticated_read`, `server_version`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_db_unauth.py
from scanner.db_scanner import interpret_redis_info

def test_redis_unauthenticated():
    out = interpret_redis_info("$100\r\n# Server\r\nredis_version:7.2.4\r\n")
    assert out["auth_required"] is False
    assert out["unauthenticated_read"] is True
    assert out["server_version"] == "7.2.4"

def test_redis_authenticated():
    out = interpret_redis_info("-NOAUTH Authentication required.\r\n")
    assert out["auth_required"] is True
    assert out["unauthenticated_read"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_db_unauth.py -v`
Expected: FAIL — `interpret_redis_info` not defined.

- [ ] **Step 3: Add the pure function and use it in `_probe_redis`**

Add to `probe/scanner/db_scanner.py` (module level):

```python
def interpret_redis_info(text: str) -> dict:
    """Classify a Redis INFO reply. `unauthenticated_read` is True only when we
    actually read server data with no credentials (the honest exposure signal)."""
    auth_required = "NOAUTH" in text
    m = re.search(r"redis_version:([0-9.]+)", text)
    return {
        "engine": "redis",
        "auth_required": auth_required,
        "unauthenticated_read": (not auth_required) and ("redis_version" in text),
        "server_version": m.group(1) if m else None,
    }
```

Replace the body of `_probe_redis`'s success branch:

```python
    text = data.decode("latin-1", "replace")
    if "NOAUTH" in text or "redis_version" in text or text.startswith("$"):
        return interpret_redis_info(text)
    return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_db_unauth.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/scanner/db_scanner.py probe/tests/test_db_unauth.py
git commit -m "feat(probe): explicit unauthenticated_read fact for Redis exposure"
```

---

### Task 4: UDP real amplification probes (NTP monlist, DNS open-recursion, Memcached)

**Files:**
- Modify: `probe/scanner/udp_scanner.py` (add probes + pure interpreters + wire into `UDP_PROBES`)
- Test: `probe/tests/test_udp_amplifiers.py` (create)

**Interfaces:**
- Produces: `interpret_ntp_monlist(reply: bytes) -> bool`, `interpret_dns_recursion(reply: bytes) -> dict`, `interpret_memcached_stats(reply: bytes) -> bool`. New UDP probe port `11211` (memcached).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_udp_amplifiers.py
import struct
from scanner.udp_scanner import (
    interpret_ntp_monlist, interpret_dns_recursion, interpret_memcached_stats,
    _ntp_monlist_probe, _memcached_stats_probe,
)

def test_ntp_monlist_enabled():
    reply = bytes([0x17 | 0x80]) + b"\x00" * 100   # mode 7 + response bit
    assert interpret_ntp_monlist(reply) is True

def test_ntp_monlist_absent():
    assert interpret_ntp_monlist(b"") is False
    assert interpret_ntp_monlist(b"\x1c" + b"\x00" * 47) is False  # normal mode-4

def test_dns_open_recursion():
    # flags: QR=1, RD=1, RA=1, RCODE=0 -> 0x8180 ; ANCOUNT=1
    header = b"\x13\x37" + struct.pack(">H", 0x8180) + struct.pack(">HHHH", 1, 1, 0, 0)
    out = interpret_dns_recursion(header + b"\x00" * 4)
    assert out["recursion_available"] is True
    assert out["open_recursion"] is True

def test_memcached_exposed():
    assert interpret_memcached_stats(b"STAT pid 123\r\n") is True
    assert interpret_memcached_stats(b"") is False

def test_probe_builders_are_bytes():
    assert isinstance(_ntp_monlist_probe(), bytes)
    assert _memcached_stats_probe().endswith(b"stats\r\n")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_udp_amplifiers.py -v`
Expected: FAIL — new symbols not defined.

- [ ] **Step 3: Add probes + interpreters + register memcached**

Add to `probe/scanner/udp_scanner.py`:

```python
def _ntp_monlist_probe() -> bytes:
    # NTP mode 7 (private), impl NTPDC(3), request MON_GETLIST_1(42=0x2a). Read-only:
    # asks the server for its own monitor list. A reply = classic amplification vector.
    return b"\x17\x00\x03\x2a" + b"\x00" * 4

def _memcached_stats_probe() -> bytes:
    # Memcached UDP frame header (reqid, seq, total=1, reserved) + "stats\r\n".
    return b"\x00\x00\x00\x00\x00\x01\x00\x00" + b"stats\r\n"

def interpret_ntp_monlist(reply: bytes) -> bool:
    # mode-7 response: response bit (0x80) set AND mode field (low 3 bits) == 7.
    return bool(reply) and bool(reply[0] & 0x80) and (reply[0] & 0x07) == 7

def interpret_dns_recursion(reply: bytes) -> dict:
    if len(reply) < 12:
        return {"responded": False, "recursion_available": False, "open_recursion": False}
    flags = struct.unpack(">H", reply[2:4])[0]
    rcode = flags & 0x000F
    ra = bool(flags & 0x0080)
    ancount = struct.unpack(">H", reply[6:8])[0]
    return {"responded": True, "recursion_available": ra,
            "open_recursion": ra and rcode == 0 and ancount > 0}

def interpret_memcached_stats(reply: bytes) -> bool:
    return b"STAT " in (reply or b"")
```

Register the two new UDP ports (extend `UDP_PROBES`):

```python
UDP_PROBES: dict[int, tuple[str, bytes]] = {
    53: ("dns", _dns_probe()),
    123: ("ntp", _ntp_probe()),
    161: ("snmp", _snmp_probe()),
    137: ("netbios-ns", _netbios_probe()),
    11211: ("memcached", _memcached_stats_probe()),
}
```

In `_probe`, after a positive reply, enrich the `data` dict using the interpreters:

```python
        result_data = {"service": svc, "responded": True,
                       "reply_bytes": len(data), "reply_hex_head": data[:48].hex()}
        if svc == "ntp":
            result_data["monlist_enabled"] = interpret_ntp_monlist(
                _ntp_monlist_reply(target, port))  # see note below
        if svc == "dns":
            result_data.update(interpret_dns_recursion(data))
        if svc == "memcached":
            result_data["exposed_unauthenticated"] = interpret_memcached_stats(data)
        return ScanResult(self.name, target, port=port, proto="udp",
                          status="open", data=result_data,
                          evidence=f"{svc} replied with {len(data)} bytes")
```

> NOTE for the implementer: the NTP monlist probe is a *second* datagram. Add a
> helper `_send_recv` call for it inside `_probe` when `svc == "ntp"` (send
> `_ntp_monlist_probe()` after the mode-3 probe), and pass that reply to
> `interpret_ntp_monlist`. Keep it inside the existing semaphore/limiter scope.
> If monlist gets no reply, set `monlist_enabled=False`.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_udp_amplifiers.py -v`
Expected: PASS

- [ ] **Step 5: Re-add the amplification claim + commit**

Update `uc_udp_service_exposure` description to truthfully mention amplification checks and add a `test_use_cases.py` assertion:

```python
def test_udp_claims_amplification():
    d = USE_CASES["uc_udp_service_exposure"]["description"].lower()
    assert "amplification" in d or "monlist" in d
```

Description (replace Task-1 interim text):
```python
"description": (
    "UDP attack surface + amplification checks: NTP monlist (123), DNS open "
    "recursion (53), Memcached (11211), SNMP public (161), NetBIOS-NS (137)."
),
```

```bash
git add probe/scanner/udp_scanner.py probe/tests/test_udp_amplifiers.py \
        probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "feat(probe): real UDP amplification probes (monlist, open recursion, memcached)"
```

---

### Task 5: Web OPTIONS method enumeration + robots.txt

**Files:**
- Modify: `probe/scanner/web_scanner.py` (add pure `parse_allow_header`; issue an OPTIONS request)
- Test: `probe/tests/test_web_methods.py` (create)

**Interfaces:**
- Produces: `parse_allow_header(allow: str | None) -> dict` with keys `allowed_methods: list[str]`, `dangerous_methods: list[str]`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_web_methods.py
from scanner.web_scanner import parse_allow_header

def test_dangerous_methods_flagged():
    out = parse_allow_header("GET, POST, PUT, DELETE, OPTIONS, TRACE")
    assert "PUT" in out["dangerous_methods"]
    assert "DELETE" in out["dangerous_methods"]
    assert "TRACE" in out["dangerous_methods"]
    assert "GET" in out["allowed_methods"]

def test_safe_methods_only():
    out = parse_allow_header("GET, HEAD, OPTIONS")
    assert out["dangerous_methods"] == []

def test_no_allow_header():
    assert parse_allow_header(None)["allowed_methods"] == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_web_methods.py -v`
Expected: FAIL — `parse_allow_header` not defined.

- [ ] **Step 3: Add the parser + an OPTIONS fetch**

Add to `probe/scanner/web_scanner.py` (module level):

```python
_DANGEROUS_METHODS = {"PUT", "DELETE", "TRACE", "CONNECT", "PATCH"}

def parse_allow_header(allow: str | None) -> dict:
    """Read the Allow header from an OPTIONS response. Read-only."""
    if not allow:
        return {"allowed_methods": [], "dangerous_methods": []}
    methods = [m.strip().upper() for m in allow.split(",") if m.strip()]
    return {
        "allowed_methods": methods,
        "dangerous_methods": [m for m in methods if m in _DANGEROUS_METHODS],
    }
```

Add an OPTIONS request in `_fetch` (after the GET block, before `return`):

```python
    allow = None
    try:
        opt = urllib.request.Request(url, method="OPTIONS")
        with _OPENER.open(opt, timeout=timeout) as r:
            allow = r.headers.get("Allow")
    except Exception:
        allow = None
```

and merge into the returned dict:

```python
        **parse_allow_header(allow),
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_web_methods.py -v`
Expected: PASS

- [ ] **Step 5: Re-add the "HTTP methods" claim + commit**

Update `uc_web_app_triage` description to include HTTP methods, and assert it:

```python
def test_web_claims_methods():
    assert "method" in USE_CASES["uc_web_app_triage"]["description"].lower()
```

```bash
git add probe/scanner/web_scanner.py probe/tests/test_web_methods.py \
        probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "feat(probe): enumerate HTTP methods via OPTIONS in web scanner"
```

---

### Task 6: IoT survey collects banners

**Files:**
- Modify: `probe/agent/use_cases.py` (`uc_iot_device_survey.scan_type`: `discovery` → `service_fingerprint`)
- Test: `probe/tests/test_use_cases.py` (add)

**Interfaces:**
- Consumes: `agent.use_cases.resolve`. `service_fingerprint` already maps to a banner-ceiling mode in `engine._SCAN_MAP`.

- [ ] **Step 1: Write the failing test**

```python
def test_iot_survey_collects_banners():
    from agent.use_cases import resolve
    scan_type, profile = resolve("uc_iot_device_survey", None, {})
    assert scan_type == "service_fingerprint"   # reaches the banner stage
    assert profile == "iot"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py::test_iot_survey_collects_banners -v`
Expected: FAIL — currently resolves to `discovery` (stops at port scan, no banner).

- [ ] **Step 3: Change the scan_type**

In `use_cases.py`, `uc_iot_device_survey`: set `"scan_type": "service_fingerprint"`.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "feat(probe): IoT survey reaches the banner stage (service_fingerprint)"
```

---

### Task 7: Widen the IT port catalog (container/cloud/infra)

**Files:**
- Modify: `probe/workflow/gates.py:22-24` (`IT_PORTS`)
- Test: `probe/tests/test_port_catalog.py` (create)

**Interfaces:**
- Produces: `gates.IT_PORTS` now a superset including modern infra ports. Consumed by `_port_candidates` / `PROFILE_PORTS`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_port_catalog.py
from workflow.gates import IT_PORTS

def test_modern_infra_ports_present():
    for p in (111, 623, 2049, 2375, 5060, 6443, 10250):  # rpcbind,IPMI,NFS,Docker,SIP,k8s,kubelet
        assert p in IT_PORTS, f"port {p} missing from IT_PORTS"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_port_catalog.py -v`
Expected: FAIL — new ports absent.

- [ ] **Step 3: Extend IT_PORTS**

In `probe/workflow/gates.py` append the new ports to `IT_PORTS` (keep existing, sorted):

```python
IT_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 389, 443, 445, 465, 587,
           623, 636, 993, 995, 1433, 1521, 2049, 2375, 3306, 3389, 5060, 5432, 5900,
           5985, 5986, 6379, 6443, 8000, 8080, 8443, 9200, 10250, 11211, 27017]
```

- [ ] **Step 4: Run test to verify it passes + full suite (no regression)**

Run: `cd probe && .venv/bin/python -m pytest tests/test_port_catalog.py -v && .venv/bin/python -m pytest -q`
Expected: PASS, and 290+ prior tests still green.

- [ ] **Step 5: Commit**

```bash
git add probe/workflow/gates.py probe/tests/test_port_catalog.py
git commit -m "feat(probe): add container/cloud/infra ports to IT catalog"
```

---

### Task 8: Dynamic routing for DB services on non-standard ports

**Files:**
- Modify: `probe/workflow/router.py` (add `looks_like_db` + `db` candidate branch)
- Modify: `probe/workflow/workflow_engine.py:360-363` (consume the db routing hint)
- Test: `probe/tests/test_router_db.py` (create)

**Interfaces:**
- Consumes: `router.route_branches(asset, candidate_branches)`.
- Produces: `route_branches` may now return a `"db"` branch for a port whose banner matches a DB greeting signature. `gate_5_branch_eligible("db", ..., dynamically_routed=True)` already accepts a routed branch.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_router_db.py
from workflow.router import looks_like_db

def test_mysql_greeting_on_odd_port():
    # MySQL greeting carries a version string like "5.7.42-log" early in the banner.
    assert looks_like_db({"banner": "J\\x00\\x00\\x00\\x0a5.7.42-log\\x00"}) is True

def test_redis_noauth_signature():
    assert looks_like_db({"banner": "-NOAUTH Authentication required."}) is True

def test_plain_http_is_not_db():
    assert looks_like_db({"first_line": "HTTP/1.1 200 OK", "banner": "<html>"}) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_router_db.py -v`
Expected: FAIL — `looks_like_db` not defined.

- [ ] **Step 3: Add the signature check and route it**

Add to `probe/workflow/router.py`:

```python
import re as _re

_DB_SIGNATURES = (
    _re.compile(r"[0-9]+\.[0-9]+\.[0-9]+-(log|mariadb|ubuntu)", _re.I),  # MySQL/MariaDB greeting
    _re.compile(r"NOAUTH|redis_version", _re.I),                          # Redis
    _re.compile(r"ismaster|mongodb", _re.I),                             # MongoDB
)

def looks_like_db(banner_fact: dict | None) -> bool:
    """True when a service banner carries a database greeting signature, so a DB
    on a non-standard port still routes to db_scan. Never matches HTTP."""
    if not banner_fact or looks_like_http(banner_fact):
        return False
    hay = f"{banner_fact.get('banner') or ''} {banner_fact.get('first_line') or ''}"
    return any(rx.search(hay) for rx in _DB_SIGNATURES)
```

Extend `route_branches` to include `db` when requested:

```python
def route_branches(asset, candidate_branches=("tls", "web", "db")):
    routed = {}
    for port in asset.open_ports_for_deep_scan():
        fact = asset.services.get(port)
        branches = set()
        if "web" in candidate_branches and fact and looks_like_http(fact):
            branches.add("web")
        if "tls" in candidate_branches and looks_like_tls(port, fact):
            branches.add("tls")
        if "db" in candidate_branches and looks_like_db(fact):
            branches.add("db")
        if branches:
            routed[port] = branches
    return routed
```

In `workflow_engine.py`, capture the db routing and pass it to the db branch (replace the db-branch guard at line ~401):

```python
        db_dynamic = {p for p, b in routed.items() if "db" in b}
        if gate_5_branch_eligible("db", asset, profile, service_filter, bool(db_dynamic)):
            ports = sorted((asset.open_ports_for_deep_scan() & DB_PORTS) | db_dynamic)
```

- [ ] **Step 4: Run test to verify it passes + full suite**

Run: `cd probe && .venv/bin/python -m pytest tests/test_router_db.py -v && .venv/bin/python -m pytest -q`
Expected: PASS, no regressions.

- [ ] **Step 5: Commit**

```bash
git add probe/workflow/router.py probe/workflow/workflow_engine.py probe/tests/test_router_db.py
git commit -m "feat(probe): route DB services on non-standard ports via banner signature"
```

---

### Task 9: Surface the authenticated-inventory use-cases

**Files:**
- Modify: `probe/agent/use_cases.py` (two new `USE_CASES` entries)
- Test: `probe/tests/test_use_cases.py` (add)

**Interfaces:**
- Consumes: `resolve`. Both resolve to `scan_type="assessment"` (full funnel); credentials arrive via job `params.ssh_creds` / `params.win_creds` (`engine._tuning_from_params`), gating Gate-6 collection.

- [ ] **Step 1: Write the failing test**

```python
def test_authenticated_inventory_use_cases_exist():
    from agent.use_cases import USE_CASES, resolve
    for uc in ("uc_linux_authenticated_inventory", "uc_windows_authenticated_inventory"):
        assert uc in USE_CASES
        scan_type, profile = resolve(uc, None, {})
        assert scan_type == "assessment"
        assert "credential" in USE_CASES[uc]["description"].lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py::test_authenticated_inventory_use_cases_exist -v`
Expected: FAIL — keys absent.

- [ ] **Step 3: Add the entries**

Add to `USE_CASES` in `use_cases.py`:

```python
    "uc_linux_authenticated_inventory": {
        "display_name": "Authenticated Linux Inventory",
        "description": (
            "Credentialed read-only inventory over SSH: OS release, package list "
            "(dpkg/rpm), listening sockets. Highest-fidelity CVE input. Requires "
            "operator-supplied SSH credentials."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "2–10 min per host",
    },
    "uc_windows_authenticated_inventory": {
        "display_name": "Authenticated Windows Inventory",
        "description": (
            "Credentialed read-only inventory over WinRM (SMB fallback): OS build, "
            "hotfixes/KBs, installed software, services. Requires operator-supplied "
            "Windows credentials."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "3–15 min per host",
    },
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_use_cases.py -v`
Expected: PASS

- [ ] **Step 5: Commit + run the whole probe suite**

```bash
cd probe && .venv/bin/python -m pytest -q
git add probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "feat(probe): add authenticated Linux/Windows inventory use-cases"
```

---

## Phase 2 — Boundary-crossing capabilities (DECISION MADE: SMB shares + web safe-files + IoT protocols; Modbus deferred, `ot` stays passive)

**Hard rules for this phase:**
- **`ot` profile is never touched.** No active probe here is ever reachable from the `ot` profile — `gate_0_is_passive_profile` short-circuits before any of these run.
- **Modbus / OT industrial protocols are out of scope** — deferred to a future dedicated, opt-in, rate-capped OT-active mode.
- New IoT protocol scanners run **only** in the `iot` profile and **only** when explicitly requested (opt-in service filter), never in a default assessment.
- Same core-tech pattern as Phase 1: pure `bytes -> dict` interpreters, tested against fixtures; network calls are thin and mocked in tests.

### Task 10: SMB null-session share enumeration (impacket, graceful degrade)

Hand-rolling DCERPC/SRVSVC `NetShareEnumAll` in stdlib is error-prone; **impacket is already an optional project dependency** (`windows_collector.py` uses it). Reuse it behind the same optional-import degrade pattern.

**Files:**
- Create: `probe/scanner/smb_share_scanner.py`
- Test: `probe/tests/test_smb_shares.py`

**Interfaces:**
- Produces: `parse_share_list(raw_shares: list) -> dict` with keys `shares: list[str]`, `share_count: int`; and `HAVE_IMPACKET: bool`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_smb_shares.py
from scanner.smb_share_scanner import parse_share_list

def test_parse_shares_strips_nulls():
    # impacket listShares() returns dicts with null-terminated 'shi1_netname'
    raw = [{"shi1_netname": "ADMIN$\x00"}, {"shi1_netname": "IPC$\x00"},
           {"shi1_netname": "Public\x00"}]
    out = parse_share_list(raw)
    assert out["shares"] == ["ADMIN$", "IPC$", "Public"]
    assert out["share_count"] == 3

def test_parse_empty():
    assert parse_share_list([]) == {"shares": [], "share_count": 0}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_smb_shares.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Create the scanner**

```python
# probe/scanner/smb_share_scanner.py
"""smb_share_scanner.py — read-only null-session share LISTING (no file access).

Lists shares via an anonymous SMB session. Unauthenticated and read-only, but
more intrusive than negotiate-only, so it is a separate, opt-in module. Uses
impacket when present; degrades to "capability unavailable" when it is not.
"""
from __future__ import annotations

from .scanner_base import BaseScanner, ScanResult

try:
    from impacket.smbconnection import SMBConnection
    HAVE_IMPACKET = True
except ImportError:
    HAVE_IMPACKET = False


def parse_share_list(raw_shares: list) -> dict:
    """Normalize impacket's listShares() output to plain names."""
    names = []
    for s in raw_shares or []:
        name = s.get("shi1_netname", "") if isinstance(s, dict) else str(s)
        names.append(name.rstrip("\x00"))
    return {"shares": names, "share_count": len(names)}


class SMBShareScanner(BaseScanner):
    name = "smb_share_scan"

    def __init__(self, *args, port: int = 445, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port

    def _list(self, target: str) -> dict | None:
        if not HAVE_IMPACKET:
            return None
        try:
            conn = SMBConnection(target, target, sess_port=self.port,
                                 timeout=int(self.timeout))
            conn.login("", "")  # null session — no credentials
            shares = conn.listShares()
            conn.close()
            return parse_share_list(shares)
        except Exception:
            return None

    async def scan_target(self, target: str) -> list[ScanResult]:
        import asyncio
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            info = await loop.run_in_executor(None, self._list, target)
        if info is None:
            return []  # unavailable or refused — nothing to report
        return [ScanResult(
            self.name, target, port=self.port, proto="tcp", status="open",
            data={"null_session": True, **info},
            evidence=f"null-session shares: {', '.join(info['shares']) or 'none'}")]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_smb_shares.py -v`
Expected: PASS

- [ ] **Step 5: Re-add the "shares" claim + commit**

Update `uc_windows_estate` description to include share exposure, and assert it in `test_use_cases.py`:

```python
def test_windows_estate_claims_shares():
    assert "share" in USE_CASES["uc_windows_estate"]["description"].lower()
```

Description: `"SMB dialect + signing + null-session share listing. SMBv1? Signing required? Shares exposed?"`

```bash
git add probe/scanner/smb_share_scanner.py probe/tests/test_smb_shares.py \
        probe/agent/use_cases.py probe/tests/test_use_cases.py
git commit -m "feat(probe): read-only null-session SMB share listing (impacket, graceful degrade)"
```

---

### Task 11: Web safe-file content checks (fixed set, read-only)

Bounded to a **fixed 3-path set** — never directory brute-forcing.

**Files:**
- Modify: `probe/scanner/web_scanner.py`
- Test: `probe/tests/test_web_safefiles.py`

**Interfaces:**
- Produces: `SAFE_FILES: dict`, `interpret_safe_file(path: str, status: int, body: bytes) -> str | None` (returns a finding label or None).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_web_safefiles.py
from scanner.web_scanner import interpret_safe_file, SAFE_FILES

def test_git_head_exposed():
    assert interpret_safe_file("/.git/HEAD", 200, b"ref: refs/heads/main\n") == "git_repo_exposed"

def test_dotenv_exposed():
    assert interpret_safe_file("/.env", 200, b"DB_PASSWORD=secret\nAPI_KEY=abc\n") == "dotenv_exposed"

def test_dotenv_false_on_html():
    assert interpret_safe_file("/.env", 200, b"<html>x = y</html>") is None

def test_not_found_is_none():
    assert interpret_safe_file("/.git/HEAD", 404, b"") is None

def test_fixed_set_only():
    assert set(SAFE_FILES) == {"/.git/HEAD", "/.env", "/server-status"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_web_safefiles.py -v`
Expected: FAIL — symbols not defined.

- [ ] **Step 3: Add the fixed-set checks**

Add to `probe/scanner/web_scanner.py`:

```python
_ENV_RE = re.compile(rb"(?m)^[A-Z][A-Z0-9_]*=\S")

SAFE_FILES = {
    "/.git/HEAD": ("git_repo_exposed", lambda b: b.startswith(b"ref:") or b"refs/" in b[:64]),
    "/.env": ("dotenv_exposed", lambda b: bool(_ENV_RE.search(b))),
    "/server-status": ("apache_status_exposed", lambda b: b"Apache Server Status" in b),
}

def interpret_safe_file(path: str, status: int, body: bytes) -> str | None:
    entry = SAFE_FILES.get(path)
    if not entry or status != 200:
        return None
    label, matches = entry
    return label if matches(body or b"") else None
```

In `_scan_port`, after the main fetch, check the fixed set (read-only GET each):

```python
        findings = []
        for path in SAFE_FILES:
            probe_url = f"{scheme}://{bracket_host(target)}:{port}{path}"
            hit = await loop.run_in_executor(None, _fetch_raw, probe_url, self.timeout)
            if hit:
                label = interpret_safe_file(path, hit["status"], hit["body"])
                if label:
                    findings.append(label)
        if findings:
            info["exposed_files"] = findings
```

Add a minimal `_fetch_raw` helper returning `{"status", "body"}` (mirrors `_fetch` but keeps the raw body):

```python
def _fetch_raw(url: str, timeout: float) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": "va-scanner/1.0"}, method="GET")
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": resp.read(8192)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": b""}
    except Exception:
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_web_safefiles.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/scanner/web_scanner.py probe/tests/test_web_safefiles.py
git commit -m "feat(probe): fixed-set web safe-file exposure checks (.git/.env/server-status)"
```

---

### Task 12: MQTT anonymous-connect probe (new scanner)

**Files:**
- Create: `probe/scanner/mqtt_scanner.py`
- Test: `probe/tests/test_mqtt.py`

**Interfaces:**
- Produces: `build_mqtt_connect(client_id: bytes) -> bytes`, `interpret_connack(reply: bytes) -> dict` (keys `is_connack: bool`, `accepts_anonymous: bool`, `return_code: int | None`).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_mqtt.py
from scanner.mqtt_scanner import build_mqtt_connect, interpret_connack

def test_connect_is_mqtt311():
    pkt = build_mqtt_connect(b"va-scan")
    assert pkt[0] == 0x10           # CONNECT packet type
    assert b"MQTT" in pkt           # protocol name
    assert pkt[9] == 0x04           # protocol level 4 (MQTT 3.1.1)

def test_connack_anonymous_accepted():
    out = interpret_connack(b"\x20\x02\x00\x00")   # CONNACK, rc=0
    assert out["is_connack"] is True
    assert out["accepts_anonymous"] is True
    assert out["return_code"] == 0

def test_connack_not_authorized():
    out = interpret_connack(b"\x20\x02\x00\x05")   # rc=5 not authorized
    assert out["accepts_anonymous"] is False
    assert out["return_code"] == 5

def test_non_connack():
    assert interpret_connack(b"\x00")["is_connack"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_mqtt.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Create the scanner**

```python
# probe/scanner/mqtt_scanner.py
"""mqtt_scanner.py — detect MQTT brokers that accept ANONYMOUS connections.

Read-only: sends one MQTT 3.1.1 CONNECT and reads the CONNACK return code. Does
NOT subscribe, publish, or read topics. Return code 0 = broker accepted an
anonymous client (a finding); 4/5 = auth enforced.
"""
from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import BaseScanner, ScanResult


def build_mqtt_connect(client_id: bytes = b"va-scan") -> bytes:
    var_header = b"\x00\x04MQTT" + b"\x04" + b"\x02" + b"\x00\x3c"  # name, level 4, clean-session, keepalive 60
    payload = struct.pack(">H", len(client_id)) + client_id
    body = var_header + payload
    return b"\x10" + bytes([len(body)]) + body  # remaining length (< 128)


def interpret_connack(reply: bytes) -> dict:
    if len(reply) < 4 or reply[0] != 0x20:
        return {"is_connack": False, "accepts_anonymous": False, "return_code": None}
    rc = reply[3]
    return {"is_connack": True, "accepts_anonymous": rc == 0, "return_code": rc}


class MQTTScanner(BaseScanner):
    name = "mqtt_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or [1883, 8883]

    def _connect(self, target: str, port: int) -> bytes | None:
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.sendall(build_mqtt_connect())
                return s.recv(64)
        except OSError:
            return None

    async def _probe(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            reply = await loop.run_in_executor(None, self._connect, target, port)
        if not reply:
            return None
        info = interpret_connack(reply)
        if not info["is_connack"]:
            return None
        return ScanResult(self.name, target, port=port, proto="tcp", status="open",
                          data={"service": "mqtt", **info},
                          evidence=f"MQTT CONNACK rc={info['return_code']}")

    async def scan_target(self, target: str) -> list[ScanResult]:
        results = await asyncio.gather(*(self._probe(target, p) for p in self.ports))
        return [r for r in results if r is not None]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_mqtt.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/scanner/mqtt_scanner.py probe/tests/test_mqtt.py
git commit -m "feat(probe): MQTT anonymous-connect detection (read-only CONNECT/CONNACK)"
```

---

### Task 13: RTSP OPTIONS probe (new scanner)

**Files:**
- Create: `probe/scanner/rtsp_scanner.py`
- Test: `probe/tests/test_rtsp.py`

**Interfaces:**
- Produces: `build_rtsp_options(url: str, cseq: int) -> bytes`, `parse_rtsp_public(response: bytes) -> dict` (keys `is_rtsp`, `public_methods: list[str]`).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_rtsp.py
from scanner.rtsp_scanner import build_rtsp_options, parse_rtsp_public

def test_options_request_shape():
    req = build_rtsp_options("rtsp://10.0.0.5:554/", 1)
    assert req.startswith(b"OPTIONS rtsp://10.0.0.5:554/ RTSP/1.0\r\n")
    assert b"CSeq: 1" in req

def test_parse_public():
    resp = b"RTSP/1.0 200 OK\r\nCSeq: 1\r\nPublic: OPTIONS, DESCRIBE, PLAY\r\n\r\n"
    out = parse_rtsp_public(resp)
    assert out["is_rtsp"] is True
    assert "DESCRIBE" in out["public_methods"]

def test_non_rtsp():
    assert parse_rtsp_public(b"HTTP/1.1 200 OK\r\n")["is_rtsp"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_rtsp.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Create the scanner**

```python
# probe/scanner/rtsp_scanner.py
"""rtsp_scanner.py — RTSP OPTIONS probe (read-only capability discovery).

Sends one RTSP OPTIONS and reads the Public: methods header. Does NOT DESCRIBE
a stream path, authenticate, or open media. Text protocol, HTTP-like.
"""
from __future__ import annotations

import asyncio
import socket

from .scanner_base import BaseScanner, ScanResult


def build_rtsp_options(url: str, cseq: int = 1) -> bytes:
    return (f"OPTIONS {url} RTSP/1.0\r\nCSeq: {cseq}\r\n"
            f"User-Agent: va-scanner\r\n\r\n").encode("ascii")


def parse_rtsp_public(response: bytes) -> dict:
    text = (response or b"").decode("latin-1", "replace")
    if not text.startswith("RTSP/1."):
        return {"is_rtsp": False, "public_methods": []}
    methods: list[str] = []
    for line in text.split("\r\n"):
        if line.lower().startswith("public:"):
            methods = [m.strip() for m in line.split(":", 1)[1].split(",") if m.strip()]
    return {"is_rtsp": True, "public_methods": methods}


class RTSPScanner(BaseScanner):
    name = "rtsp_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or [554]

    def _options(self, target: str, port: int) -> bytes | None:
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.sendall(build_rtsp_options(f"rtsp://{target}:{port}/"))
                return s.recv(1024)
        except OSError:
            return None

    async def _probe(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            resp = await loop.run_in_executor(None, self._options, target, port)
        info = parse_rtsp_public(resp) if resp else {"is_rtsp": False}
        if not info.get("is_rtsp"):
            return None
        return ScanResult(self.name, target, port=port, proto="tcp", status="open",
                          data={"service": "rtsp", **info},
                          evidence=f"RTSP methods: {', '.join(info['public_methods'])}")

    async def scan_target(self, target: str) -> list[ScanResult]:
        results = await asyncio.gather(*(self._probe(target, p) for p in self.ports))
        return [r for r in results if r is not None]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_rtsp.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/scanner/rtsp_scanner.py probe/tests/test_rtsp.py
git commit -m "feat(probe): RTSP OPTIONS capability probe (read-only)"
```

---

### Task 14: CoAP `.well-known/core` probe (new scanner)

**Files:**
- Create: `probe/scanner/coap_scanner.py`
- Test: `probe/tests/test_coap.py`

**Interfaces:**
- Produces: `build_coap_wellknown(mid: bytes) -> bytes`, `interpret_coap_reply(reply: bytes) -> dict` (keys `is_coap`, `content: bool`).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_coap.py
from scanner.coap_scanner import build_coap_wellknown, interpret_coap_reply

def test_request_encodes_uri_path():
    pkt = build_coap_wellknown(b"\x00\x01")
    assert pkt[0] == 0x40            # ver 1, CON, token len 0
    assert pkt[1] == 0x01            # GET
    assert b".well-known" in pkt
    assert b"core" in pkt

def test_reply_content():
    # 0x60 = ver1/ACK, 0x45 = 2.05 Content
    out = interpret_coap_reply(b"\x60\x45\x00\x01\xff</a>;rt=x")
    assert out["is_coap"] is True
    assert out["content"] is True

def test_empty_reply():
    assert interpret_coap_reply(b"")["is_coap"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_coap.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Create the scanner**

```python
# probe/scanner/coap_scanner.py
"""coap_scanner.py — CoAP resource discovery via GET /.well-known/core (RFC 7252).

Read-only: one confirmable GET for the standard discovery resource. Parses only
whether the endpoint speaks CoAP and returned content (2.05). UDP binary.
"""
from __future__ import annotations

import asyncio
import socket

from .scanner_base import BaseScanner, ScanResult


def build_coap_wellknown(mid: bytes = b"\x00\x01") -> bytes:
    header = b"\x40\x01" + mid          # ver1 / CON / TKL0, code 0.01 GET, message id
    opt1 = b"\xbb" + b".well-known"     # option 11 (Uri-Path), delta 11, len 11
    opt2 = b"\x04" + b"core"            # option 11 again, delta 0, len 4
    return header + opt1 + opt2


def interpret_coap_reply(reply: bytes) -> dict:
    if len(reply) < 2 or (reply[0] & 0xC0) != 0x40:  # CoAP version must be 1
        return {"is_coap": False, "content": False}
    code = reply[1]
    return {"is_coap": True, "content": code == 0x45}  # 2.05 Content


class CoAPScanner(BaseScanner):
    name = "coap_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or [5683]

    def _get(self, target: str, port: int) -> bytes | None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(self.timeout)
            try:
                s.sendto(build_coap_wellknown(), (target, port))
                data, _ = s.recvfrom(2048)
                return data
            finally:
                s.close()
        except OSError:
            return None

    async def _probe(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            reply = await loop.run_in_executor(None, self._get, target, port)
        info = interpret_coap_reply(reply) if reply else {"is_coap": False}
        if not info.get("is_coap"):
            return None
        return ScanResult(self.name, target, port=port, proto="udp", status="open",
                          data={"service": "coap", **info},
                          evidence=f"CoAP reply content={info['content']}")

    async def scan_target(self, target: str) -> list[ScanResult]:
        results = await asyncio.gather(*(self._probe(target, p) for p in self.ports))
        return [r for r in results if r is not None]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_coap.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add probe/scanner/coap_scanner.py probe/tests/test_coap.py
git commit -m "feat(probe): CoAP .well-known/core resource discovery (read-only)"
```

---

### Task 15: Wire the IoT protocol scanners into the funnel (iot opt-in) + a use-case

Adds one new deep branch `iot_proto` that dispatches to MQTT/RTSP/CoAP by port, allowed **only** in the `iot` profile and **only** via an explicit service filter. `ot` is untouched (Gate 0 short-circuits).

**Files:**
- Modify: `probe/workflow/gates.py` (branch table + `iot` allowed set), `probe/workflow/workflow_engine.py` (new branch block), `probe/workflow/modes.py:11` (`VALID_SERVICES`), `probe/agent/engine.py:90-108` (`_SCAN_MAP`), `probe/agent/use_cases.py`
- Test: `probe/tests/test_iot_proto_wiring.py`

**Interfaces:**
- Consumes: `gate_5_branch_eligible`, `route_branches`. Produces: `scan_type="iot_protocol_scan"` → service filter `{"iot_proto"}`; `IOT_PROTO_PORTS = {1883, 8883, 554, 5683}`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_iot_proto_wiring.py
from workflow.gates import PROFILE_DEEP_BRANCHES, IOT_PROTO_PORTS
from agent.engine import _SCAN_MAP
from agent.use_cases import USE_CASES, resolve

def test_iot_proto_only_in_iot_profile():
    assert "iot_proto" in PROFILE_DEEP_BRANCHES["iot"]
    assert "iot_proto" not in PROFILE_DEEP_BRANCHES["it"]
    assert "iot_proto" not in PROFILE_DEEP_BRANCHES["ot"]   # OT stays passive

def test_iot_proto_ports():
    assert IOT_PROTO_PORTS == {1883, 8883, 554, 5683}

def test_scan_type_registered():
    default_profile, mode, svc = _SCAN_MAP["iot_protocol_scan"]
    assert svc == {"iot_proto"}
    assert default_profile == "iot"

def test_use_case_present():
    assert resolve("uc_iot_protocol_probe", None, {}) == ("iot_protocol_scan", "iot")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_iot_proto_wiring.py -v`
Expected: FAIL — symbols not defined.

- [ ] **Step 3: Wire it in**

`modes.py`: add `"iot_proto"` to `VALID_SERVICES`.

`gates.py`: add the port set and allow the branch for `iot` only:

```python
IOT_PROTO_PORTS = {1883, 8883, 554, 5683}
# ... in PROFILE_DEEP_BRANCHES:
    "iot": {"tls", "web", "iot_proto"},
# ... in _BRANCH_PORT_TABLE:
    "iot_proto": IOT_PROTO_PORTS,
```

`engine.py`: add to `_SCAN_MAP`:

```python
    "iot_protocol_scan":    ("iot", None, {"iot_proto"}),
```

`workflow_engine.py`: import the three scanners and add a branch block inside the Gate-5 loop (after the snmp block), dispatching by port:

```python
from scanner.mqtt_scanner import MQTTScanner
from scanner.rtsp_scanner import RTSPScanner
from scanner.coap_scanner import CoAPScanner
# ...
        if gate_5_branch_eligible("iot_proto", asset, profile, service_filter):
            open_ports = asset.open_ports_for_deep_scan()
            for scanner_cls, branch_ports in (
                (MQTTScanner, {1883, 8883}), (RTSPScanner, {554}), (CoAPScanner, {5683}),
            ):
                hit = sorted(open_ports & branch_ports)
                if hit:
                    sc = scanner_cls(scope, ports=hit, rate=rate,
                                     concurrency=concurrency, timeout=timeout)
                    results = await _scan_one(sc, host)
                    _record(trace, sc.name, target_count=1, results=results)
                    _store_results(results, assets=assets, cache=cache, profile=profile)
```

`use_cases.py`: add the opt-in use-case:

```python
    "uc_iot_protocol_probe": {
        "display_name": "IoT Protocol Probe",
        "description": (
            "Read-only IoT protocol checks (iot profile): MQTT anonymous connect, "
            "RTSP OPTIONS, CoAP resource discovery. Does not touch OT/ICS."
        ),
        "scan_type": "iot_protocol_scan",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
```

- [ ] **Step 4: Run test + full suite (confirm OT untouched, no regression)**

Run: `cd probe && .venv/bin/python -m pytest tests/test_iot_proto_wiring.py -v && .venv/bin/python -m pytest -q`
Expected: PASS; all prior tests green.

- [ ] **Step 5: Commit**

```bash
git add probe/workflow/gates.py probe/workflow/workflow_engine.py probe/workflow/modes.py \
        probe/agent/engine.py probe/agent/use_cases.py probe/tests/test_iot_proto_wiring.py
git commit -m "feat(probe): opt-in IoT protocol branch (MQTT/RTSP/CoAP), iot profile only"
```

---

## Self-Review

**Spec coverage** (audit gap → task): SMB signing → T2; SMB shares → T10; DB unauthenticated → T3; UDP monlist/DNS-amp/memcached → T4; web methods → T5; web content exposure → T11; IoT banner → T6; IoT protocols (MQTT/RTSP/CoAP) → T12–T15; container/cloud ports → T7; non-standard DB ports/dynamic routing → T8; authenticated inventory use-case → T9; overclaim descriptions → T1 (re-added truthfully by T2/T4/T5/T10/T15). **Deferred by decision:** Modbus/OT active probes (never in `ot`). **Out of scope (separate follow-ups noted in the audit):** IPv6 support, TLS-vuln depth.

**Placeholder scan:** none — every code step contains complete, runnable content. The one prose NOTE (Task 4, second NTP datagram) reuses the file's existing `_send_recv` helper; its interpreters are fully specified and tested.

**Type consistency:** each pure function defined once and consumed with matching signatures — `parse_smb2_security_mode`, `interpret_redis_info`, `interpret_ntp_monlist`, `interpret_dns_recursion`, `interpret_memcached_stats`, `parse_allow_header`, `looks_like_db`, `parse_share_list`, `interpret_safe_file`, `build_mqtt_connect`/`interpret_connack`, `build_rtsp_options`/`parse_rtsp_public`, `build_coap_wellknown`/`interpret_coap_reply`. New service `"iot_proto"` is added consistently to `VALID_SERVICES`, `PROFILE_DEEP_BRANCHES["iot"]`, `_BRANCH_PORT_TABLE`, and `_SCAN_MAP`. `route_branches` default includes `"db"` in both router and engine.

**Safety invariant check:** no Phase-2 active probe is reachable from the `ot` profile — `gate_0_is_passive_profile` returns before Gate 5, and `iot_proto` is absent from `PROFILE_DEEP_BRANCHES["ot"]` (asserted in `test_iot_proto_wiring.py`).
