<#
  Vedha agent build kit - the ONE script to run.   Double-click  install.cmd  in the kit folder.

  What it does, in order. It stops at the first thing it cannot fix and says exactly what to do:
    1  asks for the three things only you know (server login, ssh key file, manager https address),
       remembers them in %USERPROFILE%\.vedha\kit-settings.json (no passwords, no key contents)
    2  checks THIS PC: 64-bit Windows, PowerShell 5.1+, free disk space, Python 3.10-3.12 (installs
       Python 3.12 with winget when it is missing), ssh and scp, internet access to the build downloads,
       the ssh key file
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

function Test-KitPythonOutput([string]$Text) {
  # 'Python 3.12.4' -> true for 3.10, 3.11, 3.12 only (the build needs a version Nuitka and the pins support).
  return [bool]($Text -match '^\s*Python 3\.(10|11|12)\.\d+')
}

function Get-KitDefaultComposeDir { return '/opt/Project-Vedha/manager' }

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
        [bool]$Tokenless, [bool]$DryRun, [bool]$SkipBuild)
  $a = @('-Server', $Server)
  if ($SshKey) { $a += @('-SshKey', $SshKey) }
  $a += @('-ManagerUrl', $ManagerUrl.TrimEnd('/'), '-ConfigureManager')
  if ($ComposeDir) { $a += @('-RemoteComposeDir', $ComposeDir) }
  if ($ReleaseDir) { $a += @('-RemoteReleaseDir', $ReleaseDir) }
  if ($Tokenless) { $a += '-AllowTokenlessInstall' }
  if ($DryRun) { $a += '-DryRun' }
  if ($SkipBuild) { $a += '-SkipBuild' }
  return $a
}

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

$script:Problems = @()
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

function Get-KitPythonVersionText {
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try { return ((& python --version 2>&1) | Out-String).Trim() } catch { return '' } finally { $ErrorActionPreference = $previous }
}

function Confirm-KitPython {
  $text = Get-KitPythonVersionText
  if (Test-KitPythonOutput $text) { Write-Ok ($text + ' is installed'); return }
  if ($text) { Write-Warn ("Found '$text'; the build needs Python 3.10, 3.11 or 3.12.") } else { Write-Warn 'Python was not found.' }
  if ($CheckOnly) { Write-Bad 'Python 3.10-3.12 is missing' 'Run install.cmd without -CheckOnly and it installs Python 3.12 for you.'; return }
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host '         installing Python 3.12 with winget (a few minutes; nothing else on this PC is changed) ...'
    & winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Update-KitPath
    $text = Get-KitPythonVersionText
    if (Test-KitPythonOutput $text) { Write-Ok ($text + ' was installed'); return }
  }
  Write-Bad 'Python 3.10-3.12 could not be installed automatically' 'Install Python 3.12 from https://www.python.org/downloads/ (tick "Add Python to PATH"), then double-click install.cmd again.'
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
  try {
    $drive = (Get-Item -LiteralPath $PSScriptRoot).PSDrive
    $freeGb = [math]::Round($drive.Free / 1GB, 1)
    if ($freeGb -ge 5) { Write-Ok ("$freeGb GB free on " + $drive.Name + ':') }
    else { Write-Bad ("Only $freeGb GB free on " + $drive.Name + ': (5 GB are needed for the build)') 'Free some disk space and run again.' }
  } catch { Write-Warn 'Could not read the free disk space.' }
  Confirm-KitPython
  Confirm-KitSsh
  foreach ($site in @(@('pypi.org', 'https://pypi.org/simple/'), @('files.pythonhosted.org', 'https://files.pythonhosted.org/'), @('github.com', 'https://github.com/'))) {
    try { Invoke-WebRequest -UseBasicParsing -Method Head -Uri $site[1] -TimeoutSec 20 | Out-Null; Write-Ok ($site[0] + ' is reachable') }
    catch { Write-Warn ($site[0] + ' did not answer (' + $_.Exception.Message + '). The build downloads from it; behind a proxy, set HTTPS_PROXY first.') }
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
      # Not captured: the first connection asks whether to trust the server, and a key may ask for its passphrase.
      & ssh @KeyArgs -o ConnectTimeout=20 $Target $Command
      return [pscustomobject]@{ Code = $LASTEXITCODE; Output = '' }
    }
    $out = & ssh @KeyArgs -o ConnectTimeout=20 $Target $Command 2>&1 | Out-String
    return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $out }
  } finally { $ErrorActionPreference = $previous }
}

