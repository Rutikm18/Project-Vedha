"""Pure-logic tests for the ARP/MAC/mobile-detection helpers in
host_discovery. No network, fully deterministic."""

from scanner.host_discovery import (
    normalize_mac, is_locally_administered, vendor_for_mac, device_hint,
)


class TestNormalizeMac:
    def test_zero_pads_octets(self):
        # macOS `arp -a` strips leading zeros; we must restore them.
        assert normalize_mac("d2:58:2b:ff:cb:4") == "d2:58:2b:ff:cb:04"

    def test_lowercases(self):
        assert normalize_mac("34:F3:9A:A1:A9:8C") == "34:f3:9a:a1:a9:8c"

    def test_extracts_from_arp_line(self):
        line = "? (192.168.1.68) at 34:f3:9a:a1:a9:8c on en0 ifscope [ethernet]"
        assert normalize_mac(line) == "34:f3:9a:a1:a9:8c"

    def test_rejects_broadcast(self):
        assert normalize_mac("ff:ff:ff:ff:ff:ff") is None

    def test_rejects_multicast(self):
        assert normalize_mac("01:00:5e:00:00:fb") is None

    def test_rejects_garbage(self):
        assert normalize_mac("not-a-mac") is None
        assert normalize_mac("") is None


class TestLocallyAdministered:
    def test_randomized_phone_macs(self):
        # 2nd-LSB of first octet set -> randomized (0x2,0x6,0xa,0xe nibble).
        for mac in ("96:f5:cb:90:09:52", "42:76:60:6d:e8:ac",
                    "d2:58:2b:ff:cb:04", "6e:bc:2b:81:3f:e8"):
            assert is_locally_administered(mac), mac

    def test_globally_unique_macs(self):
        for mac in ("34:f3:9a:a1:a9:8c", "5c:8c:30:fd:d5:90", "b8:27:eb:00:00:01"):
            assert not is_locally_administered(mac), mac


class TestVendorLookup:
    def test_known_oui(self):
        assert vendor_for_mac("b8:27:eb:00:00:01") == "Raspberry Pi"

    def test_unknown_oui(self):
        assert vendor_for_mac("de:ad:be:ef:00:01") is None


class TestDeviceHint:
    def test_iphone_lockdownd_port(self):
        assert "apple-mobile" in device_hint("34:f3:9a:a1:a9:8c", None, {62078})

    def test_randomized_mac_is_mobile(self):
        assert "randomized" in device_hint("96:f5:cb:90:09:52", None, set())

    def test_mobile_vendor(self):
        assert device_hint("b8:27:eb:00:00:01", "Samsung", set()) == "mobile (Samsung)"

    def test_plain_vendor_passthrough(self):
        assert device_hint("b8:27:eb:00:00:01", "Raspberry Pi", set()) == "Raspberry Pi"

    def test_no_signal(self):
        assert device_hint(None, None, set()) is None


class TestWindowsMac:
    """Windows `arp -a` prints MACs with dashes; device inventory was blank on
    Windows because the parser only accepted colons."""

    def test_normalize_dash_separated_mac(self):
        assert normalize_mac("aa-bb-cc-dd-ee-ff") == "aa:bb:cc:dd:ee:ff"

    def test_normalize_dash_mac_zero_pads_and_lowers(self):
        assert normalize_mac("A-F3-9A-A1-A9-8C") == "0a:f3:9a:a1:a9:8c"

    def test_parse_windows_arp_line(self):
        from scanner.host_discovery import parse_neighbor_line
        line = "  192.168.1.1           aa-bb-cc-dd-ee-ff     dynamic"
        nb = parse_neighbor_line(line, want_ip="192.168.1.1")
        assert nb is not None and nb.mac == "aa:bb:cc:dd:ee:ff"

    def test_windows_interface_header_is_not_a_mac(self):
        from scanner.host_discovery import parse_neighbor_line
        assert parse_neighbor_line("Interface: 192.168.1.5 --- 0x4") is None

    def test_vendor_still_resolves_for_a_dash_mac(self):
        # normalize first, then the OUI lookup works the same as colon form.
        mac = normalize_mac("34-F3-9A-A1-A9-8C")
        assert mac == "34:f3:9a:a1:a9:8c"
        assert vendor_for_mac(mac) == vendor_for_mac("34:f3:9a:a1:a9:8c")
