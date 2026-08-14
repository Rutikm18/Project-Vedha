"""
VA scanner module — pure collection/scanning layer.

Each submodule is an independent scanner with a unified output schema so you can
measure accuracy and false-positive rate per scanner in isolation:

  host_discovery   liveness (TCP probes + ARP cache)
  port_scanner     TCP connect scan (open/closed/filtered)
  syn_scanner      stateless SYN half-open scan (Linux raw); connect fallback
  service_banner   probe-ladder banner grab + soft-match to product/version
  os_fingerprint   ICMP echo/TTL + TCP-hint OS-family fingerprint
  tls_scanner      TLS versions, ciphers, cert facts, cipher/posture grading
  tls_fingerprint  active TLS fingerprint (JARM methodology) for host identity
  udp_scanner      DNS/NTP/SNMP/NetBIOS/IKE/SIP/TFTP/IPMI/SSDP/mDNS (event-loop UDP)
  scan_funnel      per-host orchestrator: discovery → ports → routed deep scanners
  smb_scanner      SMB dialect detection (SMBv1 enabled?, signing, null sessions)
  snmp_scanner     SNMP full MIB walk: community discovery, ARP table, amplification
  web_scanner      passive HTTP(S) fingerprinting
  mcp_ai_scanner   MCP / AI inference endpoint discovery
  iot_scanner      IoT/embedded: SSDP/UPnP, mDNS, RTSP, MQTT, CoAP, TR-069
  delta_scanner    Scan-state comparison: new services, version changes, host drift
  mobile_scanner   Mobile device exposure: ADB (Android), iOS lockdownd, mDNS
  nmap_wrapper     orchestrate nmap, normalize XML
  ssh_collector    credentialed Linux inventory (authorized creds)

All scanners enforce a scope allowlist before touching any target, and perform
NO exploitation, brute-forcing, or modification.
"""

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, RateLimiter, ResultWriter,
    expand_targets, parse_ports,
)

__all__ = [
    "BaseScanner", "ScanResult", "ScopeGuard", "RateLimiter",
    "ResultWriter", "expand_targets", "parse_ports",
]
