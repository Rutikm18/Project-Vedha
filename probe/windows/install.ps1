<#
.SYNOPSIS
  Vedha agent - one-command installer for Windows.

.DESCRIPTION
  Installs the Vedha agent as a background task that starts at boot, connects it to
  your Vedha manager, and tells you plainly whether it worked. Everything the agent
  needs is inside this package: nothing is downloaded and no other software is needed.

  If anything goes wrong the installer says what it saw and the exact fix, and writes
  a log you can send to Vedha support (see: vedha-agent.exe support-bundle).

.EXAMPLE
  install.cmd -Token vet_XXXXXXXX
  Install and connect using the one-time install token shown in Fleet.

.EXAMPLE
  install.cmd -Token vet_XXXXXXXX -Proxy http://proxy.example.local:3128 -CaBundle C:\certs\company-root.pem
  Behind a web proxy that inspects HTTPS.

.EXAMPLE
  install.cmd -Repair        # re-apply the installation and re-check it (keeps the agent's identity)
  install.cmd -Uninstall     # remove the agent (add -Purge to also delete its identity and logs)

.EXAMPLE
  install.cmd -Repair        # run from a NEWER package: updates the installed agent in place
  An installed agent is updated in place: its identity, settings and scan results are kept and the old
  program files are removed. A package OLDER than the installed agent is refused unless you add
  -AllowDowngrade.

.NOTES
  This installer never changes your firewall, proxy, antivirus or certificate settings.

  An update can undo itself: the previous program folder, settings and identity are kept until the new
  agent has connected (up to 5 minutes). If it does not, the previous version is put back, the result is
  written to ProgramData\vedha-agent\update\last-update.json, and the installer exits with code 4.
  Exit codes: 0 done (connected, or waiting for approval) | 1 failed, nothing changed | 3 installed but
  not connected yet (fresh install or repair) | 4 update undone, previous version restored.
#>
[CmdletBinding()]
param(
  [string]$Token = '',        # one-time install token from Fleet (vet_...)
  [string]$TokenFile = '',    # read the token from a file instead of the command line
  [string]$Manager = '',      # manager address; the package normally carries it already
  [string]$Scope = '',        # networks this agent may scan, e.g. 192.168.1.0/24 (default: this computer's network)
  [string]$Proxy = '',        # web proxy for the agent, e.g. http://proxy:3128
  [string]$CaBundle = '',     # your company's root certificate (.pem) when HTTPS is inspected
  [string]$Name = '',         # name shown in Fleet (default: <computer name>-probe)
  [switch]$Repair,
  [switch]$Uninstall,
  [switch]$Purge,
  [switch]$AllowDowngrade,    # install even if the installed agent is newer than this package
  [switch]$NoWait,            # register and start, but do not wait to see it connect
  [switch]$SkipPreflight,     # skip the pre-install network check (not recommended)
  [switch]$NoPause,
  [switch]$Pairing,           # no install token: do not ask for one; the agent shows a pairing code to approve in Fleet
  [switch]$ElevatedChild      # internal: set when this script re-launched itself as administrator
)

# The arguments this script was started with (a function's own $PSBoundParameters would be empty).
$script:BoundParams = $PSBoundParameters

# Values the package builder fills in. Left as-is in a source checkout.
$BakedManager   = '__VEDHA_MANAGER_URL__'
$PackageVersion = '__VEDHA_PACKAGE_VERSION__'

$TaskName   = 'VedhaAgent'
$WaitSeconds = 120
$UpgradeWaitSeconds = 300   # replacing a working agent: give the new one longer before undoing the update

# ---------------------------------------------------------------------------
# Pure helpers (no side effects; unit-tested)
# ---------------------------------------------------------------------------

function Test-VedhaToken {
  param([string]$Value)
  return [bool]($Value -match '^vet_[A-Za-z0-9_-]{8,}$')
}

function Resolve-VedhaManager {
  # Returns the manager URL to use, or throws a message saying what to do.
  param([string]$Given, [string]$Baked, [string]$Existing = '')
  $candidate = $Given
  if (-not $candidate) { $candidate = $Existing }
  if (-not $candidate -and $Baked -and $Baked -notlike '__*') { $candidate = $Baked }
  if (-not $candidate) {
    throw 'This package does not carry a manager address. Run the installer again with -Manager https://<your manager address>.'
  }
  $candidate = $candidate.Trim().TrimEnd('/')
  if ($candidate -match '\.invalid(:\d+)?(/|$)') {
    throw "The manager address '$candidate' is a placeholder. Run the installer again with -Manager https://<your manager address>."
  }
  if ($candidate -notmatch '^https://[A-Za-z0-9.-]+(:\d+)?$') {
    throw "The manager address must look like https://manager.example.com (got '$candidate')."
  }
  return $candidate
}

function ConvertTo-NetworkCidr {
  # Network (CIDR) that contains an address with a given prefix length. Very large
  # networks are narrowed to the /24 around this computer so a scan scope is never
  # accidentally huge; the note says so and how to widen it.
  param([string]$Address, [int]$PrefixLength)
  $parsed = $null
  if (-not [System.Net.IPAddress]::TryParse($Address, [ref]$parsed) -or $parsed.AddressFamily -ne 'InterNetwork') {
    throw "Not an IPv4 address: $Address"
  }
  if ($PrefixLength -lt 1 -or $PrefixLength -gt 32) { throw "Bad prefix length: $PrefixLength" }
  $note = ''
  $prefix = $PrefixLength
  if ($prefix -lt 22) {
    $note = "This computer's network is /$PrefixLength (very large); the scan scope is limited to its /24. Pass -Scope to choose another."
    $prefix = 24
  } elseif ($prefix -gt 30) {
    $note = "This computer is on a /$PrefixLength link; the scope is that single address."
    $prefix = 32
  }
  $bytes = $parsed.GetAddressBytes()
  $ip = ([uint32]$bytes[0] -shl 24) -bor ([uint32]$bytes[1] -shl 16) -bor ([uint32]$bytes[2] -shl 8) -bor [uint32]$bytes[3]
  if ($prefix -eq 32) { $mask = [uint32]::MaxValue } else { $mask = [uint32]([math]::Pow(2, 32) - [math]::Pow(2, 32 - $prefix)) }
  $net = $ip -band $mask
  $text = '{0}.{1}.{2}.{3}' -f (($net -shr 24) -band 255), (($net -shr 16) -band 255), (($net -shr 8) -band 255), ($net -band 255)
  return [pscustomobject]@{ Cidr = "$text/$prefix"; Note = $note }
}

