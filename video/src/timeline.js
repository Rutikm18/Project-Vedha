// Every beat of the film, in frames at 30 fps. One file so timing, captions
// and the SRT all read from the same numbers.
export const FPS = 30;
export const DURATION = 900;

export const SCENES = [
  { id: 'hook',    name: '1 Hook',     from: 0,   to: 90 },
  { id: 'path',    name: '2 The path', from: 90,  to: 270 },
  { id: 'pierce',  name: '3 Pierce',   from: 270, to: 420 },
  { id: 'partner', name: '4 Partner',  from: 420, to: 510 },
  { id: 'console', name: '5 Console',  from: 510, to: 750 },
  { id: 'report',  name: '6 Report',   from: 750, to: 825 },
  { id: 'cta',     name: '7 CTA',      from: 825, to: 900 },
];

export const T = {
  // 1 Hook
  bloomFrom: 0, bloomDur: 30,
  pulseAt: 40, pulseDur: 12,
  gapOpenAt: 66, gapOpenDur: 18,
  hookTextAt: 9, hookWordStagger: 3,
  // 2 Path
  contoursAt: 90,
  devicesAt: 96,
  printerAt: 90, cameraAt: 120, keyAt: 150,
  routeAt: 210, routeDur: 48,
  // 3 Pierce
  sealAt: 270, sealScaleDur: 12,
  strikeAt: 282, strikeDur: 8,
  displaceAt: 282, displaceDur: 18,
  eyeAt: 290, eyeDur: 16,
  pupilAt: 306, pupilLockAt: 336, blinkAt: 352, blinkDur: 6,
  nameAt: 276, devaAt: 282, glossAt: 288, whatAt: 330,
  // 4 Partner
  partnerAt: 420, partnerLineAt: 432, partnerLineDur: 24,
  // 5 Console
  consoleAt: 510, findingsAt: 510, attackAt: 570, fixAt: 630,
  tickAt: 632, holdAt: 640, holdDur: 18, snapAt: 658,
  healAt: 658, healDur: 18, tealAt: 660, gradeAt: 664,
  washAt: 670, washDur: 20,
  // 6 Report
  reportAt: 750, doorsAt: 760, doorStagger: 6, verifiedAt: 784,
  // 7 CTA
  ctaAt: 825, ctaStagger: 4, stillFrom: 885,
};

// Captions: what the viewer must read, when. Also the SRT source (Appendix B).
// `key` points into copy.*.json.
export const CAPTIONS = [
  { from: 9,   to: 90,  key: 'hook' },
  { from: 90,  to: 210, key: 'list' },
  { from: 210, to: 270, key: 'path' },
  { from: 276, to: 420, key: 'name' },
  { from: 420, to: 510, key: 'partner' },
  { from: 510, to: 570, key: 'find' },
  { from: 570, to: 630, key: 'prove' },
  { from: 630, to: 750, key: 'fix' },
  { from: 750, to: 825, key: 'report' },
  { from: 825, to: 900, key: 'cta' },
];
