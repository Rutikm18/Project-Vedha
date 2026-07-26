import type { FindingSeverity } from "./findings-store";
import { randomUUID } from "crypto";

export interface OpenVASFinding {
  title: string;
  severity: FindingSeverity;
  cvss: string;
  cves: string[];
  affectedHost: string;
  port: string;
  description: string;
  solution?: string;
  insight?: string;
  detection?: string;
  nvtOid?: string;
  qod?: string;
}

export interface OpenVASTaskState {
  taskId: string;
  ownerTenantId: string;
  ownerUserId: string;
  status: "queued" | "running" | "done" | "error";
  progress: number;
  findings: OpenVASFinding[];
  error?: string;
}

const taskStore = new Map<string, OpenVASTaskState>();

export function getTask(taskId: string): OpenVASTaskState | undefined {
  return taskStore.get(taskId);
}

export function setTask(taskId: string, state: OpenVASTaskState): void {
  taskStore.set(taskId, state);
}

export function cvssToSeverity(score: number): FindingSeverity {
  if (score >= 9.0) return "CRITICAL";
  if (score >= 7.0) return "HIGH";
  if (score >= 4.0) return "MEDIUM";
  if (score > 0)    return "LOW";
  return "INFO";
}

interface OpenVASHelperOutput {
  status: "done" | "error";
  findings?: OpenVASFinding[];
  reason?: string;
  error?: string;
}

function isOpenVASFinding(value: unknown): value is OpenVASFinding {
  if (!value || typeof value !== "object") return false;
  const finding = value as Partial<OpenVASFinding>;
  return (
    typeof finding.title === "string"
    && ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"].includes(finding.severity ?? "")
    && typeof finding.cvss === "string"
    && Array.isArray(finding.cves)
    && finding.cves.every((cve) => typeof cve === "string")
    && typeof finding.affectedHost === "string"
    && typeof finding.port === "string"
    && typeof finding.description === "string"
  );
}

export function parseOpenVASHelperOutput(raw: string): OpenVASFinding[] {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`OpenVAS helper returned malformed JSON: ${String(err)}`);
  }

  if (!parsed || typeof parsed !== "object") {
    throw new Error("OpenVAS helper returned an invalid response envelope.");
  }

  const output = parsed as OpenVASHelperOutput;
  if (output.status === "error") {
    const reason = output.reason ? ` (${output.reason})` : "";
    throw new Error(`OpenVAS helper failed${reason}: ${output.error ?? "unknown error"}`);
  }
  if (output.status !== "done") {
    throw new Error("OpenVAS helper response did not contain a terminal status.");
  }
  if (!Array.isArray(output.findings)) {
    throw new Error("OpenVAS helper success response did not contain a findings array.");
  }
  const invalidIndex = output.findings.findIndex((finding) => !isOpenVASFinding(finding));
  if (invalidIndex >= 0) {
    throw new Error(`OpenVAS helper returned an invalid finding at index ${invalidIndex}.`);
  }

  return output.findings;
}

function boundedEnvMs(
  name: string,
  fallback: number,
  minimum: number,
  maximum: number,
): number {
  const configured = Number(process.env[name]);
  if (!Number.isFinite(configured)) return fallback;
  return Math.min(maximum, Math.max(minimum, Math.trunc(configured)));
}

export async function startOpenVASScan(params: {
  targets: string[];
  gvmHost: string;
  gvmPort: number;
  gvmUser: string;
  gvmPassword: string;
  scanConfig: string;
  ownerTenantId: string;
  ownerUserId: string;
}): Promise<{ taskId: string }> {
  const taskId = `openvas-${Date.now()}-${randomUUID()}`;
  const owner = {
    ownerTenantId: params.ownerTenantId,
    ownerUserId: params.ownerUserId,
  };
  setTask(taskId, { taskId, ...owner, status: "queued", progress: 0, findings: [] });

  void runOpenVASScanBackground(taskId, params, owner);

  return { taskId };
}

