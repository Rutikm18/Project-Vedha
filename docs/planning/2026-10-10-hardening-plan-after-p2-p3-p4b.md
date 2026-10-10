# Hardening plan after P2 / P3 / P4b and the backlog pass (10 Oct)

**Why this exists.** The attack-path work (P2 capability map, P3 relay and shared-credential edges, P4b suggested
crown jewels) and the backlog pass (Smart Install severity, Re-scan use case enabled) were built and tested the same
day. A second, adversarial read of that work against the code found places where it is wrong or will not scale.
This plan lists them, says why each matters, and splits the fixes into small tasks done one at a time.

## 1. Failure areas found (verified in the code, not assumed)

| # | Area | What is wrong | Why it matters | Evidence |
|---|---|---|---|---|
| F1 | Capability map promotes by ATT&CK tag | A finding with no curated rule falls back to its category, then its ATT&CK technique, and `T1190` / `T1210` / `T1133` / `T1021` map to a **control** capability | Imported scanner findings (`routers/vuln_scans.py` stores free-form `mitre_techniques`) become footholds. The module's own docstring promises "a future rule cannot be silently promoted to a foothold by a loose heuristic" and the code breaks that | `capability_map._MITRE_CAPABILITY`, `vuln_scans.py:551` |
| F2 | Exposure counted as ownership | `POSTURE-RDP-EXPOSED` and `POSTURE-RTSP-EXPOSED` are `lateral` (control). Reaching an RDP login screen is not owning the host | On a Windows estate every workstation with RDP open becomes "ownable", which is the FM-05 false positive the engine exists to prevent | `capability_map._RULE_CAPABILITY` |
| F3 | Relay precondition bypassed | `CORR-NTLM-RELAY-PATH` is `lateral` (control) on its own host, so the P3 rule "a relay needs a distinct same-subnet coercion source" (FM-09) is skipped whenever the composite fires | Signing-off hosts become ownable with no relay edge at all | `capability_map`, `credentials.py` |
| F4 | Preconditions treated as footholds | SMBv1 enabled, RDP without NLA, end-of-life OS and an exposed TR-069 port are `foothold` at full weight. The repo's own exploitability module says "a misconfiguration is NOT the CVE": a patched host still speaks SMBv1 | Over-confident routes; a route resting on "SMBv1 is on" ranks like one resting on an unauthenticated database | `exploitability.py` header, `capability_map` |
| F5 | Shared default credentials manufacture control | Hosts sharing a default SNMP community or vendor default get `CREDENTIAL_REUSE` edges at 0.85 likelihood. A read-only SNMP community grants no control, a vendor default is already each host's own foothold, and the edge needs no captured credential (the default is public) | Inflated likelihoods and O(k²) edges: 200 printers on `public` = 39,800 edges | `credentials.py`, `analyzer.movement_graph` |
| F6 | Relay edges are O(n²) per subnet | One edge per (SMB host, signing-off host) pair. A Windows /24 commonly has both on almost every host | 200 × 200 = 40,000 edges; the path search slows sharply, the same explosion FM-21 removed with subnet hubs | `credentials.derive_credential_edges` |
| F7 | Suggested crown jewels uncapped | Every host with a datastore port becomes a target. 50 Redis hosts = 50 targets × 80 candidates of shortest-path runs, plus one max-flow per target | Slow recompute on a GET-triggered first computation | `crown_jewels.py`, `analyzer.choke_analysis` |
| F8 | Suggested targets invisible on the dashboard | The engagement page says targets were suggested; the dashboard row and tiles say "crown jewels reachable" as if the operator chose them | Breaks the rule that an auto-pick never reads as a chosen scope | `graph/overview.py`, `OverviewList` |
| F9 | "Re-scan & Change Detection" overclaims | Enabled on 10 Oct, it runs a normal assessment. Nothing reports what changed between runs, although the catalogue says it "highlights new hosts, newly opened ports and configuration drift" | A customer-facing claim the product does not deliver | `use_cases.py`, `agents.py` |
| F10 | Never run on a real database | `_suggest_target_assets` (SQL) and the stored `target_selection` JSON were only exercised through patched unit tests | A type or query error would surface only in production | unit tests patch `_resolve_targets` |
| F11 | Stale or duplicated status | STATUS P1-3 still says P2/P3/P4b are not built; four rows appear twice; the stray `probe copy` row is already clean; P1-4 / P1-7 list SNMPv3 noAuth, FTP write and SIP/NetBIOS/mDNS/IKE as missing though they exist | The owner plans from a list that is wrong | `docs/STATUS.md` |

**Status: H1–H6 built, tested and pushed on `claude/elegant-noether-ggdafj`** (commits `e49e8bb7`
H1, `e0d08305` H2, `051c2277` H3, `b11d388f` H4, `fd9d9c0c` H5, `8dfad69a` H6). Local verification:
backend 3,143 passed / 8 skipped, detection engine 553, frontend 664, `tsc` clean, the 9-fixture
attack-path harness 9/9 with 0 fabricated paths, and a live PostgreSQL 16 run of the recompute,
overview and the new `/changes` endpoint (H6) that found and fixed a real boundary bug. Not run:
the Ubuntu weak-lab VM, Windows, CI, and a human review on real engagement data.

## 2. Tasks (small, done in order, each tested before the next)

| Task | Fixes | Done when |
|---|---|---|
| H1 | F1–F4 | Control is granted only by a curated rule id. Category/ATT&CK fallbacks classify but never grant control. RDP/RTSP exposure is recon; `CORR-NTLM-RELAY-PATH` is a relay precondition like signing-off; SMBv1 / no-NLA / EOL / TR-069 become a low-weight `exploit_precondition` step, raised only by real KEV/EPSS evidence. Tests prove each case. Validation harness still 9/9 |
| H2 | F5 | Shared default credentials are recorded as information (in the stored analysis, for the report) and create no movement edges |
| H3 | F6 | Relay is modelled through one relay hub per subnet: O(sources + targets) edges, same routes, `technique = RELAY`, the hub never appears as a subnet in a hop's `via`. A 200-host test stays fast |
| H4 | F7, F8 | Suggestions capped (domain controllers and hypervisors first, at most 10). The overview row and the dashboard say "suggested" when the targets were suggested, and the engagement page says so on an empty result too |
| H5 | F9 | `GET /engagements/{id}/changes`: what the latest completed detection run changed against the one before it (new hosts, newly seen services, new / resolved / reopened findings), read-only. The use-case text is narrowed to what is computed |
| H6 | F10 | Run the recompute, the overview and the new changes endpoint against PostgreSQL 16 with real rows |
| H7 | F11 | STATUS, the attack-path plan and the dashboard plan match the code |
| H8 | — | Full backend, detection engine, probe parity, frontend tests, `tsc`, `next build`; commit and push after each task |

## 3. Out of scope here (needs the owner or a lab)

Windows signing, AI credentials, AWS hosting, CI billing, a weak-lab re-scan, the field test on a clean Windows machine.
Accuracy on a real network is not claimed by any task above: the tests show the model is consistent, not that it is
right on a live estate.
