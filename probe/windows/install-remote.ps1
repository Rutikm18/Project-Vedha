<#
  Vedha Agent - one-command Windows installer.

  Served by your Vedha manager at  <manager>/agent/install.ps1  and run from an
  ELEVATED PowerShell (Fleet -> Add agent prints the exact command, token filled in):

    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    & ([scriptblock]::Create((irm 'https://manager.example.com/agent/install.ps1'))) -Manager 'https://manager.example.com' -Token 'vet_...'

  or double-click / run install.cmd (it asks for administrator rights itself).

  What it does, in order - and it stops at the first thing that does not check out:
    1. Fetches the release manifest and its ECDSA P-256 signature from the manager and
       verifies the signature with the release public key baked into THIS script.
    2. Downloads the Windows package (the install token authorises the download) and
       checks its size and SHA-256 against the signed manifest.
    3. If the release pins an Authenticode certificate, requires vedha-agent.exe to carry a
       valid signature from exactly that certificate.
    4. Unpacks it (refusing any path that would escape the target folder) and runs the
       packaged install.ps1, which registers the "VedhaAgent" Scheduled Task (SYSTEM).

  Add -VerifyOnly to do steps 1-3 and the unpack, then stop: nothing is installed and no
  administrator rights are needed. Useful to audit a release before rolling it out.

  Trust model: the script is fetched over TLS from the manager, so TLS to the manager is the
  root of trust for the script itself. The signature then protects everything the script
  downloads: a tampered or swapped package, a stale manifest, or a mirror that was changed after
  the release was signed. It does not protect against a manager that serves you a different
  script. Verify out-of-band with the release key id shown in Fleet if that matters to you.

  Needs PowerShell 5.1 or later and a 64-bit Windows. ASCII only, on purpose: Windows PowerShell
  5.1 reads a BOM-less file in the ANSI code page.
#>
[CmdletBinding()]
param(
  [string]$Manager = '',
  [string]$Token   = '',
  [string]$Scope   = '',          # CIDR list; empty = auto-detect this host's /24
  [switch]$AllowInsecureHttp,     # lab use: allow an http:// manager (the token is sent in clear text)
  [switch]$VerifyOnly,            # download and verify everything, install nothing (no administrator needed)
  [switch]$PauseAtEnd             # keep the window open (set by install.cmd after it elevates)
)
Set-StrictMode -Version 2
$ErrorActionPreference = 'Stop'

# Filled in by scripts/agent_release.py when the release is assembled. Each marker must
# stay on a line of its own, starting in column 1; the build refuses a script without them.
$script:VedhaReleaseP256Spki = ''
$script:VedhaReleaseVersion = ''

$script:MaxManifestBytes = 1MB
$script:MaxUnpackedBytes = 2GB
$script:MaxEntries = 20000

function Write-Step([string]$Message) { Write-Host ('[vedha] ' + $Message) }

# --- input ----------------------------------------------------------------------------------

function Get-CleanManager {
  if (-not $Manager) { throw 'Missing -Manager: the address of your Vedha manager, for example https://manager.example.com' }
  $m = $Manager.Trim().TrimEnd('/')
  if ($m -notmatch '^(?<scheme>https?)://[A-Za-z0-9.\-]+(:[0-9]{1,5})?$') {
    throw "Manager must look like https://host or https://host:port (got '$Manager')."
  }
  if ($Matches['scheme'] -eq 'http' -and -not $AllowInsecureHttp) {
    throw 'Refusing an http:// manager: the install token would cross the network in clear text. Use the https:// address (or pass -AllowInsecureHttp for a lab).'
  }
  return $m
}

function Assert-CleanToken {
  if (-not $Token) {
    throw 'An install token is required to download the agent. In Fleet -> Add agent, create one and copy the command it prints.'
  }
  if ($Token -notmatch '^vet_[A-Za-z0-9_\-]+$') { throw 'The install token is malformed (expected vet_...). Copy it again from Fleet -> Add agent.' }
}

