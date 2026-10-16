"use client";

/* Deep scan — every TCP port plus the full assessment, on exactly ONE host.
   This is the ONLY way to run an all-ports scan from either Scanner (there is
   no multi-host full-port option). Shown on both Scanners. On the portal the customer enters a single IP and the
   card explains the plan's rules before they spend a scan (one asset only, in
   scope, repeat policy, what's left). On the operator Scanner there is no plan
   (`plan={null}`): operators are unlimited and the card says the scan is not
   charged to the customer. The manager re-validates everything — this is the
   explanation, not the gate. */

import { useState } from "react";
import { ChevronDown, Crosshair, Loader, Play } from "lucide-react";
import type { Entitlement } from "../../lib/entitlements";

/** Client-side pre-check for a single asset. Returns a sentence, or null. */
export function deepTargetProblem(
  raw: string, scope: string[], history: string[], distinct: boolean,
  scopeLabel = "your authorized scope",
): string | null {
  const value = raw.trim();
  if (!value) return "Enter the one IP address to deep-scan.";
  if (/[\s,;]/.test(value)) return "A deep scan covers exactly one asset — enter a single IP.";
  const v4 = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(\/32)?$/.exec(value);
  if (value.includes("/") && !/\/(32|128)$/.test(value)) return "That's a range — enter a single IP.";
  if (!v4 && !value.includes(":")) return `'${value}' isn't an IP address.`;
  if (v4 && v4.slice(1, 5).some((o) => Number(o) > 255)) return `'${value}' isn't an IP address.`;
  const host = value.replace(/\/(32|128)$/, "");
  if (v4 && scope.length && !scope.some((cidr) => ipv4InCidr(host, cidr)))
    return `${host} is outside ${scopeLabel}.`;
  if (distinct && history.some((t) => t.replace(/\/(32|128)$/, "") === host))
    return `${host} has already had a deep scan. Your plan allows one per asset — choose another.`;
  return null;
}

function ipv4ToInt(ip: string): number | null {
  const p = ip.split(".").map(Number);
  if (p.length !== 4 || p.some((n) => !Number.isInteger(n) || n < 0 || n > 255)) return null;
  return ((p[0] << 24) >>> 0) + (p[1] << 16) + (p[2] << 8) + p[3];
}

function ipv4InCidr(ip: string, cidr: string): boolean {
  const [base, bitsRaw] = cidr.split("/");
  const bits = bitsRaw === undefined ? 32 : Number(bitsRaw);
  const a = ipv4ToInt(ip);
  const b = ipv4ToInt(base);
  if (a == null || b == null || !(bits >= 0 && bits <= 32)) return true; // not v4: let the server decide
  const mask = bits === 0 ? 0 : (~0 << (32 - bits)) >>> 0;
  return (a & mask) === (b & mask);
}

export interface DeepScanCopy {
  badge: string;
  rules: string[];
  footer: string;
  scopeLabel: string;
}

/** Everything the card says, for a customer plan or (null) the operator. */
export function deepScanCopy(plan: Entitlement | null): DeepScanCopy {
  if (!plan) {
    const scopeLabel = "this engagement's scope";
    return {
      badge: "Operator · not counted",
      rules: [
        `Exactly one host per deep scan — a single IP inside ${scopeLabel}.`,
        "Operator scans don't use the customer's Deep allowance and can repeat an asset.",
      ],
      footer: "Runs on the one host you enter and doesn't use the customer's Deep allowance.",
      scopeLabel,
    };
  }
  const scopeLabel = "your authorized scope";
  const left = plan.modes.deep.left;
  return {
    badge: left == null ? "Unlimited" : `${left} left`,
    rules: [
      `Exactly one host per deep scan — a single IP inside ${scopeLabel}.`,
      plan.deep_repeat_policy === "distinct"
        ? "Each deep scan must be a different asset."
        : "You may deep-scan the same asset again.",
    ],
    footer: "Uses 1 deep scan from your plan.",
    scopeLabel,
  };
}

