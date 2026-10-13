# Finding-backed attack-path accuracy

## Outcome and scope

The global attack-path dashboard must describe recorded findings and stored possible connections without inventing attacks, mixing engagement identities, or crediting unverified fixes. It is a coherent captured view, not a live test of the environment. No migration, scan, exploitation, or lifecycle write is needed for these checks.

## Contract

1. The existing authorized repeatable-read capture seals systems, findings and stored models at the same cut. Every shown connection must reference a captured source, captured destination, and a finding attached to that destination in the same engagement. Its direction must follow consecutive systems in the stored model. Missing/invalid references are omitted and the incomplete-view notice remains visible.
2. Stored-model connections remain possible regardless of finding verdict, severity, CVSS or an `exploited` flag. The frontend repeats binding checks and prevents this source from promoting confirmed routes. Cross-engagement relationships still require a reviewed observation adapter; selecting several engagements does not create connectivity.
3. False-positive or contradicted findings cannot enable connections. Connections explicitly marked stale are excluded from route counts while remaining inspectable. Conflicting duplicate freshness cannot overwrite a stale observation with a fresh label. A missing timestamp stays unknown rather than being invented.
4. A critical asset needs a non-zero simple route from an entry to count as reachable. A critical/entry annotation alone and a cycle returning to its own start do not qualify. Traversal remains independent of path enumeration limits and continues through critical assets to downstream critical assets.
5. A scan-confirmed fix requires remediated lifecycle, the existing coverage-gated automatic-resolution method, and a completed detection-run reference belonging to the finding's engagement. Running, failed, missing and foreign runs do not qualify. Accepted risks remain unresolved; manual remediation awaits scan confirmation. Dismissed or missing findings are separate from fixes in comparisons.
6. Finding verdict, last recorded observation time, source-finding link and capture time let an operator inspect provenance. Findings changed after the cut cannot silently modify that captured result. The operator analyzes again to refresh it. Incompatible projection versions withhold route counts until reassessment.

## Implementation checkpoints

| Checkpoint | Verification |
| --- | --- |
| Scoped finding and ordered model bindings | Backend projection and API integration tests reject foreign, reversed and mismatched references |
| Findings are evidence, not whole-connection proof | Backend and frontend tests keep confirmed findings on possible stored-model routes |
| Withdrawal and stale handling | False-positive, contradicted and duplicate-freshness regression cases |
| Correct route/reachability counts | Zero-hop critical entries, cycles, critical-to-critical traversal and enumeration-budget cases |
| Fix provenance and comparison | Same-engagement completed run required; closure, dismissal and missing-record cases remain distinct |
| Coherent source cut and refresh | API tests mutate a finding after capture, preserve the old result, and reflect dismissal only in the next capture |
| Presentation and rollout | Type/lint/build checks and local browser confirmation; route-map version advances to `stored-environment-routes@2` |

## Limits

These checks establish consistency with captured platform records. They do not establish that an imported finding is factually correct, that unobserved connections do not exist, or that a possible route can be executed. The legacy model lacks reviewed actor, permission-transfer and current reachability observations. Consequently actual stored-model routes cannot become confirmed attacks. Missing coverage and unavailable grades remain explicit. The local preview uses synthetic records; its example graph is isolated and labelled.

## Rollout

Deploy the API and assessment worker from the same artifact because the assembly digest seals this projection. Refresh enabled selections after deployment; captures produced under the older contract remain immutable and require reassessment. Existing pilot access controls and engagement allowlists remain unchanged. Rollback requires refreshing under the restored model rather than rewriting sealed snapshots.
