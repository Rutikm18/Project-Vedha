#!/usr/bin/env bash
# images.sh — build and tidy the release images. Sourced by install.sh.
#
# Needs from the caller: log, warn, COMPOSE_CMD (array), VEDHA_BACKEND_IMAGE,
# VEDHA_FRONTEND_IMAGE; optional PREVIOUS_BACKEND_IMAGE / PREVIOUS_FRONTEND_IMAGE,
# SERIAL_BUILD=1, FORCE_REBUILD=1, BUILD_CACHE_KEEP (default 3GB).
#
# Why a helper: the deploy used to build the backend, then the frontend, every time
# (even for a release whose images already existed), and never removed an old
# release's images (about half a GB each), so a small disk filled up over a few deploys.

# Build one service unless this release's image is already on the host. The image
# tag is the commit, so an existing one is by definition identical.
_build_service() {
  local svc="$1" image="$2" logfile="$3"
  if [ "${FORCE_REBUILD:-0}" != "1" ] && docker image inspect "$image" >/dev/null 2>&1; then
    echo "reusing $image (already built for this release)" > "$logfile"
    return 0
  fi
  "${COMPOSE_CMD[@]}" build "$svc" > "$logfile" 2>&1
}

# Build the API and dashboard images, concurrently. They are different tags, so the
# "image already exists" race (three services sharing the backend tag) cannot
# happen; each is still a single-target build. The backend is mostly network wait
# (pip) and the frontend mostly CPU, so the backend hides inside the frontend's time.
# SERIAL_BUILD=1 builds one after the other (very small hosts).
build_images() {
  local dir backend_rc=0 frontend_rc=0 pid_b pid_f
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
