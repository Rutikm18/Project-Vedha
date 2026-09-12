# Node Description Batch 5 of 380

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commit:repo:github.com/Rutikm18/Project-Vedha@3c9062a2ad7bbd5d67a2343aa035a835d02e3818": "3c9062a refactor: Update dashboard components for improved styling and function…" | kind=Commit | source=git | neighbors=[page.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c52feb410341da146973ec21b59b90f8985b8c73": "c52feb4 feat(portal): reskin User Portal to console theme + comprehensive dashb…" | kind=Commit | source=git | neighbors=[35f02a9 feat(portal): rich scan request…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fd5dc9658c8f71049864680b5317900dde34f0eb": "fd5dc96 feat(remediation): AI + deterministic-KB per-finding remediation plans" | kind=Commit | source=git | neighbors=[54503ae feat(scanner): SYN path harvest…, llm_report.py, main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity]
- "detection_engine_posture_rules_d": "_d()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L244 | neighbors=[posture_rules.py, _cert(), _db_auth(), _db_cleartext_transport(), _db_unauthenticated(), _default_cred_candidate()]
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[5c59db1 Implement instance locking mech…, 9c54022 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, AttackNarrativeOut, buildReportUserMessage()]
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[engine.py, 09c6c0a feat(probe): per-host wall-cloc…, 198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2c53ae9 evasion(scanner): randomized sc…]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, .setup_method(), .test_compute_coverage(), .test_coverage_empty(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking()]
- "workflow_gates": "gates.py" | kind=code-symbol | source=probe/workflow/gates.py:L1 | neighbors=[explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, 64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c4386e4cbc0ee346a71c211a96326772b677c561": "c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug" | kind=Commit | source=git | neighbors=[ae08d19 feat(scanner): adaptive timeout…, main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[audit_log.py, Base, Immutable, append-only audit trail for …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[base.py, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L15 | neighbors=[enums.py, str, Operator-set lifecycle. `ongoing` (asse…, Engagement, EngagementUpdate, Re-runs the detection pipeline against …]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[exploit_approval.py, str, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, 95904f1 feat(probe): detect SMB signing…]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx]
- "tests_test_campaign_progress": "test_campaign_progress.py" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L1 | neighbors=[25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _beat()]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, Raised when an LDAP/Kerberos/SMB connec…, FindingSeverity, FindingStatus, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, Raised when an optional offensive depen…, FindingSeverity, FindingStatus, ACE]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10ceacaffacf60f95eeb0e9b2b247b62bfa5dfb8": "10ceaca feat: implement AI model fallback mechanism and enhance model selection…" | kind=Commit | source=git | neighbors=[AssistantDrawer.tsx, ModelSwitcher.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer]
- "commit:repo:github.com/Rutikm18/Project-Vedha@8ebc0534dda8a1316f41c2fccf928f42acf9ed46": "8ebc053 feat(risk-rank-ui): surface verification + lifecycle state on findings …" | kind=Commit | source=git | neighbors=[6a1c958 docs(plans): record execution s…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "id_campaignprogress": "CampaignProgress.tsx" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/CampaignProgress.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 198bae4 snapshot: uncommitted system/ui…, 25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[AssistantDrawer.tsx, EngagementStatusControl.tsx, page.tsx, aibrain-workspace-api.ts, campaign-workspace-api.ts, console-source.tsx]
- "tests_test_va_campaign": "test_va_campaign.py" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, scanner_base.py, va_campaign.py, _Buf, _detect_stage()]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@01f43989ed63ef32dcf3abe8b305659ff281c464": "01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint)" | kind=Commit | source=git | neighbors=[use_cases.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@50d65540db573b6b680c257d3d693b216940069f": "50d6554 feat(active-validation): approve→enqueue endpoint + result ingestion (P…" | kind=Commit | source=git | neighbors=[3c277ba feat(lifecycle): add POST /find…, main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer]
- "commit:repo:github.com/Rutikm18/Project-Vedha@75650c143e0e92e93ca7fed76c46893953456bf8": "75650c1 feat: add Posture & Patch-Comparison Scorecard design spec" | kind=Commit | source=git | neighbors=[agent.py, config.py, ModelSwitcher.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cdee859546b57100944ef98e4f180fc049700dbe": "cdee859 feat(probe): add container/cloud/infra ports to IT catalog" | kind=Commit | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]
- "routers_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1727f4f feat(findings): MTTR + open-by-…, 1fe16c8 stable but some dead code, need…, 3c277ba feat(lifecycle): add POST /find…, 3ddc104 feat: unify customer and manage…, 3e6b187 feat: unify customer and manage…]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L706 | neighbors=[test_detection_core.py, .test_ai_cap_at_60(), .test_ai_no_cap_if_already_below(), .test_auth_enforced_penalty(), .test_authoritative_tier_base_95(), .test_backport_penalty()]
- "tests_test_probe_next_features": "test_probe_next_features.py" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, engine.py, use_cases.py, scanner_base.py, _cache_with(), test_device_inventory_post_stage_classi…]
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 6bb51ab feat: add detection-explain end…, 6be8259 feat(integrations): outbox deli…, 81c81cb feat: implement outbox reclaim …, 8f6bf49 Refactor code structure and rem…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-004.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
