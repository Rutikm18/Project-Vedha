#!/usr/bin/env bash
# Publish a built Windows agent package to S3 (behind CloudFront) and print the one-line
# install commands to give a customer.
#
#   probe/windows/hosting/publish-to-s3.sh \
#       --bucket vedha-agent-downloads-123456789012 \
#       --zip vedha-agent-win.zip --release vedha-agent-win.release.json \
#       --base-url https://downloads.example.com/windows \
#       --distribution-id E123ABCDEF4567
#
# The zip, vedha-agent-win.zip.sha256 and vedha-agent-win.release.json come from the
# "vedha-agent-windows" artifact of the vedha-agent-windows-build workflow.
#
# What it does, in this order (so a half-finished publish never points anyone at a missing file):
#   1. checks the zip against its release.json (SHA-256 and size);
#   2. refuses to overwrite a version that is already published (versions are immutable) unless --force;
#   3. uploads  <prefix>/<version>/vedha-agent-win.zip, .zip.sha256 and release.json  (cached for a year);
#   4. uploads  <prefix>/get.ps1  with your --base-url filled in  (never cached);
#   5. uploads  <prefix>/latest.json  last (never cached) unless --no-latest;
#   6. asks CloudFront to forget get.ps1 and latest.json when --distribution-id is given;
#   7. prints the install commands.
#
# Needs: bash, the AWS CLI (configured), python3. Works on macOS and Linux.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bucket=""; zip=""; release=""; base_url=""; prefix="windows"; region=""; profile=""
distribution=""; make_latest=1; force=0; dry_run=0

usage() { sed -n '2,24p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }
die() { echo "publish-to-s3: $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --bucket) bucket="${2:-}"; shift 2 ;;
    --zip) zip="${2:-}"; shift 2 ;;
    --release) release="${2:-}"; shift 2 ;;
    --base-url) base_url="${2:-}"; shift 2 ;;
    --prefix) prefix="${2:-}"; shift 2 ;;
    --region) region="${2:-}"; shift 2 ;;
    --profile) profile="${2:-}"; shift 2 ;;
    --distribution-id) distribution="${2:-}"; shift 2 ;;
    --no-latest) make_latest=0; shift ;;
    --force) force=1; shift ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

