import fs   from 'fs';
import path from 'path';

/**
 * campaign-store — persistence for Network-VA campaign progress snapshots.
 *
 * A "campaign" is one sequential background VA job run by the probe's
 * `scanner/va_campaign.py`. Its ProgressReporter emits a JSON snapshot after
 * every stage transition (the contract mirrored by the types below) and writes
 * it to `campaign_progress.json`. This store is the manager-side landing zone
 * for that exact document: one file per campaign under `data/campaigns/<id>.json`.
 *
 * Producer → store bridge:
 *   • dev / self-contained — a producer POSTs the snapshot to
 *     `/api/scan/campaigns` (see that route), or drops the file in the dir.
 *   • production (follow-up) — the probe reports progress on its existing job
 *     heartbeat; the FastAPI backend persists the latest snapshot on the job and
 *     the BFF proxies it here. Same shape either way, so the page is unchanged.
 *
 * File-backed to match the app's other dev stores (job-store, findings-store).
 */

// ── the snapshot contract (byte-for-byte the probe's ProgressReporter.snapshot) ─
export type StageStatus = 'pending' | 'running' | 'done' | 'skipped' | 'error';
export type CampaignStatus = 'running' | 'completed';

export interface StageSnapshot {
  id: string;
  name: string;
  detail: string;
  status: StageStatus;
  started_at: string | null;
  ended_at: string | null;
  count: number;
  note: string;
}

export interface CampaignTotals {
  live_hosts?: number;
  open_ports?: number;
  facts?: number;
}

export interface CampaignSnapshot {
  campaign_id: string;
  targets: string[];
  status: CampaignStatus;
  started_at: string;
  updated_at: string;
  percent: number;
  current_stage: string | null;
  eta_seconds: number | null;
  stages: StageSnapshot[];
  totals: CampaignTotals;
}

/** A compact row for the campaign list view (no per-stage detail). */
export interface CampaignSummary {
  campaign_id: string;
  targets: string[];
  status: CampaignStatus;
  percent: number;
  current_stage: string | null;
  started_at: string;
  updated_at: string;
  stage_count: number;
}

// This is a runtime data directory, not a build input. Without the annotation,
// Turbopack's file tracer conservatively includes the whole project in the
// standalone server artifact and emits an NFT warning during every CI build.
const DEFAULT_DIR = path.join(/*turbopackIgnore: true*/ process.cwd(), 'data', 'campaigns');
export let CAMPAIGN_DIR = process.env.CAMPAIGN_DATA_DIR ?? DEFAULT_DIR;

// Exposed for tests: override the campaigns directory.
export function setCampaignDir(dir: string): void { CAMPAIGN_DIR = dir; }

function ensureDir(): void {
  if (!fs.existsSync(/*turbopackIgnore: true*/ CAMPAIGN_DIR)) {
    fs.mkdirSync(/*turbopackIgnore: true*/ CAMPAIGN_DIR, { recursive: true });
  }
}

// A campaign_id is used verbatim as a filename — keep it to a safe charset so it
// can never traverse out of the store dir (`../`, absolute paths, etc.).
const SAFE_ID = /^[A-Za-z0-9._-]+$/;
export function isSafeCampaignId(id: unknown): id is string {
  return typeof id === 'string' && id.length > 0 && id.length <= 128 && SAFE_ID.test(id);
}

function fileFor(id: string): string {
  return path.join(/*turbopackIgnore: true*/ CAMPAIGN_DIR, `${id}.json`);
}

/**
 * Validate an untrusted object as a CampaignSnapshot. Returns the normalized
 * snapshot or throws with a human message — the ingest route surfaces that as 400.
 * We only pin the fields the UI depends on; unknown extras are preserved.
 */
