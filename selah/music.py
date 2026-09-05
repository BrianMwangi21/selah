"""Music generation via Lyria (Gemini Interactions API).

NOTE: Lyria 3.5 is brand new; the exact call surface may shift. Everything that
could change is isolated here, and model IDs come from .env — so a rename is a
one-line config fix, not a code change."""

from __future__ import annotations

import base64
from pathlib import Path

from selah import config
from selah.storage import Song
from selah.vibes import get_preset


def _music_prompt(song: Song) -> str:
    try:
        style = get_preset(song.preset).music_prompt() if song.preset else ""
    except KeyError:
        style = ""
    if not style:
        style = "Genre: gospel worship, full arrangement with vocals."
    return (
        f"A gospel worship song. {style} "
        f"Theme: {song.theme}. Sing the following lyrics with the section "
        f"structure exactly as tagged.\n\n{song.lyrics}"
    )


def render(song: Song, preview: bool = True) -> Path:
    """Generate audio for a song and write it into the song folder.

    preview=True -> short cheap clip; preview=False -> full song.
    Returns the path to the written MP3.
    """
    client = config.get_client()
    model = config.LYRIA_PREVIEW_MODEL if preview else config.LYRIA_FULL_MODEL

    interaction = client.interactions.create(
        model=model,
        input=_music_prompt(song),
    )

    audio = getattr(interaction, "output_audio", None)
    if audio is None or not getattr(audio, "data", None):
        raise RuntimeError(
            "Lyria returned no audio. The Interactions API shape may have "
            "changed — check selah/music.py against the current docs."
        )

    song.dir.mkdir(parents=True, exist_ok=True)
    out = song.dir / ("preview.mp3" if preview else "song.mp3")
    out.write_bytes(base64.b64decode(audio.data))
    return out
