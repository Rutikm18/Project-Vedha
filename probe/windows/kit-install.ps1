<#
  Vedha agent build kit - the ONE script to run.   Double-click  install.cmd  in the kit folder.

  What it does, in order. It stops at the first thing it cannot fix and says exactly what to do:
    1  shows the settings it will use on ONE screen, already filled in (server login, ssh key file found
       automatically, manager https address, tokenless install): press Enter to accept, or type 1-4 to change
       one. Defaults come from the kit (kit-defaults.json) and then from your last run
       (%USERPROFILE%\.vedha\kit-settings.json: no passwords, no key contents)
    2  checks THIS PC: 64-bit Windows, PowerShell 5.1+, Python 3.10-3.12 (installs Python 3.12 with winget
       when it is missing), ssh and scp, internet access to the build downloads, the ssh key file
    3  checks the SERVER over ssh BEFORE the long build: you can log in, the manager folder with
       docker-compose.yml and .env is where you said, and your login may run docker
    4  builds, signs and publishes the Windows agent (publish-release.ps1: 15-35 minutes the first time),
       puts the public keys on the manager and restarts it, then confirms the manager serves the package
    5  opens the folder with your signing keys and reminds you to back it up

  Nothing is installed or changed on the server until step 4. -CheckOnly stops after step 3.
  Re-running is safe: the build environment, the built agent and the keys are reused, never deleted.

  ASCII only, on purpose: Windows PowerShell 5.1 reads a BOM-less file in the ANSI code page.
#>
[CmdletBinding()]
param(
  [string]$Server = '',                 # user@host of the manager server
  [string]$SshKey = '',                 # C:\path\to\server.pem
  [string]$ManagerUrl = '',             # https://api.example.com
  [string]$RemoteComposeDir = '',       # the folder on the server that holds docker-compose.yml and .env
  [string]$RemoteReleaseDir = '',       # default: <compose folder>/agent-releases
  [switch]$AllowTokenlessInstall,       # let machines install with no token (you approve them in Fleet)
  [switch]$Yes,                         # ask nothing: use the values given or saved
  [switch]$CheckOnly,                   # check this PC and the server, change nothing, build nothing
  [switch]$DryRun,                      # print the publish plan and stop
  [switch]$SkipBuild,                   # reuse the agent already built
  [switch]$NoPause
)
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Pure helpers (no side effects; unit-tested by tests\Test-KitInstall.ps1)
# ---------------------------------------------------------------------------

function Test-KitServer([string]$Value)     { return [bool]($Value -match '^([A-Za-z0-9._-]+@)?[A-Za-z0-9.-]+$') }
function Test-KitManagerUrl([string]$Value) { return [bool]($Value.TrimEnd('/') -match '^https://[A-Za-z0-9.-]+(:[0-9]{1,5})?$') }
function Test-KitRemoteDir([string]$Value)  { return [bool]($Value -match '^/[A-Za-z0-9_./-]+$') -and ($Value -notmatch '\.\.') }
function Test-KitKeyPath([string]$Value) {
  return [bool]($Value -match '^[A-Za-z]:\\[A-Za-z0-9 _.()\\-]{1,200}$') -and ($Value -notmatch '\.\.')
}

function Select-KitPython($Found) {
  # $Found: objects with .Path and .Text (the output of `<path> --version`). The best SUPPORTED one wins: 3.12, then
  # 3.11, then 3.10. 3.13 and newer are skipped on purpose (the compiler and pinned libraries do not support them yet).
  $best = ''; $bestMinor = -1
  foreach ($f in @($Found)) {
    if ($f.Text -match '^\s*Python 3\.(10|11|12)\.\d+') {
      $minor = [int]$Matches[1]
      if ($minor -gt $bestMinor) { $best = [string]$f.Path; $bestMinor = $minor }
    }
  }
  return $best
}

function Test-KitPythonOutput([string]$Text) {
  # 'Python 3.12.4' -> true for 3.10, 3.11, 3.12 only (the build needs a version Nuitka and the pins support).
  return [bool]($Text -match '^\s*Python 3\.(10|11|12)\.\d+')
}

function Get-KitDefaultComposeDir { return '/opt/Project-Vedha/manager' }