export function DeepScanCard({ plan, scope, probeReady, launching, onLaunch }: {
  /** The customer's plan on the portal; null on the operator Scanner. */
  plan: Entitlement | null;
  scope: string[];
  probeReady: boolean;
  launching: boolean;
  onLaunch: (ip: string) => void;
}) {
  const [ip, setIp] = useState("");
  const [touched, setTouched] = useState(false);
  const copy = deepScanCopy(plan);
  const history = plan?.deep_scanned_targets ?? [];
  const distinct = plan?.deep_repeat_policy === "distinct";
  const problem = deepTargetProblem(ip, scope, history, distinct, copy.scopeLabel);
  const blocked = plan && !plan.modes.deep.can_scan ? plan.modes.deep.reason : !probeReady
    ? "No online vedha-agent can run a deep scan right now." : null;

  const scopeHint = scope.length
    ? `${copy.scopeLabel[0].toUpperCase()}${copy.scopeLabel.slice(1)}: ${scope.slice(0, 3).join(", ")}${scope.length > 3 ? ` +${scope.length - 3} more` : ""}`
    : null;

  return (
    // Collapsed by default: a deep scan is a specialist, single-host action, so it
    // stays one line tall until opened and the main campaign form keeps the room.
    <details className="dsc">
      <style>{STYLES}</style>
      <summary>
        <span className="dsc-icon"><Crosshair size={17} /></span>
        <div>
          <h3 id="deep-scan-title">Deep scan · one host</h3>
          <p>Checks all 65,535 TCP ports on a single host, then runs the full assessment
            (banners, OS, TLS / SMB / database / RDP) on whatever it finds.</p>
        </div>
        <span className="dsc-left">{copy.badge}</span>
        <ChevronDown size={16} className="dsc-chevron" aria-hidden />
      </summary>

      <div className="dsc-body">
      <dl className="dsc-facts" aria-label="What a deep scan covers">
        <div><dt>Hosts</dt><dd>1</dd></div>
        <div><dt>TCP ports</dt><dd>65,535</dd></div>
        <div><dt>Assessment</dt><dd>Full</dd></div>
        <div><dt>Typical time</dt><dd>20–90 min</dd></div>
      </dl>

      <ul className="dsc-rules">
        {copy.rules.map((rule) => <li key={rule}>{rule}</li>)}
        {history.length > 0 && (
          <li>Already deep-scanned: {history.map((t) => (
            <code key={t}>{t.replace(/\/(32|128)$/, "")}</code>
          ))}</li>
        )}
      </ul>

      <form className="dsc-form" onSubmit={(e) => {
        e.preventDefault();
        setTouched(true);
        if (!problem && !blocked) onLaunch(ip.trim().replace(/\/(32|128)$/, ""));
      }}>
        <label>
          <span>Host to deep-scan <em>(one IP address)</em></span>
          <input value={ip} onChange={(e) => setIp(e.target.value)} onBlur={() => setTouched(true)}
            placeholder={scope[0] ? `e.g. ${exampleHost(scope[0])}` : "e.g. 10.0.0.5"}
            aria-invalid={touched && !!problem} aria-describedby="deep-scan-msg"
            inputMode="decimal" autoComplete="off" spellCheck={false} />
          {scopeHint && <small>{scopeHint}</small>}
        </label>
        <button type="submit" disabled={launching || !!blocked || (touched && !!problem)}>
          {launching ? <><Loader size={14} className="scn-spin" /> Dispatching…</>
            : <><Play size={14} fill="currentColor" /> Deep-scan this host</>}
        </button>
      </form>
      <p id="deep-scan-msg" className="dsc-msg" role={blocked || (touched && problem) ? "alert" : undefined}>
        {blocked ?? (touched ? problem : null) ?? copy.footer}
      </p>
      </div>
    </details>
  );
}

