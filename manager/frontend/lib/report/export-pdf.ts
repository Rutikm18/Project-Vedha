/**
 * PDF security report.
 *
 * Built from the shared presentation layer, so the PDF says exactly what the
 * web report says: recorded values and disclosed derivations, masked. Layout:
 * cover → document control and contents → executive summary → scope and
 * method → findings overview → one section per finding → remediation roadmap
 * → retest and closure → compliance context → appendices.
 *
 * Text is set in IBM Plex Sans / Mono. Any character Plex lacks (CJK, rare
 * scripts) is drawn with the bundled GNU Unifont instead, so every recorded
 * character survives and can be copied out of the PDF.
 */
import path from "node:path";
import PDFDocument from "pdfkit";

import {
  BRAND_HEX,
  METHOD_FIELDS,
  SEVERITY_DEFINITIONS,
  SEVERITY_HEX,
  SEVERITY_LABEL,
  closureView,
  compactRefs,
  evidenceView,
  excerpt,
  findingNarrative,
  findingRefs,
  formatDate,
  groupAssets,
  groupRef,
  issueGroups,
  sharedNarrativeKeys,
  assetLabel,
  formatDateTime,
  gapInventory,
  humanize,
  isIssued,
  isOpenStatus,
  executiveNarrative,
  issueFacts,
  keyMetrics,
  statusSummary,
  priorityLines,
  maskedText,
  metadataText,
  orderFindings,
  overallRating,
  remediationRoadmap,
  remediationView,
  severityRows,
  statusLabel,
  statusRows,
  topRisks,
  usableTimeZone,
  type IssueGroup,
  type Readable,
  type SeverityKey,
} from "./presentation";
import type { ReportDocument, ReportEvidence, ReportFinding } from "./report-document";

// ─── Page geometry ───────────────────────────────────────────────────────────

const PAGE_W = 595.28;
const PAGE_H = 841.89;
const MARGIN_X = 54;
const CONTENT_W = PAGE_W - MARGIN_X * 2;
const TOP = 76;
const BOTTOM = 776;

const FONT_DIR = path.join(process.cwd(), "public", "fonts");
const FONTS = {
  regular: "IBMPlexSans-Regular.woff",
  italic: "IBMPlexSans-Italic.woff",
  medium: "IBMPlexSans-Medium.woff",
  semibold: "IBMPlexSans-SemiBold.woff",
  bold: "IBMPlexSans-Bold.woff",
  mono: "IBMPlexMono-Regular.woff",
  monoMedium: "IBMPlexMono-Medium.woff",
  fallback: "unifont-17.0.05.otf",
} as const;
type FontName = keyof typeof FONTS;

/** Findings at these severities beyond this many are tabulated, not paged. */
const CONDENSE_LOW_AFTER = 25;
const EVIDENCE_LINES = 28;
/** Above this many findings, per-finding provenance lives in the workbook. */
const PROVENANCE_DETAIL_MAX = 60;
/** Above this many affected assets, list them three per row. */
const ASSET_GRID_AFTER = 20;

// ─── Layout kit ──────────────────────────────────────────────────────────────

interface TextOptions {
  font?: FontName;
  size?: number;
  color?: string;
  width?: number;
  align?: "left" | "right" | "center" | "justify";
  lineGap?: number;
}

type Cell = string | {
  text: string;
  font?: FontName;
  color?: string;
  fill?: string;
  pill?: SeverityKey;
  size?: number;
};

interface Column { header: string; width: number; align?: "left" | "right" | "center"; font?: FontName }

class Layout {
  readonly doc: PDFKit.PDFDocument;
  readonly trace: string[] = [];
  private coverage = new Map<FontName, (cp: number) => boolean>();
  /** Section title → physical page number, for the contents page. */
  readonly sections: Array<{ title: string; page: number; dest: string; level: number }> = [];

  constructor(doc: PDFKit.PDFDocument) {
    this.doc = doc;
    for (const [name, file] of Object.entries(FONTS)) doc.registerFont(name, path.join(FONT_DIR, file));
  }

  get y(): number { return this.doc.y; }
  set y(value: number) { this.doc.y = value; }

  page(): void {
    this.doc.addPage({ size: "A4", margins: { top: TOP, bottom: 20, left: MARGIN_X, right: MARGIN_X } });
    this.doc.x = MARGIN_X;
    this.doc.y = TOP;
  }

  pageNumber(): number {
    const range = this.doc.bufferedPageRange();
    return range.start + range.count;
  }

  ensure(height: number): void {
    if (this.y + height > BOTTOM) this.page();
  }

  private covers(font: FontName): (cp: number) => boolean {
    let check = this.coverage.get(font);
    if (!check) {
      this.doc.font(font);
      const fk = (this.doc as unknown as { _font?: { font?: { hasGlyphForCodePoint?: (cp: number) => boolean } } })._font?.font;
      check = fk?.hasGlyphForCodePoint ? (cp: number) => fk.hasGlyphForCodePoint!(cp) : () => true;
      this.coverage.set(font, check);
    }
    return check;
  }

  /** Split text into runs the primary font can draw and runs it cannot. */
  private runs(text: string, font: FontName): Array<{ text: string; fallback: boolean }> {
    const has = this.covers(font);
    const runs: Array<{ text: string; fallback: boolean }> = [];
    for (const ch of text) {
      const cp = ch.codePointAt(0)!;
      const fallback = cp > 0x20 && !has(cp);
      const last = runs[runs.length - 1];
      if (last && last.fallback === fallback) last.text += ch;
      else runs.push({ text: ch, fallback });
    }
    return runs;
  }

  measure(text: string, o: TextOptions = {}): number {
    this.doc.font(o.font ?? "regular").fontSize(o.size ?? 9.5);
    return this.doc.heightOfString(text || " ", { width: o.width ?? CONTENT_W, lineGap: o.lineGap ?? 2.2 });
  }

  /** Draw text at (x, y); returns the height used. Every string is traced. */
  text(text: string, x: number, y: number, o: TextOptions = {}): number {
    const value = text.replace(/\u0000/g, "");
    if (value.trim()) this.trace.push(value);
    const font = o.font ?? "regular";
    const size = o.size ?? 9.5;
    const width = o.width ?? CONTENT_W;
    const lineGap = o.lineGap ?? 2.2;
    const height = this.measure(value, { ...o, font, size, width, lineGap });
    const runs = this.runs(value || " ", font);
    // Drawing never moves the cursor; callers advance `y` explicitly.
    const cursor = this.doc.y;
    this.doc.fillColor(o.color ?? BRAND_HEX.ink);
    runs.forEach((run, index) => {
      this.doc.font(run.fallback ? "fallback" : font).fontSize(size);
      const options = { width, align: o.align ?? "left", lineGap, continued: index < runs.length - 1 };
      if (index === 0) this.doc.text(run.text, x, y, options);
      else this.doc.text(run.text, options);
    });
    this.doc.x = MARGIN_X;
    this.doc.y = cursor;
    return height;
  }

  /** Flowing paragraph at the cursor, breaking pages as needed. */
  para(text: string, o: TextOptions & { gap?: number; indent?: number } = {}): void {
    const indent = o.indent ?? 0;
    const width = (o.width ?? CONTENT_W) - indent;
    const h = this.measure(text, { ...o, width });
    if (h > BOTTOM - TOP) {
      // A paragraph longer than a page: split on lines so it can flow.
      for (const line of text.split("\n")) this.para(line, o);
      return;
    }
    this.ensure(h);
    this.text(text, MARGIN_X + indent, this.y, { ...o, width });
    this.y += h + (o.gap ?? 5);
  }

