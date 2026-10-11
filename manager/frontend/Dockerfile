# ─────────────────────────────────────────────────────────────────────────────
# VEDHA Platform dashboard: small image, quick rebuilds.
#
#   deps     install the lockfile's packages (npm cache kept out of the image)
#   builder  Next.js standalone build
#   runner   plain Alpine + the single `node` binary + the standalone output.
#            node:22-alpine is ~240 MB because it also carries npm, yarn and
#            corepack; a running Next server needs none of them.
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: install reproducible build dependencies ─────────────────────────
FROM node:22-alpine AS deps
WORKDIR /app

COPY package.json package-lock.json* ./

# ci install is reproducible and uses the lockfile exactly. The cache mount keeps
# npm's download cache between builds without putting it in a layer.
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

# ── Stage 2: build Next.js standalone bundle ─────────────────────────────────
FROM node:22-alpine AS builder
WORKDIR /app

# Copy deps from previous stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Deployed version, passed from the repo-root VERSION file via docker-compose
# (mirrors how the backend image receives VEDHA_VERSION). Exposed to the client
# bundle as NEXT_PUBLIC_APP_VERSION so the sidebar footer stays in sync.
ARG VEDHA_VERSION=dev
ENV NEXT_PUBLIC_APP_VERSION=$VEDHA_VERSION

# The TypeScript check takes about half of `next build` and is the step that needs
# the big heap. CI already runs `tsc --noEmit` and the tests on every change, and
# the installer only deploys a CI-verified release, so the server skips repeating
# it. Build with --build-arg SKIP_TYPECHECK=0 to keep it.
ARG SKIP_TYPECHECK=1
ENV NEXT_SKIP_TYPECHECK=$SKIP_TYPECHECK

# Raise the V8 heap ceiling so the build does not OOM on small hosts (Node
# auto-sizes a tiny heap on low-RAM boxes). Backed by the host swap the installer
# provisions when RAM < 4GB.
ENV NODE_OPTIONS="--max-old-space-size=3072"

RUN npm run build

# ── Stage 3: minimal production runner ───────────────────────────────────────
# Must be the same Alpine release as node:22-alpine (the node binary links the
# system musl, libstdc++ and libgcc).
FROM alpine:3.24 AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# The node binary and the two shared libraries it needs, taken from the image the
# app was built with, so the runtime and the build can never drift apart.
COPY --from=deps /usr/local/bin/node /usr/local/bin/node
COPY --from=deps /usr/lib/libstdc++.so.6* /usr/lib/libgcc_s.so.1 /usr/lib/

# Non-root user for security
RUN addgroup -S -g 1001 nodejs \
 && adduser -S -u 1001 -G nodejs nextjs \
 # Writable data directory retained for server-side cache/runtime state.
 && mkdir -p /app/data && chown nextjs:nodejs /app/data

# Copy the standalone output (self-contained Node server)
COPY --from=builder /app/public                           ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static     ./.next/static

USER nextjs

EXPOSE 3000

# Probes the dedicated liveness route; busybox wget ships with Alpine. `-Y off`
# ignores any HTTP(S)_PROXY the container inherits, which would otherwise send the
# probe to the proxy instead of this server.
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD wget -q -Y off -O /dev/null http://127.0.0.1:3000/api/health || exit 1

CMD ["node", "server.js"]