function Test-VedhaScope {
  param([string]$Value)
  foreach ($part in ($Value -split ',')) {
    $p = $part.Trim()
    if ($p -notmatch '^(\d{1,3}\.){3}\d{1,3}(/(\d|[12]\d|3[0-2]))?$') { return $false }
    foreach ($octet in (($p -split '/')[0] -split '\.')) { if ([int]$octet -gt 255) { return $false } }
  }
  return $true
}

function New-VedhaAgentConfig {
  # Text of agent.env: the agent's settings. One KEY=VALUE per line, no BOM.
  param(
    [Parameter(Mandatory = $true)][string]$ManagerUrl,
    [Parameter(Mandatory = $true)][string]$DataDir,
    [string]$AgentName = '',
    [string]$ScopeValue = '',
    [string]$ProxyUrl = '',
    [string]$CaBundlePath = '',
    [string]$InstallToken = '',
    [string]$InstallerVersion = '',
    [string]$BuildDigest = ''
  )
  $lines = @(
    '# Vedha agent settings. Written by install.ps1. Contains no password; do not edit while the agent runs.',
    "PLATFORM_URL=$ManagerUrl",
    'VERIFY_TLS=true',
    'LICENSE_ENFORCED=false',
    'PROBE_KEEP_RETRYING=true',
    "PROBE_NAME=$AgentName",
    "PROBE_NETWORK_SEGMENTS=$ScopeValue",
    "STATE_FILE=$DataDir\state.json",
    "RESULT_SPOOL_DIR=$DataDir\spool",
    "PROBE_RESULT_DIR=$DataDir\results",    # scan archive: inside the locked data folder, not Program Files
    "PROBE_LOG_FILE=$DataDir\logs\agent.log",
    "PROBE_STATUS_FILE=$DataDir\status.json"
  )
  if ($InstallerVersion) { $lines += "PROBE_INSTALLER_VERSION=$InstallerVersion" }
  if ($BuildDigest)      { $lines += "PROBE_BUILD_DIGEST=$BuildDigest" }
  if ($ProxyUrl)         { $lines += "HTTPS_PROXY=$ProxyUrl" }
  if ($CaBundlePath)     { $lines += "PROBE_CA_BUNDLE=$CaBundlePath" }
  if ($InstallToken)     { $lines += "PROBE_ENROLL_TOKEN=$InstallToken" }
  return ($lines -join "`r`n") + "`r`n"
}

function Read-VedhaConfig {
  # agent.env text -> hashtable (BOM tolerant).
  param([string]$Text)
  $values = @{}
  foreach ($line in ($Text.TrimStart([char]0xFEFF) -split "`r?`n")) {
    $l = $line.Trim()
    if ($l -and -not $l.StartsWith('#') -and $l.Contains('=')) {
      $i = $l.IndexOf('=')
      $values[$l.Substring(0, $i).Trim()] = $l.Substring($i + 1).Trim().Trim('"').Trim("'")
    }
  }
  return $values
}

function Remove-VedhaTokenLine {
  param([string]$Text)
  $kept = @()
  foreach ($line in ($Text -split "`r?`n")) { if ($line -notmatch '^\s*PROBE_ENROLL_TOKEN\s*=') { $kept += $line } }
  return (($kept -join "`r`n").TrimEnd() + "`r`n")
}

# Settings the installer writes itself. Anything else found in an existing agent.env was added by hand
# and is kept across an update or repair.
$script:VedhaManagedKeys = @(
  'PLATFORM_URL', 'VERIFY_TLS', 'LICENSE_ENFORCED', 'PROBE_KEEP_RETRYING', 'PROBE_NAME',
  'PROBE_NETWORK_SEGMENTS', 'STATE_FILE', 'RESULT_SPOOL_DIR', 'PROBE_RESULT_DIR', 'PROBE_LOG_FILE',
  'PROBE_STATUS_FILE', 'PROBE_INSTALLER_VERSION', 'PROBE_BUILD_DIGEST', 'HTTPS_PROXY', 'PROBE_CA_BUNDLE',
  'PROBE_ENROLL_TOKEN'
)

function Get-VedhaExtraSettingLines {
  # The KEY=VALUE lines of an existing agent.env that the installer does not manage (PROBE_DEBUG,
  # HEARTBEAT_INTERVAL, ...). Returned as they were written.
  param([string]$ExistingText)
  $kept = @()
  foreach ($line in ($ExistingText.TrimStart([char]0xFEFF) -split "`r?`n")) {
    $l = $line.Trim()
    if (-not $l -or $l.StartsWith('#') -or -not $l.Contains('=')) { continue }
    $key = $l.Substring(0, $l.IndexOf('=')).Trim()
    if (-not $key -or ($script:VedhaManagedKeys -contains $key)) { continue }
    $kept += $l
  }
  return @($kept)
}

function Add-VedhaExtraSettings {
  # Appends the kept lines to freshly generated settings text. Safe to repeat: the heading is a comment,
  # so it is never read back as a setting.
  param([string]$ConfigText, [string[]]$ExtraLines = @())
  if (-not $ExtraLines -or $ExtraLines.Count -eq 0) { return $ConfigText }
  return ($ConfigText.TrimEnd() + "`r`n# Kept from the previous settings file (the installer does not manage these):`r`n" +
          ($ExtraLines -join "`r`n") + "`r`n")
}

function Get-VedhaVersionNumber {
  # The version in agent output such as 'Vedha Probe 2.2.0'; $null when there is none.
  param([string]$Text)
  if ($Text -match '(\d+)\.(\d+)\.(\d+)') {
    return [version]('{0}.{1}.{2}' -f [int]$Matches[1], [int]$Matches[2], [int]$Matches[3])
  }
  return $null
}

