# vedha-agent — data handling statement

## Classification
Scan output (network topology, service+version inventory, banners, hostnames) is
**confidential customer data**, not telemetry. It is protected in transit, at rest
on the agent, and at rest on the Manager.

## Minimization
The agent records normalized service + version identifiers, not indiscriminate
full-banner capture. Metric labels are low-cardinality and never contain IPs,
hostnames, or target lists.

## At rest (on the agent)
The durable result queue is **encrypted** with a host-sealed key
(`queue.key`, `0600`), append-only, and bounded by size + age with a declared
drop-oldest overflow. Records are deleted on successful delivery (`ack`).

## In transit
TLS 1.2+ to a **per-deployment** Manager URL. The agent never sends to a default
or hardcoded endpoint. mTLS optional. FIPS mode is roadmap.

## Residency
Where results are stored is a property of the Manager deployment (per-deployment
URL). Under DPDP / GDPR / sector rules this is typically a contractual term set at
deployment — the agent imposes no default destination.

## Retention & deletion
- **Agent:** the local queue self-prunes by age/size; `uninstall` + state-dir
  purge wipes identity and any queued results.
- **Manager:** "delete this host's data" is an end-to-end operation (Manager track).

## Disclosure surfaces (redacted)
Logs and the `collect-diagnostics` bundle are the most likely accidental-
disclosure vectors, so both are **redacted**: secrets stripped, own-IPs masked,
no secrets/full-results/target-lists at info level.
