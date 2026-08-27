import { test, describe, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import os   from 'node:os';
import fs   from 'node:fs';
import path from 'node:path';

// Isolated temp dir per run — the store is one JSON file per campaign.
const TMP_DIR = path.join(os.tmpdir(), `vedha-campaign-test-${Date.now()}`);
process.env.CAMPAIGN_DATA_DIR = TMP_DIR;

import {
  saveCampaign, getCampaign, listCampaigns, validateSnapshot,
  isSafeCampaignId, setCampaignDir,
  type CampaignSnapshot,
} from '../lib/campaign-store';

// A minimal but contract-complete snapshot (the shape the probe emits).
function makeSnapshot(overrides: Partial<CampaignSnapshot> = {}): CampaignSnapshot {
  return {
    campaign_id: 'CAMP-1',
    targets: ['10.0.0.0/24'],
    status: 'running',
    started_at: '2026-08-27T10:00:00Z',
    updated_at: '2026-08-27T10:01:00Z',
    percent: 25,
    current_stage: 'port_map',
    eta_seconds: 120,
    stages: [
      { id: 'discovery', name: 'Host & Network Discovery', detail: 'Finding every live device.',
        status: 'done', started_at: '2026-08-27T10:00:00Z', ended_at: '2026-08-27T10:00:30Z', count: 4, note: '4 live' },
      { id: 'port_map', name: 'Port & Service Mapping', detail: 'Mapping open TCP ports.',
        status: 'running', started_at: '2026-08-27T10:00:30Z', ended_at: null, count: 0, note: '' },
    ],
    totals: { live_hosts: 4, open_ports: 0, facts: 4 },
    ...overrides,
  };
}

beforeEach(() => {
  fs.rmSync(TMP_DIR, { recursive: true, force: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });
  setCampaignDir(TMP_DIR);
});

describe('campaign-store', () => {
  test('save then get round-trips the snapshot', () => {
    saveCampaign(makeSnapshot());
    const got = getCampaign('CAMP-1');
    assert.ok(got);
    assert.equal(got!.campaign_id, 'CAMP-1');
    assert.equal(got!.percent, 25);
    assert.equal(got!.stages.length, 2);
    assert.equal(got!.stages[1].status, 'running');
    assert.equal(got!.totals.live_hosts, 4);
  });

  test('save overwrites by campaign_id (progress advances in place)', () => {
    saveCampaign(makeSnapshot({ percent: 25, status: 'running' }));
    saveCampaign(makeSnapshot({ percent: 100, status: 'completed', current_stage: null }));
    const got = getCampaign('CAMP-1');
    assert.equal(got!.percent, 100);
    assert.equal(got!.status, 'completed');
    // still one file, not two
    assert.equal(listCampaigns().length, 1);
  });

  test('getCampaign returns null for an unknown id', () => {
    assert.equal(getCampaign('nope'), null);
  });

  test('listCampaigns returns compact summaries, newest-updated first', () => {
    saveCampaign(makeSnapshot({ campaign_id: 'CAMP-old', updated_at: '2026-08-27T09:00:00Z' }));
    saveCampaign(makeSnapshot({ campaign_id: 'CAMP-new', updated_at: '2026-08-27T12:00:00Z' }));
    const list = listCampaigns();
    assert.equal(list.length, 2);
    assert.equal(list[0].campaign_id, 'CAMP-new');   // most recent first
    assert.equal(list[1].campaign_id, 'CAMP-old');
    // summary carries no per-stage detail, only the count
    assert.equal(list[0].stage_count, 2);
    assert.ok(!('stages' in list[0]));
  });

  test('validateSnapshot rejects a missing/invalid campaign_id', () => {
    assert.throws(() => validateSnapshot({ stages: [] }), /campaign_id/);
    assert.throws(() => validateSnapshot({ campaign_id: '../etc/passwd', stages: [] }), /campaign_id/);
    assert.throws(() => validateSnapshot(null), /object/);
  });

  test('validateSnapshot coerces status and unknown stage status safely', () => {
    const snap = validateSnapshot({
      campaign_id: 'CAMP-x',
      stages: [{ id: 'a', name: 'A', detail: '', status: 'bogus', count: 0, note: '' }],
      status: 'weird',
    });
    assert.equal(snap.status, 'running');          // anything not "completed" → running
    assert.equal(snap.stages[0].status, 'pending'); // unknown stage status → pending
    assert.deepEqual(snap.totals, {});
  });

  test('isSafeCampaignId blocks path traversal and bad charsets', () => {
    assert.ok(isSafeCampaignId('CAMP-2026_08.27'));
    assert.ok(!isSafeCampaignId('../../secret'));
    assert.ok(!isSafeCampaignId('a/b'));
    assert.ok(!isSafeCampaignId(''));
    assert.ok(!isSafeCampaignId(42));
  });

  test('a traversal id can never be persisted (save throws, no file escapes)', () => {
    assert.throws(() => saveCampaign(makeSnapshot({ campaign_id: '../escape' })), /campaign_id/);
    // nothing written outside the store dir
    assert.equal(listCampaigns().length, 0);
  });

  test('save writes no leftover .tmp file (atomic rename)', () => {
    saveCampaign(makeSnapshot());
    const leftovers = fs.readdirSync(TMP_DIR).filter((f) => f.endsWith('.tmp'));
    assert.equal(leftovers.length, 0);
  });
});
