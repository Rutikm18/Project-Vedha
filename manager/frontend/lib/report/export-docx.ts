/**
 * Word (DOCX) security report — the same document as the PDF, built from the
 * shared presentation layer, as editable Word with real styles: Title,
 * Heading 1–3 (so the navigation pane and contents work), a table style, code
 * and note paragraphs, a contents field, and a running header and footer.
 */
import {
  BRAND_HEX,
  METHOD_FIELDS,
  SEVERITY_DEFINITIONS,
  SEVERITY_HEX,
  SEVERITY_LABEL,
  assetLabel,
  closureView,
  evidenceView,
  excerpt,
  findingNarrative,
  findingRefs,
  formatDate,
  formatDateTime,
  gapInventory,
  groupAssets,
  groupRef,
  humanize,
  isIssued,
  isOpenStatus,
  issueGroups,
  executiveNarrative,
  issueFacts,
  keyMetrics,
  statusSummary,
  priorityLines,
  mask,
  maskedText,
  metadataText,
  orderFindings,
  overallRating,
  remediationRoadmap,
  remediationView,
  severityRows,
  sharedNarrativeKeys,
  statusLabel,
  statusRows,
  topRisks,
  usableTimeZone,
  compactRefs,
  type IssueGroup,
  type Readable,
  type SeverityKey,
} from "./presentation";
import type { ReportDocument, ReportEvidence, ReportFinding } from "./report-document";
import { zip } from "./zip";

// A4 with 2 cm margins, in twentieths of a point.
const PAGE_W = 11906;
const PAGE_H = 16838;
const MARGIN = 1134;
const CONTENT = PAGE_W - MARGIN * 2;
const FONT = "Calibri";
const MONO = "Consolas";
const ASSET_GRID_AFTER = 20;
const EVIDENCE_LINES = 28;

const hex = (color: string) => color.replace("#", "").toUpperCase();

// ─── XML primitives ──────────────────────────────────────────────────────────