async function runOpenVASScanBackground(taskId: string, params: {
  targets: string[];
  gvmHost: string;
  gvmPort: number;
  gvmUser: string;
  gvmPassword: string;
  scanConfig: string;
}, owner: { ownerTenantId: string; ownerUserId: string }): Promise<void> {
  setTask(taskId, { taskId, ...owner, status: "running", progress: 5, findings: [] });

  let scriptPath = "";
  let configPath = "";
  let outputPath = "";

  try {
    const { spawn } = await import("child_process");
    const { default: os }   = await import("os");
    const { default: path } = await import("path");
    const { default: fs }   = await import("fs");

    scriptPath = path.join(os.tmpdir(), `vedha-openvas-${taskId}.py`);
    configPath = path.join(os.tmpdir(), `vedha-openvas-${taskId}.json`);
    outputPath = path.join(os.tmpdir(), `vedha-openvas-out-${taskId}.json`);

    const scanTimeoutMs = boundedEnvMs(
      "OPENVAS_SCAN_TIMEOUT_MS",
      7_200_000,
      60_000,
      86_400_000,
    );
    const pollIntervalMs = boundedEnvMs(
      "OPENVAS_POLL_INTERVAL_MS",
      15_000,
      1_000,
      60_000,
    );

    const helperConfig = {
      gvmHost: params.gvmHost,
      gvmPort: params.gvmPort,
      gvmUser: params.gvmUser,
      gvmPassword: params.gvmPassword,
      targets: params.targets,
      taskId,
      outputPath,
      scanConfig: params.scanConfig,
      scanTimeoutSeconds: Math.ceil(scanTimeoutMs / 1000),
      pollIntervalSeconds: Math.ceil(pollIntervalMs / 1000),
    };

    const pyScript = `
import json
import sys
import time
import traceback
from gvm.connections import TLSConnection
from gvm.protocols import Gmp
from gvm.transforms import EtreeCheckCommandTransform

with open(sys.argv[1], "r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

GVM_HOST = CONFIG["gvmHost"]
GVM_PORT = CONFIG["gvmPort"]
GVM_USER = CONFIG["gvmUser"]
GVM_PASSWORD = CONFIG["gvmPassword"]
TARGET_VALUES = CONFIG["targets"]
TASK_ID = CONFIG["taskId"]
OUT_PATH = CONFIG["outputPath"]
SCAN_CONFIG_NAME = CONFIG["scanConfig"]
SCAN_TIMEOUT_SECONDS = CONFIG["scanTimeoutSeconds"]
POLL_INTERVAL_SECONDS = CONFIG["pollIntervalSeconds"]

if type(GVM_PORT) is not int or not 1 <= GVM_PORT <= 65535:
    raise ValueError("gvmPort must be an integer between 1 and 65535")
if not isinstance(TARGET_VALUES, list) or not TARGET_VALUES:
    raise ValueError("targets must be a non-empty list")
if not all(isinstance(target, str) and target for target in TARGET_VALUES):
    raise ValueError("every target must be a non-empty string")
if type(SCAN_TIMEOUT_SECONDS) is not int or SCAN_TIMEOUT_SECONDS <= 0:
    raise ValueError("scanTimeoutSeconds must be a positive integer")
if type(POLL_INTERVAL_SECONDS) is not int or POLL_INTERVAL_SECONDS <= 0:
    raise ValueError("pollIntervalSeconds must be a positive integer")

TARGETS = ",".join(TARGET_VALUES)

CONFIG_IDS = {
    "full-fast":          "daba56c8-73ec-11df-a475-002264764cea",
    "full-fast-ultimate": "698f691e-7489-11df-9d8c-002264764cea",
    "empty":              "085569ce-73ed-11df-83c3-002264764cea",
    "system-discovery":   "8715c877-47a0-438d-98a3-27c7a6ab2196",
}
FULL_PORT_LIST_ID = "33d0cd82-57c6-11e1-8ed1-406186ea4fc5"
OPENVAS_SCANNER_ID = "08b69003-5fc2-4037-a479-93b440211c73"

def require_resource(response, element_name, resource_id, label):
    if response.find(f".//{element_name}[@id='{resource_id}']") is None:
        raise RuntimeError(
            f"{label} {resource_id} is unavailable. Verify the Greenbone feed "
            "has finished importing and the resource is owned by the GMP user."
        )

target_id = None
gvm_task_id = None

try:
    config_id = CONFIG_IDS.get(SCAN_CONFIG_NAME)
    if config_id is None:
        raise ValueError(f"unsupported scan config: {SCAN_CONFIG_NAME}")

    with TLSConnection(hostname=GVM_HOST, port=GVM_PORT) as conn:
        with Gmp(conn, transform=EtreeCheckCommandTransform()) as gmp:
            gmp.authenticate(GVM_USER, GVM_PASSWORD)

            require_resource(gmp.get_scan_configs(), "config", config_id, "scan config")
            require_resource(gmp.get_port_lists(), "port_list", FULL_PORT_LIST_ID, "port list")
            require_resource(gmp.get_scanners(), "scanner", OPENVAS_SCANNER_ID, "scanner")

            try:
                target_resp = gmp.create_target(
                    name=f"vedha-{TASK_ID}",
                    hosts=TARGETS,
                    port_list_id=FULL_PORT_LIST_ID,
                )
                target_id = target_resp.get("id")
                if not target_id:
                    raise RuntimeError("GMP create_target response did not include an id")

                task_resp = gmp.create_task(
                    name=f"vedha-task-{TASK_ID}",
                    config_id=config_id,
                    target_id=target_id,
                    scanner_id=OPENVAS_SCANNER_ID,
                )
                gvm_task_id = task_resp.get("id")
                if not gvm_task_id:
                    raise RuntimeError("GMP create_task response did not include an id")

                gmp.start_task(gvm_task_id)
                deadline = time.monotonic() + SCAN_TIMEOUT_SECONDS
                terminal_failures = {
                    "stopped",
                    "interrupted",
                    "failed",
                    "delete requested",
                    "stop requested",
                }

                while True:
                    if time.monotonic() >= deadline:
                        try:
                            gmp.stop_task(gvm_task_id)
                        except Exception:
                            pass
                        raise TimeoutError(
                            f"OpenVAS task exceeded {SCAN_TIMEOUT_SECONDS}s deadline"
                        )

                    report = gmp.get_task(gvm_task_id)
                    status = (report.findtext("task/status") or "unknown").strip().lower()
                    if status == "done":
                        break
                    if status in terminal_failures:
                        raise RuntimeError(f"OpenVAS task entered terminal state: {status}")
                    time.sleep(POLL_INTERVAL_SECONDS)

                results = gmp.get_results(
                    task_id=gvm_task_id,
                    filter_string="levels=hmlg rows=-1",
                )

                findings = []
                for result in results.findall(".//result"):
                    severity = float(result.findtext("severity") or "0")
                    if severity < 0.1:
                        continue
                    nvt = result.find("nvt")
                    cves = []
                    if nvt is not None:
                        cves = [
                            ref.get("id")
                            for ref in nvt.findall("refs/ref[@type='cve']")
                            if ref.get("id")
                        ]
                    sev_map = [
                        (9.0, "CRITICAL"),
                        (7.0, "HIGH"),
                        (4.0, "MEDIUM"),
                        (0.1, "LOW"),
                    ]
                    sev_label = next(
                        (label for score, label in sev_map if severity >= score),
                        "INFO",
                    )
                    findings.append({
                        "title":        result.findtext("name") or "Unnamed OpenVAS result",
                        "severity":     sev_label,
                        "cvss":         str(severity),
                        "cves":         cves,
                        "affectedHost": result.findtext("host/hostname") or result.findtext("host") or "",
                        "port":         result.findtext("port") or "",
                        "description":  result.findtext("description") or "",
                        "solution":     nvt.findtext("solution") if nvt is not None else None,
                        "insight":      nvt.findtext("insight") if nvt is not None else None,
                        "detection":    nvt.findtext("detection") if nvt is not None else None,
                        "nvtOid":       nvt.get("oid") if nvt is not None else None,
                        "qod":          result.findtext("qod/value"),
                    })
            finally:
                if gvm_task_id:
                    try:
                        gmp.delete_task(gvm_task_id, ultimate=True)
                    except Exception:
                        pass
                if target_id:
                    try:
                        gmp.delete_target(target_id, ultimate=True)
                    except Exception:
                        pass

        with open(OUT_PATH, "w") as f:
            json.dump(
                {"status": "done", "findings": findings, "count": len(findings)},
                f,
            )
except Exception as exc:
    with open(OUT_PATH, "w") as f:
        json.dump(
            {
                "status": "error",
                "reason": type(exc).__name__,
                "error": str(exc),
                "findings": [],
            },
            f,
        )
    traceback.print_exc()
    raise
`;

    fs.writeFileSync(
      configPath,
      JSON.stringify(helperConfig),
      { mode: 0o600, flag: "wx" },
    );
    fs.writeFileSync(scriptPath, pyScript, { mode: 0o600, flag: "wx" });

    const processResult = await new Promise<{
      code: number | null;
      signal: NodeJS.Signals | null;
      stderr: string;
      spawnError?: string;
    }>((resolve) => {
      let settled = false;
      let stderr = "";
      const finish = (result: {
        code: number | null;
        signal: NodeJS.Signals | null;
        spawnError?: string;
      }): void => {
        if (settled) return;
        settled = true;
        resolve({ ...result, stderr });
      };

      const proc = spawn("python3", [scriptPath, configPath], {
        timeout: scanTimeoutMs + 30_000,
        killSignal: "SIGTERM",
        stdio: ["ignore", "ignore", "pipe"],
      });
      proc.stderr?.on("data", (chunk: Buffer | string) => {
        stderr = `${stderr}${chunk.toString()}`.slice(-16_384);
      });
      proc.on("error", (err) => {
        finish({ code: null, signal: null, spawnError: err.message });
      });
      proc.on("close", (code, signal) => {
        finish({ code, signal });
      });
    });

    if (processResult.spawnError) {
      throw new Error(`OpenVAS helper failed to start: ${processResult.spawnError}`);
    }
    if (!fs.existsSync(outputPath)) {
      const detail = processResult.stderr.trim() || "helper produced no result file";
      throw new Error(
        `OpenVAS helper exited without a result (code=${processResult.code}, signal=${processResult.signal}): ${detail}`,
      );
    }

    const findings = parseOpenVASHelperOutput(fs.readFileSync(outputPath, "utf-8"));
    if (processResult.code !== 0 || processResult.signal) {
      const detail = processResult.stderr.trim() || "no stderr";
      throw new Error(
        `OpenVAS helper exited abnormally (code=${processResult.code}, signal=${processResult.signal}): ${detail}`,
      );
    }
    setTask(taskId, { taskId, ...owner, status: "done", progress: 100, findings });
  } catch (err) {
    setTask(taskId, { taskId, ...owner, status: "error", progress: 0, findings: [], error: String(err) });
  } finally {
    const { default: fs } = await import("fs");
    for (const filePath of [scriptPath, configPath, outputPath]) {
      if (!filePath) continue;
      try {
        fs.unlinkSync(filePath);
      } catch {
        // The helper may fail before creating its output file.
      }
    }
  }
}
