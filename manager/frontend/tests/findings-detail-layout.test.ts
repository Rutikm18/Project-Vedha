import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, test } from "node:test";

const findingsPage = readFileSync(
  new URL("../app/findings/page.tsx", import.meta.url),
  "utf8",
);

describe("findings detail layout", () => {
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
      /key=\{selected\.id\}\s+className="finding-detail-column"/,
    );
  });

  test("makes the selected detail the primary reading surface", () => {
    assert.match(
      findingsPage,
      /\.findings-workspace\[data-detail="true"\]\s*\{[^}]*grid-template-columns:\s*minmax\(288px, 332px\) minmax\(0, 1fr\);/,
    );
    assert.match(
      findingsPage,
      /\.finding-detail-title\s*\{[^}]*font:\s*700 20px\/1\.35 var\(--font-ui\);/,
    );
    assert.match(
      findingsPage,
      /\.finding-overview-primary p,[\s\S]*?\.finding-overview-technical-narrative p\s*\{[^}]*max-width:\s*72ch;[^}]*font:\s*400 14px\/1\.65 var\(--font-ui\);/,
    );
  });

  test("keeps the queue compact and progressively reveals secondary analysis", () => {
    assert.doesNotMatch(findingsPage, /<FixFirstStrip/);
    assert.doesNotMatch(findingsPage, /<TriageKey/);
    assert.match(findingsPage, /<details className="findings-advanced-filters">/);
    assert.match(findingsPage, /className="finding-card-meta"/);
    assert.match(findingsPage, /<details className="finding-overview-disclosure">/);
    assert.match(findingsPage, /className="finding-action-select"/);
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
    assert.match(findingsPage, /text=\{presentation\.copyText\} showLabel/);
    assert.match(findingsPage, /Copy includes all masked lines\./);
    assert.doesNotMatch(findingsPage, /\{false && tab === "evidence"/);
  });
});