  bullets(items: string[], o: TextOptions & { numbered?: boolean } = {}): void {
    items.forEach((item, index) => {
      const marker = o.numbered ? `${index + 1}.` : "•";
      const h = this.measure(item, { ...o, width: CONTENT_W - 16 });
      this.ensure(h);
      this.text(marker, MARGIN_X + 2, this.y, { ...o, color: BRAND_HEX.muted, width: 14 });
      this.text(item, MARGIN_X + 16, this.y, { ...o, width: CONTENT_W - 16 });
      this.y += h + 3;
    });
    this.y += 2;
  }

  readable(body: Readable): void {
    if (body.kind === "text") body.paragraphs.forEach((p) => this.para(p));
    else if (body.kind === "list") this.bullets(body.items);
    else this.keyValues(body.rows.map(([k, v]) => ({ label: k, value: v })), 2);
  }

  heading(title: string, level: 1 | 2 | 3, o: { newPage?: boolean; toc?: boolean; number?: string } = {}): void {
    if (o.newPage) this.page();
    const label = o.number ? `${o.number}  ${title}` : title;
    if (level === 1) {
      this.ensure(60);
      if (o.toc !== false) this.mark(label, 1);
      this.text(label, MARGIN_X, this.y, { font: "semibold", size: 19, color: BRAND_HEX.navy });
      this.y += 28;
      this.doc.rect(MARGIN_X, this.y, 36, 2.4).fill(BRAND_HEX.accent);
      this.y += 14;
    } else if (level === 2) {
      this.ensure(44);
      if (o.toc) this.mark(label, 2);
      this.y += 6;
      this.text(label, MARGIN_X, this.y, { font: "semibold", size: 12.5, color: BRAND_HEX.navy });
      this.y += 20;
    } else {
      // Keep a subheading with at least two lines of what follows it.
      this.ensure(52);
      this.y += 3;
      this.text(label.toUpperCase(), MARGIN_X, this.y, { font: "semibold", size: 7.6, color: BRAND_HEX.accent });
      this.y += 13;
    }
  }

  mark(title: string, level: number): void {
    const dest = `sec-${this.sections.length}`;
    this.doc.addNamedDestination(dest);
    this.sections.push({ title, page: this.pageNumber(), dest, level });
    if (level === 1) this.doc.outline.addItem(title);
  }

  note(text: string, tone: "muted" | "caution" | "info" = "muted"): void {
    const colors = { muted: [BRAND_HEX.wash, BRAND_HEX.muted], caution: ["#FFF8EB", "#8A5300"], info: ["#EEF3FD", BRAND_HEX.navy] } as const;
    const [fill, ink] = colors[tone];
    const h = this.measure(text, { size: 8.4, width: CONTENT_W - 22 }) + 12;
    this.ensure(h + 4);
    this.doc.roundedRect(MARGIN_X, this.y, CONTENT_W, h, 3).fill(fill);
    this.doc.rect(MARGIN_X, this.y, 2.4, h).fill(ink);
    this.text(text, MARGIN_X + 12, this.y + 6, { size: 8.4, color: ink, width: CONTENT_W - 22 });
    this.y += h + 8;
  }

  pill(severity: SeverityKey | "none", x: number, y: number, label?: string, size = 7.4): number {
    const text = (label ?? (severity === "none" ? "None" : SEVERITY_LABEL[severity])).toUpperCase();
    this.doc.font("semibold").fontSize(size);
    const w = this.doc.widthOfString(text) + 12;
    const color = severity === "none" ? BRAND_HEX.ok : SEVERITY_HEX[severity].fg;
    this.doc.roundedRect(x, y, w, size + 7, (size + 7) / 2).fill(color);
    this.text(text, x + 6, y + 2.7, { font: "semibold", size, color: "#FFFFFF", width: w });
    return w;
  }

  /** Label/value grid with `cols` columns; only recorded values are passed in. */
  keyValues(rows: Array<{ label: string; value: string; mono?: boolean }>, cols = 2, wash = false): void {
    if (rows.length === 0) return;
    const gap = 14;
    const colW = (CONTENT_W - gap * (cols - 1)) / cols;
    const top = this.y;
    for (let i = 0; i < rows.length; i += cols) {
      const slice = rows.slice(i, i + cols);
      const heights = slice.map((r) => 11 + this.measure(r.value, { size: 9, width: colW, font: r.mono ? "mono" : "regular" }));
      const rowH = Math.max(...heights) + 7;
      this.ensure(rowH);
      if (wash) this.doc.rect(MARGIN_X - 6, this.y - 3, CONTENT_W + 12, rowH).fill(BRAND_HEX.wash);
      slice.forEach((r, j) => {
        const x = MARGIN_X + j * (colW + gap);
        this.text(r.label.toUpperCase(), x, this.y, { font: "medium", size: 6.8, color: BRAND_HEX.muted, width: colW });
        this.text(r.value, x, this.y + 10, { size: r.mono ? 8 : 9, width: colW, font: r.mono ? "mono" : "regular" });
      });
      this.y += rowH;
    }
    void top;
    this.y += 4;
  }

  table(columns: Column[], rows: Cell[][], o: { size?: number; zebra?: boolean; empty?: string } = {}): void {
    const size = o.size ?? 8.4;
    const pad = 5;
    const total = columns.reduce((a, c) => a + c.width, 0);
    const widths = columns.map((c) => (c.width / total) * CONTENT_W);
    const drawHeader = () => {
      const h = 18;
      this.ensure(h + 20);
      this.doc.rect(MARGIN_X, this.y, CONTENT_W, h).fill(BRAND_HEX.navy);
      let x = MARGIN_X;
      columns.forEach((c, i) => {
        this.text(c.header.toUpperCase(), x + pad, this.y + 5.6, { font: "semibold", size: 6.8, color: "#FFFFFF", width: widths[i]! - pad * 2, align: c.align });
        x += widths[i]!;
      });
      this.y += h;
    };
    drawHeader();
    if (rows.length === 0) {
      this.text(o.empty ?? "None recorded.", MARGIN_X + pad, this.y + 5, { font: "italic", size, color: BRAND_HEX.muted });
      this.y += 22;
      return;
    }
    rows.forEach((row, index) => {
      const cells = row.map((cell) => (typeof cell === "string" ? { text: cell } : cell));
      const heights = cells.map((cell, i) => (cell.pill ? size + 7 : this.measure(cell.text.slice(0, 1600), { font: cell.font ?? columns[i]!.font ?? "regular", size: cell.size ?? size, width: widths[i]! - pad * 2, lineGap: 1.6 })));
      const rowH = Math.max(...heights) + pad * 2;
      if (this.y + rowH > BOTTOM) {
        this.page();
        drawHeader();
      }
      if (o.zebra !== false && index % 2 === 1) this.doc.rect(MARGIN_X, this.y, CONTENT_W, rowH).fill(BRAND_HEX.wash);
      let x = MARGIN_X;
      cells.forEach((cell, i) => {
        if (cell.fill) this.doc.rect(x, this.y, widths[i]!, rowH).fill(cell.fill);
        if (cell.pill) this.pill(cell.pill, x + pad, this.y + pad, cell.text || undefined, 6.6);
        else this.text(cell.text.slice(0, 1600), x + pad, this.y + pad, { font: cell.font ?? columns[i]!.font ?? "regular", size: cell.size ?? size, color: cell.color, width: widths[i]! - pad * 2, align: columns[i]!.align, lineGap: 1.6 });
        x += widths[i]!;
      });
      this.y += rowH;
      this.doc.moveTo(MARGIN_X, this.y).lineTo(MARGIN_X + CONTENT_W, this.y).lineWidth(0.4).strokeColor(BRAND_HEX.rule).stroke();
    });
    this.y += 10;
  }