function Get-KitKeyFolders([string]$UserHome, [string]$KitRoot) {
  # Where a downloaded AWS key file usually is. Checked in this order.
  return @((Join-Path $UserHome 'Downloads'), (Join-Path $UserHome '.ssh'), (Join-Path $UserHome 'Desktop'),
           (Join-Path $UserHome 'Documents'), $KitRoot)
}

function Find-KitSshKeys([string[]]$Folders, [scriptblock]$Accept = ${function:Test-KitKeyPath}) {
  # Every .pem file (not searched recursively) in those folders whose path is safe to hand to ssh, newest first
  # within a folder, without duplicates.
  $found = @()
  foreach ($f in $Folders) {
    if (-not $f -or -not (Test-Path -LiteralPath $f -PathType Container)) { continue }
    foreach ($file in @(Get-ChildItem -LiteralPath $f -Filter '*.pem' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending)) {
      if ((& $Accept $file.FullName) -and ($found -notcontains $file.FullName)) { $found += $file.FullName }
    }
  }
  return $found
}

function Get-KitSettingsPath([string]$UserHome) { return (Join-Path (Join-Path $UserHome '.vedha') 'kit-settings.json') }

function ConvertTo-KitSettingsJson {
  param([string]$Server, [string]$SshKey, [string]$ManagerUrl, [string]$ComposeDir, [bool]$Tokenless)
  $o = [ordered]@{ server = $Server; ssh_key = $SshKey; manager_url = $ManagerUrl; remote_compose_dir = $ComposeDir; tokenless = $Tokenless }
  return ($o | ConvertTo-Json)
}

function ConvertFrom-KitSettingsJson([string]$Text) {
  # Only well-formed values survive: a hand-edited or damaged file can never smuggle a bad value into a command.
  $out = @{ server = ''; ssh_key = ''; manager_url = ''; remote_compose_dir = ''; tokenless = $false }
  try { $o = $Text | ConvertFrom-Json } catch { return $out }
  if ($o.server -and (Test-KitServer ([string]$o.server))) { $out.server = [string]$o.server }
  if ($o.ssh_key -and (Test-KitKeyPath ([string]$o.ssh_key))) { $out.ssh_key = [string]$o.ssh_key }
  if ($o.manager_url -and (Test-KitManagerUrl ([string]$o.manager_url))) { $out.manager_url = ([string]$o.manager_url).TrimEnd('/') }
  if ($o.remote_compose_dir -and (Test-KitRemoteDir ([string]$o.remote_compose_dir))) { $out.remote_compose_dir = [string]$o.remote_compose_dir }
  if ($o.tokenless -eq $true) { $out.tokenless = $true }
  return $out
}

function Get-KitRemoteLayoutCommand([string]$ComposeDir) {
  # One shell line run on the server. Every value was checked against a strict pattern first, so it cannot
  # break out of its single quotes. It prints one word per fact so the answer can be read back reliably.
  if (-not (Test-KitRemoteDir $ComposeDir)) { throw "Not a safe folder path on the server: '$ComposeDir'" }
  return ("d='" + $ComposeDir + "'; " +
          'if [ -f "$d/docker-compose.yml" ]; then echo compose-file-ok; else echo compose-file-missing; fi; ' +
          'if [ -f "$d/.env" ]; then echo env-file-ok; else echo env-file-missing; fi; ' +
          'if docker ps >/dev/null 2>&1; then echo docker-ok; else echo docker-denied; fi')
}

function Get-KitRemoteFacts([string]$Output) {
  return [pscustomobject]@{
    ComposeFile = ($Output -match '(?m)^compose-file-ok\s*$')
    EnvFile     = ($Output -match '(?m)^env-file-ok\s*$')
    Docker      = ($Output -match '(?m)^docker-ok\s*$')
  }
}

function Get-KitPublishArguments {
  # The argument list for publish-release.ps1, built only from values that passed their checks.
  param([string]$Server, [string]$SshKey, [string]$ManagerUrl, [string]$ComposeDir, [string]$ReleaseDir,
        [bool]$Tokenless, [bool]$DryRun, [bool]$SkipBuild, [string]$PythonExe = '')
  $a = @('-Server', $Server)
  if ($SshKey) { $a += @('-SshKey', $SshKey) }
  $a += @('-ManagerUrl', $ManagerUrl.TrimEnd('/'), '-ConfigureManager')
  if ($ComposeDir) { $a += @('-RemoteComposeDir', $ComposeDir) }
  if ($ReleaseDir) { $a += @('-RemoteReleaseDir', $ReleaseDir) }
  if ($Tokenless) { $a += '-AllowTokenlessInstall' }
  if ($DryRun) { $a += '-DryRun' }
  if ($SkipBuild) { $a += '-SkipBuild' }
  if ($PythonExe) { $a += @('-PythonExe', $PythonExe) }
  return $a
}

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

