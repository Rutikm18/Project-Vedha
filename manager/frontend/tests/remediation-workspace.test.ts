import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";

import {
  downloadRemediationArtifact,
  MAX_REMEDIATION_WORKSPACE_FINDINGS,
  previewRemediationWorkspace,
  type RemediationArtifact,
  type RemediationWorkspacePreview,
  validateRemediationFindingIds,
} from "../lib/remediation-workspace.client";

const originalFetch = globalThis.fetch;
const FINDING_A = "11111111-1111-4111-8111-111111111111";
const FINDING_B = "22222222-2222-4222-8222-222222222222";
const SHA_A = "a".repeat(64);
const SHA_B = "b".repeat(64);

const artifact: RemediationArtifact = {
  artifact_id: "33333333-3333-4333-8333-333333333333",
  asset_id: "44444444-4444-4444-8444-444444444444",
  os_family: "linux",
  format: "bash",
  filename: "../../repair web.sh",
  finding_ids: [FINDING_A, FINDING_B],
  context_sha256: SHA_A,
  content_sha256: SHA_B,
  content: "#!/usr/bin/env bash\necho review-only\n",
};

const preview: RemediationWorkspacePreview = {
  engagement_id: "55555555-5555-4555-8555-555555555555",
  catalog_version: "2026.09.1",
  context_sha256: SHA_A,
  generated_at: "2026-09-27T05:30:00Z",
  review_only: true,
  finding_count: 2,
  operation_count: 1,
  artifacts: [artifact],
  blocked: [],
  advisory: null,
  warnings: [],
};

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe("remediation workspace client module", () => {
  test("validates an exact, unique selection of at most twenty UUIDs", () => {
    assert.deepEqual(validateRemediationFindingIds([FINDING_A, FINDING_B]), [FINDING_A, FINDING_B]);
    assert.throws(() => validateRemediationFindingIds([]), /between 1 and 20/i);
    assert.throws(
      () => validateRemediationFindingIds(Array.from(
        { length: MAX_REMEDIATION_WORKSPACE_FINDINGS + 1 },
        (_, index) => `00000000-0000-4000-8000-${String(index).padStart(12, "0")}`,
      )),
      /between 1 and 20/i,
    );
    assert.throws(() => validateRemediationFindingIds([FINDING_A, FINDING_A]), /unique/i);
    assert.throws(() => validateRemediationFindingIds(["not-a-finding-id"]), /valid UUID/i);
  });

  test("hides the wire contract behind one typed preview operation", async () => {
    let requestedUrl = "";
    let forwardedBody: unknown;
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      forwardedBody = JSON.parse(String(init?.body));
      return new Response(JSON.stringify(preview), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const result = await previewRemediationWorkspace(
      [FINDING_A, FINDING_B],
      { includeAdvisory: true },
    );

    assert.equal(requestedUrl, "/api/findings/remediation-workspaces/preview");
    assert.deepEqual(forwardedBody, {
      finding_ids: [FINDING_A, FINDING_B],
      include_advisory: true,
    });
    assert.deepEqual(result, preview);
  });

  test("downloads inert text with a basename-only, format-correct filename", () => {
    const originalDocument = Object.getOwnPropertyDescriptor(globalThis, "document");
    let clicked = false;
    let appended = false;
    const anchor = {
      download: "",
      href: "",
      rel: "",
      style: { display: "" },
      click() { clicked = true; },
      remove() {},
    };
    Object.defineProperty(globalThis, "document", {
      configurable: true,
      value: {
        createElement: () => anchor,
        body: { append: () => { appended = true; } },
      },
    });

    try {
      downloadRemediationArtifact(artifact);
    } finally {
      if (originalDocument) Object.defineProperty(globalThis, "document", originalDocument);
      else Reflect.deleteProperty(globalThis, "document");
    }

    assert.equal(anchor.download, "repair-web.sh");
    assert.equal(anchor.rel, "noopener");
    assert.equal(appended, true);
    assert.equal(clicked, true);
  });
});
