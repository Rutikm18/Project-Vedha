| Step | Check | Result | Note |
|---|---|---|---|
| Step0 | Fixtures started + ground truth snapshotted | INFO | open=3306 3389 8080 8443; see ./accuracy_test_results_20260706_023915/00_ground_truth.txt |
| Step1 host_discovery | host reported alive/open | PASS |  |
| Step2 port_scanner | all truly-open ports (3306 3389 8080 8443) detected | PASS |  |
| Step2 port_scanner | negative control: closed port 22 not reported open | PASS |  |
| Step3 service_banner | 3389 banner matches ground truth verbatim | PASS |  |
| Step3 service_banner | 8080 reports SimpleHTTP server header | PASS |  |
| Step4 tls_scanner | accepted TLSv1.3 matches openssl ground truth | PASS |  |
| Step4 tls_scanner | negative control: 8080 (plain HTTP) yields no TLS result | PASS |  |
| Step5 web_scanner | 8080 title exactly matches planted GROUND-TRUTH-PAGE | PASS |  |
| Step6 db_scanner | true positive: mysql/mariadb engine detected on 3306 | PASS |  |
| Step7 udp_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 smb_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 snmp_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 udp_scanner | true positive: router service (e.g. DNS 53) detected | PASS |  |
| Step8 mcp_ai_scanner | no AirPlay false positive on 5000 this run | PASS | run 'ollama serve' for a true positive on 11434 |
| Step9 cross-engine | nmap_wrapper & mass_scan agree with port_scanner on 3306 3389 8080 8443 | PASS |  |
| Step10 pipeline | reproduces all truly-open ports (3306 3389 8080 8443) | PASS |  |
| Step11 OT passive | skipped by default (RUN_OT_TEST=1 to enable) | INFO | run manually per guide, or set RUN_OT_TEST=1 |

**Totals:** PASS=16 FAIL=0 INFO=2
