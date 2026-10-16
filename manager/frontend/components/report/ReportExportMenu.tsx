"use client";

import React, { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import {
  CheckCircle2,
  ChevronDown,
  Download,
  FileSpreadsheet,
  FileText,
  Loader2,
  Printer,
  Sheet,
} from "lucide-react";
import type { ReportExportFormat } from "../../lib/report/export-files";

const OPTIONS: Array<{
  format: ReportExportFormat;
  label: string;
  description: string;
  icon: React.ElementType;
}> = [
  { format: "pdf", label: "PDF report", description: "Paginated delivery copy", icon: FileText },
  { format: "docx", label: "Word document", description: "Editable review copy", icon: FileText },
  { format: "xlsx", label: "Excel workbook", description: "Multi-sheet evidence workbook", icon: FileSpreadsheet },
  { format: "csv", label: "CSV tracker", description: "Flat tracker without evidence bodies", icon: Sheet },
];

export type ReportPrintMode = "customer" | "full";

const PRINT_OPTIONS: Array<{ mode: ReportPrintMode; label: string; description: string }> = [
  { mode: "customer", label: "Print customer copy", description: "The reading view, without the operator readiness check" },
  { mode: "full", label: "Print complete record", description: "Everything, with every finding's full record open" },
];

function responseFilename(header: string | null, fallback: string): string {
  const encoded = header?.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
  if (encoded) {
    try { return decodeURIComponent(encoded); } catch { /* use fallback */ }
  }
  const ascii = header?.match(/filename="([^"]+)"/i)?.[1];
  return ascii || fallback;
}

const GUTTER = 14;
const MENU_WIDTH = 280;

/** Where the format list opens, in viewport coordinates: 8 px under the
 *  button, right-aligned to it, never past the screen's 14 px gutter. The list
 *  is portaled to <body> because the PageShell header clips overflow — opened
 *  in place it was cut off out of sight, so "Export" appeared to do nothing. */
export function exportMenuPosition(
  button: { left: number; right: number; bottom: number },
  viewportWidth: number,
): { top: number; left: number; width: number } {
  const width = Math.min(MENU_WIDTH, viewportWidth - GUTTER * 2);
  const left = Math.max(GUTTER, Math.min(button.right - width, viewportWidth - width - GUTTER));
  return { top: button.bottom + 8, left, width };
}

export function ReportExportMenu({ engagementId, disabled = false, onPrint }: {
  engagementId?: string;
  disabled?: boolean;
  /** When given, the menu also offers the two print copies, so the page header
   *  carries one control instead of three (three overflowed a phone). */
  onPrint?: (mode: ReportPrintMode) => void;
}) {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const [menuAt, setMenuAt] = useState<{ top: number; left: number; width: number } | null>(null);
  const [active, setActive] = useState<ReportExportFormat | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function download(format: ReportExportFormat) {
    if (!engagementId || active) return;
    setActive(format);
    setError("");
    setMessage(`Preparing ${format.toUpperCase()}…`);
    setMenuAt(null);

    try {
      const response = await fetch("/api/reports/export", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format, engagementId }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null) as { error?: string } | null;
        throw new Error(body?.error || `Export failed (${response.status}).`);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = responseFilename(
        response.headers.get("content-disposition"),
        `vedha-report.${format}`,
      );
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
      setMessage(`${format.toUpperCase()} downloaded.`);
    } catch (cause) {
      setMessage("");
      setError(cause instanceof Error ? cause.message : "The report could not be exported.");
    } finally {
      setActive(null);
    }
  }

  const unavailable = disabled || !engagementId || Boolean(active);
  const open = menuAt !== null;

  function toggle() {
    if (unavailable) return;
    if (open) { setMenuAt(null); return; }
    const rect = buttonRef.current?.getBoundingClientRect();
    if (rect) setMenuAt(exportMenuPosition(rect, window.innerWidth));
  }

  // Close on an outside press, Escape, scroll or resize (the list is fixed to
  // where the button was when it opened).
  useEffect(() => {
    if (!open) return;
    const close = () => setMenuAt(null);
    const onPointerDown = (event: PointerEvent) => {
      const target = event.target as Node;
      if (menuRef.current?.contains(target) || buttonRef.current?.contains(target)) return;
      close();
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      close();
      buttonRef.current?.focus();
    };
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    window.addEventListener("resize", close);
    window.addEventListener("scroll", close, true);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("resize", close);
      window.removeEventListener("scroll", close, true);
    };
  }, [open]);

  return (
    <div className="cr-export-control no-print">
      <button
        ref={buttonRef}
        type="button"
        className="btn btn-secondary cr-export-trigger"
        aria-label={onPrint ? "Export or print report" : "Export report"}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-disabled={unavailable}
        onClick={toggle}
      >
        {active ? <Loader2 size={14} className="spin" aria-hidden /> : <Download size={14} aria-hidden />}
        {onPrint ? "Export & print" : "Export"}
        <ChevronDown size={13} aria-hidden />
      </button>
      {menuAt && createPortal(
        <div
          ref={menuRef}
          className="cr-export-popover no-print"
          role="menu"
          aria-label="Report export formats"
          style={{ position: "fixed", top: menuAt.top, left: menuAt.left, right: "auto", width: menuAt.width }}
        >
          {onPrint && (
            <>
              <div className="cr-export-group" role="presentation">Print</div>
              {PRINT_OPTIONS.map(({ mode, label, description }) => (
                <button
                  key={mode}
                  type="button"
                  role="menuitem"
                  onClick={() => { setMenuAt(null); onPrint(mode); }}
                >
                  <Printer size={16} aria-hidden />
                  <span><strong>{label}</strong><small>{description}</small></span>
                </button>
              ))}
              <div className="cr-export-group" role="presentation">Download</div>
            </>
          )}
          {OPTIONS.map(({ format, label, description, icon: Icon }) => (
            <button
              key={format}
              type="button"
              role="menuitem"
              disabled={Boolean(active)}
              onClick={() => void download(format)}
            >
              <Icon size={16} aria-hidden />
              <span><strong>{label}</strong><small>{description}</small></span>
            </button>
          ))}
        </div>,
        document.body,
      )}
      <span className="cr-export-status" data-error={Boolean(error) || undefined} aria-live="polite">
        {error || (message && <><CheckCircle2 size={12} aria-hidden />{message}</>)}
      </span>
    </div>
  );
}
