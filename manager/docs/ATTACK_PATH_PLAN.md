# Engagement-wide, multi-subnet attack-path generation — plan (for review)

Status (2026-10-08): **P0, P1a, P1b, P4a and P5 implemented.** P2, P3 and P4b are **not implemented**
(see §7). Decisions: §8 recommendations accepted (flat-internal labelled `assumed`, engagement-scoped,
(site, IP) identity). Operator-defined crown jewels remain the only path targets.
Revised 2026-10-06 with a failure-mode analysis (§9): 32 failure modes found,
4 of which make the feature silently empty in production today. Phasing (§7)
now starts with a **P0 engine-correctness** phase.

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
  - `observed` when there is real evidence that subnet A reaches subnet B. NOTE
    (P1a finding): a probe that reaches both A and B is **not** such evidence —
    scanners are routinely firewall-whitelisted, and `Agent.network_segments` is
    the probe's declared dispatch scope, not where it sits. P1a therefore emits
    no `observed` inter-subnet links; only `same_subnet` and `assumed`.
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

## 7. Phasing — REVISED after the failure-mode analysis (§9)

The failure-mode analysis showed the existing engine has correctness defects that
would corrupt any path built on top of it, and that the original P1 design (pairwise
`SAME_SEGMENT` mesh + `all_simple_paths`) cannot scale past ~11 hosts per subnet.
So a **P0 correctness phase** now comes first, and P1/P5 designs changed.

| Phase | Delivers | Fixes failure modes (§9) |
|---|---|---|
| **P0 — engine correctness** ✅ done | Filter findings to live statuses; **monotonic compromise** (pivot only FROM a compromised node); replace `all_simple_paths` with **Yen k-shortest / Dijkstra**; **multiplicative likelihood** scoring; stable path IDs (upsert by deterministic hash, `refresh=False` default); **explain-empty** result; drop/scope dead Neo4j Cypher. | FM-04, 07, 10, 11, 12, 13, 17, 18, 19, 22, 23 |
| **P1a — subnet model + topology** ✅ done | `app/detection/reachability.py`: subnet per scope CIDR (/24 or /64 buckets for broad scopes, marked `inferred`); subnet **hub** nodes (O(n) edges); inter-subnet links `assumed` (flat posture) or only via a compromised gateway (segmented, `rules_of_engagement.attack_path_reachability`); hops count hosts; each hop carries `via` subnets, `basis`, likelihood. Wired into `build_from_db`. | FM-01, 11, 21 |
| **P1b — site-aware identity** ✅ done | `(site, ip)` asset identity (migration + the 5 asset-creation paths), multi-NIC linking, stale-asset ageing. Split out of P1: it changes asset identity across discovery, job results, findings and two routers, so it gets its own review. | FM-14, 15, 16 |
| **P2 — finding→capability map** ⛔ not implemented | Posture/IOA/misconfig findings as foothold/lateral/priv-esc steps with ATT&CK + per-step success likelihood (confidence × EPSS/KEV × state). | FM-03, 05, 06 |
| **P3 — credential & relay edges** ⛔ not implemented | Relay edges with **full precondition checks** (target signing off + coercion source + protocol); shared-admin edges **only when LAPS absent**, labelled `possible`. | FM-08, 09 |
| **P4a — internet entry points** ✅ done | Assets with a service the fleet-fused exposure verdict marks `external` become entry candidates (`exposure_basis`, `exposed_ports` recorded). An entry point must ALSO carry an existing exploitable finding — exposure is reachability, not compromise. `diagnose` separates "nothing exposed" from "exposed but not compromisable". | FM-02 |
| **P4b — crown-jewel selection** ⛔ not implemented | Not implemented. Targets remain operator-defined (`criticality=critical`); without them the result is empty and `why_empty` reports `no_targets`. | FM-04 |
| **P5 — choke points, output, validation** ✅ done | **Min-cut / betweenness** choke points (not path-frequency); subnet-grouped D3; recompute-after-scan (async, not on GET); **validation harness** with ground-truth fixtures + cascade-failure path validity metric. | FM-24, 25, 26 |

