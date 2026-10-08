<#
  Runs a release's REAL install.ps1 the way a customer does - the scriptblock form, in Windows
  PowerShell 5.1 (or pwsh) - against the stub manager (agent_stub_manager.py) in -VerifyOnly mode,
  and checks the outcome:

    -ExpectOutput <text>    the install must verify, exit 0 and print <text>
    -ExpectFailure <text>   the install must be REFUSED (non-zero exit) and say <text>

  -Tamper makes the stub lie (manifest, signature, package, truncated, oversize, redirect);
  -ClientToken makes the installer present a token the stub does not accept.
  Throws on any unmet expectation, so a calling CI step fails.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$ReleaseDir,
  [string]$Tamper = 'none',
  [string]$Token = 'vet_ci_token',
  [string]$ClientToken = '',
  [ValidateSet('powershell', 'pwsh')][string]$Shell = 'powershell',
  [string]$ExpectOutput = '',
  [string]$ExpectFailure = ''
)
$ErrorActionPreference = 'Stop'
if (-not $ExpectOutput -and -not $ExpectFailure) { throw 'give -ExpectOutput (must succeed) or -ExpectFailure (must be refused)' }
if (-not $ClientToken) { $ClientToken = $Token }
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$release = (Resolve-Path $ReleaseDir).Path

$listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
$listener.Start()
$port = $listener.LocalEndpoint.Port
$listener.Stop()

$stubArgs = @((Join-Path $repo 'scripts/ci/agent_stub_manager.py'), '--release', $release, '--token', $Token, '--port', "$port", '--tamper', $Tamper)
$hide = @{}
if ($PSVersionTable['Platform'] -ne 'Unix') { $hide.WindowStyle = 'Hidden' }      # not available on Linux/macOS
$stub = Start-Process -FilePath python -ArgumentList $stubArgs -PassThru @hide
try {
  $base = "http://127.0.0.1:$port"
  $up = $false
  for ($i = 0; $i -lt 30 -and -not $up; $i++) {
    try { Invoke-WebRequest -Uri "$base/agent/manifest.json" -UseBasicParsing -TimeoutSec 2 | Out-Null; $up = $true }
    catch { Start-Sleep -Milliseconds 500 }
  }
  if (-not $up) { throw 'the stub manager did not start' }

  $command = "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " +
             "& ([scriptblock]::Create((irm '$base/agent/install.ps1'))) -Manager '$base' -Token '$ClientToken' -AllowInsecureHttp -VerifyOnly"
  $output = (& $Shell -NoProfile -ExecutionPolicy Bypass -Command $command 2>&1 | Out-String)
  $code = $LASTEXITCODE
  Write-Host $output

  if ($ExpectOutput) {
    if ($code -ne 0) { throw "[$Shell] the installer failed (exit $code) but should have verified this release" }
    if (-not $output.Contains($ExpectOutput)) { throw "[$Shell] the installer succeeded but its output lacks '$ExpectOutput'" }
  } else {
    if ($code -eq 0) { throw "[$Shell] the installer ACCEPTED a release it must refuse (tamper=$Tamper, token=$ClientToken)" }
    if (-not $output.Contains($ExpectFailure)) { throw "[$Shell] refused, but not for the expected reason '$ExpectFailure'" }
  }
  Write-Host "ok: shell=$Shell tamper=$Tamper"
}
finally {
  if ($stub -and -not $stub.HasExited) { Stop-Process -Id $stub.Id -Force -ErrorAction SilentlyContinue }
}
