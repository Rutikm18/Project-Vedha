"use client";

import { INTENSITY, type Intensity } from "../../lib/scan-intensity";

const summaries: Record<Intensity, string> = {
  stealth: "Lower traffic · focused coverage",
  normal: "Balanced coverage · everyday assessments",
  aggressive: "Broader coverage · additional retries",
};

export function ScanIntensityControl({ value, onChange, disabled, allowed = INTENSITY.map(option => option.id), badges }: {
  value: Intensity; onChange: (value: Intensity) => void; disabled?: boolean;
  allowed?: readonly Intensity[]; badges?: Partial<Record<Intensity, string>>;
}) {
  const selected = INTENSITY.find(option => option.id === value)!;
  const angle = { stealth: -60, normal: 0, aggressive: 60 }[value];
  return <fieldset className="scanner-intensity" disabled={disabled}>
    <legend>Scan intensity</legend>
    <div className="scanner-intensity-dial" aria-hidden="true">
      <svg viewBox="0 0 200 112" focusable="false">
        <path d="M22 96 A78 78 0 0 1 178 96" fill="none" className="scanner-dial-track" strokeWidth="7" strokeLinecap="round" />
        {[[-60, "stealth"], [0, "normal"], [60, "aggressive"]].map(([rotation, name]) => <g key={name} transform={`rotate(${rotation} 100 96)`}>
          <line x1="100" y1="14" x2="100" y2="23" className={name === value ? "scanner-dial-selected" : "scanner-dial-track"} strokeWidth="2" />
        </g>)}
        <g transform={`rotate(${angle} 100 96)`} className="scanner-dial-needle">
          <line x1="100" y1="96" x2="100" y2="36" className="scanner-dial-selected" strokeWidth="2" strokeLinecap="round" />
        </g>
        <circle cx="100" cy="96" r="4" className="scanner-dial-hub" />
      </svg><strong>{selected.label}</strong>
    </div>
    <div className="scanner-mode-options">
      {INTENSITY.map(option => <label key={option.id} data-selected={value === option.id} data-disabled={!allowed.includes(option.id)}>
        <span className="scanner-mode-title"><input type="radio" name="scan-intensity" value={option.id}
          checked={value === option.id} disabled={!allowed.includes(option.id)} onChange={() => onChange(option.id)} />
          <strong>{option.label}</strong></span>
        <span className="scanner-mode-description">{summaries[option.id]}</span>
        {badges?.[option.id] && <small>{badges[option.id]}</small>}
      </label>)}
    </div>
    <p className="scanner-help">{selected.why}</p>
  </fieldset>;
}
