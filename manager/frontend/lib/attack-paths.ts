/**
 * Attack paths — response types and the pure view-model behind the page.
 *
 * Every function here takes what the backend returned and decides what to SAY about
 * it. The page only lays that out. The rules the wording follows:
 *   - an empty result never reads as "safe" (the model may simply have lacked input);
 *   - a route that rests on an assumption says so, in words, beside the route;
 *   - coverage is "observed" or "partial", never "complete" — the backend does not
 *     track which addresses were actually scanned.
 */

// ── Backend shapes (manager/backend/app/routers/attack_paths.py) ─────────────

export type Freshness = "fresh" | "partly_stale" | "stale";

export interface RouteNode {
  /** The asset's own id — the one the choke-point analysis names. */
  asset_id: string;
  label: string;
}

export interface PathSummary {
  id: string;
  risk_score: number | null;
  hops: number;
  source: string | null;
  target: string | null;
  source_label: string | null;
  target_label: string | null;
  freshness: Freshness;
  chokepoint_count: number;
  nodes: RouteNode[];
}

export interface Reason {
  code: string;
  detail: string;
}

export interface Diagnostics {
  assets: number;
  findings: number;
  exploitable_findings: number;
  /** Findings that can compromise a host: exploitable OR a foothold/lateral/priv-esc capability (P2). */
  compromising_findings?: number;
  entry_points: number;
  internet_exposed_assets: number;
  targets: number;
  reachability_edges: number;
  control_edges: number;
  segments: number;
  reachability_posture: string | null;
  unplaced_assets: number;
  reasons: Reason[];
}

export interface PathList {
  total: number;
  page: number;
  page_size: number;
  items: PathSummary[];
  /** Present only when the list is empty: why. */
  why_empty?: Diagnostics;
}

export interface Hop {
  from: string;
  to: string;
  technique: string | null;
  weight: number | null;
  exploited: boolean | null;
  cvss: number | null;
  via: string[];
  basis: string | null;
  likelihood: number | null;
  stale: boolean;
  /** What the final step of this hop lets the attacker do: foothold/lateral/priv_esc (P2). */
  capability?: string | null;
  explanation: string;
}

export interface PathDetail {
  id: string;
  risk_score: number | null;
  freshness: Freshness;
  node_count: number;
  nodes: string[];
  hops: Hop[];
  chokepoints: string[];
}

export interface ChokeEntry {
  asset_id: string;
  label: string;
  /** Modelled risk removed if this one host were fixed: a sum over crown jewels, so NOT
   *  bounded by 100. Use `riskShare` for anything drawn as a bar. */
  risk_removed: number;
  targets_cut_off: string[];
  targets_cut_off_labels: string[];
  remediation_priority: "critical" | "high" | "medium";
}

export interface FixSet {
  size: number;
  assets: { asset_id: string; label: string }[];
  /** Vertex-disjoint routes to each target, keyed by the target's label. */
  independent_routes: Record<string, number>;
  /** Crown jewels exposed to the internet outright: their OWN exposure must be removed —
   *  cutting other hosts cannot protect them (D8). Absent in analyses stored before the field. */
  exposed_targets?: { asset_id: string; label: string }[];
}

/** How the path targets were chosen (P4b). `suggested` = nothing was marked critical, so
 *  high-value hosts were picked automatically; the UI must say so. */
export interface TargetSelection {
  basis: "operator" | "suggested" | "explicit" | "none";
  suggested: { asset_id: string; label: string; reason: string | null }[];
}

export interface ChokeTarget {
  asset_id: string;
  label: string;
  /** 0 = no modelled route reaches it. */
  best_likelihood: number;
  risk: number;
  /** The crown jewel is itself an exploitable internet-exposed host: it has no route to cut.
   *  Absent in analyses stored before the flag existed; see `targetExposed`. */
  exposed_directly?: boolean;
}

/** A likelihood this high can only be a jewel that is its own entry point (every route
 *  multiplies at least one step probability, and the highest step value is 0.95). */
export const EXPOSED_LIKELIHOOD = 0.9999;

export function targetExposed(t: Pick<ChokeTarget, "best_likelihood" | "exposed_directly">): boolean {
  return typeof t.exposed_directly === "boolean" ? t.exposed_directly : t.best_likelihood >= EXPOSED_LIKELIHOOD;
}

export interface ChokeAnalysis {
  ranked: ChokeEntry[];
  min_fix_set: FixSet;
  targets: ChokeTarget[];
  entry_points?: number;
  method?: string;
}

export interface CoverageSegment {
  segment: string;
  cidr: string;
  site: string | null;
  hosts: number;
  stale_hosts: number;
  last_seen: string | null;
  inferred: boolean;
  in_scope: boolean;
}

export interface Coverage {
  basis: string;
  confidence: "observed" | "partial";
  segments: CoverageSegment[];
  scope_without_observed_hosts: { cidr: string; addresses: number }[];
  observed_outside_scope: string[];
  assets_placed: number;
  assets_without_a_subnet: number;
  inferred_subnets: number;
}

export interface FreshnessReport {
  window_days: number | null;
  assets: number;
  stale_assets: number;
  stale_fraction: number;
  assets_without_timestamp: number;
  oldest_seen: string | null;
  newest_seen: string | null;
}

export type Analysis =
  | { computed: false; detail?: string }
  | {
      computed: true;
      computed_at: string;
      path_count: number;
      choke: ChokeAnalysis;
      coverage: Coverage | null;
      freshness: FreshnessReport | null;
      diagnostics: Diagnostics | null;
      target_selection?: TargetSelection | null;
    };

// ── Wording ──────────────────────────────────────────────────────────────────

export type Tone = "firm" | "inferred" | "weak" | "neutral";

export interface BasisInfo {
  label: string;
  tone: Tone;
  /** Shown beside the hop when the step rests on an assumption. */
  caveat: string | null;
}

/** What a hop's `basis` means for how far to trust it. Unknown values degrade to a
 *  neutral label rather than hiding the step. */
export function basisInfo(basis: string | null | undefined): BasisInfo {
  switch (basis) {
    case "observed":
      return { label: "Observed", tone: "firm", caveat: null };
    case "same_subnet":
      return { label: "Same subnet", tone: "inferred", caveat: null };
    case "same_host_fqdn":
      return { label: "Same machine (FQDN)", tone: "inferred", caveat: null };
    case "same_host_name":
      return {
        label: "Same machine (name only)",
        tone: "weak",
        caveat: "Linked as one machine by host name alone. Confirm they are the same device.",
      };
    case "assumed":
      return {
        label: "Assumed route",
        tone: "weak",
        caveat: "Reachability between these subnets is assumed, not observed. Verify segmentation.",
      };
    case "assumed_cross_site":
      return {
        label: "Assumed link between sites",
        tone: "weak",
        caveat: "Two sites' private networks. That they connect at all is assumed, and unlikely by default.",
      };
    case "possible":
      return { label: "Possible", tone: "weak", caveat: "Not confirmed." };
    default:
      return { label: basis ? humanize(basis) : "Direct step", tone: "neutral", caveat: null };
  }
}