export function validateSnapshot(raw: unknown): CampaignSnapshot {
  if (!raw || typeof raw !== 'object') throw new Error('snapshot must be an object');
  const s = raw as Record<string, unknown>;
  if (!isSafeCampaignId(s.campaign_id)) {
    throw new Error('campaign_id is required and must match [A-Za-z0-9._-]');
  }
  if (!Array.isArray(s.stages)) throw new Error('stages must be an array');
  const status = s.status === 'completed' ? 'completed' : 'running';
  return {
    campaign_id: s.campaign_id,
    targets: Array.isArray(s.targets) ? (s.targets as string[]) : [],
    status,
    started_at: typeof s.started_at === 'string' ? s.started_at : '',
    updated_at: typeof s.updated_at === 'string' ? s.updated_at : '',
    percent: typeof s.percent === 'number' ? s.percent : 0,
    current_stage: typeof s.current_stage === 'string' ? s.current_stage : null,
    eta_seconds: typeof s.eta_seconds === 'number' ? s.eta_seconds : null,
    stages: (s.stages as unknown[]).map(normalizeStage),
    totals: (s.totals && typeof s.totals === 'object' ? s.totals : {}) as CampaignTotals,
  };
}

function normalizeStage(raw: unknown): StageSnapshot {
  const st = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>;
  const status = ['pending', 'running', 'done', 'skipped', 'error'].includes(st.status as string)
    ? (st.status as StageStatus)
    : 'pending';
  return {
    id:         typeof st.id === 'string' ? st.id : '',
    name:       typeof st.name === 'string' ? st.name : '',
    detail:     typeof st.detail === 'string' ? st.detail : '',
    status,
    started_at: typeof st.started_at === 'string' ? st.started_at : null,
    ended_at:   typeof st.ended_at === 'string' ? st.ended_at : null,
    count:      typeof st.count === 'number' ? st.count : 0,
    note:       typeof st.note === 'string' ? st.note : '',
  };
}

/** Persist (create or overwrite) a campaign snapshot. Returns the stored doc. */
export function saveCampaign(raw: unknown): CampaignSnapshot {
  const snap = validateSnapshot(raw);
  ensureDir();
  // Atomic write: tmp + rename, so a concurrent read never sees a half file
  // (the same guarantee the probe's ProgressReporter makes on its side).
  const dest = fileFor(snap.campaign_id);
  const tmp = `${dest}.tmp`;
  fs.writeFileSync(/*turbopackIgnore: true*/ tmp, JSON.stringify(snap, null, 2));
  fs.renameSync(/*turbopackIgnore: true*/ tmp, /*turbopackIgnore: true*/ dest);
  return snap;
}

/** Full snapshot for one campaign, or null if unknown. */
export function getCampaign(id: string): CampaignSnapshot | null {
  if (!isSafeCampaignId(id)) return null;
  const file = fileFor(id);
  if (!fs.existsSync(/*turbopackIgnore: true*/ file)) return null;
  try {
    return validateSnapshot(JSON.parse(fs.readFileSync(/*turbopackIgnore: true*/ file, 'utf-8')));
  } catch {
    return null;
  }
}

/** All campaigns as compact summaries, most-recently-updated first. */
export function listCampaigns(): CampaignSummary[] {
  ensureDir();
  const out: CampaignSummary[] = [];
  for (const name of fs.readdirSync(/*turbopackIgnore: true*/ CAMPAIGN_DIR)) {
    if (!name.endsWith('.json') || name.endsWith('.tmp')) continue;
    const snap = getCampaign(name.slice(0, -'.json'.length));
    if (!snap) continue;
    out.push({
      campaign_id: snap.campaign_id,
      targets: snap.targets,
      status: snap.status,
      percent: snap.percent,
      current_stage: snap.current_stage,
      started_at: snap.started_at,
      updated_at: snap.updated_at,
      stage_count: snap.stages.length,
    });
  }
  out.sort((a, b) => (b.updated_at || b.started_at).localeCompare(a.updated_at || a.started_at));
  return out;
}
