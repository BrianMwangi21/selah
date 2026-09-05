---
Date: 2026-09-04
tags:
---

# Selah — The AI Gospel Pipeline

*A pause in the music. A moment where the house listens. That is the lane.*

# Summary

A programmatic pipeline that writes, produces, and packages gospel songs for YouTube. One channel, 12 strong songs, zero flooding. Each track goes through an approval gate (me) before I upload it — uploads I handle myself.

The moat is the musical ear. The AI drafts, the ear approves. Quality gate = human.

# Why This Lane

- Christian/gospel content reliably blows up on YouTube. Loyal audience, shares like crazy, evergreen search traffic.
- The 10-second AI gospel hook that keeps replaying in my head is the proof — the ear is already catching what the algorithm can't.
- Passive income math: 12 good songs, published once, AdSense runs while I sleep.
- Serve, don't flood. A tight playlist of 12 beats a thousand throwaways.

# The Pipeline

## 1. Lyrics
- Gemini call per track (one Google house — same project as the music).
- Prompt per song: a core Christian element (grace, mercy, redemption, the cross, praise, the prodigal, the valley, the harvest...).
- Output: full lyric sheet + a title + the song's core "vibe directive" for the music model.

## 2. Song
- **Lyria via the Gemini Interactions API** — full songs with vocals + custom lyrics (section tags), 44.1kHz stereo. Confirmed it sings your lyrics, not just instrumentals.
- Model: `lyria-3-pro-preview` — full ~3-min song. Each render is a fresh performance, so there's no separate preview step.
- The render is nudged to ~3–3.5 min with a dynamic-arc directive (restrained verses → big choruses → building bridge → final-chorus climax).
- Same Google Cloud project as everything else — one house, one billing.
- ~~Suno backup~~ dropped. Lyria does vocals; no need to mix-and-mash.

## 3. Approval gate
- I listen to the generated MP3 and give the nod (or reject).
- Only approved tracks proceed. This is where the ear earns its keep.

## 4. Meta
- Auto-generate from the lyric script: title, description, tags, keywords, and the "AI-generated content" declaration for YouTube.

## 5. Cover art
- **Nano Banana (Gemini image)** paints a *heavenly, worshipful* scene (divine light, god-rays) from the theme — atmosphere, not literal lyric metaphors. `selah cover <slug>`. (Imagen was retired Aug 2026 → Nano Banana.)
- One shared album style so the 12 tracks look like an album, not a bot.
- Song title + **SELAH** wordmark are overlaid with Pillow (`selah title`), not AI-rendered — uniform typography across every cover. Re-runnable for free.

## 6. Video assembly
- ffmpeg: titled cover + audio → MP4. `selah video <slug>` (or `--square`).
- Slow zoom (Ken Burns) so it's not a static frame — YouTube likes motion. Pure ffmpeg, no spend.

## 7. Upload (manual)
- I upload approved tracks to YouTube myself, one per week or as the playlist fills.
- The auto-generated meta (title, description, tags) is there to paste in; thumbnail and the AI-content checkbox I set by hand.

# Account Setup (the one-time part)

- One Google Cloud project. That's it — everything lives there.
- Enable the Gemini API (Generative Language API) — lyrics and music both run through it.
- Billing: Google Cloud is postpaid — card on file, charged monthly after usage. Attach a budget alert at e.g. $5 so it behaves like the prepaid top-ups I already know.
- Free tier covers a lot — 12 songs a month is easily within it.

# Tech Stack

- **Gemini API (Lyria)** — song generation (vocals + lyrics)
- **Gemini (`gemini-3.7-flash`)** — lyrics + meta. OpenRouter dropped; one Google house.
- **Nano Banana (Gemini image)** — cover art
- **ffmpeg** — video assembly (titled cover + audio, Ken Burns zoom)
- **Python CLI** (Typer + Rich) — the studio front-end where the ear works

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
3. Build the pipeline repo: lyrics → song → (listen & approve) → cover → ffmpeg → manual upload.
4. First track in the DMs by tonight.

# Decisions & Build Log

*Updated 2026-09-05.*

**Decisions locked:**
- **One Google house.** Gemini for lyrics + meta, Lyria for music, Nano Banana (Gemini image) for art. No OpenRouter, no Suno.
- **CLI-first, human in the loop.** Not full autopilot. Creation is hands-on (vibe → lyrics → tweak *before* spending on audio). Cover art + video assembly get automated later; approval and upload stay manual by choice.
- **Regenerate-with-notes** for tweaking (whole song each pass). Flat files, one folder per song: `songs/<slug>/lyrics.md` with frontmatter.
- **Flash for lyrics** (cents), Lyria money spent where the ear can hear it (~$1/full song).
- **Presets over free-text vibe** — six detailed fingerprints: elevation, maverick-city, bethel, hillsong, mary-mary, ron-kenoly. Specific BPM/instrumentation/vocals/imagery, because AIs reward specifics. Temperature knob for experimentation.
- **Approval + upload = manual, on purpose.** Cover art + video assembly automated later.
- **No preview step.** Lyria is non-deterministic (a fresh performance each run), so a 30s clip doesn't predict the full song — one render, always the full song.

**Project:** Google Cloud `selah-507714` · repo `github.com:BrianMwangi21/selah`.

**Built & working:**
- Rich CLI: `new`, `list`, `show`, `render`, `presets`, `preset <key>`.
- Lyrics generation + the in-the-loop tweak flow — verified (elevation, bethel).
- Six presets — all heard and tuned; distinct, faithful voices confirmed (call-and-response annotations locked in for maverick-city & ron-kenoly).
- Lyrics craft layer — a "write for the arc" super-prompt (hook → verse/chorus contrast → pre-chorus lift → bridge-as-peak → final-chorus payoff) layered on top of each preset's voice.
- Lyria music stage — **verified**: full ~3-min song renders to a valid 192 kbps / 44.1 kHz stereo MP3 (`selah render`).
- Cover art stage — **verified**: heavenly 2048×2048 art (Nano Banana) + Pillow title/SELAH overlay (`selah cover`, `selah title`).
- Video stage — **verified**: titled cover + audio → 1920×1080 MP4 with a Ken Burns zoom, length pinned to the audio (`selah video`). Pure ffmpeg.

**Next:**
1. Write the twelve, then upload the winners by hand.

The full creation pipeline — lyrics → song → cover → video — is built and verified end to end.

# Link

- [Google AI music generation docs](https://ai.google.dev/gemini-api/docs/music-generation)