# Checkpoints: what the film shows Vedha checking, and why

The first cut was built around a printer and a camera. Owners don't pay to protect a printer. They pay so they don't lose **their books, their backups, their ability to bill and get paid, and the trust of the customers and insurers who ask about security.** This file sets the checkpoints first, from research and from what the product verifiably detects (`NETWORK_VA_USE_CASES.md`, "verified & shipped" only). The film is then built on them.

## 1. What actually hurts a growing Indian business (research)

| Finding | Number | Source |
|---|---|---|
| Ransomware dominates small-business breaches | Ransomware present in **88%** of SMB breaches vs 39% at large orgs | Verizon 2025 DBIR, via [Infosecurity Magazine](https://infosecurity-magazine.com/news/verizon-dbir-smb-ransomware-attacks) |
| Remote access is the front door | Remote-access tools incl. RDP behind **87%** of ransomware claims; stolen credentials 47%, software exploits 29% | At-Bay 2026 InsurSec report (2025 data), via [Risk & Insurance](https://riskandinsurance.com/small-businesses-fear-cyber-threats-as-ransomware-risks-surge/) |
| Firewall / VPN edge devices are being broken into | Akira campaign via SonicWall SSL VPN accounts (2025); 16,000+ Fortinet devices backdoored | [CyberInsider](https://cyberinsider.com/sonicwall-vpns-targeted-in-akira-ransomware-surge-using-suspected-zero-day-exploits/), [OpenVPN blog](https://blog.openvpn.net/april-2025-security-alert-sonicwall-fortinet) |
| India: owners don't know where the gaps are | Operational root causes: lack of protection **43%**, **unknown security gap 40%**, poor-quality protection 38% | Sophos State of Ransomware in India 2026, via [Outlook Business](https://www.outlookbusiness.com/technology/around-53-of-indian-firms-surveyed-paid-ransom-to-recover-data-from-cyber-attacks) |
| India: data gets encrypted, backups decide the outcome | 60% of attacks encrypted data; 67% recovered using backups | Sophos India 2026 (same) |
| NAS devices hold the data and the backups | A NAS that is encrypted can take the backups with it (eCh0raix, DeadBolt via weak logins and old firmware) | [SANS ISC](https://isc.sans.edu/diary/18481), [Dark Reading](https://www.darkreading.com/cyberattacks-data-breaches/roundtable-cyberattack-frenzy-qnap-customers-protect-business) |
| Insurers now ask for evidence | Underwriters ask for regular vulnerability scanning and its coverage; RDP must be off or behind MFA; backups offline or immutable | [Flamingo](https://www.flamingo.run/blog/cyber-insurance-requirements), [Dealplexus: Indian SME cyber insurance](https://www.dealplexus.com/blog/cyber-insurance-indian-smes/raw) |
| Suppliers to big companies get security questionnaires | Supply-chain security is a top reason SMBs buy security | [Analysys Mason / Check Point](https://www.checkpoint.com/resources/items/report-analysys-mason-smb-cyber-security-challenges-solutions) |

**Caveat:** I couldn't open the Sophos India PDF (blocked by this environment's network). Its figures come from press coverage. The brief's guardrail stands: **no statistics appear on screen** (STAT_CARD = no). These numbers only justify what the film emphasises.

**Why they pay** (the value the film must make visible):
1. **Keep the business running:** books, billing, GST filing, payroll.
2. **Be able to recover:** backups that survive an attack.
3. **Close the front door:** remote logins and the firewall/VPN.
4. **Proof for others:** a plain report for the insurer, the big customer's questionnaire, the board.

## 2. The checkpoints (what the 7-day check looks at)

Each checkpoint is an asset an owner recognises, mapped to checks the product **already ships** (✅ in `NETWORK_VA_USE_CASES.md`).

| # | Checkpoint (owner's words) | Asset it protects | Vedha checks (shipped) |
|---|---|---|---|
| 1 | **Remote logins** | The way in: RDP, VNC, remote management | RDP without NLA, RDP without TLS, VNC with no or weak auth, exposed WinRM/X11 (UC 30, posture rules) |
| 2 | **Accounts and file servers** | Books, billing, client files on Windows shares | SMBv1 on (EternalBlue), SMB signing off (NTLM relay), null sessions; unauthenticated database reads |
| 3 | **Backups** | The copy you recover from | World-readable NFS exports, anonymous rsync/FTP, exposed admin web UIs |
| 4 | **Passwords nobody changed** | Admin access to network gear and servers | Default-credential candidates, SNMP default community, IPMI cipher-zero |
| 5 | **Old, unpatched systems** | Everything still running on them | OS past end of support, known-exploited CVEs prioritised by CISA KEV and EPSS |
| 6 | **What the internet can reach** | All of the above, seen from outside | Multi-vantage internet-exposure mapping (UC 81) |

Then the proof steps, which are what make it more than a scan:
- **Prove:** attack-path correlation shows the chain, e.g. legacy Windows surface (SMBv1 + exposed RDP), NTLM-relay path.
- **Fix, then verify:** "coverage-proven clean". A finding closes only when re-checks prove it, and a blind rule can't pass as clean.
- **Report:** plain language; confirmed and suspected findings stay separate.

## 3. How the film uses them

- **Scene 2 (the path)** is now about assets that matter: *a remote login left open → a password never changed → the accounts server → the backups.*
- **New beat (12.5 to 16.0 s):** the six checkpoints appear as a numbered list under the line "It checks what your business runs on."
- **Scene 5 (console):** findings, attack path and fix all use checkpoints 1 to 3. The fix closes the **remote login**, which is the same door the hook opened, so the visual rhyme gets stronger.
- **Report:** "Remote login locked down · Backup share restricted · Default password changed".

## 4. Product gaps this exposed (not film work; for the roadmap)

The film names assets by role ("accounts server", "backups"), not by product. The product doesn't yet:
- recognise **Tally** (default port 9000 is labelled "dev app / SonarQube / Portainer" in `port_intel.py`)
- classify a **NAS** (Synology 5000/5001 collides with "Docker registry")
- recognise **firewall/VPN appliances** by model, the 2025 edge-device campaigns above

Adding these would make the checkpoints in the film fully literal.
