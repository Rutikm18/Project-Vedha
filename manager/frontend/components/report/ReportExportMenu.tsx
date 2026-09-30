"use client";

import React, { useRef, useState } from "react";
import {
  CheckCircle2,
  ChevronDown,
  Download,
  FileSpreadsheet,
  FileText,
  Loader2,
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

function responseFilename(header: string | null, fallback: string): string {
  const encoded = header?.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
  if (encoded) {
    try { return decodeURIComponent(encoded); } catch { /* use fallback */ }
  }
  const ascii = header?.match(/filename="([^"]+)"/i)?.[1];
  return ascii || fallback;
}

export function ReportExportMenu({ engagementId, disabled = false }: {
  engagementId?: string;
  disabled?: boolean;
}) {
  const detailsRef = useRef<HTMLDetailsElement>(null);
  const [active, setActive] = useState<ReportExportFormat | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function download(format: ReportExportFormat) {
    if (!engagementId || active) return;
    setActive(format);
    setError("");
    setMessage(`Preparing ${format.toUpperCase()}…`);
    if (detailsRef.current) detailsRef.current.open = false;

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

  return (
    <div className="cr-export-control no-print">
      <details ref={detailsRef} className="cr-export-menu">
        <summary
          className="btn btn-secondary"
          aria-label="Export report"
          aria-disabled={disabled || !engagementId || Boolean(active)}
          onClick={(event) => {
            if (disabled || !engagementId || active) event.preventDefault();
          }}
        >
          {active ? <Loader2 size={14} className="spin" aria-hidden /> : <Download size={14} aria-hidden />}
          Export
          <ChevronDown size={13} aria-hidden />
        </summary>
        <div className="cr-export-popover" role="menu" aria-label="Report export formats">
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
        </div>
      </details>
      <span className="cr-export-status" data-error={Boolean(error) || undefined} aria-live="polite">
        {error || (message && <><CheckCircle2 size={12} aria-hidden />{message}</>)}
      </span>
    </div>
  );
}
