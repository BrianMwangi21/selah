"""Environment + client wiring. Everything tunable lives in .env."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_LYRICS_MODEL = os.getenv("GEMINI_LYRICS_MODEL", "gemini-3.7-flash")

# Creativity. Higher = wilder/more varied, lower = safer/more predictable.
# Overridable per-run with `selah new --temp`.
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "1.0"))

# Lyria (music). Env-driven so a rename is a one-line fix, not a code change.
LYRIA_MODEL = os.getenv("LYRIA_MODEL", "lyria-3-pro-preview")

# Cover art (Nano Banana / Gemini image generation).
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gemini-3.1-flash-image")
COVER_ASPECT = os.getenv("COVER_ASPECT", "1:1")   # 1:1 album · 16:9 video
COVER_SIZE = os.getenv("COVER_SIZE", "2K")

# Title layer (Pillow overlay).
ARTIST_NAME = os.getenv("ARTIST_NAME", "Selah")
COVER_TITLE_FONT = os.getenv("COVER_TITLE_FONT", "/usr/share/fonts/noto/NotoSerif-Bold.ttf")
COVER_ARTIST_FONT = os.getenv("COVER_ARTIST_FONT", "/usr/share/fonts/liberation/LiberationSans-Bold.ttf")

SONGS_DIR = Path(os.getenv("SONGS_DIR", "songs"))


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


@lru_cache(maxsize=1)
def get_client():
    """Return a configured google-genai client, or raise a friendly error."""
    if not GEMINI_API_KEY:
        raise ConfigError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and paste your key."
        )
    try:
        from google import genai
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "google-genai is not installed. Run:  pip install -e ."
        ) from exc
    return genai.Client(api_key=GEMINI_API_KEY)
