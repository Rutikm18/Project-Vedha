# Network VA — Use-Case Scripts

Manual, per-use-case scripts that run the **same scanner modules the probe runs
in the field** (`python3 -m scanner.<module>`) and print the **actual findings**
so you can review them by hand. One script per network-VA use case, mirroring
the probe's `agent/use_cases.py` library and its funnel
(`host_discovery → port_scan → service_banner → deep_scan`).

Run from this directory. Each takes a target (single host or CIDR):

```bash
cd probe/tests/scan/usecases
./uc_discovery.sh 192.168.1.0/24
./uc_web_triage.sh 192.168.1.10
```

Tunables (env): `RATE` (300) · `CONC` (100) · `TOUT` (4) · `UC_OUT` (/tmp/vedha_uc).
Raw JSONL for every run is kept under `$UC_OUT/` for deeper inspection.

## Use cases → script → vuln it surfaces

| Script | Probe use_case | Scanner(s) | Vuln / finding to plant & detect |
|---|---|---|---|
| `uc_discovery.sh` | uc_discovery_only | host_discovery, port_scan | rogue/unknown host, shadow IT, live mobile |
| `uc_service_fingerprint.sh` | service_fingerprint | port_scan, service_banner | exposed service, version disclosure, Telnet |
| `uc_web_triage.sh` | uc_external_web_triage / uc_web_app_triage | web_scan, tls_scan | missing sec-headers, dangerous HTTP methods, weak/expired TLS |
| `uc_db_exposure.sh` | uc_db_exposure | db_scan | exposed / **unauthenticated** DB (Redis, Mongo, MySQL…) |
| `uc_smb_windows.sh` | uc_windows_estate | smb_scan | **SMBv1 enabled**, SMB signing not required |
| `uc_snmp_exposure.sh` | uc_snmp_exposure | snmp_scan | **default community** (public/private) |
| `uc_udp_exposure.sh` | uc_udp_service_exposure | udp_scan | NTP monlist / DNS recursion / memcached **amplification** |
| `uc_iot_survey.sh` | uc_iot_device_survey | port_scan, service_banner | exposed MQTT / RTSP camera / Telnet / printer / DVR |
| `uc_ai_endpoints.sh` | uc_ai_endpoint_sweep | mcp_ai_scan | exposed AI inference / MCP endpoint |
| `uc_full_assessment.sh` | uc_full_assessment | all of the above | the whole funnel, every branch |

## Suggested vulns to plant (Docker one-liners) for manual testing

```bash
# Redis with NO auth  -> uc_db_exposure.sh should flag 6379 unauth
docker run -d -p 6379:6379 redis

# MongoDB no auth     -> uc_db_exposure.sh flags 27017
docker run -d -p 27017:27017 mongo

# Old web server, missing security headers -> uc_web_triage.sh
docker run -d -p 8080:80 httpd:2.4

# SNMP with 'public'  -> uc_snmp_exposure.sh flags weak community
docker run -d -p 161:161/udp -e SNMP_COMMUNITY=public polinux/snmpd

# MQTT broker open    -> uc_iot_survey.sh flags 1883
docker run -d -p 1883:1883 eclipse-mosquitto

# Ollama AI endpoint  -> uc_ai_endpoints.sh flags 11434
docker run -d -p 11434:11434 ollama/ollama
```

Then point the matching script at `127.0.0.1` (or the Docker host IP) and confirm
the finding appears.

## The exact commands each script runs

Every script prints the underlying `python3 -m scanner.<module> ...` command
before it runs, so you can copy/paste and run any single scanner by hand.
