| Step | Check | Result | Note |
|---|---|---|---|
| Step0 | Fixtures started + ground truth snapshotted | INFO | see ./accuracy_test_results_20260706_011544/00_ground_truth.txt |
| Step1 host_discovery | host reported alive/open | PASS |  |
| Step2 port_scanner | true positives 3306/3389/8080/8443 all present | PASS |  |
| Step2 port_scanner | negative control on closed port 22 stays silent | PASS |  |
| Step3 service_banner | 3389 banner matches ground truth verbatim | PASS |  |
| Step3 service_banner | 8080 reports SimpleHTTP server header | PASS |  |
| Step4 tls_scanner | accepted_versions matches openssl s_client | INFO | manually diff ./accuracy_test_results_20260706_011544/04_tls_scanner.json vs ./accuracy_test_results_20260706_011544/00_ground_truth.txt |
| Step4 tls_scanner | negative control: 8080 (plain HTTP) yields no TLS result | FAIL | false positive, check ./accuracy_test_results_20260706_011544/04b_tls_scanner_negctrl.json |
| Step5 web_scanner | 8080 title exactly matches planted GROUND-TRUTH-PAGE | PASS |  |
| Step6 db_scanner | no mysql running -> correct negative (no output) | FAIL | false positive, check ./accuracy_test_results_20260706_011544/06_db_scanner.json |
| Step7 udp_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 smb_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 snmp_scanner | localhost negative control (no false positives) | PASS |  |
| Step7 udp_scanner | true positive: router DNS (53) detected | PASS |  |
| Step8 mcp_ai_scanner | no AirPlay false positive on 5000 this run | PASS | or run 'ollama serve' first for a true positive on 11434 |
| Step9 cross-engine | nmap_wrapper & mass_scan agree with port_scanner on all 4 ports | PASS |  |
| Step10 pipeline | reproduces all 4 ports/services from individual scans | PASS |  |
| Step11 OT passive | skipped by default (RUN_OT_TEST=1 to enable) | INFO | run manually per guide, or set RUN_OT_TEST=1 |

**Totals:** PASS=13 FAIL=2 INFO=3
