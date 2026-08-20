"""
iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.

Covers playbook 09 (IoT/Embedded Survey) using pure-Python protocol probes:

  SSDP/UPnP (UDP 1900)  — unicast M-SEARCH + HTTP GET of rootDesc.xml
  mDNS/DNS-SD (UDP 5353) — PTR/ANY query for _services._dns-sd._udp.local
  RTSP  (TCP 554, 8554)  — OPTIONS probe; Public header reveals supported methods
  MQTT  (TCP 1883, 8883) — CONNECT; CONNACK return code 0 = unauthenticated access
  CoAP  (UDP 5683)       — GET /.well-known/core; resource listing
  TR-069 (TCP 7547)      — HTTP banner grab; CPE management protocol exposure

COLLECTION METHOD: we only READ or initiate connection-stage messages.
We do NOT authenticate, send commands that alter state, subscribe to data,
or execute any MQTT/CoAP operations beyond what is needed to confirm
unauthenticated access.  An MQTT SUBSCRIBE '#' is performed solely to verify
that no authentication is required (the broker's return code proves it).
"""

from __future__ import annotations

import asyncio
import re
import socket
import struct
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    resolve, setup_logging, base_argparser, main_entrypoint, LOG,
    user_agent,
)

# ── SSDP / UPnP ──────────────────────────────────────────────────────────────

_SSDP_MSEARCH = (
    b"M-SEARCH * HTTP/1.1\r\n"
    b"HOST: 239.255.255.250:1900\r\n"
    b'MAN: "ssdp:discover"\r\n'
    b"MX: 3\r\n"
    b"ST: ssdp:all\r\n"
    b"\r\n"
)
_SSDP_PORT = 1900


def _parse_ssdp_headers(data: bytes) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in data.decode("latin-1", "replace").split("\r\n")[1:]:
        if ":" in line:
            k, _, v = line.partition(":")
            headers[k.strip().lower()] = v.strip()
    return headers


def _fetch_upnp_root_desc(location: str, timeout: float) -> dict:
    """HTTP GET the UPnP rootDesc.xml and extract device info."""
    try:
        req = urllib.request.Request(location, headers={"User-Agent": user_agent()})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_body = resp.read(65536)
    except (urllib.error.URLError, OSError, Exception):
        return {}
    try:
        root = ET.fromstring(xml_body)
        ns = {"upnp": "urn:schemas-upnp-org:device-1-0"}
        device = root.find(".//upnp:device", ns) or root.find(".//{*}device")
        if device is None:
            return {"raw_xml_bytes": len(xml_body)}
        def _text(tag: str) -> str:
            el = device.find(f"{{urn:schemas-upnp-org:device-1-0}}{tag}") or \
                 device.find(f"{{*}}{tag}")
            return el.text.strip() if el is not None and el.text else ""
        return {
            "device_type":        _text("deviceType"),
            "friendly_name":      _text("friendlyName"),
            "manufacturer":       _text("manufacturer"),
            "model_name":         _text("modelName"),
            "model_number":       _text("modelNumber"),
            "firmware_version":   _text("modelDescription"),
            "serial_number":      _text("serialNumber"),
            "udn":                _text("UDN"),
        }
    except ET.ParseError:
        return {"raw_xml_bytes": len(xml_body)}


