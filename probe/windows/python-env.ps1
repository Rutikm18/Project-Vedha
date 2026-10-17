<#
  Which Python the Windows agent build may use. Dot-sourced by build-agent-exe.ps1 and
  publish-release.ps1, so there is ONE rule instead of two that can disagree.

  The build needs Python 3.10, 3.11 or 3.12. Nuitka refuses --mingw64 on Python 3.13 and newer, and
  MinGW is what compiles impacket's large generated RPC modules (MSVC runs out of heap space on them).

  Why this is its own file: the version check used to live only in publish-release.ps1 and only ran
  when the build environment (.venv-win) did not exist yet. An environment that already existed,
  made with Python 3.13, skipped the check, installed fine, and failed inside Nuitka.

  ASCII only, on purpose: Windows PowerShell 5.1 reads a BOM-less file in the ANSI code page.
  No PowerShell 7-only syntax either (no &&, ||, ?:, ??, ?.).
#>

function ConvertFrom-VedhaPythonVersion {
  # "Python 3.12.4" (what `python --version` prints) -> "3.12". $null when it cannot be read.
  param([string]$Text)
  if ("$Text" -match 'Python\s+(\d+)\.(\d+)') { return "$($Matches[1]).$($Matches[2])" }
  return $null
}

function Test-VedhaSupportedPython {
  # $true for 3.10, 3.11 and 3.12 only.
  param([string]$Version)
  return [bool]("$Version" -match '^3\.(10|11|12)$')
}

function Get-VedhaPythonVersion {
  # The "major.minor" of the Python at $File (with any launcher arguments such as -3.12), or $null when
  # it cannot be run or its version cannot be read. The version is parsed here, in PowerShell, from
  # `--version`: do NOT pass Python source with double quotes through `-c`, because Windows PowerShell 5.1
  # strips the inner double quotes and the source arrives malformed.
  param([string]$File, [string[]]$Arguments = @())
  try {
    $text = (& $File @Arguments --version 2>&1 | Out-String)
  } catch {
    return $null
  }
  return (ConvertFrom-VedhaPythonVersion $text)
}

function Find-VedhaPython {
  # A Python the build can use, or $null. The `py` launcher goes first: it can pick 3.12 even when the
  # `python` on the PATH is a newer one (the usual cause of this build failing). Returns
  # @{ File = ...; Arguments = ...; Version = ... }.
  $candidates = @()
  if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($v in '3.12', '3.11', '3.10') { $candidates += , @('py', "-$v") }
  }
  if (Get-Command python -ErrorAction SilentlyContinue) { $candidates += , @('python') }
  foreach ($c in $candidates) {
    $file = $c[0]
    $pyArgs = @($c | Select-Object -Skip 1)
    $ver = Get-VedhaPythonVersion $file $pyArgs
    if (Test-VedhaSupportedPython $ver) { return @{ File = $file; Arguments = $pyArgs; Version = $ver } }
  }
  return $null
}

function Assert-VedhaBuildPython {
  # Stop, with the way out, when the Python of an EXISTING build environment is one the build cannot use.
  param([string]$Python, [string]$Venv)
  $have = Get-VedhaPythonVersion $Python
  if (Test-VedhaSupportedPython $have) { return }
  $shown = if ($have) { "Python $have" } else { 'a Python whose version could not be read' }
  throw ("The build environment $Venv uses $shown, but the Windows build needs Python 3.10, 3.11 or 3.12 " +
         "(Nuitka cannot use MinGW on 3.13 or newer). Delete that folder and run this again:  " +
         "Remove-Item -Recurse -Force '$Venv'")
}

function Get-VedhaNoPythonMessage {
  return ('Python 3.10, 3.11 or 3.12 was not found. Install Python 3.12 (python.org, tick "Add python.exe to PATH", ' +
          'or run: winget install --id Python.Python.3.12 -e) and run this again. Python 3.13 and newer cannot be used.')
}
