# #5 Signal/Noise #1: the DBIR finding

One verified fact, one translation for owners, one thing to do. It follows the brand rules: no fear, no guarantees, every number credited.

**Before sending:** copy the DBIR sentence exactly from page 10 of the report (see `04-site-stats/STATS.md`), and fill `{first_name}` and `{founder_name}`.

## LinkedIn (978 characters)

Post from the founder profile. Attach `video/out/poster_4x5.png`, or no image (text posts do well for newsletters).

```
Signal/Noise #1 · The way in has changed

SIGNAL
For the first time, exploiting a vulnerability is the most common way attackers get in: 31% of breaches, now ahead of stolen logins.
(Verizon 2026 Data Breach Investigations Report)

What that means for a 30-person office: the risk isn't only "someone guessed a password". It's a service that's switched on, reachable, and not updated: remote desktop, a file share, a router admin page.

NOISE
"AI will hack everyone tomorrow." Maybe faster, but the doors are the same ones. Start there.

WHAT TO DO THIS WEEK
1. Ask your IT person or firm one question: "What on our network can be reached from outside?"
2. If the answer is "not sure", that's normal. It's also the first thing to fix.
3. Anything that can be reached and doesn't need to be: close it. Anything that does: put it behind a VPN with MFA.

Signal/Noise is a short weekly note from Vedha on what actually matters for office networks. No fear, no jargon.

vedhasec.com
```

## Email

**Subject:** Signal/Noise #1: the way in has changed
**Preview text:** One finding, one question for your IT person.

```
Hi {first_name},

One finding worth your two minutes this week.

SIGNAL
Exploiting vulnerabilities is now the most common way attackers get into an organisation: 31% of breaches, ahead of stolen logins for the first time.
Source: Verizon 2026 Data Breach Investigations Report.

Why it matters for a growing business: the risk isn't only a guessed password. It's a service that's switched on, reachable and out of date: remote desktop, a shared folder, a router's admin page.

NOISE
"AI will break everything overnight." Attacks are getting faster, but they still come through the same doors.

ONE QUESTION FOR YOUR IT PERSON
"What on our network can be reached from outside, and does it need to be?"
If nobody's sure, that's the first thing to find out.

That's it for this week.
{founder_name}, Vedha
vedhasec.com · 7-day network health checks through IT partners you already trust

You're receiving this because you asked for Signal/Noise. Reply "stop" and we'll take you off the list.
```

Send only to people who opted in (the WhatsApp opt-in comes with #14). Keep the unsubscribe line.

## WhatsApp (403 characters)

For forwarding by partners and to opted-in contacts. Short, scannable, and the one action is in bold.

```
*Signal/Noise #1* 🔎

*Signal:* exploiting vulnerabilities is now the #1 way attackers get in: *31%* of breaches, ahead of stolen logins.
_(Verizon 2026 Data Breach Investigations Report)_

*For your office:* the risk is a service that's ON, reachable and old: remote desktop, a shared folder, the router admin page.

*Ask your IT person:* "What on our network can be reached from outside?"

vedhasec.com
```

## Fact sheet

| Claim | Source | Status |
|---|---|---|
| Vulnerability exploitation is the top initial access vector, 31% | Verizon 2026 DBIR (via Help Net Security, Tenable coverage) | Verify wording on p.10 |
| Ahead of stolen credentials (13%) | Same | Verify |
| Remote desktop / file share / router admin as examples | Vedha's own checks (`SVC-RDP-EXPOSED` seen in real probe runs; SMB/NFS rules shipped) | Sourced |
| "VPN with MFA" advice | The product's own recommendation text for RDP exposure | Sourced |
