#!/usr/bin/env bash
# ubuntu-weak-lab.sh - build the Linux-hostable Vedha network-VA test scenarios on ONE
# Ubuntu 22.04/24.04 lab VM, verify each independently, and print a final report of what
# was CREATED+VERIFIED, what is UNCONFIRMED, and what FAILED.
#
#   sudo ./ubuntu-weak-lab.sh up --allow-cidr 192.168.56.0/24 --i-understand-isolated-lab
#   sudo ./ubuntu-weak-lab.sh retry-failed           # rebuild ONLY what FAILED last time
#   sudo ./ubuntu-weak-lab.sh verify                 # re-check everything, change nothing
#   sudo ./ubuntu-weak-lab.sh blind 3306             # firewall a port from the scanner (blind control)
#   sudo ./ubuntu-weak-lab.sh unblind 3306
#   sudo ./ubuntu-weak-lab.sh down [--purge]         # remove units, restore configs, drop firewall
#        ./ubuntu-weak-lab.sh list                   # scenarios + what cannot be hosted here
#        ./ubuntu-weak-lab.sh report                 # last report
#
# Options for `up`/`verify`:  --only T01,G03   --skip T13   --min-severity medium|high|critical
#                             --verify-host IP  --no-controls
#
# SAFETY - this script makes a host DELIBERATELY VULNERABLE:
#   * it refuses to run unless you pass --allow-cidr (your scanner's network, RFC1918/CGNAT
#     only) and --i-understand-isolated-lab;
#   * every lab port is firewalled to that CIDR by a systemd-managed iptables chain that is
#     installed BEFORE any service starts and re-applied at boot (before the network is up);
#   * the SMTP "open relay" discards mail, Redis has its RCE commands disabled, FTP/WebDAV
#     uploads land on small tmpfs mounts, UDP emulators are rate-limited and never amplify
#     (except the NTP monlist emulator, which exists to be measured - keep the firewall on).
# Use a throwaway VM on an isolated network. Never a host with data you care about.
set -uo pipefail

SCRIPT_VERSION="2026-10-10"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="${VEDHA_LAB_DIR:-/opt/vedha-lab}"
CONF_DIR="${VEDHA_LAB_CONF_DIR:-/etc/vedha-lab}"
STATE_DIR="${VEDHA_LAB_STATE:-/var/lib/vedha-lab}"
LOG_DIR="$STATE_DIR/logs"
RESULTS="$STATE_DIR/results.tsv"
CHAIN="VEDHA_LAB"
PY="python3"
VHOST="127.0.0.1"
VLAN=""

# ── small utilities ───────────────────────────────────────────────────────────

say()  { printf '%s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 2; }

need_root() { [ "$(id -u)" -eq 0 ] || die "run as root (sudo)"; }

check_os() {
  [ -r /etc/os-release ] || die "cannot read /etc/os-release"
  # shellcheck disable=SC1091
  . /etc/os-release
  [ "${ID:-}" = "ubuntu" ] || die "Ubuntu only (found ${ID:-unknown})"
  case "${VERSION_ID:-}" in
    22.04|24.04) ;;
    *) warn "tested design targets Ubuntu 22.04/24.04; found ${VERSION_ID:-?} - continuing" ;;
  esac
}

cidr_ok() { # refuse anything that is not RFC1918 / CGNAT
  "$PY" - "$1" <<'PY'
import ipaddress, sys
try:
    n = ipaddress.ip_network(sys.argv[1], strict=False)
except ValueError:
    sys.exit(1)
allowed = [ipaddress.ip_network(x) for x in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "100.64.0.0/10")]
sys.exit(0 if any(n.subnet_of(a) for a in allowed) else 1)
PY
}

public_iface_ips() {
  "$PY" - <<'PY'
import ipaddress, subprocess
out = subprocess.run(["ip", "-4", "-o", "addr", "show", "scope", "global"], capture_output=True, text=True).stdout
nets = [ipaddress.ip_network(x) for x in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "100.64.0.0/10")]
bad = []
for line in out.splitlines():
    ip = ipaddress.ip_interface(line.split()[3]).ip
    if not any(ip in n for n in nets):
        bad.append(str(ip))
print(" ".join(bad))
PY
}

lan_ip() {
  ip -4 route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}'
}

ensure_dirs() { mkdir -p "$LAB_DIR" "$CONF_DIR" "$STATE_DIR" "$LOG_DIR" "$STATE_DIR/backup"; }

# ── apt / config / unit helpers ───────────────────────────────────────────────

APT_UPDATED=0
apt_update_once() {
  [ "$APT_UPDATED" -eq 1 ] && return 0
  wait_apt_idle || warn "apt is still busy; trying anyway"
  DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=900 update -qq || warn "apt-get update failed; using cached lists"
  APT_UPDATED=1
}

wait_apt_idle() { # a fresh VM runs unattended-upgrades; wait (max 15 min) for it instead of failing
  local n=180
  command -v fuser >/dev/null 2>&1 || return 0
  while fuser /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/lib/apt/lists/lock >/dev/null 2>&1; do
    if [ "$n" -le 0 ]; then
      echo "apt/dpkg is still locked by another process after 15 minutes"
      return 1
    fi
    [ $((n % 12)) -eq 0 ] && echo "waiting for another apt/dpkg process to finish ..."
    sleep 5
    n=$((n - 1))
  done
}

pkg() { # install packages, remembering which ones WE added (for `down --purge`)
  local p
  apt_update_once
  wait_apt_idle || return 1
  for p in "$@"; do
    if ! dpkg -s "$p" >/dev/null 2>&1; then echo "$p" >>"$STATE_DIR/new-pkgs.txt"; fi
  done
  DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=900 install -y -qq "$@"
}

bak() { # back a config file up once, so `down` can restore it
  local f="$1" b="$STATE_DIR/backup$1"
  [ -e "$b" ] || [ -e "$b.absent" ] && return 0
  mkdir -p "$(dirname "$b")"
  if [ -e "$f" ]; then cp -a "$f" "$b"; else : >"$b.absent"; fi
}

write_unit() { # name description service-body [unit-section-extra]
  cat >"/etc/systemd/system/vedha-lab-$1.service" <<EOF
[Unit]
Description=Vedha lab: $2
After=network.target
${4:-}

[Service]
$3
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
  echo "vedha-lab-$1.service" >>"$STATE_DIR/units.txt"
  systemctl daemon-reload
}

svc_start() { # unit [unit...] : enable, (re)start, require active
  local u
  for u in "$@"; do
    systemctl enable "$u" >/dev/null 2>&1 || true
    systemctl restart "$u" || { journalctl -u "$u" -n 12 --no-pager 2>/dev/null; return 1; }
    sleep 1
    if ! systemctl is-active --quiet "$u"; then
      journalctl -u "$u" -n 12 --no-pager 2>/dev/null
      echo "unit $u is not active"
      return 1
    fi
    echo "$u" >>"$STATE_DIR/touched-svcs.txt"
  done
}

wait_port() { # tcp|udp port [seconds]
  local proto="$1" port="$2" n="${3:-20}" flag="-ltnH"
  [ "$proto" = "udp" ] && flag="-lunH"
  while [ "$n" -gt 0 ]; do
    if ss $flag "sport = :$port" 2>/dev/null | grep -q .; then return 0; fi
    sleep 1
    n=$((n - 1))
  done
  echo "nothing is listening on $proto/$port"
  return 1
}

emu() { # name [args...] : run lab_emulators.py serve NAME as a hardened systemd unit
  local n="$1"
  shift
  write_unit "emu-$n" "emulator $n" "DynamicUser=yes
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ExecStart=/usr/bin/python3 $LAB_DIR/lab_emulators.py serve $n $*"
  svc_start "vedha-lab-emu-$n"
}

