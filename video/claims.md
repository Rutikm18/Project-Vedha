# Claims register

Every claim the film makes on screen, where it comes from, and its status. **Unsourced claims need a human sign-off before publishing.** Product capability references point at `NETWORK_VA_USE_CASES.md` ("✅ verified & shipped" rows only). Background research is in `CHECKPOINTS.md`.

| # | On-screen claim | Source in repo | Status |
|---|---|---|---|
| 1 | "A 7-day network health check." / "Book your 7-day check" | `PlanPanel.tsx`: POC presets 7/14/30 days (default 14). No product copy says "7-day health check". | **Needs confirmation** |
| 2 | "Delivered by a partner you already trust." | Not found | **Needs confirmation** |
| 3 | "For office networks. Not cloud networks." | Probe runs inside the client network (`README.md`); not stated as copy | **Needs confirmation** |
| 4 | Vedha, वेद्या, "TO PIERCE THROUGH" | Not found. Owner instruction: the Devanagari is वेद्या. **वेद्या (vedyā, from the root vid, "to know") does not mean "to pierce through"; that gloss belongs to वेध.** | **Needs confirmation of the gloss + cultural review** |
| 5 | Checkpoint 1: "Remote logins" | RDP without NLA/TLS, VNC no or weak auth, exposed WinRM/X11 (posture rules, UC 30) | Sourced |
| 6 | Checkpoint 2: "Accounts & file servers" | SMBv1, SMB signing, null session; unauthenticated database read | Sourced (as the file services those servers run; the product doesn't identify Tally by name) |
| 7 | Checkpoint 3: "Backups" | NFS world-readable export, rsync/FTP anonymous, exposed admin UIs | Sourced (as the shares a backup sits on; no NAS device class yet) |
| 8 | Checkpoint 4: "Passwords nobody changed" | Default-credential candidates, SNMP default community, IPMI cipher-zero | Sourced |
| 9 | Checkpoint 5: "Old, unpatched systems" | OS past end of support (EOL catalog); KEV/EPSS-prioritised CVE correlation | Sourced |
| 10 | Checkpoint 6: "What the internet can reach" | Multi-vantage internet-exposure mapping (UC 81, needs 2+ probes) | Sourced (note: needs a second vantage point) |
| 11 | "Find what's open. Prove what's real. Show the fix worked." | Discovery and posture rules; attack-path correlation; coverage-proven clean before a finding auto-closes | Sourced |
| 12 | "A plain-language report. With proof." | Report pipeline (`lib/report/*`, `prompts/report.ts`: confidence-matched language) | Sourced |
| 13 | Grade C → B | Real scale A–F (`services/posture.py`); values illustrative | Sourced scale, illustrative values |
| 14 | Findings, hosts, IPs, "Verified 03 Oct 2026" | Illustrative (RFC 5737 IPs, `.example` hosts), each mapped to a shipped check in `src/data.illustrative.json`; tagged "Illustrative data" on screen | Illustrative |
| 15 | vedhasec.com | `docs/STATUS.md` | Sourced |

No statistics appear on screen (STAT_CARD = no). The QA gate checks that the captions contain none of the guardrail words: secure, protected, safe, hack-proof, 100%, certified, compliant, attack.
