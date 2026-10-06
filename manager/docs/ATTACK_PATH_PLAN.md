# Engagement-wide, multi-subnet attack-path generation — plan (for review)

Status: **PLAN ONLY — not implemented.** Awaiting approval before any code.

Goal (user's words): *create attack paths based on the findings in the
infrastructure, across multiple subnets of the same org, by choosing the
engagement.*

---

## 1. Research — how attack paths are generated (what the field does)

Synthesis of the literature + commercial practice, mapped to what Vedha can do
with probe-collected facts (no agent on every host, no firewall configs).

**Academic / logical attack graphs**
- **MulVAL** (Ou et al., Princeton/USENIX'05) is the reference: encode the
  network as **Datalog facts** and derive multi-host/multi-stage privilege with
  generic rules. Crucially it models reachability as **HACL** — host
  access-control tuples like `hacl(internet, web, TCP, 80)` ("who can reach what
  port"). Attack-graph generation = *reachability analysis → attack-template
  instantiation → graph construction*. (cs.princeton.edu/~appel/papers/mulval.pdf)
- Surveys (Zeng 2019; arXiv:2302.14479) converge on the same four stages:
  **acquire system info → generate graph → analyse (paths/chokepoints) → use**.
  Node-aggregation / importance methods exist to keep large graphs legible
  (ACM 10.1145/3723890.3723912).

**Identity graphs**
- **BloodHound** answers "given what I control, what is the shortest chain to
  Domain Admin / a high-value target?" over a graph of users, computers, groups,
  ACLs, sessions and **credential/relationship edges**. Lesson for us: model
  **credential reuse and AD-exposure as first-class edges**, and frame output as
  *shortest path from a foothold to a crown jewel*.

**Commercial exposure-graph tools (XM Cyber, Microsoft Security Exposure
Management, Wiz)**
- Model **all lateral-movement chains continuously** and score **by reachability
  to critical assets**, not per-vuln in isolation.
- **Choke points**: the few nodes where many paths to crown jewels converge —
  XM Cyber's own data says **~2% of exposures sit on choke points, ~74% are dead
  ends**, and **~80% of real exposures are misconfigurations/identity, <1% CVEs**.
  Two direct implications for Vedha:
  1. **Posture / IOA / misconfig findings must be attack-step sources**, not only
     CVE-`exploitable` findings (today the graph only uses `exploitable`).
  2. The value is in **pruning to the paths that actually reach crown jewels** and
     surfacing **choke points**, which the existing `PathAnalyzer` already computes.

**Takeaway for Vedha's constraints:** we don't have firewall ACLs, so we **infer**
reachability (MulVAL's HACL) from what the probes already observe — subnet
membership, multi-vantage exposure (external vs internal-only), and device roles
(gateways) — and we **label every reachability edge `observed` vs `assumed`** so a
cross-subnet guess is never presented as fact (mirrors the confirmed/suspected
discipline the engine already enforces).

---

## 2. What already exists in the codebase (and the real gap)

Mostly-built, genuinely capable — and **dormant**:

| Component | State |
|---|---|
| `graph/builder.py` `GraphBuilder` | Builds a multi-type `networkx` graph (Asset/Service/Finding/Credential/NetworkSegment) with `EXPLOITS`, `SAME_SEGMENT`, `CONNECTS_TO`, `CREDENTIAL_REUSE`, optional Neo4j mirror. |
| `graph/analyzer.py` `PathAnalyzer` | Attacker **movement projection**, `find_paths_to_target` (simple paths), `score_path`, `identify_chokepoints`, `find_blast_radius`. Solid. |
| `routers/attack_paths.py` | `/attack-paths`, `/attack-paths/{id}`, `/chokepoints`, `/blast-radius/{asset}`, `/attack-graph` (D3). Persists `AttackPath` rows per engagement. |
| `models/attack_path.py` | `path_nodes`, `path_edges`, `risk_score`, `chokepoints`, FK to engagement. |
| `detection/attack_paths.py` | Per-**host** composite CORR-* findings (NTLM relay, legacy-Windows, cleartext cluster, DB-unauth, SNMP-lateral, + AD-exposure/mgmt-plane from the last PR). |
| `detection/attack_matrix.py` | ATT&CK tactic/technique roll-up (last PR). |
| `detection/vantage_fusion.py` + `exposure_fusion_service.py` | Fuse multi-probe `exposure_matrix` → `Service.exposure ∈ {external, internal_only, ambiguous, not_exposed}`. |

**The gap that makes multi-subnet paths not work today:**

1. **`GraphBuilder.build_from_db()` calls `build_asset_graph(...)` with NO
   `network_topology` and NO `credentials`.** So `add_network_edges` and
   `_add_credential_edges` **never run in production** → the movement graph has
   **zero lateral edges** → `find_paths_to_target` returns essentially nothing.
   The engine is wired to a reachability model that is never populated.
2. **No subnet model.** `Engagement.scope_cidrs` holds the subnets but nothing
   assigns assets to subnets or builds cross-subnet reachability. "Multiple
   subnets of the same org" is simply not represented.
3. **Only CVE-`exploitable` findings are attack steps.** Posture/IOA/misconfig
   findings (unauth DB, ADB shell, VNC-no-auth, IPMI cipher-0, RDP-no-NLA,
   SMB-signing-off, default SNMP…) — i.e. ~80% of what actually chains — carry
   `exploitable=false`, so they never create `EXPLOITS`/foothold edges.
4. **No credential/relay edges** derived from facts (shared local admins, reused
   SSH keys, NTLM-relay reachability, default SNMP on network gear).
5. **Entry points not derived** from fused exposure; `is_internet_exposed` only
   reads `asset.environment`/`tags`, which the detection path rarely sets.

So this is **~70% a wiring + derivation problem**, not a greenfield build. We feed
the existing graph engine a reachability/credential/foothold model derived from
facts the engine already has, and extend it for subnets and misconfig steps.

---

## 3. Design — deriving the model from facts (the core work)

New module **`app/detection/reachability.py`** (pure, deterministic, unit-testable;
no DB, no I/O — same discipline as `attack_paths.py`). It consumes the engagement's
assets, services (with fused `exposure`), findings, and `scope_cidrs`, and emits
the `network_topology` + `credentials` structures `GraphBuilder` already accepts,
plus a **foothold map** (asset → how an attacker first lands there).

### 3.1 Subnet model (multi-subnet, the headline ask)
- Build a **subnet node per `scope_cidrs` entry** (`subnet:<cidr>`); assign each
  asset to the most-specific containing CIDR by `ip_address` (stdlib `ipaddress`).
  Assets with no CIDR match → an `unscoped` bucket (visible, never dropped).
- **Intra-subnet reachability** = `SAME_SEGMENT` among a subnet's assets (the
  builder already supports segments). This is the safe, defensible default:
  hosts on one L2/L3 subnet generally reach each other.
- **Inter-subnet reachability** = `CONNECTS_TO`, **inferred and labelled**:
  - `observed` when a probe vantage actually saw the cross-subnet service open
    (from `exposure_matrix` / a probe sitting in subnet A seeing B's port).
  - `assumed` otherwise, with a **reachability confidence** and a configurable
    posture: default **flat-internal** (org subnets mutually reachable unless
    evidence of segmentation), with a **segmented** mode that only connects
    subnets through an observed **gateway** (`device_role = network_device`).
  - Every cross-subnet edge records `basis ∈ {observed, assumed}` so the UI/report
    can show "confirmed reachable" vs "assumed reachable (verify segmentation)".
- **Gateways/routers** (`device_role network_device`, or the `.1`/default-gateway
  heuristic) become explicit inter-subnet **pivot nodes** → natural choke points.

### 3.2 Entry points (path sources)
- **Internet → asset** edge where any `Service.exposure == external` (fleet-fused),
  or `asset.tags.internet_exposed`, or environment ∈ dmz/edge/perimeter.
- **Foothold findings** (initial access without prior position): unauth DB,
  ADB unauthenticated shell, VNC-no-auth, IPMI cipher-0, MQTT unauth, anonymous
  FTP/rsync/NFS, exposed container API, default-cred candidate, a validated-
  exploitable CVE. Each seeds the attacker at that asset with a technique + weight.

### 3.3 Compromise / movement semantics from findings (fix gap #3)
A **capability map** `rule_id / category → {capability, mitre, complexity}` where
capability ∈ `foothold | priv_esc | lateral | credential_access | recon`. Examples:
- `foothold`: unauth DB (T1190/T1213), ADB shell (T1021), VNC-no-auth (T1021.005),
  IPMI cipher-0 (T1078 → full OOB), exposed container (T1610), validated CVE.
- `lateral` / `credential_access`: SMB-signing-off → NTLM relay (T1557.001),
  default SNMP on network gear (T1602.001), LDAP anon (T1087.002), shared local
  admin (T1078), reused SSH key.
- `priv_esc`: unquoted service path (T1574.009), service binary in writable dir
  (T1543.003), AV disabled amplifies post-foothold success (T1562.001).
This makes misconfig/IOA findings real edges with honest weights, independent of
the CVE `exploitable` flag. Edge weight = exploit/complexity × state factor
(confirmed < suspected cost) so confirmed chains score above speculative ones.

### 3.4 Credential & relay edges (fix gap #4), cross-subnet by nature
Derive `credentials` + relay edges from facts already collected:
- **Shared local admin**: same non-builtin admin name across hosts
  (`windows_inventory.local_admins`) → `CREDENTIAL_REUSE` among them.
- **Reused SSH host/user keys**, identical service credentials where evidenced.
- **NTLM-relay reachability**: SMB-signing-off hosts are relay *targets* reachable
  from any coerce-capable host → relay edges (esp. to a DC → domain compromise).
- **Default SNMP community on network gear** → config/topology disclosure edge
  enabling lateral movement across subnets.
These are the edges that make a path cross subnet boundaries like a real attacker.

### 3.5 Crown jewels (path targets)
`criticality == critical`, or `role_detail ∈ {domain_controller, vmware_hypervisor}`,
or a database/datastore asset, or operator-tagged. If none tagged, fall back to the
highest-risk assets so a path set is still produced (and say so).

---

## 4. Generation pipeline (engagement-scoped, "choose the engagement")

```
choose engagement
  → load assets+services(exposure)+findings  (build_from_db, extended)
  → reachability.derive_topology(assets, services, scope_cidrs, posture)   # NEW
  → reachability.derive_credentials(findings, inventory facts)             # NEW
  → reachability.derive_footholds(findings, services)                      # NEW
  → GraphBuilder.build_asset_graph(..., network_topology, credentials)     # now populated
  → PathAnalyzer: sources = internet ∪ footholds; targets = crown jewels
      find_paths_to_target across ALL subnets  (existing)
  → score, prune dead-ends, identify_chokepoints (gateways + shared-cred hosts)
  → persist AttackPath rows (subnet-annotated hops, ATT&CK, observed/assumed)
  → attack_matrix roll-up for the report
```

Trigger: the existing `GET /attack-paths?refresh=true` path, **plus** recompute at
the end of a detection run in `engine_bridge` so paths are fresh after each scan
(best-effort, never sinks the run).

---

## 5. Scoring, pruning, honesty
- Keep/extend `PathAnalyzer.score_path`: CVSS/criticality along path, credential-
  reuse bonus, hop penalty, **crown-jewel-reachability** weighting (XM Cyber's
  core idea), and a **down-weight for `assumed` reachability** so observed chains
  rank first. **Confidence/state** of each finding flows in (confirmed > suspected).
- **Prune dead ends** (XM Cyber: ~74%): only persist paths that reach a crown
  jewel or materially increase blast radius.
- **Choke points**: already computed; add subnet gateways and shared-credential
  hosts as first-class choke candidates; remediation-priority ranking.
- **Every edge is explainable** (`evidence.correlated`, technique, basis
  observed/assumed, the finding ids it rests on) — no black-box hop. Reachability
  we could not confirm is labelled `assumed`, never asserted as fact.

## 6. Output / UX (multi-subnet view)
- `GET /engagements/{id}/attack-paths` — ranked cross-subnet paths (exists; now
  non-empty), each hop labelled with **source subnet → dest subnet**, technique,
  observed/assumed, finding refs.
- `GET /engagements/{id}/attack-graph` — D3 JSON **grouped by subnet** (cluster per
  CIDR, internet node, gateways between clusters) — the "multiple subnets of one
  org" picture the request asks for.
- `/chokepoints`, `/blast-radius/{asset}` — already there, now meaningful.
- Report + ATT&CK matrix integration.

## 7. Phasing (small, reviewable PRs; each green before the next)
- **P1 — subnet model + topology derivation** (`reachability.py` core): subnet
  nodes, intra-subnet edges, inter-subnet observed/assumed edges, gateways; wire
  into `build_from_db`. Pure-logic unit tests on fixtures. *Biggest single unlock —
  paths become non-empty across subnets.*
- **P2 — finding→capability map**: misconfig/IOA/posture findings as foothold/
  lateral/priv-esc edges with ATT&CK + state-weighted cost (fix gap #3).
- **P3 — credential & relay edges** (shared admin, NTLM relay, default SNMP,
  reused keys) — the cross-subnet movers (fix gap #4).
- **P4 — entry-point derivation** from fused exposure + footholds (fix gap #5);
  crown-jewel selection.
- **P5 — scoring/pruning/choke-point upgrades**, observed-vs-assumed weighting,
  recompute-after-scan hook, subnet-grouped D3 output + report wiring.

Each phase ships with unit tests (pure functions, fixture graphs) and keeps the
backend detection suite green; no probe changes (detection stays on the manager).

## 8. Risks / decisions to confirm with you
1. **Default reachability posture**: flat-internal (assume org subnets mutually
   reachable, mark `assumed`) vs segmented-by-default (only via observed gateways).
   Flat-internal finds more paths (pen-tester default); segmented is more
   conservative. **Recommend flat-internal default, operator-togglable per
   engagement**, with every assumed edge clearly labelled.
2. **Crown-jewel definition** when nothing is tagged critical (fall back to role/
   risk, or require the operator to pick targets?).
3. **Scale**: in-memory networkx is fine to low-thousands of assets/engagement;
   Neo4j mirror already exists for larger. Confirm expected max engagement size.
4. Keep this engagement-scoped (one tenant's engagement). "Same org, multiple
   subnets" = the subnets in that engagement's `scope_cidrs`. Cross-engagement
   correlation is out of scope unless you want it.

---

### Sources
- MulVAL: <https://www.cs.princeton.edu/~appel/papers/mulval.pdf>, USENIX'05
  <https://static.usenix.org/event/sec05/tech/full_papers/ou/ou_html/index.html>
- Attack-graph survey: <https://onlinelibrary.wiley.com/doi/10.1155/2019/2031063>,
  <https://arxiv.org/pdf/2302.14479>; node-aggregation
  <https://dl.acm.org/doi/full/10.1145/3723890.3723912>
- BloodHound: <https://specterops.io/bloodhound-community-edition/>,
  <https://www.wiz.io/academy/bloodhound-overview>
- XM Cyber choke points / exposure stats:
  <https://thehackernews.com/2024/05/new-xm-cyber-research-80-of-exposures.html>,
  <https://xmcyber.com/platform/external-attack-surface-management/>
- Attack path management: <https://en.wikipedia.org/wiki/Attack_path_management>
