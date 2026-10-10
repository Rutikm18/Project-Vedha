#!/usr/bin/env python3
"""Independent verifier for the Vedha weak lab.

Deliberately does NOT use the Vedha probe scanners: the point is to prove the weakness
exists *before* Vedha is pointed at it, so a pass here is not circular.

    lab_probe.py up tcp|udp HOST PORT
    lab_probe.py check NAME HOST [PORT]

Exit codes:  0 weakness CONFIRMED   1 service reachable, weakness ABSENT
             2 service UNREACHABLE or a required tool is missing
The single line on stdout is the human-readable evidence / reason.
"""
import http.client
import io
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import urllib.request

CONF_DIR = os.environ.get("VEDHA_LAB_CONF_DIR", "/etc/vedha-lab")
CONFIRMED, ABSENT, UNREACHABLE = 0, 1, 2


class Unreachable(Exception):
    pass


def tcp(host, port, timeout=6.0):
    try:
        s = socket.create_connection((host, port), timeout)
        s.settimeout(timeout)
        return s
    except OSError as exc:
        raise Unreachable(f"{host}:{port}/tcp {exc}")


def recv_n(s, n):
    buf = b""
    while len(buf) < n:
        chunk = s.recv(n - len(buf))
        if not chunk:
            raise Unreachable("connection closed early")
        buf += chunk
    return buf