function esc(value: unknown): string {
  return mask(String(value ?? ""))
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

interface RunStyle { bold?: boolean; italic?: boolean; color?: string; size?: number; font?: string; caps?: boolean; spacing?: number }

/** A run; newlines become line breaks. Every string is masked on the way in. */
function run(text: string, s: RunStyle = {}): string {
  const props = [
    s.font ? `<w:rFonts w:ascii="${s.font}" w:hAnsi="${s.font}" w:cs="${s.font}"/>` : "",
    s.bold ? "<w:b/>" : "",
    s.italic ? "<w:i/>" : "",
    s.caps ? "<w:caps/>" : "",
    s.color ? `<w:color w:val="${hex(s.color)}"/>` : "",
    s.spacing ? `<w:spacing w:val="${s.spacing}"/>` : "",
    s.size ? `<w:sz w:val="${Math.round(s.size * 2)}"/><w:szCs w:val="${Math.round(s.size * 2)}"/>` : "",
  ].join("");
  const parts = String(text).split("\n").map((line) => `<w:t xml:space="preserve">${esc(line)}</w:t>`);
  return `<w:r>${props ? `<w:rPr>${props}</w:rPr>` : ""}${parts.join("<w:br/>")}</w:r>`;
}

interface ParaStyle {
  style?: string;
  align?: "left" | "center" | "right" | "both";
  before?: number;
  after?: number;
  keepNext?: boolean;
  pageBreakBefore?: boolean;
  shade?: string;
  numId?: number;
  indent?: number;
}

function para(content: string, p: ParaStyle = {}): string {
  const props = [
    p.style ? `<w:pStyle w:val="${p.style}"/>` : "",
    p.keepNext ? "<w:keepNext/>" : "",
    p.pageBreakBefore ? "<w:pageBreakBefore/>" : "",
    p.numId ? `<w:numPr><w:ilvl w:val="0"/><w:numId w:val="${p.numId}"/></w:numPr>` : "",
    p.shade ? `<w:shd w:val="clear" w:color="auto" w:fill="${hex(p.shade)}"/>` : "",
    p.before !== undefined || p.after !== undefined ? `<w:spacing${p.before !== undefined ? ` w:before="${p.before}"` : ""}${p.after !== undefined ? ` w:after="${p.after}"` : ""}/>` : "",
    p.indent ? `<w:ind w:left="${p.indent}"/>` : "",
    p.align ? `<w:jc w:val="${p.align}"/>` : "",
  ].join("");
  return `<w:p>${props ? `<w:pPr>${props}</w:pPr>` : ""}${content}</w:p>`;
}

const text = (value: string, s?: RunStyle, p?: ParaStyle) => para(run(value, s), p);

interface Cell {
  content: string;
  fill?: string;
  width?: number;
  span?: number;
}

function cellXml(cell: Cell, width: number, margins = 80): string {
  return `<w:tc><w:tcPr><w:tcW w:w="${width}" w:type="dxa"/>${cell.span && cell.span > 1 ? `<w:gridSpan w:val="${cell.span}"/>` : ""}${cell.fill ? `<w:shd w:val="clear" w:color="auto" w:fill="${hex(cell.fill)}"/>` : ""}<w:tcMar><w:top w:w="${margins}" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="${margins}" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar><w:vAlign w:val="center"/></w:tcPr>${cell.content || "<w:p/>"}</w:tc>`;
}

/** A table in the report's table style. `widths` are relative. */
function table(headers: string[] | null, widths: number[], rows: Cell[][], opts: { style?: string; total?: number; noBorders?: boolean } = {}): string {
  const total = opts.total ?? CONTENT;
  const sum = widths.reduce((a, b) => a + b, 0);
  const cols = widths.map((w) => Math.round((w / sum) * total));
  const grid = `<w:tblGrid>${cols.map((w) => `<w:gridCol w:w="${w}"/>`).join("")}</w:tblGrid>`;
  const header = headers
    ? `<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>${headers.map((h, i) => cellXml({ content: text(h, { bold: true, color: "#FFFFFF", size: 7.5, caps: true }, { after: 0 }), fill: BRAND_HEX.navy }, cols[i]!)).join("")}</w:tr>`
    : "";
  const body = rows.map((row) => {
    let col = 0;
    const cells = row.map((cell) => {
      const span = cell.span ?? 1;
      const width = cols.slice(col, col + span).reduce((a, b) => a + b, 0);
      col += span;
      return cellXml(cell, width);
    }).join("");
    return `<w:tr><w:trPr><w:cantSplit/></w:trPr>${cells}</w:tr>`;
  }).join("");
  const borders = opts.noBorders
    ? `<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>`
    : "";
  return `<w:tbl><w:tblPr><w:tblStyle w:val="${opts.style ?? "VedhaTable"}"/><w:tblW w:w="${total}" w:type="dxa"/><w:tblLayout w:type="fixed"/>${borders}<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>${grid}${header}${body}</w:tbl>${para("", { after: 120 })}`;
}

const cellText = (value: string, s: RunStyle = {}): Cell => ({ content: text(value || "—", { size: 9, ...s }, { after: 0 }) });

function pillCell(severity: SeverityKey | "none", label?: string): Cell {
  const color = severity === "none" ? BRAND_HEX.ok : SEVERITY_HEX[severity].fg;
  return { content: text((label ?? (severity === "none" ? "None" : SEVERITY_LABEL[severity])).toUpperCase(), { bold: true, color: "#FFFFFF", size: 7.5 }, { after: 0, align: "center" }), fill: color };
}

// ─── Document builder ────────────────────────────────────────────────────────

class Doc {
  private parts: string[] = [];
  /** Numbered lists each need their own numbering instance to restart at 1. */
  numbered = 0;
  readonly headings: Array<{ title: string; level: number }> = [];

  add(xml: string): void { this.parts.push(xml); }
  get xml(): string { return this.parts.join(""); }

  h1(title: string, newPage = true): void {
    this.headings.push({ title, level: 1 });
    this.add(text(title, {}, { style: "Heading1", pageBreakBefore: newPage }));
  }
  h2(title: string): void {
    this.headings.push({ title, level: 2 });
    this.add(text(title, {}, { style: "Heading2" }));
  }
  h3(title: string): void { this.add(text(title, {}, { style: "Heading3" })); }

  p(value: string, s: RunStyle = {}, p: ParaStyle = {}): void { this.add(text(value, s, p)); }
  muted(value: string): void { this.add(text(value, { italic: true, color: BRAND_HEX.muted, size: 8.5 })); }
  note(value: string, tone: "muted" | "caution" | "info" = "muted"): void {
    this.add(text(value, { size: 9, color: tone === "caution" ? "#8A5300" : tone === "info" ? BRAND_HEX.navy : BRAND_HEX.muted }, { style: tone === "caution" ? "NoteCaution" : "Note" }));
  }

  bullets(items: string[]): void {
    for (const item of items) this.add(text(item, {}, { style: "ListParagraph", numId: 1 }));
  }
  numberedList(items: string[]): void {
    this.numbered += 1;
    const numId = 100 + this.numbered;
    for (const item of items) this.add(text(item, {}, { style: "ListParagraph", numId }));
  }
  readable(body: Readable): void {
    if (body.kind === "text") body.paragraphs.forEach((p) => this.p(p));
    else if (body.kind === "list") this.bullets(body.items);
    else this.keyValues(body.rows.map(([label, value]) => ({ label, value })), 2);
  }
  code(value: string): void {
    this.add(value.split("\n").map((line) => text(line || " ", { font: MONO, size: 8 }, { style: "Code" })).join(""));
  }

  keyValues(rows: Array<{ label: string; value: string; mono?: boolean }>, cols = 2): void {
    if (!rows.length) return;
    const out: Cell[][] = [];
    for (let i = 0; i < rows.length; i += cols) {
      const slice = rows.slice(i, i + cols);
      out.push(Array.from({ length: cols }, (_, j) => {
        const r = slice[j];
        if (!r) return { content: "<w:p/>" };
        return { content: text(r.label, { size: 7, color: BRAND_HEX.muted, bold: true, caps: true }, { after: 20 }) + text(r.value, { size: 9.5, font: r.mono ? MONO : undefined }, { after: 0 }) };
      }));
    }
    this.add(table(null, Array(cols).fill(1), out, { style: "VedhaGrid", noBorders: true }));
  }
}

// ─── Sections ────────────────────────────────────────────────────────────────

interface Ctx {
  D: Doc;
  report: ReportDocument;
  tz: string;
  refs: Map<string, string>;
  ordered: ReportFinding[];
  groups: IssueGroup[];
  issued: boolean;
}

const dash = (value: string | null | undefined) => (value && value.trim() ? value : "—");
const plain = (value: unknown) => maskedText(value) ?? "";

function cover({ D, report, tz, issued }: Ctx): void {
  const meta = (k: string) => metadataText(report, k);
  const band =
    text("VEDHA   SECURITY ASSESSMENT", { bold: true, color: "#9DB2D6", size: 8.5, spacing: 20 }, { after: 900 }) +
    text("Vulnerability Assessment Report", { bold: true, color: "#FFFFFF", size: 26 }, { after: 120 }) +
    text(report.engagement.name, { color: "#D6E0F2", size: 15 }, { after: 80 }) +
    text(report.engagement.client ? `Prepared for ${plain(report.engagement.client)}` : "Client not recorded", { color: "#9DB2D6", size: 10.5 }, { after: issued ? 600 : 240 }) +
    (issued ? "" : text("DRAFT / NOT APPROVED — HUMAN REVIEW REQUIRED", { bold: true, color: "#FCD34D", size: 8.5 }, { after: 240 }));
  D.add(table(null, [1], [[{ content: band, fill: BRAND_HEX.navy }]], { style: "VedhaGrid", noBorders: true }));

  const rating = overallRating(report);
  const color = rating.level === "none" ? BRAND_HEX.ok : SEVERITY_HEX[rating.level].fg;
  D.add(table(null, [1, 2.4], [[
    { content: text("OVERALL RISK", { bold: true, size: 7, color: BRAND_HEX.muted }, { after: 40 }) + text(rating.label, { bold: true, size: 20, color }, { after: 0 }), fill: BRAND_HEX.wash },
    { content: text(rating.basis, { size: 9.5 }, { after: 60 }) + text("Rating method: highest severity among open findings.", { size: 7.5, color: BRAND_HEX.muted }, { after: 0 }), fill: BRAND_HEX.wash },
  ]], { style: "VedhaGrid", noBorders: true }));

  const rows = severityRows(report);
  D.add(table(null, [1, 1, 1, 1, 1], [rows.map((r) => ({
    content: text(String(r.open), { bold: true, size: 18, color: SEVERITY_HEX[r.severity].fg }, { after: 0 }) +
      text(`${SEVERITY_LABEL[r.severity]} open`, { bold: true, size: 8 }, { after: 0 }) +
      text(`${r.total} recorded`, { size: 7, color: BRAND_HEX.muted }, { after: 0 }),
    fill: SEVERITY_HEX[r.severity].bg,
  }))], { style: "VedhaGrid", noBorders: true }));

  const period = meta("reporting_period")
    ?? ([formatDate(report.engagement.start_time, tz), formatDate(report.engagement.end_time, tz)].filter(Boolean).join(" – ") || null);
  D.keyValues([
    { label: "Client", value: dash(plain(report.engagement.client)) },
    { label: "Assessment period", value: dash(period) },
    { label: "Report version", value: dash(meta("version")) },
    { label: "Issue date", value: dash(formatDate(meta("issue_date"), tz)) },
    { label: "Classification", value: dash(meta("classification")) },
    { label: "Document status", value: dash(meta("document_status") ?? (issued ? "Issued" : "Draft")) },
    { label: "Prepared by", value: dash(meta("prepared_by") ?? plain(report.engagement.assessor)) },
    { label: "Generated", value: dash(formatDateTime(report.document.generated_at, tz)) },
  ], 2);
  D.muted(`${meta("classification") ?? "Confidential"}. This report contains security-sensitive information about ${plain(report.engagement.client) || "the client"}'s systems. Distribute only to the named recipients.`);
}

function documentControl({ D, report, tz }: Ctx): void {
  D.h1("Document control");
  const meta = (k: string) => metadataText(report, k);
  const rows: Array<[string, string | null]> = [
    ["Report version", meta("version")], ["Document status", meta("document_status")], ["Classification", meta("classification")],
    ["Prepared by", meta("prepared_by")], ["Prepared at", formatDateTime(meta("prepared_at"), tz)],
    ["Reviewed by", meta("reviewed_by")], ["Reviewed at", formatDateTime(meta("reviewed_at"), tz)],
    ["Approved by", meta("approved_by")], ["Approved at", formatDateTime(meta("approved_at"), tz)],
    ["Issue date", formatDateTime(meta("issue_date"), tz)], ["Reporting period", meta("reporting_period")], ["Distribution", meta("distribution")],
  ];
  const recorded = rows.filter(([, v]) => v);
  if (recorded.length) D.add(table(["Field", "Recorded value"], [1, 2.4], recorded.map(([k, v]) => [cellText(k, { bold: true }), cellText(v!)])));
  else D.note("No document-control metadata is recorded for this engagement.");
  const missing = rows.filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) D.note(`Not recorded: ${missing.join(", ")}.`);
  D.add(text("Contents", {}, { style: "Heading2" }));
  D.add("__TOC__");
}

