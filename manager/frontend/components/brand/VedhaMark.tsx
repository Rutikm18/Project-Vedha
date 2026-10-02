/* Vedha brand mark — the rounded square with the notch and the eye.
   Same geometry as app/icon.svg and public/brand/vedha-mark.svg; drawn in
   currentColor so it follows the theme (accent on light and dark). */

export function VedhaMark({ size = 16, title }: { size?: number; title?: string }) {
  return (
    <svg
      width={size} height={size} viewBox="0 0 100 100" fill="currentColor"
      role={title ? "img" : undefined} aria-label={title} aria-hidden={title ? undefined : true}
      focusable="false"
    >
      <path
        fillRule="evenodd"
        d="M28 6H39L50 24L61 6H72A22 22 0 0 1 94 28V72A22 22 0 0 1 72 94H28A22 22 0 0 1 6 72V28A22 22 0 0 1 28 6ZM18 53Q50 21 82 53Q50 85 18 53Z"
      />
      <circle cx="50" cy="53" r="11" />
    </svg>
  );
}

/* Stacked lockup — the mark above the "vedha" wordmark. Same geometry as
   public/brand/vedha-logo-stacked.svg, in currentColor. Width is 4:3 of height. */
export function VedhaLogoStacked({ height = 72, title = "Vedha" }: { height?: number; title?: string }) {
  return (
    <svg width={(height * 4) / 3} height={height} viewBox="0 0 240 180" fill="currentColor" role="img" aria-label={title} focusable="false">
      <g transform="translate(70,0)">
        <path fillRule="evenodd" d="M30 10H42L50 24L58 10H70A20 20 0 0 1 90 30V70A20 20 0 0 1 70 90H30A20 20 0 0 1 10 70V30A20 20 0 0 1 30 10ZM24 52Q50 26 76 52Q50 78 24 52Z" />
        <circle cx="50" cy="52" r="8.5" />
      </g>
      <g transform="translate(18.5,130)">
        <polygon points="0,0 7.5,0 17,26 26.5,0 34,0 21,36 13,36" />
        <g fill="none" stroke="currentColor" strokeWidth={6}>
          <path d="M44 18H74A15 15 0 1 0 70.5 27.6" />
          <circle cx="101" cy="18" r="15" />
          <path d="M116 -22V36M128 -22V36" />
          <path d="M128 20A15 15 0 0 1 158 20V36" />
          <circle cx="185" cy="18" r="15" />
          <path d="M200 0V36" />
        </g>
      </g>
    </svg>
  );
}