[ -n "$bucket" ]   || die "--bucket is required"
[ -n "$zip" ]      || die "--zip is required"
[ -n "$release" ]  || die "--release is required"
[ -n "$base_url" ] || die "--base-url is required (the public https address of <prefix>, e.g. https://downloads.example.com/windows)"
[ -f "$zip" ]      || die "zip not found: $zip"
[ -f "$release" ]  || die "release file not found: $release"
case "$base_url" in https://*) ;; *) die "--base-url must start with https://" ;; esac
case "$base_url" in *[!A-Za-z0-9._~:/%-]*) die "--base-url contains characters that are not allowed" ;; esac
base_url="${base_url%/}"
case "$prefix" in ""|*[!A-Za-z0-9._/-]*|/*|*..*) die "--prefix must be a plain relative path such as windows" ;; esac
prefix="${prefix%/}"
command -v python3 >/dev/null 2>&1 || die "python3 is required"
if [ "$dry_run" -eq 0 ]; then command -v aws >/dev/null 2>&1 || die "the AWS CLI (aws) is required"; fi

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi
}
size_of() { wc -c < "$1" | tr -d ' '; }

# --- read and check the release file ------------------------------------------------------------
info="$(python3 - "$release" <<'PY'
import json, re, sys
data = json.load(open(sys.argv[1], encoding="utf-8-sig"))
version, sha, size = str(data.get("version", "")), str(data.get("sha256", "")).lower(), data.get("size", "")
if not re.fullmatch(r"\d+(\.\d+){1,3}", version): sys.exit("release.json has no valid version")
if not re.fullmatch(r"[0-9a-f]{64}", sha): sys.exit("release.json has no valid sha256")
if not isinstance(size, int) or size <= 0: sys.exit("release.json has no valid size")
print(version, sha, size)
PY
)" || die "the release file is not usable"
read -r version sha size <<<"$info"

actual_sha="$(sha256_of "$zip")"
actual_size="$(size_of "$zip")"
[ "$actual_sha" = "$sha" ]   || die "the zip's SHA-256 ($actual_sha) is not the one in the release file ($sha). Use the zip and release file from the same build."
[ "$actual_size" = "$size" ] || die "the zip's size ($actual_size) is not the one in the release file ($size)."

aws_cmd=(aws)
[ -n "$profile" ] && aws_cmd+=(--profile "$profile")
[ -n "$region" ]  && aws_cmd+=(--region "$region")

run() {
  if [ "$dry_run" -eq 1 ]; then echo "  [dry run] $*"; else "$@"; fi
}

version_key="$prefix/$version/vedha-agent-win.zip"

# --- never overwrite a published version ----------------------------------------------------------
if [ "$dry_run" -eq 0 ]; then
  if "${aws_cmd[@]}" s3api head-object --bucket "$bucket" --key "$version_key" >/dev/null 2>&1; then
    if [ "$force" -eq 1 ]; then
      echo "WARNING: version $version is already published; overwriting it because of --force."
    else
      die "version $version is already published at s3://$bucket/$version_key. Versions are immutable: bump AGENT_VERSION and build again, or pass --force if you really mean to replace it."
    fi
  fi
fi

echo "Publishing agent $version (SHA-256 $sha) to s3://$bucket/$prefix/"

# --- upload ------------------------------------------------------------------------------------------
immutable="public, max-age=31536000, immutable"
nocache="no-cache, max-age=0"

run "${aws_cmd[@]}" s3 cp "$zip" "s3://$bucket/$version_key" \
  --content-type application/zip --cache-control "$immutable" --only-show-errors
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
printf '%s  vedha-agent-win.zip\n' "$sha" > "$tmp/vedha-agent-win.zip.sha256"
run "${aws_cmd[@]}" s3 cp "$tmp/vedha-agent-win.zip.sha256" "s3://$bucket/$prefix/$version/vedha-agent-win.zip.sha256" \
  --content-type text/plain --cache-control "$immutable" --only-show-errors
run "${aws_cmd[@]}" s3 cp "$release" "s3://$bucket/$prefix/$version/release.json" \
  --content-type application/json --cache-control "$immutable" --only-show-errors

# the bootstrap script, with the download address filled in
python3 - "$here/get.ps1" "$tmp/get.ps1" "$base_url" <<'PY'
import sys
src, dst, base = sys.argv[1:4]
text = open(src, encoding="utf-8").read()
if "__VEDHA_DOWNLOAD_BASE__" not in text:
    sys.exit("get.ps1 has no download-address placeholder")
open(dst, "w", encoding="utf-8", newline="").write(text.replace("__VEDHA_DOWNLOAD_BASE__", base, 1))
PY
run "${aws_cmd[@]}" s3 cp "$tmp/get.ps1" "s3://$bucket/$prefix/get.ps1" \
  --content-type "text/plain; charset=utf-8" --cache-control "$nocache" --only-show-errors

if [ "$make_latest" -eq 1 ]; then
  run "${aws_cmd[@]}" s3 cp "$release" "s3://$bucket/$prefix/latest.json" \
    --content-type application/json --cache-control "$nocache" --only-show-errors
fi

if [ -n "$distribution" ]; then
  paths=("/$prefix/get.ps1")
  [ "$make_latest" -eq 1 ] && paths+=("/$prefix/latest.json")
  run "${aws_cmd[@]}" cloudfront create-invalidation --distribution-id "$distribution" --paths "${paths[@]}" >/dev/null
fi

# --- what to give the customer ---------------------------------------------------------------------------
cat <<EOF

Published agent $version.

Give the customer ONE of these (replace <TOKEN> with a one-time install token from Fleet;
send the token and this command by a different channel from any email that links to the zip).
They must run it in an ADMINISTRATOR prompt.

  PowerShell (works on every supported Windows):

    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm $base_url/get.ps1))) -Version $version -Sha256 $sha -Token <TOKEN>

  Command Prompt with curl (Windows 10 1803 / Server 2019 or newer):

    curl.exe -fsSL $base_url/get.ps1 -o "%SystemRoot%\\Temp\\vedha-get.ps1" && powershell -NoProfile -ExecutionPolicy Bypass -File "%SystemRoot%\\Temp\\vedha-get.ps1" -Version $version -Sha256 $sha -Token <TOKEN>

Add  -Proxy http://proxy:3128   or   -Scope 10.0.5.0/24   to either command when needed.
The hash in the command is what makes the download trustworthy: it comes from you, not from the bucket.
EOF
