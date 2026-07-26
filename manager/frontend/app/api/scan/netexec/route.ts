import { NextRequest, NextResponse } from "next/server";
import { spawn } from "child_process";
import os from "os";
import path from "path";
import fs from "fs";
import { randomUUID } from "crypto";
import { createFinding } from "../../../../lib/findings-store";
import { parseNetExecLog, type NetExecHost } from "../../../../lib/netexec-parser";
import { withVerifiedLocalScanner } from "../../../../lib/with-backend";
import { isScopeAllowed } from "../../../../lib/permissions-store";
import { validateNetExecScanRequest } from "../../../../lib/scanner-request-validation";

const MAX_PROCESS_OUTPUT = 65_536;

interface NetExecProcessResult {
  code: number | null;
  signal: NodeJS.Signals | null;
  stdout: string;
  stderr: string;
  timedOut: boolean;
  spawnError?: string;
}

interface NetExecRunResult {
  hosts: NetExecHost[];
  warnings: string[];
}

function appendTail(current: string, chunk: Buffer | string): string {
  return `${current}${chunk.toString()}`.slice(-MAX_PROCESS_OUTPUT);
}

async function runNxc(
  args: string[],
  outputFile: string,
  options: { successfulAuthIsNullSession?: boolean } = {},
): Promise<NetExecRunResult> {
  try {
    const result = await new Promise<NetExecProcessResult>((resolve) => {
      let settled = false;
      let stdout = "";
      let stderr = "";
      let timedOut = false;
      let forceKillTimer: NodeJS.Timeout | undefined;

      const proc = spawn(
        "nxc",
        [...args, "--no-progress", "--log", outputFile],
        { stdio: ["ignore", "pipe", "pipe"] },
      );

      const timeout = setTimeout(() => {
        timedOut = true;
        proc.kill("SIGTERM");
        forceKillTimer = setTimeout(() => proc.kill("SIGKILL"), 5_000);
      }, 120_000);

      const finish = (
        code: number | null,
        signal: NodeJS.Signals | null,
        spawnError?: string,
      ): void => {
        if (settled) return;
        settled = true;
        clearTimeout(timeout);
        if (forceKillTimer) clearTimeout(forceKillTimer);
        resolve({ code, signal, stdout, stderr, timedOut, spawnError });
      };

      proc.stdout?.on("data", (chunk: Buffer | string) => {
        stdout = appendTail(stdout, chunk);
      });
      proc.stderr?.on("data", (chunk: Buffer | string) => {
        stderr = appendTail(stderr, chunk);
      });
      proc.on("error", (err) => finish(null, null, err.message));
      proc.on("close", (code, signal) => finish(code, signal));
    });

    if (result.spawnError) {
      throw new Error(`NetExec failed to start: ${result.spawnError}`);
    }
    if (result.timedOut) {
      throw new Error("NetExec exceeded the 120s scan deadline.");
    }
    if (result.code !== 0 || result.signal) {
      const detail = result.stderr.trim() || result.stdout.trim() || "no diagnostic output";
      throw new Error(
        `NetExec exited abnormally (code=${result.code}, signal=${result.signal}): ${detail}`,
      );
    }

    const logOutput = fs.existsSync(outputFile)
      ? fs.readFileSync(outputFile, "utf-8")
      : "";
    const output = [logOutput, result.stdout]
      .filter((part) => part.trim())
      .join("\n");
    if (!output.trim()) {
      throw new Error("NetExec completed without producing log output.");
    }

    const parsed = parseNetExecLog(output, options);
    if (parsed.status === "schema_mismatch") {
      throw new Error(
        `NetExec output schema was not recognized (${parsed.candidateDiscoveryLines} candidate discovery line(s), ${parsed.recognizedDiscoveryLines} parsed).`,
      );
    }
    const warnings = parsed.status === "degraded"
      ? [
          `NetExec output was only partially recognized (${parsed.unrecognizedDiscoveryLines} of ${parsed.candidateDiscoveryLines} candidate discovery line(s) unparsed).`,
        ]
      : [];
    return { hosts: parsed.hosts, warnings };
  } finally {
    try {
      fs.unlinkSync(outputFile);
    } catch {
      // NetExec may fail before creating its log.
    }
  }
}