  /** Monospace block with a tinted background; splits across pages. */
  code(text: string, caption?: string): void {
    const size = 7.4;
    const lines = text.split("\n");
    let i = 0;
    while (i < lines.length) {
      const room = BOTTOM - this.y - 14;
      if (room < 40) { this.page(); continue; }
      const chunk: string[] = [];
      let h = 0;
      while (i < lines.length) {
        const lh = this.measure(lines[i] || " ", { font: "mono", size, width: CONTENT_W - 16, lineGap: 1.4 });
        if (h + lh > room && chunk.length) break;
        chunk.push(lines[i] || " ");
        h += lh;
        i++;
      }
      this.doc.rect(MARGIN_X, this.y, CONTENT_W, h + 12).fill("#F3F5F8");
      this.doc.rect(MARGIN_X, this.y, 2, h + 12).fill(BRAND_HEX.rule);
      this.text(chunk.join("\n"), MARGIN_X + 9, this.y + 6, { font: "mono", size, color: "#1E293B", width: CONTENT_W - 16, lineGap: 1.4 });
      this.y += h + 12;
    }
    if (caption) {
      this.text(caption, MARGIN_X, this.y + 3, { font: "italic", size: 7.4, color: BRAND_HEX.muted });
      this.y += 13;
    }
    this.y += 6;
  }
}

// ─── Small helpers ───────────────────────────────────────────────────────────

function dash(value: string | null | undefined): string {
  return value && value.trim() ? value : "—";
}

function plainText(value: unknown): string {
  return maskedText(value) ?? "";
}

function short(hash: string | null | undefined): string {
  if (!hash) return "—";
  return hash.length > 20 ? `${hash.slice(0, 12)}…${hash.slice(-6)}` : hash;
}

// ─── Sections ────────────────────────────────────────────────────────────────

interface Ctx {
  L: Layout;
  report: ReportDocument;
  tz: string;
  refs: Map<string, string>;
  ordered: ReportFinding[];
  groups: IssueGroup[];
  issued: boolean;
}

function cover({ L, report, tz, issued }: Ctx): void {
  const doc = L.doc;
  const meta = (k: string) => metadataText(report, k);
  L.page();
  doc.rect(0, 0, PAGE_W, 330).fill(BRAND_HEX.navy);
  doc.rect(0, 330, PAGE_W, 4).fill(BRAND_HEX.accent);
  L.text("VEDHA", MARGIN_X, 56, { font: "bold", size: 13, color: "#FFFFFF" });
  L.text("SECURITY ASSESSMENT", MARGIN_X + 62, 59.5, { font: "medium", size: 8, color: "#9DB2D6" });
  L.text("Vulnerability Assessment Report", MARGIN_X, 168, { font: "semibold", size: 27, color: "#FFFFFF", width: CONTENT_W });
  L.text(report.engagement.name, MARGIN_X, 212, { font: "regular", size: 15, color: "#D6E0F2", width: CONTENT_W });
  L.text(report.engagement.client ? `Prepared for ${plainText(report.engagement.client)}` : "Client not recorded", MARGIN_X, 240, { size: 10.5, color: "#9DB2D6" });
  if (!issued) {
    L.text("DRAFT / NOT APPROVED — HUMAN REVIEW REQUIRED", MARGIN_X, 288, { font: "semibold", size: 8.6, color: "#FCD34D" });
  }

  // Overall rating panel.
  const rating = overallRating(report);
  const color = rating.level === "none" ? BRAND_HEX.ok : SEVERITY_HEX[rating.level].fg;
  doc.roundedRect(MARGIN_X, 366, CONTENT_W, 74, 5).fill(BRAND_HEX.wash);
  doc.rect(MARGIN_X, 366, 4, 74).fill(color);
  L.text("OVERALL RISK", MARGIN_X + 18, 380, { font: "semibold", size: 7.2, color: BRAND_HEX.muted });
  L.text(rating.label, MARGIN_X + 18, 393, { font: "bold", size: 20, color });
  L.text(rating.basis, MARGIN_X + 190, 384, { size: 9, color: BRAND_HEX.ink, width: CONTENT_W - 210 });
  L.text("Rating method: highest severity among open findings.", MARGIN_X + 190, 414, { size: 7.4, color: BRAND_HEX.muted, width: CONTENT_W - 210 });

  // Severity tiles.
  const rows = severityRows(report);
  const tileW = (CONTENT_W - 4 * 8) / 5;
  rows.forEach((row, i) => {
    const x = MARGIN_X + i * (tileW + 8);
    doc.roundedRect(x, 456, tileW, 58, 4).fill(SEVERITY_HEX[row.severity].bg);
    doc.rect(x, 456, tileW, 3).fill(SEVERITY_HEX[row.severity].fg);
    L.text(String(row.open), x + 10, 466, { font: "bold", size: 18, color: SEVERITY_HEX[row.severity].fg });
    L.text(`${SEVERITY_LABEL[row.severity]} open`, x + 10, 491, { font: "medium", size: 7.4, color: BRAND_HEX.ink, width: tileW - 14 });
    L.text(`${row.total} recorded`, x + 10, 501, { size: 6.8, color: BRAND_HEX.muted, width: tileW - 14 });
  });

  // Document facts.
  L.y = 542;
  const period = meta("reporting_period")
    ?? ([formatDate(report.engagement.start_time, tz), formatDate(report.engagement.end_time, tz)].filter(Boolean).join(" – ") || null);
  L.keyValues([
    { label: "Client", value: dash(plainText(report.engagement.client)) },
    { label: "Assessment period", value: dash(period) },
    { label: "Report version", value: dash(meta("version")) },
    { label: "Issue date", value: dash(formatDate(meta("issue_date"), tz)) },
    { label: "Classification", value: dash(meta("classification")) },
    { label: "Document status", value: dash(meta("document_status") ?? (issued ? "Issued" : "Draft")) },
    { label: "Prepared by", value: dash(meta("prepared_by") ?? plainText(report.engagement.assessor)) },
    { label: "Generated", value: dash(formatDateTime(report.document.generated_at, tz)) },
  ], 2);

  const classification = meta("classification") ?? "Confidential";
  L.text(
    `${classification}. This report contains security-sensitive information about ${plainText(report.engagement.client) || "the client"}'s systems. Distribute only to the named recipients.`,
    MARGIN_X, 752, { size: 7.4, color: BRAND_HEX.muted, width: CONTENT_W },
  );
}

function documentControl({ L, report, tz }: Ctx): number {
  L.page();
  L.heading("Document control", 1, { toc: false });
  const meta = (k: string) => metadataText(report, k);
  const rows: Array<[string, string | null]> = [
    ["Report version", meta("version")],
    ["Document status", meta("document_status")],
    ["Classification", meta("classification")],
    ["Prepared by", meta("prepared_by")],
    ["Prepared at", formatDateTime(meta("prepared_at"), tz)],
    ["Reviewed by", meta("reviewed_by")],
    ["Reviewed at", formatDateTime(meta("reviewed_at"), tz)],
    ["Approved by", meta("approved_by")],
    ["Approved at", formatDateTime(meta("approved_at"), tz)],
    ["Issue date", formatDateTime(meta("issue_date"), tz)],
    ["Reporting period", meta("reporting_period")],
    ["Distribution", meta("distribution")],
  ];
  const recorded = rows.filter(([, v]) => v);
  L.table(
    [{ header: "Field", width: 1 }, { header: "Recorded value", width: 2.4 }],
    recorded.map(([k, v]) => [{ text: k, font: "medium" }, v!]),
    { empty: "No document-control metadata is recorded for this engagement." },
  );
  const missing = rows.filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) L.note(`Not recorded: ${missing.join(", ")}.`, "muted");

  L.y += 10;
  L.heading("Contents", 2);
  const tocTop = L.y;
  return tocTop;
}

