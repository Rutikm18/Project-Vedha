# #2 Founder LinkedIn: headlines + first post (T1)

**Technical founder (CTO): Rutik Mangale.** `[CONFIRM: the other co-founder's name and role, and which founder posts first]`

## Headlines (LinkedIn limit: 220 characters)

### Business founder (CEO)

1. Co-founder, Vedha · 7-day network health checks for growing Indian businesses, delivered by IT partners you already trust · vedhasec.com  
   *(136 characters)*
2. Building Vedha · Helping owners see what's open on their office network, and prove it's fixed · Looking for Partner Zero IT firms  
   *(129 characters)*
3. Co-founder, Vedha · Find what's open. Prove what's real. Show the fix worked. · For office networks, not cloud  
   *(110 characters)*

### Technical founder (CTO): Rutik Mangale

1. Co-founder & CTO, Vedha · Building a network check that won't call a finding confirmed without evidence · vedhasec.com  
   *(118 characters)*
2. Co-founder, Vedha · Office-network health checks for MSMEs: scanner inside the network, analysis outside, plain-language report  
   *(127 characters)*
3. Building Vedha · A finding is only "confirmed" when the evidence says so; guesses stay "suspected" · 7-day checks through IT partners  
   *(133 characters)*

Pick one per founder. Lead with **who you help**, not your job title. Every headline points to vedhasec.com.

## First post: recommended version A, "the open door" (1062 characters)

Post it **with the 30-second film** (`video/out/vedha_30s_4x5_1080x1350.mp4`, captions `vedha_30s_en.srt`, thumbnail `poster_4x5.png`). The first two lines are the hook, visible before "see more":

```
Last month a scan of one office PC found remote desktop open to the network it was scanned from.
Nobody had switched it on on purpose. Nobody remembered it was there.

That's the problem we're building Vedha for.

Most growing businesses in India don't have a security team. They have an IT person or a local IT firm, a router, a file server, an accounts PC, and a few things nobody has looked at since the day they were installed.

Vedha is a 7-day network health check, run through IT partners you already trust:
→ Find what's open on the office network
→ Prove what's real, with evidence, not guesses
→ Show the fix worked, with a re-check and a plain-language report

No fear, no 200-page PDF. Just: here's what's open, here's the proof, here's the fix, and here's the re-check that shows it's closed.

We're starting with a small group of IT firms, installers and ISO/CA consultants we're calling Partner Zero. If that's you, or someone you trust, I'd like to talk.

30-second film below. Book a 7-day check: vedhasec.com

#MSME #NetworkSecurity #ITPartners
```

**Fact check:** the opening anecdote matches a real Vedha probe run (`probe/scans/*/findings.jsonl`, rule `SVC-RDP-EXPOSED`, "RDP exposed to the scan vantage"). It was a test machine, so it says "one office PC", never a customer. If you'd rather not use a test run as the anecdote, use version B.

## Alternative: version B, "Day 1" (561 characters)

```
Day 1 of telling people what we're building.

Vedha is a 7-day network health check for growing businesses, delivered by the IT partner they already use.

Three things we refuse to do:
1. Scare people. A finding is a fact with a fix, not a threat.
2. Call something "confirmed" without evidence. A port-only guess stays marked "suspected".
3. Hide the fix. Every finding ends with a re-check that shows it's closed.

Office networks only. Not cloud.

If you run IT for small offices and want to be one of our first partners (Partner Zero), my DMs are open.

vedhasec.com
```

## Posting checklist

- [ ] Headlines updated on both founder profiles **before** the post goes out (people click through)
- [ ] Post from the founder's personal profile, then share it from the company page about 2 hours later
- [ ] Upload the film natively (not a YouTube link); add the SRT; set the poster as the thumbnail
- [ ] First comment from the founder: the booking link and one line on Partner Zero
- [ ] Reply to every comment within the first hour
- [ ] Log on Monday's scoreboard: impressions, comments, profile visits, DMs from IT firms

**Claim check:** the "confirmed vs suspected" line matches the product rule in `NETWORK_VA_USE_CASES.md` §3a ("banner-inferred stays suspected").