export const POST = withVerifiedLocalScanner(async (req: NextRequest, { user }) => {
  const body = await req.json().catch(() => null);
  const validated = validateNetExecScanRequest(body);
  if (validated.ok === false) {
    return NextResponse.json({ error: validated.error }, { status: 400 });
  }
  const {
    targets,
    domain,
    username,
    password,
    checks,
    createFindings,
  } = validated.value;

  if (!user.email) {
    return NextResponse.json(
      { error: "Local scanner routes require a user-backed access token." },
      { status: 403 },
    );
  }
  const denied = targets.filter((target) => !isScopeAllowed(user.email!, target));
  if (denied.length > 0) {
    return NextResponse.json(
      { error: `Targets out of your permitted scope: ${denied.join(", ")}` },
      { status: 403 },
    );
  }

  const scanId    = `netexec-${Date.now()}`;
  const startTime = new Date().toISOString();
  const t0        = Date.now();
  const allHosts: NetExecHost[] = [];
  const allFindings = [];
  const findingsCreated: string[] = [];
  const warnings: string[] = [];

  const failureResponse = (err: unknown) => NextResponse.json({
    scanId,
    status: "failed",
    error: err instanceof Error ? err.message : String(err),
    partial: allHosts.length > 0 || allFindings.length > 0 || warnings.length > 0,
    hosts: allHosts,
    findings: allFindings,
    warnings,
    startTime,
    endTime: new Date().toISOString(),
    elapsed: `${((Date.now() - t0) / 1000).toFixed(1)}s`,
  }, { status: 502 });

  for (const cidr of targets) {
    const suffix   = `${scanId}-${randomUUID()}`;
    const baseFile = path.join(os.tmpdir(), `vedha-nxc-base-${suffix}.log`);
    const nullFile = path.join(os.tmpdir(), `vedha-nxc-null-${suffix}.log`);
    const authFile = path.join(os.tmpdir(), `vedha-nxc-auth-${suffix}.log`);

    if (checks.includes("smb")) {
      let baseResult: NetExecRunResult;
      try {
        baseResult = await runNxc(["smb", cidr], baseFile);
      } catch (err) {
        return failureResponse(err);
      }
      warnings.push(...baseResult.warnings);

      for (const host of baseResult.hosts) {
        allHosts.push(host);
        if (host.smbv1 === true) {
          allFindings.push({
            title: `SMBv1 Enabled — ${host.host}`,
            severity: "CRITICAL" as const,
            cvss: "9.8",
            cvssVector: "",
            category: "Network Service",
            status: "OPEN" as const,
            affectedHost: host.host,
            description: "SMBv1 is enabled. Vulnerable to EternalBlue (MS17-010) and other SMBv1 exploits.",
            technicalDetails: `Host: ${host.host}\nHostname: ${host.hostname ?? ""}\nOS: ${host.os ?? ""}`,
            attackPath: `External → ${host.host}:445 → SMBv1 Exploit (EternalBlue)`,
            evidence: [{ label: "NetExec Result", content: JSON.stringify(host, null, 2) }],
            impact: "Full remote code execution without authentication on unpatched systems.",
            remediation: [
              { step: 1, title: "Disable SMBv1", command: "Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force", description: "Disable SMBv1 protocol immediately.", estimatedHours: 0.5, completed: false },
            ],
            compliance: [],
            mitre: [{ id: "T1210", name: "Exploitation of Remote Services" }],
            source: "netexec" as const,
          });
        }
        if (host.signing === false) {
          allFindings.push({
            title: `SMB Signing Disabled — ${host.host}`,
            severity: "HIGH" as const,
            cvss: "7.5",
            cvssVector: "",
            category: "Network Service",
            status: "OPEN" as const,
            affectedHost: host.host,
            description: "SMB signing is not enforced. Vulnerable to NTLM relay attacks.",
            technicalDetails: `Host: ${host.host}\nSigning: false`,
            attackPath: `CORP VLAN → LLMNR/NBNS Poison → NTLMv2 Capture → Relay to ${host.host}`,
            evidence: [{ label: "NetExec Result", content: JSON.stringify(host, null, 2) }],
            impact: "NTLM relay attack possible — lateral movement without cracking credentials.",
            remediation: [
              { step: 1, title: "Enforce SMB signing", command: "Set-SmbServerConfiguration -RequireSecuritySignature $true -Force", description: "Require SMB signing on all hosts.", estimatedHours: 1, completed: false },
            ],
            compliance: [],
            mitre: [{ id: "T1557.001", name: "LLMNR/NBT-NS Poisoning and SMB Relay" }],
            source: "netexec" as const,
          });
        }
      }
    }

    if (checks.includes("null-session")) {
      let nullResult: NetExecRunResult;
      try {
        nullResult = await runNxc(
          ["smb", cidr, "-u", "", "-p", "", "--shares"],
          nullFile,
          { successfulAuthIsNullSession: true },
        );
      } catch (err) {
        return failureResponse(err);
      }
      warnings.push(...nullResult.warnings);

      for (const host of nullResult.hosts) {
        if (host.nullSession === true) {
          const existing = allHosts.find((h) => h.host === host.host);
          if (existing) existing.nullSession = true;
          allFindings.push({
            title: `SMB Null Session Enabled — ${host.host}`,
            severity: "HIGH" as const,
            cvss: "7.5",
            cvssVector: "",
            category: "Authentication",
            status: "OPEN" as const,
            affectedHost: host.host,
            description: "SMB null session is enabled. Unauthenticated enumeration of shares and user information is possible.",
            technicalDetails: `Host: ${host.host}\nNull session authentication succeeded.`,
            attackPath: `External → ${host.host}:445 → Anonymous SMB Authentication`,
            evidence: [{ label: "NetExec Null Session", content: JSON.stringify(host, null, 2) }],
            impact: "Unauthenticated access to SMB shares and user enumeration.",
            remediation: [
              { step: 1, title: "Restrict anonymous SMB access", description: "Set RestrictAnonymous=2 in registry.", estimatedHours: 0.5, completed: false },
            ],
            compliance: [],
            mitre: [{ id: "T1135", name: "Network Share Discovery" }],
            source: "netexec" as const,
          });
        }
      }
    }

    if (checks.includes("shares") && username && password) {
      const passwordFile = path.join(os.tmpdir(), `vedha-nxc-password-${suffix}`);
      try {
        fs.writeFileSync(passwordFile, `${password}\n`, { mode: 0o600, flag: "wx" });
        const authResult = await runNxc(
          [
            "smb",
            cidr,
            "-u",
            username,
            "-p",
            passwordFile,
            ...(domain ? ["-d", domain] : []),
            "--shares",
            "--pass-pol",
          ],
          authFile,
        );
        warnings.push(...authResult.warnings);
      } catch (err) {
        return failureResponse(err);
      } finally {
        try {
          fs.unlinkSync(passwordFile);
        } catch {
          // The credential file may fail to be created.
        }
      }
    }
  }

  if (createFindings) {
    for (const f of allFindings) {
      try {
        const created = createFinding(f);
        findingsCreated.push(created.id);
      } catch { /* non-fatal */ }
    }
  }

  return NextResponse.json({
    scanId,
    status: warnings.length > 0 ? "degraded" : "completed",
    startTime,
    endTime: new Date().toISOString(),
    elapsed: `${((Date.now() - t0) / 1000).toFixed(1)}s`,
    hosts: allHosts,
    findings: allFindings,
    findingsCreated,
    warnings: [...new Set(warnings)],
  });
});
