#!/usr/bin/env bash
# UC9 — IoT / Embedded Device Survey (probe use_case: uc_iot_device_survey)
# Inventory IoT/embedded devices on the IoT port set. Finds exposed MQTT (1883/
# 8883), RTSP cameras (554), Telnet (23), printers (9100), DVRs (37777).
#
#   ./uc_iot_survey.sh 192.168.1.0/24
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "IoT port scan ($UC_IOT_PORTS)" port_scanner -p "$UC_IOT_PORTS"
uc_open "$UC_LAST"

uc_run "IoT service banners" service_banner -p "$UC_IOT_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
names = {23:"Telnet",554:"RTSP",1883:"MQTT",8883:"MQTT/TLS",9100:"Printer(JetDirect)",37777:"DVR",80:"HTTP",8080:"HTTP-alt"}
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no IoT services responded)"); raise SystemExit
for r in sorted(rows, key=lambda x: x.get("port") or 0):
    d = r.get("data") or {}
    fl = (str(d.get("first_line") or r.get("evidence") or "")).replace("\r"," ").replace("\n"," ")[:60]
    print(f"   {str(r.get('port')):<6} {names.get(r.get('port'),'?'):<18} {fl}")
PY
echo
