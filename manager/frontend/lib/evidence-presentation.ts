import { redact } from "./report/finding-model";

export interface EvidenceArtifact {
  label: string;
  content: string;
  type?: string;
  tool?: string;
  source?: string;
  command?: string;
  timestamp?: string;
  capturedAt?: string;
  capturedBy?: string;
  sourceHost?: string;
  sha256?: string;
}

export interface EvidenceProvenanceItem {
  label: "Tool" | "Captured" | "Source" | "Operator" | "SHA-256";
  value: string;
  title?: string;
}

export interface EvidencePresentation {
  kind: string;
  copyText: string;
  lines: string[];
  visibleLines: string[];
  truncated: boolean;
  redactions: number;
  command: string | null;
  provenance: EvidenceProvenanceItem[];
}

const INLINE_LINE_LIMIT = 200;

function stableTimestamp(value: string): string {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString().replace("T", " ").replace(/\.\d{3}Z$/, " UTC");
}

function provenanceOf(artifact: EvidenceArtifact): EvidenceProvenanceItem[] {
  const items: EvidenceProvenanceItem[] = [];
  const tool = artifact.tool?.trim() || artifact.source?.trim();
  const capturedAt = artifact.capturedAt?.trim() || artifact.timestamp?.trim();
  const sha256 = artifact.sha256?.trim();

  if (tool) items.push({ label: "Tool", value: tool });
  if (capturedAt) items.push({ label: "Captured", value: stableTimestamp(capturedAt), title: capturedAt });
  if (artifact.sourceHost?.trim()) items.push({ label: "Source", value: artifact.sourceHost.trim() });
  if (artifact.capturedBy?.trim()) items.push({ label: "Operator", value: artifact.capturedBy.trim() });
  if (sha256) {
    items.push({
      label: "SHA-256",
      value: sha256.length > 18 ? `${sha256.slice(0, 12)}…${sha256.slice(-6)}` : sha256,
      title: sha256,
    });
  }
  return items;
}

function evidenceKind(artifact: EvidenceArtifact, content: string): string {
  const declared = artifact.type?.trim();
  if (declared) return declared.slice(0, 24).toUpperCase();

  const hint = `${artifact.label} ${content.slice(0, 120)}`.toLowerCase();
  if (/command|stdout|stderr|terminal|scan|nmap|curl|powershell|shell/.test(hint)) return "OUTPUT";
  if (/log|event|trace/.test(hint)) return "LOG";
  return "TEXT";
}

export function presentEvidence(artifact: EvidenceArtifact): EvidencePresentation {
  const source = artifact.content ?? "";
  let formatted = source;
  let kind = evidenceKind(artifact, source);

  if (source.length <= 100_000) {
    try {
      formatted = JSON.stringify(JSON.parse(source), null, 2);
      kind = "JSON";
    } catch {
      // Scanner and terminal output is intentionally retained verbatim.
    }
  }

  const output = redact(formatted);
  const command = artifact.command?.trim() ? redact(artifact.command.trim()) : null;
  const lines = output.text ? output.text.split("\n") : [];
  const visibleLines = lines.slice(0, INLINE_LINE_LIMIT);

  return {
    kind,
    copyText: output.text,
    lines,
    visibleLines,
    truncated: lines.length > visibleLines.length,
    redactions: output.total + (command?.total ?? 0),
    command: command?.text ?? null,
    provenance: provenanceOf(artifact),
  };
}