lab_tmpfs() { # dir size owner-user [mode] : small tmpfs so anonymous uploads cannot fill the disk
  local dir="$1" size="$2" user="$3" mode="${4:-755}" uid gid opts
  uid=$(id -u "$user")
  gid=$(id -g "$user")
  opts="size=$size,uid=$uid,gid=$gid,mode=$mode"
  mkdir -p "$dir"
  if mountpoint -q "$dir"; then
    mount -o "remount,$opts" "$dir"     # already mounted by an earlier run: apply the new options
  else
    mount -t tmpfs -o "$opts" tmpfs "$dir"
  fi
  sed -i "\\# $dir tmpfs #d" /etc/fstab
  echo "tmpfs $dir tmpfs $opts 0 0 # vedha-lab" >>/etc/fstab
}

# ── probes ────────────────────────────────────────────────────────────────────

probe() { "$PY" "$LAB_DIR/lab_probe.py" "$@"; }

vchk() { # check-name [port] : 0 = weakness confirmed, else FAILED with the reason
  local out rc
  out=$(probe check "$1" "$VHOST" ${2:+"$2"} 2>&1)
  rc=$?
  case $rc in
    0) echo "$out"; return 0 ;;
    1) echo "service is up but NOT weak: $out"; return 1 ;;
    *) echo "unreachable / verifier error: $out"; return 2 ;;
  esac
}

vchk_lan() { # same, but against the LAN address (services that ignore loopback)
  local saved="$VHOST"
  VHOST="${VLAN:-$VHOST}"
  vchk "$@"
  local rc=$?
  VHOST="$saved"
  return $rc
}

vctl() { # control: the safe twin must NOT be weak. rc 1 from the probe is the PASS here
  local out rc
  out=$(probe check "$1" "$VHOST" ${2:+"$2"} 2>&1)
  rc=$?
  case $rc in
    1) echo "control is clean: $out"; return 0 ;;
    0) echo "control is unexpectedly weak: $out"; return 1 ;;
    *) echo "control unreachable: $out"; return 2 ;;
  esac
}

vport() { # proto port... : listener exists (used for port-only emulators)
  local proto="$1" p out
  shift
  for p in "$@"; do
    out=$(probe up "$proto" "$VHOST" "$p" 2>&1) || { echo "$out"; return 2; }
  done
  echo "$proto ports $* answer"
}