function drawContents(L: Layout, tocPage: number, tocTop: number): void {
  const doc = L.doc;
  doc.switchToPage(tocPage - 1);
  let y = tocTop;
  for (const section of L.sections) {
    if (section.level !== 1) continue;
    const page = String(section.page);
    doc.font("regular").fontSize(10);
    const pageW = doc.widthOfString(page);
    L.text(section.title, MARGIN_X, y, { size: 10, color: BRAND_HEX.ink, width: CONTENT_W - 40 });
    doc.save();
    doc.moveTo(MARGIN_X + doc.widthOfString(section.title) + 6, y + 9.5)
      .lineTo(MARGIN_X + CONTENT_W - pageW - 6, y + 9.5)
      .dash(0.6, { space: 2.4 }).lineWidth(0.6).strokeColor(BRAND_HEX.rule).stroke();
    doc.restore();
    L.text(page, MARGIN_X + CONTENT_W - pageW, y, { size: 10, color: BRAND_HEX.ink, width: pageW + 2 });
    doc.goTo(MARGIN_X, y, CONTENT_W, 14, section.dest);
    y += 19;
  }
}

function executiveSummary({ L, report, tz }: Ctx): void {
  L.heading("Executive summary", 1, { newPage: true, number: "1" });
  const m = keyMetrics(report);
  const rows = severityRows(report);
  const narrative = executiveNarrative(report, tz);
  narrative.sentences.forEach((line, i) => L.para(line, { size: 10, lineGap: 3, font: i === narrative.ratingIndex ? "semibold" : "regular" }));
  L.y += 6;

  // KPI tiles.
  const tiles: Array<[string, number, string]> = [
    ["Open findings", m.open, BRAND_HEX.navy],
    ["Critical and high open", m.criticalHighOpen, m.criticalHighOpen ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok],
    ["Past SLA deadline", m.slaBreached, m.slaBreached ? SEVERITY_HEX.high.fg : BRAND_HEX.ok],
    ["Assets with open findings", m.assetsAffected, BRAND_HEX.navy],
  ];
  L.ensure(70);
  const tw = (CONTENT_W - 3 * 10) / 4;
  tiles.forEach(([label, value, color], i) => {
    const x = MARGIN_X + i * (tw + 10);
    L.doc.roundedRect(x, L.y, tw, 58, 4).lineWidth(0.6).strokeColor(BRAND_HEX.rule).stroke();
    L.text(String(value), x + 12, L.y + 9, { font: "bold", size: 20, color });
    L.text(label, x + 12, L.y + 37, { font: "medium", size: 7.6, color: BRAND_HEX.muted, width: tw - 18 });
  });
  L.y += 74;

  // Severity distribution chart: open (solid) and closed (tint), per severity.
  L.heading("Findings by severity", 3);
  const max = Math.max(1, ...rows.map((r) => r.total));
  const labelW = 92;
  const barW = CONTENT_W - labelW - 80;
  L.ensure(rows.length * 22 + 26);
  rows.forEach((row) => {
    const y = L.y;
    L.text(SEVERITY_LABEL[row.severity], MARGIN_X, y + 2, { font: "medium", size: 8.8, width: labelW });
    L.doc.rect(MARGIN_X + labelW, y + 1, barW, 12).fill("#F1F3F6");
    const openW = (row.open / max) * barW;
    const closedW = (row.closed / max) * barW;
    if (openW) L.doc.rect(MARGIN_X + labelW, y + 1, openW, 12).fill(SEVERITY_HEX[row.severity].fg);
    if (closedW) L.doc.rect(MARGIN_X + labelW + openW, y + 1, closedW, 12).fill(SEVERITY_HEX[row.severity].bg);
    L.text(`${row.open} open · ${row.total} total`, MARGIN_X + labelW + barW + 8, y + 2.5, { size: 7.8, color: BRAND_HEX.muted, width: 80 });
    L.y += 20;
  });
  L.text("Solid: open or confirmed. Light: remediated, risk accepted or false positive.", MARGIN_X, L.y + 2, { font: "italic", size: 7.4, color: BRAND_HEX.muted });
  L.y += 20;

  // Status breakdown.
  const statuses = statusRows(report);
  if (statuses.length) {
    L.heading("Findings by status", 3);
    L.table(
      statuses.map((s) => ({ header: s.label, width: 1, align: "center" as const })),
      [statuses.map((s) => ({ text: String(s.count), font: "semibold" as FontName, size: 11 }))],
      { zebra: false },
    );
  }

  // Top risks.
  const top = topRisks(report, 5);
  L.heading("Top open risks", 3);
  if (top.length) {
    L.table(
      [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.8 }, { header: "Severity", width: 0.95 }, { header: "Assets", width: 1.4 }, { header: "Fix by", width: 1 }],
      top.map(({ ref, group }) => {
        const live = group.findings.filter((f) => isOpenStatus(f.status));
        const earliest = live.map((f) => f.current_sla.deadline).filter((d): d is string => Boolean(d)).sort()[0];
        return [
          { text: ref, font: "semibold" },
          group.title,
          { text: "", pill: group.severity },
          dash(groupAssets(live)),
          dash(formatDate(earliest, tz)),
        ];
      }),
    );
  } else {
    L.note("No findings are open.", "info");
  }

  // Priorities from the roadmap.
  const roadmap = remediationRoadmap(report);
  if (roadmap.length) {
    L.heading("Recommended priorities", 3);
    L.bullets(priorityLines(report));
  }
}

function scopeAndMethod({ L, report, tz }: Ctx): void {
  L.heading("Scope and methodology", 1, { newPage: true, number: "2" });
  const e = report.engagement;
  L.heading("Assessment scope", 3);
  L.keyValues([
    { label: "In scope", value: dash(e.scope_cidrs.join(", ")) },
    { label: "Excluded", value: dash(e.excluded_cidrs.join(", ")) },
    { label: "Assessment window", value: dash([formatDateTime(e.start_time, tz), formatDateTime(e.end_time, tz)].filter(Boolean).join(" – ")) },
    { label: "Lead assessor", value: dash(plainText(e.assessor)) },
    { label: "Engagement status", value: humanize(e.status) },
    { label: "Tags", value: dash(e.tags.join(", ")) },
  ], 2);
  const description = maskedText(e.description);
  if (description) {
    L.heading("Engagement description", 3);
    L.para(description);
  }
  if (e.regulatory_profiles.length) {
    L.heading("Selected regulatory profiles", 3);
    L.bullets(e.regulatory_profiles.map((p) => [p.name, p.version, p.jurisdiction].filter(Boolean).join(" · ") || "Profile name not recorded"));
  }
  const missing: string[] = [];
  for (const [key, title] of METHOD_FIELDS) {
    const value = metadataText(report, key);
    if (!value) { missing.push(title.toLowerCase()); continue; }
    L.heading(title, 3);
    L.para(value);
  }
  if (missing.length) L.note(`Not recorded in the report metadata: ${missing.join(", ")}. Absence of a recorded limitation does not establish that the assessment had none.`, "muted");
}


