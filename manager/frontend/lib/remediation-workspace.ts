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

