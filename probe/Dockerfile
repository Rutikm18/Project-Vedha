# Probe image — scanner_module (engine) + agent (transport).
# Thin by design: pure-Python scanners, no vuln DB, no nmap/masscan required
# (the scanners are stdlib TCP-based; mass_scan falls back to a pure sweep).
# Dials OUT to the manager only — no inbound ports.
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STATE_FILE=/var/lib/vedha-probe/state.json

# Engine + sequencing + transport (scanner/ is frozen — never modified).
COPY requirements-runtime.txt .
RUN pip install --no-cache-dir -r requirements-runtime.txt \
    && groupadd --gid 10001 vedha \
    && useradd --no-log-init --uid 10001 --gid 10001 \
       --home-dir /nonexistent --shell /usr/sbin/nologin vedha \
    && mkdir -p /var/lib/vedha-probe \
    && chown 10001:10001 /var/lib/vedha-probe

COPY scanner/  ./scanner/
COPY workflow/ ./workflow/
COPY agent/    ./agent/

# register -> heartbeat -> poll -> scan -> submit (raw facts)
USER 10001:10001
CMD ["python", "-m", "agent.agent"]
