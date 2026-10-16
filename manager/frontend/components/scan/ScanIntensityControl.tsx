"use client";

import { INTENSITY, type Intensity } from "../../lib/scan-intensity";

const arcs = [
  { id: 'stealth', d: 'M22,96 A78,78 0 0 1 61,29.4' },
  { id: 'normal', d: 'M61,29.4 A78,78 0 0 1 139,29.4' },
  { id: 'aggressive', d: 'M139,29.4 A78,78 0 0 1 178,96' },
];

export function ScanIntensityControl({ value, onChange, disabled, allowed = INTENSITY.map(option => option.id), badges }: {
  value: Intensity; onChange: (value: Intensity) => void; disabled?: boolean;
  allowed?: readonly Intensity[]; badges?: Partial<Record<Intensity, string>>;
}) {
  const selected = INTENSITY.find(option => option.id === value)!;
  const angle = { stealth: -60, normal: 0, aggressive: 60 }[value];
  return <fieldset className="scanner-intensity" data-mode={value} disabled={disabled}>
    <legend>Scan intensity</legend>
    <div className="scanner-intensity-dial" aria-hidden="true">
      <svg viewBox="0 0 200 110" focusable="false">
        {arcs.map(arc => <path key={arc.id} d={arc.d} fill="none" stroke={`var(--scan-${arc.id})`} strokeWidth="9" strokeLinecap="round" opacity={arc.id === value ? .8 : .26} />)}
        <g style={{ transform: `rotate(${angle}deg)` }} className="scanner-dial-needle">
          <line x1="100" y1="96" x2="100" y2="26" stroke="var(--scan-selected)" strokeWidth="2.5" strokeLinecap="round" />
        </g>
        <circle cx="100" cy="96" r="5.5" fill="var(--bg-panel)" stroke="var(--scan-selected)" strokeWidth="2" />
      </svg>
      <div className="scanner-dial-readout"><strong>{selected.rate} pps</strong><span>{selected.label} · preset rate</span></div>
    </div>
    <div className="scanner-mode-options">
      {INTENSITY.map(option => <label key={option.id} data-mode={option.id} data-selected={value === option.id} data-disabled={!allowed.includes(option.id)}>
        <input type="radio" name="scan-intensity" value={option.id} checked={value === option.id}
          disabled={!allowed.includes(option.id)} onChange={() => onChange(option.id)} />
        <span className="scanner-mode-title"><i aria-hidden="true" /><strong>{option.label}</strong></span>
        {badges?.[option.id] && <small>{badges[option.id]}</small>}
      </label>)}
    </div>
    <p className="scanner-help">{selected.why}</p>
  </fieldset>;
}
