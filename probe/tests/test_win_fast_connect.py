"""The Windows connect fast-fail (scanner/win_fast_connect.py).

Windows answers an RST to a SYN by re-sending the SYN, so a closed port took
2.2 s to report on a customer agent and the connect scan read it as `filtered`.
These tests pin the exact bytes and control code handed to WSAIoctl (taken from
mstcpip.h), the version gate (pre-RS3 builds misread "no retransmissions" as
255), and that any failure leaves the socket untouched. The last test runs only
on Windows and measures the real effect.
"""
from __future__ import annotations

import socket
import struct
import sys
import time

import pytest

from scanner import win_fast_connect as wfc


def test_control_code_is_wsaiow_ioc_vendor_17():
    ioc_in, ioc_vendor = 0x80000000, 0x18000000
    assert wfc.SIO_TCP_INITIAL_RTO == ioc_in | ioc_vendor | 17


def test_payload_is_the_c_struct_with_padding():
    # { USHORT Rtt; UCHAR MaxSynRetransmissions; } -> 4 bytes, little-endian
    assert wfc.payload(0xFE) == struct.pack("<HBx", 0xFFFF, 0xFE)
    assert len(wfc.payload(1)) == 4


@pytest.mark.parametrize("build, expected", [
    (22631, 0xFE),      # Windows 11
    (16299, 0xFE),      # Windows 10 RS3: first build that knows "none"
    (15063, 1),         # Windows 10 RS2: "none" reads as 255 retries here
    (9200, 1),          # Windows 8
    (7601, None),       # Windows 7: no such ioctl
])
def test_version_gate(build, expected):
    assert wfc.max_syn_retransmissions(build) == expected


def test_enable_sends_the_ioctl_and_reports_success():
    calls = []

    def fake(handle, code, data):
        calls.append((handle, code, data))
        return 0

    with socket.socket() as s:
        assert wfc.enable(s, setting=0xFE, ioctl=fake) is True
        assert calls == [(s.fileno(), wfc.SIO_TCP_INITIAL_RTO, wfc.payload(0xFE))]


def test_not_applicable_does_nothing():
    def fake(*_a):
        raise AssertionError("must not be called")

    with socket.socket() as s:
        assert wfc.enable(s, setting=None, ioctl=fake) is False


def test_off_windows_it_is_a_no_op():
    if sys.platform == "win32":
        pytest.skip("checks the non-Windows default")
    wfc._setting.cache_clear()
    with socket.socket() as s:
        assert wfc.enable(s) is False
    assert wfc.describe()["applies"] is False


@pytest.mark.parametrize("outcome", [10022, RuntimeError("no ws2_32")])
def test_any_failure_leaves_the_socket_usable(outcome):
    def fake(*_a):
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    with socket.socket() as s:
        assert wfc.enable(s, setting=0xFE, ioctl=fake) is False
        s.settimeout(1)
        s.bind(("127.0.0.1", 0))       # still an ordinary socket


@pytest.mark.skipif(sys.platform != "win32", reason="measures real Windows behaviour")
def test_on_windows_a_closed_port_reports_fast():
    wfc._setting.cache_clear()
    if not wfc.describe()["applies"]:
        pytest.skip("Windows build predates SIO_TCP_INITIAL_RTO")
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()                       # nothing listens there now
    with socket.socket() as s:
        assert wfc.enable(s) is True
        s.settimeout(5)
        t0 = time.monotonic()
        with pytest.raises(ConnectionRefusedError):
            s.connect(("127.0.0.1", port))
        assert time.monotonic() - t0 < 1.0   # default Windows: ~2 s


# ── self-check (T3): did the option take effect on this machine? ─────────────

def test_closed_port_measurement_is_real():
    took = wfc.closed_port_seconds(False, timeout=2.0)
    assert took is not None and 0 <= took < 2.0


def test_fast_fail_measurement_needs_the_option():
    if sys.platform == "win32":
        pytest.skip("checks the non-Windows default")
    assert wfc.closed_port_seconds(True) is None       # nothing to apply here


def test_self_check_is_silent_off_windows(monkeypatch):
    monkeypatch.setattr(wfc, "describe", lambda: {"applies": False, "mode": "default"})
    assert wfc.self_check(include_default=True) is None


@pytest.mark.parametrize("fast, effective", [(0.002, True), (2.1, False), (None, False)])
def test_self_check_judges_the_timing(monkeypatch, fast, effective):
    monkeypatch.setattr(wfc, "describe", lambda: {"applies": True, "mode": "none"})
    timings = {True: fast, False: 2.2}
    r = wfc.self_check(include_default=True, measure=lambda ff: timings[ff])
    assert r["effective"] is effective and r["default_s"] == 2.2


def test_startup_does_not_pay_for_the_slow_default(monkeypatch):
    monkeypatch.setattr(wfc, "describe", lambda: {"applies": True, "mode": "none"})
    asked = []
    wfc.self_check(include_default=False, measure=lambda ff: asked.append(ff) or 0.001)
    assert asked == [True]


def test_doctor_reports_each_outcome():
    from agent.doctor import check_connect_fast_fail
    assert check_connect_fast_fail(None) is None
    ok = check_connect_fast_fail({"fast_fail_s": 0.002, "default_s": 2.2, "effective": True})
    assert ok.status == "pass" and "0.002s" in ok.detail and "2.2s" in ok.detail
    bad = check_connect_fast_fail({"fast_fail_s": 2.1, "default_s": 2.2, "effective": False})
    assert bad.status == "warn" and "Linux agent" in bad.remediation


def test_doctor_off_windows_has_no_fast_fail_line(tmp_path):
    if sys.platform == "win32":
        pytest.skip("checks the non-Windows default")
    from agent import doctor
    names = [c.name for c in doctor.run("", is_privileged=False, state_dir=str(tmp_path))]
    assert "connect_fast_fail" not in names
