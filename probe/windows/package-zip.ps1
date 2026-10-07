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
  [Parameter(Mandatory = $true)][string]$Manager,
  [string]$AgentDir = '',
  [string]$OutZip  = ''
)
$ErrorActionPreference = 'Stop'

# $PSScriptRoot can be empty inside a param() default (see build-agent-exe.ps1); resolve here.
if (-not $AgentDir) { $AgentDir = Join-Path $PSScriptRoot 'dist\vedha-agent' }
if (-not $OutZip)   { $OutZip   = Join-Path $PSScriptRoot 'dist\vedha-probe-win.zip' }

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

# Bake the chosen manager URL into the staged launchers.
foreach ($f in @('run.cmd','install.ps1')) {
  $p = Join-Path $stage $f
  (Get-Content $p) -replace '__VEDHA_MANAGER_URL__', $Manager | Set-Content $p
}

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $OutZip
Remove-Item $stage -Recurse -Force

Write-Host ''
Write-Host "Packaged: $OutZip" -ForegroundColor Green
Write-Host "  Manager baked in: $Manager"
Write-Host '  Send this ZIP to the customer. They unzip and run run.cmd (test) or install.cmd (permanent).'
