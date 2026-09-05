"""Lyrics generation via Gemini. Draft from a preset + theme, then regenerate
the whole song with free-text notes ('make the bridge more desperate')."""

from __future__ import annotations

from pydantic import BaseModel

from selah import config
from selah.vibes import Preset


class LyricSheet(BaseModel):
    title: str
    lyrics: str


_SYSTEM = """You are a gifted gospel songwriter. You write singable, emotionally \
honest, theologically grounded Christian worship lyrics — never cheesy, never \
cliché-stuffed, never preachy filler. Every line should be able to be sung by \
a congregation and land on the ear.

Rules:
- Use section tags in square brackets exactly like [Verse 1], [Chorus], [Bridge].
- Keep hook lines short and repeatable.
- Ground the imagery in real Christian truth; avoid vague spirituality.
- Return the lyrics as plain text with the section tags, blank line between sections."""


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
