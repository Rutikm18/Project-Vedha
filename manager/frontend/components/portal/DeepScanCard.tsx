"use client";

import { useState } from "react";
import { Loader, Play } from "lucide-react";
import type { Entitlement } from "../../lib/entitlements";
import { parseScanIp, scanIpAllowed, deepScanAssetOptions, type ScanAssetOption } from "../../lib/scan-target";

/** Immediate feedback only; the manager rechecks IP, scope, exclusions and quota. */
export function deepTargetProblem(raw: string, scope: string[], history: string[], distinct: boolean,
  scopeLabel = "your authorized scope", excluded: string[] = []): string | null {
  const value = raw.trim();
  if (!value) return "Enter the one IP address to deep-scan.";
  if (/[\s,;]/.test(value)) return "A deep scan covers exactly one asset — enter a single IP.";
  if (value.includes("/") && !/\/(32|128)$/.test(value)) return "That's a range — enter a single IP.";
  const ip = parseScanIp(value);
  if (!ip) return `'${value}' isn't an IP address.`;
  if (!scanIpAllowed(value, scope, excluded)) return `${ip.host} is outside ${scopeLabel} or excluded.`;
  if (distinct && history.some(t => parseScanIp(t)?.host === ip.host))
    return `${ip.host} has already had a deep scan. Your plan allows one per asset — choose another.`;
  return null;
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

export function DeepScanCard({ plan, scope, excluded = [], assets = [], assetsLoading = false,
  assetsError, onRetryAssets, probeReady, launching, blockedReason, onLaunch }: {
  plan: Entitlement | null;
  scope: string[];
  excluded?: string[];
  assets?: ScanAssetOption[];
  assetsLoading?: boolean;
  assetsError?: string | null;
  onRetryAssets?: () => void;
  probeReady: boolean;
  launching: boolean;
  blockedReason?: string | null;
  onLaunch: (ip: string) => void;
}) {
  const [ip, setIp] = useState("");
  const [manual, setManual] = useState(false);
  const [touched, setTouched] = useState(false);
  const copy = deepScanCopy(plan);
  const options = deepScanAssetOptions(assets, scope, excluded);
  const useManual = manual || (!assetsLoading && options.length === 0);
  const problem = !useManual && !options.some(asset => asset.ip_address === ip)
    ? "Select one IP from this engagement."
    : deepTargetProblem(ip, scope, plan?.deep_scanned_targets ?? [],
      plan?.deep_repeat_policy === "distinct", copy.scopeLabel, excluded);
  const blocked = blockedReason || (plan && !plan.can_scan ? plan.reason || "Your scan allowance is unavailable."
    : plan && !plan.modes.deep.can_scan ? plan.modes.deep.reason || "Deep scanning is unavailable in your plan."
    : !scope.length ? "This engagement has no authorized IP scope. Add scope before scanning."
    : !probeReady ? "No online vedha-agent can run a deep scan right now." : null);

  return (
    <section className="scanner-deep" aria-labelledby="deep-scan-title">
      <h3 id="deep-scan-title">Deep scan · one host</h3>
      <p>All 65,535 TCP ports on one IP, followed by service assessment.</p>
      <form onSubmit={event => {
        event.preventDefault(); setTouched(true);
        if (!launching && !problem && !blocked) onLaunch(parseScanIp(ip)!.host);
      }}>
        <label htmlFor="deep-scan-ip">{useManual ? "IP address" : "Select one IP"}</label>
        {useManual ? <input id="deep-scan-ip" value={ip}
          onChange={event => { setIp(event.target.value); setTouched(true); }} onBlur={() => setTouched(true)}
          placeholder="One IPv4 or IPv6 address" autoComplete="off" spellCheck={false}
          disabled={launching} aria-invalid={touched && !!problem} aria-describedby="deep-scan-msg" />
          : <select id="deep-scan-ip" value={ip} disabled={assetsLoading || launching}
            onChange={event => { setIp(event.target.value); setTouched(true); }} aria-describedby="deep-scan-msg">
            <option value="">{assetsLoading ? "Loading engagement IPs…" : "Choose one discovered IP…"}</option>
            {options.map(asset => <option key={asset.ip_address} value={asset.ip_address}>
              {asset.ip_address}{asset.hostname ? ` · ${asset.hostname}` : ""}
            </option>)}
          </select>}
        {options.length > 0 && <button className="scanner-text-action" type="button" disabled={launching} onClick={() => {
          setManual(!useManual); setIp(""); setTouched(false);
        }}>{useManual ? "Choose a discovered IP" : "Enter an IP instead"}</button>}
        {assetsError && <p className="scanner-help">IP list unavailable. Enter one authorized IP.
          {onRetryAssets && <button type="button" className="scanner-text-action" onClick={onRetryAssets}>Retry IP list</button>}
        </p>}
        <p id="deep-scan-msg" role={touched && problem ? "alert" : "status"} className="scanner-help">
          {blocked ?? (touched ? problem : null) ?? "Only this IP will be scanned. Engagement exclusions still apply."}
        </p>
        <div className="scanner-submit-row">
          <span>{plan ? copy.footer : "Operator scan · customer allowance unchanged"}</span>
          <button className="btn btn-primary" type="submit" disabled={launching || !!blocked || !!problem}>
            {launching ? <><Loader size={15} className="scn-spin" /> Dispatching…</> : <><Play size={15} /> Deep-scan this host</>}
          </button>
        </div>
      </form>
      {plan && <details className="scanner-details"><summary>Deep scan allowance · {copy.badge}</summary>
        <ul>{copy.rules.map(rule => <li key={rule}>{rule}</li>)}</ul>
      </details>}
    </section>
  );
}
