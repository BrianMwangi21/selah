"""Music generation via Lyria (Gemini Interactions API).

Each render is a fresh Lyria performance (non-deterministic), so there is no
separate 'preview' step — `render` always cuts the full song. Model ID comes
from .env, so a rename is a one-line config fix, not a code change."""

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

    # Give Lyria the length + dynamic arc so the build has room to breathe.
    directive = (
        " Create a complete song approximately 3 to 3.5 minutes long. Build "
        "the dynamics across the whole song: restrained verses, lifting "
        "pre-choruses, big anthemic choruses, a stripped-back bridge that "
        "grows in intensity, and a final chorus that lifts higher than the "
        "rest with ad-libs and key-change energy."
    )

    return (
        f"A gospel worship song. {style}{directive} "
        f"Theme: {song.theme}. Sing the following lyrics with the section "
        f"structure exactly as tagged.\n\n{song.lyrics}"
    )


def render(song: Song) -> Path:
    """Generate the full song audio and write it into the song folder.

    Returns the path to the written MP3."""
    client = config.get_client()

    interaction = client.interactions.create(
        model=config.LYRIA_MODEL,
        input=_music_prompt(song),
    )

    audio = getattr(interaction, "output_audio", None)
    if audio is None or not getattr(audio, "data", None):
        raise RuntimeError(
            "Lyria returned no audio. The Interactions API shape may have "
            "changed — check selah/music.py against the current docs."
        )

    song.dir.mkdir(parents=True, exist_ok=True)
    out = song.dir / "song.mp3"
    out.write_bytes(base64.b64decode(audio.data))
    return out
