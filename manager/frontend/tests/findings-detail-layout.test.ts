import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, test } from "node:test";

const findingsPage = readFileSync(
  new URL("../app/findings/page.tsx", import.meta.url),
  "utf8",
);
const portalFindingsPage = readFileSync(
  new URL("../app/portal/findings/page.tsx", import.meta.url),
  "utf8",
);

describe("findings detail layout", () => {
  test("renders the exact shared workspace in the customer portal", () => {
    assert.match(findingsPage, /export function FindingsWorkspace/);
    assert.match(portalFindingsPage, /<FindingsWorkspace surface="portal" \/>/);
    assert.doesNotMatch(portalFindingsPage, /read.only/i);
  });

  test("keeps the desktop detail panel visible and independently scrollable", () => {
    assert.match(findingsPage, /className="finding-detail-column"/);
    assert.match(
      findingsPage,
      /\.finding-detail-column\s*\{[\s\S]*?position:\s*sticky;[^}]*top:\s*var\(--space-3\);[^}]*max-height:\s*calc\(100dvh - 100px\);[^}]*overflow-y:\s*auto;[^}]*overscroll-behavior:\s*contain;/,
    );
  });

  test("recreates the scroll container for each selected finding", () => {
    assert.match(
      findingsPage,
      /<aside key=\{selectedId\}[^>]*className="finding-detail-column"/,
    );
  });

  test("makes the selected detail the primary reading surface", () => {
    assert.match(
      findingsPage,
      /\.findings-workspace\[data-detail="true"\]\s*\{[^}]*grid-template-columns:\s*minmax\(300px, 356px\) minmax\(0, 1fr\);/,
    );
    assert.match(
      findingsPage,
      /\.finding-detail-title\s*\{[^}]*font:\s*700 20px\/1\.32 var\(--font-ui\);/,
    );
    assert.match(
      findingsPage,
      /\.finding-overview-narrative p\s*\{[^}]*max-width:\s*72ch;[^}]*font:\s*400 13\.5px\/1\.65 var\(--font-ui\);/,
    );
  });

  test("keeps the queue focused and progressively explains prioritization", () => {
    assert.match(findingsPage, /<FixFirstStrip/);
    assert.match(findingsPage, /<TriageKey/);
    assert.match(findingsPage, /className="findings-filter-panel"/);
    assert.match(findingsPage, /className="finding-card-metrics"/);
    assert.match(findingsPage, /className="finding-overview-narrative"/);
    assert.match(findingsPage, /className="finding-action-options"/);
  });

  test("refreshes active agents from heartbeats with perceptible feedback", () => {
    assert.match(findingsPage, /const AGENT_REFRESH_FEEDBACK_MS = 2_000;/);
    assert.match(findingsPage, /agentOptionsQuery\.refetch\(\)/);
    assert.match(findingsPage, /agent\.status !== "OFFLINE"/);
    assert.match(findingsPage, /aria-label="Refresh active Vedha agents and probes"/);
    assert.match(findingsPage, /agentsRefreshing \? "Checking agents…" : "Refresh agents"/);
  });

  test("returns the detail panel to document flow on narrow screens", () => {
    assert.match(
      findingsPage,
      /@media \(max-width: 920px\)[\s\S]*?\.finding-detail-column\s*\{[^}]*position:\s*static;[^}]*max-height:\s*none;[^}]*overflow:\s*visible;/,
    );
  });

  test("presents evidence as an analyst review record", () => {
    assert.match(findingsPage, /<h3 id="finding-evidence-title">Evidence review<\/h3>/);
    assert.match(findingsPage, /className="finding-evidence-provenance"/);
    assert.match(findingsPage, /className="finding-evidence-output-heading"/);
    assert.match(findingsPage, /text=\{presentation\.copyText\}[\s\S]*?showLabel/);
    assert.match(findingsPage, /Copy includes all masked lines\./);
    assert.doesNotMatch(findingsPage, /\{false && tab === "evidence"/);
  });
});