function executiveSummary({ D, report, tz, refs }: Ctx): void {
  D.h1("1  Executive summary");
  const m = keyMetrics(report);
  const rows = severityRows(report);
  const narrative = executiveNarrative(report, tz);
  narrative.sentences.forEach((line, i) => D.p(line, { bold: i === narrative.ratingIndex }));

  const tiles: Array<[string, number, string]> = [
    ["Open findings", m.open, BRAND_HEX.navy],
    ["Critical and high open", m.criticalHighOpen, m.criticalHighOpen ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok],
    ["Past SLA deadline", m.slaBreached, m.slaBreached ? SEVERITY_HEX.high.fg : BRAND_HEX.ok],
    ["Assets with open findings", m.assetsAffected, BRAND_HEX.navy],
  ];
  D.add(table(null, [1, 1, 1, 1], [tiles.map(([label, value, color]) => ({
    content: text(String(value), { bold: true, size: 20, color }, { after: 0 }) + text(label, { size: 8, color: BRAND_HEX.muted }, { after: 0 }),
    fill: BRAND_HEX.wash,
  }))], { style: "VedhaGrid", noBorders: true }));

  D.h3("Findings by severity");
  const max = Math.max(1, ...rows.map((r) => r.total));
  const barTotal = Math.round(CONTENT * 0.55);
  D.add(table(null, [1.1, 3.6, 1.3], rows.map((r) => {
    const openW = Math.round((r.open / max) * barTotal);
    const closedW = Math.round((r.closed / max) * barTotal);
    const restW = Math.max(barTotal - openW - closedW, 0);
    const segments = [
      openW ? { content: "<w:p/>", fill: SEVERITY_HEX[r.severity].fg, width: openW } : null,
      closedW ? { content: "<w:p/>", fill: SEVERITY_HEX[r.severity].bg, width: closedW } : null,
      restW ? { content: "<w:p/>", fill: "#F1F3F6", width: restW } : null,
    ].filter((x): x is { content: string; fill: string; width: number } => x !== null);
    const bar = `<w:tbl><w:tblPr><w:tblW w:w="${barTotal}" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${segments.map((s) => `<w:gridCol w:w="${s.width}"/>`).join("")}</w:tblGrid><w:tr><w:trPr><w:trHeight w:val="200" w:hRule="exact"/></w:trPr>${segments.map((s) => `<w:tc><w:tcPr><w:tcW w:w="${s.width}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="${hex(s.fill!)}"/></w:tcPr><w:p><w:pPr><w:spacing w:after="0" w:line="40" w:lineRule="exact"/></w:pPr></w:p></w:tc>`).join("")}</w:tr></w:tbl><w:p><w:pPr><w:spacing w:after="0" w:line="20" w:lineRule="exact"/></w:pPr></w:p>`;
    return [cellText(SEVERITY_LABEL[r.severity], { bold: true }), { content: bar }, cellText(`${r.open} open · ${r.total} total`, { color: BRAND_HEX.muted, size: 8 })];
  }), { style: "VedhaGrid", noBorders: true }));
  D.muted("Dark: open or confirmed. Light: remediated, risk accepted or false positive.");

  const statuses = statusRows(report);
  if (statuses.length) {
    D.h3("Findings by status");
    D.add(table(statuses.map((s) => s.label), statuses.map(() => 1), [statuses.map((s) => cellText(String(s.count), { bold: true, size: 12 }))]));
  }

  D.h3("Top open risks");
  const top = topRisks(report, 5);
  if (top.length) {
    D.add(table(["Ref", "Finding", "Severity", "Assets", "Fix by"], [0.8, 2.8, 0.95, 1.4, 1], top.map(({ ref, group }) => {
      const live = group.findings.filter((f) => isOpenStatus(f.status));
      const earliest = live.map((f) => f.current_sla.deadline).filter((d): d is string => Boolean(d)).sort()[0];
      return [cellText(ref, { bold: true }), cellText(group.title), pillCell(group.severity), cellText(dash(groupAssets(live))), cellText(dash(formatDate(earliest, tz)))];
    })));
  } else {
    D.note("No findings are open.", "info");
  }

  const roadmap = remediationRoadmap(report);
  if (roadmap.length) {
    D.h3("Recommended priorities");
    D.bullets(priorityLines(report));
  }
  void refs;
}

