"""
test_kernel_limits.py — A1: kernel preflight for large scans.

The probe already accounts honestly for failures the KERNEL REPORTS BACK
(EMFILE/EADDRNOTAVAIL land in scanner_base._ERRNO_MAP as `local_resource_error`,
never `filtered`). The limits checked here are the other kind: when they are
exceeded the kernel drops the packet SILENTLY, so the scanner sees only a
timeout and reports `filtered` — a false negative it cannot detect from the
inside. The only defence is to measure the ceilings up front and say so.

Pure arithmetic, monkeypatched IO — same shape as test_doctor.py.
"""
from __future__ import annotations

from agent import kernel_limits as kl

# ── ephemeral ports: the hard ceiling on connect() scanning ──────────────────

def test_max_sustained_connect_rate_is_capacity_over_time_wait():
    # Linux default range 32768-60999 = 28232 ports, TIME_WAIT 60s.
    rate = kl.max_sustained_connect_rate(32768, 60999)
    assert rate is not None
    assert abs(rate - 28232 / 60) < 0.5          # ~470 conn/sec

    # Widening the range to 1024-65535 raises the ceiling proportionally.
    wide = kl.max_sustained_connect_rate(1024, 65535)
    assert wide is not None and wide > rate * 2


def test_max_sustained_connect_rate_unknown_when_range_missing():
    assert kl.max_sustained_connect_rate(None, 60999) is None
    assert kl.max_sustained_connect_rate(32768, None) is None
    assert kl.max_sustained_connect_rate(60999, 32768) is None   # inverted


def test_ephemeral_check_warns_when_requested_rate_exceeds_ceiling():
    # 600 pps (the UI's "aggressive") against the default range cannot be
    # sustained: the scan will stall on EADDRNOTAVAIL.
    warn = kl.check_ephemeral_ports(32768, 60999, requested_rate=600)
    assert warn is not None and warn.status == "warn"
    assert "470" in warn.detail                  # the computed ceiling is shown
    assert warn.remediation                      # and it says what to change


def test_ephemeral_check_passes_when_rate_fits():
    ok = kl.check_ephemeral_ports(32768, 60999, requested_rate=200)
    assert ok is not None and ok.status == "pass"


def test_ephemeral_check_skipped_when_unreadable():
    assert kl.check_ephemeral_ports(None, None, requested_rate=600) is None


# ── conntrack: Docker bridge = NAT = one table entry per probe ───────────────

def test_conntrack_demand_is_rate_times_syn_sent_timeout():
    # An unanswered SYN holds a conntrack entry for nf_conntrack_tcp_timeout_syn_sent.
    assert kl.conntrack_demand(600) == 600 * kl.CONNTRACK_SYN_SENT_SECONDS
    assert kl.conntrack_demand(0) == 0


def test_conntrack_check_warns_when_demand_exceeds_headroom():
    # 600 pps needs ~72,000 entries; a default 65,536 table cannot hold it.
    warn = kl.check_conntrack(65536, 1000, requested_rate=600)
    assert warn is not None and warn.status == "warn"
    assert "72000" in warn.detail.replace(",", "")
    # This is the failure mode that masquerades as a firewall — say so.
    assert "filtered" in warn.remediation.lower()


def test_conntrack_check_accounts_for_entries_already_in_use():
    # Same table, but nearly full already → still a warning at a lower rate.
    warn = kl.check_conntrack(65536, 60000, requested_rate=100)
    assert warn is not None and warn.status == "warn"


def test_conntrack_check_passes_with_headroom():
    ok = kl.check_conntrack(262144, 1000, requested_rate=600)
    assert ok is not None and ok.status == "pass"


def test_conntrack_check_skipped_when_unreadable():
    # Not Linux, or no netfilter — nothing to say.
    assert kl.check_conntrack(None, None, requested_rate=600) is None


# ── neighbour table: the one that bites at exactly 1000 hosts ────────────────

def test_neighbour_check_warns_when_host_count_approaches_gc_thresh3():
    # Default gc_thresh3 is 1024; a 1000-host sweep on a flat L2 sits on the cliff.
    warn = kl.check_neighbour_table(1024, host_count=1000)
    assert warn is not None and warn.status == "warn"
    assert "1024" in warn.detail


