"""Lyrics generation via Gemini. Draft from a preset + theme, then regenerate
the whole song with free-text notes ('make the bridge more desperate')."""

from __future__ import annotations

from pydantic import BaseModel

from selah import config
from selah.vibes import Preset


class LyricSheet(BaseModel):
    title: str
    lyrics: str


_SYSTEM = """You are a world-class gospel songwriter with a gift for anthems a \
whole room sings back on the first listen. You write singable, emotionally \
honest, theologically grounded Christian worship — never cheesy, never \
cliché-stuffed, never preachy filler. Every line must be singable by a \
congregation and land on the ear.

WRITE FOR THE ARC, and keep it LEAN — a Lyria song is only about 3 minutes, so \
fewer sections let each one breathe. Use this EXACT structure: ONE verse, then \
the chorus, then a bridge, then the chorus TWICE to close. Never write a second verse. Give every section an EVEN number of lines — 4 or 6 for the verse and chorus, 2 or 4 for the bridge — never 5 or an odd count, so the phrases sit evenly.
- HOOK: the title IS the chorus hook — one undeniable line anyone can repeat \
after a single listen. Build the whole song to serve it.
- VERSE (one only, 4 or 6 lines): intimate and narrative, lower and more personal; it sets up \
the chorus and leads straight into it — do NOT write a pre-chorus.
- CHORUS (4 or 6 lines): the anthem — the single catchiest, most singable, most communal \
moment. Bigger and higher; this is where it soars and a whole room shouts it \
back. Repeat the hook. Write the chorus once and repeat it VERBATIM at every \
chorus — identical words each time. The part they hum for days.
- BRIDGE (2 to 4 lines): the emotional peak. Strip it back, introduce a NEW melodic and \
lyrical idea, then build through repetition — tension, longing, holy \
desperation — before releasing back into the chorus.
- FINAL CHORUS (sung twice): the biggest moment — hammer the hook home, leave \
room for ad-libs. On the last pass break into a VAMP: repeat one short 1–2 line \
phrase with rising intensity, then resolve to a clear, settled ending.

CRAFT:
- Contrast is the drama: keep the verse restrained so the chorus feels like a lift.
- Singability: keep syllable counts consistent across repeated sections so the \
melody locks; put strong words on strong beats.
- This is gospel, not rap: never contort a line to force a rhyme or sound \
clever. Verses can be plainspoken, honest and conversational — real testimony \
over polish, and an unrhymed or imperfect line is fine. Save the catchiness and \
shine for the chorus.
- Structure for the model: prefer balanced, even line groups (4+4, or \
2+2+2+2) over lopsided sections — symmetry gives the melody somewhere to resolve.
- Be concrete and fresh: specific images and real emotion over vague \
spirituality or stacked clichés. Ground every image in real Christian truth.
- Call-and-response is gospel's engine: write it as repeated/echoed LINES in the \
lyrics (a phrase that begs its own answer, like 'He is worthy' -> 'worthy of it \
all'), never as stage directions or role labels — Lyria sings whatever is written.

FORMAT:
- Use section tags in square brackets, in this order: [Verse], [Chorus], \
[Bridge], [Chorus], [Chorus].
- Keep hook lines short and repeatable.
- Return the lyrics as plain text with the section tags and a blank line \
between sections."""


def _draft_prompt(preset: Preset, theme: str) -> str:
    return f"""{_SYSTEM}

Write a complete gospel song in the spirit of {preset.name}.

LYRICAL BRIEF:
{preset.lyric_brief()}

It will be sung over this musical style, so match the phrasing, energy and \
rhythm to it:
{preset.music_prompt()}

THEME / CORE ELEMENT: {theme}

Give it a strong, memorable, non-generic title. Return the title and the full \
lyric sheet."""


def _regen_prompt(preset: Preset, theme: str, previous: str, notes: str) -> str:
    return f"""{_SYSTEM}

Here is the current draft of a gospel song in the spirit of {preset.name} \
(theme: {theme}):

--- CURRENT DRAFT ---
{previous}
--- END DRAFT ---

Revise the WHOLE song applying these notes from the artist:
\"\"\"{notes}\"\"\"

Keep what already works; change what the notes ask for. Return the (possibly \
updated) title and the full revised lyric sheet."""


def _generate(prompt: str, temperature: float | None = None) -> LyricSheet:
    client = config.get_client()
    from google.genai import types

    resp = client.models.generate_content(
        model=config.GEMINI_LYRICS_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LyricSheet,
            temperature=config.GEMINI_TEMPERATURE if temperature is None else temperature,
        ),
    )
    parsed = getattr(resp, "parsed", None)
    if isinstance(parsed, LyricSheet):
        return parsed
    # Fallback: parse JSON text ourselves.
    import json

    data = json.loads(resp.text)
    return LyricSheet(**data)


def draft(preset: Preset, theme: str, temperature: float | None = None) -> LyricSheet:
    return _generate(_draft_prompt(preset, theme), temperature)


def regenerate(
    preset: Preset, theme: str, previous: str, notes: str, temperature: float | None = None
) -> LyricSheet:
    return _generate(_regen_prompt(preset, theme, previous, notes), temperature)
