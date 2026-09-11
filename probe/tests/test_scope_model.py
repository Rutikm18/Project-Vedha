"""Phase 1 — typed-scope model: interface classification, the permanent denylist,
Segment validation, the job-scope re-check, container/WSL2 refusal, IPv6 note.
Pure logic — no network, no root."""
from __future__ import annotations

from agent import scope_model as sm


# ── classify_interface ───────────────────────────────────────────────────────
def test_classify_loopback():
    assert sm.classify_interface("lo") == "loopback"
    assert sm.classify_interface("lo0") == "loopback"

def test_classify_tunnel():
    for n in ("tun0", "utun3", "wg0", "ppp0", "tailscale0"):
        assert sm.classify_interface(n) == "tunnel", n

def test_classify_container_and_virtual():
    assert sm.classify_interface("docker0") == "container"
    assert sm.classify_interface("veth1a2b") == "container"
    assert sm.classify_interface("vEthernet (WSL)") == "virtual"
    assert sm.classify_interface("vmnet8") == "virtual"

def test_classify_physical_default():
    for n in ("eth0", "en0", "ens160", "Ethernet 2", "wlan0"):
        assert sm.classify_interface(n) == "physical", n


# ── is_denied (permanent denylist) ───────────────────────────────────────────
def test_denylist_blocks_special_ranges():
    assert sm.is_denied("127.0.0.1")
    assert sm.is_denied("169.254.169.254")     # cloud metadata (link-local)
    assert sm.is_denied("169.254.0.0/16")
    assert sm.is_denied("224.0.0.1")           # multicast
    assert sm.is_denied("255.255.255.255")     # broadcast
    assert sm.is_denied("::1")                 # IPv6 out of scope v1 → denied
    assert sm.is_denied("not-an-ip")           # unparseable → fail-closed

def test_denylist_allows_normal_private_ranges():
    assert not sm.is_denied("192.168.1.0/24")
    assert not sm.is_denied("10.20.0.5")

def test_denylist_blocks_manager_address():
    assert sm.is_denied("10.20.0.0/24", manager_ip="10.20.0.9")
    assert not sm.is_denied("10.20.0.0/24", manager_ip="10.99.0.9")


# ── Segment validation ───────────────────────────────────────────────────────
def test_valid_it_segment_passes():
    seg = sm.Segment(cidr="10.20.0.0/24", type="IT", profile="it", site="hq")
    assert sm.validate_segment(seg) == []

def test_ot_active_is_rejected_in_v1():
    seg = sm.Segment(cidr="10.99.0.0/24", type="OT", active=True, site="plant")
    errs = sm.validate_segment(seg)
    assert any("OT" in e for e in errs)

def test_never_segment_must_be_inactive():
    seg = sm.Segment(cidr="10.0.9.0/24", type="NEVER", active=True)
    assert any("NEVER" in e for e in sm.validate_segment(seg))

def test_active_segment_requires_site_and_valid_cidr():
    assert any("site" in e for e in sm.validate_segment(sm.Segment(cidr="10.0.0.0/24", type="IT", profile="it")))
    assert any("cidr" in e for e in sm.validate_segment(sm.Segment(cidr="notacidr", type="IT", profile="it", site="hq")))


# ── target_allowed (job-scope re-check) ──────────────────────────────────────
SEGMENTS = [
    sm.Segment(cidr="10.20.0.0/24", type="IT", profile="it", site="hq"),
    sm.Segment(cidr="10.99.0.0/24", type="OT", active=False, site="plant"),
]

def test_target_allowed_inside_it_segment():
    ok, why = sm.target_allowed("10.20.0.5", SEGMENTS)
    assert ok and why == "IT"

def test_target_in_ot_segment_is_refused():
    ok, why = sm.target_allowed("10.99.0.5", SEGMENTS)
    assert not ok

def test_target_on_denylist_is_refused():
    ok, why = sm.target_allowed("169.254.169.254", SEGMENTS)
    assert not ok and "denylist" in why


# ── container / WSL2 refusal ─────────────────────────────────────────────────
def test_detect_container_signals():
    assert sm.detect_container(dockerenv_exists=True, cgroup_text="", proc_version="") == "docker"
    assert sm.detect_container(False, "12:cpuset:/kubepods/pod123", "") == "container"
    assert sm.detect_container(False, "", "Linux ... microsoft-standard WSL2") == "wsl2"
    assert sm.detect_container(False, "", "Linux 6.1.0 generic") is None

def test_refusal_reason_for_container():
    r = sm.refusal_reason("docker")
    assert r and "not possible" in r
    assert sm.refusal_reason(None) is None


# ── IPv6 note ────────────────────────────────────────────────────────────────
def test_ipv6_note_when_no_v4():
    assert sm.ipv6_scope_note(None) is not None
    assert sm.ipv6_scope_note("192.168.1.5") is None


# ── linux `ip -j addr` parse ─────────────────────────────────────────────────
def test_parse_linux_ip_json():
    records = [
        {"ifname": "lo", "addr_info": [{"family": "inet", "local": "127.0.0.1", "prefixlen": 8}]},
        {"ifname": "eth0", "addr_info": [{"family": "inet", "local": "10.20.0.5", "prefixlen": 24}]},
        {"ifname": "docker0", "addr_info": [{"family": "inet", "local": "172.17.0.1", "prefixlen": 16}]},
    ]
    ifaces = sm.parse_linux_ip_json(records)
    by = {i.name: i for i in ifaces}
    assert by["eth0"].kind == "physical"
    assert by["eth0"].addresses == ["10.20.0.5/24"]
    assert by["lo"].kind == "loopback"
    assert by["docker0"].kind == "container"
