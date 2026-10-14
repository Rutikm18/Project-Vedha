<#
  Assemble the customer ZIP from the built agent folder + the installer scripts.
  RUN THIS ON A WINDOWS MACHINE after build-agent-exe.ps1.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Manager https://api.example.com
    powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Release

  -Manager bakes ONE manager address into the package (a ZIP you hand to a customer).
  -Release builds the package the manager itself serves (agent-release.yml): no address is baked in,
  because the one-command installer (install-remote.ps1) passes -Manager and -Token at install time.

  Output: probe\windows\dist\vedha-agent-win.zip   (and the zip's SHA-256, to send to the customer separately)

  What goes in the zip:
    vedha-agent\          the compiled agent with everything it needs (no Python or other software required)
    install.cmd / .ps1    the one-command installer
    uninstall.cmd / .ps1  removal
    run.cmd               a foreground test run (no administrator rights needed)
    README.txt            what the customer does
    ALLOWLIST.txt         what their security team should allow, with this build's hash
    SHA256SUMS.txt        a checksum of every file, checked by the installer
#>
[CmdletBinding(DefaultParameterSetName = 'Customer')]
param(
  # A hand-delivered ZIP must name its manager (the launchers refuse to run without one).
  [Parameter(Mandatory = $true, ParameterSetName = 'Customer')][string]$Manager,
  # The release package carries no manager address; it is given at install time.
  [Parameter(Mandatory = $true, ParameterSetName = 'Release')][switch]$Release,
  [string]$AgentDir = '',
  [string]$OutZip = '',
  [string]$PackageVersion = ''
)
$ErrorActionPreference = 'Stop'

# $PSScriptRoot can be empty inside a param() default (see build-agent-exe.ps1); resolve here.
if (-not $AgentDir) { $AgentDir = Join-Path $PSScriptRoot 'dist\vedha-agent' }
if (-not $OutZip)   { $OutZip   = Join-Path $PSScriptRoot 'dist\vedha-agent-win.zip' }
if (-not $PackageVersion) {
  $versionFile = Join-Path $PSScriptRoot '..\..\VERSION'
  if (Test-Path -LiteralPath $versionFile) { $PackageVersion = (Get-Content -LiteralPath $versionFile -TotalCount 1).Trim() } else { $PackageVersion = 'dev' }
}

$exe = Join-Path $AgentDir 'vedha-agent.exe'
if (-not (Test-Path -LiteralPath $exe)) { throw "compiled agent not found in $AgentDir  (run build-agent-exe.ps1 first)" }
if ($Release) {
  $managerHost = 'the Vedha manager address you were given'
} else {
  $managerHost = ([uri]$Manager).Host
  if (-not $managerHost) { throw "-Manager must be a full address such as https://api.example.com (got '$Manager')" }
}

$stage = Join-Path $PSScriptRoot 'dist\_stage'
if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stage | Out-Null

Copy-Item -LiteralPath $AgentDir -Destination (Join-Path $stage 'vedha-agent') -Recurse
foreach ($name in 'run.cmd', 'install.ps1', 'install.cmd', 'uninstall.ps1', 'uninstall.cmd') {
  Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination $stage
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'README-CUSTOMER.txt') -Destination (Join-Path $stage 'README.txt')

$exeHash = (Get-FileHash -LiteralPath (Join-Path $stage 'vedha-agent\vedha-agent.exe') -Algorithm SHA256).Hash.ToLower()
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Fill in the values this package carries. Exact text replacement, so line endings are kept.
function Set-Placeholders {
  param([string]$Path, [hashtable]$Values)
  $text = [System.IO.File]::ReadAllText($Path)
  foreach ($key in $Values.Keys) { $text = $text.Replace($key, $Values[$key]) }
  [System.IO.File]::WriteAllText($Path, $text, $utf8)
}
if ($Release) {
  # The manager placeholder stays: install.ps1 then insists on -Manager, run.cmd refuses to run unconfigured.
  Set-Placeholders (Join-Path $stage 'install.ps1') @{ '__VEDHA_PACKAGE_VERSION__' = $PackageVersion }
} else {
  Set-Placeholders (Join-Path $stage 'run.cmd')     @{ '__VEDHA_MANAGER_URL__' = $Manager }
  Set-Placeholders (Join-Path $stage 'install.ps1') @{ '__VEDHA_MANAGER_URL__' = $Manager; '__VEDHA_PACKAGE_VERSION__' = $PackageVersion }
}

$allow = [System.IO.File]::ReadAllText((Join-Path $PSScriptRoot 'ALLOWLIST.template.txt'))
$allow = $allow.Replace('{{MANAGER_HOST}}', $managerHost).Replace('{{VERSION}}', $PackageVersion).Replace('{{EXE_SHA256}}', $exeHash)
[System.IO.File]::WriteAllText((Join-Path $stage 'ALLOWLIST.txt'), $allow, $utf8)

# A checksum for every file; the installer re-checks them so damage, tampering or an
# antivirus quarantine is reported before anything is installed.
$root = (Resolve-Path -LiteralPath $stage).Path.TrimEnd('\')
$lines = Get-ChildItem -LiteralPath $stage -Recurse -File | Where-Object { $_.Name -ne 'SHA256SUMS.txt' } | Sort-Object FullName | ForEach-Object {
  $relative = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
  '{0}  {1}' -f (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower(), $relative
}
[System.IO.File]::WriteAllText((Join-Path $stage 'SHA256SUMS.txt'), (($lines -join "`n") + "`n"), $utf8)

$outDir = Split-Path -Parent $OutZip
if ($outDir -and -not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
if (Test-Path -LiteralPath $OutZip) { Remove-Item -LiteralPath $OutZip -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $OutZip
Remove-Item -LiteralPath $stage -Recurse -Force

$zipHash = (Get-FileHash -LiteralPath $OutZip -Algorithm SHA256).Hash.ToLower()
Write-Host ''
Write-Host "Packaged: $OutZip" -ForegroundColor Green
if ($Release) { Write-Host '  Manager baked in : (none - release package; given at install time)' } else { Write-Host "  Manager baked in : $Manager" }
Write-Host "  Package version  : $PackageVersion"
Write-Host "  vedha-agent.exe  : $exeHash"
Write-Host "  ZIP SHA-256      : $zipHash"
Write-Host ''
if ($Release) {
  Write-Host '  Release package: agent-release.yml signs it into the release; customers install it with the command from Fleet.'
} else {
  Write-Host '  Send the ZIP to the customer, and give them the ZIP SHA-256 and their one-time install token'
  Write-Host '  through a DIFFERENT channel (phone, chat). They then run:  install.cmd -Token vet_XXXXXXXX'
}
Set-Content -LiteralPath ($OutZip + '.sha256') -Value "$zipHash  $(Split-Path -Leaf $OutZip)"

# release.json: what the S3 publish step (hosting\publish-to-s3.sh) needs to know about this build,
# so publishing never has to guess the version or recompute anything.
$agentVersion = ''
$versionPy = Join-Path $PSScriptRoot '..\agent\version.py'
if (Test-Path -LiteralPath $versionPy) {
  $m = [regex]::Match([System.IO.File]::ReadAllText($versionPy), 'AGENT_VERSION\s*=\s*"([^"]+)"')
  if ($m.Success) { $agentVersion = $m.Groups[1].Value }
}
# NB: not $release - that is case-insensitively the same as the [switch]$Release
# parameter, so assigning an ordered dict to it throws a type-conversion error.
$releaseInfo = [ordered]@{
  schema          = 1
  version         = $agentVersion
  package_version = $PackageVersion
  manager         = $(if ($Release) { '' } else { $Manager })
  zip             = "$agentVersion/vedha-agent-win.zip"
  sha256          = $zipHash
  exe_sha256      = $exeHash
  size            = (Get-Item -LiteralPath $OutZip).Length
  built_at        = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
}
$releasePath = $OutZip -replace '\.zip$', '.release.json'
[System.IO.File]::WriteAllText($releasePath, ($releaseInfo | ConvertTo-Json -Compress), $utf8)
Write-Host "  Release info     : $releasePath  (agent $agentVersion)"
