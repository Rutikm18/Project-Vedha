"use client";

import React, { useEffect, useRef } from "react";
import {
  AlertTriangle,
  Download,
  FileCode2,
  LoaderCircle,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";

import {
  downloadRemediationArtifact,
  type RemediationWorkspacePreview,
} from "../../lib/remediation-workspace.client";

interface Props {
  preview: RemediationWorkspacePreview | null;
  loading: boolean;
  error: string | null;
  selectedCount: number;
  includeAdvisory: boolean;
  onIncludeAdvisoryChange: (value: boolean) => void;
  onGenerate: () => void;
  onClose: () => void;
}

function shortHash(value: string): string {
  return `${value.slice(0, 12)}…${value.slice(-8)}`;
}

function artifactLabel(format: string): string {
  if (format === "powershell") return "PowerShell";
  if (format === "bash") return "Bash";
  return "Manual runbook";
}

export function RemediationWorkspaceDialog({
  preview,
  loading,
  error,
  selectedCount,
  includeAdvisory,
  onIncludeAdvisoryChange,
  onGenerate,
  onClose,
}: Props) {
  const dialogRef = useRef<HTMLElement>(null);
  useEffect(() => {
    const previous = document.activeElement instanceof HTMLElement
      ? document.activeElement
      : null;
    dialogRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab" || !dialogRef.current) return;
      const focusable = [...dialogRef.current.querySelectorAll<HTMLElement>(
        "button:not(:disabled), input:not(:disabled), summary, [href], [tabindex]:not([tabindex='-1'])",
      )];
      if (focusable.length === 0) {
        event.preventDefault();
        dialogRef.current.focus();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      previous?.focus();
    };
  }, [onClose]);

  return (
    <div className="remediation-workspace-layer">
      <button
        type="button"
        className="remediation-workspace-backdrop"
        onClick={onClose}
        aria-label="Close remediation workspace"
      />
      <section
        ref={dialogRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-busy={loading}
        aria-labelledby="remediation-workspace-title"
        className="remediation-workspace-dialog"
      >
        <header className="remediation-workspace-header">
          <div>
            <span><FileCode2 size={17} aria-hidden /></span>
            <div>
              <h2 id="remediation-workspace-title">Remediation workspace</h2>
              <p>{selectedCount} selected finding{selectedCount === 1 ? "" : "s"} · review-only preview</p>
            </div>
          </div>
          <button type="button" onClick={onClose} aria-label="Close remediation workspace">
            <X size={17} aria-hidden />
          </button>
        </header>

        <div className="remediation-workspace-body">
          <div className="remediation-workspace-safety" role="note">
            <ShieldCheck size={17} aria-hidden />
            <div>
              <strong>Executable bytes come from reviewed templates, not the model.</strong>
              <p>Files start in check mode. Apply requires the exact context hash shown in the artifact. Vedha has not executed or approved a change.</p>
            </div>
          </div>

          <div className="remediation-workspace-controls">
            <label>
              <input
                type="checkbox"
                checked={includeAdvisory}
                onChange={(event) => onIncludeAdvisoryChange(event.target.checked)}
              />
              <span><Sparkles size={13} aria-hidden /> Add an AI operational summary</span>
            </label>
            <button type="button" onClick={onGenerate} disabled={loading}>
              <RefreshCw size={13} className={loading ? "findings-spinner" : undefined} aria-hidden />
              {preview ? "Regenerate" : "Generate preview"}
            </button>
          </div>

          {loading && (
            <div className="remediation-workspace-loading" aria-live="polite">
              <LoaderCircle className="findings-spinner" size={19} aria-hidden />
              Resolving current findings and compiling safe artifacts…
            </div>
          )}

          {error && (
            <div className="remediation-workspace-error" role="alert">
              <AlertTriangle size={16} aria-hidden />
              <div><strong>Preview could not be built</strong><p>{error}</p></div>
            </div>
          )}

          {preview && (
            <>
              <dl className="remediation-workspace-summary">
                <div><dt>Findings</dt><dd>{preview.finding_count}</dd></div>
                <div><dt>Operations</dt><dd>{preview.operation_count}</dd></div>
                <div><dt>Artifacts</dt><dd>{preview.artifacts.length}</dd></div>
                <div><dt>Manual blockers</dt><dd>{preview.blocked.length}</dd></div>
              </dl>

              <div className="remediation-workspace-identity">
                <span>Catalog <code>{preview.catalog_version}</code></span>
                <span title={preview.context_sha256}>Context <code>{shortHash(preview.context_sha256)}</code></span>
              </div>

              {preview.advisory && (
                <section className="remediation-workspace-advisory">
                  <h3><Sparkles size={14} aria-hidden /> AI advisory</h3>
                  <p>{preview.advisory.summary}</p>
                  {preview.advisory.notes.map((note) => <small key={note}>{note}</small>)}
                </section>
              )}

              {(preview.warnings.length > 0 || preview.blocked.length > 0) && (
                <section className="remediation-workspace-blockers">
                  <h3><AlertTriangle size={14} aria-hidden /> Requires human review</h3>
                  {preview.warnings.map((warning) => <p key={warning}>{warning}</p>)}
                  {preview.blocked.map((blocked) => (
                    <p key={blocked.finding_id}>
                      <code>{blocked.finding_id.slice(0, 8)}</code> — {blocked.detail}
                    </p>
                  ))}
                </section>
              )}

              <section className="remediation-workspace-artifacts" aria-label="Generated remediation artifacts">
                {preview.artifacts.map((artifact) => (
                  <article key={artifact.artifact_id}>
                    <header>
                      <div>
                        <span>{artifactLabel(artifact.format)}</span>
                        <strong>{artifact.filename}</strong>
                        <small>{artifact.os_family} · {artifact.finding_ids.length} finding{artifact.finding_ids.length === 1 ? "" : "s"}</small>
                      </div>
                      <button type="button" onClick={() => downloadRemediationArtifact(artifact)}>
                        <Download size={14} aria-hidden /> Download
                      </button>
                    </header>
                    <div className="remediation-workspace-hash" title={artifact.content_sha256}>
                      SHA-256 <code>{shortHash(artifact.content_sha256)}</code>
                    </div>
                    <details>
                      <summary>Review file contents</summary>
                      <pre><code>{artifact.content}</code></pre>
                    </details>
                  </article>
                ))}
              </section>
            </>
          )}
        </div>
      </section>
    </div>
  );
}