def udp_exchange(host, port, payload, timeout=4.0, extra_wait=0.0):
    """Send one datagram, return the list of reply datagrams."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    out = []
    try:
        s.sendto(payload, (host, port))
        out.append(s.recvfrom(65535)[0])
        if extra_wait:
            s.settimeout(extra_wait)
            while True:
                out.append(s.recvfrom(65535)[0])
    except socket.timeout:
        pass
    except OSError as exc:
        raise Unreachable(f"{host}:{port}/udp {exc}")
    finally:
        s.close()
    if not out:
        raise Unreachable(f"{host}:{port}/udp no reply")
    return out


def need(tool):
    if not shutil.which(tool):
        raise Unreachable(f"verifier tool '{tool}' is not installed")


def run(cmd, timeout=20):
    need(cmd[0])
    p = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return (p.stdout + p.stderr).decode("utf-8", "replace")


# ── SSH ───────────────────────────────────────────────────────────────────────

def ssh_kexinit(host, port):
    s = tcp(host, port)
    banner = b""
    while not banner.endswith(b"\n") and len(banner) < 512:
        c = s.recv(1)
        if not c:
            break
        banner += c
    s.sendall(b"SSH-2.0-LabProbe_1.0\r\n")
    plen = struct.unpack(">I", recv_n(s, 4))[0]
    body = recv_n(s, plen)
    payload = body[1:plen - body[0]]
    if not payload or payload[0] != 20:
        raise Unreachable("no SSH_MSG_KEXINIT")
    off, lists = 17, []
    for _ in range(10):
        ln = struct.unpack(">I", payload[off:off + 4])[0]
        off += 4
        lists.append(payload[off:off + ln].decode().split(",") if ln else [])
        off += ln
    s.close()
    return banner.decode("latin-1").strip(), lists


WEAK_KEX = {"diffie-hellman-group1-sha1", "diffie-hellman-group14-sha1",
            "diffie-hellman-group-exchange-sha1"}


def c_ssh_weak(host, port):
    banner, lists = ssh_kexinit(host, port)
    kex, ciphers = lists[0], lists[2]
    wk = sorted(WEAK_KEX & set(kex))
    wc = [c for c in ciphers if any(t in c for t in ("cbc", "arcfour", "3des"))]
    if wk or wc:
        return CONFIRMED, f"{banner}: weak kex={wk} weak ciphers={wc}"
    return ABSENT, f"{banner}: no SHA-1 kex or CBC/3DES/RC4 cipher offered"


def c_ssh_terrapin(host, port):
    banner, lists = ssh_kexinit(host, port)
    kex, ciphers = lists[0], lists[2]
    strict = "kex-strict-s-v00@openssh.com" in kex
    risky = [c for c in ciphers if "chacha20" in c or "cbc" in c]
    if not strict and risky:
        return CONFIRMED, f"{banner}: no strict-kex marker, offers {risky[:2]}"
    return ABSENT, f"{banner}: strict-kex={strict} risky ciphers={bool(risky)}"


# ── VNC ───────────────────────────────────────────────────────────────────────

def vnc_types(host, port):
    s = tcp(host, port)
    ver = recv_n(s, 12)
    if not ver.startswith(b"RFB"):
        raise Unreachable(f"not VNC: {ver!r}")
    s.sendall(b"RFB 003.008\n")
    n = recv_n(s, 1)[0]
    if n == 0:
        raise Unreachable("VNC server refused the handshake")
    types = list(recv_n(s, n))
    s.close()
    return ver.decode().strip(), types


def c_vnc_none(host, port):
    ver, types = vnc_types(host, port)
    return (CONFIRMED if 1 in types else ABSENT), f"{ver} security types {types}"


def c_vnc_auth(host, port):
    ver, types = vnc_types(host, port)
    return (CONFIRMED if 2 in types and 1 not in types else ABSENT), f"{ver} security types {types}"


# ── IPMI (cipher zero) ────────────────────────────────────────────────────────

def c_ipmi_cipher0(host, port):
    payload = (bytes([0, 0, 0, 0]) + b"\xa0\xa1\xa2\xa3"
               + bytes([0, 0, 0, 8, 0, 0, 0, 0]) + bytes([1, 0, 0, 8, 0, 0, 0, 0])
               + bytes([2, 0, 0, 8, 0, 0, 0, 0]))
    req = (bytes([0x06, 0x00, 0xFF, 0x07]) + bytes([0x06, 0x10]) + b"\x00" * 8
           + struct.pack("<H", len(payload)) + payload)
    resp = udp_exchange(host, port, req)[0]
    if len(resp) < 18 or resp[0] != 0x06 or resp[5] != 0x11:
        return ABSENT, f"reply is not an RMCP+ Open Session Response: {resp[:8].hex()}"
    status = resp[17]
    return (CONFIRMED if status == 0 else ABSENT), f"RMCP+ open-session status 0x{status:02x}"


# ── datastores, mail, ftp, tftp ───────────────────────────────────────────────

def c_redis_noauth(host, port):
    s = tcp(host, port)
    s.sendall(b"PING\r\n")
    r = s.recv(64)
    s.close()
    if r.startswith(b"+PONG"):
        return CONFIRMED, "PING answered without authentication"
    return ABSENT, f"reply {r[:40]!r}"


def c_mqtt_anon(host, port):
    cid = b"mqtt-client"
    rem = b"\x00\x04MQTT" + b"\x04\x02" + struct.pack(">H", 60) + struct.pack(">H", len(cid)) + cid
    s = tcp(host, port)
    s.sendall(b"\x10" + bytes([len(rem)]) + rem)
    r = s.recv(16)
    s.close()
    if len(r) >= 4 and r[0] == 0x20:
        return (CONFIRMED if r[3] == 0 else ABSENT), f"CONNACK return code {r[3]}"
    return ABSENT, f"no CONNACK: {r!r}"


def c_mysql_cleartext(host, port):
    s = tcp(host, port)
    pkt = s.recv(512)
    s.close()
    if len(pkt) < 20 or pkt[4] != 10:
        raise Unreachable(f"not a MySQL greeting: {pkt[:12]!r}")
    end = pkt.index(b"\x00", 5)
    version = pkt[5:end].decode("latin-1")
    caps = struct.unpack("<H", pkt[end + 14:end + 16])[0]
    if caps & 0x0800:
        return ABSENT, f"{version}: server offers TLS (CLIENT_SSL set)"
    return CONFIRMED, f"{version}: server does not offer TLS"


def c_tftp_read(host, port):
    r = udp_exchange(host, port, b"\x00\x01lab.txt\x00octet\x00")[0]
    op = struct.unpack(">H", r[:2])[0]
    if op == 3:
        return CONFIRMED, f"RRQ lab.txt answered with DATA ({len(r) - 4} bytes)"
    return ABSENT, f"opcode {op}: {r[4:60]!r}"


def c_ftp_anon_write(host, port):
    import ftplib
    ftp = ftplib.FTP()
    try:
        ftp.connect(host, port, timeout=8)
    except OSError as exc:
        raise Unreachable(str(exc))
    try:
        ftp.login()
        ftp.cwd("upload")
        ftp.storbinary("STOR vedha-probe.txt", io.BytesIO(b"probe"))
        ftp.delete("vedha-probe.txt")
        return CONFIRMED, "anonymous login can STOR into /upload"
    except ftplib.all_errors as exc:
        return ABSENT, f"anonymous write refused: {exc}"
    finally:
        try:
            ftp.close()
        except OSError:
            pass


def c_smtp_relay(host, port):
    import smtplib
    s = smtplib.SMTP(timeout=8)
    try:
        s.connect(host, port)
        s.ehlo()
        starttls = s.has_extn("starttls")
        s.mail("<probe@external.invalid>")
        code, _ = s.rcpt("<victim@external.invalid>")
        vcode, _ = s.verify("root")
        s.rset()
    except OSError as exc:
        raise Unreachable(str(exc))
    except smtplib.SMTPException as exc:
        return ABSENT, f"SMTP refused: {exc}"
    finally:
        try:
            s.close()
        except OSError:
            pass
    detail = f"RCPT external={code} VRFY={vcode} STARTTLS={'yes' if starttls else 'no'} (no DATA sent)"
    return (CONFIRMED if code in (250, 251) else ABSENT), detail


# ── web / TLS ─────────────────────────────────────────────────────────────────

def c_http_methods(host, port):
    try:
        c = http.client.HTTPConnection(host, port, timeout=8)
        c.request("OPTIONS", "/dav/")
        r = c.getresponse()
        allow = r.getheader("Allow", "")
        r.read()
        c.request("TRACE", "/")
        t = c.getresponse()
        t.read()
    except OSError as exc:
        raise Unreachable(str(exc))
    bad = [m for m in ("PUT", "DELETE") if m in allow]
    if bad or t.status == 200:
        return CONFIRMED, f"Allow='{allow}' TRACE={t.status}"
    return ABSENT, f"Allow='{allow}' TRACE={t.status}"


def tls_cert(host, port):
    need("openssl")
    env = dict(os.environ)
    conf = os.path.join(CONF_DIR, "openssl-seclevel0.cnf")
    if os.path.exists(conf):
        env["OPENSSL_CONF"] = conf
    p = subprocess.run(["openssl", "s_client", "-connect", f"{host}:{port}", "-showcerts",
                        "-cipher", "DEFAULT:@SECLEVEL=0"], input=b"", capture_output=True,
                       timeout=20, env=env)
    pem = re.search(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
                    p.stdout.decode("latin-1"), re.S)
    if not pem:
        raise Unreachable(f"{host}:{port} no certificate returned")
    t = subprocess.run(["openssl", "x509", "-noout", "-text"], input=pem.group(0).encode(),
                       capture_output=True, timeout=10, env=env).stdout.decode("latin-1")
    bits = re.search(r"Public-Key: \((\d+) bit\)", t)
    sig = re.search(r"Signature Algorithm: (\S+)", t)
    return (int(bits.group(1)) if bits else 0), (sig.group(1) if sig else "?")


def c_tls_weakkey(host, port):
    bits, sig = tls_cert(host, port)
    return (CONFIRMED if 0 < bits < 2048 else ABSENT), f"{bits}-bit key, signature {sig}"


def c_tls_sha1(host, port):
    bits, sig = tls_cert(host, port)
    weak = any(x in sig.lower() for x in ("sha1", "md5"))
    return (CONFIRMED if weak else ABSENT), f"{bits}-bit key, signature {sig}"


def c_tls_strong(host, port):
    bits, sig = tls_cert(host, port)
    ok = bits >= 2048 and not any(x in sig.lower() for x in ("sha1", "md5"))
    return (CONFIRMED if ok else ABSENT), f"{bits}-bit key, signature {sig} (control: expect strong)"


def c_proxy_open(host, port):
    s = tcp(host, port)
    s.sendall(b"GET http://example.invalid/ HTTP/1.0\r\nHost: example.invalid\r\n\r\n")
    r = s.recv(1024).decode("latin-1")
    s.close()
    first = r.split("\r\n", 1)[0]
    if not first.startswith("HTTP/"):
        raise Unreachable(f"not an HTTP proxy: {first!r}")
    if " 407 " in first or "407" in first.split(" ")[1:2]:
        return ABSENT, f"proxy asks for authentication: {first}"
    return CONFIRMED, f"proxy processed a request without credentials: {first}"


# ── IoT / AI emulator-backed ──────────────────────────────────────────────────

def rtsp_exchange(host, port, method):
    s = tcp(host, port)
    url = "*" if method == "OPTIONS" else f"rtsp://{host}:{port}/"
    s.sendall(f"{method} {url} RTSP/1.0\r\nCSeq: 1\r\n\r\n".encode())
    r = s.recv(2048).decode("latin-1")
    s.close()
    return r


def c_rtsp_options(host, port):
    r = rtsp_exchange(host, port, "OPTIONS")
    pub = next((ln.split(":", 1)[1].strip() for ln in r.split("\r\n")
                if ln.lower().startswith("public:")), "")
    return (CONFIRMED if r.startswith("RTSP/") and pub else ABSENT), f"Public: {pub}"


def c_rtsp_describe(host, port):
    r = rtsp_exchange(host, port, "DESCRIBE")
    first = r.split("\r\n", 1)[0]
    return (CONFIRMED if " 200 " in first else ABSENT), f"DESCRIBE -> {first}"


def c_adb_noauth(host, port):
    data = b"host::features=shell_v2,cmd\x00"
    hdr = struct.pack("<IIIIII", 0x4E584E43, 0x01000000, 256 * 1024, len(data),
                      sum(data) & 0xFFFFFFFF, 0x4E584E43 ^ 0xFFFFFFFF)
    s = tcp(host, port)
    s.sendall(hdr + data)
    r = recv_n(s, 24)
    s.close()
    cmd = struct.unpack("<I", r[:4])[0]
    if cmd == 0x4E584E43:
        return CONFIRMED, "CNXN returned with no AUTH step"
    return ABSENT, f"command 0x{cmd:08x} (AUTH means authenticated)"


def http_get(host, port, path):
    try:
        with urllib.request.urlopen(f"http://{host}:{port}{path}", timeout=8) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except OSError as exc:
        raise Unreachable(str(exc))


def c_ollama(host, port):
    status, body = http_get(host, port, "/api/tags")
    return (CONFIRMED if status == 200 and '"models"' in body else ABSENT), f"/api/tags -> {status}"


def c_cwmp(host, port):
    status, body = http_get(host, port, "/")
    return (CONFIRMED if "cwmp" in body.lower() else ABSENT), f"GET / -> {status}"


def c_ssdp_igd(host, port):
    req = (b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\n'
           b"MX: 3\r\nST: ssdp:all\r\n\r\n")
    r = udp_exchange(host, port, req)[0].decode("latin-1")
    loc = re.search(r"(?im)^location:\s*(\S+)", r)
    if not loc:
        return ABSENT, "SSDP reply has no LOCATION"
    with urllib.request.urlopen(loc.group(1), timeout=8) as resp:
        xml = resp.read().decode("utf-8", "replace")
    ok = "InternetGatewayDevice" in xml and "WANIPConnection" in xml
    return (CONFIRMED if ok else ABSENT), f"rootDesc at {loc.group(1)}: IGD+WANIPConnection={ok}"


def c_ntp_monlist(host, port):
    replies = udp_exchange(host, port, b"\x17\x00\x03\x2a" + b"\x00" * 4, timeout=4, extra_wait=1.0)
    first = replies[0]
    total = sum(len(x) for x in replies)
    if first[0] & 0x80 and (first[0] & 7) == 7:
        return CONFIRMED, f"monlist answered: {len(replies)} datagrams, {total} bytes for an 8-byte request (x{total // 8})"
    return ABSENT, f"no mode-7 response: {first[:8].hex()}"


def c_sip_options(host, port):
    req = (f"OPTIONS sip:probe@{host} SIP/2.0\r\nVia: SIP/2.0/UDP {host}:5060;branch=z9hG4bKlab1\r\n"
           f"Max-Forwards: 70\r\nTo: <sip:probe@{host}>\r\nFrom: <sip:lab@lab.invalid>;tag=lab1\r\n"
           "Call-ID: lab-probe-1\r\nCSeq: 1 OPTIONS\r\nContent-Length: 0\r\n\r\n").encode()
    r = udp_exchange(host, port, req)[0].decode("latin-1")
    first = r.split("\r\n", 1)[0]
    server = next((ln.split(":", 1)[1].strip() for ln in r.split("\r\n")
                   if ln.lower().startswith("server:")), "")
    return (CONFIRMED if first.startswith("SIP/2.0 200") else ABSENT), f"{first}; Server: {server}"


def c_nbns(host, port):
    q = (b"\x13\x37\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20"
         + b"CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + b"\x00\x00\x21\x00\x01")
    r = udp_exchange(host, port, q)[0]
    return (CONFIRMED if len(r) > 56 else ABSENT), f"NetBIOS node-status reply, {len(r)} bytes"


def c_mdns(host, port):
    q = (b"\x12\x34\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x09_services\x07_dns-sd\x04_udp"
         b"\x05local\x00\x00\x0c\x00\x01")
    r = udp_exchange(host, port, q)[0]
    return (CONFIRMED if len(r) > 12 else ABSENT), f"mDNS answered unicast query, {len(r)} bytes"


# ── CLI-tool based ────────────────────────────────────────────────────────────

def c_dns_axfr(host, port):
    out = run(["dig", f"@{host}", "-p", str(port), "axfr", "lab.local", "+time=3", "+tries=1"])
    if "XFR size" in out:
        return CONFIRMED, "AXFR of lab.local completed"
    if "connection timed out" in out or "no servers could be reached" in out:
        raise Unreachable("DNS server unreachable")
    return ABSENT, "zone transfer refused"


def c_nfs_export(host, port):
    out = run(["showmount", "-e", host])
    if "/srv/lab/nfs" in out and "*" in out:
        return CONFIRMED, "export /srv/lab/nfs is open to *"
    if "RPC" in out or "Unable" in out or "timed out" in out:
        raise Unreachable(out.strip().splitlines()[0] if out.strip() else "no mountd")
    return ABSENT, out.strip()[:100]


def c_rsync_anon(host, port):
    out = run(["rsync", "--list-only", f"--port={port}", f"rsync://{host}/"])
    if "public" in out:
        return CONFIRMED, "anonymous module list includes 'public'"
    if "failed" in out or "refused" in out:
        raise Unreachable(out.strip()[:100])
    return ABSENT, out.strip()[:100]


def c_ldap_anon_search(host, port):
    out = run(["ldapsearch", "-x", "-H", f"ldap://{host}:{port}", "-b", "dc=lab,dc=local", "-LLL"])
    n = len(re.findall(r"(?m)^dn:", out))
    if n >= 2:
        return CONFIRMED, f"anonymous search returned {n} entries"
    if "Can't contact" in out:
        raise Unreachable("LDAP unreachable")
    return ABSENT, f"{n} entries returned"


def c_snmpv3_noauth(host, port):
    out = run(["snmpget", "-v3", "-l", "noAuthNoPriv", "-u", "labnoauth", "-t", "3", "-r", "1",
               f"{host}:{port}", "1.3.6.1.2.1.1.1.0"])
    if "STRING" in out or "sysDescr" in out:
        return CONFIRMED, "SNMPv3 noAuthNoPriv user answered"
    if "Timeout" in out:
        raise Unreachable("SNMP timeout")
    return ABSENT, out.strip()[:100]


def c_snmp_bulk(host, port):
    out = run(["snmpbulkwalk", "-v2c", "-c", "public", "-Cr50", "-t", "3", "-r", "1",
               f"{host}:{port}", "1.3.6.1.2.1"], timeout=30)
    lines = [ln for ln in out.splitlines() if "=" in ln]
    if len(lines) >= 20:
        return CONFIRMED, f"GETBULK returned {len(lines)} varbinds from one request"
    if "Timeout" in out:
        raise Unreachable("SNMP timeout")
    return ABSENT, f"only {len(lines)} varbinds"


CHECKS = {
    "ssh-weak": (2222, c_ssh_weak), "ssh-terrapin": (2223, c_ssh_terrapin),
    "vnc-none": (5900, c_vnc_none), "vnc-auth": (5901, c_vnc_auth),
    "ipmi-cipher0": (623, c_ipmi_cipher0), "redis-noauth": (6379, c_redis_noauth),
    "mqtt-anon": (1883, c_mqtt_anon), "mysql-cleartext": (3306, c_mysql_cleartext),
    "tftp-read": (69, c_tftp_read), "ftp-anon-write": (21, c_ftp_anon_write),
    "smtp-relay": (25, c_smtp_relay), "http-methods": (8080, c_http_methods),
    "tls-weakkey": (8444, c_tls_weakkey), "tls-sha1": (8445, c_tls_sha1),
    "tls-strong": (9443, c_tls_strong), "proxy-open": (3128, c_proxy_open),
    "rtsp-options": (554, c_rtsp_options), "rtsp-describe": (8554, c_rtsp_describe),
    "adb-noauth": (5555, c_adb_noauth), "ollama": (11434, c_ollama), "cwmp": (7547, c_cwmp),
    "ssdp-igd": (1900, c_ssdp_igd), "ntp-monlist": (123, c_ntp_monlist),
    "sip-options": (5060, c_sip_options), "nbns": (137, c_nbns), "mdns": (5353, c_mdns),
    "dns-axfr": (53, c_dns_axfr), "nfs-export": (2049, c_nfs_export),
    "rsync-anon": (873, c_rsync_anon), "ldap-anon-search": (389, c_ldap_anon_search),
    "snmpv3-noauth": (161, c_snmpv3_noauth), "snmp-bulk": (161, c_snmp_bulk),
}


def main(argv):
    if len(argv) >= 5 and argv[1] == "up":
        proto, host, port = argv[2], argv[3], int(argv[4])
        try:
            if proto == "tcp":
                tcp(host, port).close()
                print(f"{host}:{port}/tcp accepts connections")
            else:
                udp_exchange(host, port, b"\x00")
                print(f"{host}:{port}/udp answers")
            return CONFIRMED
        except Unreachable as exc:
            print(str(exc))
            return UNREACHABLE
    if len(argv) >= 4 and argv[1] == "check" and argv[2] in CHECKS:
        default_port, fn = CHECKS[argv[2]]
        host = argv[3]
        port = int(argv[4]) if len(argv) > 4 else default_port
        try:
            code, detail = fn(host, port)
        except Unreachable as exc:
            print(str(exc))
            return UNREACHABLE
        except (OSError, subprocess.SubprocessError, ValueError, IndexError, struct.error) as exc:
            print(f"probe error: {exc}")
            return UNREACHABLE
        print(detail)
        return code
    print("usage: lab_probe.py up tcp|udp HOST PORT | check NAME HOST [PORT]\nchecks: "
          + ", ".join(sorted(CHECKS)))
    return UNREACHABLE


if __name__ == "__main__":
    sys.exit(main(sys.argv))
