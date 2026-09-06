/**
 * adapt.ts — maps the admin UI `Finding` shape (produced by lib/adapters.ts::
 * toUiFinding) into the report module's `RawFinding`. Kept pure and unit-tested;
 * the reports page applies it at the call site because its other tabs still
 * consume the UI shape. Backend enrichment (Phase 3) later supplies real values
 * for the fields derived here, at which point the derivations become pass-throughs.
 */
import type { RawFinding, RawAsset, DetectionMethod } from "./finding-model";

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
    epss: f?.epssRecorded && typeof f.epssScore === "number" ? f.epssScore : undefined,
    epssPercentile: f?.epssPercentile || undefined,
    assets: toReportAssets(f),
    detectionMethod: deriveDetectionMethod(f),
    internetReachable: deriveInternetReachable(f),
    exploitValidated: Boolean(f?.exploitValidated),
    activelyExploited: Boolean(f?.activelyExploited),
    detectionCoverage: f?.detectionCoverage ?? "",
  } as RawFinding;
}