function scopeAndMethod({ D, report, tz }: Ctx): void {
  D.h1("2  Scope and methodology");
  const e = report.engagement;
  D.h3("Assessment scope");
  D.keyValues([
    { label: "In scope", value: dash(e.scope_cidrs.join(", ")) },
    { label: "Excluded", value: dash(e.excluded_cidrs.join(", ")) },
    { label: "Assessment window", value: dash([formatDateTime(e.start_time, tz), formatDateTime(e.end_time, tz)].filter(Boolean).join(" – ")) },
    { label: "Lead assessor", value: dash(plain(e.assessor)) },
    { label: "Engagement status", value: humanize(e.status) },
    { label: "Tags", value: dash(e.tags.join(", ")) },
  ], 2);
  const description = maskedText(e.description);
  if (description) { D.h3("Engagement description"); D.p(description); }
  if (e.regulatory_profiles.length) {
    D.h3("Selected regulatory profiles");
    D.bullets(e.regulatory_profiles.map((p) => [p.name, p.version, p.jurisdiction].filter(Boolean).join(" · ") || "Profile name not recorded"));
  }
  const missing: string[] = [];
  for (const [key, title] of METHOD_FIELDS) {
    const value = metadataText(report, key);
    if (!value) { missing.push(title.toLowerCase()); continue; }
    D.h3(title);
    D.p(value);
  }
  if (missing.length) D.note(`Not recorded in the report metadata: ${missing.join(", ")}. Absence of a recorded limitation does not establish that the assessment had none.`);
}


function findingsOverview({ D, ordered, groups, refs }: Ctx): void {
  D.h1("3  Findings overview");
  const repeated = groups.length < ordered.length;
  D.muted(`${ordered.length} finding${ordered.length === 1 ? "" : "s"}${repeated ? ` across ${groups.length} distinct issues` : ""}, most severe first.${repeated ? " An issue found on several assets is listed once, with its range of references." : ""}`);
  if (!groups.length) { D.note("No findings are recorded for this engagement."); return; }
  D.add(table(["Ref", "Finding", "Severity", "CVSS", "Assets", "Status"], [0.8, 2.8, 0.95, 0.55, 1.3, 1.2], groups.map((g) => {
    const cvss = [...new Set(g.findings.map((f) => f.cvss_score).filter((v) => v !== null && v !== "").map(String))];
    return [
      cellText(groupRef(g, refs), { bold: true }),
      cellText(g.title),
      pillCell(g.severity),
      cellText(cvss.length === 0 ? "—" : cvss.length === 1 ? cvss[0]! : "varies"),
      cellText(dash(groupAssets(g.findings))),
      cellText(statusSummary(g.findings), { bold: true, color: g.open ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok }),
    ];
  })));
}

function evidence(D: Doc, ev: ReportEvidence, prefix: string, tz: string, maxLines = EVIDENCE_LINES): void {
  for (const artifact of ev.artifacts) {
    const view = evidenceView(artifact, `${prefix}/E${String(artifact.index).padStart(2, "0")}`);
    D.p([view.ref, view.label, view.tool, formatDateTime(view.capturedAt, tz)].filter(Boolean).join(" · "), { bold: true, size: 8.5, color: BRAND_HEX.navy }, { keepNext: true, after: 40 });
    if (view.command) D.code(`$ ${view.command}`);
    const cut = excerpt(view.content || "No evidence content recorded.", maxLines);
    D.code(cut.text);
    const notes = [
      cut.truncated ? `Excerpt: ${cut.shownLines} of ${cut.totalLines} lines. The complete masked evidence is in the Excel workbook (Evidence sheet).` : null,
      view.sha256 ? `SHA-256 ${view.sha256}${view.verified === true ? " (verified)" : view.verified === false ? " (not verified)" : ""}` : null,
    ].filter(Boolean).join("  ·  ");
    if (notes) D.muted(notes);
  }
}

