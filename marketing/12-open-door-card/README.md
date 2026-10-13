# #12 Open Door share card

| File | What |
|---|---|
| `index.html` | The share page: mobile-first, no trackers, no external requests |
| `og-image.png` | 1200×630 preview that WhatsApp, LinkedIn and X show when the link is shared |
| `preview-mobile.png` | What it looks like on a phone (390 px wide) |
| `build.mjs` | Rebuilds both (`node 12-open-door-card/build.mjs`) |

**Buttons**
- **Share:** uses the phone's own share sheet (WhatsApp, LinkedIn and so on). On desktop it falls back to WhatsApp Web.
- **Send to my IT person:** opens WhatsApp with a ready message: "Hi, can we get our office network checked? Vedha does a 7-day network health check through IT partners: [link]". Email, LinkedIn and copy-link are underneath.
- Every link carries UTM tags (`utm_campaign=open_door`, plus `utm_medium=it_person` for the IT-person button), so #6 analytics can count how many owners forward it to their IT person. That's the number that matters.

**Deploy (in the site repo):** copy `index.html` → `/open-door/index.html` and `og-image.png` → `/open-door/og-image.png`. Add the site's existing font stylesheet to the `<head>` (the page falls back to system fonts on its own). Then test the preview with LinkedIn Post Inspector and by sending the link to yourself on WhatsApp.

**Done when:** it's live with both buttons working on a real phone.
