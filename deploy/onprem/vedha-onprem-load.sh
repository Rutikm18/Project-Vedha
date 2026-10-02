#!/bin/sh
# Vedha on-prem bundle loader.
#
#   sh vedha-onprem-load.sh vedha-onprem-<you>-<version>.tar.age \
#      --identity ~/vedha-age-key.txt --sha256 <checksum Vedha gave you separately> \
#      [--dir /opt/vedha]
#
# What it does, refusing to continue at the first problem:
#   1. checks the bundle's SHA-256 against the value Vedha gave you out of band,
#   2. decrypts it with YOUR age private key (it was encrypted only to you),
#   3. verifies the manifest's Ed25519 signature with the Vedha vendor key
#      embedded below, and every file against the manifest,
#   4. loads the platform images into Docker and unpacks the compose files.
#
# Needs: docker, age (apt install age / brew install age), OpenSSL 3, tar.
set -eu

# Set when Vedha builds your bundle (scripts/onprem_bundle.py); do not edit.
VEDHA_VENDOR_SPKI=""

say() { printf '%s\n' "$*"; }
die() { say "ERROR: $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

BUNDLE=""; IDENTITY=""; EXPECTED=""; DEST="./vedha-onprem"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --identity) [ "$#" -ge 2 ] || die "--identity needs a file"; IDENTITY=$2; shift 2 ;;
    --sha256)   [ "$#" -ge 2 ] || die "--sha256 needs a value"; EXPECTED=$2; shift 2 ;;
    --dir)      [ "$#" -ge 2 ] || die "--dir needs a path"; DEST=$2; shift 2 ;;
    -h|--help)  sed -n '2,20p' "$0"; exit 0 ;;
    -*)         die "unknown option $1" ;;
    *)          [ -z "$BUNDLE" ] || die "only one bundle at a time"; BUNDLE=$1; shift ;;
  esac
done
[ -n "$BUNDLE" ] && [ -f "$BUNDLE" ] || die "give the .tar.age bundle file"
[ -n "$IDENTITY" ] && [ -r "$IDENTITY" ] || die "--identity must point at your age private key file"
[ -n "$EXPECTED" ] || die "--sha256 is required: confirm the checksum Vedha sent you over a separate channel"
[ -n "$VEDHA_VENDOR_SPKI" ] || die "this loader has no vendor key embedded; use the one delivered with your bundle"
for tool in docker age openssl tar; do have "$tool" || die "$tool is required"; done
case "$(openssl version 2>/dev/null)" in "OpenSSL 3."*|"OpenSSL 4."*) ;; *) die "OpenSSL 3 is required to verify the signature" ;; esac

sha256() { { sha256sum "$1" 2>/dev/null || shasum -a 256 "$1"; } | awk '{print $1}'; }

say "1/4 Checking the bundle checksum ..."
GOT="$(sha256 "$BUNDLE")"
[ "$GOT" = "$(printf '%s' "$EXPECTED" | tr 'A-F' 'a-f')" ] || die "checksum mismatch (got $GOT). Do not use this file; contact Vedha."

WORK="$(mktemp -d "${TMPDIR:-/tmp}/vedha-onprem.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

say "2/4 Decrypting with your key ..."
age --decrypt --identity "$IDENTITY" --output "$WORK/bundle.tar" "$BUNDLE" \
  || die "decryption failed — is this the key whose public half you gave Vedha?"
# Refuse archive members that are absolute or climb out of the work dir.
tar -tf "$WORK/bundle.tar" | awk '/^\// || /(^|\/)\.\.(\/|$)/ {bad=1} END {exit bad}' \
  || die "bundle contains unsafe paths"
tar -xf "$WORK/bundle.tar" -C "$WORK"
rm -f "$WORK/bundle.tar"
ROOT="$(find "$WORK" -mindepth 1 -maxdepth 1 -type d -name 'vedha-onprem-*' | head -1)"
[ -n "$ROOT" ] && [ -f "$ROOT/manifest.json" ] || die "bundle has no manifest"

say "3/4 Verifying the Vedha signature and every file ..."
printf -- '-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----\n' "$VEDHA_VENDOR_SPKI" > "$WORK/vendor.pub"
tr -d '\n\r ' < "$ROOT/manifest.json.sig" > "$WORK/sig.b64"
openssl base64 -d -A -in "$WORK/sig.b64" -out "$WORK/sig.bin" 2>/dev/null || die "signature is not valid base64"
openssl pkeyutl -verify -pubin -inkey "$WORK/vendor.pub" -rawin \
  -in "$ROOT/manifest.json" -sigfile "$WORK/sig.bin" >/dev/null 2>&1 \
  || die "the bundle is NOT signed by Vedha. Do not load it; contact Vedha."
# manifest.json is written with sorted keys and fixed indentation: each file
# entry is "path", then "sha256".
awk -F'"' '/"path":/ {p=$4} /"sha256":/ && p != "" {print $4 "  " p; p=""}' "$ROOT/manifest.json" > "$WORK/files.sha"
[ -s "$WORK/files.sha" ] || die "manifest lists no files"
LISTED=0
while read -r want path; do
  case "$path" in /*|*..*) die "manifest lists an unsafe path: $path" ;; esac
  [ -f "$ROOT/$path" ] || die "missing file: $path"
  [ "$(sha256 "$ROOT/$path")" = "$want" ] || die "file does not match the manifest: $path"
  LISTED=$((LISTED + 1))
done < "$WORK/files.sha"
# Only the bundle's own top-level manifest + signature are unlisted (a nested
# agent-release/<v>/manifest.json is an ordinary listed file).
ACTUAL="$(cd "$ROOT" && find . -type f ! -path ./manifest.json ! -path ./manifest.json.sig | wc -l | tr -d ' ')"
[ "$ACTUAL" -eq "$LISTED" ] || die "bundle holds files the manifest does not list"
CUSTOMER="$(awk -F'"' '/^  "customer":/ {print $4; exit}' "$ROOT/manifest.json")"
VERSION="$(awk -F'"' '/^  "version":/ {print $4; exit}' "$ROOT/manifest.json")"
BUNDLE_ID="$(awk -F'"' '/^  "bundle_id":/ {print $4; exit}' "$ROOT/manifest.json")"
say "    Signed by Vedha — bundle $BUNDLE_ID, version $VERSION, issued to $CUSTOMER."

say "4/4 Loading images and unpacking to $DEST ..."
docker load -i "$ROOT/images.tar.gz"
mkdir -p "$DEST"
cp "$ROOT/compose/docker-compose.yml" "$DEST/docker-compose.yml"
[ -f "$DEST/.env" ] || cp "$ROOT/compose/.env.example" "$DEST/.env.example"
if [ -d "$ROOT/agent-release" ]; then
  mkdir -p "$DEST/agent-releases"
  cp -R "$ROOT/agent-release/." "$DEST/agent-releases/"
  say "    Agent release unpacked; set AGENT_RELEASE_PUBLIC_KEY=$(cat "$ROOT/agent-release/PUBLIC_KEY") in .env"
fi
cp "$ROOT/manifest.json" "$DEST/bundle-manifest.json"
say ""
say "Done. Next: cd $DEST, copy .env.example to .env, fill in every secret, then"
say "  docker compose --env-file .env -f docker-compose.yml --profile ui --profile edge up -d"