function Get-VedhaUpdatePlan {
  # What installing this package would do to what is already on the computer.
  # Kind: fresh | upgrade | same | downgrade | unknown. Allowed is false only for a downgrade that was not
  # asked for: replacing a newer agent with an older one is almost always a mistake (an old download
  # folder run by habit) and the older one may be missing fixes the newer one has.
  param([bool]$InstalledPresent, $Installed, $Package, [switch]$AllowDowngrade)
  if (-not $InstalledPresent) {
    return [pscustomobject]@{ Kind = 'fresh'; Allowed = $true; Message = 'No previous installation found: installing fresh.' }
  }
  if ($null -eq $Installed -or $null -eq $Package) {
    return [pscustomobject]@{ Kind = 'unknown'; Allowed = $true
      Message = 'An agent is installed but its version could not be read (or this package''s could not); it will be replaced.' }
  }
  if ($Package -gt $Installed) {
    return [pscustomobject]@{ Kind = 'upgrade'; Allowed = $true
      Message = "Updating the installed agent $Installed -> $Package. Its identity, settings and scan results are kept; the old program files are removed." }
  }
  if ($Package -eq $Installed) {
    return [pscustomobject]@{ Kind = 'same'; Allowed = $true
      Message = "This package is the same version as the installed agent ($Installed); re-applying it." }
  }
  if ($AllowDowngrade) {
    return [pscustomobject]@{ Kind = 'downgrade'; Allowed = $true
      Message = "Replacing the installed agent $Installed with the OLDER $Package, because -AllowDowngrade was given." }
  }
  return [pscustomobject]@{ Kind = 'downgrade'; Allowed = $false
    Message = "This package ($Package) is OLDER than the installed agent ($Installed). Installing it would replace a newer agent with an older one." }
}

function Get-VedhaRollbackDecision {
  # After an update, should the previous version be put back? Only when there was a previous
  # version to go back to, the update really changed the program (a repair of the same version
  # would only bring back identical files, and the new run's output is what a person needs to see),
  # and the new agent never got to 'online' or 'awaiting-approval' within the wait.
  param([bool]$HadPrevious, [string]$Kind, [string]$State)
  if (-not $HadPrevious) { return $false }
  if ($Kind -eq 'same' -or $Kind -eq 'fresh') { return $false }
  return ($State -ne 'online' -and $State -ne 'awaiting-approval')
}

function Save-VedhaPreviousState {
  # The settings file and the identity file as they were before the update, so a rollback puts the
  # previous agent back exactly as it was. They stay inside the locked data folder.
  param([string]$DataDir)
  $saved = Join-Path (Join-Path $DataDir 'update') 'previous'
  New-Item -ItemType Directory -Force -Path $saved | Out-Null
  foreach ($name in 'agent.env', 'state.json') {
    $source = Join-Path $DataDir $name
    if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination (Join-Path $saved $name) -Force }
  }
  return $saved
}

function Remove-VedhaPreviousState {
  param([string]$SavedDir)
  if ($SavedDir -and (Test-Path -LiteralPath $SavedDir)) { Remove-Item -LiteralPath $SavedDir -Recurse -Force -ErrorAction SilentlyContinue }
}

function Write-VedhaUpdateRecord {
  # One small file that says how the last update ended; the agent logs it when it next starts.
  param([string]$DataDir, [string]$Result, [string]$From, [string]$To, [string]$Reason)
  $dir = Join-Path $DataDir 'update'
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $record = [ordered]@{ result = $Result; from = $From; to = $To; reason = $Reason; at = (Get-Date).ToUniversalTime().ToString('o') }
  Write-Utf8NoBom -Path (Join-Path $dir 'last-update.json') -Text ($record | ConvertTo-Json)
}

function Restore-VedhaPrevious {
  # Undo an update: stop the new agent, put the previous program folder and its settings and identity
  # back, and start it again. The scan results and logs were never touched (they live in the data folder).
  param([string]$AppDir, [string]$Backup, [string]$DataDir, [string]$SavedDir)
  Stop-VedhaAgent -AppDir $AppDir
  if (Test-Path -LiteralPath $AppDir) { Remove-Item -LiteralPath $AppDir -Recurse -Force }
  Move-Item -LiteralPath $Backup -Destination $AppDir -Force
  foreach ($name in 'agent.env', 'state.json') {
    $kept = Join-Path $SavedDir $name
    if (Test-Path -LiteralPath $kept) { Copy-Item -LiteralPath $kept -Destination (Join-Path $DataDir $name) -Force }
  }
  Set-VedhaAcl -Path $DataDir
  Register-VedhaTask -AppDir $AppDir
  Start-ScheduledTask -TaskName $TaskName
}

function Copy-VedhaLegacyResults {
  # Agent 2.2.0 and 2.2.1 kept their archive of submitted scans inside the program folder
  # (Program Files\Vedha Agent\result). Replacing or removing that folder would delete the only copy, so it
  # is copied into the locked data folder first. Returns how many files were saved (0 = nothing to save).
  # Throws, having removed its partial copy, unless every file arrived; the caller then keeps the old folder.
  param([string]$LegacyDir, [string]$DataDir)
  if (-not (Test-Path -LiteralPath $LegacyDir)) { return 0 }
  $files = @(Get-ChildItem -LiteralPath $LegacyDir -Recurse -File -Force -ErrorAction SilentlyContinue)
  if ($files.Count -eq 0) { return 0 }
  $dest = Join-Path (Join-Path $DataDir 'results') ('from-program-files-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Copy-Item -Path (Join-Path $LegacyDir '*') -Destination $dest -Recurse -Force
  $copied = @(Get-ChildItem -LiteralPath $dest -Recurse -File -Force -ErrorAction SilentlyContinue).Count
  if ($copied -ne $files.Count) {
    Remove-Item -LiteralPath $dest -Recurse -Force -ErrorAction SilentlyContinue
    throw "Only $copied of $($files.Count) saved scan results could be copied out of the old program folder, so nothing was changed."
  }
  return $files.Count
}

function Hide-VedhaSecrets {
  # Removes install tokens from text that is about to be kept (logs).
  param([string]$Text)
  return ($Text -replace 'vet_[A-Za-z0-9_-]{6,}', 'vet_[removed]')
}

function Get-VedhaSha256 {
  # SHA-256 of a file as lower-case hex. Uses .NET directly, so it works even when the
  # PowerShell module that holds Get-FileHash cannot be found (see Reset-WindowsPowerShellModulePath).
  param([string]$Path)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $stream = [System.IO.File]::OpenRead($Path)
    try { return (($sha.ComputeHash($stream) | ForEach-Object { $_.ToString('x2') }) -join '') }
    finally { $stream.Dispose() }
  } finally { $sha.Dispose() }
}

