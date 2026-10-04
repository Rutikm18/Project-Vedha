// Brand tokens, extracted from the product repo (see ../RECON.md).
// Sources: manager/frontend/app/globals.css, docs/design/design-system.md,
// manager/frontend/public/brand/vedha-mark.svg.
export const C = {
  blue: '#1D4ED8',        // --accent (light): route and action
  blueOnNight: '#60A5FA', // --accent (dark): the mark's own dark-scheme fill
  teal: '#0F766E',        // --nominal-color: verified only
  tealOnNight: '#5EEAD4', // --nominal-color (dark)
  night: '#060B14',
  day: '#F3F6FA',
  panel: '#FFFFFF',       // --bg-panel (light)
  border: '#DCE3EC',      // --border-subtle (light)
  textPrimary: '#0F172A', // --text-primary (light)
  textSecondary: '#475569',
  textMuted: '#607086',
};

export const FONT = {
  display: '"Instrument Serif", serif',
  ui: '"Geist Sans", sans-serif',
  mono: '"Geist Mono", monospace',
  deva: '"Tiro Devanagari Hindi", serif',
};

// The seal, verbatim from manager/frontend/public/brand/vedha-mark.svg (viewBox 0 0 100 100).
// Outer body with the V-notch, then the eye (an even-odd cut-out), then the pupil.
export const SEAL = {
  body: 'M28 6H39L50 24L61 6H72A22 22 0 0 1 94 28V72A22 22 0 0 1 72 94H28A22 22 0 0 1 6 72V28A22 22 0 0 1 28 6Z',
  eye: 'M18 53Q50 21 82 53Q50 85 18 53Z',
  pupil: { cx: 50, cy: 53, r: 11 },
};