function findingsOverview({ L, ordered, groups, refs }: Ctx): void {
  L.heading("Findings overview", 1, { newPage: true, number: "3" });
  const repeated = groups.length < ordered.length;
  L.para(
    `${ordered.length} finding${ordered.length === 1 ? "" : "s"}${repeated ? ` across ${groups.length} distinct issue${groups.length === 1 ? "" : "s"}` : ""}, most severe first. ${repeated ? "An issue found on several assets is listed once, with its range of references (F001…)." : "References (F001…) are used throughout this report."}`,
    { color: BRAND_HEX.muted, size: 9 },
  );
  L.table(
    [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.9 }, { header: "Severity", width: 0.95 }, { header: "CVSS", width: 0.5, align: "center" }, { header: "Assets", width: 1.3 }, { header: "Status", width: 1.15 }],
    groups.map((g) => {
      const cvss = [...new Set(g.findings.map((f) => f.cvss_score).filter((v) => v !== null && v !== "").map(String))];
      return [
        { text: groupRef(g, refs), font: "semibold" },
        g.title,
        { text: "", pill: g.severity },
        cvss.length === 0 ? "—" : cvss.length === 1 ? cvss[0]! : "varies",
        dash(groupAssets(g.findings)),
        { text: statusSummary(g.findings), color: g.open ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok, font: "medium" },
      ];
    }),
    { empty: "No findings are recorded for this engagement." },
  );
}

function evidenceBlock(L: Layout, evidence: ReportEvidence, prefix: string, tz: string, maxLines = EVIDENCE_LINES): void {
  for (const artifact of evidence.artifacts) {
    const view = evidenceView(artifact, `${prefix}/E${String(artifact.index).padStart(2, "0")}`);
    const caption = [view.ref, view.label, view.tool, formatDateTime(view.capturedAt, tz)].filter(Boolean).join(" · ");
    L.ensure(60);
    L.text(caption, MARGIN_X, L.y, { font: "medium", size: 8.4, color: BRAND_HEX.navy });
    L.y += 13;
    if (view.command) {
      L.code(`$ ${view.command}`);
      L.y -= 4;
    }
    const cut = excerpt(view.content || "No evidence content recorded.", maxLines);
    const integrity = view.sha256 ? `SHA-256 ${view.sha256}${view.verified === true ? " (verified)" : view.verified === false ? " (not verified)" : ""}` : null;
    const notes = [
      cut.truncated ? `Excerpt: ${cut.shownLines} of ${cut.totalLines} lines. The complete masked evidence is in the Excel workbook (Evidence sheet).` : null,
      integrity,
    ].filter(Boolean).join("  ·  ");
    L.code(cut.text, notes || undefined);
  }
}

function findingSection(ctx: Ctx, group: IssueGroup): void {
  const { L, tz, refs } = ctx;
  const f = group.lead;
  const many = group.findings.length > 1;
  const ref = refs.get(f.id) ?? "";
  const headRef = many ? groupRef(group, refs) : ref;
  const sev = group.severity;
  const hex = SEVERITY_HEX[sev];

  // Header band.
  const titleH = L.measure(f.title, { font: "semibold", size: 13.5, width: CONTENT_W - 30 });
  // Start a finding with room for its header, facts and first section.
  L.ensure(titleH + 210);
  const top = L.y;
  L.doc.rect(MARGIN_X, top, CONTENT_W, titleH + 40).fill(hex.bg);
  L.doc.rect(MARGIN_X, top, 4, titleH + 40).fill(hex.fg);
  L.mark(`${headRef}  ${f.title}`, 2);
  L.doc.font("bold").fontSize(9);
  const refW = L.doc.widthOfString(headRef);
  L.text(headRef, MARGIN_X + 16, top + 10, { font: "bold", size: 9, color: hex.fg, width: refW + 4 });
  const pw = L.pill(sev, MARGIN_X + 24 + refW, top + 8.5);
  const statusText = many ? `${group.findings.length} affected assets · ${statusSummary(group.findings)}` : statusLabel(f.status);
  L.text(statusText, MARGIN_X + 32 + refW + pw, top + 10, { font: "medium", size: 8.4, color: group.open ? hex.fg : BRAND_HEX.ok, width: CONTENT_W - refW - pw - 50 });
  L.text(f.title, MARGIN_X + 16, top + 27, { font: "semibold", size: 13.5, color: BRAND_HEX.ink, width: CONTENT_W - 30 });
  L.y = top + titleH + 52;

  const facts = issueFacts(group, tz).map((x) => (x.label === "Affected assets" ? { ...x, value: `${x.value} (listed below)` } : x));
  if (facts.length) L.keyValues(facts.map((x) => ({ label: x.label, value: x.value, mono: x.label === "CVSS vector" })), 3, false);

  const narrative = findingNarrative(f);
  const shared = many ? sharedNarrativeKeys(group) : null;
  for (const section of narrative.sections) {
    L.heading(section.title, 3);
    if (shared && !shared.has(section.key)) L.para(`As recorded for ${ref}; other instances record this differently (see the Excel workbook).`, { font: "italic", size: 7.8, color: BRAND_HEX.muted, gap: 3 });
    L.readable(section.body);
  }

  if (f.evidence.artifacts.length) {
    L.heading(many ? `Evidence (representative, from ${ref})` : "Evidence", 3);
    evidenceBlock(L, f.evidence, ref, tz);
  }

  const rem = remediationView(f);
  if (rem.text || rem.plans.length || rem.recommendations.length) {
    L.heading("Remediation", 3);
    if (rem.text) L.para(rem.text);
    for (const plan of rem.plans) {
      if (plan.summary) L.para(`Reviewed plan: ${plan.summary}${plan.effort ? ` (effort: ${plan.effort})` : ""}`, { font: "medium" });
      if (plan.steps.length) L.bullets(plan.steps, { numbered: true });
      if (plan.verification.length) { L.para("Verify the fix:", { font: "medium", size: 9 }); L.bullets(plan.verification); }
      if (plan.longTerm.length) { L.para("Longer term:", { font: "medium", size: 9 }); L.bullets(plan.longTerm); }
      if (plan.compensating) L.para(`Compensating controls: ${plan.compensating}`);
    }
    if (rem.recommendations.length) {
      L.para("Recommendations:", { font: "medium", size: 9 });
      L.bullets(rem.recommendations);
    }
  }

  // Closure and retest (per instance; an issue on many assets lists them below).
  const c = closureView(f);
  if (!many && (c.closed || c.retest || c.reopened)) {
    L.heading("Closure and retest", 3);
    L.keyValues([
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
        ["Method", retest.method], ["Vantage point", retest.vantage_point], ["Expected result", retest.expected_result],
        ["Actual result", retest.actual_result], ["Change reference", retest.change_reference], ["Residual risk", retest.residual_risk],
      ];
      const recorded = pairs.map(([k, v]) => ({ label: k, value: plainText(typeof v === "string" ? v : v == null ? null : JSON.stringify(v)) })).filter((x) => x.value);
      if (recorded.length) L.keyValues(recorded, 2);
      if (retest.integrity_status !== "verified") {
        L.note(`Retest evidence integrity: ${humanize(retest.integrity_status)}${retest.integrity_gaps.length ? ` (${retest.integrity_gaps.join(", ")})` : ""}.`, "caution");
      }
      if (retest.before_evidence.artifacts.length || retest.after_evidence.artifacts.length) {
        evidenceBlock(L, retest.before_evidence, `${ref}/RETEST/BEFORE`, tz, 8);
        evidenceBlock(L, retest.after_evidence, `${ref}/RETEST/AFTER`, tz, 8);
      }
    }
    if (f.closure.recorded_closure_evidence.artifacts.length) {
      evidenceBlock(L, f.closure.recorded_closure_evidence, `${ref}/CLOSE`, tz, 8);
    }
  }

  if (f.compliance_mappings.length) {
    L.heading("Recorded compliance mappings", 3);
    L.bullets(f.compliance_mappings.map((m) => [
      [m.framework, m.framework_version].filter(Boolean).join(" ") || "Framework not recorded",
      [m.control_id, m.control_title].filter(Boolean).join(" "),
      m.result ?? m.assessment_status ? `recorded result: ${m.result ?? m.assessment_status}` : null,
      maskedText(m.rationale),
    ].filter(Boolean).join(" — ")));
  }

  if (many && group.findings.length > ASSET_GRID_AFTER) {
    // Long lists: three assets per row. Per-asset deadlines are in the workbook.
    L.heading(`Affected assets (${group.findings.length})`, 3);
    const per = 3;
    const rows: Cell[][] = [];
    for (let i = 0; i < group.findings.length; i += per) {
      const slice = group.findings.slice(i, i + per);
      rows.push(Array.from({ length: per }).flatMap((_, j) => {
        const x = slice[j];
        if (!x) return ["", "", ""] as Cell[];
        return [
          { text: refs.get(x.id) ?? "", font: "semibold" as FontName },
          dash(assetLabel(x)),
          { text: statusLabel(x.status), color: isOpenStatus(x.status) ? hex.fg : BRAND_HEX.ok, font: "medium" as FontName },
        ] as Cell[];
      }));
    }
    const triple = [{ header: "Ref", width: 0.55 }, { header: "Asset", width: 1.3 }, { header: "Status", width: 0.85 }];
    L.table([...triple, ...triple, ...triple], rows, { size: 7 });
    L.para("Fix-by dates and SLA state for each asset are in the Excel workbook (Findings sheet).", { font: "italic", size: 7.6, color: BRAND_HEX.muted });
  } else if (many) {
    L.heading("Affected assets", 3);
    L.table(
      [{ header: "Ref", width: 0.55 }, { header: "Asset", width: 2.2 }, { header: "Status", width: 1 }, { header: "First seen", width: 0.9 }, { header: "Fix by", width: 0.9 }, { header: "SLA", width: 0.8 }],
      group.findings.map((x) => [
        { text: refs.get(x.id) ?? "", font: "semibold" },
        dash(assetLabel(x)),
        { text: statusLabel(x.status), color: isOpenStatus(x.status) ? hex.fg : BRAND_HEX.ok, font: "medium" },
        dash(formatDate(x.first_seen, tz)),
        isOpenStatus(x.status) ? dash(formatDate(x.current_sla.deadline, tz)) : "—",
        isOpenStatus(x.status) && x.current_sla.state !== "untracked" ? humanize(x.current_sla.state) : "—",
      ]),
      { size: 7.6 },
    );
  }

  if (narrative.missing.length) {
    L.para(`Not recorded for this finding: ${narrative.missing.map((x) => x.toLowerCase()).join(", ")}.`, { font: "italic", size: 7.6, color: BRAND_HEX.muted, gap: 6 });
  }
  L.y += 18;
}

