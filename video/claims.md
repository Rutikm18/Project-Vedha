# Claims register

Every claim the film makes on screen, where it comes from, and its status. **Unsourced claims need a human sign-off before publishing.** Product capability references point at `NETWORK_VA_USE_CASES.md` ("✅ verified & shipped" rows only). Background research is in `CHECKPOINTS.md`.

| # | On-screen claim | Source in repo | Status |
|---|---|---|---|
| 1 | "A 7-day network health check." / "Book your 7-day check" | `PlanPanel.tsx`: POC presets 7/14/30 days (default 14). No product copy says "7-day health check". | **Needs confirmation** |
| 2 | "Delivered by a partner you already trust." | Not found | **Needs confirmation** |
| 3 | "For office networks. Not cloud networks." | Probe runs inside the client network (`README.md`); not stated as copy | **Needs confirmation** |
| 4 | Vedha, वेद्या, "TO PIERCE THROUGH" | Not found. Owner instruction: the Devanagari is वेद्या. **वेद्या (vedyā, from the root vid, "to know") does not mean "to pierce through"; that gloss belongs to वेध.** | **Needs confirmation of the gloss + cultural review** |
| 5 | Scan + "DEVICES FOUND 16" | Network discovery and device inventory (UC 1, UC 2); the count is illustrative | Sourced capability, illustrative number |
| 6 | "The accounts PC: remote login left open." | **Observed in real probe output** (`probe/scans/*/findings.jsonl`): rule `SVC-RDP-EXPOSED`, "RDP exposed to the scan vantage", severity medium. The film uses the same severity (MEDIUM), the same evidence shape (3389 open + `tls_scan` handshake on 3389 as corroboration) and the rule's own fix ("Restrict RDP to VPN/jump hosts; enforce NLA + MFA") | Sourced from real output (asset illustrative) |
| 7 | "Client files: open to anyone on the Wi-Fi." | SMB null session, NFS world-readable export (posture rules) | Sourced (illustrative asset) |
| 8 | "Billing data: readable without a password." | Unauthenticated database read (posture rule) | Sourced (illustrative asset) |
| 9 | Checkpoints: Everything on your network · Remote logins · Accounts & file servers · What the internet can reach | UC 1/2; remote-access rules; file service + database rules; UC 81 | Sourced. **Backups, passwords and patching were removed on the owner's instruction (not offered)** |
| 10 | "Prove what's real." shown as evidence; "Proven" = "Confirmed by two independent checks" | Real runs record per-finding evidence and confidence; port-only RDP is "medium" until a second scanner corroborates it (here `tls_scan` on the same port) | Sourced |
| 11 | "Find what's open. Prove what's real. Show the fix worked." | Discovery and posture rules; attack-path correlation; coverage-proven clean before a finding auto-closes | Sourced |
| 12 | "A plain-language report. With proof." | Report pipeline (`lib/report/*`, `prompts/report.ts`: confidence-matched language) | Sourced |
| 13 | Grade C → B | Real scale A–F (`services/posture.py`); values illustrative | Sourced scale, illustrative values |
| 14 | Findings, hosts, IPs, "Verified 03 Oct 2026" | Illustrative (RFC 5737 IPs, `.example` hosts), each mapped to a shipped check in `src/data.illustrative.json`; tagged "Illustrative data" on screen | Illustrative |
| 15 | vedhasec.com | `docs/STATUS.md` | Sourced |

No statistics appear on screen (STAT_CARD = no). The QA gate checks that the captions contain none of the guardrail words: secure, protected, safe, hack-proof, 100%, certified, compliant, attack.
