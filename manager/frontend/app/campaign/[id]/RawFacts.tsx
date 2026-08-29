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
import { useCallback, useState } from "react";

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

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "same-origin" });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((body as { error?: string }).error ?? res.statusText);
  return body as T;
}

export default function RawFacts({ engagementId }: { engagementId: string }) {
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
      setData(await fetchJson<RawFactsResp>(`/api/engagements/${engagementId}/raw-facts${q}`));
    } catch (e) { setErr((e as Error).message); }
    finally { setLoading(false); }
  }, [engagementId]);

  const toggle = () => {
    const next = !open;
    setOpen(next);
    if (next && !data && !loading) void load(scanner);
  };

  const pickScanner = (s: string) => {
    setScanner(s);
    void load(s);
  };

  return (
    <div style={{ borderRadius: 12, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
      <button onClick={toggle}
        style={{ width: "100%", display: "flex", alignItems: "center", gap: 10, padding: "12px 16px", cursor: "pointer", background: "transparent", border: "none", textAlign: "left" }}>
        <span style={{ fontSize: 12.5, fontWeight: 700, color: "var(--text-primary)" }}>Raw scanner data</span>
        <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>what the vedha-agent actually collected — verbatim facts</span>
        <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-faint)" }}>{open ? "▾" : "▸"}</span>
      </button>

      {open && (
        <div style={{ padding: "0 16px 16px", borderTop: "0.5px solid var(--border-subtle)" }}>
          {err && <div style={{ color: "var(--sev-high,#f97316)", fontSize: 12, marginTop: 12 }}>Failed to load raw facts: {err}</div>}
          {loading && !data && <div style={{ color: "var(--text-muted)", fontSize: 12, marginTop: 12 }}>Loading raw facts…</div>}
          {data && (
            <>
              {/* scanner filter — chips built from the full by_scanner breakdown */}
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 12, marginBottom: 12 }}>
                <Chip label={`all · ${Object.values(data.by_scanner).reduce((a, b) => a + b, 0)}`}
                  active={scanner === ""} onClick={() => pickScanner("")} />
                {data.scanners.map((s) => (
                  <Chip key={s} label={`${s} · ${data.by_scanner[s] ?? 0}`}
                    active={scanner === s} onClick={() => pickScanner(s)} />
                ))}
                {data.scanners.length === 0 && <span style={{ fontSize: 12, color: "var(--text-muted)" }}>No facts submitted yet.</span>}
              </div>

              {/* one card per submission (ScanResult) */}
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {data.scan_results.map((r) => {
                  const isOpen = openRows[r.id];
                  return (
                    <div key={r.id} style={{ borderRadius: 10, border: "0.5px solid var(--border-subtle)", background: "var(--bg-base,var(--bg-panel))", overflow: "hidden" }}>
                      <button onClick={() => setOpenRows((o) => ({ ...o, [r.id]: !o[r.id] }))}
                        style={{ width: "100%", display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", cursor: "pointer", background: "transparent", border: "none", textAlign: "left", flexWrap: "wrap" }}>
                        <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-primary)", fontFamily: "var(--font-mono)" }}>{r.scan_type ?? "scan"}</span>
                        <span style={{ fontSize: 11, color: "var(--text-muted)" }}><strong style={{ color: "var(--text-secondary)" }}>{r.fact_count ?? r.facts.length}</strong> facts</span>
                        {r.validation_state && <span style={{ fontSize: 10, fontFamily: "var(--font-mono)", padding: "1px 6px", borderRadius: 5, background: "var(--accent-ghost)", color: "var(--accent)" }}>{r.validation_state}</span>}
                        {r.job_id && <span style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: "var(--text-faint)" }}>job {r.job_id.slice(0, 8)}</span>}
                        {r.created_at && <span style={{ fontSize: 10, color: "var(--text-faint)" }}>{new Date(r.created_at).toLocaleString()}</span>}
                        <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-faint)" }}>{isOpen ? "▾" : "▸"}</span>
                      </button>
                      {/* per-submission scanner breakdown */}
                      <div style={{ display: "flex", gap: 10, padding: "0 14px 8px", flexWrap: "wrap" }}>
                        {Object.entries(r.by_scanner).map(([s, n]) => (
                          <span key={s} style={{ fontSize: 10.5, fontFamily: "var(--font-mono)", color: "var(--text-muted)" }}>{s}·{n}</span>
                        ))}
                      </div>
                      {isOpen && (
                        <div style={{ padding: "0 14px 12px" }}>
                          {r.truncated && <div style={{ fontSize: 10.5, color: "var(--sev-medium,#eab308)", marginBottom: 6 }}>⚠ facts truncated — use scanner/job filters to narrow.</div>}
                          <pre style={{ margin: 0, padding: 12, borderRadius: 8, background: "var(--bg-code,rgba(0,0,0,.28))", color: "var(--text-secondary)", fontSize: 10.5, lineHeight: 1.5, fontFamily: "var(--font-mono)", overflowX: "auto", maxHeight: 420, overflowY: "auto" }}>
                            {JSON.stringify(r.facts, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  );
                })}
                {data.scan_results.length === 0 && !err && (
                  <div style={{ fontSize: 12, color: "var(--text-muted)" }}>No scan submissions recorded for this engagement yet.</div>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function Chip({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button onClick={onClick}
      style={{ fontSize: 11, fontFamily: "var(--font-mono)", padding: "3px 10px", borderRadius: 999, cursor: "pointer",
        border: active ? "0.5px solid var(--accent)" : "0.5px solid var(--border-subtle)",
        background: active ? "var(--accent-ghost)" : "transparent",
        color: active ? "var(--accent)" : "var(--text-muted)" }}>
      {label}
    </button>
  );
}
