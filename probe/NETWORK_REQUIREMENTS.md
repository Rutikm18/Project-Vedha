# vedha-agent — network requirements

The only rule IT/security must approve is **one outbound 443 to the Manager**.
The agent opens **no inbound listener**.

| Direction | Port | Proto | Destination | Why |
|---|---|---|---|---|
| **Outbound** | **443** | TCP | Manager host | REST + WebSocket (control + results, one port) |
| Outbound | 53 | UDP/TCP | DNS resolver | Resolve the Manager hostname |
| Outbound (LAN) | scan ports | TCP/UDP | the agent's confirmed typed scope | Scanning the customer's own assets |
| **Inbound** | — | — | — | **NONE** — the agent never listens |

- **Egress proxy:** set `HTTPS_PROXY`. If the proxy can't carry WebSockets, set
  `PROBE_WS_ENABLED=false` and the agent long-polls over HTTPS.
- **Private CA:** set `PROBE_CA_BUNDLE=/path/ca.pem`; never `VERIFY_TLS=false` in prod.
- **Never contacted:** loopback, link-local (incl. `169.254.169.254`), multicast,
  broadcast, and the Manager's own address are on a permanent, non-overridable
  denylist. Container/WSL2 namespaces refuse LAN scanning outright.
- **Self-scan mode** contacts nothing off-host and needs no Manager.
- Verify all of the above from a host with `python -m agent.setup doctor`
  (DNS → TCP → TLS → cert-chain to the Manager, plus clock offset).
