# VEDHA Manager API image: small, quick to rebuild, runs as an unprivileged user.
#
#   deps    resolves and installs the Python dependencies into /install (wheels only,
#           so no compiler is ever needed); a BuildKit cache mount keeps pip's download
#           cache OUT of the image and across builds.
#   runner  the base image plus /install, the code, and the detection engine.
#
# The base is Alpine (musl) by default: about 107 MB smaller than Debian slim. The
# optional INSTALL_EXTRAS=1 stack (scikit-learn, xgboost, shap...) ships glibc-only
# wheels, so it builds on the slim base instead:
#
#   docker build --build-arg INSTALL_EXTRAS=1 --build-arg PYTHON_BASE=python:3.12-slim .
#
# (Makefile `up-ai` does exactly that.)
ARG PYTHON_BASE=python:3.12-alpine

# ── deps ─────────────────────────────────────────────────────────────────────
FROM ${PYTHON_BASE} AS deps
ARG INSTALL_EXTRAS=0
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build
# Only the requirement files: the layer (and the install below) is reused until
# a dependency actually changes, however often the code does.
COPY requirements-core.txt requirements-extras.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$INSTALL_EXTRAS" = "1" ] && [ -f /etc/alpine-release ]; then \
      echo "INSTALL_EXTRAS=1 needs glibc wheels: build with --build-arg PYTHON_BASE=python:3.12-slim (make up-ai does)" >&2; \
      exit 1; \
    fi \
 && pip install --prefix=/install --only-binary=:all: -r requirements-core.txt \
 && if [ "$INSTALL_EXTRAS" = "1" ]; then \
      pip install --prefix=/install -r requirements-extras.txt; \
    fi \
 # Packages ship their own test suites inside the wheel; nothing imports them.
 && find /install -type d -name tests -prune -exec rm -rf {} + \
 # The compiled caches stay (read-only root, and PYTHONDONTWRITEBYTECODE below,
 # mean they could not be regenerated at run time).
 && python -m compileall -q /install/lib

# ── runner ───────────────────────────────────────────────────────────────────
FROM ${PYTHON_BASE} AS runner
# Deployed version, injected from the repo-root VERSION file via the
# VEDHA_VERSION build arg (see docker-compose.yml / Makefile). Surfaced at
# runtime by app.version.get_version() and GET /health.
ARG VEDHA_VERSION=dev
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 VEDHA_VERSION=$VEDHA_VERSION
WORKDIR /app

COPY --from=deps /install /usr/local

# Alpine has no system time-zone database. Python's zoneinfo (blackout windows,
# report time zones) and the TZ variable (log lines) both read /usr/share/zoneinfo,
# so point it at the data the `tzdata` package already installed: no extra bytes.
RUN if [ ! -d /usr/share/zoneinfo ]; then \
      ln -s "$(python -c 'import tzdata, os; print(os.path.join(os.path.dirname(tzdata.__file__), "zoneinfo"))')" /usr/share/zoneinfo; \
    fi

# Unprivileged user, created the same way on Alpine and Debian (no useradd/adduser
# differences). The code stays root-owned and read-only to it: the API never writes
# under /app. /var/lib/vedha is where offline intel bundles are written when
# VEDHA_INTEL_DIR points there; /tmp is always writable.
RUN echo 'vedha:x:10001:10001::/nonexistent:/sbin/nologin' >> /etc/passwd \
 && echo 'vedha:x:10001:' >> /etc/group \
 && mkdir -p /var/lib/vedha \
 && chown 10001:10001 /var/lib/vedha

COPY . .
# Compile the app's own modules now. The code is read-only to the runtime user and
# PYTHONDONTWRITEBYTECODE is set, so without this every start (and every uvicorn
# worker) would recompile all of it from source before serving.
RUN python -m compileall -q app alembic scripts

# P1: bake detection_engine (+ its pinned vuln/KEV/EPSS snapshots) INTO the
# image so it's self-contained for prod: no runtime volume mount, no drift.
# `detection_engine` is a named build context (docker-compose additional_contexts);
# DETECTION_ENGINE_PATH points here. Its own .dockerignore keeps tests out.
COPY --from=detection_engine . /opt/detection_engine

USER 10001:10001

EXPOSE 8000

# Container health is checked by compose with Python (no curl in the image).
# Default command serves the API. The compose `migrate` service overrides this
# to run `alembic upgrade head` + seed before the API starts.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