function findingSection(ctx: Ctx, group: IssueGroup): void {
  const { D, tz, refs } = ctx;
  const f = group.lead;
  const many = group.findings.length > 1;
  const ref = refs.get(f.id) ?? "";
  const headRef = many ? groupRef(group, refs) : ref;
  const sev = group.severity;
  const color = SEVERITY_HEX[sev];

  D.headings.push({ title: `${headRef}  ${f.title}`, level: 2 });
  const statusText = many ? `${group.findings.length} affected assets · ${statusSummary(group.findings)}` : statusLabel(f.status);
  D.add(table(null, [0.022, 1], [[
    { content: "<w:p/>", fill: color.fg },
    {
      content: para(run(`${headRef}   `, { bold: true, color: color.fg, size: 9 }) + run(` ${SEVERITY_LABEL[sev].toUpperCase()} `, { bold: true, color: color.fg, size: 8 }) + run(`   ${statusText}`, { color: group.open ? color.fg : BRAND_HEX.ok, size: 8.5 }), { after: 40, keepNext: true }) +
        para(run(f.title, { bold: true, size: 14, color: BRAND_HEX.ink }), { style: "Heading2", after: 0, before: 0 }),
      fill: color.bg,
    },
  ]], { style: "VedhaGrid", noBorders: true }));

  const facts = issueFacts(group, tz).map((x) => (x.label === "Affected assets" ? { ...x, value: `${x.value} (listed below)` } : x));
  D.keyValues(facts.map((x) => ({ label: x.label, value: x.value, mono: x.label === "CVSS vector" })), 3);

  const narrative = findingNarrative(f);
  const shared = many ? sharedNarrativeKeys(group) : null;
  for (const section of narrative.sections) {
    D.h3(section.title);
    if (shared && !shared.has(section.key)) D.muted(`As recorded for ${ref}; other instances record this differently (see the Excel workbook).`);
    D.readable(section.body);
  }

  if (f.evidence.artifacts.length) {
    D.h3(many ? `Evidence (representative, from ${ref})` : "Evidence");
    evidence(D, f.evidence, ref, tz);
  }

  const rem = remediationView(f);
  if (rem.text || rem.plans.length || rem.recommendations.length) {
    D.h3("Remediation");
    if (rem.text) D.p(rem.text);
    for (const plan of rem.plans) {
      if (plan.summary) D.p(`Reviewed plan: ${plan.summary}${plan.effort ? ` (effort: ${plan.effort})` : ""}`, { bold: true });
      if (plan.steps.length) D.numberedList(plan.steps);
      if (plan.verification.length) { D.p("Verify the fix:", { bold: true, size: 9 }); D.bullets(plan.verification); }
      if (plan.longTerm.length) { D.p("Longer term:", { bold: true, size: 9 }); D.bullets(plan.longTerm); }
      if (plan.compensating) D.p(`Compensating controls: ${plan.compensating}`);
    }
    if (rem.recommendations.length) { D.p("Recommendations:", { bold: true, size: 9 }); D.bullets(rem.recommendations); }
  }

  const c = closureView(f);
  if (!many && (c.closed || c.retest || c.reopened)) {
    D.h3("Closure and retest");
    D.keyValues([
      { label: "Disposition", value: c.disposition },
      ...(c.resolvedAt ? [{ label: "Resolved", value: formatDate(c.resolvedAt, tz)! }] : []),
      ...(c.method ? [{ label: "Method", value: c.method }] : []),
      ...(c.reviewedBy ? [{ label: "Reviewed by", value: c.reviewedBy }] : []),
      ...(c.retest ? [{ label: "Retest", value: `${c.retest}${c.retestAt ? `, ${formatDate(c.retestAt, tz)}` : ""}` }] : []),
      ...(c.reopened ? [{ label: "Reopened", value: `${c.reopened} time${c.reopened === 1 ? "" : "s"}` }] : []),
    ], 3);
    const retest = f.closure.retest;
    if (retest) {
      const pairs: Array<[string, unknown]> = [
        ["Retest method", retest.method], ["Vantage point", retest.vantage_point], ["Expected result", retest.expected_result],
        ["Retest actual result", retest.actual_result], ["Change reference", retest.change_reference], ["Residual risk", retest.residual_risk],
      ];
      D.keyValues(pairs.map(([k, v]) => ({ label: k, value: plain(typeof v === "string" ? v : v == null ? null : JSON.stringify(v)) })).filter((x) => x.value), 2);
      if (retest.integrity_status !== "verified") {
        D.note(`Retest evidence integrity: ${humanize(retest.integrity_status)}${retest.integrity_gaps.length ? ` (${retest.integrity_gaps.join(", ")})` : ""}.`, "caution");
      }
      evidence(D, retest.before_evidence, `${ref}/RETEST/BEFORE`, tz, 8);
      evidence(D, retest.after_evidence, `${ref}/RETEST/AFTER`, tz, 8);
    }
    evidence(D, f.closure.recorded_closure_evidence, `${ref}/CLOSE`, tz, 8);
  }

  if (f.compliance_mappings.length) {
    D.h3("Recorded compliance mappings");
    D.bullets(f.compliance_mappings.map((m) => [
      [m.framework, m.framework_version].filter(Boolean).join(" ") || "Framework not recorded",
      [m.control_id, m.control_title].filter(Boolean).join(" "),
      m.result ?? m.assessment_status ? `recorded result: ${m.result ?? m.assessment_status}` : null,
      maskedText(m.rationale),
    ].filter(Boolean).join(" — ")));
  }

  if (many) {
    D.h3(`Affected assets (${group.findings.length})`);
    if (group.findings.length > ASSET_GRID_AFTER) {
      const rows: Cell[][] = [];
      for (let i = 0; i < group.findings.length; i += 3) {
        rows.push([0, 1, 2].flatMap((j) => {
          const x = group.findings[i + j];
          if (!x) return [cellText(""), cellText(""), cellText("")];
          return [cellText(refs.get(x.id) ?? "", { bold: true, size: 8 }), cellText(dash(assetLabel(x)), { size: 8 }), cellText(statusLabel(x.status), { size: 8, color: isOpenStatus(x.status) ? color.fg : BRAND_HEX.ok })];
        }));
      }
      D.add(table(["Ref", "Asset", "Status", "Ref", "Asset", "Status", "Ref", "Asset", "Status"], [0.55, 1.3, 0.85, 0.55, 1.3, 0.85, 0.55, 1.3, 0.85], rows));
      D.muted("Fix-by dates and SLA state for each asset are in the Excel workbook (Findings sheet).");
    } else {
      D.add(table(["Ref", "Asset", "Status", "First seen", "Fix by", "SLA"], [0.55, 2.2, 1, 0.9, 0.9, 0.8], group.findings.map((x) => [
        cellText(refs.get(x.id) ?? "", { bold: true }),
        cellText(dash(assetLabel(x))),
        cellText(statusLabel(x.status), { color: isOpenStatus(x.status) ? color.fg : BRAND_HEX.ok }),
        cellText(dash(formatDate(x.first_seen, tz))),
        cellText(isOpenStatus(x.status) ? dash(formatDate(x.current_sla.deadline, tz)) : "—"),
        cellText(isOpenStatus(x.status) && x.current_sla.state !== "untracked" ? humanize(x.current_sla.state) : "—"),
      ])));
    }
  }

  if (narrative.missing.length) D.muted(`Not recorded for this finding: ${narrative.missing.map((x) => x.toLowerCase()).join(", ")}.`);
  D.add(para("", { after: 240 }));
}

function detailedFindings(ctx: Ctx): void {
  const { D, groups, refs } = ctx;
  D.h1("4  Detailed findings");
  if (!groups.length) { D.note("No findings are recorded for this engagement.", "info"); return; }
  const low = groups.filter((g) => g.severity === "low" || g.severity === "info");
  const condense = low.length > 25;
  (condense ? groups.filter((g) => !low.includes(g)) : groups).forEach((g) => findingSection(ctx, g));
  if (condense) {
    D.h2("Low and informational observations");
    D.muted(`${low.length} low and informational issues are listed in brief. Their complete records are in the Excel workbook.`);
    D.add(table(["Ref", "Finding", "Severity", "Assets", "Summary"], [0.8, 2.5, 0.95, 1.2, 3], low.map((g) => [
      cellText(groupRef(g, refs), { bold: true }), cellText(g.title), pillCell(g.severity), cellText(dash(groupAssets(g.findings))), cellText((plain(g.lead.description) || "—").slice(0, 220), { size: 8 }),
    ])));
  }
}

function roadmapSection({ D, report, tz }: Ctx): void {
  D.h1("5  Remediation roadmap");
  const roadmap = remediationRoadmap(report);
  if (!roadmap.length) { D.note("No findings are open, so no remediation is outstanding.", "info"); return; }
  D.muted("Open findings grouped by priority. Target windows come only from the current SLA policy recorded for each finding; where none is recorded, no target is shown.");
  for (const bucket of roadmap) {
    D.h2(bucket.title);
    D.muted(`${bucket.findings} open finding${bucket.findings === 1 ? "" : "s"}${bucket.items.length < bucket.findings ? ` in ${bucket.items.length} issue${bucket.items.length === 1 ? "" : "s"}` : ""}${bucket.target ? ` · fix ${bucket.target}` : " · no SLA window recorded"}`);
    D.add(table(["Ref", "Finding", "Assets", "Owner", "Fix by", "SLA"], [0.8, 2.6, 1.4, 1.1, 0.95, 0.8], bucket.items.map((i) => [
      cellText(i.ref, { bold: true }), cellText(i.title), cellText(dash(i.asset)), cellText(dash(i.owner)), cellText(dash(formatDate(i.deadline, tz))),
      cellText(i.slaState ? humanize(i.slaState) : "—", { bold: Boolean(i.slaState), color: i.slaState === "breached" ? SEVERITY_HEX.critical.fg : i.slaState === "at_risk" ? SEVERITY_HEX.high.fg : undefined }),
    ])));
  }
}