def _probe_ssdp_sync(target: str, port: int, timeout: float) -> dict | None:
    try:
        family, sockaddr = resolve(target, port, proto="udp")
    except OSError:
        return None
    sock = socket.socket(family, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(_SSDP_MSEARCH, sockaddr)
        data, _ = sock.recvfrom(4096)
    except (socket.timeout, OSError):
        return None
    finally:
        sock.close()

    headers = _parse_ssdp_headers(data)
    result: dict = {
        "location": headers.get("location", ""),
        "server": headers.get("server", ""),
        "st": headers.get("st", ""),
        "usn": headers.get("usn", ""),
    }
    # Follow Location to rootDesc.xml
    location = result["location"]
    if location.startswith("http"):
        result["upnp_device"] = _fetch_upnp_root_desc(location, timeout)
    return result


# ── mDNS / DNS-SD ─────────────────────────────────────────────────────────────

_MDNS_PORT = 5353
# PTR query for _services._dns-sd._udp.local (QU=1 in class field)
_MDNS_SERVICES_QUERY = (
    b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    b"\x09_services\x07_dns-sd\x04_udp\x05local\x00"
    b"\x00\x0c\x80\x01"
)


def _decode_mdns_name(data: bytes, offset: int) -> tuple[str, int]:
    """Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)."""
    labels, seen = [], set()
    while offset < len(data):
        length = data[offset]
        if (length & 0xC0) == 0xC0:   # pointer
            if offset + 1 >= len(data):
                break
            ptr = ((length & 0x3F) << 8) | data[offset + 1]
            if ptr in seen:
                break
            seen.add(ptr)
            name_rest, _ = _decode_mdns_name(data, ptr)
            labels.append(name_rest)
            offset += 2
            return ".".join(labels), offset
        elif length == 0:
            offset += 1
            break
        else:
            offset += 1
            labels.append(data[offset:offset + length].decode("utf-8", "replace"))
            offset += length
    return ".".join(labels), offset


def _parse_mdns_response(data: bytes) -> list[str]:
    """Extract PTR target names from mDNS response (services discovered)."""
    if len(data) < 12:
        return []
    ancount = struct.unpack(">H", data[6:8])[0]
    if ancount == 0:
        return []
    offset = 12
    # Skip question section
    qcount = struct.unpack(">H", data[4:6])[0]
    for _ in range(qcount):
        try:
            _, offset = _decode_mdns_name(data, offset)
            offset += 4  # qtype + qclass
        except Exception:
            return []
    # Parse answer section
    services: list[str] = []
    for _ in range(ancount):
        try:
            _, offset = _decode_mdns_name(data, offset)
            if offset + 10 > len(data):
                break
            rtype, _, _, rdlen = struct.unpack(">HHIH", data[offset:offset + 10])
            offset += 10
            if rtype == 12 and offset + rdlen <= len(data):  # PTR
                target, _ = _decode_mdns_name(data, offset)
                services.append(target)
            offset += rdlen
        except Exception:
            break
    return services


def _probe_mdns_sync(target: str, port: int, timeout: float) -> dict | None:
    try:
        family, sockaddr = resolve(target, port, proto="udp")
    except OSError:
        return None
    sock = socket.socket(family, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(_MDNS_SERVICES_QUERY, sockaddr)
        data, _ = sock.recvfrom(4096)
    except (socket.timeout, OSError):
        return None
    finally:
        sock.close()

    services = _parse_mdns_response(data)
    return {"services": services, "replied": True, "reply_bytes": len(data)}


# ── RTSP ──────────────────────────────────────────────────────────────────────

_RTSP_OPTIONS = (b"OPTIONS * RTSP/1.0\r\nCSeq: 1\r\nUser-Agent: "
                 + user_agent().encode() + b"\r\n\r\n")
_RTSP_PORTS = [554, 8554]


async def _probe_rtsp(target: str, port: int, timeout: float) -> dict | None:
    try:
        fut = asyncio.open_connection(target, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None
    try:
        writer.write(_RTSP_OPTIONS)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(2048), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        return None
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    text = data.decode("latin-1", "replace")
    if not text.startswith("RTSP/"):
        return None
    public_methods = ""
    server = ""
    for line in text.split("\r\n"):
        ll = line.lower()
        if ll.startswith("public:"):
            public_methods = line.split(":", 1)[1].strip()
        elif ll.startswith("server:"):
            server = line.split(":", 1)[1].strip()
    return {
        "rtsp_version": text.split(" ")[0],
        "status": text.split(" ")[1] if len(text.split(" ")) > 1 else "",
        "public_methods": public_methods,
        "server": server,
    }


# ── MQTT ──────────────────────────────────────────────────────────────────────

_MQTT_PORTS = [1883, 8883]

# MQTT CONNECT packet (v3.1.1, no auth, no will, keepalive=60, clean-session=1)
def _mqtt_connect() -> bytes:
    client_id = b"mqtt-client"          # neutral MQTT client id (no tool signature)
    payload = (struct.pack("!H", len(client_id)) + client_id)
    # Connect flags: clean-session=1 (0x02)
    var_header = (b"\x00\x04MQTT"  # protocol name
                  b"\x04"          # protocol level 3.1.1
                  b"\x02"          # connect flags: clean-session
                  b"\x00\x3c")     # keep-alive = 60 s
    remaining = len(var_header) + len(payload)
    return b"\x10" + _mqtt_remaining_len(remaining) + var_header + payload


def _mqtt_remaining_len(n: int) -> bytes:
    """MQTT variable-length encoding."""
    result = bytearray()
    while True:
        b = n % 128
        n //= 128
        result.append(b | (0x80 if n > 0 else 0))
        if n == 0:
            break
    return bytes(result)


def _mqtt_subscribe_all() -> bytes:
    """MQTT SUBSCRIBE to '#' (all topics), QoS 0."""
    topic = b"#"
    payload = struct.pack("!H", 1) + struct.pack("!H", len(topic)) + topic + b"\x00"
    remaining = len(payload)
    return b"\x82" + _mqtt_remaining_len(remaining) + payload


async def _probe_mqtt(target: str, port: int, timeout: float) -> dict | None:
    try:
        fut = asyncio.open_connection(target, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None
    try:
        writer.write(_mqtt_connect())
        await writer.drain()
        data = await asyncio.wait_for(reader.read(4), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        writer.close()
        return None

    if len(data) < 4 or data[0] != 0x20:  # CONNACK type
        writer.close()
        return None

    return_code = data[3]
    result: dict = {
        "mqtt_connack": True,
        "return_code": return_code,
        "unauthenticated_access": return_code == 0,
        "return_code_meaning": {
            0: "Connection Accepted",
            1: "Refused: Unacceptable protocol version",
            2: "Refused: Identifier rejected",
            3: "Refused: Server unavailable",
            4: "Refused: Bad username or password",
            5: "Refused: Not authorized",
        }.get(return_code, f"Unknown ({return_code})"),
    }

    if return_code == 0:
        # Broker accepted without auth — try SUBSCRIBE # to confirm full access
        try:
            writer.write(_mqtt_subscribe_all())
            await writer.drain()
            sub_data = await asyncio.wait_for(reader.read(5), timeout=timeout)
            # SUBACK: 0x90, remaining=3, pkt_id(2), return_code(1)
            if len(sub_data) >= 5 and sub_data[0] == 0x90:
                result["subscribe_all_granted"] = sub_data[4] != 0x80
        except Exception:
            pass

    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass
    return result


# ── CoAP ─────────────────────────────────────────────────────────────────────

_COAP_PORT = 5683

def _coap_get_wellknown_core() -> bytes:
    """CoAP Confirmable GET for /.well-known/core — resource discovery."""
    # Fixed header: Ver=1, T=CON(0), TKL=0, Code=GET(0.01)
    # Uri-Path option: delta=11, ".well-known" (len=11), then delta=0, "core" (len=4)
    msg_id = 0xAB01
    hdr = struct.pack("!BBH", 0x40, 0x01, msg_id)
    # Uri-Path option num=11: first seg ".well-known" (11 bytes), delta=11, len=11
    opt1 = bytes([(11 << 4) | 11]) + b".well-known"
    # Uri-Path option num=11: second seg "core" (4 bytes), delta=0, len=4
    opt2 = bytes([(0 << 4) | 4]) + b"core"
    return hdr + opt1 + opt2


def _parse_coap_response(data: bytes) -> dict:
    """Extract CoAP response code and content."""
    if len(data) < 4:
        return {}
    ver_t_tkl = data[0]
    code = data[1]
    code_class = code >> 5
    code_detail = code & 0x1F
    code_str = f"{code_class}.{code_detail:02d}"
    # Try to extract payload (after 0xFF marker or from fixed offset)
    payload = b""
    if b"\xff" in data[4:]:
        payload = data[data.index(b"\xff", 4) + 1:]
    elif len(data) > 4:
        payload = data[4:]
    content = payload.decode("utf-8", "replace") if payload else ""
    return {
        "coap_response_code": code_str,
        "core_resources": content[:2048],
    }


def _probe_coap_sync(target: str, port: int, timeout: float) -> dict | None:
    try:
        family, sockaddr = resolve(target, port, proto="udp")
    except OSError:
        return None
    sock = socket.socket(family, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        pkt = _coap_get_wellknown_core()
        sock.sendto(pkt, sockaddr)
        data, _ = sock.recvfrom(8192)
    except (socket.timeout, OSError):
        return None
    finally:
        sock.close()
    return _parse_coap_response(data)


# ── TR-069 / CWMP ─────────────────────────────────────────────────────────────

_CWMP_PORTS = [7547, 7548]

async def _probe_cwmp(target: str, port: int, timeout: float) -> dict | None:
    """HTTP GET to CWMP port — detect ACS or CPE management interface."""
    try:
        fut = asyncio.open_connection(target, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None
    try:
        req = (f"GET / HTTP/1.1\r\nHost: {target}:{port}\r\n"
               f"User-Agent: {user_agent()}\r\nConnection: close\r\n\r\n")
        writer.write(req.encode())
        await writer.drain()
        data = await asyncio.wait_for(reader.read(2048), timeout=timeout)
    except (asyncio.TimeoutError, OSError):
        writer.close()
        return None
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    text = data.decode("latin-1", "replace")
    first_line = text.split("\r\n")[0] if text else ""
    server = ""
    cwmp_detected = "cwmp" in text.lower() or "acs" in text.lower()
    for line in text.split("\r\n"):
        ll = line.lower()
        if ll.startswith("server:"):
            server = line.split(":", 1)[1].strip()
    return {
        "http_response": first_line,
        "server": server,
        "cwmp_indicators": cwmp_detected,
    }


# ── Main scanner class ────────────────────────────────────────────────────────

class IoTScanner(BaseScanner):
    """
    Surveys a target for IoT/embedded device exposure across 6 protocol families.
    Each probe is independent; all are read-only.
    """
    name = "iot_scan"

    async def scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()
        results: list[ScanResult] = []

        async def _add(coro, port: int, proto: str, label: str):
            await self.limiter.wait()
            async with self.sem:
                try:
                    data = await coro
                except Exception as exc:
                    results.append(ScanResult(
                        self.name, target, port=port, proto=proto,
                        status="error", error=str(exc)))
                    return
            if data:
                results.append(ScanResult(
                    self.name, target, port=port, proto=proto,
                    status="open", data=data,
                    evidence=f"{label}: {self._short_evidence(data)}"))

        def _short_evidence(d: dict) -> str:
            for k in ("friendly_name", "server", "rtsp_version", "return_code_meaning",
                      "coap_response_code", "http_response", "services"):
                if k in d:
                    v = d[k]
                    return str(v)[:80] if not isinstance(v, list) else f"{len(v)} service(s)"
            return str(list(d.keys())[:3])

        self._short_evidence = _short_evidence

        # SSDP
        await self.limiter.wait()
        async with self.sem:
            ssdp = await loop.run_in_executor(
                None, _probe_ssdp_sync, target, _SSDP_PORT, self.timeout)
        if ssdp:
            results.append(ScanResult(
                self.name, target, port=_SSDP_PORT, proto="udp",
                status="open", data=ssdp,
                evidence=f"SSDP: {ssdp.get('server') or ssdp.get('st') or 'device found'}"))

        # mDNS
        await self.limiter.wait()
        async with self.sem:
            mdns = await loop.run_in_executor(
                None, _probe_mdns_sync, target, _MDNS_PORT, self.timeout)
        if mdns:
            svc_str = ", ".join(mdns["services"][:5]) if mdns["services"] else "no PTR records"
            results.append(ScanResult(
                self.name, target, port=_MDNS_PORT, proto="udp",
                status="open", data=mdns,
                evidence=f"mDNS services: {svc_str}"))

        # CoAP
        await self.limiter.wait()
        async with self.sem:
            coap = await loop.run_in_executor(
                None, _probe_coap_sync, target, _COAP_PORT, self.timeout)
        if coap:
            results.append(ScanResult(
                self.name, target, port=_COAP_PORT, proto="udp",
                status="open", data=coap,
                evidence=f"CoAP {coap.get('coap_response_code', '?')}: "
                         f"{coap.get('core_resources','')[:80]}"))

        # RTSP (try each port)
        for rport in _RTSP_PORTS:
            await self.limiter.wait()
            async with self.sem:
                rtsp = await _probe_rtsp(target, rport, self.timeout)
            if rtsp:
                results.append(ScanResult(
                    self.name, target, port=rport, proto="tcp",
                    status="open", data=rtsp,
                    evidence=f"RTSP methods: {rtsp.get('public_methods','?')}"))
                break  # stop at first successful RTSP port

        # MQTT (try each port)
        for mport in _MQTT_PORTS:
            await self.limiter.wait()
            async with self.sem:
                mqtt = await _probe_mqtt(target, mport, self.timeout)
            if mqtt:
                status = "open"
                evidence = (f"MQTT CONNACK: {mqtt.get('return_code_meaning', '?')}"
                            + (" — UNAUTHENTICATED" if mqtt.get("unauthenticated_access") else ""))
                results.append(ScanResult(
                    self.name, target, port=mport, proto="tcp",
                    status=status, data=mqtt, evidence=evidence))
                break

        # TR-069/CWMP
        for cport in _CWMP_PORTS:
            await self.limiter.wait()
            async with self.sem:
                cwmp = await _probe_cwmp(target, cport, self.timeout)
            if cwmp:
                results.append(ScanResult(
                    self.name, target, port=cport, proto="tcp",
                    status="open", data=cwmp,
                    evidence=f"CWMP/TR-069: {cwmp.get('http_response','?')} "
                             f"server={cwmp.get('server','?')}"))
                break

        return results


def main() -> None:
    parser = base_argparser("IoT/embedded device survey (SSDP/mDNS/RTSP/MQTT/CoAP/CWMP)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = IoTScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