# ── scenario registry ─────────────────────────────────────────────────────────
# reg ID SEVERITY(C/H/M/-) TYPE NAME "proto:port ..."
# TYPE: REAL = the real product/config; EMULATED = protocol emulator (fingerprint-tier);
#       PORTONLY = listener only (tests reach/exposure, not protocol); CONTROL = safe twin.
REG=""
reg() { REG="${REG}$1|$2|$3|$4|$5
"; }

register_all() {
  reg T01 H REAL     "Weak SSH algorithms (sshd :2222)"                     "tcp:2222"
  reg T02 M REAL     "Terrapin-exposed SSH (old Dropbear :2223)"            "tcp:2223"
  reg T03 C REAL     "VNC with no authentication :5900"                     "tcp:5900"
  reg T04 M REAL     "VNC legacy password auth :5901"                       "tcp:5901"
  reg T05 C EMULATED "IPMI cipher-zero :623/udp"                            "udp:623"
  reg T07 M REAL     "LDAP anonymous search :389"                           "tcp:389"
  reg T08 H REAL     "DNS zone transfer allowed :53"                        "tcp:53 udp:53"
  reg T10 H REAL     "NFS world-readable export :2049"                      "tcp:2049 tcp:111 udp:111 tcp:20048 udp:20048"
  reg T11 H REAL     "Rsync anonymous module :873"                          "tcp:873"
  reg T12 C REAL     "Redis without authentication :6379"                   "tcp:6379"
  reg T13 M REAL     "MariaDB without TLS :3306"                            "tcp:3306"
  reg T14 H REAL     "TLS certificate with 1024-bit key :8444"              "tcp:8444"
  reg T15 H REAL     "TLS certificate signed with SHA-1 :8445"              "tcp:8445"
  reg T16 M REAL     "HTTP TRACE / PUT / DELETE enabled :8080"              "tcp:8080"
  reg T18 H REAL     "MQTT broker, anonymous clients :1883"                 "tcp:1883"
  reg T19 M EMULATED "RTSP camera endpoint :554"                            "tcp:554"
  reg T20 M EMULATED "TR-069 / CWMP listener :7547"                         "tcp:7547"
  reg T21 C EMULATED "Android ADB over TCP, no auth :5555"                  "tcp:5555"
  reg T22 H EMULATED "AI endpoint (Ollama API) with no auth :11434"         "tcp:11434"
  reg T23 M REAL     "SNMP GETBULK amplification :161/udp"                  "udp:161"
  reg G01 H REAL     "SNMPv3 noAuthNoPriv user :161/udp"                    "udp:161"
  reg G02 M EMULATED "UPnP / SSDP Internet Gateway Device :1900"            "udp:1900 tcp:5000"
  reg G03 M REAL     "TFTP unauthenticated read :69/udp"                    "udp:69"
  reg G04 M EMULATED "NTP monlist amplification :123/udp"                   "udp:123"
  reg G05 M EMULATED "RTSP stream with no authentication :8554"             "tcp:8554"
  reg G06 H REAL     "FTP anonymous WRITE :21"                              "tcp:21 tcp:40000:40010"
  reg G07 M REAL     "SMTP open relay (discarding) + VRFY :25"              "tcp:25"
  reg G08 M REAL     "IKEv1 aggressive mode PSK :500/udp"                   "udp:500 udp:4500"
  reg G09 H EMULATED "SIP server exposed :5060"                             "udp:5060 tcp:5060"
  reg G10 M REAL     "mDNS (avahi) exposed :5353/udp"                       "udp:5353"
  reg G11 H REAL     "NetBIOS name service exposed :137/udp"                "udp:137 udp:138"
  reg G14 C PORTONLY "Cisco Smart Install port :4786"                       "tcp:4786"
  reg G15 H PORTONLY "SLP :427"                                             "tcp:427 udp:427"
  reg G16 H PORTONLY "XDMCP :177/udp"                                       "udp:177"
  reg G17 H PORTONLY "Radmin :4899"                                         "tcp:4899"
  reg G18 H PORTONLY "AFP :548"                                             "tcp:548"
  reg G19 H PORTONLY "Erlang EPMD :4369"                                    "tcp:4369"
  reg G20 H PORTONLY "BGP :179"                                             "tcp:179"
  reg G21 M PORTONLY "MikroTik Winbox :8291"                                "tcp:8291"
  reg G22 H PORTONLY "Ubiquiti discovery :10001/udp"                        "udp:10001"
  reg G23 M PORTONLY "MSMQ :1801"                                           "tcp:1801"
  reg G24 M PORTONLY "ActiveMQ / AMQP :61616 :5672"                         "tcp:61616 tcp:5672"
  reg G25 H PORTONLY "NAT-PMP :5351/udp"                                    "udp:5351"
  reg G26 M PORTONLY "WS-Discovery, STUN, CoAP, QOTD, chargen, DB2 disc."   "udp:3702 udp:3478 udp:5683 tcp:17 udp:17 tcp:19 udp:19 udp:523"
  reg G27 M REAL     "Open HTTP proxy (no auth, no real egress) :3128"      "tcp:3128"
  reg C01 -  CONTROL "Control: strong TLS cert (2048-bit, SHA-256) :9443"   "tcp:9443"
  reg C02 -  CONTROL "Control: Redis with a password :6380"                 "tcp:6380"
  reg C03 -  CONTROL "Control: stock sshd :22 (no legacy algorithms)"       ""
}

# Not buildable on a single Ubuntu host, or refused on purpose. Printed in every report.
SKIPPED="T24|OS past end-of-support|needs an end-of-life OS image, separate VM
T25|Default-credential candidate|needs a vendor device banner on the allowlist
T26|Endpoint protection disabled|Windows host
T27|Service binary in user-writable path|Windows host
T28|Unquoted Windows service path|Windows host
T30|Miner / malware process|needs a credentialed host inventory
T31|Backdoor listener bound on host|needs a credentialed host inventory
T32|TLS fingerprint of known tooling|needs a C2 TLS fingerprint
T33|AD exposure correlation|needs a Windows domain controller
T35 T37 T39|Correlations needing Telnet / router role / SMB users|compose from the Windows rig
T34 T36 T38|Correlations (mgmt plane, datastore+unauth, anon data)|emerge from services created here, no extra setup
T40-T58|KEV overlay, attack paths, round-1 fixes, platform|manager-side or need Windows / vulnerable versions
G28|Heartbleed / ROBOT|needs vulnerable OpenSSL, unavailable on supported Ubuntu
G29|ESXi / vCenter fingerprint|proprietary appliance
G30 G31|Edge-device CVEs, end-of-support devices|vendor appliances / lifecycle data
G36-G39|Kerberos, ADCS, LLMNR, LDAP signing|needs a Windows AD
G40 G42|Credentialed scan, confirmed default credentials|probe features not built
G43|Rogue DHCP|REFUSED: would disrupt the LAN
G44 G50|Active IPv6, Kubernetes audit|separate lab"
EXCLUDED_NOTE="Excluded as Low/Info by design: T06 LDAP anonymous bind, T09 DNS version.bind, T17 no HSTS, T29 excessive admins, GTP, NTRIP."

# ── scenarios: up_<ID> builds, verify_<ID> proves ─────────────────────────────

supported_csv() { # type candidates... -> comma list of what this ssh build supports
  local t="$1" c out="" all
  shift
  all=$(ssh -Q "$t" 2>/dev/null)
  for c in "$@"; do echo "$all" | grep -qx "$c" && out="${out:+$out,}$c"; done
  echo "$out"
}

up_T01() {
  pkg openssh-server openssh-client
  ssh-keygen -A
  local kex ciph
  kex=$(supported_csv kex diffie-hellman-group1-sha1 diffie-hellman-group14-sha1 diffie-hellman-group-exchange-sha1)
  ciph=$(supported_csv cipher aes128-cbc aes256-cbc 3des-cbc)
  [ -n "$kex$ciph" ] || { echo "this OpenSSH build offers no legacy algorithms"; return 1; }
  cat >"$CONF_DIR/sshd_weak_config" <<EOF
Port 2222
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
PidFile /run/sshd_weak.pid
${kex:+KexAlgorithms +$kex}
${ciph:+Ciphers +$ciph}
PasswordAuthentication no
PermitRootLogin no
UsePAM no
EOF
  mkdir -p /run/sshd
  /usr/sbin/sshd -t -f "$CONF_DIR/sshd_weak_config"
  write_unit sshd-weak "OpenSSH with legacy algorithms" "ExecStartPre=/bin/mkdir -p /run/sshd
ExecStart=/usr/sbin/sshd -D -e -f $CONF_DIR/sshd_weak_config"
  svc_start vedha-lab-sshd-weak
  wait_port tcp 2222
}
verify_T01() { vchk ssh-weak 2222; }

up_T02() {
  pkg dropbear-bin
  mkdir -p /etc/dropbear
  write_unit dropbear "Dropbear without strict-kex" "ExecStart=$(command -v dropbear) -F -E -R -w -p 2223"
  svc_start vedha-lab-dropbear
  wait_port tcp 2223
}
verify_T02() { vchk ssh-terrapin 2223; }

xvfb_unit() {
  pkg xvfb x11vnc
  write_unit xvfb "virtual display :99" "ExecStart=/usr/bin/Xvfb :99 -screen 0 800x600x16 -nolisten tcp"
  svc_start vedha-lab-xvfb
}
up_T03() {
  xvfb_unit
  write_unit vnc-none "x11vnc with no password" "ExecStartPre=/bin/sleep 2
ExecStart=/usr/bin/x11vnc -display :99 -rfbport 5900 -nopw -forever -shared -noxdamage -noipv6" \
    "Requires=vedha-lab-xvfb.service
After=vedha-lab-xvfb.service"
  svc_start vedha-lab-vnc-none
  wait_port tcp 5900
}
verify_T03() { vchk vnc-none 5900; }

up_T04() {
  xvfb_unit
  write_unit vnc-auth "x11vnc with legacy VNC password auth" "ExecStartPre=/bin/sleep 2
ExecStart=/usr/bin/x11vnc -display :99 -rfbport 5901 -passwd labpass12 -forever -shared -noxdamage -noipv6" \
    "Requires=vedha-lab-xvfb.service
After=vedha-lab-xvfb.service"
  svc_start vedha-lab-vnc-auth
  wait_port tcp 5901
}
verify_T04() { vchk vnc-auth 5901; }

up_T05() { emu ipmi --udp 623; wait_port udp 623; }
verify_T05() { vchk ipmi-cipher0 623; }

up_T07() {
  cat <<'EOF' | debconf-set-selections
slapd slapd/domain string lab.local
slapd shared/organization string Vedha Lab
slapd slapd/password1 password labadmin
slapd slapd/password2 password labadmin
slapd slapd/no_configuration boolean false
slapd slapd/purge_database boolean false
EOF
  pkg slapd ldap-utils
  if ! ldapsearch -x -H ldap://127.0.0.1 -b dc=lab,dc=local -s base >/dev/null 2>&1; then
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure slapd
  fi
  systemctl enable --now slapd
  cat >"$STATE_DIR/lab.ldif" <<'EOF'
dn: ou=people,dc=lab,dc=local
objectClass: organizationalUnit
ou: people

dn: uid=alice,ou=people,dc=lab,dc=local
objectClass: inetOrgPerson
cn: Alice Lab
sn: Lab
uid: alice
mail: alice@lab.local
EOF
  ldapadd -x -H ldap://127.0.0.1 -D cn=admin,dc=lab,dc=local -w labadmin -f "$STATE_DIR/lab.ldif" >/dev/null 2>&1 || true
  wait_port tcp 389
}
verify_T07() { vchk ldap-anon-search 389; }

up_T08() {
  pkg bind9 dnsutils
  bak /etc/bind/named.conf.options
  bak /etc/bind/named.conf.local
  cat >/etc/bind/named.conf.options <<'EOF'
options {
  directory "/var/cache/bind";
  listen-on { any; };
  listen-on-v6 { none; };
  allow-query { any; };
  allow-transfer { any; };
  recursion no;
  dnssec-validation no;
};
EOF
  cat >/etc/bind/named.conf.local <<'EOF'
zone "lab.local" { type master; file "/etc/bind/db.lab.local"; allow-transfer { any; }; };
EOF
  cat >/etc/bind/db.lab.local <<'EOF'
$TTL 300
@   IN SOA ns1.lab.local. admin.lab.local. ( 1 3600 600 86400 300 )
@   IN NS  ns1.lab.local.
ns1 IN A   127.0.0.1
www IN A   10.0.0.10
db  IN A   10.0.0.11
vpn IN A   10.0.0.12
EOF
  named-checkconf
  named-checkzone lab.local /etc/bind/db.lab.local >/dev/null
  svc_start bind9
  wait_port tcp 53
}
verify_T08() { vchk dns-axfr 53; }

up_T10() {
  pkg nfs-kernel-server nfs-common rpcbind
  mkdir -p /srv/lab/nfs /etc/exports.d /etc/nfs.conf.d
  echo "vedha lab nfs file" >/srv/lab/nfs/readme.txt
  printf '/srv/lab/nfs *(ro,sync,no_subtree_check,no_root_squash)\n' >/etc/exports.d/vedha-lab.exports
  printf '[mountd]\nport=20048\n' >/etc/nfs.conf.d/vedha-lab.conf
  svc_start nfs-kernel-server
  exportfs -ra
  wait_port tcp 2049
}
verify_T10() { vchk nfs-export 2049; }

up_T11() {
  pkg rsync
  bak /etc/rsyncd.conf
  mkdir -p /srv/lab/rsync
  echo "vedha lab rsync file" >/srv/lab/rsync/readme.txt
  cat >/etc/rsyncd.conf <<'EOF'
uid = nobody
gid = nogroup
use chroot = yes
read only = yes
max connections = 10
[public]
  path = /srv/lab/rsync
  comment = Vedha lab public module
  list = yes
EOF
  svc_start rsync
  wait_port tcp 873
}
verify_T11() { vchk rsync-anon 873; }

up_T12() {
  pkg redis-server
  bak /etc/redis/redis.conf
  sed -i -E 's/^bind .*/bind 0.0.0.0/; s/^protected-mode .*/protected-mode no/; /^requirepass/d; /^rename-command/d' /etc/redis/redis.conf
  cat >>/etc/redis/redis.conf <<'EOF'
# vedha lab: unauthenticated on purpose, but the classic remote-code-execution paths are off
rename-command CONFIG ""
rename-command SLAVEOF ""
rename-command REPLICAOF ""
rename-command MODULE ""
rename-command DEBUG ""
rename-command FLUSHALL ""
rename-command FLUSHDB ""
EOF
  svc_start redis-server
  wait_port tcp 6379
}
verify_T12() { vchk redis-noauth 6379; }

up_T13() {
  pkg mariadb-server
  printf '[mysqld]\nbind-address=0.0.0.0\nskip-ssl\n' >/etc/mysql/mariadb.conf.d/99-vedha-lab.cnf
  echo "mariadb" >>"$STATE_DIR/touched-svcs.txt"
  systemctl restart mariadb
  wait_port tcp 3306
}
verify_T13() { vchk mysql-cleartext 3306; }

tls_prepare() {
  pkg openssl
  mkdir -p "$CONF_DIR/tls"
  cat >"$CONF_DIR/openssl-seclevel0.cnf" <<'EOF'
openssl_conf = default_conf
[default_conf]
ssl_conf = ssl_sect
[ssl_sect]
system_default = system_default_sect
[system_default_sect]
CipherString = DEFAULT:@SECLEVEL=0
MinProtocol = TLSv1.2
EOF
}
tls_unit() { # name port bits sigflag weak(1|0)
  local name="$1" port="$2" bits="$3" sig="$4" weak="$5" envp=""
  tls_prepare
  [ "$weak" = "1" ] && envp="OPENSSL_CONF=$CONF_DIR/openssl-seclevel0.cnf"
  env ${envp:+$envp} openssl req -x509 -newkey "rsa:$bits" -nodes -keyout "$CONF_DIR/tls/$name.key" \
    -out "$CONF_DIR/tls/$name.crt" -days 825 -subj "/CN=$name.lab.local" "-$sig"
  chmod 644 "$CONF_DIR/tls/$name.key" "$CONF_DIR/tls/$name.crt"
  write_unit "tls-$name" "TLS test server $name" "StandardInput=null
DynamicUser=yes
ExecStart=/usr/bin/env ${envp:+$envp} /usr/bin/openssl s_server -accept $port -cert $CONF_DIR/tls/$name.crt -key $CONF_DIR/tls/$name.key -tls1_2 -www -quiet"
  svc_start "vedha-lab-tls-$name"
  wait_port tcp "$port"
}
up_T14() { tls_unit weakkey 8444 1024 sha256 1; }
verify_T14() { vchk tls-weakkey 8444; }
up_T15() { tls_unit sha1sig 8445 2048 sha1 1; }
verify_T15() { vchk tls-sha1 8445; }
up_C01() { tls_unit strong 9443 2048 sha256 0; }
verify_C01() { vchk tls-strong 9443; }

up_T16() {
  pkg apache2
  a2enmod dav dav_fs >/dev/null
  a2dissite 000-default >/dev/null 2>&1 || true
  bak /etc/apache2/ports.conf
  sed -i 's/^Listen 80$/#Listen 80/' /etc/apache2/ports.conf
  mkdir -p /srv/lab/web
  echo "vedha lab web" >/srv/lab/web/index.html
  lab_tmpfs /srv/lab/web/dav 8m www-data
  cat >/etc/apache2/conf-available/vedha-lab.conf <<'EOF'
ServerName lab.local
TraceEnable On
DavLockDB /var/lock/apache2/DavLock
Listen 8080
<VirtualHost *:8080>
  DocumentRoot /srv/lab/web
  <Directory /srv/lab/web>
    Require all granted
  </Directory>
  <Location /dav>
    DAV On
    Require all granted
  </Location>
</VirtualHost>
EOF
  a2enconf vedha-lab >/dev/null
  apache2ctl configtest
  svc_start apache2
  wait_port tcp 8080
}
verify_T16() { vchk http-methods 8080; }

up_T18() {
  pkg mosquitto
  printf 'listener 1883 0.0.0.0\nallow_anonymous true\n' >/etc/mosquitto/conf.d/vedha-lab.conf
  svc_start mosquitto
  wait_port tcp 1883
}
verify_T18() { vchk mqtt-anon 1883; }

up_T19() { emu rtsp --tcp 554,8554; wait_port tcp 554; }
verify_T19() { vchk rtsp-options 554; }
up_T20() { emu cwmp --tcp 7547; wait_port tcp 7547; }
verify_T20() { vchk cwmp 7547; }
up_T21() { emu adb --tcp 5555; wait_port tcp 5555; }
verify_T21() { vchk adb-noauth 5555; }
up_T22() { emu ollama --tcp 11434; wait_port tcp 11434; }
verify_T22() { vchk ollama 11434; }

snmpd_setup() {
  pkg snmpd snmp
  bak /etc/snmp/snmpd.conf
  systemctl stop snmpd 2>/dev/null || true
  rm -f /var/lib/snmp/snmpd.conf
  cat >/etc/snmp/snmpd.conf <<'EOF'
agentaddress udp:161
rocommunity public default
createUser labnoauth
rouser labnoauth noauth
sysLocation Vedha lab
sysContact lab@example.invalid
EOF
  svc_start snmpd
  wait_port udp 161
}
up_T23() { snmpd_setup; }
verify_T23() { vchk snmp-bulk 161; }
up_G01() { snmpd_setup; }
verify_G01() { vchk snmpv3-noauth 161; }

up_G02() { emu ssdp --udp 1900; wait_port udp 1900; }
verify_G02() { vchk ssdp-igd 1900; }

up_G03() {
  pkg tftpd-hpa
  bak /etc/default/tftpd-hpa
  mkdir -p /srv/lab/tftp
  echo "vedha lab tftp file" >/srv/lab/tftp/lab.txt
  chmod 644 /srv/lab/tftp/lab.txt
  printf 'TFTP_USERNAME="tftp"\nTFTP_DIRECTORY="/srv/lab/tftp"\nTFTP_ADDRESS=":69"\nTFTP_OPTIONS="--secure"\n' >/etc/default/tftpd-hpa
  svc_start tftpd-hpa
  wait_port udp 69
}
verify_G03() { vchk tftp-read 69; }

up_G04() { emu ntp --udp 123; wait_port udp 123; }
verify_G04() { vchk ntp-monlist 123; }
up_G05() { emu rtsp --tcp 554,8554; wait_port tcp 8554; }
verify_G05() { vchk rtsp-describe 8554; }

up_G06() {
  pkg vsftpd
  bak /etc/vsftpd.conf
  mkdir -p /srv/lab/ftp /var/run/vsftpd/empty
  chown root:root /srv/lab/ftp
  chmod 755 /srv/lab/ftp
  lab_tmpfs /srv/lab/ftp/upload 16m ftp 777      # world-writable but only 16 MB, RAM-backed
  cat >/etc/vsftpd.conf <<'EOF'
listen=YES
listen_ipv6=NO
anonymous_enable=YES
local_enable=NO
write_enable=YES
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=NO
anon_umask=022
chown_uploads=NO
anon_root=/srv/lab/ftp
secure_chroot_dir=/var/run/vsftpd/empty
seccomp_sandbox=NO
xferlog_enable=YES
vsftpd_log_file=/var/log/vsftpd.log
log_ftp_protocol=YES
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40010
ftpd_banner=Vedha lab FTP
EOF
  svc_start vsftpd
  wait_port tcp 21
}
verify_G06() {
  local out rc
  out=$(vchk ftp-anon-write 21)
  rc=$?
  if [ $rc -ne 0 ]; then
    {
      echo "== G06 diagnostics (why anonymous upload failed)"
      mount | grep ' /srv/lab/ftp/upload ' || echo "upload dir is NOT a mount point"
      ls -ld /srv/lab/ftp /srv/lab/ftp/upload
      id ftp
      grep -E '^(anon|write|chown|seccomp|local)' /etc/vsftpd.conf
      journalctl -u vsftpd -n 15 --no-pager 2>&1
      tail -n 12 /var/log/vsftpd.log 2>&1
      (dmesg 2>/dev/null | grep -i -E 'apparmor.*vsftpd|DENIED.*vsftpd' | tail -n 5)
    } >>"$LOG_DIR/G06.log" 2>&1
    out="$out [diagnostics appended to $LOG_DIR/G06.log]"
  fi
  echo "$out"
  return $rc
}

up_G07() {
  cat <<'EOF' | debconf-set-selections
postfix postfix/main_mailer_type select Internet Site
postfix postfix/mailname string lab.local
EOF
  pkg postfix
  bak /etc/postfix/main.cf
  postconf -e "inet_interfaces = all" "inet_protocols = ipv4" "mynetworks = 0.0.0.0/0" \
    "smtpd_relay_restrictions = permit" "smtpd_recipient_restrictions = permit" \
    "disable_vrfy_command = no" "smtpd_tls_security_level = none" \
    "default_transport = discard:vedha-lab" "relay_transport = discard:vedha-lab" \
    "message_size_limit = 10240" "smtpd_client_message_rate_limit = 20"
  svc_start postfix
  wait_port tcp 25
}
verify_G07() { vchk smtp-relay 25; }

up_G08() {
  pkg strongswan-starter
  bak /etc/ipsec.conf
  bak /etc/ipsec.secrets
  cat >/etc/ipsec.conf <<'EOF'
config setup
conn lab-aggressive
  keyexchange=ikev1
  aggressive=yes
  authby=secret
  left=%any
  leftid=@lab-gw
  right=%any
  ike=aes128-sha1-modp1024!
  auto=add
EOF
  printf '@lab-gw : PSK "vedha-lab-not-a-secret"\n' >/etc/ipsec.secrets
  chmod 600 /etc/ipsec.secrets
  systemctl enable strongswan-starter >/dev/null 2>&1 || true
  systemctl restart strongswan-starter || systemctl restart strongswan
  echo "strongswan-starter" >>"$STATE_DIR/touched-svcs.txt"
  wait_port udp 500
}
verify_G08() {
  # UNCONFIRMED by design: we confirm IKE is listening; proving aggressive-mode acceptance
  # needs a full ISAKMP exchange the lab verifier does not implement.
  if ss -lunH 'sport = :500' | grep -q .; then
    echo "strongSwan listening on udp/500 with aggressive=yes (aggressive-mode acceptance not independently proven)"
    return 3
  fi
  echo "nothing listening on udp/500"
  return 1
}

up_G09() { emu sip --tcp 5060 --udp 5060; wait_port udp 5060; }
verify_G09() { vchk sip-options 5060; }

up_G10() { pkg avahi-daemon; svc_start avahi-daemon; wait_port udp 5353; }
verify_G10() { vchk_lan mdns 5353; }

up_G11() {
  pkg samba
  bak /etc/samba/smb.conf
  printf '[global]\n  workgroup = LAB\n  netbios name = LABHOST\n  disable netbios = no\n' >/etc/samba/smb.conf
  systemctl disable --now smbd winbind >/dev/null 2>&1 || true
  svc_start nmbd
  wait_port udp 137
}
verify_G11() { vchk_lan nbns 137; }

up_G27() {
  pkg tinyproxy
  bak /etc/tinyproxy/tinyproxy.conf
  printf 'example\\.invalid\n' >/etc/tinyproxy/lab-filter
  cat >/etc/tinyproxy/tinyproxy.conf <<'EOF'
User tinyproxy
Group tinyproxy
Port 3128
Listen 0.0.0.0
Timeout 30
MaxClients 20
Allow 0.0.0.0/0
Filter "/etc/tinyproxy/lab-filter"
FilterDefaultDeny Yes
ConnectPort 443
LogFile "/var/log/tinyproxy/tinyproxy.log"
PidFile "/run/tinyproxy/tinyproxy.pid"
EOF
  svc_start tinyproxy
  wait_port tcp 3128
}
verify_G27() { vchk proxy-open 3128; }

up_C02() {
  pkg redis-server
  mkdir -p "$STATE_DIR/redis-auth"
  chown redis:redis "$STATE_DIR/redis-auth"
  printf 'port 6380\nbind 0.0.0.0\nrequirepass labsecret-not-for-prod\nprotected-mode yes\ndir %s\n' \
    "$STATE_DIR/redis-auth" >"$CONF_DIR/redis-auth.conf"
  write_unit redis-auth "Redis with a password (control)" "User=redis
ExecStart=/usr/bin/redis-server $CONF_DIR/redis-auth.conf"
  svc_start vedha-lab-redis-auth
  wait_port tcp 6380
}
verify_C02() { vctl redis-noauth 6380; }

up_C03() { pkg openssh-server; systemctl enable --now ssh; wait_port tcp 22; }
verify_C03() { vctl ssh-weak 22; }

# port-only scenarios: the shared `listen` emulator is started once, before the run
for _id in G14 G15 G16 G17 G18 G19 G20 G21 G22 G23 G24 G25 G26; do
  eval "up_$_id() { true; }"
done
port_verify() { # ID : check every proto:port the registry declares for it
  local spec p proto port bad=""
  spec=$(ports_of "$1")
  for p in $spec; do
    proto=${p%%:*}
    port=${p#*:}
    probe up "$proto" "$VHOST" "$port" >/dev/null 2>&1 || bad="$bad $p"
  done
  if [ -n "$bad" ]; then echo "listener missing on:$bad"; return 2; fi
  echo "listening: $spec (port-only emulator: exposure/reach test, protocol not emulated)"
}
for _id in G14 G15 G16 G17 G18 G19 G20 G21 G22 G23 G24 G25 G26; do
  eval "verify_$_id() { port_verify $_id; }"
done

# ── registry helpers ──────────────────────────────────────────────────────────

sev_rank() { case "$1" in C) echo 3 ;; H) echo 2 ;; M) echo 1 ;; *) echo 0 ;; esac; }
sev_name() { case "$1" in C) echo CRIT ;; H) echo HIGH ;; M) echo MED ;; *) echo ctrl ;; esac; }