### 7.1 What P1b and P5 delivered (and what they do not claim)

**P1b — site-aware identity.** `rules_of_engagement.asset_identity` is `global` (default, the old
behaviour) or `per_site`. Under `per_site` only a **non-globally-routable** address is partitioned by probe
site, so two sites' `10.0.0.5` are two hosts while a public address stays one host everywhere. One
resolver (`pick_asset` / `find_asset` / `resolve_asset`) serves every asset-creation path, and legacy rows
with no site are adopted on first sight. Exposure fusion runs per asset scope, so one site's exposure is
never stamped on another site's machine. In the graph, subnets are keyed `{cidr}@{site}`; links between two
sites' private networks are `assumed_cross_site` (confidence 0.3) and a gateway never routes into another
site's private network. A machine seen on several addresses is linked by `SAME_HOST` only on a conservative
match (FQDN 0.9, short name 0.7; capped at 4 NICs) and never merged. Hosts not seen within
`rules_of_engagement.attack_path_freshness_days` (default 30; `0` disables) halve their step likelihood and
mark the hop and path `stale`. `GET /engagements/{id}/asset-identity` reports the evidence for choosing a
mode: sites with overlapping private ranges, private IPs that different sites report under different host
names, addresses that already map to more than one asset, machines seen at several addresses, and stale
assets. Migration `0055`.

**P5 — choke points, output, validation.**
- *Choke points* are ranked by **risk removed if that one host were fixed** (best remaining path, not a
  sum), not by how often a host appears in a truncated path list. A separate **minimum vertex cut**
  (max-flow with vertex splitting; entry hosts cost slightly more than shared infrastructure so a tie goes
  to the shared host) gives the smallest set whose fix disconnects every target, with the number of
  vertex-disjoint routes (Menger) as the evidence that one fix is or is not enough.
- *Stored once per engagement* in `attack_path_analyses` (migration `0056`), read by `GET .../chokepoints`
  and `GET .../attack-path-analysis`; per-path rows keep only the choke points that are on that path.
- *Coverage and freshness* are reported alongside every analysis: hosts observed and stale hosts per subnet,
  scope CIDRs with no observed host, hosts observed outside scope, hosts with no subnet. Coverage is
  `partial` or `observed`, never "complete" — the scanned address space itself is not tracked, so a subnet
  with no path may simply be one nobody scanned.
- *Subnet-grouped D3 output* (`groups`, node `site`/`stale`, edge `basis`).
- *Validation harness* (`python -m app.graph.validation tests/fixtures/attack_paths`): nine hand-built
  networks with their true paths written down, scored for recall, forbidden hops, unreachable targets,
  freshness, independent routes, minimum fix set, top choke point, and a **cascade validity** metric (a path
  is credited only up to its first invalid hop). The harness is tested against deliberately wrong fixtures.
- *Recompute after detection*: a detection run that created or resolved findings refreshes the stored paths
  and analysis (in a savepoint, only for engagements that already have stored results; failures never fail
  the run). Reading still never recomputes.
- *Neo4j mirror hygiene* (FM-28/29): `:GraphNode(engagement_id, type)` and `(engagement_id, key)` indexes,
  per-engagement atomic replace, node identity `(engagement_id, key)`, parallel edges kept distinct.

**Limits that still apply.**
- Likelihoods and link confidences are **ordering weights, not measured probabilities**; they rank paths and
  say which assumptions a path rests on. They are not a prediction that an attack would succeed.
- Reachability between subnets is **inferred** (no firewall rules are read) and labelled `assumed`.
- The validation fixtures are hand-written, so they show the model is internally consistent and regresses
  loudly; they do not measure accuracy on real networks. Only an engagement with a known ground truth can.