$script:Problems = @()
$script:PythonExe = ''
$script:KitSshKey = ''
function Write-Head([string]$Text) { Write-Host ''; Write-Host $Text -ForegroundColor Cyan }
function Write-Ok([string]$Text)   { Write-Host ('  [ OK ] ' + $Text) -ForegroundColor Green }
function Write-Warn([string]$Text) { Write-Host ('  [WARN] ' + $Text) -ForegroundColor Yellow }
function Write-Bad([string]$Text, [string]$Fix) {
  Write-Host ('  [FAIL] ' + $Text) -ForegroundColor Red
  if ($Fix) { Write-Host ('         -> ' + $Fix) -ForegroundColor Yellow }
  $script:Problems += $Text
}

function Read-KitValue {
  # Ask once, showing the saved or default value; Enter keeps it. With -Yes nothing is asked.
  param([string]$Prompt, [string]$Current, [scriptblock]$Valid, [string]$Hint)
  if ($Yes) {
    if ($Current -and (& $Valid $Current)) { return $Current }
    throw ('-Yes was given but this value is missing or not valid: ' + $Prompt)
  }
  while ($true) {
    $shown = if ($Current) { " [$Current]" } else { '' }
    $answer = (Read-Host ($Prompt + $shown)).Trim().Trim('"')
    if (-not $answer) { $answer = $Current }
    if ($answer -and (& $Valid $answer)) { return $answer }
    Write-Host ('  That does not look right. ' + $Hint) -ForegroundColor Yellow
  }
}

# ---------------------------------------------------------------------------
# Checks of this PC
# ---------------------------------------------------------------------------

function Update-KitPath {
  # A program installed a moment ago (Python) is not on this window's PATH yet: re-read it.
  $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
  $user = [Environment]::GetEnvironmentVariable('Path', 'User')
  $env:Path = (@($machine, $user) | Where-Object { $_ }) -join ';'
}

function Get-KitPythonVersionOf([string]$Exe) {
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try { return ((& $Exe --version 2>&1) | Out-String).Trim() } catch { return '' } finally { $ErrorActionPreference = $previous }
}

function Get-KitPythonCandidates {
  # Every python.exe worth asking: the one on PATH, the ones the py launcher knows, and the usual install folders.
  # Several Pythons can be installed side by side, and the newest is often the one first on PATH.
  $paths = @()
  foreach ($c in @(Get-Command python -All -ErrorAction SilentlyContinue)) { if ($c.Source) { $paths += $c.Source } }
  if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($v in '3.12', '3.11', '3.10') {
      $previous = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
      try { $p = ((& py "-$v" -c 'import sys; print(sys.executable)' 2>$null) | Out-String).Trim() } catch { $p = '' } finally { $ErrorActionPreference = $previous }
      if ($p) { $paths += $p }
    }
  }
  foreach ($v in '312', '311', '310') {
    foreach ($root in @((Join-Path $env:LOCALAPPDATA 'Programs\Python'), $env:ProgramFiles, 'C:\')) {
      if ($root) { $paths += (Join-Path (Join-Path $root ('Python' + $v)) 'python.exe') }
    }
  }
  return @($paths | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } | Select-Object -Unique)
}

function Find-KitPython {
  $found = @()
  foreach ($exe in (Get-KitPythonCandidates)) { $found += [pscustomobject]@{ Path = $exe; Text = (Get-KitPythonVersionOf $exe) } }
  return $found
}

