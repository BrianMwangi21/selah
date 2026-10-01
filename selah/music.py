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

# The directive is three parts: a lean structure so the song has room to
# breathe, a dynamic arc (presets can swap in their own), and singable lines.
_STRUCTURE = (
    " Create a complete song about 3 minutes long with a lean structure so it can "
    "breathe: one verse, then the chorus, then a bridge, then the chorus twice to "
    "close (no second verse). Give each section an EVEN number of lines — 4 or 6 "
    "for the verse and chorus, 2 or 4 for the bridge, never 5 or an odd count. "
    "Repeat the chorus verbatim every time."
)
_DYNAMICS = (
    " Build the dynamics — a restrained "
    "verse, a big anthemic chorus, a bridge that grows — and on the final chorus "
    "break into a vamp (repeat one short phrase with rising intensity), then land "
    "a clear, resolved ending (do not cut off abruptly)."
)
_SINGABLE = (
    " Keep every line short and "
    "easy to sing — few words per line, a comfortable, even syllable count; never "
    "cram a line so full it becomes a mouthful, especially in the verses."
)
_GOSPEL_OPENER = "A gospel worship song."


def _preset(song: Song):
    try:
        return get_preset(song.preset) if song.preset else None
    except KeyError:
        return None


def _style(song: Song) -> str:
    pre = _preset(song)
    return pre.music_prompt() if pre else "Genre: gospel worship, full arrangement with vocals."


def _opener(song: Song) -> str:
    pre = _preset(song)
    return pre.opener if pre else _GOSPEL_OPENER


def _directive(song: Song) -> str:
    pre = _preset(song)
    dynamics = pre.dynamics if pre and pre.dynamics else _DYNAMICS
    return f"{_STRUCTURE}{dynamics}{_SINGABLE}"


def _music_prompt(song: Song) -> str:
    return (
        f"{_opener(song)} {_style(song)}{_directive(song)} "
        f"Theme: {song.theme}. Sing the following lyrics with the section "
        f"structure exactly as tagged.\n\n{song.lyrics}"
    )


_CREATIVE_DIRECTIVE = (
    " Treat the theme as a spark, not a script — do NOT paraphrase or restate it "
    "line by line. Write like a real songwriter: find your own fresh, concrete "
    "images, an unexpected angle, a specific moment or story that makes the "
    "feeling land. Surprise the listener. Avoid the obvious, on-the-nose phrasing."
)


def _auto_prompt(song: Song) -> str:
    # No preset -> drop the style block entirely and let Lyria pick the sound
    # from the theme alone (a proven mode — some of the strongest tracks).
    style = f"{_style(song)} " if song.preset else ""
    return (
        f"{_opener(song)} {style}Write your own lyrics (do not "
        f"wait for lyrics to be provided): a song inspired by {song.theme}."
        f"{_CREATIVE_DIRECTIVE}{_directive(song)}"
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