function closureRegister({ D, groups, refs, tz }: Ctx): void {
  D.h1("6  Retest and closure register");
  D.muted("Disposition and retest status for every finding. “Closed” is an operational disposition: remediated, risk-accepted and false-positive records stay distinct and are not a regulatory closure conclusion.");
  if (!groups.length) { D.note("No findings are recorded."); return; }
  D.add(table(["Ref", "Finding", "Severity", "Disposition", "Resolved", "Retest", "Reopened"], [0.8, 2.4, 0.95, 1.35, 0.9, 0.85, 0.65], groups.map((g) => {
    const views = g.findings.map(closureView);
    const resolved = views.map((v) => v.resolvedAt).filter((d): d is string => Boolean(d)).sort();
    const passed = views.filter((v) => v.retest === "Passed").length;
    const failed = views.filter((v) => v.retest === "Failed").length;
    const retest = g.findings.length === 1 ? views[0]!.retest : passed || failed ? [passed ? `${passed} passed` : null, failed ? `${failed} failed` : null].filter(Boolean).join(", ") : null;
    return [
      cellText(groupRef(g, refs), { bold: true }), cellText(g.title), pillCell(g.severity),
      cellText(g.findings.length === 1 ? views[0]!.disposition : statusSummary(g.findings), { bold: true, color: g.open ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok }),
      cellText(g.open === 0 && resolved.length ? dash(formatDate(resolved[resolved.length - 1], tz)) : "—"),
      cellText(retest ?? "—", { color: failed ? SEVERITY_HEX.critical.fg : retest ? BRAND_HEX.ok : undefined }),
      cellText(String(views.reduce((a, v) => a + v.reopened, 0))),
    ];
  })));
}

function complianceSection({ D, report, refs }: Ctx): void {
  D.h1("7  Compliance context");
  const roll = report.compliance_rollup;
  D.h2("Recorded finding-to-control mappings");
  D.note("Recorded references only. This is not a certification, audit opinion, or compliance verdict, and unrecorded controls are not inferred.", "caution");
  const rows = roll.frameworks.flatMap((fw) => fw.controls.map((c) => [
    cellText([fw.framework, fw.framework_version].filter(Boolean).join(" ") || "Not recorded"), cellText(dash(c.control_id), { bold: true }), cellText(dash(c.control_title)),
    cellText(dash(c.recorded_results.join(", "))), cellText(compactRefs(c.finding_ids.map((id) => refs.get(id) ?? id))),
  ]));
  if (rows.length) D.add(table(["Framework", "Control", "Title", "Recorded result", "Findings"], [1.3, 0.8, 1.8, 1, 1.1], rows));
  else D.note(roll.gap ? humanize(roll.gap) : "No finding-to-control mappings are recorded.");
  if (roll.unmapped_finding_ids.length) D.muted(`Findings without a recorded mapping: ${compactRefs(roll.unmapped_finding_ids.map((id) => refs.get(id) ?? id))}.`);
  const mappingGaps = new Set(report.findings.flatMap((f) => f.compliance_mappings)
    .filter((m) => m.validation_gaps.length)
    .map((m) => `${[m.framework, m.control_id].filter(Boolean).join(" ")}: ${m.validation_gaps.join(", ")}`));
  for (const line of mappingGaps) D.muted(`Mapping review: ${line}`);

  if (roll.regulatory_profiles.length) {
    D.h2("Selected regulatory profiles");
    D.note("A selected profile records applicability context only. It does not by itself establish compliance, and no conditional annexure or obligation is inferred.");
    D.add(table(["Profile", "Version", "Jurisdiction", "Applicability"], [2.2, 0.9, 0.9, 2], roll.regulatory_profiles.map((p) => [cellText(dash(p.name)), cellText(dash(p.version)), cellText(dash(p.jurisdiction)), cellText(dash(maskedText(p.applicability)))])));
  }

  const d = report.derived_regional_compliance;
  D.h2("Derived regional compliance context — not assessed");
  D.note("Derived context only. The following profile, frameworks, obligations, and reporting clocks are not assessed control results, a certification, an attestation, or legal advice.", "caution");
  const sector = typeof d.profile.sector === "string" ? humanize(d.profile.sector) : null;
  const jurisdictions = Array.isArray(d.profile.jurisdictions) ? d.profile.jurisdictions.filter((x): x is string => typeof x === "string").join(", ") : null;
  D.keyValues([
    { label: "Profile basis", value: humanize(d.profile_source) },
    { label: d.profile_source === "recorded_engagement_profile" ? "Configured sector" : "Default sector", value: dash(sector) },
    { label: "Jurisdictions", value: dash(jurisdictions) },
    { label: "Asset tags considered", value: dash(d.asset_tags.join(", ")) },
  ], 2);
  if (d.frameworks.length) {
    D.add(table(["Framework", "Authority", "Basis", "Source reference"], [1.8, 1.6, 0.9, 2.2], d.frameworks.map((fw) => [cellText(fw.name, { bold: true }), cellText(fw.authority), cellText(fw.tag_triggered ? "Asset tag" : "Profile"), cellText(fw.source_reference, { size: 8 })])));
  }
  if (d.reporting_clocks.length) {
    D.h3("Contextual reporting clocks");
    D.add(table(["Framework", "Deadline", "Trigger", "Reference"], [1.7, 0.7, 1.8, 2], d.reporting_clocks.map((c) => [cellText(c.framework), cellText(`${c.deadline_hours} hours`, { bold: true }), cellText(c.trigger), cellText(c.reference, { size: 8 })])));
    D.muted("A listed reporting deadline is a contextual trigger reference; this report does not assert that an incident or notification trigger occurred.");
  }
  D.muted(d.disclaimer);
}