function Test-PackageHashes {
  # Checks every file named in SHA256SUMS.txt. Returns problems (empty = intact).
  param([string]$Root, [string]$SumsFile)
  $problems = @()
  if (-not (Test-Path -LiteralPath $SumsFile)) { return @('SHA256SUMS.txt is missing from the package.') }
  foreach ($line in (Get-Content -LiteralPath $SumsFile)) {
    if (-not $line.Trim()) { continue }
    if ($line -notmatch '^([0-9a-fA-F]{64})\s+\*?(.+)$') { $problems += "Unreadable line in SHA256SUMS.txt: $line"; continue }
    $expected = $Matches[1].ToLower()
    $relative = $Matches[2].Trim().Replace('\', '/').Replace('/', [string][System.IO.Path]::DirectorySeparatorChar)
    $path = Join-Path $Root $relative
    if (-not (Test-Path -LiteralPath $path)) {
      $problems += "Missing: $relative"
    } elseif ((Get-VedhaSha256 -Path $path) -ne $expected) {
      $problems += "Changed or damaged: $relative"
    }
  }
  return $problems
}

function Test-AclLocked {
  # Given `icacls <path>` output, true when only SYSTEM and Administrators can access it.
  param([string[]]$IcaclsOutput)
  $text = ($IcaclsOutput -join "`n")
  if ($text -match '(?i)\\Users:|Everyone:|Authenticated Users:|S-1-5-32-545|S-1-1-0|S-1-5-11') { return $false }
  return [bool]($text -match '(?i)SYSTEM:' -and $text -match '(?i)Administrators:')
}

function Get-StatusLine {
  # One line for the progress display from `status --json` output.
  param($Status)
  switch ($Status.state) {
    'starting'          { return 'starting up' }
    'enrolling'         { return 'registering with the manager' }
    'awaiting-approval' { return 'waiting for approval in Fleet' }
    'online'            { return 'connected' }
    'retrying'          { return "cannot reach the manager yet ($($Status.reason))" }
    'failed'            { return "stopped ($($Status.reason))" }
    default             { return [string]$Status.state }
  }
}

# ---------------------------------------------------------------------------
# Windows-only helpers
# ---------------------------------------------------------------------------

function Test-IsWindows { return ([Environment]::OSVersion.Platform -eq 'Win32NT') }

function Reset-WindowsPowerShellModulePath {
  # Defensive: Windows PowerShell inherits PSModulePath from whatever started install.cmd (cmd,
  # PowerShell 7, a management tool). A foreign or damaged value can hide its built-in commands, so
  # the installer, which needs only built-ins, uses its own folders. Does nothing under PowerShell 7.
  # (A real install once stopped at Get-FileHash; the exact cause was not isolated, so the installer
  # also avoids that cmdlet - see Get-VedhaSha256.)
  if ($PSVersionTable.PSEdition -ne 'Desktop') { return }
  $env:PSModulePath = (@((Join-Path $env:ProgramFiles 'WindowsPowerShell\Modules'), (Join-Path $PSHOME 'Modules'))) -join ';'
}

function Remove-VedhaFolder {
  # Deletes a folder, retrying briefly (antivirus or a log that is just closing can hold a file
  # for a moment). True only when the folder is really gone.
  param([string]$Path)
  for ($i = 0; $i -lt 6; $i++) {
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction SilentlyContinue
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    Start-Sleep -Milliseconds 500
  }
  return (-not (Test-Path -LiteralPath $Path))
}

function Test-IsAdmin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  return ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Write-Step  { param([string]$Number, [string]$Text) Write-Host ''; Write-Host "[$Number] $Text" -ForegroundColor Cyan }
function Write-Good  { param([string]$Text) Write-Host "    OK   $Text" -ForegroundColor Green }
function Write-Warn  { param([string]$Text) Write-Host "    WARN $Text" -ForegroundColor Yellow }
function Write-Bad   { param([string]$Text) Write-Host "    FAIL $Text" -ForegroundColor Red }
function Write-Fix   { param([string]$Text) Write-Host "         -> $Text" -ForegroundColor Yellow }

function Set-VedhaAcl {
  # Only SYSTEM and Administrators may touch the data folder (identity, settings, logs).
  param([string]$Path)
  & icacls.exe $Path /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Could not restrict access to $Path (icacls exit code $LASTEXITCODE)." }
}

function Set-VedhaAppAcl {
  # The program folder: SYSTEM and Administrators may change it; everyone else may only run it.
  param([string]$Path)
  & icacls.exe $Path /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' '*S-1-5-32-545:(OI)(CI)RX' | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Could not set permissions on $Path (icacls exit code $LASTEXITCODE)." }
}

function Write-Utf8NoBom {
  param([string]$Path, [string]$Text)
  [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false)))
}

function Get-VedhaScopeAuto {
  # The network this computer is on, from its main (default-route) adapter.
  $best = Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue |
    Where-Object { $_.NextHop -ne '0.0.0.0' } |
    ForEach-Object {
      $interfaceMetric = (Get-NetIPInterface -InterfaceIndex $_.InterfaceIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue).InterfaceMetric
      [pscustomobject]@{ Route = $_; Metric = ([int]$_.RouteMetric + [int]$interfaceMetric) }
    } | Sort-Object Metric | Select-Object -First 1
  if (-not $best) { return $null }
  $route = $best.Route
  $addr = Get-NetIPAddress -InterfaceIndex $route.InterfaceIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike '169.254.*' } | Select-Object -First 1
  if (-not $addr) { return $null }
  $adapter = (Get-NetAdapter -InterfaceIndex $route.InterfaceIndex -ErrorAction SilentlyContinue).Name
  $net = ConvertTo-NetworkCidr -Address $addr.IPAddress -PrefixLength $addr.PrefixLength
  return [pscustomobject]@{ Cidr = $net.Cidr; Note = $net.Note; Adapter = $adapter; Address = $addr.IPAddress }
}

function Invoke-AgentCommand {
  # Runs vedha-agent.exe and returns @{ Output; ExitCode }. Never throws on a non-zero exit.
  param([string]$Exe, [string[]]$Arguments)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $output = & $Exe @Arguments 2>&1 | ForEach-Object { "$_" }
    return [pscustomobject]@{ Output = ($output -join "`n"); ExitCode = $LASTEXITCODE }
  } finally { $ErrorActionPreference = $previous }
}

function Get-AgentStatus {
  param([string]$Exe)
  $r = Invoke-AgentCommand -Exe $Exe -Arguments @('status', '--json')
  try { return ($r.Output | ConvertFrom-Json) } catch { return $null }
}

function Stop-VedhaAgent {
  param([string]$AppDir)
  $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  if ($task) { Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue }
  for ($i = 0; $i -lt 20; $i++) {
    $running = Get-Process -Name 'vedha-agent' -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -like "$AppDir*" }
    if (-not $running) { return }
    if ($i -ge 8) { $running | Stop-Process -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Milliseconds 500
  }
}

