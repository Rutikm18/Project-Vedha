# First-Level Enterprise Network VA — Plan

> Scope correction (2026-08-25): enterprise on-prem network, NOT cloud. CDN/cloud
> enrichment dropped. Tier-1 = breadth-first, unauthenticated / empty-credential,
> READ-ONLY checks against internal network services. Out of scope: cloud posture,
> web-app deep testing, credentialed scans, exploitation. Invariant preserved: NO
> credential guessing / spraying — anonymous / null / default-community only.

## Current Tier-1 coverage (already built)
Discovery (host/port/UDP) · service+version+OS ID · per-service checks for SMB
(v1/signing/null-session), SSH (weak algos/Terrapin), TLS (proto/cipher/cert), RDP
(NLA), SNMP (default community), DNS (AXFR/DNSSEC/version), LDAP (anon bind), Web
(methods/headers/version), DB (exposed/unauth), UDP (amplifiers/open-resolver).

## Confirmed gaps (service is identified, but no Tier-1 vuln check exists)
| Service (port) | Missing check | Core logic | In-policy |
|---|---|---|---|
| NFS (2049/111) | Anonymous export enum (showmount -e) | ONC RPC portmap + MOUNT EXPORT | ✅ read-only |
| FTP (21) | Anonymous login actually tested | USER anonymous handshake | ✅ documented anon acct |
| rsync (873) | Anonymous module listing | @RSYNCD handshake | ✅ read-only |
| VNC (5900) | Auth-type / no-auth detection | RFB security-types | ✅ read offered types |
| IPMI (623/udp) | Cipher-zero auth-bypass detection | IPMI 2.0 RMCP+ open-session | ⚠️ detect only, no hash grab |
| SMTP (25) | VRFY/EXPN user-enum + STARTTLS presence | SMTP verbs | ⚠️ enum only, no relay send |
| MSRPC (135) | Endpoint-mapper enumeration | impacket epm | ✅ read-only |
| Printers (9100/631) | JetDirect/IPP exposure | PJL/IPP identify | ✅ read-only |

## Phased step-by-step plan
**Phase A — anonymous data/file exposure (highest ROI; continues null-session/anon-bind theme)**
1. NFS export enumeration (2049/111) → NFS-EXPORT-WORLD-READABLE (high)
2. FTP anonymous login (21) → FTP-ANON-ACCESS (high if writable)
3. rsync anonymous modules (873) → RSYNC-ANON-MODULES (high if readable)

**Phase B — remote-access & console exposure**
4. VNC auth detection (5900) → VNC-NO-AUTH (critical) / VNC-WEAK-AUTH (medium)
5. IPMI cipher-zero (623/udp) → IPMI-CIPHER-ZERO (critical) — detection only

**Phase C — mail & Windows RPC recon**
6. SMTP hygiene (25) → SMTP-USER-ENUM / SMTP-NO-STARTTLS — no active relay
7. MSRPC endpoint map (135) → MSRPC-ENDPOINTS-EXPOSED (info/low)

**Phase D — printers + consolidation**
8. Printer exposure (9100/631) → PRINTER-EXPOSED (low)
9. Enterprise attack-path correlations + per-scanner ground-truth/accuracy gate

## Per-step recipe
study protocol core logic → design → implement (BaseScanner, both trees, lazy
import, run_in_executor, bounded/guarded, monkeypatchable probe) → findings rule
(both trees) → wire run_all + scan_funnel + workflow (both trees) → tests
(pure-logic + monkeypatched probe + parity) → full suite green ×2.

## Cross-cutting foundations (thread in, not a separate project)
1. Two-tree (scanner/ vs main_scripts/) consolidation before Phase C.
2. Sealed-build (Nuitka) prototype for the new impacket submodules.
3. Accuracy gate — no check reaches "available" without ground-truth numbers.
