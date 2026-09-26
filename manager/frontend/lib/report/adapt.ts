/**
 * adapt.ts — maps the admin UI `Finding` shape (produced by lib/adapters.ts::
 * toUiFinding) into the report module's `RawFinding`. Kept pure and unit-tested;
 * the reports page applies it at the call site because its other tabs still
 * consume the UI shape. Backend enrichment (Phase 3) later supplies real values
 * for the fields derived here, at which point the derivations become pass-throughs.
 */
import type { RawFinding, RawAsset, RawRemediation, DetectionMethod } from "./finding-model";
import type { Bundle } from "../remediation";
import type { PortalFinding } from "../portal-client";

/** Best-effort exposure read from the asset's environment label. */
function deriveInternetReachable(f: any): boolean | undefined {
  const env = String(f?.assetContext?.environment ?? "").toLowerCase();
  if (!env) return undefined;
  if (/(internet|dmz|external|public|edge)/.test(env)) return true;
  if (/(internal|corp|private|lan|intranet)/.test(env)) return false;
  return undefined;
}

/**
 * How the finding was ESTABLISHED → module confidence input. Undefined ⇒
 * "Unverified" (honest — Phase 3 adds a first-class detection_method).
 *
 * Only genuine validation signals are used. `detectionCoverage`
 * (COVERED/PARTIAL/BLIND) is deliberately NOT consulted: it is blue-team
 * detection coverage (did defensive tooling observe the attack), not evidence
 * of how the finding was proven, and conflating the two would overstate
 * confidence.
 */
export function deriveDetectionMethod(f: any): DetectionMethod | undefined {
  if (f?.exploitValidated) return "exploit";
  const vs = String(f?.verificationState ?? "").toLowerCase();
  if (vs === "confirmed") return "behavioural";
  if (vs === "corroborated") return "inference";
  return undefined;
}

/** The single-row affected-assets table from asset context; [] when absent. */
export function toReportAssets(f: any): RawAsset[] {
  const ac = f?.assetContext;
  if (!ac) return [];
  return [{
    host: ac.hostname ?? ac.fqdn ?? ac.ipAddress ?? f.affectedHost ?? "—",
    ip: ac.ipAddress ?? undefined,
    version: ac.osVersion ?? undefined,
    environment: ac.environment ?? undefined,
    owner: ac.owner ?? undefined,
    internetReachable: deriveInternetReachable(f),
  }];
}

export function toRawFinding(f: any): RawFinding {
  return {
    ...f,
    cve: f?.cve ?? f?.cves ?? undefined,
    // The API sends compliance as {framework, controls[], rationale}; the report
    // renders strings. Normalise here so an enriched payload can never crash it.
    compliance: Array.isArray(f?.compliance)
      ? f.compliance.flatMap((c: unknown) => {
          if (typeof c === "string") return [c];
          const o = c as { framework?: string; controls?: string[] };
          return o?.framework ? (o.controls ?? []).map((ctl) => `${o.framework}: ${ctl}`) : [];
        })
      : undefined,
    dueAt: f?.slaDeadline ?? f?.dueAt ?? undefined,
    epss: f?.epssRecorded && typeof f.epssScore === "number" ? f.epssScore : undefined,
    epssPercentile: f?.epssPercentile || undefined,
    assets: toReportAssets(f),
    // Prefer the backend's authoritative values (Phase 3); fall back to the
    // client-side derivation when the API hasn't provided them.
    detectionMethod: f?.detectionMethod ?? deriveDetectionMethod(f),
    internetReachable: f?.internetReachable ?? deriveInternetReachable(f),
    verification: f?.verification ?? undefined,
    kevAddedAt: f?.kevDateAdded ?? undefined,
    exploitValidated: Boolean(f?.exploitValidated),
    activelyExploited: Boolean(f?.activelyExploited),
    detectionCoverage: f?.detectionCoverage ?? "",
  } as RawFinding;
}

