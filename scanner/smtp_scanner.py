"""
smtp_scanner.py — SMTP hygiene: user enumeration + transport encryption
(VA checklist: mail-service information disclosure and cleartext credentials).

METHOD (collection, read-only): open the SMTP control channel, read the greeting,
send EHLO to learn the advertised capabilities, then:
  * check whether STARTTLS is offered (its absence means mail — and any AUTH — can
    be sent in cleartext);
  * test whether VRFY discriminates between an existing mailbox (postmaster, which
    RFC 5321 requires to exist) and a random non-existent one — if the two get
    different definitive answers, VRFY leaks valid usernames;
  * note whether EXPN is enabled (mailing-list expansion).

NO mail is ever sent and NO open-relay test is performed (that would actually
relay a message). VRFY/EXPN are read-only recon verbs — no credential is guessed
and no message is delivered — so this stays inside the probe's invariants.

SAFETY: line-based control protocol over BaseScanner timeouts; bounded reads;
every command guarded.
"""

from __future__ import annotations

import asyncio
import re
import socket

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_SMTP_PORTS = [25]
EHLO_NAME = "probe.example.com"       # neutral, non-attributing
_RANDOM_USER = "nx7q2wzkprobe"        # very unlikely to exist
_DEFINITIVE_CODES = {250, 251, 550, 551}   # VRFY answers that assert existence/non-existence


def parse_ehlo_capabilities(text: str) -> list[str]:
    """Extract EHLO capability tokens from a multi-line 250 response."""
    caps: list[str] = []
    for line in (text or "").splitlines():
        m = re.match(r"^250[ -](.*)$", line.strip())
        if m:
            cap = m.group(1).strip()
            if cap:
                caps.append(cap.upper())
    return caps


def vrfy_leaks(postmaster_code: int, random_code: int) -> bool:
    """VRFY leaks usernames when it gives DIFFERENT definitive answers for an
    existing vs a non-existent mailbox (e.g. 250 vs 550). Equal codes (accept-all
    or always-252) do not discriminate and are not a leak."""
    return (postmaster_code in _DEFINITIVE_CODES
            and random_code in _DEFINITIVE_CODES
            and postmaster_code != random_code)


class SMTPScanner(BaseScanner):
    name = "smtp_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_SMTP_PORTS

    def _read_response(self, sock: socket.socket) -> tuple[int, str]:
        buf = b""
        while len(buf) < 16384:
            try:
                chunk = sock.recv(4096)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            if re.search(rb"(?m)^\d\d\d ", buf):   # a final line 'NNN ' (code + space)
                break
        text = buf.decode("latin-1", "replace")
        m = re.search(r"(?m)^(\d\d\d) ", text)
        return (int(m.group(1)) if m else 0), text

    def _cmd(self, sock: socket.socket, line: str) -> tuple[int, str]:
        sock.sendall(line.encode("latin-1") + b"\r\n")
        return self._read_response(sock)

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: greeting → EHLO → STARTTLS/VRFY/EXPN checks. Monkeypatchable."""
        data: dict = {"smtp": None}
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                code, greet = self._read_response(s)
                if code == 0:
                    return {"smtp": None, "reason": "no_smtp_greeting"}
                data["smtp"] = True
                data["banner"] = greet.strip().splitlines()[0] if greet.strip() else ""

                _, ehlo = self._cmd(s, f"EHLO {EHLO_NAME}")
                caps = parse_ehlo_capabilities(ehlo)
                data["ehlo_capabilities"] = caps
                data["starttls"] = any(c.startswith("STARTTLS") for c in caps)

                pm_code, _ = self._cmd(s, "VRFY postmaster")
                rnd_code, _ = self._cmd(s, f"VRFY {_RANDOM_USER}")
                data["vrfy_postmaster_code"] = pm_code
                data["vrfy_random_code"] = rnd_code
                data["vrfy_enabled"] = vrfy_leaks(pm_code, rnd_code)

                expn_code, _ = self._cmd(s, "EXPN postmaster")
                # 500/502 = unknown/not-implemented, 252 = refused → EXPN effectively
                # off; anything else (250/550/551) means the verb is accepted.
                data["expn_code"] = expn_code
                data["expn_enabled"] = expn_code not in (0, 500, 502, 252)

                try:
                    self._cmd(s, "QUIT")
                except OSError:
                    pass
        except OSError as exc:
            return {"smtp": None, "reason": "no_smtp", "detail": str(exc)[:120]}
        return data

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("smtp"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_smtp"),
                              data=data)
        evidence = (f"starttls={data.get('starttls')} vrfy={data.get('vrfy_enabled')} "
                    f"expn={data.get('expn_enabled')}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("SMTP hygiene: VRFY/EXPN user-enum + STARTTLS presence")
    parser.add_argument("-p", "--ports", default=None, help="SMTP ports (default: 25)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_SMTP_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SMTPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                              timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
