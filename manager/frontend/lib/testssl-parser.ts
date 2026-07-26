import type { LiveFinding, Severity } from './engine/types';
import { generateFindingId } from './finding-id';

export type TestsslIssue = {
  id: string;
  severity: string;
  finding: string;
  cve?: string;
  cwe?: string;
};

const SKIP_SEVERITY = new Set(['OK', 'INFO', 'DEBUG']);

function mapSeverity(raw: string): Severity {
  switch (raw.toUpperCase()) {
    case 'CRITICAL': return 'CRITICAL';
    case 'HIGH':
    case 'WARN':     return 'HIGH';
    case 'MEDIUM':   return 'MEDIUM';
    case 'LOW':      return 'LOW';
    default:         return 'INFO';
  }
}

// Backwards-compat shims for pre-refactor dashboard routes
export type TestsslOutput = { findings: TestsslIssue[] } | TestsslIssue[];

export interface TestsslParseResult {
  findings: LiveFinding[];
  invalidEntries: number;
  totalEntries: number;
}

export function parseTestsslOutput(
  data: TestsslOutput | string,
  host: string,
  port = 443,
): LiveFinding[] {
  if (typeof data === 'string') return parseTestsslJson(data, host, port);
  const issues = Array.isArray(data) ? data : (data as { findings: TestsslIssue[] }).findings ?? [];
  return parseTestsslJson(JSON.stringify(issues), host, port);
}

export function parseTestsslJson(
  jsonContent: string,
  host: string,
  port: number,
): LiveFinding[] {
  try {
    return parseTestsslJsonChecked(jsonContent, host, port).findings;
  } catch {
    return [];
  }
}

export function parseTestsslJsonChecked(
  jsonContent: string,
  host: string,
  port: number,
): TestsslParseResult {
  if (!jsonContent || !jsonContent.trim()) {
    throw new Error('testssl produced an empty JSON report');
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(jsonContent);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(`testssl produced invalid JSON: ${detail}`);
  }

  let rawIssues: unknown[];
  if (Array.isArray(parsed)) {
    rawIssues = parsed;
  } else if (
    parsed
    && typeof parsed === 'object'
    && Array.isArray((parsed as { findings?: unknown }).findings)
  ) {
    rawIssues = (parsed as { findings: unknown[] }).findings;
  } else {
    throw new Error('testssl JSON report has an unsupported schema');
  }

  const findings: LiveFinding[] = [];
  const now = new Date().toISOString();
  let invalidEntries = 0;

  for (const rawIssue of rawIssues) {
    if (
      !rawIssue
      || typeof rawIssue !== 'object'
      || typeof (rawIssue as TestsslIssue).id !== 'string'
      || typeof (rawIssue as TestsslIssue).severity !== 'string'
      || typeof (rawIssue as TestsslIssue).finding !== 'string'
    ) {
      invalidEntries += 1;
      continue;
    }

    const issue = rawIssue as TestsslIssue;
    if (SKIP_SEVERITY.has(issue.severity.toUpperCase())) continue;

    const severity = mapSeverity(issue.severity);
    const title    = `${issue.id}: ${issue.finding.slice(0, 60)}`;

    findings.push({
      id:        generateFindingId(severity),
      title,
      severity,
      host,
      port,
      evidence:  [{ label: 'testssl output', content: issue.finding, timestamp: now }],
      source:    'testssl',
      cveIds:    issue.cve ? [issue.cve] : [],
      status:    'OPEN',
      timestamp: now,
    });
  }

  return { findings, invalidEntries, totalEntries: rawIssues.length };
}
