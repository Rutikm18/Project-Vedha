import { fetchJson } from "./fetcher";

export const MAX_REMEDIATION_WORKSPACE_FINDINGS = 20;

export type RemediationOsFamily = "linux" | "windows" | "macos" | "generic";
export type RemediationArtifactFormat = "bash" | "powershell" | "markdown";

export interface RemediationWorkspacePreviewRequest {
  finding_ids: string[];
  include_advisory: boolean;
}

export interface RemediationArtifact {
  artifact_id: string;
  asset_id: string | null;
  os_family: RemediationOsFamily;
  format: RemediationArtifactFormat;
  filename: string;
  finding_ids: string[];
  context_sha256: string;
  content_sha256: string;
  content: string;
}

export interface RemediationBlockedFinding {
  finding_id: string;
  asset_id: string | null;
  code: string;
  detail: string;
}

export interface RemediationAdvisory {
  summary: string;
  notes: string[];
}

export interface RemediationWorkspacePreview {
  engagement_id: string;
  catalog_version: string;
  context_sha256: string;
  generated_at: string;
  review_only: boolean;
  finding_count: number;
  operation_count: number;
  artifacts: RemediationArtifact[];
  blocked: RemediationBlockedFinding[];
  advisory: RemediationAdvisory | null;
  warnings: string[];
}

export interface RemediationWorkspacePreviewOptions {
  includeAdvisory?: boolean;
}

export class RemediationWorkspaceInputError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RemediationWorkspaceInputError";
  }
}

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const EXTENSION: Record<RemediationArtifactFormat, string> = {
  bash: ".sh",
  powershell: ".ps1",
  markdown: ".md",
};

/** Validate the exact selection before either browser or BFF performs I/O. */
export function validateRemediationFindingIds(value: unknown): string[] {
  if (
    !Array.isArray(value)
    || value.length < 1
    || value.length > MAX_REMEDIATION_WORKSPACE_FINDINGS
  ) {
    throw new RemediationWorkspaceInputError(
      `Select between 1 and ${MAX_REMEDIATION_WORKSPACE_FINDINGS} findings.`,
    );
  }

  const ids: string[] = [];
  const unique = new Set<string>();
  for (const candidate of value) {
    if (typeof candidate !== "string" || !UUID.test(candidate)) {
      throw new RemediationWorkspaceInputError("Every finding ID must be a valid UUID.");
    }
    const identity = candidate.toLowerCase();
    if (unique.has(identity)) {
      throw new RemediationWorkspaceInputError("Finding IDs must be unique.");
    }
    unique.add(identity);
    ids.push(candidate);
  }
  return ids;
}

/**
 * Build a review-only workspace from the operator's current finding selection.
 * Auth, wire casing, request validation, and transport errors stay behind this
 * interface so the Findings page only manages selection and presentation.
 */
export async function previewRemediationWorkspace(
  findingIds: readonly string[],
  options: RemediationWorkspacePreviewOptions = {},
): Promise<RemediationWorkspacePreview> {
  if (
    options.includeAdvisory !== undefined
    && typeof options.includeAdvisory !== "boolean"
  ) {
    throw new RemediationWorkspaceInputError("includeAdvisory must be a boolean.");
  }
  const body: RemediationWorkspacePreviewRequest = {
    finding_ids: validateRemediationFindingIds(findingIds),
    include_advisory: options.includeAdvisory ?? false,
  };
  return fetchJson<RemediationWorkspacePreview>(
    "/api/findings/remediation-workspaces/preview",
    { method: "POST", body: JSON.stringify(body) },
  );
}

function safeArtifactFilename(artifact: RemediationArtifact): string {
  const basename = artifact.filename.split(/[\\/]/).pop() ?? "";
  const dot = basename.lastIndexOf(".");
  const rawStem = dot > 0 ? basename.slice(0, dot) : basename;
  const stem = rawStem
    .normalize("NFKC")
    .replace(/[^a-zA-Z0-9._-]+/g, "-")
    .replace(/^[.-]+|[.-]+$/g, "")
    .slice(0, 120);
  return `${stem || `vedha-remediation-${artifact.artifact_id}`}${EXTENSION[artifact.format]}`;
}

/** Download artifact text without interpreting or executing its contents. */
export function downloadRemediationArtifact(artifact: RemediationArtifact): string {
  if (typeof document === "undefined") {
    throw new Error("Remediation artifacts can only be downloaded in a browser.");
  }
  const filename = safeArtifactFilename(artifact);
  const objectUrl = URL.createObjectURL(new Blob(
    [artifact.content],
    { type: "text/plain;charset=utf-8" },
  ));
  const anchor = document.createElement("a");
  anchor.href = objectUrl;
  anchor.download = filename;
  anchor.rel = "noopener";
  anchor.style.display = "none";
  document.body.append(anchor);
  try {
    anchor.click();
  } finally {
    anchor.remove();
    queueMicrotask(() => URL.revokeObjectURL(objectUrl));
  }
  return filename;
}
