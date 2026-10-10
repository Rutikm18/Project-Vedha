#!/usr/bin/env python3
"""Vedha weak-lab emulators.

DELIBERATELY WEAK. These answer just enough of a protocol for the probe scanners to
see the weakness. They exist because the real services cannot be installed natively
on Ubuntu (a camera, a phone, an IPMI BMC, a UPnP router ...). A detection from an
emulator is "fingerprint tier", not product-validated: label it that way.

Safety: no emulator proxies, stores, executes or forwards anything. UDP replies are
rate-limited per source, and the port-only UDP listener answers with 1 byte (no
amplification). Run only on an isolated lab VM behind the lab firewall chain.

    lab_emulators.py serve NAME [--bind ADDR] [--tcp 1,2] [--udp 3,4]
"""
import argparse
import asyncio
import json
import os
import socket
import struct
import sys
import time

RATE_LIMIT_PER_SEC = 20
ROOTDESC_PORT = int(os.environ.get("VEDHA_LAB_ROOTDESC_PORT", "5000"))


def local_ip_for(peer: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((peer, 9))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


# ── tiny HTTP helpers ─────────────────────────────────────────────────────────

async def read_head(reader, timeout=5.0) -> bytes:
    try:
        return await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout)
    except (asyncio.TimeoutError, asyncio.IncompleteReadError,
            asyncio.LimitOverrunError, ConnectionError, OSError):
        return b""