function Confirm-KitPython {
  $found = Find-KitPython
  $best = Select-KitPython $found
  if ($best) { Write-Ok ((Get-KitPythonVersionOf $best) + ' will be used (' + $best + ')'); $script:PythonExe = $best; return }
  $seen = (@($found | ForEach-Object { $_.Text }) | Where-Object { $_ } | Select-Object -Unique) -join ', '
  if ($seen) { Write-Warn ("Found $seen; the build needs Python 3.10, 3.11 or 3.12.") } else { Write-Warn 'Python was not found.' }
  if ($CheckOnly) { Write-Bad 'Python 3.10-3.12 is missing' 'Run install.cmd without -CheckOnly and it installs Python 3.12 for you (it can sit next to your other Python).'; return }
  $detail = ''
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host '         installing Python 3.12 with winget (a few minutes; your other Python is left alone) ...'
    $out = (& winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-String)
    $detail = 'winget exit code ' + $LASTEXITCODE + ': ' + (($out.Trim() -split "`n" | Select-Object -Last 2) -join ' ')
    Update-KitPath
    $best = Select-KitPython (Find-KitPython)
    if ($best) { Write-Ok ((Get-KitPythonVersionOf $best) + ' was installed (' + $best + ')'); $script:PythonExe = $best; return }
  } else { $detail = 'winget is not available on this PC' }
  Write-Bad ('Python 3.10-3.12 could not be installed automatically (' + $detail + ')') 'Install Python 3.12 from https://www.python.org/downloads/ (it can stay next to Python 3.13; tick "Add Python to PATH"), then double-click install.cmd again.'
}

function Confirm-KitSsh {
  foreach ($t in 'ssh', 'scp') {
    if (Get-Command $t -ErrorAction SilentlyContinue) { Write-Ok "$t is available" }
    else { Write-Bad "$t was not found" 'Settings > Apps > Optional features > Add a feature > OpenSSH Client, then double-click install.cmd again.' }
  }
}

function Confirm-KitPc {
  Write-Head 'Checking this PC'
  if ([Environment]::OSVersion.Platform -ne 'Win32NT') { Write-Bad 'This kit builds the Windows agent and must run on Windows' ''; return }
  if ([Environment]::Is64BitOperatingSystem) { Write-Ok '64-bit Windows' } else { Write-Bad 'A 64-bit version of Windows is required' '' }
  if ($PSVersionTable.PSVersion.Major -ge 5) { Write-Ok ('PowerShell ' + $PSVersionTable.PSVersion) } else { Write-Bad 'Windows PowerShell 5.1 or later is required' '' }
  Confirm-KitPython
  Confirm-KitSsh
  foreach ($site in @(@('pypi.org', 'https://pypi.org/simple/'), @('files.pythonhosted.org', 'https://files.pythonhosted.org/'), @('github.com', 'https://github.com/'))) {
    try { Invoke-WebRequest -UseBasicParsing -Method Head -Uri $site[1] -TimeoutSec 20 | Out-Null; Write-Ok ($site[0] + ' is reachable') }
    catch {
      # Any HTTP answer, even 404 for a page that does not exist, proves the site is reachable; only a network failure does not.
      if ($_.Exception.Response) { Write-Ok ($site[0] + ' is reachable') }
      else { Write-Warn ($site[0] + ' did not answer (' + $_.Exception.Message + '). The build downloads from it; behind a proxy, set HTTPS_PROXY first.') }
    }
  }
}

# ---------------------------------------------------------------------------
# Checks of the server
# ---------------------------------------------------------------------------

function Invoke-KitSsh {
  # Windows PowerShell 5.1 turns a native program's stderr into an error when the preference is Stop (ssh writes
  # harmless warnings there), so the preference is relaxed for this one call.
  param([string[]]$KeyArgs, [string]$Target, [string]$Command, [switch]$Show)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    if ($Show) {
      # Not captured: a key with a passphrase may ask for it. The server's host key is trusted on first use, with no question.
      & ssh @KeyArgs -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 $Target $Command
      return [pscustomobject]@{ Code = $LASTEXITCODE; Output = '' }
    }
    $out = & ssh @KeyArgs -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 $Target $Command 2>&1 | Out-String
    return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $out }
  } finally { $ErrorActionPreference = $previous }
}

