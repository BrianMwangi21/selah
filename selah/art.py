"""Cover art via Nano Banana (Gemini image generation) + a Pillow title layer.

Two steps, on purpose:
  1. render_cover() — Nano Banana paints clean, heavenly gospel art with a calm
     centre (the paid step).
  2. apply_title() — we overlay the song title + the "SELAH" wordmark ourselves
     with Pillow, so typography is pixel-perfect and identical across all 12
     covers (album cohesion). Free and re-runnable — tweak text without paying
     to regenerate the art.

AI image models mangle text, so we never ask the model to render it. Model ID is
env-driven; the API call is isolated here (one-line fix if the surface changes).

NOTE: standalone Imagen was retired (Aug 2026) in favour of Nano Banana."""

from __future__ import annotations

import base64
from pathlib import Path

from selah import config
from selah.storage import Song
from selah.vibes import get_preset

# The shared visual identity — heavenly and worshipful, NOT literal lyric
# metaphors (those made a "broken wall"). Tweak to restyle every cover at once.
ALBUM_STYLE = (
    "Heavenly, worshipful gospel album cover art. Luminous divine light, soft "
    "golden god-rays breaking through clouds, radiant glow, ethereal and "
    "atmospheric, sacred and uplifting, a sense of glory, awe and transcendence. "
    "Cinematic painterly digital art, rich warm light, high detail. Keep the "
    "central area calm and softly lit, with open space for a title. "
    "No text, no words, no lettering, no logos, no watermark."
)


def _cover_prompt(song: Song) -> str:
    # Evoke the theme as *atmosphere*, not literal objects.
    return (
        f"{ALBUM_STYLE} Evoke the feeling of '{song.theme}' through light, sky, "
        f"colour and atmosphere rather than literal objects."
    )


def render_cover(
    song: Song,
    aspect: str | None = None,
    model: str | None = None,
    index: int | None = None,
) -> Path:
    """Generate clean cover art and write it into the song folder.

    index=None -> cover.<ext>; index=N -> cover-N.<ext> (for options).
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
    stem = "cover" if index is None else f"cover-{index}"
    song.dir.mkdir(parents=True, exist_ok=True)
    out = song.dir / f"{stem}.{_image_ext(data)}"
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
    return "png"


# ----------------------------------------------------------------------------
# Title layer (Pillow)
# ----------------------------------------------------------------------------

def apply_title(song: Song, title: str | None = None, artist: str | None = None) -> Path:
    """Overlay the song title + artist wordmark onto the cover. Returns the path
    to cover-titled.jpg. Free and re-runnable — no API call."""
    from PIL import Image, ImageDraw, ImageFilter

    src = _find_cover(song)
    title = (title or song.title or "").strip()
    artist = (artist or config.ARTIST_NAME).strip()

    base = Image.open(src).convert("RGBA")
    W, H = base.size

    # Legibility scrim: a soft dark band across the middle, heavily blurred so
    # its edges melt into the art.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band = int(H * 0.38)
    ImageDraw.Draw(overlay).rectangle(
        [0, (H - band) // 2, W, (H + band) // 2], fill=(0, 0, 0, 135)
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(int(H * 0.05)))
    base = Image.alpha_composite(base, overlay)

    draw = ImageDraw.Draw(base)
    cx = W // 2
    maxw = int(W * 0.84)

    title_font, title_lines = _fit_title(
        title, config.COVER_TITLE_FONT, int(W * 0.105), int(W * 0.05), maxw, draw
    )
    artist_font = _load_font(config.COVER_ARTIST_FONT, int(W * 0.034))
    artist_text = "   ".join(list(artist.upper()))  # letter-spaced wordmark

    def _h(font, sample="Ay"):
        b = font.getbbox(sample)
        return b[3] - b[1]

    th, ah = _h(title_font), _h(artist_font)
    line_gap = int(H * 0.015)
    sec_gap = int(H * 0.022)
    rule_h = max(2, int(H * 0.003))

    block_h = ah + sec_gap + rule_h + sec_gap + len(title_lines) * th + (len(title_lines) - 1) * line_gap
    y = (H - block_h) // 2

    _shadow_text(draw, (cx, y + ah // 2), artist_text, artist_font)
    y += ah + sec_gap

    rule_w = int(W * 0.14)
    draw.rectangle([cx - rule_w // 2, y, cx + rule_w // 2, y + rule_h], fill=(255, 250, 244, 190))
    y += rule_h + sec_gap

    for ln in title_lines:
        _shadow_text(draw, (cx, y + th // 2), ln, title_font)
        y += th + line_gap

    out = song.dir / "cover-titled.jpg"
    base.convert("RGB").save(out, quality=95)
    return out


def _find_cover(song: Song) -> Path:
    for name in ("cover.jpg", "cover.jpeg", "cover.png", "cover.webp"):
        p = song.dir / name
        if p.exists():
            return p
    for p in sorted(song.dir.glob("cover*.*")):
        if "titled" not in p.name and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            return p
    raise FileNotFoundError(
        f"No cover image in {song.dir} — run `selah cover {song.slug}` first."
    )


def _load_font(path: str, size: int):
    from PIL import ImageFont

    candidates = [
        path,
        "/usr/share/fonts/noto/NotoSerif-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _shadow_text(draw, xy, text, font):
    x, y = xy
    for dx, dy in ((-2, 2), (2, 2), (0, 3), (0, 0)):
        fill = (255, 250, 244, 255) if (dx, dy) == (0, 0) else (0, 0, 0, 170)
        draw.text((x + dx, y + dy), text, font=font, fill=fill, anchor="mm")


def _fit_title(text, font_path, start, minsize, maxw, draw):
    """Shrink (and if needed wrap to 2 lines) so the title fits within maxw."""
    size = start
    step = max(2, int(start * 0.06))
    while size >= minsize:
        font = _load_font(font_path, size)
        if draw.textlength(text, font=font) <= maxw:
            return font, [text]
        words = text.split()
        if len(words) > 1:
            best = None
            for i in range(1, len(words)):
                l1, l2 = " ".join(words[:i]), " ".join(words[i:])
                w = max(draw.textlength(l1, font=font), draw.textlength(l2, font=font))
                if best is None or w < best[0]:
                    best = (w, [l1, l2])
            if best and best[0] <= maxw:
                return font, best[1]
        size -= step
    font = _load_font(font_path, minsize)
    words = text.split()
    if len(words) > 1:
        i = len(words) // 2
        return font, [" ".join(words[:i]), " ".join(words[i:])]
    return font, [text]