ports_of() { # ID -> its "proto:port" list
  printf '%s' "$REG" | awk -F'|' -v id="$1" '$1==id{print $5}'
}

in_csv() { case ",$2," in *",$1,"*) return 0 ;; *) return 1 ;; esac; }

selected() { # ID SEV TYPE
  local id="$1" sev="$2" type="$3"
  if [ "$type" = "CONTROL" ]; then
    [ "$WITH_CONTROLS" -eq 1 ] || return 1
  else
    [ "$(sev_rank "$sev")" -ge "$MIN_RANK" ] || return 1
  fi
  if [ -n "$ONLY" ] && ! in_csv "$id" "$ONLY"; then return 1; fi
  if [ -n "$SKIP" ] && in_csv "$id" "$SKIP"; then return 1; fi
  return 0
}

rec() { # ID STATUS DETAIL
  local d
  d=$(printf '%s' "$3" | tr '\n\t' '  ' | cut -c1-170)
  printf '%s\t%s\t%s\n' "$1" "$2" "$d" >>"$RESULTS"
}

result_of() { awk -F'\t' -v id="$1" '$1==id{r=$2"\t"$3} END{print r}' "$RESULTS" 2>/dev/null; }

# ── firewall (installed BEFORE any service starts) ────────────────────────────

collect_ports() { # fills TCP_PORTS / UDP_PORTS from the selected scenarios
  TCP_PORTS=""
  UDP_PORTS=""
  LISTEN_TCP=""
  LISTEN_UDP=""
  local id sev type name ports p
  while IFS='|' read -r id sev type name ports; do
    [ -n "$id" ] || continue
    selected "$id" "$sev" "$type" || continue
    for p in $ports; do
      case "$p" in
        tcp:*) TCP_PORTS="$TCP_PORTS ${p#tcp:}"; [ "$type" = PORTONLY ] && LISTEN_TCP="$LISTEN_TCP,${p#tcp:}" ;;
        udp:*) UDP_PORTS="$UDP_PORTS ${p#udp:}"; [ "$type" = PORTONLY ] && LISTEN_UDP="$LISTEN_UDP,${p#udp:}" ;;
      esac
    done
  done <<EOF