export function freshnessInfo(f: Freshness | string | null | undefined): { label: string; tone: Tone } {
  if (f === "stale") return { label: "Stale", tone: "weak" };
  if (f === "partly_stale") return { label: "Partly stale", tone: "weak" };
  return { label: "Recent", tone: "firm" };
}

export function humanize(code: string): string {
  const s = code.replace(/[_-]+/g, " ").trim().toLowerCase();
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}

/** "63%" from 0.63; "—" when the step carries no estimate. */
export function percent(p: number | null | undefined): string {
  if (p == null || !Number.isFinite(p)) return "—";
  return `${Math.round(Math.max(0, Math.min(1, p)) * 100)}%`;
}

export function riskLabel(score: number | null | undefined): string {
  return score == null || !Number.isFinite(score) ? "—" : score.toFixed(1);
}

/** Technique codes the backend emits, as a short human phrase. */
export function techniqueLabel(technique: string | null | undefined): string {
  switch (technique) {
    case "SAME_SUBNET": return "Within subnet";
    case "CROSS_SUBNET": return "Across subnets";
    case "GATEWAY_ROUTE": return "Through a gateway";
    case "CREDENTIAL_REUSE": return "Reused credentials";
    case "RELAY": return "NTLM relay";
    case "SAME_HOST": return "Same machine";
    case "SAME_SEGMENT": return "Within segment";
    case "CONNECTS_TO": return "Network connection";
    default: return technique ? humanize(technique) : "Step";
  }
}

/** What an attacker gains at a step (P2): a short phrase for the capability that made the
 *  destination compromisable. Null/unknown shows nothing. */
export function capabilityLabel(capability: string | null | undefined): string | null {
  switch (capability) {
    case "foothold": return "Foothold";
    case "lateral": return "Lateral move";
    case "priv_esc": return "Privilege escalation";
    case "credential_access": return "Credential access";
    case "recon": return "Reconnaissance";
    default: return null;
  }
}

/** The note shown when path targets were SUGGESTED, not operator-chosen (P4b). Null when the
 *  operator marked the targets (or picked one explicitly), so nothing is claimed about scoping. */
export function suggestedTargetsNote(selection: TargetSelection | null | undefined): string | null {
  if (!selection || selection.basis !== "suggested" || selection.suggested.length === 0) return null;
  const named = selection.suggested
    .map((s) => (s.reason ? `${s.label} (${s.reason})` : s.label))
    .join(", ");
  return `No asset was marked critical, so these high-value hosts were used as crown jewels: ${named}. `
    + `Mark the assets that matter to aim the analysis deliberately.`;
}

// ── Empty results ────────────────────────────────────────────────────────────

export interface EmptyReason {
  code: string;
  title: string;
  /** What the backend measured. */
  evidence: string;
  /** What to do about it. */
  action: string;
}

const REASON_TEXT: Record<string, { title: string; action: string }> = {
  no_assets: {
    title: "No hosts yet",
    action: "Run a scan or enrol an agent so hosts are discovered.",
  },
  no_entry_points: {
    title: "No internet-exposed entry point",
    action: "Paths start from hosts with a service seen open from outside. Scan from an external probe to find them.",
  },
  entry_points_not_compromisable: {
    title: "Exposed hosts, but nothing to exploit",
    action: "These hosts are reachable from outside but have no finding marked exploitable, so none is a foothold.",
  },
  no_targets: {
    title: "No crown jewels marked",
    action: "Mark the systems that matter most as critical on the engagement's assets. Targets are chosen by you.",
  },
  no_reachability: {
    title: "No network links between hosts",
    action: "Hosts need addresses in the engagement scope so routes between subnets can be inferred.",
  },
  no_exploitable_steps: {
    title: "No exploitable findings",
    action: "A step needs a finding marked exploitable. None qualifies yet.",
  },
  no_control_edges: {
    title: "Reachable, but nothing can be taken over",
    action: "Hosts can reach each other but none of the reachable ones carries an exploitable finding.",
  },
};

/** Why a list is empty, in the order the backend found the gaps. Unknown codes are
 *  shown verbatim: a reason we cannot word is still a reason. */
export function emptyReasons(d: Diagnostics | null | undefined): EmptyReason[] {
  return (d?.reasons ?? []).map((r) => {
    const known = REASON_TEXT[r.code];
    return {
      code: r.code,
      title: known?.title ?? humanize(r.code),
      evidence: r.detail,
      action: known?.action ?? "",
    };
  });
}

// ── Fix first ────────────────────────────────────────────────────────────────

/** Share (0-1) of the engagement's modelled risk that fixing one host removes. */
export function riskShare(entry: ChokeEntry, targets: ChokeAnalysis["targets"]): number {
  const total = targets.reduce((sum, t) => sum + (Number.isFinite(t.risk) ? t.risk : 0), 0);
  if (total <= 0) return 0;
  return Math.max(0, Math.min(1, entry.risk_removed / total));
}

export interface FixFirstSummary {
  headline: string;
  /** One line per target about independent routes, worded for what it means. */
  routes: string[];
}

/** The decision in one sentence, then what it rests on. `null` when there are no
 *  targets to protect (the page then explains why instead). */
export function fixFirstSummary(choke: ChokeAnalysis | null | undefined): FixFirstSummary | null {
  if (!choke || !choke.targets?.length) return null;
  const fix = choke.min_fix_set;
  const names = (fix?.assets ?? []).map((a) => a.label);
  // A crown jewel that is itself exposed has no route to cut. Saying "fix the gateway" for it
  // would be false, and an empty fix set would read as "nothing reaches it".
  const exposed = choke.targets.filter(targetExposed);
  if (exposed.length > 0) {
    const who = exposed.length === 1 ? exposed[0].label : `${exposed.length} crown jewels`;
    return {
      headline: `${who} ${exposed.length === 1 ? "is" : "are"} exposed to the internet and can be exploited directly. `
        + `Fixing other hosts does not protect ${exposed.length === 1 ? "it" : "them"}; remove that exposure first.`,
      routes: [],
    };
  }
  let headline: string;
  if (!fix || fix.size === 0) {
    headline = "No modelled route reaches a crown jewel.";
  } else if (fix.size === 1) {
    headline = `Fixing ${names[0]} alone cuts every modelled route to a crown jewel.`;
  } else {
    headline = `Cutting every modelled route takes ${fix.size} hosts: ${names.join(", ")}.`;
  }
  const routes = Object.entries(fix?.independent_routes ?? {})
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([target, n]) =>
      n <= 1
        ? `${target}: one route reaches it, so a single fix on that route is enough.`
        : `${target}: ${n} independent routes reach it, so fixing one host on one route is not enough.`,
    );
  return { headline, routes };
}

