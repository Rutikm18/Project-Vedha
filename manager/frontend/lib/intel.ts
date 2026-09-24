/**
 * intel.ts — pure helpers for evidence-based asset tags and regional compliance
 * (backend: app/intel/tagging.py, app/compliance/). No React, no fetch — unit-tested.
 */

export interface TagRecord {
  key: string;
  value: string;
  rule?: string;
  confidence?: number;
  evidence?: string;
  source?: "auto" | "manual" | string;
}

export interface TagsDoc {
  v?: number;
  auto?: TagRecord[];
  manual?: TagRecord[];
}

export interface TaggedAsset {
  id: string;
  tags?: TagsDoc | null;
}

export type TagTone = "risk" | "sector" | "manual" | "neutral";

// Display order: what an analyst needs first. Unknown (manual) keys sit before zone.
const KEY_ORDER = [
  "exposure", "data_sensitivity", "sector_fn", "compliance_scope", "role",
  "host_type", "os_family", "domain",
];
const LAST_KEYS = ["zone"];

const KEY_LABEL: Record<string, string> = {
  host_type: "Type", os_family: "OS", role: "Role", exposure: "Exposure", zone: "Segment",
  domain: "Domain", sector_fn: "Banking function", compliance_scope: "Compliance scope",
  data_sensitivity: "Sensitivity",
};

const VALUE_LABEL: Record<string, string> = {
  pci_cde_candidate: "PCI CDE candidate",
  swift_cscf_scope: "SWIFT CSCF scope",
  critical_financial_system: "Critical financial system",
  swift: "SWIFT", hsm: "HSM", atm: "ATM", ics: "ICS/OT", dns: "DNS", vpn: "VPN",
  voip: "VoIP", macos: "macOS", network_os: "Network OS", bsd: "BSD",
};

const AUTO_KEYS = new Set([...KEY_ORDER, ...LAST_KEYS]);

export function keyLabel(key: string): string {
  return KEY_LABEL[key] ?? key.replaceAll("_", " ");
}

