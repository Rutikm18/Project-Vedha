"use client";

/**
 * RawFacts — "what did the scanner actually collect?" inspection view.
 *
 * Drop in:  <RawFacts engagementId={id} />
 *
 * Renders, from GET /api/engagements/{id}/raw-facts, the RAW ScanResult facts
 * exactly as the vedha-agent / main_scripts submitted them — the ground truth
 * that feeds detection. This is deliberately separate from the findings view:
 * findings are the manager's *conclusions*; this is the *evidence* the probe sent.
 *
 * Collapsed and un-fetched by default (facts can be large); loads on first open.
 * A scanner filter narrows to one scanner (e.g. smb_scan, rdp_scan) and each
 * submission's facts are shown verbatim as pretty JSON.
 */
import { useCallback, useMemo, useState } from "react";
import { ChevronDown } from "lucide-react";
import { CAMPAIGN_CSS } from "../../../components/campaign/campaign-css";
import { createScannerWorkspaceApi, type ScannerWorkspaceSurface } from "../../../lib/scanner-workspace-api";

interface ScanResultRow {
  id: string; job_id: string | null; agent_id: string | null;
  scan_type: string | null; fact_count: number | null; validation_state: string | null;
  created_at: string | null; by_scanner: Record<string, number>;
  facts: unknown[]; truncated: boolean;
}
interface RawFactsResp {
  engagement_id: string; scanners: string[];
  by_scanner: Record<string, number>; scan_results: ScanResultRow[];
}

export default function RawFacts({ engagementId, surface = "manager" }: {
  engagementId: string;
  surface?: ScannerWorkspaceSurface;
}) {
  const api = useMemo(() => createScannerWorkspaceApi(surface), [surface]);
  const [open, setOpen] = useState(false);
  const [data, setData] = useState<RawFactsResp | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [scanner, setScanner] = useState<string>("");        // "" = all scanners
  const [openRows, setOpenRows] = useState<Record<string, boolean>>({});

  const load = useCallback(async (scannerFilter: string) => {
    setLoading(true); setErr(null);
    try {
      const q = scannerFilter ? `?scanner=${encodeURIComponent(scannerFilter)}` : "";
      setData(await api.rawFacts<RawFactsResp>(engagementId, q));
    } catch (e) { setErr((e as Error).message); }
    finally { setLoading(false); }
  }, [api, engagementId]);

  const toggle = () => {
    const next = !open;
    setOpen(next);
    if (next && !data && !loading) void load(scanner);
  };

  const pickScanner = (s: string) => {
    setScanner(s);
    void load(s);
  };

  const total = data ? Object.values(data.by_scanner).reduce((a, b) => a + b, 0) : 0;
  return (
    <div className="cpg-card" style={{ overflow: "hidden" }}>
      <style>{CAMPAIGN_CSS}</style>
      <button type="button" className="cpg-raw-toggle" aria-expanded={open} aria-controls="cpg-raw-body" onClick={toggle}>
        <span className="cpg-raw-text">
          <strong>Raw scanner data</strong>
          <span>What the vedha-agent actually collected, verbatim</span>
        </span>
        <ChevronDown size={14} aria-hidden />
      </button>

      {open && (
        <div id="cpg-raw-body" className="cpg-raw-body">
          {err && <p className="cpg-err" role="alert" style={{ marginTop: 12 }}>Failed to load raw facts: {err}</p>}
          {loading && !data && <p className="cpg-dim" style={{ marginTop: 12 }}>Loading raw facts…</p>}
          {data && (
            <>
              {/* scanner filter: chips built from the full by_scanner breakdown */}
              <div className="cpg-chips" role="group" aria-label="Filter by scanner">
                <button type="button" aria-pressed={scanner === ""} onClick={() => pickScanner("")}>all · {total}</button>
                {data.scanners.map((s) => (
                  <button key={s} type="button" aria-pressed={scanner === s} onClick={() => pickScanner(s)}>
                    {s} · {data.by_scanner[s] ?? 0}
                  </button>
                ))}
                {data.scanners.length === 0 && <span className="cpg-dim">No facts submitted yet.</span>}
              </div>

              {/* one card per submission (ScanResult) */}
              <div className="cpg-jobs">
                {data.scan_results.map((r) => {
                  const isOpen = !!openRows[r.id];
                  return (
                    <div key={r.id} className="cpg-sub">
                      <button type="button" aria-expanded={isOpen}
                        onClick={() => setOpenRows((o) => ({ ...o, [r.id]: !o[r.id] }))}>
                        <strong>{r.scan_type ?? "scan"}</strong>
                        <span className="cpg-dim"><b>{r.fact_count ?? r.facts.length}</b> facts</span>
                        {r.validation_state && <span className="cpg-chip" data-tone="accent">{r.validation_state}</span>}
                        {r.job_id && <span className="cpg-dim cpg-mono">job {r.job_id.slice(0, 8)}</span>}
                        {r.created_at && <span className="cpg-dim">{new Date(r.created_at).toLocaleString()}</span>}
                        <em aria-hidden>{isOpen ? "▾" : "▸"}</em>
                      </button>
                      {/* per-submission scanner breakdown */}
                      <div className="cpg-scanners">
                        {Object.entries(r.by_scanner).map(([s, n]) => <span key={s}>{s}·{n}</span>)}
                      </div>
                      {isOpen && (
                        <>
                          {r.truncated && <p className="cpg-dim" style={{ margin: "0 14px 6px", color: "var(--sev-medium-color)" }}>Facts truncated. Use the scanner or job filters to narrow.</p>}
                          <pre>{JSON.stringify(r.facts, null, 2)}</pre>
                        </>
                      )}
                    </div>
                  );
                })}
                {data.scan_results.length === 0 && !err && (
                  <p className="cpg-empty">No scan submissions recorded for this engagement yet.</p>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
