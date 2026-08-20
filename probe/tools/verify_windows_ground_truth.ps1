<#
    verify_windows_ground_truth.ps1
    ---------------------------------------------------------------------------
    Target-side ground truth for cross-checking a Vedha probe scan of THIS host.
    Run it ON the Windows machine the probe scanned, then compare each section to
    the probe's JSON findings (open_ports, smb{}, tls{}, snmp{}, ...).

    READ-ONLY — it changes nothing. Run in an ELEVATED PowerShell for full detail:
        powershell -ExecutionPolicy Bypass -File .\verify_windows_ground_truth.ps1

    Probe reported for 192.168.1.74 (DESKTOP-34M18MB) — expected ground truth:
      open TCP     : 135, 445, 3389 (+2179, 7680 on full-port)
      SMB          : SMBv1 OFF, signing REQUIRED, dialect 0x0302 (SMB 3.0.2)
      RDP 3389     : TLS1.2/1.3, grade A, self-signed cert CN=DESKTOP-34M18MB
      SNMP 161     : no response  (service not installed/running)
      memcached/DNS: NOT real services (UDP open|filtered artifacts)
#>
#requires -Version 5.1
$ErrorActionPreference = 'SilentlyContinue'
function Section($t) { Write-Host "`n===== $t =====" -ForegroundColor Cyan }

Section "HOST"
$os = Get-CimInstance Win32_OperatingSystem
"Hostname : $env:COMPUTERNAME"
"OS       : $($os.Caption)  build $($os.BuildNumber)"
"IPv4     : " + ((Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -notlike '127.*' } |
    Select-Object -Expand IPAddress) -join ', ')

function Scope($addr) {
    if ($addr -in '127.0.0.1', '::1') { 'loopback' }         # NOT network-reachable
    elseif ($addr -in '0.0.0.0', '::') { 'ALL-ifaces' }      # reachable (subject to firewall)
    else { $addr }                                            # a specific interface only
}

Section "WINDOWS FIREWALL  (blocks unsolicited inbound -> explains open|filtered)"
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction | Format-Table -AutoSize

Section "LISTENING TCP PORTS  (LocalAddress decides network reachability)"
"Only 'ALL-ifaces' or the .74 address can be reached externally; 'loopback' never is."
Get-NetTCPConnection -State Listen |
    Sort-Object LocalPort, LocalAddress -Unique |
    Select-Object LocalPort,
        @{ n = 'Bind';    e = { Scope $_.LocalAddress } },
        @{ n = 'Address'; e = { $_.LocalAddress } },
        @{ n = 'Process'; e = { (Get-Process -Id $_.OwningProcess).ProcessName } },
        @{ n = 'PID';     e = { $_.OwningProcess } } |
    Format-Table -AutoSize

Section "LISTENING UDP ENDPOINTS  (with bind address)"
Get-NetUDPEndpoint |
    Sort-Object LocalPort, LocalAddress -Unique |
    Select-Object LocalPort,
        @{ n = 'Bind';    e = { Scope $_.LocalAddress } },
        @{ n = 'Address'; e = { $_.LocalAddress } },
        @{ n = 'Process'; e = { (Get-Process -Id $_.OwningProcess).ProcessName } } |
    Format-Table -AutoSize

Section "SMB SERVER CONFIG  (verify probe's smb{} findings)"
$smb = Get-SmbServerConfiguration
[pscustomobject]@{
    EnableSMB1Protocol       = $smb.EnableSMB1Protocol        # probe: SMBv1 off  -> expect False
    EnableSMB2Protocol       = $smb.EnableSMB2Protocol
    RequireSecuritySignature = $smb.RequireSecuritySignature  # probe: signing required -> expect True
    EnableSecuritySignature  = $smb.EnableSecuritySignature
} | Format-List
"Note: probe negotiated dialect 0x0302 (SMB 3.0.2). The negotiated value is the"
"min of both sides' max; a Win10/11 server itself supports up to 3.1.1 (0x0311)."

Section "RDP CONFIG  (verify 3389 exposure / NLA / TLS layer)"
$ts     = Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server'
$rdpTcp = Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp'
[pscustomobject]@{
    RDP_Enabled   = ($ts.fDenyTSConnections -eq 0)   # probe found 3389 open -> expect True
    NLA_Required  = ($rdpTcp.UserAuthentication -eq 1)
    SecurityLayer = $rdpTcp.SecurityLayer            # 2 = TLS  (matches probe grade-A TLS)
} | Format-List

Section "SCHANNEL TLS PROTOCOLS  (verify TLS1.2/1.3 only, no 1.0/1.1)"
$base = 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols'
foreach ($p in 'TLS 1.0', 'TLS 1.1', 'TLS 1.2', 'TLS 1.3') {
    $s = Get-ItemProperty "$base\$p\Server" -ErrorAction SilentlyContinue
    if ($null -eq $s) { "{0,-8}: (key absent = OS default)" -f $p }
    else { "{0,-8}: Enabled={1} DisabledByDefault={2}" -f $p, $s.Enabled, $s.DisabledByDefault }
}

Section "SNMP SERVICE  (verify probe's 'no_snmp_response')"
$snmp = Get-Service -Name SNMP* -ErrorAction SilentlyContinue
if ($snmp) { $snmp | Select-Object Name, Status | Format-Table -AutoSize }
else { "SNMP service NOT installed -> matches probe (no_snmp_response)" }

Section "SERVICES THE PROBE MARKED open|filtered ON UDP  (should NOT exist)"
foreach ($svc in @('memcached', 'DNS', 'ntp', 'w3svc', 'mysql', 'postgres', 'redis')) {
    $found = Get-Service | Where-Object { $_.Name -like "*$svc*" -or $_.DisplayName -like "*$svc*" }
    if ($found) { $found | Select-Object Name, Status | Format-Table -AutoSize }
    else { "no '$svc' service -> confirms probe (no real service; UDP open|filtered was ambiguous)" }
}

Write-Host "`nDone. Diff each section against the probe JSON to score accuracy." -ForegroundColor Green