- Migrations `0055` and `0056` and the Neo4j statements have been exercised against fakes and static checks,
  **not against a live PostgreSQL or Neo4j**. The Neo4j mirror is not wired into the product by default
  (`neo4j_enabled` is off and nothing reads it); P5 only makes it correct if enabled.
- P2, P3 and P4b are not built, so only findings already marked exploitable create attacker steps, relay and
  shared-credential edges beyond what the AD modules emit do not exist, and targets are chosen by the operator.

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
5. **NEW (from §9):** two sites of one org can both use `10.0.0.0/24`. Should
   asset identity become **(probe site, IP)**? Recommend **yes** — without it,
   distinct hosts merge and paths cross sites that are not connected (FM-14).

---

## 9. Failure-mode analysis (FMEA) — accuracy and other areas

Method: read every component the plan builds on, then **reproduce** the suspected
defects against the real code (`manager/backend/scripts/attack_path_fm_probe.py` drives the actual
`PathAnalyzer`), and cross-check against published attack-graph research and
vendor documentation. Evidence column cites `file:line` (relative to
`manager/backend/app/`) or a measurement. "Phase" = where the mitigation lands (§7).

### 9.0 Headline — the feature is silently empty in production today

Four **independent** conditions each produce zero attack paths on a normal
network-VA engagement. Any one is sufficient; all four hold today. And an empty
result is **indistinguishable from "no attack paths exist"** — the exact
silent-false-clean class the detection engine fights everywhere else.

| # | Condition | Evidence | Consequence |
|---|---|---|---|
| FM-01 | No lateral edges: topology/credentials never passed to the builder | `graph/builder.py:287` calls `build_asset_graph(...)` without `network_topology`/`credentials` | Movement graph has no `SAME_SEGMENT`/`CONNECTS_TO`/`CREDENTIAL_REUSE` edges |
| FM-02 | No sources: entry points read fields nothing sets | `is_internet_exposed` (`graph/builder.py:83`) reads `asset.environment` / `tags.internet_exposed`; **no production code sets either**. The real signal, `Service.exposure=="external"`, **is** stamped (`services/job_result_service.py:796`, `exposure_fusion_service`) but unread | `_source_assets("internet_exposed")` returns `[]` |
| FM-03 | No exploit steps: only `Finding.exploitable` creates `EXPLOITS` edges | `exploitable=True` is set **only** in `ad/*.py` (AD modules) — never by the network-VA detection path | Every hop is `dest_compromisable=False` |
| FM-04 | No targets: crown jewels require `criticality=critical`, nothing assigns it | `routers/attack_paths.py:181-185`; no code sets `Asset.criticality` beyond the default `medium` | `_all_paths_to_critical([])` → `[]` |

### 9.1 Accuracy — false-POSITIVE paths (paths that are not real)

| ID | Failure mode | Evidence / cause | Impact | Mitigation | Phase |
|---|---|---|---|---|---|
| FM-05 | **Pass-through pivot**: path continues *from* a host the attacker never compromised | `graph/analyzer.py:118` adds a movement edge even when `dest_compromisable=False`; reproduced: path `A→B→C` where B has no exploit | Fabricated chains; violates MulVAL's **monotonic privilege** model (you only act from privileges you hold) | Pivot only from compromised states; model `(host, privilege)` state nodes | P0 |
| FM-06 | Resolved / accepted / false-positive findings still form steps | `graph/builder.py:280` loads **all** findings, no status filter | Paths built on already-fixed weaknesses | Filter to live statuses (open/confirmed); weight `suspected` lower | P0 |
| FM-07 | CVE false positives propagate into steps | Banner-inferred CVEs are `suspected, backport-possible` (verifier); any step built on them inherits the FP | Distro-backported hosts shown as exploitable pivots | Step likelihood = finding confidence × EPSS/KEV; never treat `suspected` as certain | P2 |
| FM-08 | **Shared-admin ≠ shared-password** | Same local-admin *name* on many hosts says nothing if **LAPS** randomises each password | False `CREDENTIAL_REUSE` edges across every Windows host | Emit only when LAPS absent; label `possible`, never `observed` | P3 |
| FM-09 | **Relay edges without preconditions** | NTLM relay needs: target signing not required **and** a coercion/poisoning source **and** a protocol that accepts it (LDAP signing / channel binding / EPA off). Signing-off alone is not a path; reflection to the same host is blocked | Over-connected relay edges, especially to DCs | Check each precondition from facts; missing evidence → edge `assumed` with low likelihood | P3 |
| FM-10 | Honeypot / deception hosts become juicy pivots | Deception host advertises many vulns (verifier already scores `deception`) | Paths route through a decoy | Down-weight or exclude assets with high deception score | P0/P2 |
| FM-11 | Flat-internal assumption over-connects segmented networks | No firewall ACLs available; default assumes subnets reach each other | Paths across a real firewall | Label `assumed`, down-weight, show "verify segmentation"; segmented mode toggle | P1 |