function Confirm-KitServer {
  param([string]$Target, [string]$Key, [string]$ComposeDir)
  Write-Head ("Checking the server $Target")
  if ($Key) {
    if (Test-Path -LiteralPath $Key -PathType Leaf) { Write-Ok "ssh key file found: $Key" } else { Write-Bad "The ssh key file was not found: $Key" 'Check the path, or leave it empty if you use ssh-agent.'; return $null }
  }
  $keyArgs = if ($Key) { @('-i', $Key) } else { @() }
  Write-Host '         (the first time, ssh asks whether to trust the server: type yes)'
  $hello = Invoke-KitSsh $keyArgs $Target 'echo vedha-ssh-ok' -Show
  if ($hello.Code -ne 0) {
    Write-Bad "Cannot log in to $Target (ssh exit code $($hello.Code); its message is above)" 'Check the user name (ubuntu on Ubuntu, ec2-user on Amazon Linux), the key file, and that the server is running and port 22 is open to this PC.'
    return $null
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

  Write-Head 'What this needs to know (Enter keeps the value shown)'
  if (-not $Server) { $Server = $saved.server }
  $Server = Read-KitValue 'Server login (user@address, for example ubuntu@16.4.75.44)' $Server ${function:Test-KitServer} 'Use user@address with letters, digits, dots and dashes only.'
  if (-not $SshKey) { $SshKey = $saved.ssh_key }
  if (-not $Yes) {
    $answer = (Read-Host ('ssh key file (C:\path\key.pem), empty if you use ssh-agent' + $(if ($SshKey) { " [$SshKey]" } else { '' }))).Trim().Trim('"')
    if ($answer) { $SshKey = $answer }
  }
  if ($SshKey -and -not (Test-KitKeyPath $SshKey)) { throw "The ssh key path must look like C:\Users\you\keys\server.pem (got '$SshKey')." }
  if (-not $ManagerUrl) { $ManagerUrl = $saved.manager_url }
  $ManagerUrl = (Read-KitValue 'Manager address (https://...)' $ManagerUrl ${function:Test-KitManagerUrl} 'It must start with https:// and have no path, for example https://api.example.com').TrimEnd('/')
  if (-not $RemoteComposeDir) { $RemoteComposeDir = if ($saved.remote_compose_dir) { $saved.remote_compose_dir } else { Get-KitDefaultComposeDir } }
  if ($RemoteComposeDir -and -not (Test-KitRemoteDir $RemoteComposeDir)) { throw "The server folder must be an absolute path such as /opt/Project-Vedha/manager (got '$RemoteComposeDir')." }
  $tokenless = ([bool]$AllowTokenlessInstall) -or ([bool]$saved.tokenless)
  if (-not $Yes -and -not $AllowTokenlessInstall) {
    $t = (Read-Host ('Let machines install with no token (you approve each one in Fleet)? [' + $(if ($tokenless) { 'Y/n' } else { 'y/N' }) + ']')).Trim().ToLower()
    if ($t) { $tokenless = ($t -eq 'y' -or $t -eq 'yes') }
  }

  Confirm-KitPc
  if (Get-Command ssh -ErrorAction SilentlyContinue) {
    $composeDir = Confirm-KitServer -Target $Server -Key $SshKey -ComposeDir $RemoteComposeDir
    if ($composeDir) { $RemoteComposeDir = $composeDir }
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
    -ReleaseDir $release -Tokenless $tokenless -DryRun ([bool]$DryRun) -SkipBuild ([bool]$SkipBuild)
  if (-not $Yes -and -not $DryRun) {
    Write-Host ''
    Write-Host ('Ready. This builds the Windows agent (15-35 minutes the first time), signs release ' + $version + ',') 
    Write-Host ("uploads it to $Server, sets the public keys in $RemoteComposeDir/.env and restarts the manager's api.")
    [void](Read-Host 'Press Enter to start (close this window to cancel)')
  }

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