function Assert-CleanScope {
  if ($Scope -and $Scope -notmatch '^[0-9A-Fa-f:.,/]+$') { throw "-Scope must be a CIDR list such as 10.0.0.0/24 (got '$Scope')." }
}

function Assert-Environment {
  $principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
  if (-not $VerifyOnly -and -not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Administrator rights are required (the agent is installed as a service). Open PowerShell with "Run as administrator" and run the command again, or use install.cmd.'
  }
  if (-not [Environment]::Is64BitOperatingSystem) { throw 'A 64-bit version of Windows is required.' }
  if ($PSVersionTable.PSVersion.Major -lt 5) { throw 'Windows PowerShell 5.1 or later is required.' }
  if (-not $script:VedhaReleaseP256Spki -or -not $script:VedhaReleaseVersion) {
    throw 'This installer was not stamped by a release build, so it cannot verify anything. Download it from your manager (/agent/install.ps1).'
  }
}

# --- HTTP -----------------------------------------------------------------------------------

function Get-ErrorDetail($Response) {
  # The manager answers 4xx with {"detail": "..."}; surface that, never more than 2 KB of it.
  try {
    $reader = New-Object System.IO.StreamReader($Response.GetResponseStream())
    try { $text = $reader.ReadToEnd() } finally { $reader.Dispose() }
    if ($text.Length -gt 2048) { $text = $text.Substring(0, 2048) }
    try { $obj = $text | ConvertFrom-Json; if ($obj.PSObject.Properties['detail']) { return [string]$obj.detail } } catch { }
    return $text.Trim()
  } catch { return '' }
}

function Open-Response([string]$Url, [string]$Bearer) {
  # Redirects are NOT followed: this request may carry the install token, and a download
  # that is bounced somewhere else should fail loudly rather than leak it.
  $req = [System.Net.HttpWebRequest]::Create($Url)
  $req.Method = 'GET'
  $req.AllowAutoRedirect = $false
  $req.UserAgent = 'vedha-installer/' + $script:VedhaReleaseVersion
  $req.Timeout = 60000
  $req.ReadWriteTimeout = 120000
  $req.Proxy = [System.Net.WebRequest]::GetSystemWebProxy()
  $req.Proxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials
  if ($Bearer) { $req.Headers.Add('Authorization', 'Bearer ' + $Bearer) }
  try {
    $resp = $req.GetResponse()
  } catch [System.Net.WebException] {
    $resp = $_.Exception.Response
    if ($null -eq $resp) { throw ('Cannot reach ' + $Url + ' : ' + $_.Exception.Message) }
  }
  $code = [int]$resp.StatusCode
  if ($code -eq 200) { return $resp }
  $detail = Get-ErrorDetail $resp
  $location = $resp.Headers['Location']
  $resp.Close()
  if ($code -ge 300 -and $code -lt 400) {
    throw ("The manager redirected $Url to '$location'. Redirects are refused; use the manager's canonical https:// address.")
  }
  if ($code -eq 401) { throw ('The install token was refused (expired, revoked or already used). Create a new one in Fleet -> Add agent. ' + $detail) }
  if ($code -eq 429) { throw 'Too many downloads from this address; wait a minute and run the command again.' }
  if ($code -eq 404 -or $code -eq 503) { throw ("The manager has no Windows agent release to offer ($code). $detail") }
  throw ("Unexpected HTTP $code from $Url. $detail")
}

function Read-Bytes([string]$Url, [long]$MaxBytes) {
  $resp = Open-Response $Url ''
  try {
    $in = $resp.GetResponseStream()
    $ms = New-Object System.IO.MemoryStream
    $buf = New-Object byte[] 8192
    while (($n = $in.Read($buf, 0, $buf.Length)) -gt 0) {
      if ($ms.Length + $n -gt $MaxBytes) { throw ("$Url is larger than $MaxBytes bytes; refusing it.") }
      $ms.Write($buf, 0, $n)
    }
    return , $ms.ToArray()
  } finally { $resp.Close() }
}

