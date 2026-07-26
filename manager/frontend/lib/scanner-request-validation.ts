import { isIP } from "node:net";

const HOST_LABEL = /^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$/;
const OPENVAS_CONFIGS = new Set([
  "full-fast",
  "full-fast-ultimate",
  "empty",
  "system-discovery",
]);
const NETEXEC_CHECKS = new Set(["smb", "null-session", "shares"]);

export type ValidationResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: string; source: "request" | "configuration" };

export interface OpenVASScanRequest {
  targets: string[];
  scanConfig: string;
  gvmHost: string;
  gvmPort: number;
  gvmUser: string;
  createFindings: boolean;
}

export interface NetExecScanRequest {
  targets: string[];
  domain: string;
  username: string;
  password: string;
  checks: Array<"smb" | "null-session" | "shares">;
  createFindings: boolean;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return !!value && typeof value === "object" && !Array.isArray(value);
}

function isValidHostname(value: string): boolean {
  return (
    value.length <= 253
    && !value.endsWith(".")
    && value.split(".").every((label) => HOST_LABEL.test(label))
  );
}

function isValidScannerTarget(value: string): boolean {
  if (!value || value.length > 200 || /[\0\s,]/.test(value)) return false;
  if (isIP(value) !== 0) return true;

  const cidr = value.match(/^(.+)\/(\d{1,3})$/);
  if (cidr) {
    const family = isIP(cidr[1]);
    const prefix = Number(cidr[2]);
    return family === 4
      ? prefix >= 0 && prefix <= 32
      : family === 6 && prefix >= 0 && prefix <= 128;
  }

  const range = value.match(/^([0-9.]+)-([0-9.]+)$/);
  if (range) return isIP(range[1]) === 4 && isIP(range[2]) === 4;
  if (/^[0-9.]+$/.test(value)) return false;

  return isValidHostname(value);
}

export function validateScannerTargets(value: unknown): ValidationResult<string[]> {
  if (!Array.isArray(value) || value.length === 0 || value.length > 4_096) {
    return {
      ok: false,
      error: "targets must be a non-empty array with at most 4096 entries.",
      source: "request",
    };
  }
  if (!value.every((target) => typeof target === "string")) {
    return { ok: false, error: "Every target must be a string.", source: "request" };
  }

  const targets = [...new Set(value.map((target) => target.trim()))];
  const invalid = targets.filter((target) => !isValidScannerTarget(target));
  if (invalid.length > 0) {
    return {
      ok: false,
      error: `Invalid target(s): ${invalid.slice(0, 5).join(", ")}`,
      source: "request",
    };
  }
  return { ok: true, value: targets };
}

function validateHost(value: unknown): value is string {
  if (typeof value !== "string") return false;
  const host = value.trim();
  return host.length > 0 && (isIP(host) !== 0 || isValidHostname(host));
}

function validateSafeString(
  value: unknown,
  options: { maxLength: number; allowEmpty?: boolean },
): value is string {
  const { maxLength, allowEmpty = false } = options;
  const hasUsableValue = allowEmpty
    ? value === "" || (typeof value === "string" && value.trim().length > 0)
    : typeof value === "string" && value.trim().length > 0;
  return (
    typeof value === "string"
    && value.length <= maxLength
    && hasUsableValue
    && !/[\0\r\n]/.test(value)
  );
}