$REG
EOF
  LISTEN_TCP="${LISTEN_TCP#,}"
  LISTEN_UDP="${LISTEN_UDP#,}"
  if [ "${MERGE_PORTS:-0}" -eq 1 ] && [ -r "$CONF_DIR/lab.conf" ]; then
    # A partial re-run (--only / retry-failed) must NOT shrink the firewall or the shared
    # listener: keep every port a previous run already opened.
    TCP_PORTS=$(merge_list " " "$(conf_get TCP_PORTS)" "$TCP_PORTS")
    UDP_PORTS=$(merge_list " " "$(conf_get UDP_PORTS)" "$UDP_PORTS")
    LISTEN_TCP=$(merge_list "," "$(conf_get LISTEN_TCP)" "$LISTEN_TCP")
    LISTEN_UDP=$(merge_list "," "$(conf_get LISTEN_UDP)" "$LISTEN_UDP")
  fi
}

conf_get() { sed -n "s/^$1=\"\\(.*\\)\"\$/\\1/p" "$CONF_DIR/lab.conf" 2>/dev/null | tail -n 1; }

merge_list() { # separator list... -> de-duplicated list joined by separator
  local sep="$1"
  shift
  printf '%s\n' "$@" | tr ' ,' '\n\n' | grep -v '^$' | sort -u | tr '\n' "$sep" | sed "s/[$sep]\$//"
}

