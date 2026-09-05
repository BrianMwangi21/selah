# Selah

> *A pause in the music. A moment where the house listens. That is the lane.*

An AI gospel-songwriting studio in your terminal. Pass a **vibe** and a **theme**,
get back a full lyric sheet, tweak it with plain-language notes until it lands on
the ear, then hand it to **Lyria** to sing. Built to write a tight set of strong
songs — not to flood a feed.

The moat is the ear. The AI drafts; you approve.

---

## How it works

```
vibe + theme ─▶ Gemini ─▶ lyric sheet ─▶ (tweak with notes) ─▶ save ─▶ Lyria ─▶ MP3
                                            └── you, in the loop ──┘
```

- **Lyrics** — Gemini writes a full, structured lyric sheet from a preset + theme.
- **Tweak loop** — you regenerate the whole song with notes like *"make the bridge
  more desperate, cut verse 2"* until it's right.
- **Music** — Lyria (Gemini Interactions API) sings the lyrics — a cheap 30s
  preview clip or a full song.
- **Storage** — every song is a plain `songs/<slug>/lyrics.md` with frontmatter.
  Git-able, eyeball-able.

Everything lives in **one Google Cloud project** — Gemini for lyrics, Lyria for
music. One house, one key.

---

## Setup

Requires Python 3.10+ and a Google Cloud project with the **Generative Language
API** enabled and **billing active**.

```bash
# 1. Install (editable, in a venv)
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Configure
cp .env.example .env
#   then paste your Gemini API key into .env  (from aistudio.google.com)
```

Your `.env` (and anything under `secrets/`) is gitignored — keys never get
committed.

### Environment

| Variable | What it is |
|---|---|
| `GEMINI_API_KEY` | API key from AI Studio, in your billed Cloud project |
| `GEMINI_LYRICS_MODEL` | Text model for lyrics (default `gemini-3.7-flash`) |
| `GEMINI_TEMPERATURE` | Default creativity 0–2 (default `1.0`) |
| `LYRIA_PREVIEW_MODEL` | 30s clip model (`lyria-3-clip-preview`) |
| `LYRIA_FULL_MODEL` | Full-song model (`lyria-3-pro-preview`) |
| `SONGS_DIR` | Where songs are written (default `songs/`) |

---

## Usage

```bash
# Draft a song, then tweak it in the loop
selah new --preset elevation --theme "grace"
selah new -p bethel -t "the wilderness" --temp 1.2   # crank creativity

# During the loop:  [a]ccept · [n]otes (regenerate) · [t]itle · [q]uit

# Browse
selah presets                 # list the vibes
selah preset elevation        # full musical + lyrical spec for one
selah list                    # all songs written so far
selah show <slug>             # print a song's lyrics

# Make audio (costs money — see below)
selah render <slug>           # cheap 30s preview clip
selah render <slug> --full    # full Lyria song

# Make cover art (Nano Banana) — heavenly art + stamped title
selah cover <slug>            # album cover (1:1) + title/SELAH overlay
selah cover <slug> -n 4       # four art options to choose from
selah cover <slug> --no-text  # art only, no title
selah title <slug>            # (re)stamp title + SELAH on the cover (free)
```

---

## Vibe presets

Each preset carries a detailed **musical spec** (fed to Lyria) and a **lyrical
brief** (fed to Gemini) — specific BPM, instrumentation, vocal arrangement,
production, imagery. AIs reward specifics.

| key | in the spirit of | feel |
|---|---|---|
| `elevation` | Elevation Worship | anthemic arena worship, builds 70→136 BPM |
| `maverick-city` | Maverick City Music | raw collective gospel-worship, 68–92 BPM soul groove |
| `bethel` | Bethel Music | intimate atmospheric worship, 62–74 BPM, spacious |
| `hillsong` | Hillsong Worship | cinematic arena worship, lush & polished |
| `mary-mary` | Mary Mary | urban contemporary gospel, 90–110 BPM R&B groove |
| `ron-kenoly` | Ron Kenoly | 90s celebratory praise, 108–135 BPM, live & brassy |

Tune them freely in `selah/vibes.py` once you hear real output — that's where the
ear gets encoded.

---

## Cost

Lyrics are noise — a few cents for the whole project. The money is in audio:
Lyria runs about **$0.006/sec**, so a 30s preview ≈ **$0.18** and a full ~3-min
song ≈ **~$1**. Twelve songs, end to end: a few dollars. Set a budget alert.

---

## Project layout

```
selah/
├── selah/
│   ├── cli.py       # Rich-styled CLI + the tweak loop
│   ├── vibes.py     # the presets (music + lyric fingerprints)
│   ├── lyrics.py    # Gemini draft + regenerate-with-notes
│   ├── music.py     # Lyria interactions API
│   ├── art.py       # cover art (Nano Banana) + Pillow title overlay
│   ├── storage.py   # songs/<slug>/lyrics.md
│   └── config.py    # env-driven config
├── songs/           # generated songs — local only, gitignored
├── .env.example
└── pyproject.toml
```

---

## Roadmap

- [x] Vibe + theme → lyrics with an in-the-loop tweak flow
- [x] Six detailed vibe presets (all heard & tuned)
- [x] Lyria music stage — verified against real 44.1 kHz stereo MP3 output
- [x] Cover art stage — heavenly Nano Banana art + Pillow title/SELAH overlay (verified, 2048×2048)
- [ ] ffmpeg video assembly

*Approval (listening) and YouTube upload are done manually, by choice.*
