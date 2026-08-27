"""
tls_scanner.py — collect TLS/SSL configuration facts.

METHOD (collection only): for each TLS port we attempt handshakes and record:
  * which protocol versions the server agrees to (TLS 1.0/1.1/1.2/1.3)
  * the negotiated cipher
  * certificate subject / issuer / validity / SANs
We only OBSERVE and RECORD. We do not judge "weak" or "vulnerable" here — the
detection layer decides that from these facts. Reporting raw facts keeps FP
measurement clean (e.g. "server accepted TLSv1.0" is a verifiable fact).

Pure standard library (ssl + socket); runs in a thread executor so it fits the
async base without blocking the loop. The 'cryptography' package enables full
DER cert parsing; without it we degrade gracefully to a byte count + hint.
"""

from __future__ import annotations

import asyncio
import ipaddress
import socket
import ssl
import warnings
from datetime import datetime, timezone

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)
from .ja4x import ja4x_from_cert   # JA4X X.509 fingerprint (advanced capability)

# Suppress the stdlib DeprecationWarning for TLS 1.0/1.1 version names once at
# import. We probe those versions deliberately to learn whether servers still
# accept them. Doing this per-handshake via warnings.catch_warnings() is not
# thread-safe (it mutates global warning state) and these handshakes run
# concurrently in a thread pool.
warnings.filterwarnings("ignore", category=DeprecationWarning, module="ssl")

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    _HAVE_CRYPTO = True
except ImportError:
    _HAVE_CRYPTO = False

# Protocol versions we probe individually to learn what the server accepts.
_PROTOCOLS = [
    ("TLSv1_3", getattr(ssl.TLSVersion, "TLSv1_3", None)),
    ("TLSv1_2", ssl.TLSVersion.TLSv1_2),
    ("TLSv1_1", ssl.TLSVersion.TLSv1_1),
    ("TLSv1_0", ssl.TLSVersion.TLSv1),
]

DEFAULT_TLS_PORTS = [443, 8443, 993, 995, 465, 636, 989, 990, 5986]


# --------------------------------------------------------------------------- #
# Cipher classification + posture grading (Tier 2.4) — pure, no network.
# --------------------------------------------------------------------------- #
def classify_cipher(name: str) -> dict:
    """
    Flag the security-relevant properties of an OpenSSL cipher-suite name:
    forward secrecy, AEAD vs CBC, and known weaknesses (RC4/NULL/DES/3DES/
    EXPORT/MD5/anonymous). Pure string analysis so it is trivially testable and
    independent of what the local OpenSSL happens to support.
    """
    up = name.upper()
    reasons: list[str] = []
    if "NULL" in up:
        reasons.append("NULL (no encryption)")
    if "RC4" in up:
        reasons.append("RC4 (broken stream cipher)")
    if "EXP" in up or "EXPORT" in up:
        reasons.append("EXPORT-grade (crippled key size)")
    if "MD5" in up:
        reasons.append("MD5 MAC")
    if "ADH" in up or "AECDH" in up or "ANON" in up:
        reasons.append("anonymous key exchange (no authentication)")
    # 3DES first (SWEET32); plain single-DES is even weaker.
    if "3DES" in up or "DES-CBC3" in up or "DES_CBC3" in up:
        reasons.append("3DES (SWEET32)")
    elif "DES" in up:
        reasons.append("DES (broken)")

    pfs = any(k in up for k in ("ECDHE", "DHE", "EECDH", "EDH")) and "ADH" not in up
    aead = any(k in up for k in ("GCM", "CHACHA20", "CCM"))
    cbc = "CBC" in up or (not aead and "RC4" not in up and "NULL" not in up)
    return {
        "name": name,
        "weak": bool(reasons),
        "weak_reasons": reasons,
        "forward_secrecy": pfs,
        "aead": aead,
        "cbc": cbc and not aead,
    }


_LOW_PROTOCOLS = {"SSLv2", "SSLv3", "TLSv1", "TLSv1_0", "TLSv1.0"}
_TLS11 = {"TLSv1_1", "TLSv1.1"}
_TLS12 = {"TLSv1_2", "TLSv1.2"}
_TLS13 = {"TLSv1_3", "TLSv1.3"}


def grade_tls_posture(accepted_versions, cipher_details: list[dict]) -> dict:
    """
    Grade overall TLS posture A/B/C/F from accepted protocol versions and the
    classified ciphers. Deterministic heuristic:
        F  deprecated protocol (SSLv3/TLS1.0) OR any weak cipher
        C  TLS 1.1 enabled, OR no forward secrecy offered
        B  TLS 1.2 fine but TLS 1.3 not offered
        A  TLS 1.3 present, PFS, no weak ciphers, no deprecated protocols
    """
    av = set(accepted_versions or [])
    findings: list[str] = []

    has_low = bool(av & _LOW_PROTOCOLS)
    has_11 = bool(av & _TLS11)
    has_12 = bool(av & _TLS12)
    has_13 = bool(av & _TLS13)

    weak = [c for c in cipher_details if c.get("weak")]
    any_pfs = any(c.get("forward_secrecy") for c in cipher_details) if cipher_details else None

    if has_low:
        findings.append("deprecated protocol enabled (SSLv3/TLS1.0)")
    if has_11:
        findings.append("TLS 1.1 enabled (deprecated)")
    for c in weak:
        findings.append(f"weak cipher {c['name']}: {', '.join(c['weak_reasons'])}")
    if any_pfs is False:
        findings.append("no forward secrecy offered")
    if not has_13 and has_12:
        findings.append("TLS 1.3 not offered")

    if has_low or weak:
        grade = "F"
    elif has_11 or any_pfs is False:
        grade = "C"
    elif not has_13:
        grade = "B"
    else:
        grade = "A"
    return {"grade": grade, "findings": findings}


