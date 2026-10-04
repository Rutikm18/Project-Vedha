// #29 Open Door Report, Stage 1: 8-page A4 PDF, 3 charts, a fix for every finding.
// Charts are drawn only from report_data.json; a chart with no data renders a labelled "data pending" frame.
// Chart rules (dataviz skill): single series, so one brand blue (validated), no legend (the title names it),
// direct value labels in ink, thin bars with rounded data ends, no grid noise.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { renderPrint } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const D = JSON.parse(fs.readFileSync(path.join(DIR, 'report_data.json'), 'utf8'));

function bars(c) {
  const W = 170, labelW = 58, barMax = W - labelW - 18, bh = 5.5, gap = 3.5;
  if (!c.rows || !c.rows.length) {
    return `<div class="pending"><b>Data pending</b><br>Source: ${c.source}<br><span>This chart is drawn only from that source. No numbers are estimated.</span></div>`;
  }
  const rows = [...c.rows].sort((a, b) => b.value - a.value), max = Math.max(...rows.map(r => r.value));
  const H = rows.length * (bh + gap) + 6;
  const g = rows.map((r, i) => { const y = 3 + i * (bh + gap), w = Math.max(0.6, (r.value / max) * barMax);
    return `<text x="${labelW - 3}" y="${y + bh * 0.72}" text-anchor="end" class="lb">${r.label}</text>
      <path d="M${labelW} ${y}h${w - 1}a1 1 0 0 1 1 1v${bh - 2}a1 1 0 0 1-1 1h-${w - 1}z" fill="#1D4ED8"><title>${r.label}: ${r.value.toLocaleString('en-IN')}</title></path>
      <text x="${labelW + w + 2}" y="${y + bh * 0.72}" class="v">${r.value.toLocaleString('en-IN')}</text>`; }).join('');
  return `<svg width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" role="img" aria-label="${c.title}"><line x1="${labelW}" y1="0" x2="${labelW}" y2="${H}" stroke="#8EA0B5" stroke-width="0.25"/>${g}</svg>`;
}
const chartPage = (n, c, note) => `<section><div class="k">CHART ${n}</div><h2>${c.title}</h2><p class="unit">Unit: ${c.unit}</p>${bars(c)}<p class="src">Source: ${c.source}</p><p>${note}</p><div class="foot"><span>THE OPEN DOOR REPORT · STAGE 1</span><span>${n + 2}</span></div></section>`;

const DOORS = [
  ['Remote desktop reachable from outside', 'Anyone who finds it can try to log in, all day, from anywhere.', 'Turn it off where nobody needs it. Where someone does, put it behind a VPN with MFA, and re-check.'],
  ['File shares anyone on the network can open', 'Client files, payroll sheets and quotations, readable by any device on the Wi-Fi.', 'Give each share only to the people who need it. Remove "Everyone".'],
  ['Databases that answer without a password', 'Billing and customer records readable by any device that asks.', 'Set authentication and let only the application server connect.'],
  ['Admin pages for routers, printers and cameras', 'Settings pages left open from the inside, and sometimes from the internet.', 'Restrict admin pages to the IT person; switch off admin from the internet.'],
  ['Cameras and DVRs exposed to the internet', '"Remote viewing" set up by forwarding a port on the router.', 'Remove the port forwarding; view through the vendor app or a VPN.'],
  ['Devices nobody can name', 'Old test servers, personal devices, forgotten boxes: unknown means unowned.', 'Keep an inventory of every device; remove what doesn’t belong.'],
];
const doorRows = (list, from) => list.map((d, i) => `<div class="door"><div class="n">${String(from + i).padStart(2, '0')}</div><div><h3>${d[0]}</h3><p>${d[1]}</p><p class="fix"><b>Fix:</b> ${d[2]}</p></div></div>`).join('');
let dots = ''; for (let y = 8; y < 297; y += 6) for (let x = 8; x < 210; x += 6) { const gap = x > 80 && x < 100 && y > 200 && y < 226; if (!gap) dots += `<circle cx="${x}" cy="${y}" r="0.5" fill="rgba(243,246,250,.18)"/>`; }

