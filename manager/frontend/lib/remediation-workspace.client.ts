"use client";

import { fetchJson } from "./fetcher";
import {
  MAX_REMEDIATION_WORKSPACE_FINDINGS,
  RemediationWorkspaceInputError,
  validateRemediationFindingIds,
  type RemediationAdvisory,
  type RemediationArtifact,
  type RemediationArtifactFormat,
  type RemediationBlockedFinding,
  type RemediationOsFamily,
  type RemediationWorkspacePreview,
  type RemediationWorkspacePreviewOptions,
  type RemediationWorkspacePreviewRequest,
} from "./remediation-workspace";

export {
  MAX_REMEDIATION_WORKSPACE_FINDINGS,
  RemediationWorkspaceInputError,
  validateRemediationFindingIds,
};
export type {
  RemediationAdvisory,
  RemediationArtifact,
  RemediationArtifactFormat,
  RemediationBlockedFinding,
  RemediationOsFamily,
  RemediationWorkspacePreview,
  RemediationWorkspacePreviewOptions,
  RemediationWorkspacePreviewRequest,
};

const EXTENSION: Record<RemediationArtifactFormat, string> = {
  bash: ".sh",
  powershell: ".ps1",
  markdown: ".md",
};

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
