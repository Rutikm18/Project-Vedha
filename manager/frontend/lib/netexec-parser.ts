const ANSI_ESCAPE = /\u001b\[[0-?]*[ -/]*[@-~]/g;

export interface NetExecHost {
  host: string;
  hostname?: string;
  domain?: string;
  os?: string;
  smbv1?: boolean;
  signing?: boolean;
  nullSession?: boolean;
}

export interface NetExecParseResult {
  hosts: NetExecHost[];
  recognizedLines: number;
  status: "ok" | "degraded" | "schema_mismatch";
  candidateDiscoveryLines: number;
  discoveryLines: number;
  recognizedDiscoveryLines: number;
  ignoredInformationalLines: number;
  unrecognizedDiscoveryLines: number;
}

function parseBoolean(value: string | undefined): boolean | undefined {
  if (!value || value.toLowerCase() === "none") return undefined;
  return value.toLowerCase() === "true";
}

/**
 * Parse NetExec's supported text log format.
 *
 * NetExec has no stable JSON output flag. Host discovery lines expose the
 * fields used by this adapter as `(name:...)`, `(domain:...)`,
 * `(signing:...)`, and `(SMBv1:...)`.
 */
export function parseNetExecLog(
  raw: string,
  options: { successfulAuthIsNullSession?: boolean } = {},
): NetExecParseResult {
  const hosts = new Map<string, NetExecHost>();
  let recognizedLines = 0;
  let discoveryLines = 0;
  let recognizedDiscoveryLines = 0;
  let ignoredInformationalLines = 0;

  for (const originalLine of raw.split(/\r?\n/)) {
    const line = originalLine.replace(ANSI_ESCAPE, "").trim();
    if (!line) continue;

    const discovery = line.match(
      /\bSMB\s+(\S+)\s+(\d+)\s+(\S+)\s+\[\*\]\s+(.+)$/i,
    );
    if (discovery) {
      discoveryLines += 1;
      const [, host, , columnHostname, details] = discovery;
      if (/^(?:Enumerated shares|Password policy)\b/i.test(details)) {
        ignoredInformationalLines += 1;
        continue;
      }
      const name = details.match(/\(name:([^)]+)\)/i)?.[1]?.trim();
      const domain = details.match(/\(domain:([^)]+)\)/i)?.[1]?.trim();
      const signingRaw = details.match(/\(signing:(True|False|None)\)/i)?.[1];
      const smbv1Raw = details.match(/\(SMBv1:(True|False|None)\)/i)?.[1];

      if (name || domain || signingRaw || smbv1Raw) {
        const os = details.split(/\s+\(name:/i, 1)[0]?.trim();
        const existing = hosts.get(host) ?? { host };
        hosts.set(host, {
          ...existing,
          hostname: name || columnHostname || existing.hostname,
          domain: domain || existing.domain,
          os: os || existing.os,
          signing: parseBoolean(signingRaw) ?? existing.signing,
          smbv1: parseBoolean(smbv1Raw) ?? existing.smbv1,
        });
        recognizedLines += 1;
        recognizedDiscoveryLines += 1;
      }
      continue;
    }

    const auth = line.match(/\bSMB\s+(\S+)\s+(\d+)\s+(\S+)\s+\[\+\]\s+/i);
    if (auth && options.successfulAuthIsNullSession) {
      const [, host, , hostname] = auth;
      const existing = hosts.get(host) ?? { host };
      hosts.set(host, {
        ...existing,
        hostname: existing.hostname || hostname,
        nullSession: true,
      });
      recognizedLines += 1;
    }
  }

  const unrecognizedDiscoveryLines = Math.max(
    0,
    discoveryLines - recognizedDiscoveryLines - ignoredInformationalLines,
  );
  const status = unrecognizedDiscoveryLines === 0
    ? "ok"
    : recognizedDiscoveryLines > 0
      ? "degraded"
      : "schema_mismatch";

  return {
    hosts: [...hosts.values()],
    recognizedLines,
    status,
    candidateDiscoveryLines: discoveryLines,
    discoveryLines,
    recognizedDiscoveryLines,
    ignoredInformationalLines,
    unrecognizedDiscoveryLines,
  };
}