write_lab_conf() {
  cat >"$CONF_DIR/lab.conf" <<EOF
ALLOW_CIDR="$ALLOW_CIDR"
TCP_PORTS="$TCP_PORTS"
UDP_PORTS="$UDP_PORTS"
LISTEN_TCP="$LISTEN_TCP"
LISTEN_UDP="$LISTEN_UDP"
EOF
}

fw_apply() {
  [ -r "$CONF_DIR/lab.conf" ] || die "no $CONF_DIR/lab.conf"
  # shellcheck disable=SC1091
  . "$CONF_DIR/lab.conf"
  local p c
  for c in iptables ip6tables; do
    command -v "$c" >/dev/null 2>&1 || continue
    "$c" -N "$CHAIN" 2>/dev/null || "$c" -F "$CHAIN"
    "$c" -C INPUT -j "$CHAIN" 2>/dev/null || "$c" -I INPUT 1 -j "$CHAIN"
    if [ "$c" = iptables ]; then
      for p in $(cat "$CONF_DIR/blind.tcp" 2>/dev/null); do "$c" -A "$CHAIN" ! -i lo -p tcp --dport "$p" -j DROP; done
      for p in $(cat "$CONF_DIR/blind.udp" 2>/dev/null); do "$c" -A "$CHAIN" ! -i lo -p udp --dport "$p" -j DROP; done
    fi
    "$c" -A "$CHAIN" -i lo -j RETURN
    [ "$c" = iptables ] && "$c" -A "$CHAIN" -s "$ALLOW_CIDR" -j RETURN
    for p in $TCP_PORTS; do "$c" -A "$CHAIN" -p tcp --dport "$p" -j DROP; done
    for p in $UDP_PORTS; do "$c" -A "$CHAIN" -p udp --dport "$p" -j DROP; done
  done
}

fw_remove() {
  local c
  for c in iptables ip6tables; do
    command -v "$c" >/dev/null 2>&1 || continue
    while "$c" -D INPUT -j "$CHAIN" 2>/dev/null; do :; done
    "$c" -F "$CHAIN" 2>/dev/null
    "$c" -X "$CHAIN" 2>/dev/null
  done
}

install_firewall() {
  pkg iptables
  write_lab_conf
  cat >/etc/systemd/system/vedha-lab-firewall.service <<EOF
[Unit]
Description=Vedha lab firewall (lab ports reachable only from the allowed CIDR)
DefaultDependencies=no
Before=network-pre.target
Wants=network-pre.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=$LAB_DIR/lab.sh fw-apply

[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl enable vedha-lab-firewall.service >/dev/null 2>&1
  fw_apply
  iptables -S "$CHAIN" >/dev/null 2>&1 || { echo "lab firewall chain was not created"; return 1; }
}

# ── engine ────────────────────────────────────────────────────────────────────

run_one() { # ID SEV TYPE NAME
  local id="$1" log="$LOG_DIR/$1.log" out rc
  : >"$log"
  ( set -e; "up_$id" ) >>"$log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then
    rec "$id" FAILED "setup failed (rc=$rc): $(grep -v '^$' "$log" | tail -n 1) [log: $log]"
    return
  fi
  out=$("verify_$id" 2>&1)
  rc=$?
  case $rc in
    0) rec "$id" VERIFIED "$out" ;;
    3) rec "$id" UNCONFIRMED "$out" ;;
    *) rec "$id" FAILED "$out [log: $log]" ;;
  esac
}

live_echo() { # one human-readable line per scenario, as soon as it finishes
  local r st detail
  r=$(result_of "$1")
  st=${r%%$'\t'*}
  detail=${r#*$'\t'}
  case "$st" in
    VERIFIED)    printf '      -> CREATED and VERIFIED   %s\n' "$detail" ;;
    UNCONFIRMED) printf '      -> CREATED, weakness not independently proven   %s\n' "$detail" ;;
    *)           printf '      -> NOT CREATED / FAILED   %s\n' "$detail" ;;
  esac
}

