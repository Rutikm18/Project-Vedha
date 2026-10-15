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
  const arc = angle + 90;
  return <fieldset className="scanner-intensity" disabled={disabled}>
    <legend>Scan intensity</legend>
    <div className="scanner-intensity-dial" aria-hidden="true">
      <svg viewBox="0 0 200 116" focusable="false">
        <path d="M22 96 A78 78 0 0 1 178 96" fill="none" className="scanner-dial-track" strokeWidth="7" strokeLinecap="round" />
        <path d="M22 96 A78 78 0 0 1 178 96" pathLength="180" fill="none" className="scanner-dial-arc" strokeWidth="7" strokeLinecap="round" strokeDasharray={`${arc} 180`} />
        {Array.from({ length: 19 }, (_, index) => <line key={index} x1="100" y1="29" x2="100" y2={index % 3 === 0 ? "36" : "33"}
          transform={`rotate(${index * 10 - 90} 100 96)`} className="scanner-dial-tick" strokeWidth="1" />)}
        {[[-60, "stealth"], [0, "normal"], [60, "aggressive"]].map(([rotation, name]) => <g key={name} transform={`rotate(${rotation} 100 96)`}>
          <line x1="100" y1="14" x2="100" y2="23" className={name === value ? "scanner-dial-selected" : "scanner-dial-track"} strokeWidth="2" />
        </g>)}
        <g style={{ transform: `rotate(${angle}deg)` }} className="scanner-dial-needle">
          <line x1="100" y1="96" x2="100" y2="43" className="scanner-dial-selected" strokeWidth="2.5" strokeLinecap="round" />
          <circle cx="100" cy="43" r="3" className="scanner-dial-hub" />
        </g>
        <circle cx="100" cy="96" r="7" className="scanner-dial-hub-ring" />
        <circle cx="100" cy="96" r="3" className="scanner-dial-hub" />
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