function Save-File([string]$Url, [string]$Path, [string]$Bearer, [long]$ExpectedSize) {
  $resp = Open-Response $Url $Bearer
  $total = [long]0
  try {
    $in = $resp.GetResponseStream()
    $out = [System.IO.File]::Open($Path, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    try {
      $buf = New-Object byte[] 262144
      while (($n = $in.Read($buf, 0, $buf.Length)) -gt 0) {
        $total += $n
        if ($total -gt $ExpectedSize) { throw 'The download is larger than the signed manifest says; refusing it.' }
        $out.Write($buf, 0, $n)
      }
    } finally { $out.Dispose() }
  } finally { $resp.Close() }
  if ($total -ne $ExpectedSize) { throw "The download is $total bytes but the signed manifest says $ExpectedSize; refusing it." }
}

# --- verification ---------------------------------------------------------------------------

function Get-Sha256Hex([string]$Path) {
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $fs = [System.IO.File]::OpenRead($Path)
  try { $hash = $sha.ComputeHash($fs) } finally { $fs.Dispose(); $sha.Dispose() }
  return ([BitConverter]::ToString($hash) -replace '-', '').ToLowerInvariant()
}

function Test-P256Signature([byte[]]$Data, [string]$SignatureB64, [string]$SpkiB64) {
  # The release key is a DER SubjectPublicKeyInfo (91 bytes: a fixed 26-byte prefix, 0x04, X, Y).
  # .NET Framework cannot read that directly, so rebuild the CNG ECCPUBLIC blob
  # (magic 'ECS1', key length 32, X, Y) and verify through ECDsaCng. The signature is the
  # 64-byte IEEE P1363 form (r || s), which is what ECDsaCng expects.
  $spki = [Convert]::FromBase64String($SpkiB64)
  $prefix = '3059301306072a8648ce3d020106082a8648ce3d030107034200'
  $head = (($spki[0..25] | ForEach-Object { $_.ToString('x2') }) -join '')
  if ($spki.Length -ne 91 -or $head -ne $prefix -or $spki[26] -ne 4) {
    throw 'The release key embedded in this installer is not an uncompressed P-256 public key.'
  }
  $sig = [Convert]::FromBase64String($SignatureB64.Trim())
  if ($sig.Length -ne 64) { return $false }
  $blob = New-Object byte[] 72
  [BitConverter]::GetBytes([uint32]0x31534345).CopyTo($blob, 0)
  [BitConverter]::GetBytes([uint32]32).CopyTo($blob, 4)
  [Array]::Copy($spki, 27, $blob, 8, 64)
  $key = [System.Security.Cryptography.CngKey]::Import($blob, [System.Security.Cryptography.CngKeyBlobFormat]::EccPublicBlob)
  try {
    $ecdsa = [System.Security.Cryptography.ECDsaCng]::new($key)
    try {
      $sha = [System.Security.Cryptography.SHA256]::Create()
      try { $digest = $sha.ComputeHash($Data) } finally { $sha.Dispose() }
      return [bool]$ecdsa.VerifyHash($digest, $sig)
    } finally { $ecdsa.Dispose() }
  } finally { $key.Dispose() }
}

function Get-Prop($Object, [string]$Name) {
  $p = $Object.PSObject.Properties[$Name]
  if ($null -eq $p) { return $null }
  return $p.Value
}

function Get-VerifiedPackage([string]$ManagerUrl) {
  Write-Step 'fetching the signed release manifest'
  $manifestBytes = Read-Bytes ($ManagerUrl + '/agent/manifest.json') $script:MaxManifestBytes
  $sigBytes = Read-Bytes ($ManagerUrl + '/agent/manifest.json.p256.sig') 4096
  $sigText = [System.Text.Encoding]::ASCII.GetString($sigBytes)
  if (-not (Test-P256Signature $manifestBytes $sigText $script:VedhaReleaseP256Spki)) {
    throw 'The release manifest signature does not verify against the key in this installer. Nothing was downloaded or installed.'
  }
  Write-Step 'manifest signature OK'

  $manifest = [System.Text.Encoding]::UTF8.GetString($manifestBytes) | ConvertFrom-Json
  if ([int](Get-Prop $manifest 'schema') -lt 2) { throw 'This release has no Windows package (manifest schema 1).' }
  if ([string](Get-Prop $manifest 'version') -ne $script:VedhaReleaseVersion) {
    throw ("The manager now serves release '" + (Get-Prop $manifest 'version') + "' but this installer belongs to '" + $script:VedhaReleaseVersion + "'. Run the command again.")
  }
  $pkg = @(@(Get-Prop $manifest 'packages') | Where-Object { (Get-Prop $_ 'os') -eq 'windows' -and (Get-Prop $_ 'cpu') -eq 'amd64' })
  if ($pkg.Count -ne 1) { throw 'The signed manifest does not list exactly one Windows amd64 package.' }
  $entry = $pkg[0]
  $sha = ([string](Get-Prop $entry 'sha256')).ToLowerInvariant()
  $size = [long](Get-Prop $entry 'size')
  if ($sha -notmatch '^[0-9a-f]{64}$' -or $size -le 0 -or $size -gt $script:MaxUnpackedBytes) { throw 'The signed manifest entry for the Windows package is malformed.' }
  $thumb = Get-Prop $entry 'authenticode_thumbprint'
  if ($thumb -and ([string]$thumb) -notmatch '^[0-9A-Fa-f]{40}$') { throw 'The signed manifest carries a malformed Authenticode thumbprint.' }
  return [pscustomobject]@{
    Version = [string](Get-Prop $manifest 'version')
    Sha256 = $sha
    Size = $size
    Thumbprint = $(if ($thumb) { ([string]$thumb).ToUpperInvariant() } else { '' })
    ManifestBytes = $manifestBytes
    SignatureText = $sigText
  }
}

function Assert-Authenticode([string]$ExePath, [string]$Thumbprint) {
  $sig = Get-AuthenticodeSignature -FilePath $ExePath
  if ($sig.Status -ne 'Valid') {
    throw ("vedha-agent.exe is meant to be Authenticode-signed but its signature is '" + $sig.Status + "'. " + $sig.StatusMessage)
  }
  $actual = ([string]$sig.SignerCertificate.Thumbprint).ToUpperInvariant()
  if ($actual -ne $Thumbprint) {
    throw ("vedha-agent.exe is signed by certificate $actual, not the one this release pins ($Thumbprint).")
  }
}

# --- files ----------------------------------------------------------------------------------

function Protect-Directory([string]$Path) {
  # SYSTEM and Administrators only: the agent's identity key and enrolment token live here.
  # Well-known SIDs, so this works on any display language.
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
  & icacls.exe $Path /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Could not restrict permissions on $Path." }
}

function Expand-SafeZip([string]$ZipPath, [string]$Destination) {
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  New-Item -ItemType Directory -Force -Path $Destination | Out-Null
  $root = [System.IO.Path]::GetFullPath($Destination).TrimEnd('\') + '\'
  $zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
  try {
    if ($zip.Entries.Count -gt $script:MaxEntries) { throw 'The package holds an unreasonable number of files; refusing it.' }
    $unpacked = [long]0
    foreach ($entry in $zip.Entries) {
      $name = $entry.FullName.Replace('\', '/')
      # ':' is never legal in a Windows file name except as an NTFS alternate data stream.
      if ($name.StartsWith('/') -or $name.Contains(':') -or $name -match '(^|/)\.\.(/|$)' -or $name.IndexOf([char]0) -ge 0) {
        throw ("The package contains an unsafe path: '" + $entry.FullName + "'.")
      }
      $target = [System.IO.Path]::GetFullPath((Join-Path $root $name.Replace('/', '\')))
      if (-not $target.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw ("The package contains a path outside the target folder: '" + $entry.FullName + "'.")
      }
      if ($name.EndsWith('/')) { New-Item -ItemType Directory -Force -Path $target | Out-Null; continue }
      $unpacked += $entry.Length
      if ($unpacked -gt $script:MaxUnpackedBytes) { throw 'The package unpacks to an unreasonable size; refusing it.' }
      New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
      [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $false)
    }
  } finally { $zip.Dispose() }
}

# --- main -----------------------------------------------------------------------------------

function Install-VedhaAgent {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $managerUrl = Get-CleanManager
  Assert-CleanToken
  Assert-CleanScope
  Assert-Environment

  Write-Step ("installing Vedha agent release " + $script:VedhaReleaseVersion + " from " + $managerUrl)
  $release = Get-VerifiedPackage $managerUrl

  $root = Join-Path $env:ProgramData 'vedha-agent'
  if ($VerifyOnly) {
    $stage = Join-Path ([System.IO.Path]::GetTempPath()) ('vedha-verify-' + [guid]::NewGuid().ToString('N'))
  } else {
    Protect-Directory $root
    $stage = Join-Path $root ('staging\' + [guid]::NewGuid().ToString('N'))
  }
  New-Item -ItemType Directory -Force -Path $stage | Out-Null
  try {
    $zipPath = Join-Path $stage 'package.zip'
    Write-Step ('downloading the Windows package (' + [math]::Round($release.Size / 1MB, 1) + ' MB)')
    Save-File ($managerUrl + '/agent/package/windows') $zipPath $Token $release.Size
    $actual = Get-Sha256Hex $zipPath
    if ($actual -ne $release.Sha256) {
      throw "The package SHA-256 ($actual) does not match the signed manifest ($($release.Sha256)). Nothing was installed."
    }
    Write-Step 'package SHA-256 matches the signed manifest'

    $unpacked = Join-Path $stage 'unpacked'
    Expand-SafeZip $zipPath $unpacked
    $exe = Join-Path $unpacked 'vedha-agent\vedha-agent.exe'
    $inner = Join-Path $unpacked 'install.ps1'
    if (-not (Test-Path -LiteralPath $exe) -or -not (Test-Path -LiteralPath $inner)) {
      throw 'The package is incomplete (vedha-agent.exe or install.ps1 missing). If security software quarantined a file, allow it and run the command again.'
    }
    if ($release.Thumbprint) {
      Assert-Authenticode $exe $release.Thumbprint
      Write-Step ('Authenticode signature OK (certificate ' + $release.Thumbprint + ')')
    } else {
      Write-Step 'note: this release is not Authenticode-signed; it is protected by TLS, the SHA-256 above and the signed manifest'
    }

    if ($VerifyOnly) {
      Write-Step 'VERIFY-ONLY OK: signature, SHA-256 and package layout verified; nothing was installed'
      return
    }

    # Keep the verified manifest for later audit; none of it is secret.
    $relDir = Join-Path $root 'release'
    New-Item -ItemType Directory -Force -Path $relDir | Out-Null
    [System.IO.File]::WriteAllBytes((Join-Path $relDir 'manifest.json'), $release.ManifestBytes)
    [System.IO.File]::WriteAllText((Join-Path $relDir 'manifest.json.p256.sig'), $release.SignatureText, [System.Text.Encoding]::ASCII)

    $global:LASTEXITCODE = 0
    try {
      & $inner -Manager $managerUrl -Scope $Scope -Token $Token
    } catch [System.Management.Automation.PSSecurityException] {
      throw ('PowerShell policy blocked the packaged installer (' + $_.Exception.Message + '). Run the command exactly as Fleet shows it: it starts PowerShell with -ExecutionPolicy Bypass for this one process, which is all that is needed.')
    }
    if ($LASTEXITCODE -ne 0) { throw "The packaged installer failed (exit code $LASTEXITCODE)." }
  } finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
  }
}

$failed = $false
try {
  Install-VedhaAgent
} catch {
  $failed = $true
  Write-Host ''
  Write-Host ('[vedha] INSTALL FAILED: ' + $_.Exception.Message) -ForegroundColor Red
}
if ($PauseAtEnd) { Read-Host 'Press Enter to close this window' | Out-Null }
if ($failed) { exit 1 }
