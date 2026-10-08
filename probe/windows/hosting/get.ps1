<#
.SYNOPSIS
  Vedha agent - one-command downloader and installer for Windows.

.DESCRIPTION
  Downloads the Vedha Windows agent package from your Vedha download address, checks that it
  is exactly the package your Vedha contact meant (its SHA-256 is part of the command they
  gave you), unpacks it in an administrator-only folder and runs the installer.

  Run it from an ADMINISTRATOR PowerShell. It refuses to run otherwise: a script that raises
  its own rights from a folder any user can write to is an easy target, so you open the
  elevated prompt yourself and the whole command then runs without a second prompt.

.EXAMPLE
  & ([scriptblock]::Create((irm https://downloads.example.com/windows/get.ps1))) `
      -Version 2.2.2 -Sha256 <64 hex characters> -Token vet_XXXXXXXX

.NOTES
  Nothing here changes your firewall, antivirus, proxy, certificate or execution-policy
  settings. The files are removed when the installer finishes.
#>
[CmdletBinding()]
param(
  [string]$Token = '',            # one-time install token (vet_...)
  [string]$TokenFile = '',        # or read it from a file
  [string]$Sha256 = '',           # SHA-256 of the package zip (from your Vedha contact)
  [string]$Version = '',          # package version to download, e.g. 2.2.2
  [string]$BaseUrl = '__VEDHA_DOWNLOAD_BASE__',   # filled in when the script is published
  [string]$Manager = '',          # passed on to the installer
  [string]$Scope = '',            # passed on to the installer
  [string]$Proxy = '',            # web proxy: used for the download AND passed to the installer
  [string]$CaBundle = '',         # passed on to the installer
  [string]$Name = '',             # passed on to the installer
  [switch]$TrustHostedHash,       # use the hash published next to the package (weaker: same server)
  [switch]$DownloadOnly,          # download, verify and unpack, then stop (used by the tests)
  [string]$WorkDir = '',          # where to unpack (default: an administrator-only folder)
  [switch]$KeepFiles,             # do not delete the downloaded files afterwards
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest   # e.g. -SkipPreflight -NoWait
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Pure helpers (no side effects; unit-tested)
# ---------------------------------------------------------------------------

function Resolve-GetBaseUrl {
  # The download address must be https (http only for this computer, for tests).
  param([string]$Value)
  $text = "$Value".Trim().TrimEnd('/')
  if (-not $text -or $text -like '__*') {
    throw 'This command does not say where to download from. Ask your Vedha contact for the full command.'
  }
  if ($text -notmatch '^(https://[A-Za-z0-9._~:/%-]+|http://(127\.0\.0\.1|localhost)(:\d+)?(/[A-Za-z0-9._~%-]*)*)$') {
    throw "The download address must be an https:// address (got '$text')."
  }
  return $text
}

function Test-GetSha256Text {
  param([string]$Value)
  return [bool]("$Value" -match '^[0-9a-fA-F]{64}$')
}

function Test-GetVersionText {
  param([string]$Value)
  return [bool]("$Value" -match '^\d+(\.\d+){1,3}$')
}

function Test-GetTokenText {
  param([string]$Value)
  return [bool]("$Value" -match '^vet_[A-Za-z0-9_-]{8,}$')
}

function ConvertFrom-GetRelease {
  # Reads the small JSON file published next to a package. Returns the fields we use, or throws.
  param([string]$Text)
  try { $data = $Text | ConvertFrom-Json } catch { throw 'The release information on the server is not valid.' }
  if (-not (Test-GetVersionText $data.version)) { throw 'The release information has no valid version.' }
  if (-not (Test-GetSha256Text $data.sha256)) { throw 'The release information has no valid SHA-256.' }
  $zip = [string]$data.zip
  if (-not $zip -or $zip -match '(^[a-zA-Z][a-zA-Z0-9+.-]*:)|(\.\.)|(^/)|(\\)' -or $zip -notmatch '^[A-Za-z0-9._/-]+\.zip$') {
    throw 'The release information names an unsafe file.'
  }
  return [pscustomobject]@{ Version = [string]$data.version; Sha256 = ([string]$data.sha256).ToLower(); Zip = $zip }
}

function Get-GetSha256 {
  # SHA-256 of a file as lower-case hex (.NET directly: no dependence on any PowerShell module).
  param([string]$Path)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $stream = [System.IO.File]::OpenRead($Path)
    try { return (($sha.ComputeHash($stream) | ForEach-Object { $_.ToString('x2') }) -join '') }
    finally { $stream.Dispose() }
  } finally { $sha.Dispose() }
}

function Get-InstallerArguments {
  # The arguments handed to install.ps1. Each value is checked: they are passed as separate
  # arguments (never through cmd.exe), but a bad value should be refused here with a clear message.
  param([string]$Token, [string]$Manager, [string]$Scope, [string]$Proxy, [string]$CaBundle, [string]$Name, [string]$TokenFile, [string[]]$Rest)
  $list = New-Object System.Collections.Generic.List[string]
  if ($Token) {
    if (-not (Test-GetTokenText $Token)) { throw 'That does not look like an install token (it should start with vet_). Copy it again.' }
    $list.Add('-Token'); $list.Add($Token)
  }
  if ($TokenFile) { $list.Add('-TokenFile'); $list.Add($TokenFile) }
  $pairs = [ordered]@{ Manager = $Manager; Scope = $Scope; Proxy = $Proxy; CaBundle = $CaBundle; Name = $Name }
  foreach ($key in $pairs.Keys) {
    $value = [string]$pairs[$key]
    if (-not $value) { continue }
    if ($value -match '[\x00-\x1f"]') { throw "The value given for -$key contains characters that are not allowed." }
    $list.Add("-$key"); $list.Add($value)
  }
  foreach ($extra in @($Rest)) { if ($extra) { $list.Add([string]$extra) } }
  return ,$list.ToArray()
}

# ---------------------------------------------------------------------------
# Windows-only helpers
# ---------------------------------------------------------------------------

function Test-GetIsWindows { return ([Environment]::OSVersion.Platform -eq 'Win32NT') }

function Test-GetIsAdmin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  return ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Write-GetStep { param([string]$Text) Write-Host ''; Write-Host $Text -ForegroundColor Cyan }
function Write-GetGood { param([string]$Text) Write-Host "    OK   $Text" -ForegroundColor Green }

function Lock-GetFolder {
  # Only SYSTEM and Administrators may touch the unpacked installer, so nothing can be swapped
  # between the check and the run. Principals are given by SID, so this works in any language.
  param([string]$Path)
  & icacls.exe $Path /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Could not restrict access to $Path (icacls exit code $LASTEXITCODE)." }
}

function Get-GetFile {
  param([string]$Url, [string]$OutFile, [string]$ProxyUrl)
  $previous = $ProgressPreference
  $ProgressPreference = 'SilentlyContinue'      # the progress bar makes Windows PowerShell 5.1 downloads very slow
  try {
    $arguments = @{ Uri = $Url; OutFile = $OutFile; UseBasicParsing = $true; ErrorAction = 'Stop' }
    if ($ProxyUrl) { $arguments['Proxy'] = $ProxyUrl }
    Invoke-WebRequest @arguments
  } catch {
    throw "Could not download $Url : $($_.Exception.Message). Check this computer can reach that address (a firewall or proxy may need to allow it; add -Proxy http://proxy:port if one is required)."
  } finally { $ProgressPreference = $previous }
}

# ---------------------------------------------------------------------------
# The download
# ---------------------------------------------------------------------------

function Invoke-Get {
  if ($DownloadOnly -and -not $WorkDir) { throw '-DownloadOnly needs -WorkDir.' }
  $base = Resolve-GetBaseUrl $BaseUrl

  # What must the package hash to? A hash given in the command is the strong choice.
  if ($Sha256) {
    if (-not (Test-GetSha256Text $Sha256)) { throw 'The -Sha256 value is not a 64-character hex string. Copy the whole command again.' }
  } elseif (-not $TrustHostedHash) {
    throw "This command needs the package's SHA-256 (-Sha256 ...), which your Vedha contact gives you with the token. Without it, the download could not be checked against anything you trust."
  }
  if ($Version) {
    if (-not (Test-GetVersionText $Version)) { throw "The -Version value '$Version' is not a version number (for example 2.2.2)." }
  } elseif (-not $TrustHostedHash) {
    throw 'This command needs the package version (-Version ...). Copy the whole command again.'
  }

  $arguments = Get-InstallerArguments -Token $Token -Manager $Manager -Scope $Scope -Proxy $Proxy -CaBundle $CaBundle -Name $Name -TokenFile $TokenFile -Rest $Rest

  if (-not $DownloadOnly) {
    if (-not (Test-GetIsWindows)) { throw 'This installer runs on Windows only.' }
    if (-not (Test-GetIsAdmin)) {
      throw "Open PowerShell as Administrator (right-click Start, 'Terminal (Admin)' or 'Windows PowerShell (Admin)'), then run the same command again. Nothing has been downloaded or changed."
    }
  }
  [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

  $root = $WorkDir
  $locked = $false
  if (-not $root) { $root = Join-Path (Join-Path $env:SystemRoot 'Temp') ('vedha-install-' + [guid]::NewGuid().ToString('N')) }
  New-Item -ItemType Directory -Force -Path $root | Out-Null
  if (-not $WorkDir) { Lock-GetFolder $root; $locked = $true }
  $exitCode = 1
  try {
    Write-GetStep '[1/3] Finding the package'
    $expected = $Sha256.ToLower()
    $zipUrl = ''
    if ($TrustHostedHash -and (-not $Version -or $Version -eq 'latest')) {
      $releaseFile = Join-Path $root 'latest.json'
      Get-GetFile "$base/latest.json" $releaseFile $Proxy
      $release = ConvertFrom-GetRelease ([System.IO.File]::ReadAllText($releaseFile))
      if (-not $expected) { $expected = $release.Sha256 }
      $Version = $release.Version
      $zipUrl = "$base/$($release.Zip)"
    } else {
      if (-not $expected) {
        $releaseFile = Join-Path $root 'release.json'
        Get-GetFile "$base/$Version/release.json" $releaseFile $Proxy
        $release = ConvertFrom-GetRelease ([System.IO.File]::ReadAllText($releaseFile))
        if ($release.Version -ne $Version) { throw 'The release information on the server is for a different version.' }
        $expected = $release.Sha256
      }
      $zipUrl = "$base/$Version/vedha-agent-win.zip"
    }
    Write-GetGood "Vedha agent package $Version"

    Write-GetStep '[2/3] Downloading and checking it'
    $zipPath = Join-Path $root 'vedha-agent-win.zip'
    Get-GetFile $zipUrl $zipPath $Proxy
    $actual = Get-GetSha256 $zipPath
    if ($actual -ne $expected) {
      Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
      throw ("The downloaded package does not match the SHA-256 in your command (expected $($expected.Substring(0, 12))..., got $($actual.Substring(0, 12))...). " +
             'Nothing was installed. Do not use it: ask your Vedha contact for a new command, and check that nothing between this computer and the download address is altering files.')
    }
    Write-GetGood 'The package is exactly the one your command names (SHA-256 matches).'
    $pkg = Join-Path $root 'package'
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $pkg)
    $installer = Join-Path $pkg 'install.ps1'
    if (-not (Test-Path -LiteralPath $installer)) { throw 'The package does not contain install.ps1.' }
    Write-GetGood "Unpacked to $pkg"

    if ($DownloadOnly) {
      Write-Host "    (download only: stopping here; the files are in $pkg)"
      return 0
    }

    Write-GetStep '[3/3] Installing'
    $powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
    & $powershell -NoProfile -ExecutionPolicy Bypass -File $installer @arguments
    $exitCode = $LASTEXITCODE
    return $exitCode
  } finally {
    if (-not $KeepFiles -and -not $DownloadOnly) {
      Set-Location $env:SystemRoot -ErrorAction SilentlyContinue
      Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
    }
  }
}

# Run only when executed, not when dot-sourced by the tests.
if ($MyInvocation.InvocationName -ne '.') {
  try {
    exit ([int](@(Invoke-Get) | Select-Object -Last 1))
  } catch {
    Write-Host ''
    Write-Host "STOPPED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
  }
}
