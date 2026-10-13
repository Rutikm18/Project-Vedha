# Ubuntu weak lab — build the network-VA scenarios on one VM

One script creates the Linux-hostable scenarios from the
[scenario catalogue](../../../../docs/testing/2026-10-10-network-va-scenario-catalogue.md),
verifies each one **independently of Vedha's own scanners**, and prints a final report of
what was **VERIFIED**, **UNCONFIRMED** and **FAILED**.

Scope: **Critical, High and Medium** only (48 rows = 45 scenarios + 3 safe controls).
Low/Info checks are excluded on purpose.

## Single-file edition (Critical + High only)

`vedha-weak-lab.sh` is one self-contained file: the emulators and the independent verifier are
embedded, so you can copy just this file to the Ubuntu VM. It builds only the **25 Critical and
High** scenarios, no safe controls unless you pass `--with-controls`, and it refuses to build
anything below High. After every scenario it echoes `CREATED and VERIFIED`, `CREATED, weakness
not independently proven`, or `NOT CREATED / FAILED`, then prints the full table at the end.

```bash
scp vedha-weak-lab.sh ubuntu@lab-vm:~
sudo ./vedha-weak-lab.sh up --allow-cidr 192.168.56.0/24 --i-understand-isolated-lab
```

It is generated: edit the three source files, then run `python3 build_onefile.py`.
Everything below applies to both editions; the multi-file `ubuntu-weak-lab.sh` defaults to
Medium and above instead.

## Run it

Use a **throwaway Ubuntu 22.04/24.04 VM on an isolated network** (not a laptop, not a cloud
host with a public IP, not a machine with data you care about).

```bash
cd probe/tests/rig/ubuntu-weak-lab
./ubuntu-weak-lab.sh list                         # what will be built, and what cannot be
sudo ./ubuntu-weak-lab.sh up --allow-cidr 192.168.56.0/24 --i-understand-isolated-lab
sudo ./ubuntu-weak-lab.sh verify                  # re-check everything, change nothing
sudo ./ubuntu-weak-lab.sh blind 3306              # blind control: scanner can no longer reach 3306
sudo ./ubuntu-weak-lab.sh unblind 3306
sudo ./ubuntu-weak-lab.sh down --purge            # remove units, restore configs, drop firewall
```

`--allow-cidr` is the network your **scanner/probe** sits on. It must be RFC1918 or CGNAT.
Useful options: `--only T01,G03`, `--skip T13`, `--min-severity high`, `--verify-host IP`,
`--no-controls`.

## Reading the report

| Result | Meaning |
|---|---|
| **VERIFIED** | Built, and an independent probe confirmed the weakness (or, for a control, that it is clean) |
| **UNCONFIRMED** | Service is up, but the weakness is not independently proven (e.g. IKE aggressive mode) |
| **FAILED** | Setup failed, the service is down, or it is up but **not** weak. The detail and a log path are printed. |

| Type | Fidelity |
|---|---|
| **REAL** | The real product, configured weakly |
| **EMULATED** | A protocol emulator (IPMI, RTSP, ADB, CWMP, Ollama API, UPnP, NTP monlist, SIP). A detection here is **fingerprint tier**, not product-validated. |
| **PORTONLY** | A listener only (G14–G26). Tests reach and exposure; the protocol is not emulated. |
| **CONTROL** | A safe twin (C01–C03) that must **not** be flagged. |

The script exits non-zero if anything FAILED. The report also lists what is **not hostable on
Ubuntu** (Windows posture, AD, vulnerable-OpenSSL, appliances) so nothing silently disappears.

Every scenario also needs a **blind control**: run `blind PORT` and confirm the scanner
reports *no evidence*, never *clean*.

## What keeps this safe

* Refuses to run without `--allow-cidr` and `--i-understand-isolated-lab`, refuses non-private
  CIDRs, and refuses a host that has a public IPv4 address on an interface.
* The firewall chain `VEDHA_LAB` is installed **before any service starts** and re-applied at boot
  (before the network is up), so lab ports are reachable only from the allowed CIDR.
* SMTP open relay **discards** mail. Redis has `CONFIG`, `SLAVEOF`, `MODULE`, `DEBUG`, `FLUSH*`
  disabled. FTP and WebDAV uploads go to small tmpfs mounts. UDP emulators are rate-limited and
  answer port-only probes with one byte. The open proxy can only reach `example.invalid`.
* Rogue DHCP is **refused by design**; it would disrupt the LAN.
* If the VM is behind NAT or a cloud public IP, **also** lock the security group.

## Tests of the tooling itself (no root, no packages)

```bash
./selftest.sh                                     # emulators vs the lab verifier, incl. dead-port controls
python3 selftest_vs_scanners.py                   # emulators vs the REAL probe scanners (use the probe venv)
./ubuntu-weak-lab.sh engine-selftest              # report/exit-code logic with fake scenarios
```

## Honest limits

* The package-based scenarios (sshd, dropbear, x11vnc, slapd, bind9, NFS, rsync, Redis, MariaDB,
  OpenSSL s_server, Apache, Mosquitto, snmpd, tftpd, vsftpd, Postfix, strongSwan, Avahi, Samba,
  tinyproxy) were **written but not yet run on a real Ubuntu VM**. The first run is the real test;
  expect to fix a config or two. The report tells you which.
* Verified only on macOS so far: the emulators, the verifier, the report logic, the CIDR guard.
* The NTP monlist emulator is a deliberate amplifier. Keep the firewall on.
* Scenario severities for the G-rows come from the Shadowserver rating or the planned rule; the
  rules for most G-rows are not built yet, so the lab gives you the target, not the finding.
