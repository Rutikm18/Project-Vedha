#!/usr/bin/env bash
# images.sh — build and tidy the release images. Sourced by install.sh.
#
# Needs from the caller: log, warn, COMPOSE_CMD (array), VEDHA_BACKEND_IMAGE,
# VEDHA_FRONTEND_IMAGE; optional PREVIOUS_BACKEND_IMAGE / PREVIOUS_FRONTEND_IMAGE,
# SERIAL_BUILD=1, FORCE_REBUILD=1, BUILD_CACHE_KEEP (default 3GB), and
# VEDHA_IMAGE_REGISTRY (e.g. ghcr.io/<owner>: pull CI-built images instead of building).
#
# Why a helper: the deploy used to build the backend, then the frontend, every time
# (even for a release whose images already existed), and never removed an old
# release's images (about half a GB each), so a small disk filled up over a few deploys.

# Get one service's release image onto the host, cheapest way first. The image tag
# is the commit, so an image that already exists, or one CI pushed under that tag,
# is by definition identical to what a build here would produce.
#   1. already on this host            → reuse
#   2. VEDHA_IMAGE_REGISTRY is set and CI pushed it → pull (seconds, no CPU)
#   3. otherwise                       → build here
# FORCE_REBUILD=1 skips 1 and 2.
_build_service() {
  local svc="$1" image="$2" logfile="$3" remote
  : > "$logfile"
  if [ "${FORCE_REBUILD:-0}" != "1" ]; then
    if docker image inspect "$image" >/dev/null 2>&1; then
      echo "reusing $image (already built for this release)" >> "$logfile"
      return 0
    fi
    if [ -n "${VEDHA_IMAGE_REGISTRY:-}" ]; then
      remote="${VEDHA_IMAGE_REGISTRY%/}/$image"
      if docker pull -q "$remote" >> "$logfile" 2>&1 && docker tag "$remote" "$image" >> "$logfile" 2>&1; then
        docker image rm "$remote" >/dev/null 2>&1 || true   # keep only the local tag
        echo "pulled $remote (built by CI, nothing to compile here)" >> "$logfile"
        return 0
      fi
      echo "$remote is not available (not pushed yet, or not logged in); building here instead" >> "$logfile"
    fi
  fi
  "${COMPOSE_CMD[@]}" build "$svc" >> "$logfile" 2>&1
}

# Build the API and dashboard images, concurrently. They are different tags, so the
# "image already exists" race (three services sharing the backend tag) cannot
# happen; each is still a single-target build. The backend is mostly network wait
# (pip) and the frontend mostly CPU, so the backend hides inside the frontend's time.
# SERIAL_BUILD=1 builds one after the other (very small hosts).
build_images() {
  local dir backend_rc=0 frontend_rc=0 pid_b pid_f
  # The registry may come from the installer's environment or from .env (the
  # installer keeps hand-added lines outside its managed block).
  if [ -z "${VEDHA_IMAGE_REGISTRY:-}" ] && [ -f "${APP_DIR:-.}/.env" ]; then
    VEDHA_IMAGE_REGISTRY="$(grep '^VEDHA_IMAGE_REGISTRY=' "${APP_DIR:-.}/.env" | tail -n1 | cut -d= -f2- || true)"
  fi
  export VEDHA_IMAGE_REGISTRY
  dir="$(mktemp -d)"
  if [ "${SERIAL_BUILD:-0}" = "1" ]; then
    _build_service api "$VEDHA_BACKEND_IMAGE" "$dir/backend.log" || backend_rc=$?
    _build_service frontend "$VEDHA_FRONTEND_IMAGE" "$dir/frontend.log" || frontend_rc=$?
  else
    _build_service api "$VEDHA_BACKEND_IMAGE" "$dir/backend.log" & pid_b=$!
    _build_service frontend "$VEDHA_FRONTEND_IMAGE" "$dir/frontend.log" & pid_f=$!
    wait "$pid_b" || backend_rc=$?
    wait "$pid_f" || frontend_rc=$?
  fi
  local name
  for name in backend frontend; do
    { printf '\n── %s image build ──\n' "$name"; cat "$dir/$name.log"; } >> "${DEPLOY_LOG:-/dev/null}"
  done
  if [ "$backend_rc" -ne 0 ] || [ "$frontend_rc" -ne 0 ]; then
    [ "$backend_rc" -eq 0 ]  || { warn "backend image build failed — last lines:";  tail -25 "$dir/backend.log"  >&2; }
    [ "$frontend_rc" -eq 0 ] || { warn "frontend image build failed — last lines:"; tail -25 "$dir/frontend.log" >&2; }
    rm -rf "$dir"
    return 1
  fi
  rm -rf "$dir"
  return 0
}

# After a release is promoted: remove the images of older releases, keeping the
# current and the previous (the rollback target), and cap BuildKit's cache. Only
# commit-tagged images (12 hex characters) are touched; an image a container still
# uses cannot be removed, which is exactly right, so failures are ignored.
prune_old_images() {
  local repo image tag keep
  for repo in vedha-backend vedha-frontend; do
    docker images --format '{{.Repository}}:{{.Tag}}' "$repo" 2>/dev/null | while read -r image; do
      tag="${image#*:}"
      [[ "$tag" =~ ^[0-9a-f]{12}$ ]] || continue
      for keep in "${VEDHA_BACKEND_IMAGE:-}" "${VEDHA_FRONTEND_IMAGE:-}" \
                  "${PREVIOUS_BACKEND_IMAGE:-}" "${PREVIOUS_FRONTEND_IMAGE:-}"; do
        [ "$image" = "$keep" ] && continue 2
      done
      if docker image rm "$image" >/dev/null 2>&1; then log "removed old release image $image"; fi
    done || true   # never let tidying fail a deploy that already succeeded (set -e)
  done
  docker image prune -f >/dev/null 2>&1 || true
  docker builder prune -f --keep-storage "${BUILD_CACHE_KEEP:-3GB}" >/dev/null 2>&1 || true
  return 0
}
