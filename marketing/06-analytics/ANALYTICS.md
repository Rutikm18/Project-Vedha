# #6 Cookieless analytics, Search Console, and "How did you hear about us?"

The site repo (with `api/book.js`) isn't in this session. Below are drop-in pieces; whoever has the site repo can apply them in about 30 minutes. **Done when:** the field is live in `api/book.js`.

## 1. Cookieless analytics (pick one)

| Option | Cookieless | Cost | Why |
|---|---|---|---|
| **Vercel Web Analytics** (recommended, since the site has a `vercel.json`) | Yes | Free tier | One line; no consent banner needed for basic page analytics; already on your host |
| Plausible | Yes | Paid (self-host free) | Simple dashboard, UTM reports |
| Cloudflare Web Analytics | Yes | Free | Only if DNS is on Cloudflare |

**Vercel (single static `index.html`):** turn on Analytics in the Vercel project, then add this before `</body>`:

```html
<script defer src="/_vercel/insights/script.js"></script>
```

**UTM tags already in use** (so they show up as sources): `utm_source=c0c0n&utm_medium=qr_card&utm_campaign=partner_zero` (#1 card). Use `utm_source=linkedin|whatsapp|email`, `utm_campaign=signal_noise_1|film_launch|partner_zero` for every link we post.

## 2. Google Search Console

1. search.google.com/search-console → Add property → **Domain** → `vedhasec.com`.
2. Add the TXT record it shows at your DNS provider; wait, then Verify.
3. Sitemaps → submit `https://vedhasec.com/sitemap.xml` (single-page site: a one-URL sitemap is fine).

## 3. "How did you hear about us?" on booking step 2

### Field (HTML, step 2 of the booking form)

```html
<label for="heard_from">How did you hear about us?</label>
<select id="heard_from" name="heard_from" required>
  <option value="">Choose one</option>
  <option value="it_partner">My IT person or IT firm</option>
  <option value="linkedin">LinkedIn</option>
  <option value="whatsapp">WhatsApp forward</option>
  <option value="friend">A friend or another business</option>
  <option value="event">An event</option>
  <option value="search">Google search</option>
  <option value="other">Other</option>
</select>
<input id="heard_from_other" name="heard_from_other" maxlength="120" placeholder="Tell us more (optional)">
```

Order matters: **IT partner is first** because it's the channel we're testing. "Other" with a free-text box catches **unprompted recall** (Monday scoreboard): read those answers word for word every week.

### Server validation (`api/book.js`)

Copy `heardFrom.js` (next to this file) into the site repo and call it in the handler before saving the booking:

```js
import { parseHeardFrom } from './heardFrom.js';
// inside the handler, after the existing validation:
const heard = parseHeardFrom(body);
if (!heard.ok) return res.status(400).json({ error: heard.error });
booking.heard_from = heard.value;            // e.g. "it_partner"
booking.heard_from_other = heard.other;      // free text or null
booking.utm = heard.utm;                     // utm_source / medium / campaign, if present
```

`heardFrom.js` allow-lists values, caps free text at 120 characters, strips control characters, and keeps UTM fields. That way the scoreboard counts are clean and nothing odd gets stored.
