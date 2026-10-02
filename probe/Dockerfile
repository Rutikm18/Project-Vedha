# Probe image — scanner_module (engine) + agent (transport).
# Thin by design: pure-Python scanners, no vuln DB, no nmap/masscan required
# (the scanners are stdlib TCP-based; mass_scan falls back to a pure sweep).
# Dials OUT to the manager only — no inbound ports.

# ── Stage 1: select exactly the agent's code ─────────────────────────────────
# The image carries the agent's import closure and nothing else: never
# scanner/findings.py (judgement rules live on the manager), the campaign
# runner, accuracy gates, main_scripts/, cve/ or dev tooling. The check fails
# the build if the agent ever starts importing one of those, or uses a dynamic
# import. The whole build context is visible here so the check can see every
# package; only /closure moves on.
FROM python:3.12-slim AS select
WORKDIR /src
COPY . .
RUN python tools/agent_closure.py --check \
    && python tools/agent_closure.py --export /closure

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STATE_FILE=/var/lib/vedha-agent/state.json

COPY requirements-runtime.txt .
RUN pip install --no-cache-dir -r requirements-runtime.txt \
    && groupadd --gid 10001 vedha \
    && useradd --no-log-init --uid 10001 --gid 10001 \
       --home-dir /nonexistent --shell /usr/sbin/nologin vedha \
    && mkdir -p /var/lib/vedha-agent \
    && chown 10001:10001 /var/lib/vedha-agent

COPY --from=select /closure/ ./

# Build gate: every module the agent may load lazily mid-scan imports here.
RUN python -m agent.agent runtime-check

# register -> heartbeat -> poll -> scan -> submit (raw facts)
USER 10001:10001
CMD ["python", "-m", "agent.agent"]
