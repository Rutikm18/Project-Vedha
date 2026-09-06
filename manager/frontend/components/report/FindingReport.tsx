"use client";

/**
 * FindingReport.tsx — one finding, rendered the way a pentest report renders it.
 *
 * The section order is fixed and numbered on purpose. Every professional
 * assessment report walks the same path, and a reader who has read one can
 * navigate any other: what it is → how bad and why → what it touches → how it
 * works → what we saw → how to see it yourself → how to fix it → how to prove
 * the fix worked → where to read more. The numbers exist so a client can email
 * "question on 4.6" and everyone opens the same block.
 *
 * Nothing in here decides anything. All judgement lives in lib/report/finding-model,
 * which shows its working; this file only lays it out.
 */

import {
  useCallback, useEffect, useMemo, useRef, useState,
  type ElementType, type ReactNode,
} from "react";
import { flushSync } from "react-dom";
import {
  AlertTriangle, ChevronDown, CheckCircle2, ClipboardCheck, Clock, Copy, Crosshair,
  Eye, EyeOff, FileWarning, Flame, Globe, Link2, ListChecks, Radar, Server,
  ShieldCheck, Terminal, Wrench,
} from "lucide-react";

import { SEVERITY, SEVERITY_ORDER, type Severity } from "../../lib/severity";
import {
  assess, provenanceOf, redact, triageSort, TIER_META,
  type AssessedFinding, type RawEvidence, type RawFinding, type RemediationTier,
} from "../../lib/report/finding-model";

/* ─── small shared pieces ─────────────────────────────────────────────────── */

const fmtDate = (v?: string | null) => {
  if (!v) return null;
  const d = new Date(v);
  return isNaN(d.getTime()) ? null : new Intl.DateTimeFormat("en-GB", { dateStyle: "medium" }).format(d);
};

const fmtDateTime = (v?: string | null) => {
  if (!v) return null;
  const d = new Date(v);
  return isNaN(d.getTime()) ? null : new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "short" }).format(d);
};

function SevTag({ sev, size = "md" }: { sev: Severity; size?: "sm" | "md" }) {
  const m = SEVERITY[sev];
  // The sigil is not decoration: it carries severity for readers who can't rely
  // on the red/orange/amber ramp, and it survives greyscale printing.
  return (
    <span className={`vf-sev vf-sev--${size}`} data-sev={sev.toLowerCase()}>
      <span aria-hidden="true">{m.sigil}</span>
      {m.label}
    </span>
  );
}

/** Copies whatever is on screen — never the unredacted original. */
function CopyButton({ text, label }: { text: string; label: string }) {
  const [done, setDone] = useState(false);
  const copy = useCallback(() => {
    void navigator.clipboard.writeText(text).then(() => {
      setDone(true);
      window.setTimeout(() => setDone(false), 1400);
    });
  }, [text]);
  return (
    <button type="button" className="vf-icon-btn no-print" onClick={copy} aria-label={done ? "Copied" : label}>
      {done ? <CheckCircle2 size={12} className="vf-ok" /> : <Copy size={12} />}
    </button>
  );
}

function Section({
  index, title, icon: Icon, children, tone,
}: {
  index: string; title: string; icon: ElementType; children: ReactNode; tone?: "fix" | "verify";
}) {
  return (
    <section className="vf-block" data-tone={tone}>
      <h4 className="vf-block-head">
        <span className="vf-block-no">{index}</span>
        <Icon size={13} aria-hidden="true" />
        {title}
      </h4>
      <div className="vf-block-body">{children}</div>
    </section>
  );
}

/** Says what is missing rather than rendering an empty box. */
function Gap({ children }: { children: ReactNode }) {
  return (
    <p className="vf-gap">
      <FileWarning size={12} aria-hidden="true" />
      {children}
    </p>
  );
}

function Prose({ text }: { text: string }) {
  return (
    <div className="vf-prose">
      {text.split(/\n{2,}/).map((p, i) => <p key={i}>{p}</p>)}
    </div>
  );
}

