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
  return <fieldset className="scanner-intensity" disabled={disabled}>
    <legend>Scan intensity</legend>
    <div className="scanner-mode-options">
      {INTENSITY.map(option => <label key={option.id} data-selected={value === option.id} data-disabled={!allowed.includes(option.id)}>
        <span className="scanner-mode-title"><input type="radio" name="scan-intensity" value={option.id}
          checked={value === option.id} disabled={!allowed.includes(option.id)} onChange={() => onChange(option.id)} />
          <strong>{option.label}</strong>{option.id === "normal" && <small>Default</small>}</span>
        <span>{summaries[option.id]}</span>
        {badges?.[option.id] && <small>{badges[option.id]}</small>}
      </label>)}
    </div>
    <p className="scanner-help">{INTENSITY.find(option => option.id === value)?.why}</p>
  </fieldset>;
}
