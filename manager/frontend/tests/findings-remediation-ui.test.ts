import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, test } from "node:test";

const findingsPage = readFileSync(
  new URL("../app/findings/page.tsx", import.meta.url),
  "utf8",
);
const workspaceDialog = readFileSync(
  new URL("../components/findings/RemediationWorkspaceDialog.tsx", import.meta.url),
  "utf8",
);

describe("multi-finding remediation workspace", () => {
  test("keeps batch selection separate from opening finding detail", () => {
    assert.match(findingsPage, /className="finding-card-open"/);
    assert.match(findingsPage, /className="finding-card-checkbox"/);
    assert.match(findingsPage, /type="checkbox"[\s\S]*?onToggleBulk\(f\.id\)/);
    assert.doesNotMatch(findingsPage, /<article[^>]*role="button"/);
  });

  test("bounds the operator selection and keeps it off the portal surface", () => {
    assert.match(findingsPage, /const MAX_BULK_FINDINGS = 20;/);
    assert.match(findingsPage, /bulkSelectable=\{surface === "manager"\}/);
    assert.match(findingsPage, /surface === "manager" && findings\.length > 0/);
  });

  test("routes the exact selection to both the assistant and artifact compiler", () => {
    assert.match(findingsPage, /explainMany\(\[\.\.\.bulkSelectedIds\]\)/);
    assert.match(findingsPage, /previewRemediationWorkspace\(ids, \{ includeAdvisory \}\)/);
    assert.match(findingsPage, /Build remediation files/);
  });

  test("states the execution and AI safety boundary in the review dialog", () => {
    assert.match(workspaceDialog, /Executable bytes come from reviewed templates, not the model\./);
    assert.match(workspaceDialog, /Files start in check mode/);
    assert.match(workspaceDialog, /Vedha has not executed or approved a change\./);
    assert.match(workspaceDialog, /downloadRemediationArtifact\(artifact\)/);
  });
});
