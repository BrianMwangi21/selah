"""Cover art via Nano Banana (Gemini image generation, Interactions API).

One cohesive album aesthetic across every track (so the channel looks like an
album, not a bot) + a per-song scene drawn from the theme and the preset's
imagery bank. Model ID is env-driven, and the API call is isolated here — a
rename is a one-line config fix, not a code change.

NOTE: the standalone Imagen API was retired (Aug 2026) in favour of Nano Banana;
this stage targets the Gemini image models."""

from __future__ import annotations

import base64
from pathlib import Path

from selah import config
from selah.storage import Song
from selah.vibes import get_preset

# The shared visual identity. Tweak this to restyle every cover at once.
ALBUM_STYLE = (
    "Cinematic painterly digital artwork for a gospel worship single cover. "
    "Rich atmospheric natural light, warm and reverent mood, evocative and "
    "slightly abstract, dramatic lighting, gallery-quality, cohesive album "
    "aesthetic. No text, no words, no lettering, no logos, no watermark."
)


def _cover_prompt(song: Song) -> str:
    try:
        preset = get_preset(song.preset) if song.preset else None
    except KeyError:
        preset = None

    parts = [ALBUM_STYLE, f"Theme: '{song.theme}'."]
    if song.title:
        parts.append(f"Evoking the song '{song.title}'.")
    if preset:
        parts.append(f"Visual motifs to draw from: {preset.lyric_imagery}.")
        parts.append(f"Overall mood: {preset.feel}.")
    return " ".join(parts)


def render_cover(
    song: Song,
    aspect: str | None = None,
    model: str | None = None,
    index: int | None = None,
) -> Path:
    """Generate a cover image and write it into the song folder.

    index=None -> cover.png; index=N -> cover-N.png (for generating options).
    Returns the path to the written PNG.
    """
    client = config.get_client()
    model = model or config.IMAGE_MODEL
    aspect = aspect or config.COVER_ASPECT

    response_format: dict = {"type": "image", "aspect_ratio": aspect}
    if config.COVER_SIZE:
        response_format["image_size"] = config.COVER_SIZE

    interaction = client.interactions.create(
        model=model,
        input=_cover_prompt(song),
        response_format=response_format,
    )

    image = getattr(interaction, "output_image", None)
    if image is None or not getattr(image, "data", None):
        raise RuntimeError(
            "Nano Banana returned no image. The Interactions API shape may have "
            "changed — check selah/art.py against the current docs."
        )

    data = base64.b64decode(image.data)
    ext = _image_ext(data)
    stem = "cover" if index is None else f"cover-{index}"
    song.dir.mkdir(parents=True, exist_ok=True)
    out = song.dir / f"{stem}.{ext}"
    out.write_bytes(data)
    return out


def _image_ext(data: bytes) -> str:
    """Pick the right extension by sniffing the image's magic bytes."""
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return "png"  # sensible fallback
