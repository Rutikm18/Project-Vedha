# #14 WhatsApp channel with opt-in

**Done when:** the channel is live (Fri 16 Oct). About 20 minutes on a phone.

## The decision: two separate WhatsApp routes

| | **WhatsApp Channel** "Vedha · Signal/Noise" | **Direct WhatsApp** (WhatsApp Business app, broadcast lists) |
|---|---|---|
| For | Anyone: owners, IT people, partners | Partners and people who booked a check |
| Direction | One-way posts, reactions and polls | Two-way conversations |
| Privacy | **Followers' numbers are hidden from us**, and ours from them | We hold their number |
| Consent | Following *is* the opt-in; we store no personal data | **Recorded opt-in required** (DPDP): names WhatsApp, not pre-ticked, logged |
| Use it for | Signal/Noise, the film, poll results, the Open Door Report | Partner Zero chats, check scheduling, report delivery |

**Why:** the channel lets Signal/Noise grow without us holding anyone's number, which is the lowest privacy burden and matches the brand promise ("your number stays private"). Direct messages are only for people with a real relationship, and they consent on the record.

Sources: [WhatsApp blog: Channels](https://blog.whatsapp.com/introducing-whatsapp-channels-a-private-way-to-follow-what-matters), [Infobip channels guide](https://www.infobip.com/blog/how-to-use-whatsapp-channels-for-your-business), [DPDPA.com: WhatsApp and DPDP](https://www.dpdpa.com/blogs/whatsapp_business_dpdpa_compliance_messaging_apps.html), [Go4WhatsUp opt-in guide](https://go4whatsup.com/guides/whatsapp-opt-in/). *Not legal advice; have counsel check the opt-in text along with #9.*

## 1. Create the channel (on the Vedha WhatsApp Business number)

1. WhatsApp → **Updates** → **+** next to Channels → **Create channel**.
2. **Name:** `Vedha · Signal/Noise`
3. **Description:**
   > One short note a week on what actually matters for office networks, from Vedha (vedhasec.com). No fear, no jargon. 7-day network health checks through IT partners you already trust.
4. **Icon:** `channel-icon.png` (the seal sits inside WhatsApp's circular crop).
5. Channel settings → **Reactions: on** (a cheap signal of what lands).
6. Copy the **invite link**, then build the poster:
   ```bash
   cd marketing && LINK="<invite link>" node 14-whatsapp-channel/build.mjs   # makes channel-poster.png
   ```
7. Put the link everywhere people already meet us: site footer, the Open Door page (#12), the Signal/Noise email (#5) footer, the email signature, and the partner kit (#23).

## 2. Opt-in for direct WhatsApp messages (booking step 2, next to #6's field)

Checkbox, **unticked by default**:

> ☐ Send me updates about my check and Vedha's weekly note on **WhatsApp**. I can stop anytime by replying STOP.

- Separate from the terms checkbox (consent must be specific).
- Store the record in the booking (`consent_log.csv` shows the fields): number, consent text version (`WA-OPTIN-v1`), channel = WhatsApp, purpose, source, timestamp, who recorded it, and the withdrawal date if any.
- In person (partners, events): ask, then send them a first message they reply "YES" to. Log it the same way.
- **STOP:** remove them within 24 hours and fill in `withdrawn_at`.
- Broadcast lists only reach people who saved our number, so ask "please save this number" in the first message.

## 3. The first three posts

**Post 1, welcome (day 1):**
```
Welcome to Signal/Noise by Vedha 👋

Once a week: one thing that matters for your office network, one thing to ignore, and one thing to do.

No fear. No jargon. No selling in the channel.

Your number stays private: we can't see who follows.
vedhasec.com
```

**Post 2, Signal/Noise #1 (same week):** the WhatsApp version from `05-signal-noise-1/SIGNAL_NOISE_1.md` (verify the DBIR wording first).

**Post 3, poll (two days later):** this also starts feeding #18, the 15 Controls Awareness Poll.
```
Quick one: do you know what on your office network can be reached from outside?
○ Yes, we've checked
○ Not sure
○ No idea, honestly
```
Then post the film (`video/out/vedha_30s_9x16_1080x1920.mp4`, vertical suits WhatsApp) with: "30 seconds on what a 7-day check finds."

## 4. Rhythm and rules

- **Tuesday:** Signal/Noise (matches the weekly plan). **One extra post a week at most:** a poll, poll results or a fix tip.
- No sales pitches in the channel; the link to book is in the description.
- Every number credited (same rule as the site); never "secure", "protected" or "guaranteed".
- **Monday scoreboard:** followers, reactions per post, poll votes, and bookings with "WhatsApp" in the #6 field.
