"use client";

/**
 * PlanView — renders one contextual remediation plan (app/remediation/plan.py).
 *
 * Pure presentation: every value comes from the backend (facts with provenance,
 * recipe, target state, due date and its source, verification check). Missing
 * facts read "not recorded" — the view never fills a gap.
 */
import React, { useMemo, useState } from "react";
import {
  AlertTriangle, CalendarClock, Check, CheckCircle2, Copy, GitCompare, Link2, ShieldAlert,
  Sparkles, Target, Terminal, Undo2,
} from "lucide-react";
import {
  CONTEXT_FIELDS, DUE_SOURCE_LABEL, TIER_LABEL, TYPE_LABEL, URGENCY_LABEL, dueState, factText, fmtIst,
  type PlanStep, type RemediationPlan, type Tier,
} from "../../lib/remediation";

const TIERS: Tier[] = ["containment", "fix", "hardening"];

function CopyButton({ text, label }: { text: string; label: string }) {
  const [state, setState] = useState<"idle" | "copied" | "failed">("idle");
  return (
    <button
      type="button"
      className="rm-copy"
      data-state={state}
      aria-label={state === "copied" ? `Copied ${label}` : `Copy ${label}`}
      onClick={async () => {
        try { await navigator.clipboard.writeText(text); setState("copied"); } catch { setState("failed"); }
        window.setTimeout(() => setState("idle"), 1800);
      }}
    >
      {state === "copied" ? <Check size={12} aria-hidden /> : <Copy size={12} aria-hidden />}
    </button>
  );
}

export function DueBadge({ at, source }: { at: string | null | undefined; source: string | null | undefined }) {
  const state = dueState(at);
  return (
    <span className="rm-due" data-state={state} title={source ? DUE_SOURCE_LABEL[source] ?? source : undefined}>
      <CalendarClock size={12} aria-hidden />
      {state === "none" ? "No target" : <>{state === "overdue" ? "Overdue · " : "Due "}{fmtIst(at)}</>}
      {source && state !== "none" && <em>{DUE_SOURCE_LABEL[source] ?? source}</em>}
    </span>
  );
}

export function UrgencyChip({ label, drivers }: { label: keyof typeof URGENCY_LABEL; drivers?: string[] }) {
  return (
    <span className="rm-urgency" data-level={label}
          title={drivers?.length ? `CISA SSVC (informational): ${drivers.join(" · ")}` : "CISA SSVC (informational)"}>
      {URGENCY_LABEL[label] ?? label}
    </span>
  );
}

function StepCard({ step }: { step: PlanStep }) {
  return (
    <li className="rm-step" data-ai={step.ai_changed || undefined}>
      <div className="rm-step-num" aria-hidden>{step.step}</div>
      <div className="rm-step-body">
        <header>
          <h5>{step.title}</h5>
          {step.ai_added && <span className="rm-tag rm-tag--ai"><Sparkles size={10} aria-hidden />Added by AI</span>}
          {step.ai_changed && !step.ai_added && <span className="rm-tag rm-tag--ai"><Sparkles size={10} aria-hidden />AI-refined</span>}
          <span className="rm-risk" data-risk={step.risk}>{step.risk} change risk</span>
        </header>
        <p>{step.description}</p>
        {step.pre_checks?.length > 0 && (
          <div className="rm-prechecks">
            <strong>Before you change anything</strong>
            <ul>{step.pre_checks.map((p, i) => <li key={i}>{p}</li>)}</ul>
          </div>
        )}
        {step.commands_for_os.length > 0 && (
          <div className="rm-commands">
            {step.commands_for_os.map((c, i) => (
              <div key={i} className="rm-command">
                <code>{c}</code>
                {!c.trim().startsWith("#") && <CopyButton text={c} label="command" />}
              </div>
            ))}
          </div>
        )}
        {step.unsafe_commands_removed && (
          <p className="rm-warn"><AlertTriangle size={12} aria-hidden />Unsafe generated commands were removed from this step.</p>
        )}
        <dl className="rm-step-meta">
          <div><dt>Restart</dt><dd>{step.reboot_required === true ? "Required" : step.reboot_required === false ? "Not required" : "Check vendor guidance"}</dd></div>
          <div><dt>Downtime</dt><dd>{step.downtime || "none expected"}</dd></div>
          {step.rollback && <div><dt><Undo2 size={11} aria-hidden /> Rollback</dt><dd>{step.rollback}</dd></div>}
        </dl>
      </div>
    </li>
  );
}

export function StepsByTier({ steps }: { steps: PlanStep[] }) {
  return (
    <div className="rm-tiers">
      {TIERS.map((tier) => {
        const inTier = steps.filter((s) => (s.tier ?? "fix") === tier);
        if (!inTier.length) return null;
        return (
          <section key={tier} className="rm-tier" data-tier={tier}>
            <h4>{TIER_LABEL[tier]}</h4>
            <ol>{inTier.map((s) => <StepCard key={s.step} step={s} />)}</ol>
          </section>
        );
      })}
    </div>
  );
}