function humanize(value: string): string {
  if (VALUE_LABEL[value]) return VALUE_LABEL[value];
  const text = value.replaceAll("_", " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/** Chip text. Known namespaces show just the value; custom keys show "key: value". */
export function tagLabel(tag: Pick<TagRecord, "key" | "value">): string {
  if (tag.key === "zone" || tag.key === "domain") return tag.value;
  if (AUTO_KEYS.has(tag.key)) return humanize(tag.value);
  return `${keyLabel(tag.key)}: ${tag.value}`;
}

export function tagTone(tag: TagRecord): TagTone {
  if (tag.source === "manual") return "manual";
  if (tag.key === "exposure" && tag.value === "internet_facing") return "risk";
  if (tag.key === "data_sensitivity" && tag.value === "restricted") return "risk";
  if (tag.key === "sector_fn" || tag.key === "compliance_scope") return "sector";
  return "neutral";
}

export function tagTitle(tag: TagRecord): string {
  const parts = [`${keyLabel(tag.key)}: ${tag.value}`];
  if (tag.source === "manual") parts.push("added by an operator");
  else {
    if (tag.evidence) parts.push(`evidence: ${tag.evidence}`);
    if (typeof tag.confidence === "number") parts.push(`confidence ${Math.round(tag.confidence * 100)}%`);
  }
  return parts.join(" · ");
}

function rank(key: string): number {
  if (LAST_KEYS.includes(key)) return 1000;
  const i = KEY_ORDER.indexOf(key);
  return i === -1 ? 500 : i;
}

export function tagString(tag: Pick<TagRecord, "key" | "value">): string {
  return `${tag.key}:${tag.value}`;
}

/** Auto + manual tags for one asset, deduped, in display order. */
export function assetTags(asset: TaggedAsset): TagRecord[] {
  const doc = asset.tags;
  if (!doc || typeof doc !== "object") return [];
  const seen = new Set<string>();
  const out: TagRecord[] = [];
  for (const [bucket, list] of [["auto", doc.auto], ["manual", doc.manual]] as const) {
    for (const tag of list ?? []) {
      if (!tag?.key || !tag?.value) continue;
      const id = tagString(tag);
      if (seen.has(id)) continue;
      seen.add(id);
      out.push({ ...tag, source: tag.source ?? bucket });
    }
  }
  return out
    .map((tag, index) => ({ tag, index }))
    .sort((a, b) => rank(a.tag.key) - rank(b.tag.key) || a.index - b.index)
    .map(({ tag }) => tag);
}

export interface TagCount {
  tag: string;
  record: TagRecord;
  count: number;
}

/** How many assets carry each tag, most common first. */
export function tagCounts(assets: TaggedAsset[]): TagCount[] {
  const counts = new Map<string, TagCount>();
  for (const asset of assets) {
    for (const record of assetTags(asset)) {
      const tag = tagString(record);
      const entry = counts.get(tag) ?? { tag, record, count: 0 };
      entry.count += 1;
      counts.set(tag, entry);
    }
  }
  return [...counts.values()].sort((a, b) =>
    b.count - a.count || rank(a.record.key) - rank(b.record.key) || a.tag.localeCompare(b.tag));
}

/** Assets carrying EVERY selected tag (AND), matching the backend's ?tag= semantics. */
export function filterAssetsByTags<T extends TaggedAsset>(assets: T[], selected: string[]): T[] {
  if (!selected.length) return assets;
  return assets.filter((asset) => {
    const have = new Set(assetTags(asset).map(tagString));
    return selected.every((tag) => have.has(tag));
  });
}

// Mirrors app/intel/fragile.py — hosts limited to gentle scans unless overridden.
const FRAGILE_TAGS = ["sector_fn:hsm", "sector_fn:atm", "sector_fn:swift", "role:ics", "scan_policy:fragile"];

export function fragileReasons(asset: TaggedAsset): string[] {
  const have = new Set(assetTags(asset).map(tagString));
  if (have.has("scan_policy:standard")) return [];
  return FRAGILE_TAGS.filter((tag) => have.has(tag));
}

const MANUAL_KEY = /^[a-z][a-z0-9_]{0,39}$/;

/** Parse the manual-tag editor ("key: value" per line) with the backend's rules. */
export function parseManualTags(text: string): { tags: Array<{ key: string; value: string }>; errors: string[] } {
  const tags: Array<{ key: string; value: string }> = [];
  const errors: string[] = [];
  text.split("\n").forEach((raw, index) => {
    const line = raw.trim();
    if (!line) return;
    const sep = line.indexOf(":");
    if (sep === -1) {
      errors.push(`Line ${index + 1}: use key: value`);
      return;
    }
    const key = line.slice(0, sep).trim();
    const value = line.slice(sep + 1).trim();
    if (!MANUAL_KEY.test(key)) errors.push(`Line ${index + 1}: key must be lower_snake_case`);
    else if (!value || value.length > 80) errors.push(`Line ${index + 1}: value must be 1–80 characters`);
    else tags.push({ key, value });
  });
  if (tags.length > 50) errors.push("At most 50 manual tags");
  return { tags, errors };
}

export function formatDeadline(hours: number): string {
  if (hours >= 24 * 7) return `${Math.round(hours / 24)} days`;
  return `${hours} ${hours === 1 ? "hour" : "hours"}`;
}

// ── compliance API shapes ────────────────────────────────────────────────────

export interface EngagementProfile {
  sector: string;
  jurisdictions: string[];
}

export interface ProfileResponse {
  profile: EngagementProfile;
  options: { sectors: string[]; jurisdictions: Record<string, string> };
}

export interface FrameworkSummary {
  id: string;
  name: string;
  authority: string;
  jurisdictions: string[];
  source: string;
  granularity: string;
  note: string | null;
  tag_triggered: boolean;
}

export interface ReportingClock {
  framework_id: string;
  framework: string;
  authority: string;
  deadline_hours: number;
  trigger: string;
  reference: string;
}

export interface ComplianceResponse {
  profile: EngagementProfile;
  frameworks: FrameworkSummary[];
  reporting: ReportingClock[];
  disclaimer: string;
}

export const SECTOR_LABEL: Record<string, string> = {
  generic: "General enterprise", banking: "Banking", payments_fintech: "Payments / fintech",
  nbfc: "NBFC / lending", insurance: "Insurance", capital_markets: "Capital markets",
  healthcare: "Healthcare", government: "Government",
};
