// Every beat of the film, in frames at 30 fps. One file so timing, captions,
// the music cues and the SRT all read from the same numbers.
export const FPS = 30;
export const DURATION = 900;

export const SCENES = [
  { id: 'hook',    name: '1 Hook',        from: 0,   to: 90 },
  { id: 'path',    name: '2 The path',    from: 90,  to: 270 },
  { id: 'pierce',  name: '3 Pierce',      from: 270, to: 375 },
  { id: 'checks',  name: '3b Checkpoints', from: 375, to: 480 },
  { id: 'partner', name: '4 Partner',     from: 480, to: 540 },
  { id: 'console', name: '5 Console',     from: 540, to: 750 },
  { id: 'report',  name: '6 Report',      from: 750, to: 825 },
  { id: 'cta',     name: '7 CTA',         from: 825, to: 900 },
];

export const T = {
  // 1 Hook
  bloomFrom: 0, bloomDur: 30,
  pulseAt: 40, pulseDur: 12,
  gapOpenAt: 66, gapOpenDur: 18,
  hookTextAt: 9, hookWordStagger: 3,
  // 2 Path: each line lights its asset
  contoursAt: 90, devicesAt: 96,
  item1At: 90, item2At: 120, item3At: 150,
  routeAt: 210, routeDur: 48,
  // 3 Pierce
  sealAt: 270, sealScaleDur: 12,
  strikeAt: 282, strikeDur: 8,
  displaceAt: 282, displaceDur: 18,
  eyeAt: 290, eyeDur: 16,
  pupilAt: 306, pupilLockAt: 336, blinkAt: 352, blinkDur: 6,
  nameAt: 276, devaAt: 282, glossAt: 288, whatAt: 318,
  // 3b Checkpoints
  checksAt: 375, checkItemsAt: 384, checkStagger: 6,
  // 4 Partner
  partnerAt: 480, partnerLineAt: 490, partnerLineDur: 24,
  // 5 Console
  consoleAt: 540, findingsAt: 540, attackAt: 595, fixAt: 645,
  tickAt: 647, holdAt: 655, holdDur: 18, snapAt: 673,
  healAt: 673, healDur: 18, tealAt: 675, gradeAt: 679,
  washAt: 685, washDur: 20,
  // 6 Report
  reportAt: 750, doorsAt: 760, doorStagger: 6, verifiedAt: 784,
  // 7 CTA
  ctaAt: 825, ctaStagger: 4, stillFrom: 885,
};

// Captions: what the viewer must read, when (also the SRT source). `key` points into copy.*.json.
export const CAPTIONS = [
  { from: 9,   to: 90,  key: 'hook' },
  { from: 90,  to: 210, key: 'list' },
  { from: 210, to: 270, key: 'path' },
  { from: 276, to: 375, key: 'name', also: 'what' },
  { from: 378, to: 480, key: 'checks' },
  { from: 484, to: 540, key: 'partner' },
  { from: 544, to: 595, key: 'find' },
  { from: 595, to: 645, key: 'prove' },
  { from: 645, to: 750, key: 'fix' },
  { from: 750, to: 825, key: 'report' },
  { from: 825, to: 900, key: 'cta' },
];
