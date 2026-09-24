# Plan — tags → domain AI → BFSI deployment

Spec: `docs/superpowers/specs/2026-09-24-intel-tags-domain-ai-bfsi-design.md`
Rule: every task is small, test-first, and independently mergeable. P0 = foundation
others depend on; P1 = customer-visible value; P2 = hardening/scale.

## Phase 1 — Asset tags (foundation)
| # | Pri | Task | Done when |
|---|---|---|---|
| T1 ✅ | P0 | `app/intel/tagging.py`: Tag dataclass, `AssetFacts`, rule registry, `derive_tags` | unit tests green |
| T2 ✅ | P0 | Rules: host_type, os_family, role (service→role catalog), exposure, zone, domain | table tests per rule |
| T3 ✅ | P0 | BFSI `sector_fn` signatures + `compliance_scope` + `data_sensitivity` derivation | tests incl. "no evidence → no tag" |
| T4 ✅ | P0 | `merge_tags(existing, auto)` keeps manual tags; hook into `_promote_assets` (zero extra queries) | promote test asserts tags |
| T5 ✅ | P1 | Asset API: tags in response, `?tag=` filter, `PUT /assets/{id}/tags` (audited), `POST /engagements/{id}/assets/retag` | router tests |
| T6 ✅ | P1 | Frontend: tag chips on assets/findings, tag filter | UI check |
| T7 | P2 | Migration: GIN index on `assets.tags` | alembic up/down |
| T8 ✅ | P1 | Fragile-asset guard: `sector_fn:hsm/atm/swift`, `role:ics` → non-intrusive only unless approved | policy tests |

## Phase 2 — Domain-expert AI + compliance
| # | Pri | Task | Done when |
|---|---|---|---|
| A1 ✅ | P0 | Engagement profile (sector, jurisdictions) in ROE JSONB + schema validation + API | tests |
| A2 ✅ | P0 | Compliance pack registry (`app/compliance/packs`): framework metadata, jurisdictions, reporting clocks | schema test |
| A3 ✅ | P0 | Region packs: India (RBI, SEBI CSCRF, CERT-In, DPDP, IRDAI) | category→control tests |
| A4 ✅ | P1 | Region packs: EU/UK (GDPR, DORA, NIS2, FCA/PRA), ME/APAC (SAMA, CBUAE, MAS TRM, HKMA), US (NYDFS, GLBA — FFIEC CAT dropped: sunset 2025), SWIFT CSCF | tests |
| A5 ✅ | P0 | `applicable_frameworks(profile, tags)` + `finding_obligations(finding, profile)` | tests |
| A6 ✅ | P0 | Domain skills (`app/ai/skills`): banking, payments_fintech, insurance, capital_markets, nbfc, healthcare, government, generic | schema test |
| A7 ✅ | P0 | Skill router + prompt composer (persona + vocabulary + pack excerpt) into `ManagerLlmService._build_system` | tests; existing AI tests still green |
| A8 ◐ | P1 | Sector-aware `client_assistant` + `/ai/generate` ✅; deterministic `/findings/{id}/obligations` ✅; LLM `compliance_brief` task — open | router tests |
| A9 | P1 | Grounding check: unknown control IDs flagged/stripped | tests |
| A10 ✅ | P1 | Frontend: profile editor, compliance-by-framework view, assistant shows skill + jurisdiction | UI check |

## Phase 3 — AI Gateway + BFSI deployment
| # | Pri | Task | Done when |
|---|---|---|---|
| G1 ✅ | P0 | `app/ai/gateway.py` pseudonymizer (IP/host/FQDN/email/user/domain) + rehydrate | round-trip tests |
| G2 ✅ | P0 | `VEDHA_DEPLOYMENT_PROFILE` (sovereign/hybrid/cloud) + route policy; wire into `_dispatch` | "no raw IP reaches transport" test |
| G3 | P1 | Hash-chained AI audit record | tests |
| G4 ✅ | P1 | ADR-0003 BFSI deployment + deployment guide (agent zoning, mTLS, CMK, retention, change windows) | doc review |
| G5 | P2 | Offline signed intel bundle (export/import, Ed25519) for sovereign | tests |
| G6 | P2 | Sovereign local-model profile hardening (vLLM/Ollama, no cloud fallback) | tests |

## Build order
T1→T2→T3→T4 → A1→A2→A3→A5→A6→A7 → G1→G2 → T5 → A8→A9 → A4 → G3→G4 → rest.

## Status (2026-09-24)
Done ✅: backend for tags, compliance packs (all 4 regions), domain skills + brief, AI gateway, ADR-0003.
Frontend (T6/A10) ✅ and fragile-asset guard (T8) ✅ — enforced at operator enqueue (incl. schedules), portal-approved scans (no override), Nuclei and Nessus; admin/manager override needs a reason and is audited.
Next: A9 citation grounding check, G3 AI audit chain, findings-drawer obligations UI, LLM compliance_brief task.
