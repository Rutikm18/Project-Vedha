FROM python:3.12-slim AS base
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      nmap testssl.sh eyewitness wget curl ca-certificates golang-go \
    && rm -rf /var/lib/apt/lists/*

# Install Go-based tools
RUN go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
RUN nuclei -update-templates

# Install NetExec and Impacket via pip
RUN pip install --no-cache-dir netexec impacket

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py .

RUN useradd -r -u 1001 -g root vedha-agent
RUN mkdir -p /etc/vedha/certs && chown vedha-agent /etc/vedha/certs

USER vedha-agent

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python3 -c "import sys; sys.exit(0)"

ENV POLL_INTERVAL=10
ENV HEARTBEAT_INTERVAL=30
ENV LOG_LEVEL=INFO

ENTRYPOINT ["python3", "-u", "agent.py"]
