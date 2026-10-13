# #9 Data-use clause: DRAFT FOR COUNSEL (not legal advice)

**Status:** draft for counsel to review. Nothing here has been legally reviewed. It's grounded in what the product actually does today (`probe/DATA_HANDLING.md`, `docs/planning/2026-10-01-data-privacy-compliance-approach.md`).

## Read this first, counsel: what the product can and can't do today

| Promise a clause might make | True today? | Source |
|---|---|---|
| Scan data is treated as confidential customer data | Yes | DATA_HANDLING.md |
| Encrypted in transit (TLS 1.2+) and at rest on the agent | Yes | DATA_HANDLING.md |
| The agent only sends to the customer's own manager URL | Yes | DATA_HANDLING.md |
| Logs are redacted | Yes | DATA_HANDLING.md |
| **Delete a customer's data on request** | **Not yet as a product feature (gap P1); manual only** | privacy approach §5 |
| **Automatic retention limits** | **Not yet (gap P2)** | privacy approach §5 |
| AI features off unless the customer turns them on | Planned principle, not yet per customer (gap P9) | privacy approach §6.1 |

So the draft below promises deletion "on written request, within 30 days" (doable manually), **not** automatic purges, and doesn't promise AI-off until that setting exists.

## Draft clause (for the 7-day check terms)

**X. How we use your network data**

X.1 **Roles.** For the network data collected during the check ("Scan Data"), you are the data fiduciary and Vedha acts as your data processor, under the Digital Personal Data Protection Act, 2023 and the rules made under it. Vedha uses Scan Data only to deliver the check, the report and the re-check, and to support you afterwards.

X.2 **What Scan Data is.** Information about devices and services on your network: addresses, device and service names, software versions, and the results of our checks. We don't collect the contents of your files, emails or business records.

X.3 **Protection.** Scan Data is encrypted in transit and at rest, access is limited to people who need it to deliver your check, and our logs are redacted.

X.4 **Aggregated research.** Vedha may use Scan Data to produce aggregated statistics (for example, "x% of offices checked had remote desktop reachable") **only** where no organisation, person, device or network can be identified, and only by combining results from many organisations. We will never publish or share your Scan Data, or anything that identifies you, without your written permission. You can opt out of aggregated research at any time by writing to info@vedhasec.com, and that won't affect your check.

X.5 **No sale.** We don't sell Scan Data or use it for advertising.

X.6 **Your partner.** Your IT partner sees your report and findings so they can help you fix them. They're bound by confidentiality terms with Vedha.

X.7 **Deletion.** On written request, we'll delete your Scan Data within 30 days, except where the law requires us to keep it, and confirm in writing.

X.8 **Incidents.** If we become aware of a breach affecting your Scan Data, we'll tell you without undue delay, and within 24 hours of confirming it, so you can meet your own obligations.

*Counsel to check: X.1 roles; X.4 (de-identification standard, opt-out vs opt-in); X.7 (30 days is feasible manually); X.8 against CERT-In 6-hour and DPDP 72-hour clocks; the sub-processor list (hosting, any AI provider) as a schedule.*

## T7 line for the booking confirmation

> Your network data is used only to run your check, protected while we hold it, and never shared or sold. Aggregated, anonymous statistics may be used in Vedha research unless you opt out (info@vedhasec.com). Full terms: [link].

*(This is why the Open Door Report (#29) can be published: X.4 is the permission it rests on. Don't publish any aggregate until this clause is live in signed check terms.)*