function detailedFindings(ctx: Ctx): void {
  const { L, groups, refs } = ctx;
  L.heading("Detailed findings", 1, { newPage: true, number: "4" });
  if (!groups.length) {
    L.note("No findings are recorded for this engagement.", "info");
    return;
  }
  const low = groups.filter((g) => g.severity === "low" || g.severity === "info");
  const condense = low.length > CONDENSE_LOW_AFTER;
  const paged = condense ? groups.filter((g) => !low.includes(g)) : groups;
  paged.forEach((g) => findingSection(ctx, g));
  if (condense) {
    L.heading("Low and informational observations", 2, { toc: true });
    L.para(`${low.length} low and informational issues are listed in brief. Their complete records are in the Excel workbook.`, { color: BRAND_HEX.muted, size: 9 });
    L.table(
      [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.5 }, { header: "Severity", width: 0.95 }, { header: "Assets", width: 1.2 }, { header: "Summary", width: 3 }],
      low.map((g) => [
        { text: groupRef(g, refs), font: "semibold" },
        g.title,
        { text: "", pill: g.severity },
        dash(groupAssets(g.findings)),
        (plainText(g.lead.description) || "—").slice(0, 220),
      ]),
      { size: 7.8 },
    );
  }
}

function roadmapSection({ L, report, tz }: Ctx): void {
  L.heading("Remediation roadmap", 1, { newPage: true, number: "5" });
  const roadmap = remediationRoadmap(report);
  if (!roadmap.length) {
    L.note("No findings are open, so no remediation is outstanding.", "info");
    return;
  }
  L.para("Open findings grouped by priority. Target windows come only from the current SLA policy recorded for each finding; where none is recorded, no target is shown.", { color: BRAND_HEX.muted, size: 9 });
  for (const bucket of roadmap) {
    const sev = bucket.severities[0]!;
    L.ensure(70);
    L.doc.rect(MARGIN_X, L.y + 2, 4, 15).fill(SEVERITY_HEX[sev].fg);
    L.text(bucket.title, MARGIN_X + 12, L.y + 2, { font: "semibold", size: 11.5, color: BRAND_HEX.navy });
    L.y += 20;
    L.text(`${bucket.findings} open finding${bucket.findings === 1 ? "" : "s"}${bucket.items.length < bucket.findings ? ` in ${bucket.items.length} issue${bucket.items.length === 1 ? "" : "s"}` : ""}${bucket.target ? ` · fix ${bucket.target}` : " · no SLA window recorded"}`, MARGIN_X + 12, L.y, { size: 8.4, color: BRAND_HEX.muted });
    L.y += 16;
    L.table(
      [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.6 }, { header: "Assets", width: 1.4 }, { header: "Owner", width: 1.1 }, { header: "Fix by", width: 0.95 }, { header: "SLA", width: 0.8 }],
      bucket.items.map((i) => [
        { text: i.ref, font: "semibold" },
        i.title,
        dash(i.asset),
        dash(i.owner),
        dash(formatDate(i.deadline, tz)),
        i.slaState ? { text: humanize(i.slaState), color: i.slaState === "breached" ? SEVERITY_HEX.critical.fg : i.slaState === "at_risk" ? SEVERITY_HEX.high.fg : BRAND_HEX.ink, font: "medium" } : "—",
      ]),
    );
  }
}

function closureRegister({ L, groups, refs, tz }: Ctx): void {
  L.heading("Retest and closure register", 1, { newPage: true, number: "6" });
  L.para("Disposition and retest status for every finding. “Closed” is an operational disposition: remediated, risk-accepted and false-positive records stay distinct and are not a regulatory closure conclusion.", { color: BRAND_HEX.muted, size: 9 });
  L.table(
    [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.4 }, { header: "Severity", width: 0.95 }, { header: "Disposition", width: 1.35 }, { header: "Resolved", width: 0.9 }, { header: "Retest", width: 0.85 }, { header: "Reopened", width: 0.65, align: "center" }],
    groups.map((g) => {
      const views = g.findings.map(closureView);
      const resolved = views.map((v) => v.resolvedAt).filter((d): d is string => Boolean(d)).sort();
      const passed = views.filter((v) => v.retest === "Passed").length;
      const failed = views.filter((v) => v.retest === "Failed").length;
      const retest = g.findings.length === 1
        ? views[0]!.retest
        : passed || failed ? [passed ? `${passed} passed` : null, failed ? `${failed} failed` : null].filter(Boolean).join(", ") : null;
      return [
        { text: groupRef(g, refs), font: "semibold" },
        g.title,
        { text: "", pill: g.severity },
        { text: g.findings.length === 1 ? views[0]!.disposition : statusSummary(g.findings), color: g.open ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok, font: "medium" },
        g.open === 0 && resolved.length ? dash(formatDate(resolved[resolved.length - 1], tz)) : "—",
        retest ? { text: retest, color: failed ? SEVERITY_HEX.critical.fg : BRAND_HEX.ok, font: "medium" } : "—",
        String(views.reduce((a, v) => a + v.reopened, 0)),
      ];
    }),
    { empty: "No findings are recorded." },
  );
}