function Register-VedhaTask {
  param([string]$AppDir)
  $exe = Join-Path $AppDir 'vedha-agent.exe'
  $action    = New-ScheduledTaskAction -Execute $exe -Argument 'run' -WorkingDirectory $AppDir
  $trigger   = New-ScheduledTaskTrigger -AtStartup
  $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
  $settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
                 -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 999 -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
                 -MultipleInstances IgnoreNew
  Register-ScheduledTask -TaskName $TaskName -Description 'Vedha network assessment agent' `
    -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
}

# ---------------------------------------------------------------------------
# The installer
# ---------------------------------------------------------------------------

function Invoke-VedhaUninstall {
  param([string]$AppDir, [string]$DataDir)
  Write-Step '1/2' 'Stopping and removing the agent'
  Stop-VedhaAgent -AppDir $AppDir
  if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Good "Removed the scheduled task '$TaskName'."
  } else {
    Write-Good 'No scheduled task was installed.'
  }
  if (Test-Path -LiteralPath $AppDir) {
    if (-not $Purge) {
      # Agent 2.2.0 / 2.2.1 archived scan results inside the program folder; keep them with the identity and logs.
      if (-not (Test-Path -LiteralPath $DataDir)) { New-Item -ItemType Directory -Force -Path $DataDir | Out-Null; Set-VedhaAcl -Path $DataDir }
      $savedResults = Copy-VedhaLegacyResults -LegacyDir (Join-Path $AppDir 'result') -DataDir $DataDir
      if ($savedResults -gt 0) { Write-Good "Saved $savedResults scan result file(s) from the program folder into $DataDir\results" }
    }
    Remove-Item -LiteralPath $AppDir -Recurse -Force
    Write-Good "Removed $AppDir"
  }
  Write-Step '2/2' 'Identity and logs'
  if ($Purge) {
    # This run's own log is still open, so the folder itself is deleted as the script finishes.
    $script:PurgeDataDir = $DataDir
    Write-Good "$DataDir (the agent's identity, settings and logs) will be deleted as this finishes."
    Write-Host '    Tell your Vedha contact so the agent is revoked on their side.'
  } else {
    Write-Good "Kept $DataDir (identity, settings, logs). Re-run with -Uninstall -Purge to delete them."
  }
  Write-Host ''
  Write-Host 'The Vedha agent has been removed.' -ForegroundColor Green
  return 0
}

function Invoke-VedhaInstall {
  param([string]$AppDir, [string]$DataDir)

  $source = Join-Path $PSScriptRoot 'vedha-agent'
  $sourceExe = Join-Path $source 'vedha-agent.exe'
  $configPath = Join-Path $DataDir 'agent.env'
  $installed = $false

  # --- 1. Check this computer and the package -------------------------------
  Write-Step '1/6' 'Checking this computer and the package'
  if (-not [Environment]::Is64BitOperatingSystem) { throw 'This agent needs 64-bit Windows.' }
  if ([Environment]::OSVersion.Version -lt [Version]'10.0.14393') {
    throw "This agent needs Windows 10 / Windows Server 2016 or newer (this is $([Environment]::OSVersion.VersionString))."
  }
  Write-Good "Windows $([Environment]::OSVersion.Version) (64-bit)"

  Get-ChildItem -LiteralPath $PSScriptRoot -Recurse -File -ErrorAction SilentlyContinue | Unblock-File -ErrorAction SilentlyContinue

  $problems = Test-PackageHashes -Root $PSScriptRoot -SumsFile (Join-Path $PSScriptRoot 'SHA256SUMS.txt')
  if ($problems.Count -gt 0) {
    foreach ($p in $problems) { Write-Bad $p }
    if ($problems -match 'Missing: vedha-agent') {
      Write-Fix 'Your antivirus may have removed the agent program. Ask your security team to allow this folder (see ALLOWLIST.txt), then unzip the package again.'
    } else {
      Write-Fix 'The package is incomplete or was damaged in transit. Download or copy it again and compare its SHA-256 with the value Vedha sent you.'
    }
    throw 'The package failed its integrity check.'
  }
  Write-Good 'Package files are intact.'

  $free = (Get-PSDrive -Name ($env:ProgramFiles.Substring(0, 1))).Free
  if ($free -lt 500MB) { throw "Not enough free disk space on $($env:ProgramFiles.Substring(0, 2)) ($([math]::Round($free / 1MB)) MB free; 500 MB needed)." }
  Write-Good "$([math]::Round($free / 1GB, 1)) GB free"

  $run = Invoke-AgentCommand -Exe $sourceExe -Arguments @('version')
  if ($run.ExitCode -ne 0) {
    Write-Bad "The agent program could not start (exit code $($run.ExitCode)). $($run.Output)"
    Write-Fix 'Antivirus or endpoint protection may be blocking it: ask your security team to allow this folder (see ALLOWLIST.txt). Otherwise send us this window.'
    throw 'The agent program does not run on this computer.'
  }
  Write-Good $run.Output.Trim()

  # What is already on this computer? Look before changing anything.
  $packageVersion   = Get-VedhaVersionNumber -Text $run.Output
  $installedExe     = Join-Path $AppDir 'vedha-agent.exe'
  $installedPresent = Test-Path -LiteralPath $installedExe
  $installedVersion = $null
  if ($installedPresent) {
    $installedRun = Invoke-AgentCommand -Exe $installedExe -Arguments @('version')
    if ($installedRun.ExitCode -eq 0) { $installedVersion = Get-VedhaVersionNumber -Text $installedRun.Output }
  }
  $plan = Get-VedhaUpdatePlan -InstalledPresent $installedPresent -Installed $installedVersion -Package $packageVersion -AllowDowngrade:$AllowDowngrade
  switch ($plan.Kind) {
    'fresh'     { Write-Good $plan.Message }
    'upgrade'   { Write-Good $plan.Message }
    'same'      { Write-Good $plan.Message }
    'unknown'   { Write-Warn $plan.Message }
    'downgrade' {
      if ($plan.Allowed) { Write-Warn $plan.Message }
      else {
        Write-Bad $plan.Message
        Write-Fix 'Use the newer package (for example the one you installed from last time), or add -AllowDowngrade if you really want the older agent.'
        throw 'Refusing to replace a newer agent with an older one.'
      }
    }
  }
  $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  if ($existingTask) {
    $runs = (@($existingTask.Actions) | ForEach-Object { ("$($_.Execute) $($_.Arguments)").Trim() }) -join '; '
    if ($runs -and $runs -notlike "*$installedExe*") {
      Write-Warn "The existing scheduled task '$TaskName' runs: $runs"
      Write-Host '         That is not the installed agent program (a source-mode lab install?). The task will be replaced; the agent''s identity is kept.'
    }
  }
  foreach ($other in @(Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {
        $_.TaskName -ne $TaskName -and (@($_.Actions) | Where-Object { ("$($_.Execute) $($_.Arguments)") -match 'vedha-agent|Vedha Agent' }) })) {
    Write-Warn "Another scheduled task, '$($other.TaskName)', also starts a Vedha agent. If it is an old install, remove it: Unregister-ScheduledTask -TaskName '$($other.TaskName)'"
  }
  foreach ($stray in @(Get-Process -Name 'vedha-agent' -ErrorAction SilentlyContinue | Where-Object { $_.Path -and ($_.Path -notlike "$AppDir*") })) {
    Write-Warn "A Vedha agent is already running from another folder: $($stray.Path) (process $($stray.Id))."
    Write-Fix 'Close it (for example a run.cmd window). Only one agent process can use an identity, so it would stop the installed agent from starting.'
  }

  # --- 2. Decide the settings -----------------------------------------------
  Write-Step '2/6' 'Working out the settings'
  $existing = @{}
  if (Test-Path -LiteralPath $configPath) { $existing = Read-VedhaConfig -Text ([System.IO.File]::ReadAllText($configPath)) }

  $managerUrl = Resolve-VedhaManager -Given $Manager -Baked $BakedManager -Existing ([string]$existing['PLATFORM_URL'])
  Write-Good "Manager: $managerUrl"

  $agentName = $Name
  if (-not $agentName) { $agentName = [string]$existing['PROBE_NAME'] }
  if (-not $agentName) { $agentName = "$($env:COMPUTERNAME)-probe" }
  Write-Good "Name in Fleet: $agentName"

  $scopeValue = $Scope
  if (-not $scopeValue) { $scopeValue = [string]$existing['PROBE_NETWORK_SEGMENTS'] }
  if ($scopeValue) {
    if (-not (Test-VedhaScope -Value $scopeValue)) { throw "The scope '$scopeValue' is not valid. Use networks like 192.168.1.0/24, separated by commas." }
    Write-Good "Scan scope: $scopeValue"
  } else {
    $auto = Get-VedhaScopeAuto
    if ($auto) {
      $scopeValue = $auto.Cidr
      Write-Good "Scan scope: $scopeValue (this computer's network, from adapter '$($auto.Adapter)' at $($auto.Address))"
      if ($auto.Note) { Write-Warn $auto.Note }
      Write-Host '         To scan a different network, run: install.cmd -Repair -Scope <network>'
    } else {
      Write-Warn 'Could not work out this computer''s network. The agent will connect but receive NO scan jobs until a scope is set.'
      Write-Fix 'Run: install.cmd -Repair -Scope 192.168.1.0/24   (use your own network)'
    }
  }

  $proxyUrl = $Proxy
  if (-not $proxyUrl) { $proxyUrl = [string]$existing['HTTPS_PROXY'] }
  $caPath = [string]$existing['PROBE_CA_BUNDLE']
  if ($CaBundle) {
    if (-not (Test-Path -LiteralPath $CaBundle)) { throw "The certificate file '$CaBundle' was not found." }
    $caPath = Join-Path $DataDir 'ca-bundle.pem'
  }

  # --- 3. Check the connection to the manager BEFORE changing anything -------
  Write-Step '3/6' 'Checking the connection to the manager'
  if ($SkipPreflight) {
    Write-Warn 'Skipped (-SkipPreflight).'
  } else {
    $savedEnv = @{}
    foreach ($pair in @(@('PLATFORM_URL', $managerUrl), @('HTTPS_PROXY', $proxyUrl), @('PROBE_CA_BUNDLE', $(if ($CaBundle) { $CaBundle } else { $caPath })))) {
      $savedEnv[$pair[0]] = [Environment]::GetEnvironmentVariable($pair[0])
      if ($pair[1]) { [Environment]::SetEnvironmentVariable($pair[0], $pair[1]) }
    }
    try {
      $doctor = Invoke-AgentCommand -Exe $sourceExe -Arguments @('doctor', '--preinstall')
    } finally {
      foreach ($key in $savedEnv.Keys) { [Environment]::SetEnvironmentVariable($key, $savedEnv[$key]) }
    }
    $doctor.Output -split "`n" | ForEach-Object { Write-Host "    $_" }
    if ($doctor.ExitCode -ne 0) {
      Write-Host ''
      Write-Bad 'This computer cannot reach the manager yet, so nothing has been installed.'
      Write-Fix 'Apply the fix shown above (your IT team can do this), then run the same command again.'
      Write-Fix 'If you are sure the network is fine, add -SkipPreflight.'
      throw 'The manager is not reachable from this computer.'
    }
  }

  # --- 4. Install -----------------------------------------------------------
  Write-Step '4/6' 'Installing'
  $backup = "$AppDir.old"
  # Replacing a working agent: remember its settings and identity, and keep its program folder until
  # the new one has connected, so a bad update can be undone (see the end of step 5).
  $hadPrevious = $installedPresent
  $savedDir = ''
  if ($hadPrevious) { $savedDir = Save-VedhaPreviousState -DataDir $DataDir }
  Stop-VedhaAgent -AppDir $AppDir
  try {
    if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse -Force }
    if (Test-Path -LiteralPath $AppDir) { Move-Item -LiteralPath $AppDir -Destination $backup -Force }
    Copy-Item -LiteralPath $source -Destination $AppDir -Recurse -Force
    Set-VedhaAppAcl -Path $AppDir
    $exe = Join-Path $AppDir 'vedha-agent.exe'
    if (-not (Test-Path -LiteralPath $exe)) { throw 'The agent program disappeared right after it was copied (antivirus may have removed it).' }
    $check = Invoke-AgentCommand -Exe $exe -Arguments @('version')
    if ($check.ExitCode -ne 0) { throw "The installed agent program does not start: $($check.Output)" }
    Write-Good "Program installed in $AppDir"

    foreach ($dir in @($DataDir, (Join-Path $DataDir 'logs'), (Join-Path $DataDir 'spool'))) {
      if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    }
    Set-VedhaAcl -Path $DataDir
    if ($CaBundle) { Copy-Item -LiteralPath $CaBundle -Destination $caPath -Force }

    # Agent 2.2.0 / 2.2.1 archived scan results inside the program folder, which is about to be deleted.
    $savedResults = Copy-VedhaLegacyResults -LegacyDir (Join-Path $backup 'result') -DataDir $DataDir
    if ($savedResults -gt 0) { Write-Good "Saved $savedResults scan result file(s) from the old program folder into $DataDir\results" }

    $digest = Get-VedhaSha256 -Path $exe
    $version = $PackageVersion
    if ($version -like '__*') { $version = '' }
    $config = New-VedhaAgentConfig -ManagerUrl $managerUrl -DataDir $DataDir -AgentName $agentName -ScopeValue $scopeValue `
      -ProxyUrl $proxyUrl -CaBundlePath $caPath -InstallToken $Token -InstallerVersion $version -BuildDigest $digest
    if (Test-Path -LiteralPath $configPath) {
      $extra = @(Get-VedhaExtraSettingLines -ExistingText ([System.IO.File]::ReadAllText($configPath)))
      if ($extra.Count -gt 0) {
        $config = Add-VedhaExtraSettings -ConfigText $config -ExtraLines $extra
        $extraNames = ($extra | ForEach-Object { $_.Substring(0, $_.IndexOf('=')).Trim() }) -join ', '
        Write-Good "Kept $($extra.Count) setting(s) you had added: $extraNames"
      }
    }
    Write-Utf8NoBom -Path $configPath -Text $config
    Write-Good "Settings saved in $configPath (readable only by administrators)"

    Register-VedhaTask -AppDir $AppDir
    Write-Good "Registered the scheduled task '$TaskName' (starts at boot, restarts itself if it stops)"
    # setup.cmd (the source-mode lab install) wrote a launcher that the old task ran; the task now runs the program.
    $labLauncher = Join-Path $DataDir 'agent-service.cmd'
    if (Test-Path -LiteralPath $labLauncher) {
      Remove-Item -LiteralPath $labLauncher -Force -ErrorAction SilentlyContinue
      if (-not (Test-Path -LiteralPath $labLauncher)) { Write-Good 'Removed the old source-mode launcher (agent-service.cmd).' }
    }
    $installed = $true
  } catch {
    Write-Bad "$($_.Exception.Message)"
    if (Test-Path -LiteralPath $backup) {
      Write-Warn 'Putting the previous installation back.'
      if (Test-Path -LiteralPath $AppDir) { Remove-Item -LiteralPath $AppDir -Recurse -Force -ErrorAction SilentlyContinue }
      Move-Item -LiteralPath $backup -Destination $AppDir -Force -ErrorAction SilentlyContinue
      if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) { Start-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue }
    }
    Remove-VedhaPreviousState -SavedDir $savedDir
    throw
  }
  # The previous program folder is kept until the new agent has connected, unless nobody is waiting to see.
  $keepBackup = $hadPrevious -and -not $NoWait -and (Test-Path -LiteralPath $backup)
  if (-not $keepBackup) {
    if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse -Force -ErrorAction SilentlyContinue }
    Remove-VedhaPreviousState -SavedDir $savedDir
  }

  # --- 5. Start and wait for it to connect ----------------------------------
  Write-Step '5/6' 'Starting the agent'
  Start-ScheduledTask -TaskName $TaskName
  if ($NoWait) {
    Write-Warn 'Not waiting for the agent to connect (-NoWait).'
    return 0
  }
  $exe = Join-Path $AppDir 'vedha-agent.exe'
  $waitFor = if ($keepBackup) { $UpgradeWaitSeconds } else { $WaitSeconds }
  $deadline = (Get-Date).AddSeconds($waitFor)
  $last = ''
  $final = $null
  while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 3
    $status = Get-AgentStatus -Exe $exe
    if ($null -eq $status) { continue }
    $line = Get-StatusLine -Status $status
    if ($line -ne $last) { Write-Host "    ... $line"; $last = $line }
    if ($status.state -in @('online', 'awaiting-approval', 'failed')) { $final = $status; break }
    $final = $status
  }

  # --- 6. Result --------------------------------------------------------------
  Write-Step '6/6' 'Result'
  if ($keepBackup) {
    $finalState = if ($null -ne $final) { [string]$final.state } else { '' }
    if (Get-VedhaRollbackDecision -HadPrevious $true -Kind $plan.Kind -State $finalState) {
      Write-Host ''
      Write-Host 'THE NEW VERSION DID NOT CONNECT, so the previous version is being put back.' -ForegroundColor Yellow
      if ($null -ne $final) { Write-Host "  The new agent's last status was: $(Get-StatusLine -Status $final)" }
      $reason = if ($finalState) { "the new agent stayed '$finalState'" } else { 'the new agent never reported a status' }
      try {
        Restore-VedhaPrevious -AppDir $AppDir -Backup $backup -DataDir $DataDir -SavedDir $savedDir
        Write-VedhaUpdateRecord -DataDir $DataDir -Result 'rolled-back' -From "$installedVersion" -To "$packageVersion" -Reason $reason
        Remove-VedhaPreviousState -SavedDir $savedDir
        Write-Host "  Restored the previous agent ($installedVersion). Scan results, logs and identity are unchanged." -ForegroundColor Green
        Write-Host '  The update will not be tried again for 24 hours. To see why the new version failed, read the lines above.'
      } catch {
        Write-Bad "Could not restore the previous version automatically: $($_.Exception.Message)"
        Write-Fix "The previous program folder is still at $backup. Rename it to '$AppDir' (after stopping the '$TaskName' task) to go back by hand."
        Write-VedhaUpdateRecord -DataDir $DataDir -Result 'rollback-failed' -From "$installedVersion" -To "$packageVersion" -Reason $_.Exception.Message
      }
      return 4
    }
    Remove-VedhaPreviousState -SavedDir $savedDir
    if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse -Force -ErrorAction SilentlyContinue }
    Write-VedhaUpdateRecord -DataDir $DataDir -Result 'updated' -From "$installedVersion" -To "$packageVersion" -Reason ''
  }
  if ($null -ne $final -and $final.state -eq 'online') {
    if ($Token -and (Test-Path -LiteralPath $configPath)) {
      Write-Utf8NoBom -Path $configPath -Text (Remove-VedhaTokenLine -Text ([System.IO.File]::ReadAllText($configPath)))
      Write-Good 'The one-time install token was used and has been removed from the settings file.'
    }
    Write-Host ''
    Write-Host 'SUCCESS: the Vedha agent is installed and connected.' -ForegroundColor Green
    Write-Host "  Manager : $managerUrl"
    $was = ''
    if ($installedVersion -and $packageVersion -and $installedVersion -ne $packageVersion) { $was = " (was $installedVersion)" }
    Write-Host "  Agent   : $packageVersion$was"
    Write-Host "  Scope   : $(if ($scopeValue) { $scopeValue } else { '(none set - no jobs will be sent)' })"
    Write-Host "  It starts automatically when this computer starts."
    Write-Host "  To check it any time, from an Administrator prompt:  `"$exe`" status"
    Write-Host "  If something stops working:                           `"$exe`" doctor"
    return 0
  }
  if ($null -ne $final -and $final.state -eq 'awaiting-approval') {
    Write-Host ''
    Write-Host 'INSTALLED. One step left: approve this agent in Fleet.' -ForegroundColor Yellow
    Write-Host "  Open  : $($final.pairing_url)"
    Write-Host "  Enter : $($final.pairing_code)"
    Write-Host '  The agent connects by itself as soon as it is approved.'
    return 0
  }

  Write-Host ''
  Write-Host 'INSTALLED, BUT NOT CONNECTED YET.' -ForegroundColor Red
  if ($null -ne $final) {
    Write-Host "  Status : $(Get-StatusLine -Status $final)"
    if ($final.remediation) { Write-Fix $final.remediation }
  }
  Write-Host ''
  Write-Host '  Running the checks to find out why:'
  $diagnosis = Invoke-AgentCommand -Exe $exe -Arguments @('doctor')
  $diagnosis.Output -split "`n" | ForEach-Object { Write-Host "    $_" }
  Write-Host ''
  Write-Host '  The agent keeps trying by itself, so once the problem above is fixed it connects without re-installing.'
  Write-Host "  To send this to Vedha support, run:  `"$exe`" support-bundle"
  return 3
}

function Invoke-Main {
  if (-not (Test-IsWindows)) { Write-Host 'This installer runs on Windows only.'; return 2 }
  Reset-WindowsPowerShellModulePath

  $appDir  = Join-Path $env:ProgramFiles 'Vedha Agent'
  $dataDir = Join-Path $env:ProgramData 'vedha-agent'

  # Administrator rights: ask for them (one prompt) and continue in a new window that stays open.
  if (-not (Test-IsAdmin)) {
    Write-Host 'The installer needs administrator rights. Windows will ask you to confirm...'
    $argList = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$PSCommandPath`"", '-ElevatedChild')
    foreach ($key in $script:BoundParams.Keys) {
      $value = $script:BoundParams[$key]
      if ($value -is [System.Management.Automation.SwitchParameter]) { if ($value.IsPresent) { $argList += "-$key" } }
      elseif ($null -ne $value -and "$value" -ne '') { $argList += "-$key"; $argList += "`"$value`"" }
    }
    try {
      $child = Start-Process -FilePath 'powershell.exe' -ArgumentList $argList -Verb RunAs -Wait -PassThru
      if ($child.ExitCode -eq 0) { Write-Host 'Finished. The details are in the window that opened and in the install log.' }
      else { Write-Host "The installer reported a problem (code $($child.ExitCode)). The details are in the window that opened." -ForegroundColor Yellow }
      return $child.ExitCode
    } catch {
      Write-Host 'Administrator rights were not granted, so nothing was changed.' -ForegroundColor Red
      Write-Host 'Run again and choose "Yes" at the Windows prompt, or open PowerShell as Administrator first.'
      return 1
    }
  }

  # A readable record of what happened, kept even if the window closes.
  $logDir = Join-Path $dataDir 'logs'
  New-Item -ItemType Directory -Force -Path $logDir | Out-Null
  Set-VedhaAcl -Path $dataDir
  $logPath = Join-Path $logDir ("install-{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
  $transcribing = $false
  try { Start-Transcript -Path $logPath -Force | Out-Null; $transcribing = $true } catch { }

  $exitCode = 1
  try {
    if ($TokenFile) {
      if (-not (Test-Path -LiteralPath $TokenFile)) { throw "The token file '$TokenFile' was not found." }
      $script:Token = ([System.IO.File]::ReadAllText($TokenFile)).Trim()
    }
    if ($Uninstall) {
      $exitCode = [int](@(Invoke-VedhaUninstall -AppDir $appDir -DataDir $dataDir) | Select-Object -Last 1)
    } else {
      if (-not $Token -and -not $Repair -and -not $Pairing -and [Environment]::UserInteractive -and -not $NoWait -and -not (Test-Path (Join-Path $dataDir 'state.json'))) {
        Write-Host ''
        Write-Host 'Paste the one-time install token from Fleet > Add agent, or press Enter to approve this agent with a pairing code instead.'
        $script:Token = (Read-Host 'Install token').Trim()
      }
      if ($Token -and -not (Test-VedhaToken -Value $Token)) {
        throw 'That does not look like an install token (it should start with vet_). Copy it again from Fleet > Add agent.'
      }
      $exitCode = [int](@(Invoke-VedhaInstall -AppDir $appDir -DataDir $dataDir) | Select-Object -Last 1)
    }
  } catch {
    Write-Host ''
    Write-Host "STOPPED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Nothing further was changed. A log of this run is in: $logPath"
    $exe = Join-Path $appDir 'vedha-agent.exe'
    if (-not (Test-Path -LiteralPath $exe)) { $exe = Join-Path (Join-Path $PSScriptRoot 'vedha-agent') 'vedha-agent.exe' }
    Write-Host "  To send it to Vedha support, run:  `"$exe`" support-bundle"
    $exitCode = 1
  } finally {
    if ($transcribing) {
      try { Stop-Transcript | Out-Null } catch { }
      if (-not $script:PurgeDataDir) {
        try { Write-Utf8NoBom -Path $logPath -Text (Hide-VedhaSecrets -Text ([System.IO.File]::ReadAllText($logPath))) } catch { }
      }
    }
  }
  if ($script:PurgeDataDir -and $exitCode -eq 0) {
    if (Remove-VedhaFolder -Path $script:PurgeDataDir) {
      Write-Host "Deleted $($script:PurgeDataDir)." -ForegroundColor Green
    } else {
      Write-Host "Could not delete $($script:PurgeDataDir) completely. Delete that folder by hand (as Administrator)." -ForegroundColor Yellow
      $exitCode = 1
    }
  }

  if ($ElevatedChild -and -not $NoPause) {
    Write-Host ''
    [void](Read-Host 'Press Enter to close this window')
  }
  return $exitCode
}

# Run only when executed, not when dot-sourced by the tests.
if ($MyInvocation.InvocationName -ne '.') { exit ([int](@(Invoke-Main) | Select-Object -Last 1)) }