function AiChanges({ plan }: { plan: RemediationPlan }) {
  const [open, setOpen] = useState(false);
  const changes = plan.ai_changes ?? [];
  if (!changes.length) return null;
  const show = (v: unknown) => Array.isArray(v) ? v.join(" · ") : v == null ? "—" : String(v);
  return (
    <section className="rm-ai-diff">
      <button type="button" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
        <GitCompare size={13} aria-hidden /> What the AI changed ({changes.length})
      </button>
      {open && (
        <ul>
          {changes.map((c, i) => (
            <li key={i}>
              <strong>{c.step ? `Step ${c.step} · ` : ""}{c.field.replace(/_/g, " ")}</strong>
              <div className="rm-diff-before">{show(c.before)}</div>
              <div className="rm-diff-after">{show(c.after)}</div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export function PlanView({
  plan, compact = false, headerExtra,
}: {
  plan: RemediationPlan;
  /** Report/print mode: no toggles, context shown inline. */
  compact?: boolean;
  headerExtra?: React.ReactNode;
}) {
  const facts = useMemo(() => {
    const ctx = plan.context ?? {};
    return CONTEXT_FIELDS.map(([k, label]) => ({
      key: k, label, text: factText(ctx, k), source: ctx[k]?.source ?? "not_recorded",
    }));
  }, [plan.context]);
  const v = plan.verification_check;

  return (
    <div className="rm-plan" data-compact={compact || undefined}>
      <header className="rm-plan-head">
        <div className="rm-plan-title">
          <h3>{plan.title ?? "Remediation plan"}</h3>
          {headerExtra}
        </div>
        <div className="rm-chips">
          {plan.remediation_type && <span className="rm-chip">{TYPE_LABEL[plan.remediation_type] ?? plan.remediation_type}</span>}
          {plan.risk_response && <span className="rm-chip rm-chip--muted">Risk response: {plan.risk_response}</span>}
          {plan.urgency && <UrgencyChip label={plan.urgency.label} drivers={plan.urgency.drivers} />}
          <span className="rm-chip rm-chip--muted">Effort {plan.effort}</span>
          <span className="rm-risk" data-risk={plan.remediation_risk}>Change risk {plan.remediation_risk}</span>
          {plan.due && <DueBadge at={plan.due.at} source={plan.due.source} />}
        </div>
      </header>

      {plan.fragile_guard?.active && (
        <div className="rm-banner" data-tone="warn">
          <ShieldAlert size={15} aria-hidden />
          <div><strong>Fragile asset</strong><span>This host is marked fragile ({plan.fragile_guard.reason}). Coordinate every change with its owner; nothing here should be automated.</span></div>
        </div>
      )}

      {plan.target_state && (
        <div className="rm-target"><Target size={14} aria-hidden /><div><span>Target state</span><strong>{plan.target_state}</strong></div></div>
      )}

      <section className="rm-context" aria-label="What the scan recorded">
        <h4>What the scan recorded</h4>
        <dl>
          {facts.map((f) => (
            <div key={f.key} data-source={f.source}>
              <dt>{f.label}</dt>
              <dd>{f.text}</dd>
            </div>
          ))}
          <div data-source="scan"><dt>Exposure</dt><dd>{plan.exposure === "internet" ? "Internet-facing" : plan.exposure === "internal" ? "Internal only" : "not recorded"}</dd></div>
        </dl>
      </section>

      {plan.sequencing_rationale && <p className="rm-rationale"><strong>Why this order:</strong> {plan.sequencing_rationale}</p>}

      <StepsByTier steps={plan.steps} />

      {v && (
        <section className="rm-verify">
          <h4><CheckCircle2 size={14} aria-hidden /> How closure is proven</h4>
          <p><strong>{v.scanner}</strong> — {v.check}</p>
          <p className="rm-expected">Expected: {v.expected}</p>
          {v.manual_command && (
            <div className="rm-command"><Terminal size={12} aria-hidden /><code>{v.manual_command}</code><CopyButton text={v.manual_command} label="verification command" /></div>
          )}
        </section>
      )}

      <div className="rm-closeout">
        <section>
          <h4>If the fix cannot land by the due date</h4>
          <p>{plan.compensating_controls || "No compensating control is recorded."}</p>
        </section>
        {plan.long_term_recommendations.length > 0 && (
          <section>
            <h4>Keep it fixed</h4>
            <ul>{plan.long_term_recommendations.map((r, i) => <li key={i}>{r}</li>)}</ul>
          </section>
        )}
      </div>

      {(plan.references?.length ?? 0) > 0 && (
        <div className="rm-refs">
          <Link2 size={12} aria-hidden />
          {plan.references!.map((r) => /^CVE-\d{4}-\d+$/i.test(r)
            ? <a key={r} className="rm-ref" href={`https://nvd.nist.gov/vuln/detail/${r}`} target="_blank" rel="noopener noreferrer">{r}</a>
            : <span key={r} className="rm-ref">{r}</span>)}
        </div>
      )}

      {!compact && <AiChanges plan={plan} />}
    </div>
  );
}