function appendices(ctx: Ctx): void {
  const { D, report, ordered, groups, refs, tz } = ctx;
  D.h1("Appendix A — Risk rating");
  D.p("Severity follows the FIRST CVSS v3.1 qualitative scale. Where an assessor recorded a different rating method, it is stated below.");
  D.add(table(["Severity", "CVSS v3.1", "Meaning"], [0.9, 0.8, 3.4], SEVERITY_DEFINITIONS.map((d) => [pillCell(d.severity), cellText(d.cvss), cellText(d.meaning)])));
  const method = metadataText(report, "risk_rating_method");
  if (method) D.p(`Recorded rating method: ${method}`);
  D.muted("Overall risk is the highest severity among findings that are still open or confirmed.");

  D.h1("Appendix B — Derived control pointers by finding — not assessed");
  D.note("Derived compliance context — not assessed. These pointers are separate from recorded mappings and are not a certification, attestation, legal conclusion, or recorded control result.", "caution");
  const pointers: Cell[][] = [];
  for (const g of groups) {
    const c = g.lead.derived_compliance_context;
    for (const p of c.global_framework_pointers) pointers.push([cellText(groupRef(g, refs), { bold: true }), cellText(p.framework), cellText(p.controls.join(", ")), cellText(humanize(c.category))]);
    for (const o of c.regional_obligations) pointers.push([cellText(groupRef(g, refs), { bold: true }), cellText(o.framework), cellText(o.controls.join(", ")), cellText(humanize(c.category))]);
  }
  if (pointers.length) D.add(table(["Ref", "Framework", "Control pointers", "Category"], [0.7, 1.8, 2.3, 1], pointers));
  else D.note("No control pointers were derived.");
  const generic = ordered.filter((f) => f.derived_compliance_context.used_generic_fallback);
  if (generic.length) D.note(`Generic fallback warning: ${compactRefs(generic.map((f) => refs.get(f.id) ?? ""))} used the generic control-pointer set. Confirm the classification and control applicability before customer delivery.`, "caution");

  D.h1("Appendix C — Evidence integrity and provenance");
  if (ordered.length <= 60) {
    D.p("Detection runs and evidence hashes for each finding, so any excerpt in this report can be traced to the scan that produced it.");
    D.add(table(["Ref", "Initial discovery run", "Latest observation run", "Evidence SHA-256"], [0.5, 1.6, 1.6, 2.2], ordered.map((f) => [
      cellText(refs.get(f.id) ?? "", { bold: true }),
      cellText(f.initial_detection_provenance ? `${f.initial_detection_provenance.run_id}\n${dash(f.initial_detection_provenance.scan_type)} · ${dash(formatDate(f.initial_detection_provenance.started_at, tz))}` : dash(f.initial_detection_run_id), { font: MONO, size: 7 }),
      cellText(f.latest_detection_provenance ? `${f.latest_detection_provenance.run_id}\n${dash(f.latest_detection_provenance.scan_type)} · ${dash(formatDate(f.latest_detection_provenance.started_at, tz))}` : dash(f.detection_run_id), { font: MONO, size: 7 }),
      cellText(f.evidence.artifacts.map((a) => `E${String(a.index).padStart(2, "0")} ${a.sha256 ?? "—"}${a.sha256_verified ? " (verified)" : ""}`).join("\n") || "No evidence recorded", { font: MONO, size: 7 }),
    ])));
  } else {
    D.p(`Summary per issue. Per-finding detection runs and evidence hashes for all ${ordered.length} findings are in the Excel workbook (Findings and Evidence sheets).`);
    D.add(table(["Ref", "Finding", "Detection runs", "Evidence items", "Hash verified"], [0.8, 2.6, 0.9, 0.9, 0.9], groups.map((g) => {
      const runs = new Set(g.findings.flatMap((f) => [f.initial_detection_run_id, f.detection_run_id]).filter(Boolean));
      const artifacts = g.findings.flatMap((f) => f.evidence.artifacts);
      return [cellText(groupRef(g, refs), { bold: true }), cellText(g.title), cellText(String(runs.size)), cellText(String(artifacts.length)), cellText(artifacts.length ? `${artifacts.filter((a) => a.sha256_verified).length} of ${artifacts.length}` : "—")];
    })));
  }

  const gaps = gapInventory(report);
  D.h1("Appendix D — Record readiness");
  D.p(report.readiness.complete
    ? "No configured completeness gaps were identified. This does not constitute approval for delivery."
    : "The live record contains gaps that need operator review before customer delivery. Each gap is listed once, with the findings it affects.");
  if (gaps.reportLevel.length) { D.h3("Report-level gaps"); D.bullets(gaps.reportLevel.map((g) => `${g.label} (${g.code})`)); }
  if (gaps.findingLevel.length) {
    D.h3("Finding-level gaps");
    D.add(table(["Gap", "Count", "Findings"], [2.2, 0.5, 2.2], gaps.findingLevel.map((g) => [
      { content: text(g.label, { size: 9 }, { after: 0 }) + text(g.code, { size: 7.5, font: MONO, color: BRAND_HEX.muted }, { after: 0 }) },
      cellText(String(g.count)), cellText(compactRefs(g.refs)),
    ])));
  }

  D.h1("Appendix E — About this document");
  D.keyValues([
    { label: "Engagement ID", value: report.engagement.id, mono: true },
    { label: "Schema version", value: report.document.schema_version },
    { label: "Generated (UTC)", value: report.document.generated_at, mono: true },
    { label: "Display time zone", value: tz },
    { label: "Snapshot", value: `${report.document.snapshot_kind} · guarantee: ${report.document.snapshot_guarantee}` },
    { label: "Persisted report record", value: report.document.persisted ? "Yes" : "No" },
  ], 2);
  D.muted("This report is generated from the live canonical record at the time shown. Unless the document status records an approved issue, it is a draft for review, not an approved, signed, or immutable deliverable.");
}

// ─── Package parts ───────────────────────────────────────────────────────────

function tocXml(headings: Doc["headings"]): string {
  // A real contents field (Word fills page numbers on open), pre-filled with
  // the section titles so it reads correctly before it is updated.
  const entries = headings.filter((h) => h.level === 1).map((h) =>
    para(run(h.title), { style: "TOC1" })).join("");
  return `<w:p><w:pPr><w:pStyle w:val="TOC1"/></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-1" \\h \\z \\u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>${entries}<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>`;
}