/** Hosts the map marks "fix here": the smallest cutting set, plus the few single
 *  hosts whose fix removes the most risk. Marking every ranked host would make the
 *  marker meaningless. */
export function fixPointIds(choke: ChokeAnalysis | null | undefined, top = 3): Set<string> {
  const ids = new Set<string>();
  for (const a of choke?.min_fix_set?.assets ?? []) ids.add(a.asset_id);
  for (const r of (choke?.ranked ?? []).slice(0, top)) {
    if (r.risk_removed > 0) ids.add(r.asset_id);
  }
  return ids;
}

// ── Caveats that qualify every result on the page ────────────────────────────

export interface Caveat {
  tone: Tone;
  text: string;
}

export interface CaveatSummary {
  /** "partial" unless the backend reported the strongest thing it can say. */
  confidence: "observed" | "partial" | "unknown";
  items: Caveat[];
}

const plural = (n: number, one: string, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

/** What the paths do NOT cover, from the stored coverage and freshness reports.
 *  Missing reports yield `unknown`, not a clean bill of health. */
export function caveatSummary(
  coverage: Coverage | null | undefined,
  freshness: FreshnessReport | null | undefined,
): CaveatSummary {
  const items: Caveat[] = [];
  if (!coverage) {
    items.push({ tone: "weak", text: "No coverage report is available for these paths." });
  } else {
    const gaps = coverage.scope_without_observed_hosts ?? [];
    if (gaps.length) {
      const shown = gaps.slice(0, 3).map((g) => g.cidr).join(", ");
      const more = gaps.length > 3 ? ` and ${gaps.length - 3} more` : "";
      items.push({
        tone: "weak",
        text: `${plural(gaps.length, "range")} in scope with no observed host (${shown}${more}). `
          + "A route through them cannot appear.",
      });
    }
    if (coverage.observed_outside_scope?.length) {
      items.push({
        tone: "weak",
        text: `${plural(coverage.observed_outside_scope.length, "subnet")} with hosts outside the engagement scope.`,
      });
    }
    if (coverage.assets_without_a_subnet > 0) {
      items.push({
        tone: "weak",
        text: `${plural(coverage.assets_without_a_subnet, "host")} without an IP address, so ${
          coverage.assets_without_a_subnet === 1 ? "it is" : "they are"} not placed on any subnet.`,
      });
    }
    if (coverage.inferred_subnets > 0) {
      items.push({
        tone: "inferred",
        text: `${plural(coverage.inferred_subnets, "subnet")} inferred from a broad scope, not declared.`,
      });
    }
  }
  if (!freshness) {
    items.push({ tone: "weak", text: "No freshness report is available for these paths." });
  } else {
    if (freshness.stale_assets > 0) {
      const window = freshness.window_days ? ` in the last ${plural(freshness.window_days, "day")}` : "";
      items.push({
        tone: "weak",
        text: `${freshness.stale_assets} of ${plural(freshness.assets, "host")} not seen${window}. `
          + "Steps onto them may no longer hold.",
      });
    }
    if (freshness.assets_without_timestamp > 0) {
      items.push({
        tone: "inferred",
        text: `${plural(freshness.assets_without_timestamp, "host")} with no last-seen time, so their age is unknown.`,
      });
    }
  }
  const confidence = coverage ? coverage.confidence : "unknown";
  return { confidence, items };
}

// ── The route map ────────────────────────────────────────────────────────────

export const MAP = { colWidth: 196, rowHeight: 58, nodeWidth: 156, nodeHeight: 36, pad: 16 } as const;

export interface MapNode {
  id: string;
  label: string;
  col: number;
  row: number;
  x: number;
  y: number;
  isEntry: boolean;
  isTarget: boolean;
  isChoke: boolean;
}

export interface MapEdge {
  key: string;
  from: string;
  to: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  /** Ids of the listed paths that take this step. */
  paths: string[];
  /** The step runs against the left-to-right flow (a cycle between routes). */
  backward: boolean;
}

export interface PathMap {
  nodes: MapNode[];
  edges: MapEdge[];
  width: number;
  height: number;
  /** Paths drawn / paths in the list: the map shows the highest-risk routes only. */
  shown: number;
}

/**
 * Lay the highest-risk routes out left to right: entry points on the left, crown
 * jewels on the right, shared hosts where routes converge. Deterministic.
 *
 * Columns come from longest-path layering over the union of the routes. Routes can
 * form a cycle between them (a→b on one, b→a on another); relaxation is capped at
 * one pass per node so that terminates, and any edge still running backwards is
 * drawn as such rather than hidden.
 */
export function layoutPathMap(
  items: PathSummary[],
  chokeIds: ReadonlySet<string> = new Set(),
  limit = 12,
): PathMap {
  const used = items.filter((p) => p.nodes?.length >= 2).slice(0, Math.max(0, limit));
  const label = new Map<string, string>();
  const order: string[] = [];                       // first appearance, highest-risk route first
  const entries = new Set<string>();
  const targets = new Set<string>();
  const edgePaths = new Map<string, { from: string; to: string; paths: string[] }>();

  for (const p of used) {
    p.nodes.forEach((n, i) => {
      if (!label.has(n.asset_id)) { label.set(n.asset_id, n.label); order.push(n.asset_id); }
      if (i === 0) entries.add(n.asset_id);
      if (i === p.nodes.length - 1) targets.add(n.asset_id);
      if (i > 0) {
        const from = p.nodes[i - 1].asset_id;
        const key = `${from}>${n.asset_id}`;
        const e = edgePaths.get(key) ?? { from, to: n.asset_id, paths: [] };
        if (!e.paths.includes(p.id)) e.paths.push(p.id);
        edgePaths.set(key, e);
      }
    });
  }

  const col = new Map<string, number>(order.map((id) => [id, 0]));
  for (let pass = 0; pass < order.length; pass++) {
    let changed = false;
    for (const { from, to } of edgePaths.values()) {
      if (from === to) continue;
      const want = (col.get(from) ?? 0) + 1;
      if (want > (col.get(to) ?? 0) && want < order.length) { col.set(to, want); changed = true; }
    }
    if (!changed) break;
  }

  const perCol = new Map<number, string[]>();
  for (const id of order) {
    const c = col.get(id) ?? 0;
    perCol.set(c, [...(perCol.get(c) ?? []), id]);
  }
  const maxCol = Math.max(0, ...perCol.keys());
  const maxRows = Math.max(1, ...[...perCol.values()].map((v) => v.length));

  const pos = new Map<string, { x: number; y: number; row: number }>();
  const nodes: MapNode[] = [];
  for (const id of order) {
    const c = col.get(id) ?? 0;
    const row = (perCol.get(c) ?? []).indexOf(id);
    const x = MAP.pad + c * MAP.colWidth;
    const y = MAP.pad + row * MAP.rowHeight;
    pos.set(id, { x, y, row });
    nodes.push({
      id, label: label.get(id) ?? id, col: c, row, x, y,
      isEntry: entries.has(id), isTarget: targets.has(id), isChoke: chokeIds.has(id),
    });
  }

  const edges: MapEdge[] = [];
  for (const [key, e] of edgePaths) {
    const a = pos.get(e.from);
    const b = pos.get(e.to);
    if (!a || !b) continue;
    const backward = (col.get(e.to) ?? 0) <= (col.get(e.from) ?? 0);
    edges.push({
      key, from: e.from, to: e.to, paths: e.paths, backward,
      x1: a.x + MAP.nodeWidth, y1: a.y + MAP.nodeHeight / 2,
      x2: b.x, y2: b.y + MAP.nodeHeight / 2,
    });
  }

  return {
    nodes, edges, shown: used.length,
    width: MAP.pad * 2 + maxCol * MAP.colWidth + MAP.nodeWidth,
    height: MAP.pad * 2 + (maxRows - 1) * MAP.rowHeight + MAP.nodeHeight,
  };
}

/** Shorten a host label for a fixed-width SVG box (full text stays in a tooltip). */
export function truncateLabel(label: string, max = 22): string {
  const s = label ?? "";
  return s.length <= max ? s : `${s.slice(0, Math.max(1, max - 1))}…`;
}

// ── Overview: one line per engagement (dashboard and /attack-paths) ──────────

/** Each state is a different claim. Exposed is the worst case, never an empty one; not computed
 *  and no crown jewel marked are "cannot assess", never "0 reachable". */
export type OverviewState = "exposed" | "reachable" | "unreachable" | "no_targets" | "unrecorded" | "not_computed";

/** One engagement's line from GET /attack-paths/overview (stored results only). */
export interface OverviewRow {
  engagement_id: string;
  name: string;
  status: string;
  /** Sent by the server. Rows from a server that predates it are classified by `overviewState`. */
  state?: OverviewState;
  /** false = nobody has computed paths for it, which is NOT the same as zero routes. */
  computed: boolean;
  computed_at: string | null;
  /** Length of a CAPPED list (at most 5 routes per entry point per crown jewel): it tracks entry
   *  points, not exposure. Never a headline. */
  path_count: number | null;
  entry_points: number | null;
  /** Alias of `jewels_total` kept for older clients. */
  crown_jewels: number | null;
  /** null = the analysis did not record it. Unknown is not zero. */
  jewels_total?: number | null;
  jewels_reachable?: number | null;
  jewels_exposed?: number | null;
  /** The most independent routes into any reachable, non-exposed crown jewel. */
  ways_in?: number | null;
  /** Highest modelled risk (an ordering weight, not a probability). */
  top_risk?: number | null;
  fix_set_size: number | null;
  fix_assets: string[];
  fix_assets_more: number;
  coverage: "observed" | "partial" | null;
  stale_assets: number | null;
  why_empty: Reason[];
  /** The headline numbers of this engagement's last computations, oldest first (at most 12). Starts
   *  when history was first recorded, so a short or empty list is "not enough to compare", not "flat". */
  history?: HistoryPoint[];
  /** The last two computations compared. null = nothing to compare, which is not "no change". */
  change?: RowChange | null;
}

export interface HistoryPoint {
  at: string;
  state: OverviewState;
  /** null = that computation recorded no per-jewel data: a gap, never a zero. */
  reachable: number | null;
  exposed: number | null;
  assets_seen: number | null;
  coverage: "observed" | "partial" | null;
}

export interface RowChange {
  since: string;
  reachable_from: number;
  reachable_to: number;
  exposed_from: number;
  exposed_to: number;
  changed: boolean;
  /** More or fewer hosts were seen, or the coverage differed: the count can move for that reason alone. */
  inputs_changed: boolean;
}

/** Counts over ALL of the tenant's engagements, not just the rows returned. Engagements only:
 *  crown jewels and hosts of different networks are never added together except as "across". */
export interface OverviewSummary {
  engagements: number;
  computed: number;
  assessed: number;
  with_reachable: number;
  exposed: number;
  single_fix: number;
  not_computed: number;
  no_targets: number;
  unrecorded: number;
  jewels_total: number;
  jewels_reachable: number;
  /** Engagements with two computations to compare, and how many of those differ. */
  compared?: number;
  changed?: number;
  truncated?: boolean;
}

export interface Overview {
  total: number;
  shown: number;
  summary?: OverviewSummary | null;
  engagements: OverviewRow[];
}

export function overviewState(row: OverviewRow): OverviewState {
  if (row.state) return row.state;
  // A server that predates `state`: say only what the fields prove.
  if (!row.computed) return "not_computed";
  if (row.jewels_total == null) return "unrecorded";
  if (row.jewels_total === 0) return "no_targets";
  if ((row.jewels_exposed ?? 0) > 0) return "exposed";
  return (row.jewels_reachable ?? 0) > 0 ? "reachable" : "unreachable";
}

export type MeterCell = "reachable" | "unreachable" | "unknown";

const METER_MAX = 8;

/** One diamond per crown jewel (at most 8, the rest counted): filled = reachable, hollow = not,
 *  dashed = nothing to count (not computed, no crown jewel marked, not recorded). The words
 *  beside the meter carry the meaning; the meter is only a quick read of the same numbers. */
export function meterCells(row: OverviewRow): { cells: MeterCell[]; more: number } {
  const state = overviewState(row);
  const total = row.jewels_total;
  if (state === "not_computed" || state === "no_targets" || state === "unrecorded" || !total || total < 1) {
    return { cells: ["unknown"], more: 0 };
  }
  const shown = Math.min(total, METER_MAX);
  const filled = Math.min(row.jewels_reachable ?? 0, shown);
  return {
    cells: Array.from({ length: shown }, (_, i): MeterCell => (i < filled ? "reachable" : "unreachable")),
    more: total - shown,
  };
}

/** The decision for one row, in one sentence. Never "fix the gateway" for a jewel that is exposed
 *  outright (the caller does not ask in that state). */
export function fixSentence(row: Pick<OverviewRow, "fix_set_size" | "fix_assets" | "fix_assets_more">): string | null {
  const size = row.fix_set_size;
  if (size == null) return null;
  const names = row.fix_assets;
  if (size === 0) return "The analysis found no host whose fix cuts these routes.";
  if (size === 1) return names.length === 1 ? `Fixing ${names[0]} alone cuts every route.` : "Fixing one host cuts every route.";
  const list = names.length > 0 ? `: ${names.join(", ")}${row.fix_assets_more > 0 ? `, +${row.fix_assets_more} more` : ""}` : "";
  return `No single host fixes this: cutting every route takes ${size} hosts${list}.`;
}

export interface OverviewLine {
  state: OverviewState;
  headline: string;
  /** The decision, or why there is nothing to decide. Null when there is nothing honest to add. */
  detail: string | null;
  /** "2 separate ways in", only where it is true. */
  ways: string | null;
  coverage: { label: string; tone: Tone } | null;
  stale: string | null;
}

/** What one overview row says. The wording rules are the page's: not computed is not
 *  "0 routes", an exposed jewel is not an empty result, zero reachable is never "safe",
 *  coverage is "observed" or "partial", and a report the analysis did not record is said
 *  to be missing. */
export function overviewLine(row: OverviewRow): OverviewLine {
  const state = overviewState(row);
  const none = { ways: null, coverage: null, stale: null };
  if (state === "not_computed") {
    return { state, headline: "Not computed yet", detail: "Open it to compute the routes.", ...none };
  }
  if (state === "unrecorded") {
    return { state, headline: "Computed; per-jewel detail not recorded", detail: "Open it to refresh the analysis.", ...none };
  }
  const coverage = row.coverage === "partial"
    ? { label: "Coverage partial", tone: "weak" as Tone }
    : row.coverage === "observed"
      ? { label: "Coverage observed", tone: "firm" as Tone }
      : { label: "Coverage not recorded", tone: "neutral" as Tone };
  const stale = (row.stale_assets ?? 0) > 0 ? `${plural(row.stale_assets as number, "host")} not seen recently` : null;
  const total = row.jewels_total ?? 0;
  const reachable = row.jewels_reachable ?? 0;

  if (state === "exposed") {
    const n = row.jewels_exposed ?? 1;
    const also = reachable > n ? ` ${plural(reachable - n, "more crown jewel")} can be reached by a route.` : "";
    return {
      state,
      headline: `${plural(n, "crown jewel")} directly exposed to the internet`,
      detail: `Fixing hosts on the way in does not protect ${n === 1 ? "it" : "them"}. Remove the exposure first.${also}`,
      ways: null, coverage, stale,
    };
  }
  if (state === "reachable") {
    const ways = row.ways_in && row.ways_in > 0 ? `${plural(row.ways_in, "separate way")} in` : null;
    return {
      state,
      headline: `${reachable} of ${plural(total, "crown jewel")} reachable`,
      detail: fixSentence(row), ways, coverage, stale,
    };
  }
  if (state === "no_targets") {
    // An engagement with no hosts at all says that first: "no asset is marked critical" is true of it, but not the news.
    const lead = emptyReasons({ reasons: row.why_empty } as Diagnostics).find((r) => r.code !== "no_targets");
    return {
      state, headline: "No crown jewels marked",
      detail: `${lead ? `${lead.title}. ` : ""}No asset is marked critical, so the model has nothing to protect. Mark the assets that matter to model routes to them. This is not evidence the network is safe.`,
      ways: null, coverage, stale,
    };
  }
  const first = emptyReasons({ reasons: row.why_empty } as Diagnostics)[0];
  const why = first ? `${first.title}.` : "The analysis recorded no reason.";
  return {
    state, headline: "No modelled route reaches a crown jewel",
    detail: `${why} This is not evidence the network is safe.`, ways: null, coverage, stale,
  };
}

export type TileTone = "critical" | "high" | "neutral";

export interface OverviewTile {
  key: "reachable" | "one_fix" | "unassessed";
  label: string;
  /** A number, or "—" when there is nothing to count (never "0 of 0"). */
  value: string;
  unit: string;
  sub: string;
  tone: TileTone;
}

/** The three triage tiles. Counts of ENGAGEMENTS only, so networks that are not alike are never
 *  added together; per-network numbers stay on each row. Null when the server sent no summary. */
export function overviewTiles(summary: OverviewSummary | null | undefined): OverviewTile[] | null {
  if (!summary) return null;
  const s = summary;
  const fixable = s.with_reachable - s.exposed;          // reachable by a route only: a fix set means something

  const t1: OverviewTile = s.assessed === 0
    ? {
        key: "reachable", label: "Engagements with a reachable crown jewel", value: "—", unit: "", tone: "neutral",
        sub: s.computed === 0 ? "Nothing computed yet." : "No computed engagement has a crown jewel marked.",
      }
    : {
        key: "reachable", label: "Engagements with a reachable crown jewel", value: String(s.with_reachable),
        unit: `of ${s.assessed} assessed`,
        sub: s.exposed > 0
          ? `${s.exposed} with a crown jewel directly exposed to the internet.`
          : s.with_reachable > 0
            ? `${s.jewels_reachable} of ${plural(s.jewels_total, "crown jewel")} reachable across them.`
            : "None reachable in the model. This is not evidence the network is safe.",
        tone: s.exposed > 0 ? "critical" : s.with_reachable > 0 ? "high" : "neutral",
      };
  if ((s.compared ?? 0) > 0) {
    // A plain count of differences: whether a difference is good or bad is not something two numbers say.
    t1.sub += ` ${s.changed ?? 0} of ${s.compared} changed since their previous computation.`;
  }

  const t2: OverviewTile = fixable <= 0
    ? {
        key: "one_fix", label: "Cut by fixing one host", value: "—", unit: "", tone: "neutral",
        sub: s.exposed > 0 ? "Exposed jewels need their exposure removed, not a fix on the way in." : "Nothing to fix in the model.",
      }
    : {
        key: "one_fix", label: "Cut by fixing one host", value: String(s.single_fix), unit: `of ${fixable}`,
        sub: fixable - s.single_fix > 0 ? `${fixable - s.single_fix} need several fixes.` : "One host each cuts every route.",
        tone: "neutral",
      };

  const n = s.not_computed + s.no_targets + s.unrecorded;
  const parts = [
    s.not_computed > 0 ? `${s.not_computed} not computed` : null,
    s.no_targets > 0 ? `${s.no_targets} with no crown jewel marked` : null,
    s.unrecorded > 0 ? `${s.unrecorded} not recorded` : null,
  ].filter(Boolean) as string[];
  const t3: OverviewTile = {
    key: "unassessed", label: "Can't be assessed yet", value: String(n), unit: n === 1 ? "engagement" : "engagements",
    sub: parts.length > 0 ? `${parts.join(" · ")}.` : "Every engagement has been assessed.", tone: "neutral",
  };
  return [t1, t2, t3];
}

/** The footer line. Counts only what is true; empty when the server sent no summary. */
export function overviewSummary(o: Overview | null | undefined): string {
  const s = o?.summary;
  if (!s || s.engagements === 0) return o && o.engagements.length === 0 ? "No engagements" : "";
  const unassessed = s.not_computed + s.no_targets + s.unrecorded;
  const base = s.assessed === 0
    ? "No engagement assessed yet"
    : `${s.with_reachable} of ${plural(s.assessed, "assessed engagement")} ${s.with_reachable === 1 ? "has" : "have"} a reachable crown jewel`;
  return unassessed > 0 ? `${base} · ${unassessed} can't be assessed yet` : base;
}

// ── Fix first: the dashboard card for one engagement ─────────────────────────

export interface FocusNode {
  asset_id: string;
  label: string;
  role: "entry" | "via" | "jewel";
  /** In the smallest fix set, or one of the few hosts whose fix removes the most risk. */
  on_fix_list: boolean;
}

export interface FocusHop {
  basis: string | null;
  technique: string | null;
  stale: boolean;
  exploited: boolean | null;
  capability?: string | null;
}

export interface FocusRoute {
  path_id: string;
  risk_score: number | null;
  freshness: Freshness | null;
  nodes: FocusNode[];
  /** hops[i] is the step from nodes[i] to nodes[i + 1]. */
  hops: FocusHop[];
}

export interface FocusBar {
  asset_id: string;
  label: string;
  /** Share (0-1) of the engagement's modelled risk this host removes ALONE; null = no modelled risk. */
  share: number | null;
  cuts_off: number;
  jewels_reachable: number | null;
}

export interface Focus {
  engagement_id: string;
  name: string;
  state: OverviewState;
  computed: boolean;
  computed_at: string | null;
  /** Length of the capped stored list, not a count of routes. */
  path_count: number | null;
  exposed: { asset_id: string; label: string }[];
  route: FocusRoute | null;
  fix: {
    size: number;
    assets: { asset_id: string; label: string }[];
    independent_routes: Record<string, number>;
    exposed_targets?: { asset_id: string; label: string }[];
  } | null;
  ranked: FocusBar[];
}

/** The card's lead sentence. For an exposed jewel it never says "fix the gateway". */
export function focusLead(f: Focus): string | null {
  if (f.state === "exposed" && f.exposed.length > 0) {
    const who = f.exposed.length === 1 ? f.exposed[0].label : `${f.exposed.length} crown jewels`;
    return `${who} ${f.exposed.length === 1 ? "is" : "are"} exposed to the internet and can be exploited directly. `
      + `Fixing other hosts does not protect ${f.exposed.length === 1 ? "it" : "them"}; remove that exposure first.`;
  }
  if (f.state !== "reachable" || !f.fix) return null;
  const names = f.fix.assets.map((a) => a.label);
  if (f.fix.size === 0) return "The analysis found no host whose fix cuts these routes.";
  if (f.fix.size === 1) return `Fixing ${names[0] ?? "one host"} alone cuts every modelled route to a crown jewel.`;
  return `No single host fixes this: cutting every modelled route takes ${f.fix.size} hosts${names.length ? `: ${names.join(", ")}` : ""}.`;
}

export type ChainItem =
  | { kind: "node"; node: FocusNode; hop: { label: string; step: string | null; caveat: string | null; weak: boolean; stale: boolean } | null }
  | { kind: "gap"; hidden: number; weakHidden: boolean };

const CHAIN_MAX = 5;

/** The route as a short chain. A long route keeps its entry, its crown jewel and every host on the
 *  fix list, then fills up to five nodes from the entry end; what is left out becomes "+N more
 *  hosts" and says if an assumed link is among them. A step is described only between two nodes
 *  that are both shown, so a hidden step never borrows a neighbour's wording. */
export function routeChainView(route: FocusRoute | null | undefined): ChainItem[] {
  if (!route || route.nodes.length === 0) return [];
  const n = route.nodes.length;
  const keep = new Set<number>([0, n - 1]);
  route.nodes.forEach((node, i) => { if (node.on_fix_list) keep.add(i); });
  for (let i = 1; i < n - 1 && keep.size < CHAIN_MAX; i++) keep.add(i);

  const hopFor = (i: number): { label: string; step: string | null; caveat: string | null; weak: boolean; stale: boolean } | null => {
    const h = route.hops[i];
    if (!h) return null;
    const info = basisInfo(h.basis);
    // What the step IS: an NTLM relay / reused credential names itself; otherwise the
    // capability the destination's weakness grants (foothold/lateral), else the movement.
    const step = h.technique === "RELAY" || h.technique === "CREDENTIAL_REUSE"
      ? techniqueLabel(h.technique)
      : (capabilityLabel(h.capability) ?? techniqueLabel(h.technique));
    return { label: info.label, step, caveat: info.caveat, weak: info.tone === "weak", stale: h.stale };
  };

  const out: ChainItem[] = [];
  let i = 0;
  while (i < n) {
    if (keep.has(i)) {
      out.push({ kind: "node", node: route.nodes[i], hop: keep.has(i + 1) ? hopFor(i) : null });
      i += 1;
      continue;
    }
    let j = i;
    while (j < n && !keep.has(j)) j += 1;
    // hops i-1 .. j-1 all touch hidden hosts
    const weakHidden = Array.from({ length: j - i + 1 }, (_, k) => i - 1 + k)
      .some((k) => k >= 0 && route.hops[k] && basisInfo(route.hops[k].basis).tone === "weak");
    out.push({ kind: "gap", hidden: j - i, weakHidden });
    i = j;
  }
  return out;
}

export interface BarView {
  key: string;
  name: string;
  /** "82%", or "—" when there is no modelled risk to share. */
  value: string;
  /** 0-100, for the bar's width. */
  width: number;
  sub: string;
}

/** One bar per host: the share of modelled risk it removes ALONE. Never stacked or summed. */
export function focusBars(f: Focus): BarView[] {
  return f.ranked.map((b) => ({
    key: b.asset_id,
    name: b.label,
    value: percent(b.share),
    width: b.share == null ? 0 : Math.round(Math.max(0, Math.min(1, b.share)) * 100),
    sub: b.jewels_reachable != null
      ? `Cuts off ${b.cuts_off} of ${plural(b.jewels_reachable, "reachable crown jewel")} on its own.`
      : `Cuts off ${b.cuts_off} crown jewel${b.cuts_off === 1 ? "" : "s"} on its own.`,
  }));
}

// ── History: a trend that says only what two numbers say ─────────────────────

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "Oct 9" from an ISO timestamp, in UTC so it reads the same wherever it is rendered. */
export function shortDate(iso: string | null | undefined): string {
  const d = iso ? new Date(iso) : null;
  return d && !Number.isNaN(d.getTime()) ? `${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}` : "an earlier computation";
}

export interface TrendView {
  /** reachable crown jewels at each recorded computation, oldest first; null = a gap */
  values: (number | null)[];
  /** What the sparkline shows, as text: the same numbers, for anyone who cannot see a line. */
  twin: string;
  /** Null when only one comparable computation exists: no change is said, not even "unchanged". */
  change: string | null;
  changed: boolean;
  /** Said beside a change whose inputs differed. */
  note: string | null;
}

/** The trend of one row, or null when there are fewer than two recorded computations. Never says
 *  "better" or "worse": a rise can be the network or can be more of the network being seen. */
export function trendView(row: OverviewRow): TrendView | null {
  const h = row.history ?? [];
  if (h.length < 2) return null;
  const values = h.map((p) => p.reachable);
  const twin = `Crown jewels reachable at the last ${h.length} computations, oldest first: ${values.map((v) => (v == null ? "not recorded" : String(v))).join(", ")}.`;
  const c = row.change;
  if (!c) return { values, twin, change: null, changed: false, note: null };
  const exposed = c.exposed_from !== c.exposed_to ? `; directly exposed ${c.exposed_from} → ${c.exposed_to}` : "";
  const change = c.changed
    ? `Changed since ${shortDate(c.since)}: ${c.reachable_from} → ${c.reachable_to} reachable${exposed}`
    : `Unchanged since ${shortDate(c.since)}: ${c.reachable_to} reachable`;
  return {
    values, twin, change, changed: c.changed,
    note: c.changed && c.inputs_changed ? "More or fewer hosts were seen, or the coverage differed, so part of this may be what was looked at, not the network." : null,
  };
}

export interface Spark {
  /** One polyline per run of recorded values (a gap breaks the line). */
  segments: string[];
  /** Where the latest value sits, or null when it is a gap. */
  last: { x: number; y: number } | null;
}

/** Points for a sparkline `w` x `h`, `pad` in from the edge so the end dot is not clipped. The scale
 *  starts at zero, so a small wobble stays small. */
export function sparkline(values: (number | null)[], w = 64, h = 20, pad = 5): Spark {
  const known = values.filter((v): v is number => v != null);
  const top = Math.max(1, ...known);
  const x = (i: number) => (values.length === 1 ? w / 2 : pad + (i * (w - 2 * pad)) / (values.length - 1));
  const y = (v: number) => h - pad - (v / top) * (h - 2 * pad);
  const segments: string[] = [];
  let run: string[] = [];
  values.forEach((v, i) => {
    if (v == null) { if (run.length > 1) segments.push(run.join(" ")); run = []; return; }
    run.push(`${x(i).toFixed(1)},${y(v).toFixed(1)}`);
  });
  if (run.length > 1) segments.push(run.join(" "));
  const lastV = values[values.length - 1];
  return { segments, last: lastV == null ? null : { x: x(values.length - 1), y: y(lastV) } };
}

// ── Surfacing: the "needs attention" item and the Compute action ─────────────

export interface AttentionItem {
  /** Short on purpose: the strip truncates a label at about 30 characters, so the count sits in `detail`. */
  label: string;
  detail: string;
  /** high = a crown jewel is exposed outright; medium = reachable by a modelled route. Neither is "critical":
   *  that word on the strip belongs to measured findings, and this is a Beta model. */
  tone: "high" | "medium";
  href: string;
}

/** The one line the "Needs attention now" strip may carry about attack paths, or null when the model has
 *  nothing reachable to point at (a quiet model is not a clear bill of health, so it says nothing). */
export function attackPathAttention(summary: OverviewSummary | null | undefined): AttentionItem | null {
  if (!summary) return null;
  const href = "/attack-paths";
  if (summary.exposed > 0) {
    return {
      label: "Crown jewel exposed (Beta)",
      detail: `${plural(summary.exposed, "engagement")} · remove the exposure first`, tone: "high", href,
    };
  }
  if (summary.with_reachable > 0) {
    return {
      label: "Crown jewel reachable (Beta)",
      detail: `${plural(summary.with_reachable, "engagement")} · modelled, not measured`, tone: "medium", href,
    };
  }
  return null;
}

/** Rows a person can ask to compute: nothing is stored yet, or the stored analysis recorded no per-jewel
 *  data. A row with no crown jewel marked is not offered: computing again cannot change that. */
export function canCompute(row: Pick<OverviewRow, "state" | "computed" | "jewels_total">): boolean {
  const state = overviewState(row as OverviewRow);
  return state === "not_computed" || state === "unrecorded";
}

// ── Zones: the stored routes grouped into the subnets they cross ─────────────

export interface Zone {
  key: string;
  /** "10.0.1.0/24", or "10.0.1.0/24 @ HQ" when the subnet belongs to a site. */
  label: string;
  /** Hosts the analysis observed in it; null = not recorded. */
  hosts: number | null;
  stale_hosts: number | null;
  inferred: boolean;
  in_scope: boolean;
  entry: boolean;
  jewel: boolean;
  fix: boolean;
  /** Stored routes (a capped list) that pass through it. */
  routes: number;
}

export interface ZoneLink {
  from: string;
  to: string;
  /** Stored routes (a capped list) that take this step. */
  routes: number;
  basis: string;
  weak: boolean;
}

export interface ZoneView {
  engagement_id: string | null;
  computed: boolean;
  computed_at: string | null;
  routes_considered: number | null;
  routes_truncated?: boolean;
  zones: Zone[];
  links: ZoneLink[];
  /** Subnets with hosts that no stored route touches. */
  other_zones: number;
  /** Hosts the analysis could not place in any subnet. */
  unplaced_assets: number | null;
  zones_hidden: number;
  links_hidden: number;
  routes_unplaced: number;
  entry_unplaced: number;
  jewel_unplaced: number;
}

export const ZONE = { boxWidth: 176, boxHeight: 66, colGap: 132, rowGap: 24, pad: 16 } as const;

export interface ZoneNode extends Zone {
  col: number;
  row: number;
  x: number;
  y: number;
  /** The roles in words (never colour alone), in reading order. */
  roles: string[];
}

export interface ZoneEdge extends ZoneLink {
  key: string;
  x1: number; y1: number; x2: number; y2: number;
  /** Runs against the left-to-right flow, or within one column: drawn as an arc over the top. */
  backward: boolean;
  basisLabel: string;
}

export interface ZoneMapLayout {
  nodes: ZoneNode[];
  edges: ZoneEdge[];
  width: number;
  height: number;
}

export function zoneRoles(z: Pick<Zone, "entry" | "jewel" | "fix" | "inferred">): string[] {
  const roles: string[] = [];
  if (z.entry) roles.push("Entry");
  if (z.jewel) roles.push("Crown jewel");
  if (z.fix) roles.push("Fix here");
  if (z.inferred) roles.push("Inferred subnet");
  return roles;
}

/**
 * Subnets left to right: the ones routes start in on the left, and each further subnet one column
 * after the nearest subnet that leads to it. Deterministic. A subnet no step leads to (all of a route
 * stays inside it, or the steps form a cycle) sits in the first column rather than disappearing, and
 * a step that runs against the flow is drawn as an arc, not hidden.
 */
export function layoutZoneMap(zones: Zone[], links: ZoneLink[]): ZoneMapLayout {
  if (zones.length === 0) return { nodes: [], edges: [], width: 0, height: 0 };
  const known = new Set(zones.map((z) => z.key));
  const usable = links.filter((l) => known.has(l.from) && known.has(l.to) && l.from !== l.to);
  const incoming = new Set(usable.map((l) => l.to));
  const starts = zones.filter((z) => z.entry || !incoming.has(z.key)).map((z) => z.key);

  const depth = new Map<string, number>(starts.map((k) => [k, 0]));
  const queue = [...starts];
  while (queue.length) {
    const k = queue.shift() as string;
    for (const l of usable) {
      if (l.from === k && !depth.has(l.to)) { depth.set(l.to, (depth.get(k) ?? 0) + 1); queue.push(l.to); }
    }
  }
  for (const z of zones) if (!depth.has(z.key)) depth.set(z.key, 0);

  const columns = new Map<number, Zone[]>();
  for (const z of [...zones].sort((a, b) => a.label.localeCompare(b.label))) {
    const c = depth.get(z.key) ?? 0;
    columns.set(c, [...(columns.get(c) ?? []), z]);
  }
  // Order each column by where its sources sit in the column before (fewer crossings), then by name.
  const rowOf = new Map<string, number>();
  const maxCol = Math.max(...columns.keys());
  for (let c = 0; c <= maxCol; c++) {
    const col = columns.get(c) ?? [];
    const score = (z: Zone) => {
      const src = usable.filter((l) => l.to === z.key && (depth.get(l.from) ?? 0) < c).map((l) => rowOf.get(l.from) ?? 0);
      return src.length ? src.reduce((a, b) => a + b, 0) / src.length : Number.MAX_SAFE_INTEGER;
    };
    col.sort((a, b) => score(a) - score(b) || a.label.localeCompare(b.label));
    col.forEach((z, i) => rowOf.set(z.key, i));
    columns.set(c, col);
  }

  const maxRows = Math.max(...[...columns.values()].map((v) => v.length));
  const nodes: ZoneNode[] = [];
  for (const [c, col] of columns) {
    col.forEach((z, i) => nodes.push({
      ...z, col: c, row: i, roles: zoneRoles(z),
      x: ZONE.pad + c * (ZONE.boxWidth + ZONE.colGap),
      y: ZONE.pad + i * (ZONE.boxHeight + ZONE.rowGap),
    }));
  }
  const at = new Map(nodes.map((n) => [n.key, n]));
  const edges: ZoneEdge[] = usable.map((l) => {
    const a = at.get(l.from) as ZoneNode;
    const b = at.get(l.to) as ZoneNode;
    return {
      ...l, key: `${l.from}>${l.to}`,
      x1: a.x + ZONE.boxWidth, y1: a.y + ZONE.boxHeight / 2, x2: b.x, y2: b.y + ZONE.boxHeight / 2,
      backward: b.col <= a.col, basisLabel: basisInfo(l.basis).label,
    };
  });
  return {
    nodes, edges,
    width: ZONE.pad * 2 + maxCol * (ZONE.boxWidth + ZONE.colGap) + ZONE.boxWidth,
    height: ZONE.pad * 2 + (maxRows - 1) * (ZONE.boxHeight + ZONE.rowGap) + ZONE.boxHeight,
  };
}

export interface ZoneSummary {
  /** One sentence on what the picture says, with the counts it rests on. Null when there is nothing drawn. */
  lead: string | null;
  /** What the picture leaves out, each as its own sentence. */
  notes: string[];
}

/** The sentence above the zone map and the things it does not show. Counts are of STORED routes, a capped
 *  list, and are worded as "listed", never as how exposed a subnet is. */
export function zoneSummary(v: ZoneView | null | undefined): ZoneSummary {
  if (!v || !v.computed) return { lead: null, notes: [] };
  const notes: string[] = [];
  if (v.zones.length === 0) {
    if ((v.routes_considered ?? 0) > 0 && v.routes_unplaced > 0) {
      notes.push(`${plural(v.routes_unplaced, "listed route")} could not be placed in any subnet, so none is drawn.`);
    }
    return { lead: null, notes };
  }
  const entries = v.zones.filter((z) => z.entry).length;
  const jewels = v.zones.filter((z) => z.jewel).length;
  const weak = v.links.filter((l) => l.weak).length;
  const steps = v.links.length;
  const where = [
    entries > 0 ? `start in ${plural(entries, "subnet")}` : null,
    jewels > 0 ? `end in ${plural(jewels, "subnet")}` : null,
  ].filter(Boolean).join(" and ");
  let crossing: string;
  if (steps === 0) {
    crossing = "no step crosses from one subnet to another";
  } else {
    const basis = weak === 0 ? "none of them rests on an assumed link"
      : weak === steps ? (steps === 1 ? "it rests on an assumed link" : "all of them rest on assumed links")
      : `${weak} of them ${weak === 1 ? "rests" : "rest"} on ${weak === 1 ? "an assumed link" : "assumed links"}`;
    crossing = `${plural(steps, "step")} ${steps === 1 ? "crosses" : "cross"} between subnets, and ${basis}`;
  }
  const lead = `The listed routes ${where || "pass through these subnets"}; ${crossing}.`;
  if (v.entry_unplaced > 0) notes.push(`${plural(v.entry_unplaced, "listed route")} start${v.entry_unplaced === 1 ? "s" : ""} at a host the analysis did not place in a subnet, so no entry subnet is claimed for ${v.entry_unplaced === 1 ? "it" : "them"}.`);
  if (v.jewel_unplaced > 0) notes.push(`${plural(v.jewel_unplaced, "listed route")} end${v.jewel_unplaced === 1 ? "s" : ""} at a crown jewel the analysis did not place in a subnet.`);
  if (v.other_zones > 0) notes.push(`${plural(v.other_zones, "other subnet")} ${v.other_zones === 1 ? "has" : "have"} hosts but no listed route touches ${v.other_zones === 1 ? "it" : "them"}.`);
  if ((v.unplaced_assets ?? 0) > 0) notes.push(`${plural(v.unplaced_assets as number, "host")} could not be placed in any subnet and ${v.unplaced_assets === 1 ? "is" : "are"} not drawn.`);
  if (v.zones_hidden > 0) notes.push(`${plural(v.zones_hidden, "more subnet")} ${v.zones_hidden === 1 ? "is" : "are"} not drawn (the ones with a role are shown first).`);
  if (v.routes_truncated) notes.push("Only the first 500 stored routes were aggregated.");
  return { lead, notes };
}