function exampleHost(cidr: string): string {
  const base = cidr.split("/")[0];
  const n = ipv4ToInt(base);
  if (n == null) return base;
  const h = n + 10;
  return [h >>> 24, (h >>> 16) & 255, (h >>> 8) & 255, h & 255].join(".");
}

const STYLES = `
.dsc { border-radius: 14px; border: 0.5px solid color-mix(in srgb, var(--sev-critical-color) 30%, var(--border-subtle)); background: var(--bg-panel); padding: 14px 18px; box-shadow: var(--shadow-sm); }
.dsc > summary { display: flex; align-items: center; gap: 12px; cursor: pointer; list-style: none; border-radius: 8px; }
.dsc > summary::-webkit-details-marker { display: none; }
.dsc > summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
.dsc-chevron { flex: 0 0 auto; color: var(--text-muted); transition: transform 180ms ease; }
.dsc[open] .dsc-chevron { transform: rotate(180deg); }
.dsc[open] > summary { margin-bottom: 14px; align-items: flex-start; }
.dsc-body { display: grid; gap: 12px; }
@media (prefers-reduced-motion: reduce) { .dsc-chevron { transition: none; } }
.dsc-icon { width: 34px; height: 34px; flex-shrink: 0; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: var(--sev-critical-color); background: color-mix(in srgb, var(--sev-critical-color) 9%, transparent); border: 0.5px solid color-mix(in srgb, var(--sev-critical-color) 30%, transparent); }
.dsc h3 { margin: 0; font-size: 14px; color: var(--text-primary); }
.dsc > summary p { margin: 3px 0 0; color: var(--text-muted); font-size: 12px; line-height: 1.5; max-width: 640px; }
.dsc-left { margin-left: auto; white-space: nowrap; font: 700 11px var(--font-mono); color: var(--text-secondary); border: 0.5px solid var(--border-subtle); border-radius: 99px; padding: 3px 10px; }
.dsc-facts { margin: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
.dsc-facts div { padding: 8px 10px; border-radius: 9px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); }
.dsc-facts dt { font-size: 9.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); }
.dsc-facts dd { margin: 3px 0 0; font: 700 14px var(--font-mono); color: var(--text-primary); }
.dsc-rules { margin: 0; padding-left: 18px; color: var(--text-secondary); font-size: 12px; line-height: 1.7; }
.dsc-rules code { font-family: var(--font-mono); font-size: 11px; margin-left: 6px; padding: 1px 6px; border-radius: 5px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); }
.dsc-form { display: flex; align-items: flex-end; gap: 10px; flex-wrap: wrap; }
.dsc-form label { display: grid; gap: 6px; flex: 1 1 240px; max-width: 360px; }
.dsc-form label small { color: var(--text-faint); font: 10.5px var(--font-mono); }
.dsc-form label em { font-style: normal; text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--text-muted); }
.dsc-form label span { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.dsc-form input { min-height: 40px; padding: 8px 11px; border-radius: 8px; border: 0.5px solid var(--border-default); background: var(--bg-surface); color: var(--text-primary); font: 12.5px var(--font-mono); outline: none; }
.dsc-form input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.dsc-form input[aria-invalid="true"] { border-color: var(--sev-high-color); }
.dsc-form button { min-height: 40px; padding: 0 16px; display: inline-flex; align-items: center; gap: 8px; border: none; border-radius: 9px; cursor: pointer; font-size: 12.5px; font-weight: 700; color: #fff; background: var(--sev-critical-color); }
.dsc-form button:disabled { opacity: 0.45; cursor: not-allowed; }
.dsc-msg { margin: 0; font-size: 11.5px; color: var(--text-muted); }
.dsc-msg[role="alert"] { color: var(--sev-high-color); }
@media (max-width: 640px) { .dsc > summary { flex-wrap: wrap; } .dsc-left { margin-left: 0; } .dsc-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
`;
