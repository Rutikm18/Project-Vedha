"use client";

import React, { useState } from "react";
import { Check, Loader2, Pencil, X } from "lucide-react";
import {
  assetTags,
  parseManualTags,
  tagLabel,
  tagString,
  tagTitle,
  tagTone,
  type TagCount,
  type TagRecord,
  type TaggedAsset,
} from "../../lib/intel";

export function TagChip({
  tag, active, onClick,
}: { tag: TagRecord; active?: boolean; onClick?: () => void }) {
  const tone = tagTone(tag);
  const content = <>{tagLabel(tag)}</>;
  if (onClick) {
    return (
      <button
        type="button"
        className="intel-tag"
        data-tone={tone}
        data-active={active || undefined}
        aria-pressed={Boolean(active)}
        title={tagTitle(tag)}
        onClick={onClick}
      >
        {content}
      </button>
    );
  }
  return <span className="intel-tag" data-tone={tone} title={tagTitle(tag)}>{content}</span>;
}

/** Chips for one asset. Segment (zone) is shown in the meta line, so it is skipped here. */
export function AssetTagList({
  asset, selected, onToggle,
}: { asset: TaggedAsset; selected: string[]; onToggle: (tag: string) => void }) {
  const tags = assetTags(asset).filter((tag) => tag.key !== "zone");
  if (!tags.length) return <span className="engagement-empty-inline">No tags yet — evidence is still thin for this host</span>;
  return (
    <div className="intel-tag-list" aria-label="Asset tags">
      {tags.map((tag) => {
        const id = tagString(tag);
        return <TagChip key={id} tag={tag} active={selected.includes(id)} onClick={() => onToggle(id)} />;
      })}
    </div>
  );
}

export function TagFilterBar({
  counts, selected, onToggle, onClear, total, shown,
}: {
  counts: TagCount[];
  selected: string[];
  onToggle: (tag: string) => void;
  onClear: () => void;
  total: number;
  shown: number;
}) {
  const [expanded, setExpanded] = useState(false);
  if (!counts.length) return null;
  const visible = expanded ? counts : counts.slice(0, 14);
  return (
    <section className="intel-filter" aria-label="Filter hosts by tag">
      <div className="intel-filter-head">
        <span>{selected.length ? `${shown} of ${total} hosts match all selected tags` : `Filter ${total} hosts by tag`}</span>
        {selected.length > 0 && <button type="button" className="intel-link" onClick={onClear}><X size={12} /> Clear</button>}
      </div>
      <div className="intel-tag-list">
        {visible.map(({ tag, record, count }) => (
          <button
            key={tag}
            type="button"
            className="intel-tag"
            data-tone={tagTone(record)}
            data-active={selected.includes(tag) || undefined}
            aria-pressed={selected.includes(tag)}
            title={tagTitle(record)}
            onClick={() => onToggle(tag)}
          >
            {tagLabel(record)} <span className="intel-tag-count">{count}</span>
          </button>
        ))}
        {counts.length > 14 && (
          <button type="button" className="intel-link" onClick={() => setExpanded((v) => !v)}>
            {expanded ? "Show fewer" : `+${counts.length - 14} more`}
          </button>
        )}
      </div>
    </section>
  );
}

/** Inline editor for operator-assigned tags ("key: value" per line). */
export function ManualTagEditor({
  asset, onSave,
}: {
  asset: TaggedAsset;
  onSave: (tags: Array<{ key: string; value: string }>) => Promise<unknown>;
}) {
  const current = (asset.tags?.manual ?? []).map((tag) => `${tag.key}: ${tag.value}`).join("\n");
  const [open, setOpen] = useState(false);
  const [text, setText] = useState(current);
  const [saving, setSaving] = useState(false);
  const [failure, setFailure] = useState<string | null>(null);
  const parsed = parseManualTags(text);

  if (!open) {
    return (
      <button type="button" className="intel-link" onClick={() => { setText(current); setOpen(true); }}>
        <Pencil size={12} /> {current ? "Edit business tags" : "Add business tags"}
      </button>
    );
  }

  async function save() {
    setSaving(true);
    setFailure(null);
    try {
      await onSave(parsed.tags);
      setOpen(false);
    } catch (error) {
      setFailure(error instanceof Error ? error.message : "Could not save tags");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="intel-editor">
      <label>
        <span>Business context the scanner cannot see — one <code>key: value</code> per line</span>
        <textarea
          rows={3}
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder={"owner_team: Cards operations\nbusiness_service: UPI switch"}
        />
      </label>
      {(parsed.errors.length > 0 || failure) && (
        <div className="engagement-form-error">{failure ?? parsed.errors.join(" · ")}</div>
      )}
      <div className="intel-editor-actions">
        <button type="button" className="btn btn-secondary" onClick={() => setOpen(false)}>Cancel</button>
        <button type="button" className="btn btn-primary" disabled={saving || parsed.errors.length > 0} onClick={save}>
          {saving ? <Loader2 size={13} className="animate-spin" /> : <Check size={13} />} Save tags
        </button>
      </div>
    </div>
  );
}
