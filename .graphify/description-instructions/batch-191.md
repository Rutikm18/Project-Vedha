# Node Description Batch 192 of 336

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L49 | neighbors=[Sidebar.tsx] | lang=en
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx] | lang=en
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx] | lang=en
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx] | lang=en
- "components_themeprovider_themecontextvalue": "ThemeContextValue" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L14 | neighbors=[ThemeProvider.tsx] | lang=en
- "components_toastprovider_toast": "Toast" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L8 | neighbors=[ToastProvider.tsx] | lang=en
- "components_toastprovider_toast_styles": "TOAST_STYLES" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L35 | neighbors=[ToastProvider.tsx] | lang=en
- "components_toastprovider_toastcontextvalue": "ToastContextValue" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L17 | neighbors=[ToastProvider.tsx] | lang=en
- "components_toastprovider_toastitem": "ToastItem()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L69 | neighbors=[ToastProvider.tsx] | lang=en
- "components_toastprovider_toasttype": "ToastType" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L6 | neighbors=[ToastProvider.tsx] | lang=en
- "customer_access_page_ca": "ca()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L10 | neighbors=[page.tsx] | lang=en
- "customer_access_page_clientuser": "ClientUser" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "customer_access_page_customeraccesspage": "CustomerAccessPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L27 | neighbors=[page.tsx] | lang=en
- "customer_access_page_scanreq": "ScanReq" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L21 | neighbors=[page.tsx] | lang=en
- "customers_page_clientuserresp": "ClientUserResp" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L20 | neighbors=[page.tsx] | lang=en
- "customers_page_customer": "Customer" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L10 | neighbors=[page.tsx] | lang=en
- "customers_page_customerspage": "CustomersPage()" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L36 | neighbors=[page.tsx] | lang=en
- "customers_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L19 | neighbors=[page.tsx] | lang=en
- "customers_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "customers_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L10 | neighbors=[route.ts] | lang=en
- "cve_cli_cmd_ingest": "cmd_ingest()" | kind=code-symbol | source=probe/cve/cli.py:L44 | neighbors=[cli.py] | lang=en
- "cve_cli_rationale_1": "cli.py — the two operator verbs for the offline CVE layer.      python -m cve.cl" | kind=entity | source=probe/cve/cli.py:L1 | neighbors=[cli.py] | lang=en
- "cve_cli_rationale_120": "Verify the offline mirror: feed counts, freshness, and — critically — whether" | kind=entity | source=probe/cve/cli.py:L120 | neighbors=[cmd_status()] | lang=en
- "cve_cli_rationale_27": "Yield fact dicts from a JSONL file ('-' = stdin). Blank/comment/bad lines     ar" | kind=entity | source=probe/cve/cli.py:L27 | neighbors=[_read_facts()] | lang=en
- "cve_cli_rationale_66": "Merge CVE-finding lists, dedup by (cve_id, target, port), highest risk first." | kind=entity | source=probe/cve/cli.py:L66 | neighbors=[_merge_findings()] | lang=en
- "cve_correlator_cvefinding_to_dict": ".to_dict()" | kind=code-symbol | source=probe/cve/correlator.py:L104 | neighbors=[CVEFinding] | lang=en
- "cve_correlator_rationale_1": "correlator.py — map probe facts to prioritized CVE findings.  Consumes the CPE i" | kind=entity | source=probe/cve/correlator.py:L1 | neighbors=[correlator.py] | lang=en
- "cve_correlator_rationale_124": "Correlate facts carrying a CPE identity against the vuln DB. Deduped by     (cve" | kind=entity | source=probe/cve/correlator.py:L124 | neighbors=[correlate()] | lang=en
- "cve_correlator_rationale_31": "Human-readable note on how old the mirror is (from meta.last_ingest_utc),     pr" | kind=entity | source=probe/cve/correlator.py:L31 | neighbors=[mirror_age_note()] | lang=en
- "cve_correlator_rationale_58": "Return the distro-backport token found in the banner, else None." | kind=entity | source=probe/cve/correlator.py:L58 | neighbors=[_backport_marker()] | lang=en
- "cve_correlator_rationale_64": "0–100 prioritization score. CVSS is halved so it can't dominate; KEV and     int" | kind=entity | source=probe/cve/correlator.py:L64 | neighbors=[risk_score()] | lang=en
- "cve_correlator_summarize": "summarize()" | kind=code-symbol | source=probe/cve/correlator.py:L170 | neighbors=[correlator.py] | lang=en
- "cve_ingest_rationale_1": "ingest.py — build / refresh the offline vulnerability mirror.  Three public feed" | kind=entity | source=probe/cve/ingest.py:L1 | neighbors=[ingest.py] | lang=en
- "cve_ingest_rationale_110": "cpe:2.3:a:vendor:product:version:... -> (part, vendor, product, version)." | kind=entity | source=probe/cve/ingest.py:L110 | neighbors=[_parse_criteria()] | lang=pt
- "cve_ingest_rationale_118": "Upsert one NVD `cve` object + its CPE-applicability rows. Idempotent:     existi" | kind=entity | source=probe/cve/ingest.py:L118 | neighbors=[ingest_one_cve()] | lang=en
- "cve_ingest_rationale_153": "Pull the NVD CVE corpus into the mirror. Resumable via meta.nvd_next_index." | kind=entity | source=probe/cve/ingest.py:L153 | neighbors=[ingest_nvd()] | lang=en
- "cve_ingest_rationale_237": "Refresh every enabled feed. KEV/EPSS first (cheap, always fresh); NVD last     (" | kind=entity | source=probe/cve/ingest.py:L237 | neighbors=[ingest_all()] | lang=en
- "cve_ingest_rationale_46": "certifi CA bundle if present, else the system default. Feeds served TLS     from" | kind=entity | source=probe/cve/ingest.py:L46 | neighbors=[_ssl_context()] | lang=en
- "cve_ingest_rationale_57": "GET with backoff on the transient failures NVD/CDNs throw under load     (403/42" | kind=entity | source=probe/cve/ingest.py:L57 | neighbors=[_get()] | lang=en
- "cve_ingest_rationale_89": "Best available CVSS: prefer v3.1 > v3.0 > v2. Returns (score, severity,     vect" | kind=entity | source=probe/cve/ingest.py:L89 | neighbors=[_cvss()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-191.json

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
