<#
  Vedha Agent - one-command Windows installer.

  Served by your Vedha manager at  <manager>/agent/install.ps1  and run from an
  ELEVATED PowerShell (Fleet -> Add agent prints the exact command, token filled in):

    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    & ([scriptblock]::Create((irm 'https://manager.example.com/agent/install.ps1'))) -Manager 'https://manager.example.com' -Token 'vet_...'

  or double-click / run install.cmd (it asks for administrator rights itself).

  The same command works from ANY window, Command Prompt or an ordinary PowerShell: when this
  script is not elevated it asks Windows for administrator permission (the UAC prompt) and
  continues in a new Administrator window. Already elevated (an RMM tool, an Administrator
  PowerShell) it simply installs.

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

  The release key is PINNED the first time: after a successful install it is stored in
  ProgramData\vedha-agent\release\trust.json (administrators only). From then on this installer
  refuses to run if it carries a different key, or an older release than the last one installed, and
  the agent's automatic update checks the installer it downloads against that stored key before it
  runs it. Changing the key on purpose needs a person: run this script by hand, from an
  Administrator PowerShell, with -ReplaceReleaseKey.

  Trust model: the script is fetched over TLS from the manager, so TLS to the manager is the
  root of trust for the script itself the FIRST time; after that the pinned key is. The signature then protects everything the script
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
  [switch]$AllowInsecureHttp,     # testing only: lets -VerifyOnly talk to a local http:// test server
  [switch]$VerifyOnly,            # download and verify everything, install nothing (no administrator needed)
  [switch]$Tokenless,             # internal: the Administrator copy of an install that was started without a token
  [switch]$ReplaceReleaseKey,     # by hand only: accept a release key different from the one this computer pinned
  [switch]$PauseAtEnd,            # keep the window open (set by install.cmd after it elevates)
  [switch]$Elevated               # internal: set on the copy this script starts with administrator rights
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
  if ($Matches['scheme'] -eq 'http') {
    if (-not $VerifyOnly) {
      throw 'The Windows agent needs an https:// manager address: the install token and everything the agent sends must be encrypted.'
    }
    if (-not $AllowInsecureHttp) {
      throw 'Refusing an http:// manager: the install token would cross the network in clear text. (-AllowInsecureHttp exists only so -VerifyOnly can talk to a local test server.)'
    }
  }
  return $m
}

function Assert-CleanToken {
  # No token is allowed: it means an APPROVAL install. The machine installs, connects, shows a pairing
  # code, and a person approves it in Fleet; the manager then hands the agent its credentials by itself.
  # (The manager must allow the tokenless download; see Open-Response for what is said if it does not.)
  if (-not $Token) {
    if ($Elevated -and -not $Tokenless) {
      throw 'The install token did not reach the Administrator window (this happens when a different account supplied the administrator password). Open PowerShell with "Run as administrator" and run the command there.'
    }
    return
  }
  if ($Token -notmatch '^vet_[A-Za-z0-9_\-]{8,}$') { throw 'The install token is malformed (expected vet_...). Copy it again from Fleet -> Add agent.' }
}

function Assert-CleanScope {
  if ($Scope -and $Scope -notmatch '^[0-9A-Fa-f:.,/]+$') { throw "-Scope must be a CIDR list such as 10.0.0.0/24 (got '$Scope')." }
}

