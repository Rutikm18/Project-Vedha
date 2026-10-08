<#
  Assemble the customer ZIP from the built exe + the launcher scripts.
  RUN THIS ON A WINDOWS MACHINE after build-agent-exe.ps1.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File package-zip.ps1
    powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Manager https://manager.example.com

    powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Release

  -Release builds the package the manager serves: the launchers keep their placeholder because the
  one-command installer (install-remote.ps1) passes -Manager and -Token to install.ps1 itself.

  Output: probe\windows\dist\vedha-probe-win.zip
#>
[CmdletBinding(DefaultParameterSetName = 'Customer')]
param(
  # A hand-delivered ZIP must name its manager (the launchers refuse to run without one).
  [Parameter(Mandatory = $true, ParameterSetName = 'Customer')][string]$Manager,
  # The release package has no manager baked in: the one-command installer passes it at install time.
  [Parameter(Mandatory = $true, ParameterSetName = 'Release')][switch]$Release,
  [string]$AgentDir = "$PSScriptRoot\dist\vedha-agent",
  [string]$OutZip  = "$PSScriptRoot\dist\vedha-probe-win.zip"
)
$ErrorActionPreference = 'Stop'

if (-not (Test-Path (Join-Path $AgentDir 'vedha-agent.exe'))) { throw "compiled agent not found in $AgentDir  (run build-agent-exe.ps1 first)" }

$stage = Join-Path $PSScriptRoot 'dist\_stage'
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stage | Out-Null

Copy-Item $AgentDir                                  (Join-Path $stage 'vedha-agent') -Recurse
Copy-Item (Join-Path $PSScriptRoot 'run.cmd')        $stage
Copy-Item (Join-Path $PSScriptRoot 'install.ps1')    $stage
Copy-Item (Join-Path $PSScriptRoot 'install.cmd')    $stage
Copy-Item (Join-Path $PSScriptRoot 'uninstall.ps1')  $stage
Copy-Item (Join-Path $PSScriptRoot 'uninstall.cmd')  $stage
Copy-Item (Join-Path $PSScriptRoot 'README-CUSTOMER.txt') (Join-Path $stage 'README.txt')

# Bake the chosen manager URL into the staged launchers (skipped for the release package).
if ($Manager) {
  foreach ($f in @('run.cmd','install.ps1')) {
    $p = Join-Path $stage $f
    (Get-Content $p) -replace '__VEDHA_MANAGER_URL__', $Manager | Set-Content $p
  }
}

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $OutZip
Remove-Item $stage -Recurse -Force

Write-Host ''
Write-Host "Packaged: $OutZip" -ForegroundColor Green
if ($Manager) {
  Write-Host "  Manager baked in: $Manager"
  Write-Host '  Send this ZIP to the customer. They unzip and run run.cmd (test) or install.cmd (permanent).'
} else {
  Write-Host '  No manager baked in: this is the release package, installed with the one-command installer.'
}