/* ─── 5. Evidence ─────────────────────────────────────────────────────────── */

/**
 * Exported so the Evidence Vault tab renders artifacts identically. If the vault
 * kept the old plain <pre>, every secret masked here would still be sitting in
 * the other tab — and in the same exported PDF.
 */
export function EvidenceArtifact({ item, refId }: { item: RawEvidence; refId: string }) {
  const [expanded, setExpanded] = useState(false);
  const [revealed, setRevealed] = useState(false);
  const revealedRef = useRef(revealed);

  useEffect(() => { revealedRef.current = revealed; }, [revealed]);
  useEffect(() => {
    let restoreReveal = false;
    const maskForPrint = () => {
      restoreReveal = revealedRef.current;
      if (restoreReveal) flushSync(() => setRevealed(false));
    };
    const restoreAfterPrint = () => {
      if (!restoreReveal) return;
      restoreReveal = false;
      setRevealed(true);
    };
    window.addEventListener("beforeprint", maskForPrint);
    window.addEventListener("afterprint", restoreAfterPrint);
    return () => {
      window.removeEventListener("beforeprint", maskForPrint);
      window.removeEventListener("afterprint", restoreAfterPrint);
    };
  }, []);

  const masked = useMemo(() => redact(item.content ?? ""), [item.content]);
  const prov = useMemo(() => provenanceOf(item), [item]);

  const full = revealed ? item.content : masked.text;
  const long = full.length > 900;
  const shown = expanded || !long ? full : `${full.slice(0, 900)}\n…`;
  const lines = full.split("\n").length;

  return (
    <figure className="vf-artifact">
      <figcaption className="vf-artifact-head">
        <span className="vf-artifact-id">{refId}</span>
        <Terminal size={12} aria-hidden="true" />
        <span className="vf-artifact-label">{item.label}</span>
        {item.type && <span className="vf-tag">{item.type}</span>}
        <span className="vf-artifact-tools no-print">
          {masked.total > 0 && (
            <button
              type="button"
              className="vf-text-btn"
              onClick={() => setRevealed(r => !r)}
              aria-pressed={revealed}
            >
              {revealed ? <EyeOff size={11} /> : <Eye size={11} />}
              {revealed ? "Hide secrets" : `Reveal ${masked.total}`}
            </button>
          )}
          {long && (
            <button type="button" className="vf-text-btn" onClick={() => setExpanded(e => !e)} aria-expanded={expanded}>
              {expanded ? "Collapse" : `Show all ${lines} lines`}
            </button>
          )}
          <CopyButton text={shown} label="Copy this artifact" />
        </span>
      </figcaption>

      {item.command && (
        <div className="vf-artifact-cmd">
          <span className="vf-artifact-cmd-sigil" aria-hidden="true">$</span>
          <code>{item.command}</code>
          <CopyButton text={item.command} label="Copy the command" />
        </div>
      )}

      <pre className="vf-artifact-out" data-expanded={expanded || !long}>{shown}</pre>

      {masked.total > 0 && !revealed && (
        <p className="vf-artifact-note vf-artifact-note--mask">
          {masked.total} value{masked.total === 1 ? "" : "s"} masked
          {" — "}
          {masked.hits.map(h => `${h.count}× ${h.kind}`).join(", ")}.
          Masked output is what gets copied and printed.
        </p>
      )}
      {revealed && (
        <p className="vf-artifact-note vf-artifact-note--warn">
          <AlertTriangle size={11} aria-hidden="true" />
          Secrets are visible. Hide them again before exporting or sharing this report.
        </p>
      )}

      <dl className="vf-provenance">
        {prov.fields.map(f => (
          <div key={f.label}>
            <dt>{f.label}</dt>
            <dd className={f.value ? undefined : "vf-unset"}>
              {f.label === "Captured" && f.value ? fmtDateTime(f.value) ?? f.value
                : f.label === "SHA-256" && f.value ? `${f.value.slice(0, 16)}…`
                : f.value ?? "not recorded"}
            </dd>
          </div>
        ))}
      </dl>
      {prov.gap && <p className="vf-artifact-note vf-artifact-note--warn"><AlertTriangle size={11} aria-hidden="true" />{prov.gap}</p>}
    </figure>
  );
}