async def http_send(writer, status: str, body: bytes, ctype="text/html", server="lab"):
    head = (f"HTTP/1.1 {status}\r\nServer: {server}\r\nContent-Type: {ctype}\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode()
    writer.write(head + body)
    try:
        await writer.drain()
    except OSError:
        pass


def request_path(head: bytes) -> str:
    parts = head.split(b"\r\n", 1)[0].split(b" ")
    return parts[1].decode("latin-1") if len(parts) > 1 else "/"


async def _close(writer):
    try:
        writer.close()
        await writer.wait_closed()
    except OSError:
        pass


# ── TCP services ──────────────────────────────────────────────────────────────

async def rtsp(reader, writer):
    """IP-camera style RTSP: OPTIONS lists methods, DESCRIBE answers without auth."""
    head = await read_head(reader)
    if head:
        lines = head.decode("latin-1").split("\r\n")
        method = lines[0].split(" ")[0]
        cseq = next((ln.split(":", 1)[1].strip() for ln in lines
                     if ln.lower().startswith("cseq:")), "1")
        body = b""
        extra = ""
        status = "200 OK"
        if method == "OPTIONS":
            extra = "Public: OPTIONS, DESCRIBE, SETUP, PLAY, TEARDOWN\r\n"
        elif method == "DESCRIBE":
            body = (b"v=0\r\no=- 0 0 IN IP4 0.0.0.0\r\ns=Lab camera (no auth)\r\n"
                    b"t=0 0\r\nm=video 0 RTP/AVP 96\r\n")
            extra = f"Content-Type: application/sdp\r\nContent-Length: {len(body)}\r\n"
        else:
            status = "405 Method Not Allowed"
        writer.write((f"RTSP/1.0 {status}\r\nCSeq: {cseq}\r\nServer: LabCam/1.0\r\n"
                      f"{extra}\r\n").encode() + body)
        try:
            await writer.drain()
        except OSError:
            pass
    await _close(writer)


async def cwmp(reader, writer):
    """TR-069 / CWMP connection-request listener on 7547."""
    await read_head(reader)
    await http_send(writer, "200 OK",
                    b"<html><body>CWMP ACS connection-request endpoint</body></html>",
                    server="gSOAP/2.8")
    await _close(writer)


A_CNXN = 0x4E584E43


async def adb(reader, writer):
    """Android Debug Bridge over TCP, no AUTH step: answers CNXN with CNXN."""
    try:
        hdr = await asyncio.wait_for(reader.readexactly(24), 5)
        cmd, _a0, _a1, dlen, _crc, _magic = struct.unpack("<IIIIII", hdr)
        if dlen:
            await asyncio.wait_for(reader.readexactly(min(dlen, 65536)), 5)
        if cmd == A_CNXN:
            payload = (b"device::ro.product.name=labdevice;ro.product.model=LabPhone;"
                       b"ro.product.device=lab;features=shell_v2,cmd\x00")
            out = struct.pack("<IIIIII", A_CNXN, 0x01000000, 256 * 1024, len(payload),
                              sum(payload) & 0xFFFFFFFF, A_CNXN ^ 0xFFFFFFFF)
            writer.write(out + payload)
            await writer.drain()
    except (asyncio.TimeoutError, asyncio.IncompleteReadError, OSError):
        pass
    await _close(writer)


async def ollama(reader, writer):
    """Ollama-shaped API with no authentication."""
    head = await read_head(reader)
    path = request_path(head).split("?")[0]
    if path == "/":
        await http_send(writer, "200 OK", b"Ollama is running", "text/plain")
    elif path == "/api/tags":
        body = json.dumps({"models": [{"name": "llama3:8b", "model": "llama3:8b",
                                       "size": 4661224676}]}).encode()
        await http_send(writer, "200 OK", body, "application/json")
    elif path == "/api/version":
        await http_send(writer, "200 OK", json.dumps({"version": "0.3.12"}).encode(),
                        "application/json")
    else:
        await http_send(writer, "404 Not Found", b"404 page not found", "text/plain")
    await _close(writer)


ROOTDESC = b"""<?xml version="1.0"?>
<root xmlns="urn:schemas-upnp-org:device-1-0"><specVersion><major>1</major><minor>0</minor></specVersion>
<device><deviceType>urn:schemas-upnp-org:device:InternetGatewayDevice:1</deviceType>
<friendlyName>Lab Router</friendlyName><manufacturer>LabCorp</manufacturer><modelName>LabIGD</modelName>
<deviceList><device><deviceType>urn:schemas-upnp-org:device:WANDevice:1</deviceType>
<deviceList><device><deviceType>urn:schemas-upnp-org:device:WANConnectionDevice:1</deviceType>
<serviceList><service><serviceType>urn:schemas-upnp-org:service:WANIPConnection:1</serviceType>
<controlURL>/ctl/IPConn</controlURL></service></serviceList></device></deviceList></device></deviceList>
</device></root>"""


async def rootdesc(reader, writer):
    head = await read_head(reader)
    if request_path(head).split("?")[0] == "/rootDesc.xml":
        await http_send(writer, "200 OK", ROOTDESC, "text/xml", "MiniUPnPd/2.1")
    else:
        await http_send(writer, "404 Not Found", b"not found", "text/plain")
    await _close(writer)


def sip_reply(req: bytes) -> bytes:
    text = req.decode("latin-1", "replace")
    first = text.split("\r\n", 1)[0]
    hdrs: dict = {}
    for line in text.split("\r\n")[1:]:
        if ":" in line:
            k, _, v = line.partition(":")
            hdrs.setdefault(k.strip().lower(), []).append(v.strip())

    def g(k):
        return hdrs.get(k, [""])[0]

    status = "200 OK" if first.startswith("OPTIONS") else "405 Method Not Allowed"
    lines = [f"SIP/2.0 {status}"]
    lines += ["Via: " + v for v in hdrs.get("via", [])]
    lines += ["From: " + g("from"), "To: " + g("to") + ";tag=lab1",
              "Call-ID: " + g("call-id"), "CSeq: " + g("cseq"),
              "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER",
              "Server: Asterisk PBX 16.2.1", "Content-Length: 0", "", ""]
    return "\r\n".join(lines).encode()


async def sip_tcp(reader, writer):
    head = await read_head(reader)
    if head:
        writer.write(sip_reply(head))
        try:
            await writer.drain()
        except OSError:
            pass
    await _close(writer)


async def hold(reader, writer):
    """Port-only listener: accept, say nothing, drop after a second."""
    try:
        await asyncio.wait_for(reader.read(64), 1.0)
    except (asyncio.TimeoutError, OSError):
        pass
    await _close(writer)


# ── UDP services: handler(data, addr) -> list[bytes] ──────────────────────────

def udp_ssdp(data, addr):
    if b"M-SEARCH" not in data:
        return []
    loc = f"http://{local_ip_for(addr[0])}:{ROOTDESC_PORT}/rootDesc.xml"
    return [("HTTP/1.1 200 OK\r\nCACHE-CONTROL: max-age=1800\r\n"
             f"LOCATION: {loc}\r\nSERVER: Linux/5.15 UPnP/1.1 MiniUPnPd/2.1\r\n"
             "ST: upnp:rootdevice\r\nUSN: uuid:lab-igd::upnp:rootdevice\r\n\r\n").encode()]


def udp_ntp(data, addr):
    """Mode 3 -> normal server reply. Mode 7 MON_GETLIST(_1) -> a large monlist."""
    if not data:
        return []
    mode = data[0] & 7
    if mode == 3:
        return [b"\x1c\x02\x00\xec" + b"\x00" * 44]
    if mode == 7 and len(data) >= 4 and data[3] in (20, 42):
        n = 6
        out = []
        for i in range(n):
            b0 = 0x97 | (0x40 if i < n - 1 else 0)      # R=1, M=more, VN=2, mode 7
            hdr = bytes([b0, i, 3, data[3]]) + struct.pack(">HH", 6, 72)
            out.append(hdr + b"\x00" * (6 * 72))
        return out
    return []


def udp_sip(data, addr):
    return [sip_reply(data)] if data.startswith(b"OPTIONS") else []


def udp_ipmi(data, addr):
    """ASF presence ping -> pong; RMCP+ Open Session with cipher 0 -> status 0 (accepted)."""
    if len(data) >= 12 and data[0] == 0x06 and data[3] == 0x06:     # ASF class
        return [bytes([6, 0, 0xFF, 6, 0, 0, 0x11, 0xBE, 0x40, data[9], 0, 0x10,
                       0, 0, 0x11, 0xBE, 0, 0, 0, 0, 0x81, 0, 0, 0, 0, 0, 0, 0])]
    if len(data) >= 24 and data[0] == 0x06 and data[3] == 0x07 and data[5] == 0x10:
        tag, console_sid = data[16], data[20:24]
        payload = (bytes([tag, 0x00, 0x04, 0x00]) + console_sid + b"\x01\x02\x03\x04"
                   + bytes([0, 0, 0, 8, 0, 0, 0, 0])
                   + bytes([1, 0, 0, 8, 0, 0, 0, 0])
                   + bytes([2, 0, 0, 8, 0, 0, 0, 0]))
        return [bytes([6, 0, 0xFF, 7, 6, 0x11]) + b"\x00" * 8
                + struct.pack("<H", len(payload)) + payload]
    return []


def udp_echo1(data, addr):
    return [b"\x00"]


class UdpProto(asyncio.DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler
        self.hits: dict = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        now = int(time.time())
        sec, count = self.hits.get(addr[0], (now, 0))
        count = count + 1 if sec == now else 1
        self.hits[addr[0]] = (now, count)
        if count > RATE_LIMIT_PER_SEC:
            return
        try:
            for pkt in self.handler(data, addr):
                self.transport.sendto(pkt, addr)
        except Exception as exc:                                  # never crash the lab
            print(f"udp handler error: {exc}", file=sys.stderr)


# name -> (tcp ports, udp ports, tcp handler, udp handler, extra tcp {port: handler})
SERVICES = {
    "rtsp":   ([554, 8554], [], rtsp, None, {}),
    "cwmp":   ([7547], [], cwmp, None, {}),
    "adb":    ([5555], [], adb, None, {}),
    "ollama": ([11434], [], ollama, None, {}),
    "ssdp":   ([], [1900], None, udp_ssdp, {ROOTDESC_PORT: rootdesc}),
    "ntp":    ([], [123], None, udp_ntp, {}),
    "sip":    ([5060], [5060], sip_tcp, udp_sip, {}),
    "ipmi":   ([], [623], None, udp_ipmi, {}),
    "listen": ([], [], hold, udp_echo1, {}),
}


async def run(name, bind, tcp_ports, udp_ports):
    _tcp, _udp, tcp_h, udp_h, extra = SERVICES[name]
    loop = asyncio.get_running_loop()
    started = []
    for p in tcp_ports:
        await asyncio.start_server(tcp_h, bind, p)
        started.append(f"tcp/{p}")
    for p, h in extra.items():
        await asyncio.start_server(h, bind, p)
        started.append(f"tcp/{p}")
    for p in udp_ports:
        await loop.create_datagram_endpoint(lambda: UdpProto(udp_h), local_addr=(bind, p))
        started.append(f"udp/{p}")
    print(f"vedha-lab emulator '{name}' listening on {bind}: {', '.join(started)}", flush=True)
    await asyncio.Event().wait()


def parse_ports(text):
    return [int(x) for x in text.split(",") if x.strip()] if text else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sv = sub.add_parser("serve")
    sv.add_argument("name", choices=sorted(SERVICES))
    sv.add_argument("--bind", default="0.0.0.0")
    sv.add_argument("--tcp", default=None, help="comma list; overrides the default")
    sv.add_argument("--udp", default=None, help="comma list; overrides the default")
    a = ap.parse_args()
    d_tcp, d_udp = SERVICES[a.name][0], SERVICES[a.name][1]
    tcp = parse_ports(a.tcp) if a.tcp is not None else d_tcp
    udp = parse_ports(a.udp) if a.udp is not None else d_udp
    if a.name == "listen" and not (tcp or udp):
        ap.error("'listen' needs --tcp and/or --udp")
    try:
        asyncio.run(run(a.name, a.bind, tcp, udp))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