def test_neighbour_check_warns_when_host_count_exceeds_gc_thresh3():
    warn = kl.check_neighbour_table(1024, host_count=4096)
    assert warn is not None and warn.status == "warn"


def test_neighbour_check_passes_with_room():
    ok = kl.check_neighbour_table(8192, host_count=1000)
    assert ok is not None and ok.status == "pass"


def test_neighbour_check_skipped_when_unreadable():
    assert kl.check_neighbour_table(None, host_count=1000) is None


# ── file descriptors: already guarded in the CLI, unguarded on the agent path ─

def test_fd_check_warns_when_concurrency_crowds_the_soft_limit():
    warn = kl.check_fd_headroom(1024, concurrency=900)
    assert warn is not None and warn.status == "warn"


def test_fd_check_passes_with_headroom():
    ok = kl.check_fd_headroom(1048576, concurrency=300)
    assert ok is not None and ok.status == "pass"


def test_fd_check_skipped_when_unreadable():
    assert kl.check_fd_headroom(0, concurrency=300) is None


# ── raw-socket capability decides whether wide sweeps are possible at all ────

def test_syn_capability_warns_for_a_wide_sweep_without_raw_sockets():
    # 65,535 connect() per host is not a scan strategy — surface it.
    warn = kl.check_syn_capability(False, port_count=65535)
    assert warn is not None and warn.status == "warn"
    assert "connect" in warn.detail.lower()


def test_syn_capability_quiet_for_a_narrow_sweep_without_raw_sockets():
    # A 15-port sweep over connect() is entirely normal — do not cry wolf.
    assert kl.check_syn_capability(False, port_count=15) is None


def test_syn_capability_passes_when_raw_sockets_work():
    ok = kl.check_syn_capability(True, port_count=65535)
    assert ok is not None and ok.status == "pass"


# ── assess(): compose the checks, skip what could not be read ────────────────

def _limits(**over) -> kl.KernelLimits:
    base = dict(fd_soft=1048576, fd_hard=1048576, conntrack_max=262144,
                conntrack_count=1000, ephemeral_lo=32768, ephemeral_hi=60999,
                gc_thresh3=8192, syn_capable=True)
    base.update(over)
    return kl.KernelLimits(**base)


def test_assess_returns_a_check_per_readable_limit():
    checks = kl.assess(_limits(), rate=200, concurrency=100,
                       host_count=254, port_count=1000)
    names = {c.name for c in checks}
    assert {"ephemeral", "conntrack", "neighbour", "fd", "raw_socket"} <= names
    assert all(c.status == "pass" for c in checks), kl.format_preflight(checks)


def test_assess_skips_unreadable_limits_and_notes_them_once():
    # macOS / a container without netfilter: three sysctls are simply absent.
    checks = kl.assess(
        _limits(conntrack_max=None, conntrack_count=None, gc_thresh3=None),
        rate=200, concurrency=100, host_count=254, port_count=1000)
    names = {c.name for c in checks}
    assert "conntrack" not in names and "neighbour" not in names
    # One note, not one warning per missing file.
    assert names & {"limits_unread"}
    assert len([c for c in checks if c.name == "limits_unread"]) == 1


def test_assess_never_calls_a_measured_non_event_unmeasurable():
    # A narrow sweep without raw sockets is normal, so check_syn_capability
    # stays quiet — but the capability WAS measured. Reporting it as unread
    # would misrepresent what the probe knows about itself.
    checks = kl.assess(_limits(syn_capable=False), rate=50, concurrency=20,
                       host_count=254, port_count=15)
    assert "raw_socket" not in {c.name for c in checks}
    unread = [c for c in checks if c.name == "limits_unread"]
    assert not unread, f"nothing was unreadable, got: {unread[0].detail if unread else ''}"


