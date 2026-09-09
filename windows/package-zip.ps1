<#
  Assemble the customer ZIP from the built exe + the launcher scripts.
  RUN THIS ON A WINDOWS MACHINE after build-agent-exe.ps1.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File package-zip.ps1
    powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Manager https://manager.example.com

  Output: probe\windows\dist\vedha-probe-win.zip
#>
[CmdletBinding()]
param(
  [string]$Manager = 'http://13.127.147.205:18080',
  [string]$ExePath = "$PSScriptRoot\dist\vedha-agent.exe",
  [string]$OutZip  = "$PSScriptRoot\dist\vedha-probe-win.zip"
)
$ErrorActionPreference = 'Stop'

if (-not (Test-Path $ExePath)) { throw "exe not found: $ExePath  (run build-agent-exe.ps1 first)" }

$stage = Join-Path $PSScriptRoot 'dist\_stage'
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stage | Out-Null

Copy-Item $ExePath                                   (Join-Path $stage 'vedha-agent.exe')
Copy-Item (Join-Path $PSScriptRoot 'run.cmd')        $stage
Copy-Item (Join-Path $PSScriptRoot 'install.ps1')    $stage
Copy-Item (Join-Path $PSScriptRoot 'install.cmd')    $stage
Copy-Item (Join-Path $PSScriptRoot 'uninstall.ps1')  $stage
Copy-Item (Join-Path $PSScriptRoot 'uninstall.cmd')  $stage
Copy-Item (Join-Path $PSScriptRoot 'README-CUSTOMER.txt') (Join-Path $stage 'README.txt')

# Bake the chosen manager URL into the staged launchers.
foreach ($f in @('run.cmd','install.ps1')) {
  $p = Join-Path $stage $f
  (Get-Content $p) -replace 'http://13\.127\.147\.205:18080', $Manager | Set-Content $p
}

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $OutZip
Remove-Item $stage -Recurse -Force

Write-Host ''
Write-Host "Packaged: $OutZip" -ForegroundColor Green
Write-Host "  Manager baked in: $Manager"
Write-Host '  Send this ZIP to the customer. They unzip and run run.cmd (test) or install.cmd (permanent).'
