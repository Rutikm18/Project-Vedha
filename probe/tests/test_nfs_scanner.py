"""
test_nfs_scanner.py — NFS export enumeration over ONC RPC.

The live RPC path needs a real NFS server (a Samba/NFS lab check), so these cover
the parts that carry the verdict and the safety guarantees:
  * XDR / ONC-RPC wire parsing against CRAFTED bytes (MOUNT EXPORT, portmap DUMP,
    RPC reply header) — byte-exact, no network
  * the parser bounds (a malicious huge length must not read unbounded)
  * world-readable detection
  * ScanResult shaping via a monkeypatched probe
  * findings (world-readable export / portmapper exposed) + secure silence
  * scanner/ + main_scripts/ parity
"""

from __future__ import annotations

import asyncio
import struct

from scanner import nfs_scanner as nfs
from scanner import findings
from scanner.scanner_base import ScopeGuard


def _xstr(s: str) -> bytes:
    b = s.encode()
    return struct.pack(">I", len(b)) + b + b"\x00" * ((-len(b)) % 4)


def _mount_export_reply(exports):
    out = b""
    for path, clients in exports:
        out += struct.pack(">I", 1) + _xstr(path)
        for c in clients:
            out += struct.pack(">I", 1) + _xstr(c)
        out += struct.pack(">I", 0)   # end of groups
    out += struct.pack(">I", 0)       # end of exports
    return out


def _portmap_dump_reply(mappings):
    out = b""
    for prog, vers, prot, port in mappings:
        out += struct.pack(">I", 1) + struct.pack(">IIII", prog, vers, prot, port)
    out += struct.pack(">I", 0)
    return out


# ── XDR / RPC wire parsing (byte-exact, the safety-critical core) ─────────────

class TestXdrParsers:
    def test_mount_export_parse_and_world_flag(self):
        data = _mount_export_reply([
            ("/export/home", ["*"]),
            ("/secure", ["10.0.0.0/8"]),
            ("/pub", []),                       # empty groups = world-readable
        ])
        e = nfs.parse_mount_export(data)
        assert [x["path"] for x in e] == ["/export/home", "/secure", "/pub"]
        assert [x["world_readable"] for x in e] == [True, False, True]

    def test_portmap_dump_parse(self):
        data = _portmap_dump_reply([(100005, 3, 6, 20048), (100003, 3, 17, 2049)])
        p = nfs.parse_portmap_dump(data)
        assert p[0] == {"program": 100005, "version": 3, "protocol": "tcp", "port": 20048}
        assert p[1]["protocol"] == "udp" and p[1]["port"] == 2049

    def test_rpc_reply_header_stripping(self):
        result = _mount_export_reply([("/x", ["*"])])
        reply = (struct.pack(">III", nfs._XID, 1, 0)   # xid, REPLY, MSG_ACCEPTED
                 + struct.pack(">II", 0, 0)            # verf AUTH_NULL
                 + struct.pack(">I", 0)                # accept_stat SUCCESS
                 + result)
        assert nfs._parse_rpc_reply(reply) == result
        assert nfs._parse_rpc_reply(struct.pack(">III", nfs._XID, 1, 1)) is None  # MSG_DENIED

    def test_world_readable_logic(self):
        assert nfs.is_world_readable([]) is True
        assert nfs.is_world_readable(["*"]) is True
        assert nfs.is_world_readable(["everyone"]) is True
        assert nfs.is_world_readable(["10.0.0.0/8"]) is False
        assert nfs.is_world_readable(["host.corp.local"]) is False

    def test_parser_is_bounded(self):
        # export "follows", then an absurd string length — must not read unbounded.
        bad = struct.pack(">I", 1) + struct.pack(">I", 0xFFFFFFFF)
        import pytest
        with pytest.raises(ValueError):
            nfs.parse_mount_export(bad)


# ── scanner (network isolated via a patched _probe) ───────────────────────────

class TestNFSScanner:
    def _sc(self):
        return nfs.NFSScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                              rate=1e9, concurrency=2, timeout=0.1, ports=[2049])

    def test_world_readable_export_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {
            "nfs": True, "portmap_open": True, "mountd_port": 20048,
            "rpc_programs": [{"program": 100005, "version": 3, "protocol": "tcp", "port": 20048}],
            "exports": [{"path": "/home", "clients": ["*"], "world_readable": True}],
            "export_count": 1, "world_readable_exports": ["/home"]}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["world_readable_exports"] == ["/home"]

    def test_no_rpc_is_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"nfs": None, "portmap_open": False, "exports": []}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


# ── findings ──────────────────────────────────────────────────────────────────

class TestNFSFindings:
    def _fact(self, **data):
        return {"scanner": "nfs_scan", "target": "10.0.0.7", "port": 2049,
                "status": "open", "data": data}

    def test_world_readable_and_portmapper(self):
        fact = self._fact(
            nfs=True, portmap_open=True, mountd_port=20048,
            rpc_programs=[{"program": 100005}, {"program": 100003}],
            exports=[{"path": "/home", "clients": ["*"], "world_readable": True}],
            export_count=1, world_readable_exports=["/home"])
        by = {f.rule_id: f for f in findings.run_findings([fact])}
        assert by["NFS-EXPORT-WORLD-READABLE"].severity == "high"
        assert "/home" in by["NFS-EXPORT-WORLD-READABLE"].data["world_readable_exports"]
        assert by["RPC-PORTMAPPER-EXPOSED"].severity == "low" and by["RPC-PORTMAPPER-EXPOSED"].port == 111

    def test_restricted_exports_no_high_finding(self):
        fact = self._fact(nfs=True, portmap_open=False,
                          exports=[{"path": "/s", "clients": ["10.0.0.0/8"], "world_readable": False}],
                          export_count=1, world_readable_exports=[])
        assert not any(f.rule_id.startswith(("NFS-", "RPC-")) for f in findings.run_findings([fact]))


# ── parity ────────────────────────────────────────────────────────────────────

class TestParity:
    def test_main_scripts(self):
        from main_scripts.nfs_scanner import NFSScanner, parse_mount_export
        from main_scripts import findings as mf
        e = parse_mount_export(_mount_export_reply([("/x", [])]))
        assert e[0]["world_readable"] is True
        fact = {"scanner": "nfs_scan", "target": "10.0.0.7", "port": 2049, "status": "open",
                "data": {"nfs": True, "portmap_open": True, "rpc_programs": [{"program": 1}],
                         "world_readable_exports": ["/x"], "export_count": 1}}
        ids = {f.rule_id for f in mf.run_findings([fact])}
        assert {"NFS-EXPORT-WORLD-READABLE", "RPC-PORTMAPPER-EXPOSED"} <= ids
        assert NFSScanner