function complianceSection({ L, report, refs }: Ctx): void {
  L.heading("Compliance context", 1, { newPage: true, number: "7" });
  const roll = report.compliance_rollup;
  L.heading("Recorded finding-to-control mappings", 2);
  L.note("Recorded references only. This is not a certification, audit opinion, or compliance verdict, and unrecorded controls are not inferred.", "caution");
  const controlRows = roll.frameworks.flatMap((fw) => fw.controls.map((c) => [
    [fw.framework, fw.framework_version].filter(Boolean).join(" ") || "Not recorded",
    dash(c.control_id),
    dash(c.control_title),
    dash(c.recorded_results.join(", ")),
    compactRefs(c.finding_ids.map((id) => refs.get(id) ?? id)),
  ] as Cell[]));
  L.table(
    [{ header: "Framework", width: 1.3 }, { header: "Control", width: 0.8 }, { header: "Title", width: 1.8 }, { header: "Recorded result", width: 1 }, { header: "Findings", width: 1.1 }],
    controlRows,
    { empty: roll.gap ? humanize(roll.gap) : "No finding-to-control mappings are recorded." },
  );
  if (roll.unmapped_finding_ids.length) {
    L.para(`Findings without a recorded mapping: ${compactRefs(roll.unmapped_finding_ids.map((id) => refs.get(id) ?? id))}.`, { size: 8.6, color: BRAND_HEX.muted });
  }

  const mappingGaps = new Set(report.findings.flatMap((f) => f.compliance_mappings)
    .filter((m) => m.validation_gaps.length)
    .map((m) => `${[m.framework, m.control_id].filter(Boolean).join(" ")}: ${m.validation_gaps.join(", ")}`));
  for (const line of mappingGaps) L.para(`Mapping review: ${line}`, { size: 8.4, color: BRAND_HEX.muted });

  if (roll.regulatory_profiles.length) {
    L.heading("Selected regulatory profiles", 2);
    L.note("A selected profile records applicability context only. It does not by itself establish compliance, and no conditional annexure or obligation is inferred.", "muted");
    L.table(
      [{ header: "Profile", width: 2.2 }, { header: "Version", width: 0.9 }, { header: "Jurisdiction", width: 0.9 }, { header: "Applicability", width: 2 }],
      roll.regulatory_profiles.map((p) => [dash(p.name), dash(p.version), dash(p.jurisdiction), dash(maskedText(p.applicability))]),
    );
  }

  const d = report.derived_regional_compliance;
  L.heading("Derived regional compliance context — not assessed", 2);
  L.note("Derived context only. The following profile, frameworks, obligations, and reporting clocks are not assessed control results, a certification, an attestation, or legal advice.", "caution");
  const sector = typeof d.profile.sector === "string" ? humanize(d.profile.sector) : null;
  const jurisdictions = Array.isArray(d.profile.jurisdictions) ? d.profile.jurisdictions.filter((x): x is string => typeof x === "string").join(", ") : null;
  L.keyValues([
    { label: "Profile basis", value: humanize(d.profile_source) },
    { label: d.profile_source === "recorded_engagement_profile" ? "Configured sector" : "Default sector", value: dash(sector) },
    { label: "Jurisdictions", value: dash(jurisdictions) },
    { label: "Asset tags considered", value: dash(d.asset_tags.join(", ")) },
  ], 2);
  L.table(
    [{ header: "Framework", width: 1.8 }, { header: "Authority", width: 1.6 }, { header: "Basis", width: 0.9 }, { header: "Source reference", width: 2.2 }],
    d.frameworks.map((fw) => [fw.name, fw.authority, fw.tag_triggered ? "Asset tag" : "Profile", fw.source_reference]),
    { empty: "No regional frameworks were derived for this profile.", size: 7.8 },
  );
  if (d.reporting_clocks.length) {
    L.heading("Contextual reporting clocks", 3);
    L.table(
      [{ header: "Framework", width: 1.7 }, { header: "Deadline", width: 0.7 }, { header: "Trigger", width: 1.8 }, { header: "Reference", width: 2 }],
      d.reporting_clocks.map((c) => [c.framework, `${c.deadline_hours} hours`, c.trigger, c.reference]),
      { size: 7.8 },
    );
    L.para("A listed reporting deadline is a contextual trigger reference; this report does not assert that an incident or notification trigger occurred.", { size: 8, color: BRAND_HEX.muted });
  }
  L.para(d.disclaimer, { size: 8, color: BRAND_HEX.muted });
}