export function validateOpenVASScanRequest(
  body: unknown,
  defaults: { gvmHost: unknown; gvmPort: unknown; gvmUser: unknown },
): ValidationResult<OpenVASScanRequest> {
  if (!isRecord(body)) {
    return { ok: false, error: "Request body must be a JSON object.", source: "request" };
  }

  const targets = validateScannerTargets(body.targets);
  if (targets.ok === false) return targets;

  const scanConfig = body.scanConfig ?? "full-fast";
  if (typeof scanConfig !== "string" || !OPENVAS_CONFIGS.has(scanConfig)) {
    return {
      ok: false,
      error: "scanConfig must be one of: full-fast, full-fast-ultimate, empty, system-discovery.",
      source: "request",
    };
  }

  for (const field of ["gvmHost", "gvmPort", "gvmUser"]) {
    if (Object.hasOwn(body, field)) {
      return {
        ok: false,
        error: `${field} is server-managed and cannot be supplied by the request.`,
        source: "request",
      };
    }
  }

  const gvmHostRaw = defaults.gvmHost;
  if (!validateHost(gvmHostRaw)) {
    return {
      ok: false,
      error: "gvmHost must be a valid hostname or IP address.",
      source: "configuration",
    };
  }
  const gvmHost = gvmHostRaw.trim();

  const gvmPort = defaults.gvmPort;
  if (typeof gvmPort !== "number" || !Number.isInteger(gvmPort) || gvmPort < 1 || gvmPort > 65_535) {
    return {
      ok: false,
      error: "gvmPort must be an integer between 1 and 65535.",
      source: "configuration",
    };
  }

  const gvmUserRaw = defaults.gvmUser;
  if (!validateSafeString(gvmUserRaw, { maxLength: 256 })) {
    return {
      ok: false,
      error: "gvmUser must be a non-empty string without control characters.",
      source: "configuration",
    };
  }

  const createFindings = body.createFindings ?? false;
  if (typeof createFindings !== "boolean") {
    return {
      ok: false,
      error: "createFindings must be a boolean.",
      source: "request",
    };
  }

  return {
    ok: true,
    value: {
      targets: targets.value,
      scanConfig,
      gvmHost,
      gvmPort,
      gvmUser: gvmUserRaw.trim(),
      createFindings,
    },
  };
}

export function validateNetExecScanRequest(body: unknown): ValidationResult<NetExecScanRequest> {
  if (!isRecord(body)) {
    return { ok: false, error: "Request body must be a JSON object.", source: "request" };
  }

  const targets = validateScannerTargets(body.targets);
  if (targets.ok === false) return targets;

  const domain = body.domain ?? "";
  const username = body.username ?? "";
  const password = body.password ?? "";
  if (!validateSafeString(domain, { maxLength: 255, allowEmpty: true })) {
    return { ok: false, error: "domain is invalid.", source: "request" };
  }
  if (!validateSafeString(username, { maxLength: 256, allowEmpty: true })) {
    return { ok: false, error: "username is invalid.", source: "request" };
  }
  if (!validateSafeString(password, { maxLength: 1_024, allowEmpty: true })) {
    return { ok: false, error: "password is invalid.", source: "request" };
  }
  if (!!username !== !!password) {
    return {
      ok: false,
      error: "username and password must be provided together.",
      source: "request",
    };
  }
  if (domain && !username) {
    return {
      ok: false,
      error: "domain requires username and password.",
      source: "request",
    };
  }

  const checksRaw = body.checks ?? ["smb", "null-session"];
  if (!Array.isArray(checksRaw) || checksRaw.length === 0) {
    return { ok: false, error: "checks must be a non-empty array.", source: "request" };
  }
  if (
    !checksRaw.every((check) => typeof check === "string" && NETEXEC_CHECKS.has(check))
  ) {
    return {
      ok: false,
      error: "checks may only contain: smb, null-session, shares.",
      source: "request",
    };
  }
  const checks = [...new Set(checksRaw)] as NetExecScanRequest["checks"];
  if (checks.includes("shares") && (!username || !password)) {
    return {
      ok: false,
      error: "The shares check requires username and password.",
      source: "request",
    };
  }

  const createFindings = body.createFindings ?? false;
  if (typeof createFindings !== "boolean") {
    return {
      ok: false,
      error: "createFindings must be a boolean.",
      source: "request",
    };
  }

  return {
    ok: true,
    value: {
      targets: targets.value,
      domain: domain.trim(),
      username: username.trim(),
      password,
      checks,
      createFindings,
    },
  };
}