### 9.2 Accuracy — false-NEGATIVE paths (real paths missed)

| ID | Failure mode | Evidence / cause | Impact | Mitigation | Phase |
|---|---|---|---|---|---|
| FM-12 | Misconfig/posture findings are not steps at all | FM-03; XM Cyber: **~80% of real exposures are misconfig/identity, <1% CVEs** | The majority of real chains are invisible | Capability map (§3.3) independent of `exploitable` | P2 |
| FM-13 | Unscanned hosts / partial coverage | A host missed by the scan has no node; a path through it cannot exist | Under-reports reachability; "clean" overstated | Coverage annotation per subnet (scan_summary completeness); flag paths that end at coverage gaps | P5 |
| FM-14 | **Overlapping RFC1918 across sites** collapse into one asset | Identity = `(engagement, ip)` (`discovery/finding_translator.py:73`). Agents carry `site_id` and two sites may both use `10.0.0.0/24` | Two real hosts merge: false edges across unconnected sites *and* missed paths | Identity `(site, ip)` via `ScanResult.agent_id → Agent.site_id` (Rapid7/Tenable "asset linking" practice) | P1 |
| FM-15 | **Multi-homed** hosts appear as two assets | One host, two NICs/IPs, no merge (hostname/MAC/NTLM name not used to link) | Misses the most important cross-subnet pivot: the dual-homed host | Link assets by stable identifiers (MAC, NetBIOS/NTLM target name, cert SAN) | P1 |
| FM-16 | DHCP churn / stale assets | Asset by IP; a re-leased IP inherits old findings | Wrong host attributed to a step | Use `last_seen`; age out stale assets; prefer MAC-linked identity | P1 |

### 9.3 Scoring & prioritisation

| ID | Failure mode | Evidence | Impact | Mitigation | Phase |
|---|---|---|---|---|---|
| FM-17 | **Longer paths score higher** | `graph/analyzer.py:210-211` adds `2×CVSS` per hop, subtracts `1.5` per hop. Measured: 4-hop CVSS 7.0 chain = **50.0**; 1-hop CVSS 9.8 = **18.1** | Ranking inverted: a long, unlikely chain outranks a one-step critical | Multiplicative likelihood `Π p(step)` (0.98 vs 0.24 in the same case) × target impact | P0 |
| FM-18 | **CVSS used as probability** | FIRST: *"CVSS measures severity, not risk"*; EPSS measures exploitation probability | Mis-calibrated step costs | Step likelihood from EPSS/KEV + finding confidence + state; CVSS only for impact | P0/P2 |
| FM-19 | Misconfig-only paths score **0** | Posture findings carry no CVSS → measured `score_path = 0.0` | Real misconfig chains ranked last or hidden | Capability-based likelihood per step (FM-12) | P0/P2 |
| FM-20 | Path dependence ignored (shared steps) | NIST metric-aggregation work: paths **rarely independent**, they share exploits; naive OR/AND of path probabilities distorts results. Cyclic Bayesian graphs break standard inference | Over-/under-stated aggregate host risk | Report per-path likelihood; aggregate per target with shared-step-aware min-cut, not naive sum | P5 |

