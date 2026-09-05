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

WRITE FOR THE ARC — a great gospel song is a build, not a list of verses:
- HOOK: the title IS the chorus hook — one undeniable line anyone can repeat \
after a single listen. Build the whole song to serve it.
- VERSES: intimate and narrative, lower and more personal; they set up the \
chorus and lead straight into it — do NOT write a pre-chorus. Each verse moves \
the story forward — never restate the same idea.
- CHORUS: the payoff — bigger, higher, declarative, communal. Repeat the hook. \
This is the part they will hum for days.
- BRIDGE: the emotional peak. Strip it back, introduce a NEW melodic and \
lyrical idea, then build through repetition — tension, longing, holy \
desperation — before releasing back into the chorus. This is the moment right \
before it goes all the way up.
- FINAL CHORUS: the biggest moment of the song — hammer the hook home, leave \
room for ad-libs and a tag, key-change energy.

CRAFT:
- Contrast is the drama: keep the verses restrained so the chorus feels like a lift.
- Singability: keep syllable counts consistent across repeated sections so the \
melody locks; put strong words on strong beats; use honest, unforced rhyme.
- Structure for the model: prefer balanced, even line groups (4+4, or \
2+2+2+2) over lopsided sections — symmetry gives the melody somewhere to resolve.
- Be concrete and fresh: specific images and real emotion over vague \
spirituality or stacked clichés. Ground every image in real Christian truth.

FORMAT:
- Use section tags in square brackets exactly like [Verse 1], [Chorus], \
[Bridge], [Final Chorus].
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
