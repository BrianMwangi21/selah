"""Music generation via Lyria (Gemini Interactions API).

Two modes:
  - render(song):      Lyria SINGS the lyrics we wrote (the human-lyric flow).
  - render_auto(song): Lyria WRITES its own lyrics from the theme, then sings
                       them, and hands the lyrics back (the --auto flow).

Each render is a fresh, non-deterministic performance. Model ID comes from .env.
Lyria's safety filter occasionally throws a spurious 'prohibited_content' on
input that succeeds on retry, so calls are retried a few times."""

from __future__ import annotations

import base64
import time
from pathlib import Path

from selah import config
from selah.storage import Song
from selah.vibes import get_preset

# Length + dynamic-arc directive so the build has room to breathe.
_FULL_DIRECTIVE = (
    " Create a complete song about 3 minutes long with a lean structure so it can "
    "breathe: one verse, then the chorus, then a bridge, then the chorus twice to "
    "close. Build the dynamics — a restrained verse, a big anthemic chorus, a "
    "bridge that grows in intensity, and a soaring final double chorus — and land "
    "a clear, resolved ending (do not cut off abruptly)."
)


def _style(song: Song) -> str:
    try:
        style = get_preset(song.preset).music_prompt() if song.preset else ""
    except KeyError:
        style = ""
    return style or "Genre: gospel worship, full arrangement with vocals."


def _music_prompt(song: Song) -> str:
    return (
        f"A gospel worship song. {_style(song)}{_FULL_DIRECTIVE} "
        f"Theme: {song.theme}. Sing the following lyrics with the section "
        f"structure exactly as tagged.\n\n{song.lyrics}"
    )


def _auto_prompt(song: Song) -> str:
    return (
        f"A gospel worship song. {_style(song)} Write your own lyrics (do not "
        f"wait for lyrics to be provided): a song about {song.theme}."
        f"{_FULL_DIRECTIVE}"
    )


def _create(prompt: str, attempts: int = 3):
    """Call Lyria, retrying the flaky spurious content refusals."""
    client = config.get_client()
    last: Exception | None = None
    for _ in range(attempts):
        try:
            interaction = client.interactions.create(
                model=config.LYRIA_MODEL, input=prompt
            )
        except Exception as e:  # noqa: BLE001 — inspect the message
            last = e
            if "prohibited_content" in str(e).lower():
                time.sleep(2)
                continue
            raise
        audio = getattr(interaction, "output_audio", None)
        if audio is not None and getattr(audio, "data", None):
            return interaction
        last = RuntimeError(
            "Lyria returned no audio. The Interactions API shape may have "
            "changed — check selah/music.py against the current docs."
        )
        time.sleep(1)
    raise last  # type: ignore[misc]


def render(song: Song) -> Path:
    """Lyria sings the song's saved lyrics. Returns the MP3 path."""
    interaction = _create(_music_prompt(song))
    return _write_mp3(song, interaction)


def render_auto(song: Song) -> tuple[Path, str]:
    """Lyria writes its own lyrics from the theme and sings them.

    Returns (mp3 path, the lyrics Lyria wrote)."""
    interaction = _create(_auto_prompt(song))
    out = _write_mp3(song, interaction)
    return out, _clean_auto_lyrics(getattr(interaction, "output_text", None))


def _write_mp3(song: Song, interaction) -> Path:
    song.dir.mkdir(parents=True, exist_ok=True)
    out = song.dir / "song.mp3"
    out.write_bytes(base64.b64decode(interaction.output_audio.data))
    return out


def _clean_auto_lyrics(text: str | None) -> str:
    """Strip Lyria's per-line '[:] ' markers for readability; keep section tags."""
    if not text:
        return ""
    lines = [ln[4:] if ln.startswith("[:] ") else ln for ln in text.splitlines()]
    return "\n".join(lines).strip()