def test_assess_flags_the_aggressive_envelope_on_a_default_host():
    # The exact reported case: 1000 hosts, full port range, UI "aggressive".
    checks = kl.assess(
        _limits(conntrack_max=65536, gc_thresh3=1024, syn_capable=False),
        rate=600, concurrency=300, host_count=1000, port_count=65535)
    warned = {c.name for c in checks if c.status == "warn"}
    # Every limit that actually bites this envelope is named.
    assert {"ephemeral", "conntrack", "neighbour", "raw_socket"} <= warned


def test_assess_is_advisory_only_and_never_fails():
    # A1 changes no behaviour: admission control (H1/H2) owns refusals, and
    # doctor's exit code must not flip because a host is merely under-tuned.
    checks = kl.assess(
        _limits(conntrack_max=1024, gc_thresh3=128, fd_soft=64,
                ephemeral_lo=60000, ephemeral_hi=60100, syn_capable=False),
        rate=2000, concurrency=500, host_count=100000, port_count=65535)
    assert checks and all(c.status != "fail" for c in checks)


# ── one-line capability summary, logged at probe start ──────────────────────

def test_describe_capability_names_every_ceiling():
    line = kl.describe_capability(_limits())
    for token in ("fd", "ephemeral", "conntrack", "neigh", "SYN"):
        assert token in line
    # The DERIVED ceiling is the useful part, not just the raw range.
    assert "470" in line                          # ~470 connect/sec
    assert "\n" not in line                       # genuinely one line


def test_describe_capability_marks_unreadable_limits_rather_than_guessing():
    line = kl.describe_capability(
        _limits(conntrack_max=None, conntrack_count=None, gc_thresh3=None,
                ephemeral_lo=None, ephemeral_hi=None))
    assert line.count("n/a") >= 3
    assert "\n" not in line


def test_describe_capability_reports_syn_availability_both_ways():
    assert "SYN scan: yes" in kl.describe_capability(_limits(syn_capable=True))
    assert "SYN scan: no" in kl.describe_capability(_limits(syn_capable=False))


# ── IO wiring ────────────────────────────────────────────────────────────────

def test_read_int_parses_and_tolerates_absence(tmp_path):
    good = tmp_path / "good"
    good.write_text("65536\n")
    assert kl.read_int(good) == 65536

    junk = tmp_path / "junk"
    junk.write_text("not a number")
    assert kl.read_int(junk) is None

    assert kl.read_int(tmp_path / "missing") is None


def test_read_port_range_parses_the_two_column_format(tmp_path):
    f = tmp_path / "range"
    f.write_text("32768\t60999\n")
    assert kl.read_port_range(f) == (32768, 60999)

    bad = tmp_path / "bad"
    bad.write_text("32768\n")
    assert kl.read_port_range(bad) == (None, None)

    assert kl.read_port_range(tmp_path / "missing") == (None, None)


def test_probe_limits_never_raises_on_this_platform():
    # Runs on macOS dev and Linux CI alike: unreadable files become None.
    limits = kl.probe_limits()
    assert isinstance(limits, kl.KernelLimits)
    assert isinstance(limits.syn_capable, bool)


# ── the advice must fit the platform (it once told a Windows agent to grant
#    NET_RAW and run docker network_mode: host) ─────────────────────────────

def test_linux_advice_is_unchanged():
    warn = kl.check_syn_capability(False, port_count=65535, platform="linux")
    assert "NET_RAW" in warn.remediation and "CAP_NET_RAW" in warn.detail


def test_windows_advice_names_what_windows_can_do():
    warn = kl.check_syn_capability(False, port_count=65535, platform="win32")
    assert warn.status == "warn" and "connect" in warn.detail.lower()
    assert "NET_RAW" not in warn.remediation and "network_mode" not in warn.remediation
    assert "Linux agent" in warn.remediation and "connect_fast_fail" in warn.remediation


def test_macos_advice_names_the_real_limit():
    warn = kl.check_syn_capability(False, port_count=65535, platform="darwin")
    assert "NET_RAW" not in warn.remediation and "Linux agent" in warn.remediation


def test_narrow_sweeps_stay_quiet_everywhere():
    for plat in ("linux", "win32", "darwin"):
        assert kl.check_syn_capability(False, port_count=15, platform=plat) is None