const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
@page{size:210mm 297mm;margin:0}html,body{width:210mm}
body{font-family:var(--sans);color:#0F172A;font-size:10.5pt;line-height:1.5}
section{width:210mm;height:297mm;box-sizing:border-box;padding:24mm 22mm;position:relative;page-break-after:always;overflow:hidden}
section:last-child{page-break-after:auto}
.cover{background:#060B14;color:#F3F6FA;padding:0}
.k{font:500 8.5pt var(--mono);letter-spacing:.12em;color:#1D4ED8}
h1{font:400 44pt/1.02 var(--serif);margin:0}h2{font:400 24pt/1.1 var(--serif);margin:3mm 0 2mm}h3{font:500 12pt var(--sans);margin:0 0 1mm}
.unit,.src{font-size:8.6pt;color:#475569}.src{margin-top:4mm}
.lb{font:400 3.3px var(--sans);fill:#0F172A}.v{font:500 3.1px var(--mono);fill:#0F172A}
.pending{border:0.4mm dashed #8EA0B5;border-radius:3mm;padding:14mm 10mm;color:#475569;margin-top:6mm;line-height:1.6}.pending b{color:#0F172A;font-size:12pt}.pending span{font-size:8.6pt}
.door{display:flex;gap:6mm;padding:5mm 0;border-bottom:0.3mm solid #DCE3EC}.door .n{font:400 22pt var(--serif);color:#1D4ED8;width:12mm}
.fix{background:#F3F6FA;border-radius:2mm;padding:2mm 3mm}
.foot{position:absolute;left:22mm;right:22mm;bottom:12mm;display:flex;justify-content:space-between;font:500 7.5pt var(--mono);color:#64748B}
</style></head><body>
<section class="cover"><svg style="position:absolute;inset:0" width="210mm" height="297mm" viewBox="0 0 210 297">${dots}<line x1="80" y1="226" x2="100" y2="226" stroke="#60A5FA" stroke-width="0.6" stroke-linecap="round"/></svg>
<div style="position:absolute;left:22mm;top:24mm;display:flex;gap:3mm;align-items:center;font:400 20pt var(--serif)">${sealSvg('#60A5FA', 44)}Vedha</div>
<div style="position:absolute;left:22mm;right:22mm;top:80mm"><div class="k" style="color:#60A5FA">THE OPEN DOOR REPORT</div><h1 style="margin-top:4mm">Every office has one door nobody remembers.</h1><p style="font-size:13pt;color:#C5D0DE;margin-top:6mm">What's open on India's office networks, and how to close it.</p></div>
<div style="position:absolute;left:22mm;bottom:22mm;font:500 9pt var(--mono);color:#C5D0DE">${D.edition} · vedhasec.com</div></section>

<section><div class="k">SUMMARY</div><h2>What this report shows</h2>
<p>Stage 1 looks at the "doors" on office networks from three angles: what's visible from the internet nationally, what Vedha checks found inside real offices, and what owners know about CERT-In's new MSME controls.</p>
<p><b>Key numbers</b> are added only when the data in Charts 1–3 is in. Each one will be quoted with its source and its n, and nothing will be rounded to change the story.</p>
<p>Every finding in this report comes with a fix (pages 6–7). This isn't a report about fear: most doors take an afternoon to close.</p>
<div class="foot"><span>THE OPEN DOOR REPORT · STAGE 1</span><span>2</span></div></section>

${chartPage(1, D.charts.exposed, 'What anyone on the internet can see. These counts are services, not organisations; one office can have several.')}
${chartPage(2, D.charts.found, 'What Vedha checks found inside offices. Aggregated across checks; no organisation, person or device can be identified.')}
${chartPage(3, D.charts.poll, 'Answers from an anonymous poll run through IT partners. Not a random sample; read it as a signal, not a census.')}

<section><div class="k">FINDINGS AND FIXES (1/2)</div><h2>The doors, and how to close them</h2>${doorRows(DOORS.slice(0, 3), 1)}<div class="foot"><span>THE OPEN DOOR REPORT · STAGE 1</span><span>6</span></div></section>
<section><div class="k">FINDINGS AND FIXES (2/2)</div><h2>The doors, and how to close them</h2>${doorRows(DOORS.slice(3), 4)}<div class="foot"><span>THE OPEN DOOR REPORT · STAGE 1</span><span>7</span></div></section>

<section><div class="k">METHOD, SOURCES AND LIMITS</div><h2>How this report was made</h2>
<ul><li><b>Chart 1:</b> ${D.charts.exposed.source}.</li><li><b>Chart 2:</b> ${D.charts.found.source}.</li><li><b>Chart 3:</b> ${D.charts.poll.source}.</li></ul>
<p><b>Limits.</b> Vedha checks cover office networks only, not cloud, and are run by IT partners with the owner's permission. Poll respondents chose to answer. This report doesn't claim any organisation is or isn't secure.</p>
<p><b>About Vedha.</b> Vedha runs 7-day network health checks for growing businesses through IT partners they already trust: find what's open, prove what's real, show the fix worked. vedhasec.com · info@vedhasec.com</p>
<div class="foot"><span>THE OPEN DOOR REPORT · STAGE 1</span><span>8</span></div></section>
</body></html>`;
fs.writeFileSync(path.join(DIR, 'report.html'), html);
await renderPrint(path.join(DIR, 'report.html'), 210, 297, { pdf: path.join(DIR, 'open-door-report-stage1.pdf') });
fs.rmSync(path.join(DIR, 'report.html'));
console.log('built');