function Test-VedhaAdmin {
  $principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
  return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-VedhaElevationCommand {
  # The command the elevated copy runs: this same one-command installer, fetched again from the
  # manager (this copy came through a pipe, so there is no file to start). The TOKEN is not in it:
  # it travels in the environment (VEDHA_INSTALL_TOKEN), so it never appears on a command line that
  # other users of the machine can list. The manager and scope were already checked against strict
  # patterns, so nothing here can break out of its single quotes.
  param([string]$ManagerUrl, [string]$InstallScope, [switch]$NoToken)
  $c = "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " +
       "& ([scriptblock]::Create((irm '" + $ManagerUrl + "/agent/install.ps1'))) -Manager '" + $ManagerUrl + "'"
  if ($NoToken) { $c += ' -Tokenless' } else { $c += ' -Token $env:VEDHA_INSTALL_TOKEN' }
  if ($InstallScope) { $c += " -Scope '" + $InstallScope + "'" }
  return $c + ' -PauseAtEnd -Elevated'
}

function Enter-VedhaElevation {
  # Not an administrator: hand the install to an elevated copy (Windows shows its permission prompt)
  # and wait for it. Returns $true when it did, with the copy's exit code in $script:ElevatedExit.
  param([string]$ManagerUrl)
  if ($VerifyOnly -or (Test-VedhaAdmin)) { return $false }
  if ($Elevated) {
    throw 'Administrator rights were not granted, so nothing was installed. Run the command again and choose Yes when Windows asks for permission, or open PowerShell with "Run as administrator".'
  }
  Write-Step 'administrator rights are needed: Windows will ask for your permission, then the install continues in a new window'
  $command = Get-VedhaElevationCommand -ManagerUrl $ManagerUrl -InstallScope $Scope -NoToken:(-not $Token)
  $powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
  if ($Token) { $env:VEDHA_INSTALL_TOKEN = $Token }
  try {
    $child = Start-Process -FilePath $powershell -Verb RunAs -Wait -PassThru `
      -ArgumentList ('-NoProfile -ExecutionPolicy Bypass -Command "' + $command + '"')
  } catch {
    throw ('Administrator permission was not given (' + $_.Exception.Message + '). Nothing was installed. Run the command again and choose Yes when Windows asks, or open PowerShell with "Run as administrator".')
  } finally {
    Remove-Item Env:\VEDHA_INSTALL_TOKEN -ErrorAction SilentlyContinue
  }
  $script:ElevatedExit = [int]$child.ExitCode
  if ($script:ElevatedExit -eq 0 -and -not $Token) { Write-Step 'the installer finished in the Administrator window: if it showed a pairing code, approve it in Fleet (Pending requests); the agent connects by itself once you do' }
  elseif ($script:ElevatedExit -eq 0) { Write-Step 'the installer finished in the Administrator window: the agent is installed and connected' }
  elseif ($script:ElevatedExit -eq 3) { Write-Step 'the agent is installed but has not connected yet; the Administrator window shows what to check' }
  else { throw ('the installer failed in the Administrator window (exit code ' + $script:ElevatedExit + '); that window says why') }
  return $true
}

# --- pinned release key ----------------------------------------------------------------------

function Get-VedhaTrustPath { return (Join-Path (Join-Path (Join-Path $env:ProgramData 'vedha-agent') 'release') 'trust.json') }

function Get-VedhaKeyId([string]$SpkiB64) {
  # The first 16 hex characters of the SHA-256 of the DER key: the id Fleet and the release tool show.
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try { $hash = $sha.ComputeHash([Convert]::FromBase64String($SpkiB64)) } finally { $sha.Dispose() }
  return (([BitConverter]::ToString($hash) -replace '-', '').ToLowerInvariant()).Substring(0, 16)
}

function ConvertTo-VedhaReleaseVersion([string]$Text) {
  # '1.0.403' -> [version]; $null for anything that is not plainly numeric (never guessed).
  if ($Text -match '^(\d+(\.\d+){1,3})') { return [version]$Matches[1] }
  return $null
}

function Read-VedhaTrust {
  # $null when nothing is pinned yet. A file that exists but cannot be read is an error, not "nothing":
  # silently ignoring it would let damage switch the protection off.
  $path = Get-VedhaTrustPath
  if (-not (Test-Path -LiteralPath $path)) { return $null }
  try {
    $trust = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
    if (-not $trust.p256_spki) { throw 'no key in it' }
    return $trust
  } catch {
    throw ("The file that pins this computer's release key ($path) cannot be read (" + $_.Exception.Message + '). Nothing was changed. Restore it from a backup, or if you are sure, delete it and run the install again to pin the key afresh.')
  }
}

function Assert-VedhaTrust {
  # Refuse a release key or an older release than the one this computer already trusts.
  param($Trust, [string]$Spki, [string]$Version, [switch]$Replace)
  if ($null -eq $Trust) { return }
  if ([string]$Trust.p256_spki -ne $Spki) {
    $have = Get-VedhaKeyId ([string]$Trust.p256_spki)
    $got = Get-VedhaKeyId $Spki
    if (-not $Replace) {
      throw ("This computer trusts Vedha release key $have, but this installer carries key $got. Nothing was changed. " +
             'If you rotated the release key on purpose, confirm the new key id ' + $got + ' with whoever runs your Vedha manager, then run this installer by hand from an Administrator PowerShell with -ReplaceReleaseKey. ' +
             'If you did not, the manager may have been tampered with: do not install.')
    }
    Write-Step ("replacing the pinned release key $have with $got, because -ReplaceReleaseKey was given")
  }
  $was = ConvertTo-VedhaReleaseVersion ([string]$Trust.release_version)
  $now = ConvertTo-VedhaReleaseVersion $Version
  if ($null -ne $was -and $null -ne $now -and $now -lt $was) {
    throw ("This installer belongs to release $Version, but release $($Trust.release_version) was already installed here. Going back to an older release is refused (a stale or replayed release). Nothing was changed.")
  }
}

function Write-VedhaTrust {
  param([string]$Spki, [string]$Version, [string]$ManagerUrl)
  $path = Get-VedhaTrustPath
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $path) | Out-Null
  $record = [ordered]@{
    schema = 1; p256_spki = $Spki; key_id = (Get-VedhaKeyId $Spki); release_version = $Version
    manager = $ManagerUrl; updated_at = (Get-Date).ToUniversalTime().ToString('o')
  }
  $tmp = $path + '.new'
  [System.IO.File]::WriteAllText($tmp, ($record | ConvertTo-Json), (New-Object System.Text.UTF8Encoding($false)))
  Move-Item -LiteralPath $tmp -Destination $path -Force
}

function Assert-Environment {
  if (-not $VerifyOnly) {
    $principal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
      throw 'Administrator rights are required (the agent is installed as a service). Open PowerShell with "Run as administrator" and run the command again, or use install.cmd.'
    }
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
  if ($code -eq 401 -and -not $Bearer) {
    throw ('This manager does not allow installing without a token. In Fleet -> Add agent create an install command with a token, or ask your Vedha administrator to switch on tokenless install (AGENT_ALLOW_TOKENLESS_INSTALL=true on the manager). ' + $detail)
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
  $sep = [System.IO.Path]::DirectorySeparatorChar
  $root = [System.IO.Path]::GetFullPath($Destination).TrimEnd($sep) + $sep
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
      $target = [System.IO.Path]::GetFullPath((Join-Path $root $name.Replace('/', $sep)))
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
  if (Enter-VedhaElevation $managerUrl) { return }
  Assert-Environment
  if (-not $VerifyOnly) { Assert-VedhaTrust -Trust (Read-VedhaTrust) -Spki $script:VedhaReleaseP256Spki -Version $script:VedhaReleaseVersion -Replace:$ReplaceReleaseKey }

  if (-not $Token) { Write-Step 'no install token: this computer will show a pairing code, and a person approves it in Fleet' }
  Write-Step ("installing Vedha agent release " + $script:VedhaReleaseVersion + " from " + $managerUrl)
  $release = Get-VerifiedPackage $managerUrl

  $root = Join-Path $env:ProgramData 'vedha-agent'
  if ($VerifyOnly) {
    $stage = Join-Path ([System.IO.Path]::GetTempPath()) ('vedha-verify-' + [guid]::NewGuid().ToString('N'))
  } else {
    Protect-Directory $root
    $stage = Join-Path (Join-Path $root 'staging') ([guid]::NewGuid().ToString('N'))
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
    $exe = Join-Path (Join-Path $unpacked 'vedha-agent') 'vedha-agent.exe'
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

    # The packaged installer does the real work (checks the package again, locks the data folder,
    # registers the task, waits for the agent to connect, removes the token). It exits 0 when the
    # agent is connected or waiting for approval, 3 when it is installed but not connected yet.
    $global:LASTEXITCODE = 0
    $innerArgs = @{ Manager = $managerUrl; NoPause = $true }
    if ($Token) { $innerArgs.Token = $Token } else { $innerArgs.Pairing = $true }
    if ($Scope) { $innerArgs.Scope = $Scope }
    try {
      & $inner @innerArgs
    } catch [System.Management.Automation.PSSecurityException] {
      throw ('PowerShell policy blocked the packaged installer (' + $_.Exception.Message + '). Run the command exactly as Fleet shows it: it starts PowerShell with -ExecutionPolicy Bypass for this one process, which is all that is needed.')
    }
    $innerExit = $LASTEXITCODE
    if ($innerExit -eq 4) {
      throw 'The new version did not connect to the manager, so the previous version was put back and keeps running. Nothing was lost. The lines above say what the new version reported; the update will be tried again after 24 hours, or run the command again once that is fixed.'
    }
    if ($innerExit -ne 0 -and $innerExit -ne 3) { throw "The packaged installer failed (exit code $innerExit)." }

    # The agent is in place: remember which release key and release this computer now trusts.
    Write-VedhaTrust -Spki $script:VedhaReleaseP256Spki -Version $script:VedhaReleaseVersion -ManagerUrl $managerUrl
    Write-Step ('release key pinned on this computer (key id ' + (Get-VedhaKeyId $script:VedhaReleaseP256Spki) + ')')

    # Keep the installer and uninstaller with the install (the package is deleted below), so the
    # agent can be repaired or removed later without downloading anything.
    $tools = Join-Path $root 'tools'
    New-Item -ItemType Directory -Force -Path $tools | Out-Null
    foreach ($name in 'install.ps1', 'install.cmd', 'uninstall.ps1', 'uninstall.cmd') {
      $source = Join-Path $unpacked $name
      if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination (Join-Path $tools $name) -Force }
    }
    if ($innerExit -eq 3) {
      $script:InstalledNotConnected = $true
      Write-Step 'the agent is installed but has not connected yet; it keeps retrying by itself (see the checks above)'
    }
  } finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
  }
}

$script:InstalledNotConnected = $false
$script:ElevatedExit = $null
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
if ($null -ne $script:ElevatedExit) { exit $script:ElevatedExit }     # the elevated copy did the work
if ($script:InstalledNotConnected) { exit 3 }
