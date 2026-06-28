#!/usr/bin/env bash
# dev.sh — fast probe operations without long commands or hand-managing scope.
# The scope allowlist is auto-built from the target(s) you pass (so a target is
# always in-scope for these quick local runs). For real engagements, scope comes
# from the manager per-job; this is a dev convenience only.
#
#   ./dev.sh scan 192.168.0.34                 full assessment, pretty output
#   ./dev.sh scan 192.168.0.34 triage          pick a mode (triage|assessment|service-specific|re-scan)
#   ./dev.sh scan 192.168.0.34,192.168.0.35    several targets (comma-separated)
#   ./dev.sh web  192.168.0.34                 service-specific: only the web branch
#   ./dev.sh check 192.168.0.34                quick reachability (ping + key TCP ports)
#   ./dev.sh facts 192.168.0.34                full assessment, dump every raw fact as a table
#   ./dev.sh export 192.168.0.34 scan.json     run scan, write the full bundle (import into manager)
set -euo pipefail
cd "$(dirname "$0")"

cmd="${1:-help}"; target="${2:-}"; arg3="${3:-}"

_scope() {  # build a temp scope allowlist from comma-separated targets
  local f; f="$(mktemp)"; IFS=','; for t in $target; do echo "${t}/32" >> "$f"; done; echo "$f"
}
_targets() { echo "${target//,/ }"; }

case "$cmd" in
  scan)
    [ -z "$target" ] && { echo "usage: ./dev.sh scan <ip[,ip2]> [mode]"; exit 1; }
    s="$(_scope)"; mode="${arg3:-assessment}"
    python3 -m workflow.cli -t $(_targets) -s "$s" --mode "$mode" -o /tmp/probe_result.json
    echo "--- result saved to /tmp/probe_result.json ---"; rm -f "$s"
    ;;
  web|db|tls|smb|udp|mcp_ai)
    [ -z "$target" ] && { echo "usage: ./dev.sh $cmd <ip>"; exit 1; }
    s="$(_scope)"
    python3 -m workflow.cli -t $(_targets) -s "$s" --mode service-specific --services "$cmd" -o /tmp/probe_result.json
    rm -f "$s"
    ;;
  facts)
    [ -z "$target" ] && { echo "usage: ./dev.sh facts <ip>"; exit 1; }
    s="$(_scope)"
    python3 -c "
import sys,json; sys.path.insert(0,'.')
from agent.engine import run_scan
r=run_scan('assessment',{'targets':'$(_targets)'.split(),'scope_cidrs':[l.strip() for l in open('$s')]})
print('%-15s %-15s %-6s %-9s %s'%('SCANNER','HOST','PORT','STATUS','DATA'))
print('-'*88)
for f in sorted(r['facts'],key=lambda x:(x['target'],x['scanner'],x.get('port') or 0)):
    d=f.get('data') or {}; sm=', '.join(f'{k}={v}' for k,v in list(d.items())[:3]) if d else (f.get('evidence') or '')
    print('%-15s %-15s %-6s %-9s %s'%(f['scanner'],f['target'],f.get('port') or '-',f['status'],str(sm)[:40]))
print('\n%d facts | %d hosts | %d open | findings=%d (probe never emits CVEs)'%(len(r['facts']),r['host_count'],r['open_ports'],r['finding_count']))
"; rm -f "$s"
    ;;
  export)
    [ -z "$target" ] && { echo "usage: ./dev.sh export <ip[,ip2]> [out.json] [mode]"; exit 1; }
    s="$(_scope)"; out="${arg3:-/tmp/scan.json}"; mode="${4:-assessment}"
    python3 -c "
import sys,json; sys.path.insert(0,'.')
from agent.engine import run_scan
r=run_scan('$mode',{'targets':'$(_targets)'.split(),'scope_cidrs':[l.strip() for l in open('$s')]})
r['generated_at']=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
json.dump(r,open('$out','w'),indent=2,default=str)
print('--- bundle: %d facts | %d hosts -> %s ---'%(len(r['facts']),r['host_count'],'$out'))
"; rm -f "$s"
    ;;
  check)
    [ -z "$target" ] && { echo "usage: ./dev.sh check <ip>"; exit 1; }
    for t in ${target//,/ }; do
      echo "== $t =="
      ping -c 1 -t 2 "$t" >/dev/null 2>&1 && echo "  ping: up" || echo "  ping: no reply"
      for p in 22 80 443 445 3306 8080 8443; do
        (nc -z -G 2 "$t" "$p" 2>/dev/null && echo "  $p OPEN") &
      done; wait
    done
    ;;
  *)
    grep '^#' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
