"""
test_ipv6_discovery.py — FIX 3: IPv6 neighbor discovery (RFC 4861 ND multicast).

Pure parsers (fixture output from `ndp -an` / `ip -6 neigh`) + the discover()
filtering (state gating, own-address exclusion, link-local scope preservation).
No network — the ping + cache-read are monkeypatched.
"""
from __future__ import annotations

import main_scripts.ipv6_discovery as d


class TestParsers:
    def test_parse_ndp_macos(self):
        text = ("Neighbor                     Linklayer Address  Netif Expire   St\n"
                "fe80::1%en0                  aa:bb:cc:dd:ee:ff   en0 permanent R\n"
                "2001:db8::5%en0              22:33:44:55:66:77   en0 5s        S\n"
                "fe80::dead%en0               (incomplete)        en0 expired   I\n")
        got = d.parse_ndp(text)
        assert ("fe80::1%en0", "REACHABLE") in got
        assert ("2001:db8::5%en0", "STALE") in got
        assert ("fe80::dead%en0", "INCOMPLETE") in got

    def test_parse_ip_neigh_linux(self):
        text = ("fe80::1 dev eth0 lladdr aa:bb:cc:dd:ee:ff router REACHABLE\n"
                "2001:db8::5 dev eth0 lladdr 22:33:44:55:66:77 STALE\n"
                "fe80::9 dev eth0  FAILED\n")
        got = d.parse_ip_neigh6(text)
        assert ("fe80::1", "REACHABLE") in got
        assert ("2001:db8::5", "STALE") in got
        assert ("fe80::9", "FAILED") in got

    def test_ignores_non_ipv6_lines(self):
        assert d.parse_ip_neigh6("192.168.1.1 dev eth0 REACHABLE\n") == []
        assert d.parse_ndp("Neighbor  Linklayer\n") == []


class TestDiscoverFiltering:
    def _patch(self, monkeypatch, cache, own=None):
        monkeypatch.setattr(d, "_ping_all_nodes", lambda *a, **k: None)
        monkeypatch.setattr(d, "_read_neighbor_cache", lambda: cache)
        monkeypatch.setattr(d, "_own_ipv6_addresses", lambda: set(own or []))

    def test_keeps_usable_drops_dead_states(self, monkeypatch):
        self._patch(monkeypatch, [
            ("fe80::1%en0", "REACHABLE"),
            ("2001:db8::5", "STALE"),
            ("fe80::dead%en0", "INCOMPLETE"),
            ("fe80::bad%en0", "FAILED"),
        ])
        hosts = d.discover_ipv6_hosts("en0")
        assert "fe80::1%en0" in hosts               # link-local keeps its %scope
        assert "2001:db8::5" in hosts               # global, no scope
        assert not any("dead" in h or "bad" in h for h in hosts)

    def test_excludes_own_addresses(self, monkeypatch):
        self._patch(monkeypatch,
                    [("fe80::1%en0", "REACHABLE"), ("fe80::aaaa%en0", "REACHABLE")],
                    own={"fe80::aaaa"})
        hosts = d.discover_ipv6_hosts("en0")
        assert "fe80::1%en0" in hosts
        assert not any("aaaa" in h for h in hosts)

    def test_dedups(self, monkeypatch):
        self._patch(monkeypatch,
                    [("fe80::1%en0", "REACHABLE"), ("fe80::1%en0", "STALE")])
        assert d.discover_ipv6_hosts("en0").count("fe80::1%en0") == 1

    def test_link_local_can_be_excluded(self, monkeypatch):
        self._patch(monkeypatch,
                    [("fe80::1%en0", "REACHABLE"), ("2001:db8::5", "REACHABLE")])
        hosts = d.discover_ipv6_hosts("en0", include_link_local=False)
        assert hosts == ["2001:db8::5"]             # only the global survives

    def test_never_raises_on_empty(self, monkeypatch):
        self._patch(monkeypatch, [])
        assert d.discover_ipv6_hosts("en0") == []
