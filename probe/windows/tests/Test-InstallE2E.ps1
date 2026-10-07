<#
  End-to-end test of the customer package on a REAL Windows machine: it unzips the package
  exactly as a customer would and runs install.cmd, so it exercises the real scheduled task,
  the real permissions, and the real compiled agent.

  It INSTALLS AND REMOVES THE AGENT on the machine it runs on, so it refuses to run anywhere
  but a CI runner unless -Force is given, and refuses if an agent is already installed.

      pwsh -NoProfile -File windows/tests/Test-InstallE2E.ps1 -ZipPath dist\vedha-agent-win.zip

  The manager used is https://127.0.0.1:9 (nothing listens there), so this proves the install
  mechanics, the permissions, the logging, the diagnostics and the failure messages. A real
  enrolment against a manager is a separate check.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$ZipPath,
  [switch]$Force
)
$ErrorActionPreference = 'Stop'

# Safety first: this script installs and removes the agent on the machine it runs on.
if ($env:GITHUB_ACTIONS -ne 'true' -and -not $Force) { throw 'Refusing to run: this installs and removes the agent on THIS computer. Run it in CI, or pass -Force.' }
if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'This test runs on Windows only.' }

$AppDir  = Join-Path $env:ProgramFiles 'Vedha Agent'
$DataDir = Join-Path $env:ProgramData 'vedha-agent'
$Exe     = Join-Path $AppDir 'vedha-agent.exe'
$Token   = 'vet_ci_test_token_AbCdEf123456'
$Manager = 'https://127.0.0.1:9'
$Work    = Join-Path $(if ($env:RUNNER_TEMP) { $env:RUNNER_TEMP } else { $env:TEMP }) 'vedha-e2e'
$Pkg     = Join-Path $Work 'pkg'

# ---- safety -------------------------------------------------------------------------------
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'Run as Administrator.' }
if ((Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue) -or (Test-Path $AppDir) -or (Test-Path $DataDir)) {
  if (-not $Force) { throw 'An agent is already installed on this computer; refusing to touch it.' }
}

$script:Failures = @()
$script:Passed = 0

function Check {
  param([string]$Name, [scriptblock]$Body)
  try { & $Body; $script:Passed++; Write-Host "  ok    $Name" -ForegroundColor Green }
  catch { $script:Failures += "$Name :: $($_.Exception.Message)"; Write-Host "  FAIL  $Name :: $($_.Exception.Message)" -ForegroundColor Red }
}
function Expect([bool]$Condition, [string]$Message) { if (-not $Condition) { throw $Message } }

function Invoke-Package {
  # Runs install.cmd the way a customer does. Returns the exit code and everything it printed.
  param([string]$Dir, [string[]]$Arguments)
  $output = (& (Join-Path $Dir 'install.cmd') @Arguments 2>&1 | Out-String)
  return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $output }
}
function Invoke-Agent {
  param([string[]]$Arguments)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try { $output = (& $Exe @Arguments 2>&1 | Out-String); return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $output } }
  finally { $ErrorActionPreference = $previous }
}
function Show-State {
  Write-Host '----- state at failure -----'
  foreach ($path in @((Join-Path $DataDir 'logs\agent.log'))) {
    if (Test-Path $path) { Write-Host "[$path]"; Get-Content $path -Tail 60 }
  }
  Get-ChildItem (Join-Path $DataDir 'logs') -Filter 'install-*.log' -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "[$($_.FullName)]"; Get-Content $_.FullName -Tail 80 }
  if (Test-Path $Exe) { Write-Host '[status]'; (Invoke-Agent @('status')).Output }
  Write-Host '[icacls data]'; icacls $DataDir 2>&1
  Write-Host '[task]'; Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue | Format-List *
}