run_selected() { # mode: build | verify
  local mode="$1" id sev type name ports
  while IFS='|' read -r id sev type name ports; do
    [ -n "$id" ] || continue
    selected "$id" "$sev" "$type" || continue
    printf '  [%s] %s ...\n' "$id" "$name"
    if [ "$mode" = build ]; then
      run_one "$id" "$sev" "$type" "$name"
    else
      local out rc
      out=$("verify_$id" 2>&1)
      rc=$?
      case $rc in 0) rec "$id" VERIFIED "$out" ;; 3) rec "$id" UNCONFIRMED "$out" ;; *) rec "$id" FAILED "$out" ;; esac
    fi
    live_echo "$id"
  done <<EOF
$REG
EOF
}

print_report() {
  local id sev type name ports r st detail nv=0 nu=0 nf=0 shown=0
  {
    echo
    echo "================ VEDHA WEAK LAB REPORT  (script $SCRIPT_VERSION, host $(hostname), $(date '+%Y-%m-%d %H:%M %Z')) ================"
    printf '%-4s %-5s %-9s %-52s %-12s %s\n' ID SEV TYPE SCENARIO RESULT DETAIL
    while IFS='|' read -r id sev type name ports; do
      [ -n "$id" ] || continue
      r=$(result_of "$id")
      [ -n "$r" ] || continue
      st=${r%%$'\t'*}
      detail=${r#*$'\t'}
      shown=$((shown + 1))
      case "$st" in VERIFIED) nv=$((nv + 1)) ;; UNCONFIRMED) nu=$((nu + 1)) ;; *) nf=$((nf + 1)) ;; esac
      printf '%-4s %-5s %-9s %-52s %-12s %s\n' "$id" "$(sev_name "$sev")" "$type" "$(printf '%s' "$name" | cut -c1-52)" "$st" "$detail"
    done <<EOF
$REG
EOF
    echo
    echo "SUMMARY: $shown scenarios/controls -> $nv VERIFIED, $nu UNCONFIRMED (up, weakness not independently proven), $nf FAILED"
    if [ "$nf" -gt 0 ]; then
      echo
      echo "FAILED:"
      # latest status per ID only: earlier FAILED rows of since-fixed scenarios must not show
      awk -F'\t' '{s[$1]=$2; d[$1]=$3} END{for(i in s) if(s[i]=="FAILED") printf "  %s  %s\n", i, d[i]}' "$RESULTS" | sort
    fi
    echo
    echo "NOT HOSTABLE ON THIS UBUNTU HOST (no scenario created):"
    printf '%s\n' "$SKIPPED" | awk -F'|' '{printf "  %-12s %-52s %s\n", $1, $2, $3}'
    echo
    echo "$EXCLUDED_NOTE"
    echo "TYPE: REAL = real product/config; EMULATED = protocol emulator (fingerprint tier, not product-validated);"
    echo "      PORTONLY = listener only (tests reach/exposure); CONTROL = safe twin that must NOT be flagged."
    echo "Sources of truth: logs in $LOG_DIR ; results in $RESULTS"
  } >"$STATE_DIR/last-report.txt"
  cat "$STATE_DIR/last-report.txt"
  [ "$nf" -eq 0 ]
}

# ── commands ──────────────────────────────────────────────────────────────────

parse_flags() {
  ALLOW_CIDR=""; ACK=0; ONLY=""; SKIP=""; MIN_SEV="medium"; WITH_CONTROLS=1; PURGE=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --allow-cidr) ALLOW_CIDR="${2:-}"; shift ;;
      --i-understand-isolated-lab) ACK=1 ;;
      --only) ONLY="${2:-}"; shift ;;
      --skip) SKIP="${2:-}"; shift ;;
      --min-severity) MIN_SEV="${2:-}"; shift ;;
      --verify-host) VHOST="${2:-}"; shift ;;
      --no-controls) WITH_CONTROLS=0 ;;
      --purge) PURGE=1 ;;
      *) die "unknown option: $1" ;;
    esac
    shift
  done
  case "$MIN_SEV" in medium) MIN_RANK=1 ;; high) MIN_RANK=2 ;; critical) MIN_RANK=3 ;; *) die "--min-severity: medium|high|critical" ;; esac
}

cmd_list() {
  register_all
  parse_flags "$@"
  printf '%-4s %-5s %-9s %-62s %s\n' ID SEV TYPE SCENARIO PORTS
  local id sev type name ports
  while IFS='|' read -r id sev type name ports; do
    [ -n "$id" ] || continue
    selected "$id" "$sev" "$type" || continue
    printf '%-4s %-5s %-9s %-62s %s\n' "$id" "$(sev_name "$sev")" "$type" "$name" "$ports"
  done <<EOF
$REG
EOF
  echo
  echo "NOT HOSTABLE ON UBUNTU:"
  printf '%s\n' "$SKIPPED" | awk -F'|' '{printf "  %-12s %-52s %s\n", $1, $2, $3}'
  echo "$EXCLUDED_NOTE"
}

cmd_up() {
  need_root; check_os; ensure_dirs
  [ -n "$ALLOW_CIDR" ] || die "--allow-cidr is required (the scanner's network, e.g. 192.168.56.0/24)"
  cidr_ok "$ALLOW_CIDR" || die "--allow-cidr must be inside 10/8, 172.16/12, 192.168/16 or 100.64/10"
  [ "$ACK" -eq 1 ] || die "pass --i-understand-isolated-lab: this makes the host deliberately vulnerable"
  local pub
  pub=$(public_iface_ips)
  [ -z "$pub" ] || die "this host has public IPv4 address(es): $pub. Use an isolated lab VM."
  warn "If this VM sits behind NAT / a cloud public IP, also lock the security group. The host firewall below only allows $ALLOW_CIDR."
  register_all
  if [ -n "$ONLY" ]; then touch "$RESULTS"; else : >"$RESULTS"; fi   # partial run keeps earlier results
  MERGE_PORTS=1
  say "== base tools"
  pkg python3 iproute2 curl ca-certificates dnsutils nfs-common ldap-utils snmp rsync openssl openssh-client \
    || warn "some verifier tools failed to install; their checks will report FAILED"
  install -m 0755 "$SRC_DIR/lab_emulators.py" "$LAB_DIR/lab_emulators.py"
  install -m 0755 "$SRC_DIR/lab_probe.py" "$LAB_DIR/lab_probe.py"
  install -m 0755 "${BASH_SOURCE[0]}" "$LAB_DIR/lab.sh"
  collect_ports
  say "== firewall first: lab ports reachable only from $ALLOW_CIDR"
  install_firewall || die "could not install the lab firewall; nothing was started"
  VLAN=$(lan_ip)
  if [ -n "$LISTEN_TCP$LISTEN_UDP" ]; then
    say "== shared port-only listener"
    ( set -e; emu listen ${LISTEN_TCP:+--tcp "$LISTEN_TCP"} ${LISTEN_UDP:+--udp "$LISTEN_UDP"} ) >"$LOG_DIR/listen.log" 2>&1 \
      || warn "port-only listener failed to start (see $LOG_DIR/listen.log); G14-G26 will report FAILED"
  fi
  say "== building scenarios"
  run_selected build
  print_report
}

cmd_retry() { # rebuild only what FAILED last time; keeps every other scenario and its firewall rules
  need_root; ensure_dirs
  [ -s "$RESULTS" ] || die "no previous results in $RESULTS; run 'up' first"
  ONLY=$(awk -F'\t' '{r[$1]=$2} END{for(i in r) if(r[i]=="FAILED") printf "%s,", i}' "$RESULTS" | sed 's/,$//')
  if [ -z "$ONLY" ]; then
    say "nothing FAILED in the last run"
    return 0
  fi
  if [ -z "$ALLOW_CIDR" ]; then ALLOW_CIDR=$(conf_get ALLOW_CIDR); fi
  ACK=1                                  # already acknowledged by the original 'up'
  say "retrying only: $ONLY (allowed network: $ALLOW_CIDR)"
  cmd_up
}

