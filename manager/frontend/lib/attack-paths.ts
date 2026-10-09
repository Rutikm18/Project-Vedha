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
  /** 0-100: modelled risk removed if this one host were fixed. */
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
}

export interface ChokeAnalysis {
  ranked: ChokeEntry[];
  min_fix_set: FixSet;
  targets: { asset_id: string; label: string; best_likelihood: number; risk: number }[];
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
    case "SAME_HOST": return "Same machine";
    case "SAME_SEGMENT": return "Within segment";
    case "CONNECTS_TO": return "Network connection";
    default: return technique ? humanize(technique) : "Step";
  }
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

/** One engagement's line from GET /attack-paths/overview (stored results only). */
export interface OverviewRow {
  engagement_id: string;
  name: string;
  status: string;
  /** false = nobody has computed paths for it, which is NOT the same as zero routes. */
  computed: boolean;
  computed_at: string | null;
  path_count: number | null;
  entry_points: number | null;
  crown_jewels: number | null;
  fix_set_size: number | null;
  fix_assets: string[];
  fix_assets_more: number;
  coverage: "observed" | "partial" | null;
  stale_assets: number | null;
  why_empty: Reason[];
}

export interface Overview {
  total: number;
  shown: number;
  engagements: OverviewRow[];
}

export type OverviewState = "routes" | "empty" | "not_computed";

export function overviewState(row: OverviewRow): OverviewState {
  if (!row.computed) return "not_computed";
  return (row.path_count ?? 0) > 0 ? "routes" : "empty";
}

export interface OverviewLine {
  state: OverviewState;
  headline: string;
  /** The decision, or why there is nothing to decide. Null when there is nothing honest to add. */
  detail: string | null;
  coverage: { label: string; tone: Tone } | null;
  stale: string | null;
}

/** What one overview row says. The wording rules are the page's: not computed is not
 *  "0 routes", zero routes is never "safe", coverage is "observed" or "partial", and
 *  a report the analysis did not record is said to be missing. */
export function overviewLine(row: OverviewRow): OverviewLine {
  const state = overviewState(row);
  if (state === "not_computed") {
    return { state, headline: "Not computed yet", detail: "Open it to compute the routes.", coverage: null, stale: null };
  }
  const coverage = row.coverage === "partial"
    ? { label: "Coverage partial", tone: "weak" as Tone }
    : row.coverage === "observed"
      ? { label: "Coverage observed", tone: "firm" as Tone }
      : { label: "Coverage not recorded", tone: "neutral" as Tone };
  const stale = (row.stale_assets ?? 0) > 0
    ? `${plural(row.stale_assets as number, "host")} not seen recently`
    : null;

  if (state === "empty") {
    const first = emptyReasons({ reasons: row.why_empty } as Diagnostics)[0];
    const why = first ? `${first.title}.` : "The analysis recorded no reason.";
    return {
      state, headline: "No routes modelled",
      detail: `${why} This is not evidence the network is safe.`, coverage, stale,
    };
  }

  const n = row.path_count as number;
  const names = row.fix_assets;
  let detail: string | null = null;
  if ((row.fix_set_size ?? 0) === 1 && names.length === 1) {
    detail = `Fixing ${names[0]} alone cuts every route.`;
  } else if ((row.fix_set_size ?? 0) > 1 && names.length > 0) {
    detail = `Cutting every route takes ${row.fix_set_size} hosts: ${names.join(", ")}${row.fix_assets_more > 0 ? `, +${row.fix_assets_more} more` : ""}.`;
  }
  return { state, headline: `${n} ${n === 1 ? "route" : "routes"}`, detail, coverage, stale };
}

/** "3 of 5 engagements have routes · 1 not computed yet" — counts only what is true. */
export function overviewSummary(o: Overview | null | undefined): string {
  const rows = o?.engagements ?? [];
  if (!rows.length) return "No engagements";
  const withRoutes = rows.filter((r) => overviewState(r) === "routes").length;
  const notComputed = rows.filter((r) => overviewState(r) === "not_computed").length;
  const base = `${withRoutes} of ${plural(rows.length, "engagement")} ha${withRoutes === 1 ? "s" : "ve"} routes`;
  return notComputed > 0 ? `${base} · ${notComputed} not computed yet` : base;
}