function Confirm-KitServer {
  param([string]$Target, [string]$Key, [string]$ComposeDir)
  Write-Head ("Checking the server $Target")
  $script:KitSshKey = ''
  $attempt = 0
  while ($true) {
    $attempt++
    if ($Key) {
      if (Test-Path -LiteralPath $Key -PathType Leaf) { Write-Ok "ssh key file found: $Key" } else { Write-Bad "The ssh key file was not found: $Key" 'Check the path, or leave it empty if you use ssh-agent.'; return $null }
    }
    $keyArgs = if ($Key) { @('-i', $Key) } else { @() }
    $hello = Invoke-KitSsh $keyArgs $Target 'echo vedha-ssh-ok' -Show
    if ($hello.Code -eq 0) { break }
    Write-Bad "Cannot log in to $Target (ssh exit code $($hello.Code); its message is above)" 'Check the user name (ubuntu on Ubuntu, ec2-user on Amazon Linux) and that the server is running and port 22 is open to this PC.'
    if ($Yes -or $CheckOnly -or $attempt -ge 3) { return $null }
    # "Permission denied (publickey)" means the server did not accept the key (or none was given). Ask for the file now.
    $script:Problems = @($script:Problems | Select-Object -SkipLast 1)
    Write-Host ''
    Write-Host '  The server did not accept the login. A server on AWS needs the key file (.pem) you were given when it was created.' -ForegroundColor Yellow
    Write-Host '  Tip: in File Explorer search your PC for *.pem; the file name is the "Key pair name" shown for the server in the AWS console.'
    $new = (Read-Host '  Paste the full path of the key file (for example C:\Users\you\Downloads\mykey.pem), or press Enter to stop').Trim().Trim('"')
    if (-not $new) { Write-Bad "Cannot log in to $Target without a key file" 'Run install.cmd again with the key file (option 2), or add your own key to the server (see the steps in the chat).'; return $null }
    if (-not (Test-KitKeyPath $new)) { Write-Warn 'That does not look like a Windows path such as C:\Users\you\Downloads\mykey.pem'; continue }
    $Key = $new
    $script:KitSshKey = $new
  }
  Write-Ok "logged in to $Target"
  $facts = $null
  while ($true) {
    $r = Invoke-KitSsh $keyArgs $Target (Get-KitRemoteLayoutCommand $ComposeDir)
    $facts = Get-KitRemoteFacts $r.Output
    if ($facts.ComposeFile -and $facts.EnvFile) { break }
    Write-Bad "The manager folder $ComposeDir does not hold docker-compose.yml and .env" 'On the server run:  docker compose ls   (it shows the folder), then enter that folder here.'
    if ($Yes -or $CheckOnly) { return $null }
    $script:Problems = @($script:Problems | Select-Object -SkipLast 1)
    $ComposeDir = Read-KitValue 'Folder on the server that holds docker-compose.yml' $ComposeDir ${function:Test-KitRemoteDir} 'It must be an absolute path such as /opt/Project-Vedha/manager.'
  }
  Write-Ok "manager folder found: $ComposeDir"
  if ($facts.Docker) { Write-Ok "$Target may run docker" }
  else { Write-Bad "$Target is not allowed to run docker" 'On the server run:  sudo usermod -aG docker <user>   then log out and in again.' }
  return $ComposeDir
}

function Show-KitSettings($S) {
  Write-Head 'These settings will be used'
  Write-Host ('  1) Server login ........... ' + $S.server)
  Write-Host ('  2) ssh key file ........... ' + $(if ($S.ssh_key) { $S.ssh_key } else { '(none: ssh uses its own default key)' }))
  Write-Host ('  3) Manager address ........ ' + $S.manager_url)
  Write-Host ('  4) Installs without token . ' + $(if ($S.tokenless) { 'yes (you approve each machine in Fleet)' } else { 'no (a token from Fleet is needed)' }))
}

function Read-KitChange([string]$Prompt, [string]$Current, [scriptblock]$Valid, [string]$Hint) {
  while ($true) {
    $answer = (Read-Host ($Prompt + $(if ($Current) { " [$Current]" } else { '' }))).Trim().Trim('"')
    if (-not $answer) { return $Current }
    if (& $Valid $answer) { return $answer }
    Write-Host ('  That does not look right. ' + $Hint) -ForegroundColor Yellow
  }
}