function stylesXml(): string {
  const font = `<w:rFonts w:ascii="${FONT}" w:hAnsi="${FONT}" w:cs="${FONT}" w:eastAsia="${FONT}"/>`;
  const heading = (id: string, name: string, size: number, color: string, extra: string, level: number, caps = false) =>
    `<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${name}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/>${extra}<w:outlineLvl w:val="${level}"/></w:pPr><w:rPr><w:b/>${caps ? "<w:caps/>" : ""}<w:color w:val="${hex(color)}"/><w:sz w:val="${size * 2}"/><w:szCs w:val="${size * 2}"/></w:rPr></w:style>`;
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>${font}<w:color w:val="${hex(BRAND_HEX.ink)}"/><w:sz w:val="20"/><w:szCs w:val="20"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="268" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:color w:val="${hex(BRAND_HEX.navy)}"/><w:sz w:val="52"/></w:rPr></w:style>
${heading("Heading1", "heading 1", 18, BRAND_HEX.navy, `<w:spacing w:before="120" w:after="200"/><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="6" w:color="${hex(BRAND_HEX.accent)}"/></w:pBdr>`, 0)}
${heading("Heading2", "heading 2", 13, BRAND_HEX.navy, `<w:spacing w:before="240" w:after="100"/>`, 1)}
${heading("Heading3", "heading 3", 8, BRAND_HEX.accent, `<w:spacing w:before="200" w:after="60"/>`, 2, true)}
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="60"/><w:ind w:left="360" w:hanging="240"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F3F5F8"/><w:pBdr><w:left w:val="single" w:sz="12" w:space="6" w:color="${hex(BRAND_HEX.rule)}"/></w:pBdr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="120"/></w:pPr><w:rPr><w:rFonts w:ascii="${MONO}" w:hAnsi="${MONO}" w:cs="${MONO}"/><w:color w:val="1E293B"/><w:sz w:val="16"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="${hex(BRAND_HEX.wash)}"/><w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="${hex(BRAND_HEX.muted)}"/></w:pBdr><w:spacing w:before="60" w:after="160"/><w:ind w:left="120" w:right="120"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="NoteCaution"><w:name w:val="Note (caution)"/><w:basedOn w:val="Note"/><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFF8EB"/><w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="8A5300"/></w:pBdr></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="${CONTENT}"/></w:tabs><w:spacing w:after="80"/></w:pPr></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="table" w:styleId="VedhaTable"><w:name w:val="Vedha Table"/><w:basedOn w:val="TableNormal"/><w:tblPr><w:tblStyleRowBandSize w:val="1"/><w:tblBorders><w:bottom w:val="single" w:sz="4" w:space="0" w:color="${hex(BRAND_HEX.rule)}"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="${hex(BRAND_HEX.rule)}"/></w:tblBorders></w:tblPr><w:tblStylePr w:type="band2Horz"><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="${hex(BRAND_HEX.wash)}"/></w:tcPr></w:tblStylePr></w:style>
<w:style w:type="table" w:styleId="VedhaGrid"><w:name w:val="Vedha Grid"/><w:basedOn w:val="TableNormal"/><w:tblPr><w:tblCellSpacing w:w="40" w:type="dxa"/></w:tblPr></w:style>
</w:styles>`;
}

function numberingXml(numbered: number): string {
  const bullet = `<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="240"/></w:pPr><w:rPr><w:color w:val="${hex(BRAND_HEX.muted)}"/></w:rPr></w:lvl></w:abstractNum>`;
  const decimal = `<w:abstractNum w:abstractNumId="2"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="300"/></w:pPr></w:lvl></w:abstractNum>`;
  const nums = [`<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>`];
  for (let i = 1; i <= numbered; i++) {
    nums.push(`<w:num w:numId="${100 + i}"><w:abstractNumId w:val="2"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>`);
  }
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">${bullet}${decimal}${nums.join("")}</w:numbering>`;
}

const W_NS = `xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"`;

function headerXml(report: ReportDocument): string {
  const classification = metadataText(report, "classification") ?? "Confidential";
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr ${W_NS}><w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="${CONTENT}"/></w:tabs><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="${hex(BRAND_HEX.rule)}"/></w:pBdr></w:pPr>${run(`VEDHA  ·  ${report.engagement.name}`, { size: 7.5, color: BRAND_HEX.muted, bold: true })}<w:r><w:tab/></w:r>${run(classification.toUpperCase(), { size: 7.5, color: BRAND_HEX.muted, bold: true })}</w:p></w:hdr>`;
}

function footerXml(report: ReportDocument, issued: boolean): string {
  const client = plain(report.engagement.client);
  const rpr = `<w:rPr><w:color w:val="${hex(BRAND_HEX.muted)}"/><w:sz w:val="15"/><w:szCs w:val="15"/></w:rPr>`;
  const field = (code: string) => `<w:r>${rpr}<w:fldChar w:fldCharType="begin"/></w:r><w:r>${rpr}<w:instrText xml:space="preserve"> ${code} </w:instrText></w:r><w:r>${rpr}<w:fldChar w:fldCharType="separate"/></w:r><w:r>${rpr}<w:t>1</w:t></w:r><w:r>${rpr}<w:fldChar w:fldCharType="end"/></w:r>`;
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr ${W_NS}><w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="${CONTENT}"/></w:tabs><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="${hex(BRAND_HEX.rule)}"/></w:pBdr><w:rPr><w:sz w:val="15"/></w:rPr></w:pPr>${run(`${client ? `${client} — ` : ""}Vulnerability assessment report${issued ? "" : " — draft"}`, { size: 7.5, color: BRAND_HEX.muted })}<w:r><w:tab/></w:r>${run("Page ", { size: 7.5, color: BRAND_HEX.muted })}${field("PAGE")}${run(" of ", { size: 7.5, color: BRAND_HEX.muted })}${field("NUMPAGES")}</w:p></w:ftr>`;
}

function created(report: ReportDocument): string {
  const date = new Date(report.document.generated_at);
  return Number.isNaN(date.getTime()) ? "" : `<dcterms:created xsi:type="dcterms:W3CDTF">${date.toISOString()}</dcterms:created>`;
}

export function buildReportDocx(report: ReportDocument): Buffer {
  const D = new Doc();
  const ctx: Ctx = {
    D,
    report,
    tz: usableTimeZone(report.document.display_timezone),
    refs: findingRefs(report),
    ordered: orderFindings(report.findings),
    groups: issueGroups(report.findings),
    issued: isIssued(report),
  };
  cover(ctx);
  documentControl(ctx);
  executiveSummary(ctx);
  scopeAndMethod(ctx);
  findingsOverview(ctx);
  detailedFindings(ctx);
  roadmapSection(ctx);
  closureRegister(ctx);
  complianceSection(ctx);
  appendices(ctx);

  const body = D.xml.replace("__TOC__", tocXml(D.headings));
  const sect = `<w:sectPr><w:headerReference w:type="default" r:id="rIdHeader"/><w:footerReference w:type="default" r:id="rIdFooter"/><w:pgSz w:w="${PAGE_W}" w:h="${PAGE_H}"/><w:pgMar w:top="${MARGIN + 200}" w:right="${MARGIN}" w:bottom="${MARGIN}" w:left="${MARGIN}" w:header="560" w:footer="560" w:gutter="0"/><w:titlePg/></w:sectPr>`;
  const document = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W_NS}><w:body>${body}${sect}</w:body></w:document>`;
  const title = esc(report.engagement.name);
  return zip([
    { name: "[Content_Types].xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>` },
    { name: "_rels/.rels", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>` },
    { name: "word/_rels/document.xml.rels", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rIdHeader" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>` },
    { name: "word/document.xml", data: document },
    { name: "word/styles.xml", data: stylesXml() },
    { name: "word/numbering.xml", data: numberingXml(D.numbered) },
    { name: "word/settings.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:updateFields w:val="true"/><w:defaultTabStop w:val="720"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>` },
    { name: "word/header1.xml", data: headerXml(report) },
    { name: "word/footer1.xml", data: footerXml(report, ctx.issued) },
    { name: "docProps/core.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${title} — vulnerability assessment report</dc:title><dc:creator>Vedha VAPT Platform</dc:creator>${created(report)}</cp:coreProperties>` },
    { name: "docProps/app.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Vedha VAPT Platform</Application></Properties>` },
  ]);
}