function appendices(ctx: Ctx): void {
  const { L, report, ordered, refs, tz } = ctx;

  L.heading("Appendix A — Risk rating", 1, { newPage: true });
  L.para("Severity follows the FIRST CVSS v3.1 qualitative scale. Where an assessor recorded a different rating method, it is stated below.", { size: 9 });
  L.table(
    [{ header: "Severity", width: 0.9 }, { header: "CVSS v3.1", width: 0.8 }, { header: "Meaning", width: 3.4 }],
    SEVERITY_DEFINITIONS.map((d) => [{ text: "", pill: d.severity }, d.cvss, d.meaning]),
  );
  const method = metadataText(report, "risk_rating_method");
  if (method) L.para(`Recorded rating method: ${method}`, { size: 9 });
  L.para("Overall risk is the highest severity among findings that are still open or confirmed.", { size: 9, color: BRAND_HEX.muted });

  L.heading("Appendix B — Derived control pointers by finding — not assessed", 1, { newPage: true });
  L.note("Derived compliance context — not assessed. These pointers are separate from recorded mappings and are not a certification, attestation, legal conclusion, or recorded control result.", "caution");
  const pointerRows: Cell[][] = [];
  for (const g of ctx.groups) {
    const ctxd = g.lead.derived_compliance_context;
    const ref = { text: groupRef(g, refs), font: "semibold" as FontName };
    for (const p of ctxd.global_framework_pointers) pointerRows.push([ref, p.framework, p.controls.join(", "), humanize(ctxd.category)]);
    for (const o of ctxd.regional_obligations) pointerRows.push([ref, o.framework, o.controls.join(", "), humanize(ctxd.category)]);
  }
  L.table(
    [{ header: "Ref", width: 0.7 }, { header: "Framework", width: 1.8 }, { header: "Control pointers", width: 2.3 }, { header: "Category", width: 1 }],
    pointerRows,
    { size: 7.6, empty: "No control pointers were derived." },
  );
  const generic = ordered.filter((f) => f.derived_compliance_context.used_generic_fallback);
  if (generic.length) {
    L.note(`Generic fallback warning: ${compactRefs(generic.map((f) => refs.get(f.id) ?? ""))} used the generic control-pointer set. Confirm the classification and control applicability before customer delivery.`, "caution");
  }

  L.heading("Appendix C — Evidence integrity and provenance", 1, { newPage: true });
  if (ordered.length <= PROVENANCE_DETAIL_MAX) {
    L.para("Detection runs and evidence hashes for each finding, so any excerpt in this report can be traced to the scan that produced it.", { size: 9 });
    L.table(
      [{ header: "Ref", width: 0.5 }, { header: "Initial discovery run", width: 1.6 }, { header: "Latest observation run", width: 1.6 }, { header: "Evidence SHA-256", width: 2.2 }],
      ordered.map((f) => [
        { text: refs.get(f.id) ?? "", font: "semibold" },
        { text: f.initial_detection_provenance ? `${f.initial_detection_provenance.run_id}\n${dash(f.initial_detection_provenance.scan_type)} · ${dash(formatDate(f.initial_detection_provenance.started_at, tz))}` : dash(f.initial_detection_run_id), font: "mono", size: 6.6 },
        { text: f.latest_detection_provenance ? `${f.latest_detection_provenance.run_id}\n${dash(f.latest_detection_provenance.scan_type)} · ${dash(formatDate(f.latest_detection_provenance.started_at, tz))}` : dash(f.detection_run_id), font: "mono", size: 6.6 },
        { text: f.evidence.artifacts.map((a) => `E${String(a.index).padStart(2, "0")} ${short(a.sha256)}${a.sha256_verified ? " ✓" : ""}`).join("\n") || "No evidence recorded", font: "mono", size: 6.6 },
      ]),
      { size: 7 },
    );
  } else {
    L.para(`Summary per issue. Per-finding detection runs and evidence hashes for all ${ordered.length} findings are in the Excel workbook (Findings and Evidence sheets).`, { size: 9 });
    L.table(
      [{ header: "Ref", width: 0.75 }, { header: "Finding", width: 2.6 }, { header: "Detection runs", width: 0.9, align: "center" }, { header: "Evidence items", width: 0.9, align: "center" }, { header: "Hash verified", width: 0.9, align: "center" }],
      ctx.groups.map((g) => {
        const runs = new Set(g.findings.flatMap((f) => [f.initial_detection_run_id, f.detection_run_id]).filter(Boolean));
        const artifacts = g.findings.flatMap((f) => f.evidence.artifacts);
        return [
          { text: groupRef(g, refs), font: "semibold" },
          g.title,
          String(runs.size),
          String(artifacts.length),
          artifacts.length ? `${artifacts.filter((a) => a.sha256_verified).length} of ${artifacts.length}` : "—",
        ];
      }),
      { size: 7.6 },
    );
  }

  const gaps = gapInventory(report);
  L.heading("Appendix D — Record readiness", 1, { newPage: true });
  L.para(report.readiness.complete
    ? "No configured completeness gaps were identified. This does not constitute approval for delivery."
    : "The live record contains gaps that need operator review before customer delivery. Each gap is listed once, with the findings it affects.", { size: 9 });
  if (gaps.reportLevel.length) {
    L.heading("Report-level gaps", 3);
    L.bullets(gaps.reportLevel.map((g) => `${g.label} (${g.code})`));
  }
  if (gaps.findingLevel.length) {
    L.heading("Finding-level gaps", 3);
    L.table(
      [{ header: "Gap", width: 2.2 }, { header: "Count", width: 0.5, align: "center" }, { header: "Findings", width: 2.2 }],
      gaps.findingLevel.map((g) => [`${g.label}\n${g.code}`, String(g.count), compactRefs(g.refs)]),
      { size: 7.8 },
    );
  }

  L.heading("Appendix E — About this document", 1, { newPage: true });
  L.keyValues([
    { label: "Engagement ID", value: report.engagement.id, mono: true },
    { label: "Schema version", value: report.document.schema_version },
    { label: "Generated (UTC)", value: report.document.generated_at, mono: true },
    { label: "Display time zone", value: tz },
    { label: "Snapshot", value: `${report.document.snapshot_kind} · guarantee: ${report.document.snapshot_guarantee}` },
    { label: "Persisted report record", value: report.document.persisted ? "Yes" : "No" },
  ], 2);
  L.para("This report is generated from the live canonical record at the time shown. Unless the document status records an approved issue, it is a draft for review, not an approved, signed, or immutable deliverable.", { size: 8.6, color: BRAND_HEX.muted });
}

function chrome(L: Layout, report: ReportDocument, issued: boolean): void {
  const doc = L.doc;
  const range = doc.bufferedPageRange();
  const classification = metadataText(report, "classification") ?? "Confidential";
  const client = plainText(report.engagement.client);
  for (let i = range.start; i < range.start + range.count; i++) {
    doc.switchToPage(i);
    if (!issued) {
      doc.save();
      doc.rotate(-35, { origin: [PAGE_W / 2, PAGE_H / 2] });
      doc.font("bold").fontSize(96).fillColor("#0F172A").fillOpacity(0.035);
      doc.text("DRAFT", 0, PAGE_H / 2 - 50, { width: PAGE_W, align: "center", lineBreak: false });
      doc.restore();
      doc.fillOpacity(1);
    }
    if (i === range.start) continue;
    doc.font("medium").fontSize(7.4).fillColor(BRAND_HEX.muted);
    doc.text(`VEDHA  ·  ${report.engagement.name}`, MARGIN_X, 36, { width: CONTENT_W * 0.7, lineBreak: false });
    doc.text(classification.toUpperCase(), MARGIN_X, 36, { width: CONTENT_W, align: "right", lineBreak: false });
    doc.moveTo(MARGIN_X, 50).lineTo(PAGE_W - MARGIN_X, 50).lineWidth(0.5).strokeColor(BRAND_HEX.rule).stroke();
    doc.moveTo(MARGIN_X, 796).lineTo(PAGE_W - MARGIN_X, 796).lineWidth(0.5).strokeColor(BRAND_HEX.rule).stroke();
    doc.font("regular").fontSize(7.4).fillColor(BRAND_HEX.muted);
    doc.text(`${client ? `${client} — ` : ""}Vulnerability assessment report${issued ? "" : " — draft"}`, MARGIN_X, 803, { width: CONTENT_W * 0.7, lineBreak: false });
    doc.text(`Page ${i - range.start + 1} of ${range.count}`, MARGIN_X, 803, { width: CONTENT_W, align: "right", lineBreak: false });
  }
}

// ─── Entry point ─────────────────────────────────────────────────────────────

export interface RenderedPdf { bytes: Buffer; text: string[] }

export function renderReportPdf(report: ReportDocument): Promise<RenderedPdf> {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({
      autoFirstPage: false,
      bufferPages: true,
      compress: true,
      pdfVersion: "1.4",
      size: "A4",
      info: {
        Title: `${plainText(report.engagement.name)} — vulnerability assessment report`,
        Author: "Vedha VAPT Platform",
        Subject: "Security assessment findings, evidence, remediation, closure and compliance",
        CreationDate: new Date(report.document.generated_at),
      },
      displayTitle: true,
    });
    const chunks: Buffer[] = [];
    doc.on("data", (chunk: Buffer | Uint8Array) => chunks.push(Buffer.from(chunk)));
    doc.once("error", reject);

    const L = new Layout(doc);
    const tz = usableTimeZone(report.document.display_timezone);
    const ordered = orderFindings(report.findings);
    const ctx: Ctx = { L, report, tz, refs: findingRefs(report), ordered, groups: issueGroups(report.findings), issued: isIssued(report) };

    try {
      cover(ctx);
      const tocTop = documentControl(ctx);
      const tocPage = L.pageNumber();
      executiveSummary(ctx);
      scopeAndMethod(ctx);
      findingsOverview(ctx);
      detailedFindings(ctx);
      roadmapSection(ctx);
      closureRegister(ctx);
      complianceSection(ctx);
      appendices(ctx);
      drawContents(L, tocPage, tocTop);
      chrome(L, report, ctx.issued);
    } catch (error) {
      reject(error);
      return;
    }
    doc.once("end", () => resolve({ bytes: Buffer.concat(chunks), text: L.trace }));
    doc.end();
  });
}
