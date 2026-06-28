# Probe image — scanner_module (engine) + agent (transport).
# Thin by design: pure-Python scanners, no vuln DB, no nmap/masscan required
# (the scanners are stdlib TCP-based; mass_scan falls back to a pure sweep).
# Dials OUT to the manager only — no inbound ports.
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 STATE_FILE=/var/lib/adversa-probe/state.json

RUN pip install --no-cache-dir httpx>=0.27 && mkdir -p /var/lib/adversa-probe

# Engine + sequencing + transport (scanner/ is frozen — never modified).
COPY scanner/  ./scanner/
COPY workflow/ ./workflow/
COPY agent/    ./agent/

# register -> heartbeat -> poll -> scan -> submit (raw facts)
CMD ["python", "-m", "agent.agent"]