/**
 * Map the deliberately-thin customer `PortalFinding` to a `RawFinding` for the
 * client report. Curated by construction: the portal payload never carries
 * evidence, exploit validation or internal judgment, so none can leak — and the
 * component is additionally rendered in `mode="client"`. Missing fields degrade
 * to empty, which client mode renders as absence rather than a gap notice.
 */
export function portalToRawFinding(pf: PortalFinding): RawFinding {
  return {
    id: pf.id,
    title: pf.title,
    severity: pf.severity ?? "",
    status: pf.status ?? "",
    affectedHost: "",
    discoveredAt: pf.first_seen ?? "",
    description: pf.description ?? "",
    technicalDetails: "",
    evidence: [],
    impact: "",
    remediation: pf.remediation ? [pf.remediation] : [],
    mitre: [],
    cve: pf.cve_ids ?? undefined,
    riskScore: pf.risk_score ?? 0,
    cvss: pf.cvss_score != null ? String(pf.cvss_score) : "",
    activelyExploited: false,
    detectionCoverage: "",
  };
}

/**
 * Ground each report finding in its fix bundle (app/remediation/bundles.py).
 * One bundles request covers the whole report: the finding's host row gives its
 * OS and live due date (engagement SLA / approved extension); the bundle gives
 * the contain → fix → prevent steps for that OS and the scanner check that
 * proves closure. Findings outside any bundle are returned unchanged.
 */
export function applyBundles(findings: RawFinding[], bundles: Bundle[]): RawFinding[] {
  const byFinding = new Map<string, { bundle: Bundle; host: Bundle["hosts"][number] }>();
  for (const bundle of bundles) {
    for (const host of bundle.hosts) {
      for (const id of host.finding_ids) byFinding.set(id, { bundle, host });
    }
  }
  const osKey = (family: string) =>
    family === "windows" || family === "linux" || family === "macos" ? family : "generic";

  return findings.map((f) => {
    const hit = byFinding.get(f.id);
    if (!hit) return f;
    const { bundle, host } = hit;
    // Bundle steps shared across hosts use fixed placeholder phrases (backend
    // bundles.MULTI_HOST_FIELDS); a per-finding card speaks about its own host.
    const own = (text: string) => text
      .split("each host in the checklist").join(host.host)
      .split("each host's IP").join(host.ip)
      .split("the OS listed per host").join(host.os);
    const steps = (bundle.steps_by_os[osKey(host.os_family)] ?? Object.values(bundle.steps_by_os)[0] ?? [])
      .map((s) => ({ ...s, title: own(s.title), description: own(s.description),
                     commands_for_os: s.commands_for_os.map(own), pre_checks: (s.pre_checks ?? []).map(own) }));
    const remediation: RawRemediation[] = steps.map((s) => ({
      tier: s.tier,
      // The report renders `action`; keep the step title with its detail and commands.
      action: [`${s.title} — ${s.description}`,
        s.pre_checks?.length ? `Before: ${s.pre_checks.join(" ")}` : "",
        s.commands_for_os.length ? `Commands: ${s.commands_for_os.join(" ; ")}` : ""]
        .filter(Boolean).join("\n"),
      downtime: s.downtime || undefined,
      rollback: s.rollback || undefined,
    }));
    const v = { ...bundle.verification_check, check: own(bundle.verification_check.check),
                manual_command: own(bundle.verification_check.manual_command ?? "") };
    return {
      ...f,
      remediation: remediation.length ? remediation : f.remediation,
      verification: {
        method: `${v.scanner} — ${v.check}`,
        command: v.manual_command || undefined,
        expected: v.expected,
      },
      dueAt: host.status === "open" || host.status === "extension_approved" ? host.due_at ?? undefined : f.dueAt,
      fixRef: bundle.ref,
      fixTarget: bundle.target_state,
    } as RawFinding;
  });
}
