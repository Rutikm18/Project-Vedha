// Layouts per aspect ratio, in that format's own pixel space.
// Only 4:5 exists for the animatic; 9:16, 1:1 and 16:9 are recomposed in Phase 3.
export const LAYOUTS = {
  '4x5': {
    W: 1080, H: 1350, safe: 80,
    hookX: 88, hookY: 470, hookLH: 110, hookPx: 104, hookMaxW: 904,
    capX: 88, capBase: 1150, capLH: 72, capPx: 60, capMaxW: 904, listBase: 1020,
    tagBase: 1215,
    sealX: 540, sealY: 560, sealSize: 360,
    namePx: 128, nameBase: 880, devaPx: 96, devaBase: 990, glossPx: 30,
    partnerSealX: 330, partnerSealY: 470, partnerSealSize: 240, partnerNode: [800, 820],
    console: { x: 80, y: 180, w: 920, h: 830 },
    ctaSealX: 540, ctaSealY: 420, ctaSealSize: 240,
    ctaNamePx: 104, ctaNameBase: 730,
    ctaBtn: { x: 180, y: 820, w: 720, h: 120 }, ctaBtnPx: 48,
    ctaUrlPx: 52, ctaUrlBase: 1030, ctaScopePx: 38, ctaScopeBase: 1120,
  },
};
