---
Date: 2026-09-04
tags:
---

# Selah — The AI Gospel Pipeline

*A pause in the music. A moment where the house listens. That is the lane.*

# Summary

A fully programmatic pipeline that writes, produces, packages, and publishes gospel songs to YouTube on autopilot. One channel, 12 strong songs, zero flooding. Each track goes through an approval gate (me) before it ever sees the upload button.

The moat is the musical ear. The AI drafts, the ear approves. Quality gate = human.

# Why This Lane

- Christian/gospel content reliably blows up on YouTube. Loyal audience, shares like crazy, evergreen search traffic.
- The 10-second AI gospel hook that keeps replaying in my head is the proof — the ear is already catching what the algorithm can't.
- Passive income math: 12 good songs, published once, AdSense runs while I sleep.
- Serve, don't flood. A tight playlist of 12 beats a thousand throwaways.

# The Pipeline

## 1. Lyrics
- LLM call per track (OpenRouter key already exists, or Gemini API if already in the project).
- Prompt per song: a core Christian element (grace, mercy, redemption, the cross, praise, the prodigal, the valley, the harvest...).
- Output: full lyric sheet + a title + the song's core "vibe directive" for the music model.

## 2. Song
- **Lyria 3.5 Pro** via the Gemini API — full songs up to 3 minutes (verses, chorus, bridge) at 44.1kHz stereo.
- Same Google Cloud project as the YouTube upload — one house, one billing.
- Backup route: third-party Suno wrapper (~$0.05–$0.11/song) if vocals need to go next level.

## 3. Approval gate
- Generated MP3 lands in Discord (the nanobot already lives there).
- I listen, give the nod (or reject).
- Only approved tracks proceed. This is where the ear earns its keep.

## 4. Meta
- Auto-generate from the lyric script: title, description, tags, keywords, and the "AI-generated content" declaration for YouTube.

## 5. Cover art
- Image generation from the song's theme (e.g., sun through a church window, a shepherd, an open road).
- Consistent visual identity across the 12 tracks so it looks like an album, not a bot.

## 6. Video assembly
- ffmpeg: cover art + audio → MP4.
- Slow zoom (Ken Burns) so it's not a static frame — YouTube likes motion.

## 7. Upload
- YouTube Data API v3 (OAuth) — scheduled publish, one per week or as the playlist fills.
- Title, description, tags, thumbnail, AI-content checkbox all set programmatically.

# Account Setup (the one-time part)

- One Google Cloud project. That's it — everything lives there.
- Enable two things: the Gemini API (for the music) and the YouTube Data API v3 (for upload).
- Billing: Google Cloud is postpaid — card on file, charged monthly after usage. Attach a budget alert at e.g. $5 so it behaves like the prepaid top-ups I already know.
- Free tier covers a lot — 12 songs a month is easily within it.

# Tech Stack

- Gemini API (Lyria 3.5 Pro) — song generation
- LLM (OpenRouter / Gemini) — lyrics + meta
- Image generation — cover art
- ffmpeg — video assembly (cover + audio, slow zoom)
- YouTube Data API v3 — scheduled uploads
- nanobot — the Discord approval loop (cron → generate → DM → approve/reject)

# Cost

- 12 songs, end to end: a few dollars. Negligible.

# Target Audience

- Christians, worldwide. The genre that never stops searching.

# Profit

- YouTube AdSense (after monetization thresholds)
- Audience grows into a community → potential for merch, live streams, collabs
- The playlist becomes a portfolio: same pipeline, new niches later

# Does it pass the mom test ?

Mum listens to gospel. If she would replay track 3 of 12, the ear was right.

# Next Steps

1. Decide: Lyria via one Google project, or Suno wrapper for vocals.
2. Set up the Cloud project + billing alert.
3. Build the pipeline repo: lyrics → song → Discord approval → cover → ffmpeg → upload.
4. First track in the DMs by tonight.

# Link

- [Google AI music generation docs](https://ai.google.dev/gemini-api/docs/music-generation)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)