### 9.4 Scale & performance

| ID | Failure mode | Evidence | Impact | Mitigation | Phase |
|---|---|---|---|---|---|
| FM-21 | **Path explosion** with `all_simple_paths` | Measured on a flat subnet mesh: 8 hosts → 1,957 paths; 10 → 109,601 (0.8s); **11 → 986,410 (7.1s)**, ~9× per host. A /24 (200 hosts) → 39,800 pairwise edges, infeasible. Same lesson as state explosion (Sheyner) and NetSPA (original version: ~17 machines) | Request hangs; worker timeout | **Yen k-shortest** (`shortest_simple_paths`, measured 0.001s on 60 nodes); subnet **hub** nodes O(n) not O(n²); logical graph (Ou CCS'06, polynomial) | P0/P1 |
| FM-22 | Recompute on **every GET** | `routers/attack_paths.py:46` `refresh=True` default | Heavy compute on the read path | Compute async after detection run; GET reads stored result | P0/P5 |
| FM-23 | Enumerate-then-truncate | `graph/analyzer.py:161-169` enumerates **all** paths then keeps 5 | Cost paid before the cut | Generator-based k-shortest stops at k | P0 |

### 9.5 Consistency, staleness, security, explainability

| ID | Failure mode | Evidence | Impact | Mitigation | Phase |
|---|---|---|---|---|---|
| FM-24 | **Path IDs churn**; concurrent GETs race | `routers/attack_paths.py:212` deletes all paths then re-inserts | A shared `/attack-paths/{id}` link 404s after the next list call; two concurrent refreshes interleave delete/insert | Deterministic path ID = hash(node sequence); upsert; engagement-level lock (as `engine_bridge` already does for detection) | P0 |
| FM-25 | Choke points = path-frequency over a truncated set | `graph/analyzer.py:218-243`: share of the (≤5-per-source) enumerated paths, threshold 0.5 | Biased by enumeration order and dense subnets; can miss the true bottleneck | **Minimum s–t cut** / betweenness on the movement graph (min-cost hardening literature) | P5 |
| FM-26 | Chokepoint list stored on **every** path | `routers/attack_paths.py:219` writes all choke ids to each row | Misleading per-path data | Store engagement-level choke set separately | P5 |
| FM-27 | **Cypher queries have no engagement/tenant filter** | `graph/analyzer.py` `CYPHER_*` match any `internet_exposed` node; unused today, a latent cross-tenant leak if wired to a shared Neo4j | Data from other tenants in results | Remove or add `engagement_id` filter + test before any use | P0 |
| FM-28 | Neo4j indexes on a label never written | `graph/neo4j_client.py:41-44` index `:Asset`/`:Finding`; sync writes `:GraphNode` (`graph/builder.py:307`) | Full scans at scale | Index `:GraphNode(engagement_id, type)` | P5 |
| FM-29 | Neo4j never deletes stale nodes; parallel edges collapse | Sync only `MERGE`s; edges `MERGE` on `(a,b,type)` | Fixed weaknesses linger in the mirror; distinct edges merge | Per-engagement delete-then-write in a transaction | P5 |
| FM-30 | **No explanation for an empty result** | Router returns `{"total": 0}` with no reason | Operator cannot tell "safe" from "not computed" (FM-01..04) | Return `why_empty`: missing sources / targets / topology / coverage gaps, mirroring posture trace verdicts | P0 |
| FM-31 | No ground truth to measure accuracy | No fixture or rig asserts expected paths. Research: LLM-generated attack graphs showed up to **83.9% noise paths**; node-counting metrics miss structural errors | Regressions invisible | Validation harness: labelled topology fixtures with expected paths; **cascade-failure** validity metric (a path is valid only up to its first invalid step) | P5 |
| FM-32 | Data staleness across subnets | Findings from scans at different times are mixed into one graph | A path mixes a fixed host (scanned yesterday) with today's state | Carry `last_seen`; flag steps older than the engagement's freshness window | P5 |

### 9.6 What this changes in the design

1. **P0 is mandatory** before any new edges: building multi-subnet topology on the
   current analyzer would multiply FM-05/17/21 rather than fix the feature.
2. **Hub, not mesh**: subnets as hub nodes keep the graph O(n); pairwise
   `SAME_SEGMENT` (what `add_network_edges` does today) is O(n²) and explodes.
3. **State-based, monotonic model** (MulVAL): nodes are `(host, privilege)`; an
   edge exists only from a privilege the attacker already holds.
4. **Likelihood, not CVSS sum**: per-step success = finding confidence × exploit
   evidence (KEV/EPSS) × reachability basis (`observed` > `assumed`); path =
   product; rank by likelihood × crown-jewel impact.
5. **Identity = (site, IP)** with linking on MAC / NTLM target name / cert SAN.
6. **Every edge carries basis + preconditions** (`observed` / `assumed` /
   `possible`), and every empty result carries `why_empty`.

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

**Failure-mode research (§9)**
- Scalable logical attack graphs, polynomial size, monotonicity (Ou et al., CCS'06):
  <https://cse.usf.edu/~xou/publications/ccs06.pdf>; MulVAL extensions survey
  <https://arxiv.org/pdf/2208.05750>; state explosion in scenario graphs
  <https://onlinelibrary.wiley.com/doi/10.1155/2014/818957>
- NetSPA (MIT Lincoln Lab), reachability through firewall rules, early scale limit:
  <https://news.mit.edu/2008/security-0827>
- CVSS measures severity, not risk; EPSS: <https://arxiv.org/pdf/1908.04856>,
  <https://brandefense.io/blog/why-cvss-scores-are-lying-to-your-security-team/>
- Bayesian attack graphs, cycles and the independence assumption:
  <https://arxiv.org/pdf/2005.06350>, NIST metric aggregation
  <https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=926022>,
  approximate inference <https://arxiv.org/pdf/1606.07025>
- Min-cut / betweenness for hardening and choke points:
  <https://www.pnnl.gov/publications/minimizing-expected-maximum-risk-cyber-attacks-probabilistic-attack-success>,
  <https://www.dline.info/jisr/fulltext/v4n1/3.pdf>
- BloodHound data staleness / collection limits:
  <https://thehacker.recipes/ad/recon/bloodhound/>,
  <https://blog.compass-security.com/author/sdefatsc>
- Asset identity across sites with overlapping IP ranges:
  <https://docs.rapid7.com/insightvm/linking-assets-across-sites/>,
  <https://docs.tenable.com/exposure-management/Content/getting-started/asset-deduping.htm>,
  multi-NIC <https://docs.rapid7.com/nexpose/enhanced-vulnerability-detection-for-multinic-assets/>
- LAPS and shared local-admin credentials:
  <https://www2.paloaltonetworks.com/cyberpedia/what-are-shared-local-admin-credentials>
- NTLM relay preconditions (signing, LDAP channel binding, EPA):
  <https://legacy.thehacker.recipes/a-d/movement/ntlm/relay>,
  <https://tesseract.academy/how-to-defend-against-ntlm-relay-attacks-in-active-directory/>
- Attack-graph validation: noise paths (GARAGE) <https://arxiv.org/pdf/2607.18108>;
  cascade-failure path validity <https://arxiv.org/pdf/2609.07344>
- Microsoft Security Exposure Management (paths incomplete if critical assets are
  not defined): <https://learn.microsoft.com/en-us/security-exposure-management/review-attack-paths>

Measurements in §9 were reproduced with `manager/backend/scripts/attack_path_fm_probe.py` against the real
`app/graph/analyzer.py` (networkx), 2026-10-06.