cmd_verify() {
  check_os; ensure_dirs; register_all
  [ -r "$CONF_DIR/lab.conf" ] || die "lab not built (no $CONF_DIR/lab.conf); run 'up' first"
  [ -f "$LAB_DIR/lab_probe.py" ] || die "lab not built"
  VLAN=$(lan_ip)
  if [ -n "$ONLY" ]; then touch "$RESULTS"; else : >"$RESULTS"; fi
  say "== re-verifying (no changes made)"
  run_selected verify
  print_report
}

cmd_blind() { # port [tcp|udp]
  need_root
  local port="${1:-}" proto="${2:-both}"
  [ -n "$port" ] || die "usage: blind PORT [tcp|udp]"
  case "$proto" in tcp|both) echo "$port" >>"$CONF_DIR/blind.tcp" ;; esac
  case "$proto" in udp|both) echo "$port" >>"$CONF_DIR/blind.udp" ;; esac
  fw_apply
  say "port $port ($proto) now DROPPED for everything except loopback. Expect the scanner to report no-evidence, never clean."
}

cmd_unblind() {
  need_root
  local port="${1:-}"
  [ -n "$port" ] || die "usage: unblind PORT"
  local f
  for f in blind.tcp blind.udp; do
    [ -f "$CONF_DIR/$f" ] && grep -vx "$port" "$CONF_DIR/$f" >"$CONF_DIR/$f.new" && mv "$CONF_DIR/$f.new" "$CONF_DIR/$f"
  done
  fw_apply
  say "port $port restored"
}

cmd_down() {
  need_root
  say "== stopping lab units"
  local u
  if [ -f "$STATE_DIR/units.txt" ]; then
    for u in $(sort -u "$STATE_DIR/units.txt"); do
      systemctl disable --now "$u" >/dev/null 2>&1
      rm -f "/etc/systemd/system/$u"
    done
  fi
  systemctl disable --now vedha-lab-firewall.service >/dev/null 2>&1
  fw_remove
  rm -f /etc/systemd/system/vedha-lab-firewall.service
  systemctl daemon-reload
  say "== restoring configs"
  if [ -d "$STATE_DIR/backup" ]; then
    local f rel
    find "$STATE_DIR/backup" -type f | while read -r f; do
      rel=${f#"$STATE_DIR/backup"}
      case "$rel" in
        *.absent) rm -f "${rel%.absent}" ;;
        *) mkdir -p "$(dirname "$rel")"; cp -a "$f" "$rel" ;;
      esac
    done
  fi
  rm -f /etc/exports.d/vedha-lab.exports /etc/nfs.conf.d/vedha-lab.conf /etc/mosquitto/conf.d/vedha-lab.conf \
    /etc/mysql/mariadb.conf.d/99-vedha-lab.cnf /etc/tinyproxy/lab-filter
  a2disconf vedha-lab >/dev/null 2>&1
  rm -f /etc/apache2/conf-available/vedha-lab.conf
  for u in /srv/lab/web/dav /srv/lab/ftp/upload; do mountpoint -q "$u" && umount "$u"; done
  sed -i '/# vedha-lab$/d' /etc/fstab
  if [ -f "$STATE_DIR/touched-svcs.txt" ]; then
    for u in $(sort -u "$STATE_DIR/touched-svcs.txt"); do
      case "$u" in vedha-lab-*) ;; *) systemctl restart "$u" >/dev/null 2>&1 ;; esac
    done
  fi
  if [ "$PURGE" -eq 1 ] && [ -f "$STATE_DIR/new-pkgs.txt" ]; then
    say "== purging packages this script installed"
    # shellcheck disable=SC2046
    DEBIAN_FRONTEND=noninteractive apt-get purge -y -qq $(sort -u "$STATE_DIR/new-pkgs.txt") || warn "purge reported errors"
  else
    say "packages were kept (use 'down --purge' to remove the ones this script added)"
  fi
  rm -rf "$CONF_DIR" "$LAB_DIR" /srv/lab
  say "lab removed. State/logs kept in $STATE_DIR"
}

# Engine self-test with fake scenarios: proves the report logic without touching the host.
cmd_engine_selftest() {
  STATE_DIR="$(mktemp -d)"; LOG_DIR="$STATE_DIR/logs"; RESULTS="$STATE_DIR/results.tsv"
  mkdir -p "$LOG_DIR"; : >"$RESULTS"
  WITH_CONTROLS=1; MIN_RANK=1; ONLY=""; SKIP=""
  REG=""
  reg F01 C REAL     "passes setup and verification"      "tcp:1"
  reg F02 H EMULATED "setup command fails"                "tcp:2"
  reg F03 M REAL     "up but weakness not proven"         "tcp:3"
  reg F04 H REAL     "setup ok, verification says absent" "tcp:4"
  reg F05 M PORTONLY "unreachable after setup"            "tcp:5"
  reg F06 -  CONTROL "control stays clean"                "tcp:6"
  up_F01() { true; };            verify_F01() { echo "weakness confirmed"; return 0; }
  up_F02() { echo "boom"; false; };   verify_F02() { return 0; }
  up_F03() { true; };            verify_F03() { echo "service up"; return 3; }
  up_F04() { true; };            verify_F04() { echo "service is up but NOT weak"; return 1; }
  up_F05() { true; };            verify_F05() { echo "unreachable"; return 2; }
  up_F06() { true; };            verify_F06() { echo "control is clean"; return 0; }
  SKIPPED="X01|example skipped scenario|reason shown here"
  run_selected build
  print_report
  local rc=$?
  local want="F01 VERIFIED|F02 FAILED|F03 UNCONFIRMED|F04 FAILED|F05 FAILED|F06 VERIFIED" got=""
  local i
  for i in F01 F02 F03 F04 F05 F06; do got="${got:+$got|}$i $(result_of "$i" | cut -f1)"; done
  if [ "$got" = "$want" ] && [ "$rc" -ne 0 ]; then
    say "ENGINE SELFTEST: PASS (statuses as expected; exit code non-zero because of FAILED rows)"
    return 0
  fi
  say "ENGINE SELFTEST: FAIL  got=[$got]"
  return 1
}

usage() {
  local me
  me=$(basename "${BASH_SOURCE[0]}")
  awk 'NR>1 && /^#/ {sub(/^# ?/,""); print; next} NR>1 {exit}' "${BASH_SOURCE[0]}" \
    | sed "s#ubuntu-weak-lab\\.sh#$me#g"
  echo
  echo "Nothing was changed. To build the scenarios, run:"
  echo "  sudo ./$me up --allow-cidr <your scanner's network, e.g. 192.168.56.0/24> --i-understand-isolated-lab"
}

main() {
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    up)       parse_flags "$@"; cmd_up ;;
    verify)   parse_flags "$@"; cmd_verify ;;
    retry-failed) parse_flags "$@"; cmd_retry ;;
    down)     parse_flags "$@"; cmd_down ;;
    blind)    cmd_blind "$@" ;;
    unblind)  cmd_unblind "$@" ;;
    list)     cmd_list "$@" ;;
    report)   cat "$STATE_DIR/last-report.txt" 2>/dev/null || die "no report yet" ;;
    fw-apply) need_root; fw_apply ;;
    engine-selftest) cmd_engine_selftest ;;
    ""|-h|--help|help) usage ;;
    *) die "unknown command: $cmd (try --help)" ;;
  esac
}

main "$@"
