"use client";

/**
 * ExportMenu — one "Export" control for every report format.
 *
 *   PDF   — the browser's print pipeline over the full report (print mode:
 *           every finding open, no filters, light theme). "Save as PDF".
 *   Word  — the same rendered report, flattened to a .doc Word opens.
 *   Excel — the remediation tracker workbook (all findings, not the 100 the
 *           page renders): By fix · By host checklist · Findings.
 *   CSV   — the findings register as a single .csv.
 */
import { useEffect, useRef, useState } from "react";
import { ChevronDown, Download, FileSpreadsheet, FileText, FileType2, Printer, RefreshCw } from "lucide-react";

type Format = "pdf" | "word" | "xlsx" | "csv";

const ITEMS: Array<{ id: Format; label: string; hint: string; Icon: typeof Printer }> = [
  { id: "pdf",  label: "PDF",            hint: "Full report — choose “Save as PDF”", Icon: Printer },
  { id: "word", label: "Word (.doc)",    hint: "Full report, editable",              Icon: FileText },
  { id: "xlsx", label: "Excel (.xlsx)",  hint: "All findings + remediation tracker", Icon: FileSpreadsheet },
  { id: "csv",  label: "CSV (.csv)",     hint: "All findings, one row each",         Icon: FileType2 },
];

export function ExportMenu({ disabled, onExport }: {
  disabled?: boolean;
  /** Resolve when the export is done; reject with a readable Error. */
  onExport: (format: Format) => Promise<void> | void;
}) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState<Format | null>(null);
  const [error, setError] = useState<string | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => { if (!ref.current?.contains(e.target as Node)) setOpen(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  const run = async (format: Format) => {
    setOpen(false);
    setError(null);
    setBusy(format);
    // Let the menu close and the spinner paint before a synchronous export
    // (print dialog, Word capture) blocks the main thread.
    await new Promise(r => setTimeout(r, 30));
    try {
      await onExport(format);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(null);
    }
  };

  return (
    <div ref={ref} className="report-export no-print">
      <button
        type="button"
        className="btn btn-secondary"
        disabled={disabled || busy !== null}
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen(o => !o)}
      >
        {busy ? <RefreshCw size={14} className="spin" /> : <Download size={14} />}
        {busy ? "Exporting…" : "Export"}
        <ChevronDown size={13} />
      </button>
      {open && (
        <div className="report-export-menu" role="menu">
          {ITEMS.map(({ id, label, hint, Icon }) => (
            <button key={id} type="button" role="menuitem" onClick={() => void run(id)}>
              <Icon size={15} aria-hidden />
              <span><strong>{label}</strong><small>{hint}</small></span>
            </button>
          ))}
        </div>
      )}
      {error && (
        <div className="report-export-error" role="alert">
          {error}
          <button type="button" aria-label="Dismiss" onClick={() => setError(null)}>×</button>
        </div>
      )}
    </div>
  );
}

export type { Format as ExportFormat };