function Edit-KitSettings($S) {
  # One screen, one Enter. Typing a number changes that one value.
  while ($true) {
    Show-KitSettings $S
    Write-Host ''
    $c = (Read-Host 'Press Enter to start, or type 1-4 to change one').Trim()
    if (-not $c) { return $S }
    if ($c -eq '1') { $S.server = Read-KitChange 'Server login (user@address)' $S.server ${function:Test-KitServer} 'Use user@address with letters, digits, dots and dashes only.' }
    elseif ($c -eq '2') {
      $v = Read-KitChange 'ssh key file (full path, empty for none)' $S.ssh_key { param($x) (Test-KitKeyPath $x) } 'It must look like C:\Users\you\keys\server.pem'
      $S.ssh_key = $v
    }
    elseif ($c -eq '3') { $S.manager_url = (Read-KitChange 'Manager address (https://...)' $S.manager_url ${function:Test-KitManagerUrl} 'It must start with https:// and have no path, for example https://api.example.com').TrimEnd('/') }
    elseif ($c -eq '4') { $S.tokenless = -not $S.tokenless }
    else { Write-Host '  Type 1, 2, 3 or 4, or just press Enter.' -ForegroundColor Yellow }
  }
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

function Invoke-KitMain {
  $kitRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
  $version = ''
  $vf = Join-Path $kitRoot 'VERSION'
  if (Test-Path -LiteralPath $vf) { $version = (Get-Content -LiteralPath $vf -TotalCount 1).Trim() }
  Write-Host ''
  Write-Host ('Vedha agent build kit ' + $version) -ForegroundColor Cyan
  Write-Host 'This checks everything it needs, then builds, signs and publishes the Windows agent.'

  $userHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { [Environment]::GetFolderPath('UserProfile') }
  $settingsPath = Get-KitSettingsPath $userHome
  $saved = @{ server = ''; ssh_key = ''; manager_url = ''; remote_compose_dir = ''; tokenless = $false }
  if (Test-Path -LiteralPath $settingsPath) { $saved = ConvertFrom-KitSettingsJson (Get-Content -Raw -LiteralPath $settingsPath) }

  # Defaults, weakest first: the kit's own, then what was used last time, then what was given on the command line.
  $defaults = @{ server = ''; ssh_key = ''; manager_url = ''; remote_compose_dir = ''; tokenless = $false }
  $defaultsPath = Join-Path $PSScriptRoot 'kit-defaults.json'
  if (Test-Path -LiteralPath $defaultsPath) { $defaults = ConvertFrom-KitSettingsJson (Get-Content -Raw -LiteralPath $defaultsPath) }
  $S = @{ server = $defaults.server; ssh_key = $defaults.ssh_key; manager_url = $defaults.manager_url
          remote_compose_dir = $defaults.remote_compose_dir; tokenless = [bool]$defaults.tokenless }
  foreach ($k in 'server', 'ssh_key', 'manager_url', 'remote_compose_dir') { if ($saved[$k]) { $S[$k] = $saved[$k] } }
  if ($saved.tokenless) { $S.tokenless = $true }
  if ($Server) { $S.server = $Server }
  if ($SshKey) { $S.ssh_key = $SshKey }
  if ($ManagerUrl) { $S.manager_url = $ManagerUrl.TrimEnd('/') }
  if ($RemoteComposeDir) { $S.remote_compose_dir = $RemoteComposeDir }
  if ($AllowTokenlessInstall) { $S.tokenless = $true }
  if (-not $S.remote_compose_dir) { $S.remote_compose_dir = Get-KitDefaultComposeDir }
  $autoKey = $false
  if (-not $S.ssh_key) {
    $keys = @(Find-KitSshKeys (Get-KitKeyFolders $userHome $kitRoot))
    if ($keys.Count -gt 0) { $S.ssh_key = $keys[0]; $autoKey = $true }
  }
  if ($autoKey) { Write-Host ('  (found an ssh key file automatically: ' + $S.ssh_key + ')') }

  if ($Yes) {
    if (-not $S.server) { throw '-Yes needs a server login (-Server user@address).' }
    if (-not $S.manager_url) { throw '-Yes needs the manager address (-ManagerUrl https://...).' }
  } else {
    if (-not $S.server) { $S.server = Read-KitChange 'Server login (user@address)' '' ${function:Test-KitServer} 'Use user@address with letters, digits, dots and dashes only.' }
    if (-not $S.manager_url) { $S.manager_url = (Read-KitChange 'Manager address (https://...)' '' ${function:Test-KitManagerUrl} 'It must start with https:// and have no path, for example https://api.example.com').TrimEnd('/') }
    $S = Edit-KitSettings $S
  }
  if (-not (Test-KitServer $S.server)) { throw "The server login must look like user@address (got '$($S.server)')." }
  if (-not (Test-KitManagerUrl $S.manager_url)) { throw "The manager address must look like https://api.example.com (got '$($S.manager_url)')." }
  if ($S.ssh_key -and -not (Test-KitKeyPath $S.ssh_key)) { throw "The ssh key path must look like C:\Users\you\keys\server.pem (got '$($S.ssh_key)')." }
  if (-not (Test-KitRemoteDir $S.remote_compose_dir)) { throw "The server folder must be an absolute path such as /opt/Project-Vedha/manager (got '$($S.remote_compose_dir)')." }
  $Server = $S.server; $SshKey = $S.ssh_key; $ManagerUrl = $S.manager_url; $RemoteComposeDir = $S.remote_compose_dir; $tokenless = [bool]$S.tokenless

  Confirm-KitPc
  if (Get-Command ssh -ErrorAction SilentlyContinue) {
    $composeDir = Confirm-KitServer -Target $Server -Key $SshKey -ComposeDir $RemoteComposeDir
    if ($composeDir) { $RemoteComposeDir = $composeDir }
    if ($script:KitSshKey) { $SshKey = $script:KitSshKey }      # the key file the person pasted when the first try was refused
  } else {
    Write-Head 'Checking the server'
    Write-Warn 'Skipped: ssh is not installed yet (see above).'
  }

  if ($script:Problems.Count -gt 0) {
    Write-Host ''
    Write-Host ('Stopped: ' + $script:Problems.Count + ' thing(s) need fixing first (see [FAIL] above). Nothing was built or changed.') -ForegroundColor Red
    return 1
  }

  New-Item -ItemType Directory -Force -Path (Split-Path $settingsPath -Parent) | Out-Null
  [System.IO.File]::WriteAllText($settingsPath, (ConvertTo-KitSettingsJson $Server $SshKey $ManagerUrl $RemoteComposeDir $tokenless), (New-Object System.Text.UTF8Encoding($false)))
  if ($CheckOnly) { Write-Host ''; Write-Host 'All checks passed. Nothing was built or changed (-CheckOnly).' -ForegroundColor Green; return 0 }

  $release = if ($RemoteReleaseDir) { $RemoteReleaseDir } else { ($RemoteComposeDir.TrimEnd('/') + '/agent-releases') }
  if (-not (Test-KitRemoteDir $release)) { throw "Not a safe release folder on the server: '$release'" }
  $publishArgs = Get-KitPublishArguments -Server $Server -SshKey $SshKey -ManagerUrl $ManagerUrl -ComposeDir $RemoteComposeDir `
    -ReleaseDir $release -Tokenless $tokenless -DryRun ([bool]$DryRun) -SkipBuild ([bool]$SkipBuild) -PythonExe ([string]$script:PythonExe)
  Write-Host ''
  Write-Host ('Starting: building and publishing release ' + $version + ' (15-35 minutes the first time). Leave this window open.') -ForegroundColor Cyan

  $publish = Join-Path $PSScriptRoot 'publish-release.ps1'
  $global:LASTEXITCODE = 0
  & powershell -NoProfile -ExecutionPolicy Bypass -File $publish @publishArgs
  $code = $LASTEXITCODE
  if ($code -ne 0) {
    Write-Host ''
    Write-Host 'The publish step stopped (see the red text above). Fix that and double-click install.cmd again: it picks up where it can.' -ForegroundColor Red
    return $code
  }
  if (-not $DryRun) {
    $keys = Join-Path $userHome '.vedha'
    Write-Host ''
    Write-Host 'DONE. Next:' -ForegroundColor Green
    Write-Host '  1. Back up the folder that just opened (your signing keys): copy it somewhere safe and offline. Never send it to anyone.'
    Write-Host '  2. Open Fleet > Add agent: the Windows install command is there now.'
    if (Test-Path -LiteralPath $keys) { try { Start-Process explorer.exe $keys } catch { } }
  }
  return 0
}

if ($MyInvocation.InvocationName -ne '.') {
  $exit = 1
  try { $exit = [int](@(Invoke-KitMain) | Select-Object -Last 1) }
  catch { Write-Host ''; Write-Host ('STOPPED: ' + $_.Exception.Message) -ForegroundColor Red }
  if (-not $NoPause) { Write-Host ''; [void](Read-Host 'Press Enter to close this window') }
  exit $exit
}