try {
  Write-Host "Windows PowerShell $($PSVersionTable.PSVersion) hosts the customer's installer (via install.cmd)."
  if (Test-Path $Work) { Remove-Item $Work -Recurse -Force }
  New-Item -ItemType Directory -Path $Work | Out-Null
  Expand-Archive -LiteralPath $ZipPath -DestinationPath $Pkg

  Write-Host "`n== The package =="
  Check 'package has everything a customer needs' {
    foreach ($f in 'install.cmd', 'install.ps1', 'uninstall.cmd', 'uninstall.ps1', 'run.cmd', 'README.txt', 'ALLOWLIST.txt', 'SHA256SUMS.txt', 'vedha-agent\vedha-agent.exe') {
      Expect (Test-Path (Join-Path $Pkg $f)) "missing $f"
    }
  }
  Check 'the compiled agent bundles its own Python runtime (no dependency on the customer machine)' {
    $python = Get-ChildItem (Join-Path $Pkg 'vedha-agent') -Filter 'python3*.dll' -Recurse | Select-Object -First 1
    Expect ($null -ne $python) 'python3xx.dll is not in the package'
    $vc = Get-ChildItem (Join-Path $Pkg 'vedha-agent') -Filter 'vcruntime140*.dll' -Recurse | Select-Object -First 1
    Write-Host "         python runtime: $($python.Name); Visual C++ runtime bundled: $(if ($vc) { $vc.Name } else { 'NO (relies on the machine having it)' })"
  }
  Check 'the manager address and version are baked in or the installer asks for -Manager' {
    $text = Get-Content (Join-Path $Pkg 'install.ps1') -Raw
    Expect ($text -notmatch "'__VEDHA_PACKAGE_VERSION__'") 'package version placeholder was not replaced'
  }

  # What a Windows PowerShell started from this session can see. install.cmd does exactly this, and a
  # customer may also run it from a PowerShell 7 prompt. Printed for diagnosis; not a pass/fail check.
  $probe = Join-Path $Work 'child-env.ps1'
  Set-Content -LiteralPath $probe -Value @(
    "`$missing = @('Get-FileHash','Get-ScheduledTask','Register-ScheduledTask','ConvertFrom-Json','Expand-Archive') | Where-Object { -not (Get-Command `$_ -ErrorAction SilentlyContinue) }",
    "'child PSVersion : ' + `$PSVersionTable.PSVersion",
    "'child cannot find: ' + `$(if (`$missing) { `$missing -join ', ' } else { '(nothing missing)' })",
    "'child PSModulePath: ' + `$env:PSModulePath"
  )
  Write-Host "`n== Windows PowerShell as started from here =="
  & powershell -NoProfile -ExecutionPolicy Bypass -File $probe 2>&1 | ForEach-Object { Write-Host "  $_" }

  Write-Host "`n== Things that must stop BEFORE anything is installed =="
  Check 'a damaged package is refused and names the file' {
    $bad = Join-Path $Work 'pkg-damaged'
    Copy-Item $Pkg $bad -Recurse
    Add-Content -Path (Join-Path $bad 'README.txt') -Value 'tampered'
    $r = Invoke-Package $bad @('-Manager', $Manager, '-Token', $Token, '-NoPause')
    Expect ($r.Code -ne 0) "exit code was $($r.Code)"
    Expect ($r.Output -match 'Changed or damaged: README.txt') "output did not name the damaged file:`n$($r.Output)"
    Expect (-not (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue)) 'a task was created'
    Expect (-not (Test-Path $AppDir)) 'the program folder was created'
  }
  Check 'a missing agent program (antivirus quarantine) is explained' {
    $bad = Join-Path $Work 'pkg-quarantined'
    Copy-Item $Pkg $bad -Recurse
    Remove-Item (Join-Path $bad 'vedha-agent\vedha-agent.exe')
    $r = Invoke-Package $bad @('-Manager', $Manager, '-Token', $Token, '-NoPause')
    Expect ($r.Code -ne 0) 'did not fail'
    Expect ($r.Output -match 'Missing: vedha-agent' -and $r.Output -match 'antivirus') "no antivirus hint:`n$($r.Output)"
  }
  Check 'something that is not an install token is refused with a clear message' {
    $r = Invoke-Package $Pkg @('-Manager', $Manager, '-Token', 'notatoken', '-NoPause')
    Expect ($r.Code -ne 0 -and $r.Output -match 'does not look like an install token') "unexpected:`n$($r.Output)"
  }
  Check 'a non-https manager address is refused' {
    $r = Invoke-Package $Pkg @('-Manager', 'http://manager.example.com', '-Token', $Token, '-NoPause')
    Expect ($r.Code -ne 0 -and $r.Output -match 'must look like https') "unexpected:`n$($r.Output)"
  }
  Check 'an unreachable manager stops the install with the cause and the fix, and changes nothing' {
    $r = Invoke-Package $Pkg @('-Manager', $Manager, '-Token', $Token, '-NoPause')
    Expect ($r.Code -ne 0) 'did not fail'
    Expect ($r.Output -match 'cannot connect to 127\.0\.0\.1:9') "the cause was not stated:`n$($r.Output)"
    Expect ($r.Output -match 'firewall') 'no fix was given'
    Expect (-not (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue)) 'a task was created'
    Expect (-not (Test-Path $AppDir)) 'the program folder was created'
    Expect ($r.Output -notmatch [regex]::Escape($Token)) 'the token was echoed'
  }

  Write-Host "`n== Install =="
  $install = $null
  Check 'install.cmd -Token ... installs and exits 0' {
    $script:install = Invoke-Package $Pkg @('-Manager', $Manager, '-Token', $Token, '-SkipPreflight', '-NoWait', '-NoPause', '-Scope', '10.99.0.0/24', '-Name', 'ci-probe')
    Expect ($script:install.Code -eq 0) "exit code $($script:install.Code):`n$($script:install.Output)"
  }
  Check 'program installed under Program Files and it runs' {
    Expect (Test-Path $Exe) 'vedha-agent.exe is not in Program Files'
    $v = Invoke-Agent @('version')
    Expect ($v.Code -eq 0 -and $v.Output -match 'Vedha Probe \d') "version failed: $($v.Output)"
  }
  Check 'scheduled task runs the agent directly, as SYSTEM, at startup' {
    $t = Get-ScheduledTask -TaskName 'VedhaAgent'
    Expect ($t.Principal.UserId -eq 'SYSTEM') "runs as $($t.Principal.UserId)"
    Expect ($t.Actions[0].Execute -eq $Exe) "executes $($t.Actions[0].Execute)"
    Expect ($t.Actions[0].Arguments -eq 'run') "arguments $($t.Actions[0].Arguments)"
    Expect (@($t.Triggers | Where-Object { $_.CimClass.CimClassName -match 'BootTrigger' }).Count -ge 1) 'no start-at-boot trigger'
  }
  Check 'identity, settings and logs are readable only by SYSTEM and Administrators' {
    . (Join-Path $Pkg 'install.ps1')
    Expect (Test-AclLocked (icacls $DataDir)) "data folder is not locked:`n$(icacls $DataDir | Out-String)"
    $app = (icacls $AppDir | Out-String)
    Expect ($app -notmatch 'Users:[^\r\n]*\((F|M|W)\)' -and $app -notmatch 'Everyone') "the program folder is writable by non-administrators:`n$app"
  }
  Check 'settings file is correct, has no byte-order mark, and carries the one-time token' {
    $path = Join-Path $DataDir 'agent.env'
    $bytes = [System.IO.File]::ReadAllBytes($path)
    Expect (-not ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)) 'file starts with a byte-order mark'
    $cfg = Read-VedhaConfig -Text ([System.IO.File]::ReadAllText($path))
    Expect ($cfg['PLATFORM_URL'] -eq $Manager) "manager: $($cfg['PLATFORM_URL'])"
    Expect ($cfg['PROBE_NETWORK_SEGMENTS'] -eq '10.99.0.0/24') "scope: $($cfg['PROBE_NETWORK_SEGMENTS'])"
    Expect ($cfg['PROBE_NAME'] -eq 'ci-probe') "name: $($cfg['PROBE_NAME'])"
    Expect ($cfg['PROBE_ENROLL_TOKEN'] -eq $Token) 'token line missing'
    Expect ($cfg['PROBE_BUILD_DIGEST'] -eq (Get-FileHash $Exe -Algorithm SHA256).Hash.ToLower()) 'build digest does not match the installed program'
  }
  Check 'the install log exists and does not contain the token' {
    $log = Get-ChildItem (Join-Path $DataDir 'logs') -Filter 'install-*.log' | Sort-Object LastWriteTime | Select-Object -Last 1
    Expect ($null -ne $log) 'no install log'
    $text = Get-Content $log.FullName -Raw
    Expect ($text -notmatch [regex]::Escape($Token)) 'the install log contains the raw token'
  }

  Write-Host "`n== The running agent =="
  $status = $null
  Check 'the agent starts and reports that it cannot reach the manager, with why and the fix' {
    $deadline = (Get-Date).AddSeconds(120)
    do {
      Start-Sleep -Seconds 3
      $r = Invoke-Agent @('status', '--json')
      try { $script:status = $r.Output | ConvertFrom-Json } catch { $script:status = $null }
    } while ((Get-Date) -lt $deadline -and ($null -eq $script:status -or $script:status.state -in @('not-running', 'starting')))
    Expect ($null -ne $script:status) "status was not valid JSON: $($r.Output)"
    Expect ($script:status.state -in @('retrying', 'enrolling', 'failed')) "state was '$($script:status.state)' ($($script:status.detail))"
    Expect ($script:status.running -eq $true -or $script:status.state -eq 'failed') 'the agent process is not running'
    Expect ($script:status.state -eq 'enrolling' -or $script:status.reason) 'no reason was reported'
    Expect ($script:status.agent_version -match '^\d+\.\d+') 'no agent version'
  }
  Check 'the agent writes a readable log file (a Scheduled Task has no console)' {
    $log = Join-Path $DataDir 'logs\agent.log'
    Expect (Test-Path $log) 'agent.log was not created'
    Expect ((Get-Content $log -Raw) -match 'Vedha Probe') 'agent.log has no start-up line'
  }

  Write-Host "`n== Troubleshooting commands on the installed agent =="
  Check 'doctor explains the problem and exits non-zero' {
    $r = Invoke-Agent @('doctor')
    Expect ($r.Code -eq 1) "exit code $($r.Code)"
    Expect ($r.Output -match 'cannot connect to 127\.0\.0\.1:9' -and $r.Output -match 'RESULT:') "doctor output:`n$($r.Output)"
  }
  Check 'status prints a human summary' {
    $r = Invoke-Agent @('status')
    Expect ($r.Output -match 'Status\s+:' -and $r.Output -match 'ci-probe|10\.99\.0\.0/24') "status output:`n$($r.Output)"
  }
  Check 'support-bundle contains the diagnosis and no secret' {
    $zip = Join-Path $Work 'bundle.zip'
    $r = Invoke-Agent @('support-bundle', '--out', $zip)
    Expect ($r.Code -eq 0 -and (Test-Path $zip)) "no bundle:`n$($r.Output)"
    $dir = Join-Path $Work 'bundle'
    Expand-Archive -LiteralPath $zip -DestinationPath $dir
    $names = (Get-ChildItem $dir -Recurse -File).Name
    foreach ($n in 'doctor.txt', 'status.json', 'system.txt', 'configuration.txt', 'README.txt', 'agent.log') { Expect ($names -contains $n) "bundle lacks $n" }
    Expect (-not ($names -contains 'state.json')) 'the identity file is in the bundle'
    $all = (Get-ChildItem $dir -Recurse -File | ForEach-Object { Get-Content $_.FullName -Raw }) -join "`n"
    Expect ($all -notmatch [regex]::Escape($Token)) 'the install token is in the bundle'
    Expect ($all -match 'PROBE_ENROLL_TOKEN=\[removed\]') 'the token setting was not masked'
  }

  Write-Host "`n== Repair, then uninstall =="
  Check '-Repair re-applies the install, keeps the settings and removes the leftover token' {
    $r = Invoke-Package $Pkg @('-Repair', '-SkipPreflight', '-NoWait', '-NoPause')
    Expect ($r.Code -eq 0) "exit code $($r.Code):`n$($r.Output)"
    $cfg = Read-VedhaConfig -Text ([System.IO.File]::ReadAllText((Join-Path $DataDir 'agent.env')))
    Expect ($cfg['PLATFORM_URL'] -eq $Manager -and $cfg['PROBE_NAME'] -eq 'ci-probe' -and $cfg['PROBE_NETWORK_SEGMENTS'] -eq '10.99.0.0/24') 'settings were not kept'
    Expect (-not $cfg.ContainsKey('PROBE_ENROLL_TOKEN')) 'the token is still in the settings file'
    Expect (-not (Test-Path "$AppDir.old")) 'a backup folder was left behind'
    Expect ($null -ne (Get-ScheduledTask -TaskName 'VedhaAgent')) 'the task is gone'
  }
  Check 'uninstall removes the program and task but keeps the identity and logs' {
    $r = Invoke-Package $Pkg @('-Uninstall', '-NoPause')
    Expect ($r.Code -eq 0) "exit code $($r.Code):`n$($r.Output)"
    Expect (-not (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue)) 'the task is still there'
    Expect (-not (Test-Path $AppDir)) 'the program folder is still there'
    Expect (Test-Path $DataDir) 'the data folder was deleted without -Purge'
    Expect (-not (Get-Process -Name 'vedha-agent' -ErrorAction SilentlyContinue)) 'the agent is still running'
  }
  Check 'uninstall -Purge deletes everything' {
    $r = Invoke-Package $Pkg @('-Uninstall', '-Purge', '-NoPause')
    Expect ($r.Code -eq 0) "exit code $($r.Code):`n$($r.Output)"
    Expect (-not (Test-Path $DataDir)) 'the data folder is still there'
  }
}
finally {
  if ($script:Failures.Count -gt 0) { Show-State }
  # Leave the machine as we found it, whatever happened.
  Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue | ForEach-Object { Stop-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue; Unregister-ScheduledTask -TaskName 'VedhaAgent' -Confirm:$false -ErrorAction SilentlyContinue }
  Get-Process -Name 'vedha-agent' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 1
  foreach ($path in $AppDir, "$AppDir.old", $DataDir) { if (Test-Path $path) { Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue } }
}

Write-Host ''
Write-Host "Installer end-to-end: $script:Passed passed, $($script:Failures.Count) failed"
foreach ($f in $script:Failures) { Write-Host "  FAIL: $f" -ForegroundColor Red }
exit ($(if ($script:Failures.Count -eq 0) { 0 } else { 1 }))