def _sni(host: str) -> str | None:
    """Never send an IP literal as SNI — non-conformant; some servers reject it."""
    try:
        ipaddress.ip_address(host)
        return None
    except ValueError:
        return host


def _try_version(host: str, port: int, version, timeout: float):
    """Attempt a handshake forcing one protocol version. Returns cipher dict or None."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        ctx.minimum_version = version
        ctx.maximum_version = version
    except (ValueError, OSError):
        return None     # this Python/OpenSSL build can't pin that version
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=_sni(host)) as ssock:
                return {"cipher": ssock.cipher(), "version": ssock.version()}
    except Exception:
        return None


def _get_cert_der(host: str, port: int, timeout: float) -> bytes | None:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=_sni(host)) as ssock:
                return ssock.getpeercert(binary_form=True)
    except Exception:
        return None


def _parse_cert_der(der: bytes | None) -> dict:
    if not der:
        return {"raw_der_bytes": 0}
    if not _HAVE_CRYPTO:
        return {"raw_der_bytes": len(der),
                "note": "install 'cryptography' for full certificate parsing"}
    try:
        cert = x509.load_der_x509_certificate(der)
    except Exception as exc:
        return {"raw_der_bytes": len(der), "parse_error": str(exc)}
    try:
        san = cert.extensions.get_extension_for_class(
            x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName)
    except Exception:
        san = []
    try:                                        # cryptography >= 42
        not_before = cert.not_valid_before_utc
        not_after = cert.not_valid_after_utc
    except AttributeError:                      # older cryptography
        not_before = cert.not_valid_before.replace(tzinfo=timezone.utc)
        not_after = cert.not_valid_after.replace(tzinfo=timezone.utc)
    try:
        fp = cert.fingerprint(hashes.SHA256()).hex()
    except Exception:
        fp = None
    # Signature hash + public-key strength — the raw facts findings.py grades
    # (SHA-1/MD5 signatures and sub-2048-bit RSA keys are deprecated/forgeable).
    # Never a verdict here; just what the certificate declares.
    try:
        sig_alg = cert.signature_hash_algorithm.name if cert.signature_hash_algorithm else None
    except Exception:
        sig_alg = None
    try:
        pub = cert.public_key()
        key_type = type(pub).__name__.replace("PublicKey", "")
        key_bits = getattr(pub, "key_size", None) \
            or getattr(getattr(pub, "curve", None), "key_size", None)
    except Exception:
        key_type, key_bits = None, None
    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "san": san,
        "expired": not_after < datetime.now(timezone.utc),
        "self_signed": cert.subject == cert.issuer,
        "sha256_fingerprint": fp,
        "sig_algorithm": sig_alg,
        "public_key_type": key_type,
        "public_key_bits": key_bits,
        # JA4X — structural certificate fingerprint (FoxIO JA4+ suite); computed
        # from the cert already parsed, no extra probing. Identifies the tooling/CA
        # that minted the cert and correlates infrastructure.
        "ja4x": ja4x_from_cert(cert),
        "serial_hex": format(cert.serial_number, "x"),
    }


def _scan_tls_sync(host: str, port: int, timeout: float) -> dict | None:
    accepted: list[str] = []
    cipher_by_ver: dict[str, str] = {}
    for label, ver in _PROTOCOLS:
        if ver is None:
            continue
        res = _try_version(host, port, ver, timeout)
        if res:
            accepted.append(label)
            c = res["cipher"]
            cipher_by_ver[res["version"] or label] = c[0] if c else None
    if not accepted:
        return None  # not a TLS service / unreachable

    cipher_details = [classify_cipher(name)
                      for name in dict.fromkeys(v for v in cipher_by_ver.values() if v)]
    posture = grade_tls_posture(accepted, cipher_details)

    der = _get_cert_der(host, port, timeout)
    return {
        "accepted_versions": accepted,
        "cipher_by_version": cipher_by_ver,
        "cipher_analysis": cipher_details,
        "posture": posture,
        "certificate": _parse_cert_der(der),
    }


class TLSScanner(BaseScanner):
    name = "tls_scan"

    def __init__(self, *args, ports: list[int], **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports

    async def _scan_port(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                info = await loop.run_in_executor(
                    None, _scan_tls_sync, target, port, self.timeout)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not info:
            return None
        return ScanResult(
            self.name, target, port=port, proto="tcp", status="open",
            data=info,
            evidence=(f"grade {info['posture']['grade']}; accepts: "
                      + ", ".join(info["accepted_versions"])),
        )

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]


def main() -> None:
    parser = base_argparser("TLS/SSL configuration scanner")
    parser.add_argument("-p", "--ports", default=None,
                        help="TLS ports (default: common TLS ports)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_TLS_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = TLSScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
