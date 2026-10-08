import { NextResponse } from "next/server";

import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";
import {
  RemediationWorkspaceInputError,
  type RemediationWorkspacePreview,
  type RemediationWorkspacePreviewRequest,
  validateRemediationFindingIds,
} from "../../../../../lib/remediation-workspace";

export const dynamic = "force-dynamic";

const CACHE_HEADERS = { "Cache-Control": "private, no-store" };
const ALLOWED_KEYS = new Set(["finding_ids", "include_advisory"]);

function privateJson(body: unknown, status = 200): Response {
  return NextResponse.json(body, { status, headers: CACHE_HEADERS });
}

function parseBody(value: unknown): RemediationWorkspacePreviewRequest {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new RemediationWorkspaceInputError("Request body must be an object.");
  }
  const body = value as Record<string, unknown>;
  if (Object.keys(body).some((key) => !ALLOWED_KEYS.has(key))) {
    throw new RemediationWorkspaceInputError(
      "Request body may contain only finding_ids and include_advisory.",
    );
  }
  let includeAdvisory = false;
  if (body.include_advisory !== undefined) {
    if (typeof body.include_advisory !== "boolean") {
      throw new RemediationWorkspaceInputError("include_advisory must be a boolean.");
    }
    includeAdvisory = body.include_advisory;
  }
  return {
    finding_ids: validateRemediationFindingIds(body.finding_ids),
    include_advisory: includeAdvisory,
  };
}

/** Authenticated Manager BFF for deterministic, review-only remediation previews. */
export async function POST(request: Request): Promise<Response> {
  const token = bearerFrom(request);
  if (!token) return privateJson({ error: "Not authenticated" }, 401);

  let value: unknown;
  try {
    value = await request.json();
  } catch {
    return privateJson({ error: "Request body must contain valid JSON." }, 400);
  }

  let body: RemediationWorkspacePreviewRequest;
  try {
    body = parseBody(value);
  } catch (error) {
    if (error instanceof RemediationWorkspaceInputError) {
      return privateJson({ error: error.message }, 400);
    }
    return privateJson({ error: "Invalid remediation workspace request." }, 400);
  }

  try {
    const preview = await backend<RemediationWorkspacePreview>(
      "/findings/remediation-workspaces/preview",
      { method: "POST", token, body },
    );
    return privateJson(preview);
  } catch (error) {
    const status = error instanceof BackendError ? error.status : 502;
    return privateJson(
      { error: error instanceof Error ? error.message : "Remediation preview failed" },
      status,
    );
  }
}
