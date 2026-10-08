<#
  Drives the REAL, release-stamped install.ps1 (install-remote.ps1) from a test.

  The installer ends with a main block that runs it. This harness loads everything above that
  block, so each function can be exercised directly, then calls Install-VedhaAgent -VerifyOnly or
  Expand-SafeZip. Nothing else is stubbed, with one exception: on Linux/macOS, where Windows CNG
  does not exist, Test-P256Signature is replaced by a managed ECDSA check - after asserting that
  the installer's SPKI slicing (X || Y at offsets 27..90) equals what .NET's own parser extracts.
  On Windows the installer's own CNG code runs unmodified.

  Output (one line each, parsed by test_windows_installer_pwsh.py):
    RESULT: PASS
    RESULT: FAIL: <message>
    ZIP <case> REFUSED: <message> | EXTRACTED   escaped=<True|False>
#>
param(
  [Parameter(Mandatory = $true)][string]$Installer,
  [int]$Port = 0,
  [string]$Token = 'vet_local',
  [switch]$NoAllowHttp,
  [string]$ZipDir = ''
)
$text = Get-Content -Raw -LiteralPath $Installer
$cut = $text.IndexOf('$failed = $false')
if ($cut -lt 0) { Write-Host 'RESULT: FAIL: harness could not find the installer main block'; exit 2 }
$tmp = Join-Path ([IO.Path]::GetTempPath()) ('installer-' + [guid]::NewGuid().ToString('N') + '.ps1')
Set-Content -LiteralPath $tmp -Value $text.Substring(0, $cut)
if (-not $env:ProgramData) { $env:ProgramData = Join-Path ([IO.Path]::GetTempPath()) 'programdata-harness' }

$loadArgs = @{ Manager = "http://127.0.0.1:$Port"; Token = $Token; VerifyOnly = $true }
if (-not $NoAllowHttp) { $loadArgs.AllowInsecureHttp = $true }
. $tmp @loadArgs

$unix = ($PSVersionTable['Platform'] -eq 'Unix')      # the key does not exist in Windows PowerShell 5.1
if ($unix) {
  function Test-P256Signature([byte[]]$Data, [string]$SignatureB64, [string]$SpkiB64) {
    $spki = [Convert]::FromBase64String($SpkiB64)
    $ec = [System.Security.Cryptography.ECDsa]::Create()
    $read = 0
    $ec.ImportSubjectPublicKeyInfo($spki, [ref]$read)
    $q = $ec.ExportParameters($false).Q
    $xy = [BitConverter]::ToString([byte[]]($q.X + $q.Y))
    $slice = New-Object byte[] 64
    [Array]::Copy($spki, 27, $slice, 0, 64)
    if ($xy -ne [BitConverter]::ToString($slice)) { throw 'SPKI slicing offsets do not match the .NET key parser' }
    $head = (($spki[0..25] | ForEach-Object { $_.ToString('x2') }) -join '')
    if ($spki.Length -ne 91 -or $spki[26] -ne 4 -or $head -ne '3059301306072a8648ce3d020106082a8648ce3d030107034200') { throw 'SPKI prefix check failed' }
    $sig = [Convert]::FromBase64String($SignatureB64.Trim())
    if ($sig.Length -ne 64) { return $false }
    $sha = [System.Security.Cryptography.SHA256]::Create()
    return [bool]$ec.VerifyHash($sha.ComputeHash($Data), $sig)
  }
}

if ($ZipDir) {
  foreach ($zip in (Get-ChildItem -LiteralPath $ZipDir -Filter *.zip | Sort-Object Name)) {
    $dest = Join-Path ([IO.Path]::GetTempPath()) ('extract-' + [guid]::NewGuid().ToString('N'))
    try { Expand-SafeZip $zip.FullName $dest; $r = 'EXTRACTED' } catch { $r = 'REFUSED: ' + $_.Exception.Message }
    $escaped = Test-Path -LiteralPath (Join-Path (Split-Path $dest -Parent) 'evil.txt')
    Write-Host ("ZIP {0} {1}   escaped={2}" -f $zip.BaseName, $r, $escaped)
  }
  exit 0
}

try {
  Install-VedhaAgent
  Write-Host 'RESULT: PASS'
} catch {
  Write-Host ('RESULT: FAIL: ' + $_.Exception.Message)
  exit 3
}