/* ─── the finding ─────────────────────────────────────────────────────────── */

export interface FindingReportProps {
  finding: RawFinding;
  ordinal: number;
  open: boolean;
  onToggle: (id: string) => void;
}

export function FindingReport({ finding, ordinal, open, onToggle }: FindingReportProps) {
  const a: AssessedFinding = useMemo(() => assess(finding), [finding]);
  const f = a.raw;
  const bodyId = `vf-body-${f.id}`;
  const n = String(ordinal).padStart(2, "0");

  const byTier = (t: RemediationTier) => a.remediation.filter(s => s.tier === t);
  const discovered = fmtDate(f.discoveredAt);
  const due = fmtDate(a.sla.dueAt?.toISOString());

  return (
    <article className="vf-card" data-sev={a.severity.toLowerCase()} data-open={open}>
      <button
        type="button"
        className="vf-head"
        onClick={() => onToggle(f.id)}
        aria-expanded={open}
        aria-controls={bodyId}
      >
        <span className="vf-head-ordinal" aria-hidden="true">{n}</span>

        <span className="vf-head-main">
          <span className="vf-head-tags">
            <SevTag sev={a.severity} />
            <span className="vf-prio" data-prio={a.priority.code}>{a.priority.code} {a.priority.label}</span>
            {a.cvssScore !== null && <span className="vf-cvss">CVSS {a.cvssScore.toFixed(1)}</span>}
            <span className="vf-conf" data-level={a.confidence.level.toLowerCase()}>{a.confidence.label}</span>
            {f.activelyExploited && (
              <span className="vf-kev"><Flame size={10} aria-hidden="true" />Exploited in the wild</span>
            )}
            {!a.readiness.ready && (
              <span className="vf-notready no-print">
                {a.readiness.blocking} field{a.readiness.blocking === 1 ? "" : "s"} missing
              </span>
            )}
          </span>

          <span className="vf-head-title">{f.title}</span>

          <span className="vf-head-meta">
            <span className="vf-ref">{f.id}</span>
            <span>{a.assets.length} asset{a.assets.length === 1 ? "" : "s"}</span>
            {discovered && <span>Found {discovered}</span>}
            <span className="vf-status">{f.status.replace(/_/g, " ").toLowerCase()}</span>
            <span className="vf-sla" data-state={a.sla.state}>
              <Clock size={10} aria-hidden="true" />
              {a.sla.state === "breached" ? "Overdue" : a.sla.state === "closed" ? "Closed" : due ? `Due ${due}` : "No target"}
            </span>
          </span>
        </span>

        <ChevronDown size={15} className="vf-chevron" aria-hidden="true" />
      </button>

      <div className="vf-body" id={bodyId} hidden={!open}>

        {/* 1 — what it is, in the client's language */}
        <Section index={`${n}.1`} title="Summary" icon={Crosshair}>
          {f.description?.trim()
            ? <Prose text={f.description} />
            : <Gap>No summary recorded. Write one before delivery — this is the paragraph most readers will stop at.</Gap>}
          {a.attackerStatement && <p className="vf-callout">{a.attackerStatement}</p>}
        </Section>

        {/* 2 — the rating, with the inputs that produced it */}
        <Section index={`${n}.2`} title="Risk rating" icon={Radar}>
          <div className="vf-rating">
            <div className="vf-rating-score" data-sev={a.severity.toLowerCase()}>
              <span className="vf-rating-num">{a.cvssScore !== null ? a.cvssScore.toFixed(1) : "—"}</span>
              <span className="vf-rating-cap">CVSS base{a.vector?.version === "4.0" ? " (v4.0)" : ""}</span>
              <SevTag sev={a.severity} size="sm" />
            </div>
            <div className="vf-rating-detail">
              <ul className="vf-signals">
                <li data-hot={f.activelyExploited || undefined}>
                  <b>Known exploited</b>{f.activelyExploited ? `yes${f.kevAddedAt ? ` — added ${fmtDate(f.kevAddedAt)}` : ""}` : "not listed"}
                </li>
                <li data-hot={(f.epss ?? 0) >= 0.5 || undefined}>
                  <b>EPSS</b>{f.epss != null
                    ? `${f.epss.toFixed(2)}${f.epssPercentile != null ? ` (${Math.round(f.epssPercentile * 100)}th percentile)` : ""}`
                    : "not scored"}
                </li>
                <li data-hot={f.exploitValidated || undefined}>
                  <b>Reproduced here</b>{f.exploitValidated ? "yes, during this assessment" : "no"}
                </li>
                <li data-hot={f.internetReachable || undefined}>
                  <b>Exposure</b>{f.internetReachable === true ? "internet-facing" : f.internetReachable === false ? "internal only" : "not recorded"}
                </li>
                <li><b>Detection coverage</b>{f.detectionCoverage ? f.detectionCoverage.toLowerCase() : "not recorded"}</li>
              </ul>

              {a.vector && (
                <>
                  <p className="vf-vector-raw"><code>{f.cvssVector}</code></p>
                  <ul className="vf-metrics">
                    {a.vector.metrics.map(m => (
                      <li key={m.key} data-hot={m.aggravating || undefined} title={`${m.name}: ${m.reading}`}>
                        <span>{m.name}</span>
                        <b>{m.reading}</b>
                      </li>
                    ))}
                  </ul>
                  <div className="vf-two-up">
                    <div>
                      <h5>What an attacker needs</h5>
                      <ul className="vf-list">{a.vector.prerequisites.map(p => <li key={p}>{p}</li>)}</ul>
                    </div>
                    <div>
                      <h5>What they get</h5>
                      <ul className="vf-list">{a.vector.outcomes.map(o => <li key={o}>{o}</li>)}</ul>
                    </div>
                  </div>
                </>
              )}
              {!a.vector && <Gap>No CVSS vector recorded, so the score cannot be checked against its inputs.</Gap>}
            </div>
          </div>

          <div className="vf-why">
            <h5>Why this is {a.priority.code} — {a.priority.label.toLowerCase()}</h5>
            {a.priority.drivers.length > 0
              ? <ul className="vf-list vf-list--hot">{a.priority.drivers.map(d => <li key={d}>{d}</li>)}</ul>
              : <p className="vf-muted">Nothing raises this above its base severity.</p>}
            {a.priority.dampeners.length > 0 && (
              <>
                <h5>What holds it down</h5>
                <ul className="vf-list vf-list--cool">{a.priority.dampeners.map(d => <li key={d}>{d}</li>)}</ul>
              </>
            )}
            <p className="vf-note">
              CVSS rates the flaw; priority rates the situation. {a.sla.note} Targets follow the engagement's
              default policy and can be reset per finding.
            </p>
            {f.severityRationale && <Prose text={f.severityRationale} />}
            {f.severityAdjustedFrom && (
              <p className="vf-note">Adjusted from {f.severityAdjustedFrom} for this environment.</p>
            )}
          </div>

          <div className="vf-confidence" data-level={a.confidence.level.toLowerCase()}>
            <h5>How this was established — {a.confidence.label.toLowerCase()}</h5>
            <p>{a.confidence.basis}</p>
            {a.confidence.caveat && <p className="vf-confidence-caveat">{a.confidence.caveat}</p>}
          </div>
        </Section>

        {/* 3 — what it touches */}
        <Section index={`${n}.3`} title="Affected assets" icon={Server}>
          {a.assets.length ? (
            <div className="vf-table-wrap">
              <table className="vf-table">
                <thead>
                  <tr>
                    <th scope="col">Host</th><th scope="col">Address</th>
                    <th scope="col">Service</th><th scope="col">Version</th>
                    <th scope="col">Environment</th><th scope="col">Exposure</th>
                  </tr>
                </thead>
                <tbody>
                  {a.assets.map((as, i) => (
                    <tr key={`${as.host}-${i}`}>
                      <th scope="row">{as.host}</th>
                      <td>{as.ip ?? <span className="vf-unset">not recorded</span>}</td>
                      <td>{as.service ? `${as.service}${as.port ? `/${as.port}` : ""}` : as.port ? String(as.port) : <span className="vf-unset">—</span>}</td>
                      <td>{as.version ?? <span className="vf-unset">—</span>}</td>
                      <td>{as.environment ?? <span className="vf-unset">—</span>}</td>
                      <td>
                        {as.internetReachable === true ? <span className="vf-exposed"><Globe size={10} aria-hidden="true" />Internet</span>
                          : as.internetReachable === false ? "Internal"
                          : <span className="vf-unset">unknown</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <Gap>No asset recorded against this finding.</Gap>}
        </Section>

        {/* 4 — the mechanism */}
        <Section index={`${n}.4`} title="Technical detail" icon={ListChecks}>
          {f.technicalDetails?.trim()
            ? <Prose text={f.technicalDetails} />
            : <Gap>No technical detail recorded.</Gap>}
          {f.rootCause && (
            <>
              <h5>Root cause</h5>
              <Prose text={f.rootCause} />
            </>
          )}
          {f.impact?.trim() && (
            <>
              <h5>Business impact</h5>
              <Prose text={f.impact} />
            </>
          )}
          {(f.prerequisites?.length || f.attackPath?.length) && (
            <div className="vf-two-up">
              {f.prerequisites?.length ? (
                <div>
                  <h5>Preconditions</h5>
                  <ul className="vf-list">{f.prerequisites.map(p => <li key={p}>{p}</li>)}</ul>
                </div>
              ) : null}
              {f.attackPath?.length ? (
                <div>
                  <h5>Attack path</h5>
                  <ol className="vf-path">{f.attackPath.map(s => <li key={s}>{s}</li>)}</ol>
                </div>
              ) : null}
            </div>
          )}
        </Section>

        {/* 5 — what we actually saw */}
        <Section index={`${n}.5`} title={`Evidence (${f.evidence?.length ?? 0})`} icon={Terminal}>
          {f.evidence?.length ? (
            <div className="vf-artifacts">
              {f.evidence.map((item, i) => (
                <EvidenceArtifact key={`${f.id}-e${i}`} item={item} refId={`${f.id}/E${String(i + 1).padStart(2, "0")}`} />
              ))}
            </div>
          ) : <Gap>No artifact supports this finding. It cannot be delivered as written.</Gap>}
        </Section>

        {/* 6 — so the client can see it themselves */}
        <Section index={`${n}.6`} title="Reproduction" icon={ClipboardCheck}>
          {f.reproductionSteps?.trim() ? (
            <>
              <pre className="vf-repro">{f.reproductionSteps}</pre>
              <p className="vf-note">Run against the assets listed in {n}.3, from an authorised source address, within the agreed test window.</p>
            </>
          ) : <Gap>No reproduction steps recorded, so the client cannot confirm this independently.</Gap>}
        </Section>

        {/* 7 — the fix, in the order it actually gets done */}
        <Section index={`${n}.7`} title="Remediation" icon={Wrench} tone="fix">
          {a.remediation.length ? (
            (["containment", "fix", "hardening"] as RemediationTier[]).map(tier => {
              const steps = byTier(tier);
              if (!steps.length) return null;
              return (
                <div key={tier} className="vf-tier" data-tier={tier}>
                  <h5>
                    {TIER_META[tier].label}
                    <span>{TIER_META[tier].when}</span>
                  </h5>
                  <ol className="vf-steps">
                    {steps.map((s, i) => (
                      <li key={i}>
                        <p>{s.action}</p>
                        {(s.owner || s.effort || s.downtime || s.rollback) && (
                          <dl className="vf-step-meta">
                            {s.owner && <div><dt>Owner</dt><dd>{s.owner}</dd></div>}
                            {s.effort && <div><dt>Effort</dt><dd>{s.effort}</dd></div>}
                            {s.downtime && <div><dt>Downtime</dt><dd>{s.downtime}</dd></div>}
                            {s.rollback && <div><dt>Rollback</dt><dd>{s.rollback}</dd></div>}
                          </dl>
                        )}
                      </li>
                    ))}
                  </ol>
                </div>
              );
            })
          ) : <Gap>No remediation recorded. The client is told there is a problem and not what to do about it.</Gap>}
        </Section>

        {/* 8 — the part almost every automated report skips */}
        <Section index={`${n}.8`} title="Verification" icon={ShieldCheck} tone="verify">
          {f.verification?.expected?.trim() ? (
            <dl className="vf-verify">
              {f.verification.method && <div><dt>Retest method</dt><dd>{f.verification.method}</dd></div>}
              {f.verification.command && (
                <div>
                  <dt>Command</dt>
                  <dd className="vf-verify-cmd"><code>{f.verification.command}</code><CopyButton text={f.verification.command} label="Copy the retest command" /></dd>
                </div>
              )}
              <div><dt>Passes when</dt><dd className="vf-verify-pass">{f.verification.expected}</dd></div>
              {f.verification.retain && <div><dt>Evidence to keep</dt><dd>{f.verification.retain}</dd></div>}
              {f.retestedAt && <div><dt>Last retested</dt><dd>{fmtDateTime(f.retestedAt)}</dd></div>}
            </dl>
          ) : (
            <Gap>No pass criteria recorded, so a retest cannot be judged and the finding cannot be closed with confidence.</Gap>
          )}
        </Section>

        {/* 9 — where to read more */}
        <Section index={`${n}.9`} title="References" icon={Link2}>
          <div className="vf-refs">
            {f.cve?.map(cve => (
              <a key={cve} className="vf-chip vf-chip--cve" href={`https://nvd.nist.gov/vuln/detail/${cve}`} target="_blank" rel="noopener noreferrer">{cve}</a>
            ))}
            {f.cwe?.map(c => <span key={c.id} className="vf-chip" title={c.name}>{c.id} {c.name}</span>)}
            {f.mitre?.map(t => (
              <a key={t.id} className="vf-chip vf-chip--mitre" href={`https://attack.mitre.org/techniques/${t.id.replace(".", "/")}/`} target="_blank" rel="noopener noreferrer" title={t.name}>
                {t.id} {t.name}
              </a>
            ))}
            {f.advisories?.map(ad => {
              const safe = /^https?:\/\//i.test(ad.url);
              return safe
                ? <a key={ad.url} className="vf-chip" href={ad.url} target="_blank" rel="noopener noreferrer">{ad.label}</a>
                : <span key={`${ad.label}-${ad.url}`} className="vf-chip">{ad.label}</span>;
            })}
            {f.compliance?.map(c => <span key={c} className="vf-chip vf-chip--std">{c}</span>)}
          </div>
          {!f.cve?.length && !f.cwe?.length && !f.mitre?.length && !f.advisories?.length && (
            <Gap>No published identifier is linked to this finding.</Gap>
          )}
          {f.compliance?.length ? (
            <p className="vf-note">
              Control references are mappings only. A compliance verdict needs an approved scope, tested controls and a qualified reviewer.
            </p>
          ) : null}
        </Section>

        {!a.readiness.ready && (
          <div className="vf-blockers no-print">
            <h5><AlertTriangle size={12} aria-hidden="true" />Not ready for delivery</h5>
            <ul>
              {a.readiness.gaps.map(g => (
                <li key={g.field} data-blocking={g.blocking || undefined}>
                  <b>{g.field}</b> — {g.why}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </article>
  );
}

/* ─── the tab that holds them ─────────────────────────────────────────────── */

type SevFilter = Severity | "ALL";

export function FindingsSection({ findings, total }: { findings: RawFinding[]; total: number }) {
  const assessed = useMemo(() => findings.map(f => assess(f)).sort(triageSort), [findings]);

  const [sev, setSev] = useState<SevFilter>("ALL");
  const [onlyExploited, setOnlyExploited] = useState(false);
  const [onlyIncomplete, setOnlyIncomplete] = useState(false);
  const [open, setOpen] = useState<Set<string>>(() => new Set());

  // A collapsed report prints as a list of headings. Open everything for the
  // print pass, then put it back the way the assessor had it.
  //
  // beforeprint is not a React event, so a normal setState would still be
  // queued when the browser paginates. flushSync commits before we return.
  const openRef = useRef(open);
  useEffect(() => { openRef.current = open; }, [open]);

  useEffect(() => {
    const snapshot = { value: null as Set<string> | null };
    const expand = () => {
      snapshot.value = openRef.current;
      flushSync(() => setOpen(new Set(assessed.map(a => a.raw.id))));
    };
    const restore = () => {
      if (!snapshot.value) return;
      const restored = snapshot.value;
      snapshot.value = null;
      setOpen(restored);
    };
    window.addEventListener("beforeprint", expand);
    window.addEventListener("afterprint", restore);
    return () => {
      window.removeEventListener("beforeprint", expand);
      window.removeEventListener("afterprint", restore);
    };
  }, [assessed]);

  const shown = assessed.filter(a =>
    (sev === "ALL" || a.severity === sev) &&
    (!onlyExploited || a.raw.activelyExploited || a.raw.exploitValidated) &&
    (!onlyIncomplete || !a.readiness.ready)
  );

  const blocked = assessed.filter(a => !a.readiness.ready).length;
  const p0 = assessed.filter(a => a.priority.code === "P0").length;
  const overdue = assessed.filter(a => a.sla.state === "breached").length;
  const allOpen = shown.length > 0 && shown.every(a => open.has(a.raw.id));

  const toggle = useCallback((id: string) => {
    setOpen(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }, []);

  return (
    <>
      <div className="vf-triage">
        <p>
          <b>{p0}</b> need fixing now, <b>{overdue}</b> past their target date.
          {blocked > 0 && <> <b>{blocked}</b> are missing fields required for client delivery.</>}
        </p>
      </div>

      <div className="vf-filters no-print">
        <div className="vf-filter-group" role="group" aria-label="Filter by severity">
          {(["ALL", ...SEVERITY_ORDER] as SevFilter[]).map(s => (
            <button
              key={s}
              type="button"
              onClick={() => setSev(s)}
              aria-pressed={sev === s}
              data-sev={s === "ALL" ? undefined : s.toLowerCase()}
            >
              {s === "ALL" ? "All" : SEVERITY[s].label}
            </button>
          ))}
        </div>
        <label className="vf-check">
          <input type="checkbox" checked={onlyExploited} onChange={e => setOnlyExploited(e.target.checked)} />
          Exploited or proven
        </label>
        <label className="vf-check">
          <input type="checkbox" checked={onlyIncomplete} onChange={e => setOnlyIncomplete(e.target.checked)} />
          Missing fields
        </label>
        <span className="vf-filters-count">{shown.length} of {total}</span>
        <button
          type="button"
          className="vf-text-btn"
          onClick={() => setOpen(allOpen ? new Set() : new Set(shown.map(a => a.raw.id)))}
        >
          {allOpen ? "Collapse all" : "Expand all"}
        </button>
      </div>

      <div className="vf-stack">
        {shown.length === 0 && <p className="vf-empty">Nothing matches these filters.</p>}
        {shown.map((a, i) => (
          <FindingReport
            key={a.raw.id}
            finding={a.raw}
            ordinal={i + 1}
            open={open.has(a.raw.id)}
            onToggle={toggle}
          />
        ))}
      </div>
    </>
  );
}
