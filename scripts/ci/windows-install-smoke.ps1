<#
  Installs the real Windows package with its packaged install.ps1 on a CI runner, checks what
  the installer promises, then uninstalls:

    * the "VedhaAgent" Scheduled Task exists;
    * C:\ProgramData\vedha-agent is restricted to SYSTEM and Administrators (inheritance removed);
    * the install token sits in that folder, not in the service wrapper;
    * uninstall -Purge removes the task and the folder.

  The manager address is unreachable on purpose: the agent cannot enrol, so the token file must
  still be there (it is only deleted after a successful enrolment) and the installer must say so.
  Throws on any failure.
#>
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Package)
$ErrorActionPreference = 'Stop'

$work = Join-Path ([IO.Path]::GetTempPath()) ('install-smoke-' + [guid]::NewGuid().ToString('N'))
Expand-Archive -Path $Package -DestinationPath $work
foreach ($needed in 'install.ps1', 'uninstall.ps1', 'vedha-agent\vedha-agent.exe') {
  if (-not (Test-Path (Join-Path $work $needed))) { throw "package lacks $needed" }
}

$dir = Join-Path $env:ProgramData 'vedha-agent'
$global:LASTEXITCODE = 0
& (Join-Path $work 'install.ps1') -Manager 'https://manager.invalid' -Token 'vet_ci_smoke_token' -EnrolWaitSeconds 6
if ($LASTEXITCODE -ne 0) { throw "install.ps1 exited $LASTEXITCODE" }

if (-not (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue)) { throw 'the VedhaAgent task was not registered' }

$acl = Get-Acl $dir
if (-not $acl.AreAccessRulesProtected) { throw 'the install folder still inherits permissions' }
$principals = @($acl.Access | ForEach-Object { $_.IdentityReference.Value } | Sort-Object -Unique)
$unexpected = @($principals | Where-Object { @('NT AUTHORITY\SYSTEM', 'BUILTIN\Administrators') -notcontains $_ })
if ($unexpected.Count) { throw "the install folder grants access to: $($unexpected -join ', ')" }

$tokenFile = Join-Path $dir 'enroll.token'
if (-not (Test-Path $tokenFile)) { throw 'the token file is gone although the agent never enrolled' }
if ((Get-Content $tokenFile -Raw).Trim() -ne 'vet_ci_smoke_token') { throw 'the token file does not hold the token' }
$wrapper = Get-Content (Join-Path $dir 'agent-service.cmd') -Raw
if ($wrapper -match 'vet_') { throw 'the install token leaked into the service wrapper' }
if ($wrapper -notmatch 'set /p PROBE_ENROLL_TOKEN=<') { throw 'the service wrapper does not read the token from the locked file' }

& (Join-Path $work 'uninstall.ps1') -Purge
if (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue) { throw 'uninstall left the task behind' }
if (Test-Path $dir) { throw 'uninstall -Purge left the install folder behind' }
Remove-Item $work -Recurse -Force -ErrorAction SilentlyContinue
Write-Host 'ok: install, token handling, folder permissions and uninstall behave as promised'
