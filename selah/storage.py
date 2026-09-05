"""Song persistence: one folder per track, songs/<slug>/lyrics.md, with a
small YAML-ish frontmatter block on top. Git-able and eyeball-able."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from slugify import slugify

from selah import config


@dataclass
class Song:
    title: str
    preset: str
    theme: str
    lyrics: str
    slug: str = ""
    status: str = "draft"          # draft -> approved -> rendered
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))

    def __post_init__(self):
        if not self.slug:
            self.slug = slugify(self.title) or slugify(self.theme) or "untitled"

    # --- paths ---
    @property
    def dir(self) -> Path:
        return config.SONGS_DIR / self.slug

    @property
    def lyrics_path(self) -> Path:
        return self.dir / "lyrics.md"

    # --- serialization ---
    def to_markdown(self) -> str:
        fm = [
            "---",
            f"title: {self.title}",
            f"slug: {self.slug}",
            f"preset: {self.preset}",
            f"theme: {self.theme}",
            f"status: {self.status}",
            f"created: {self.created}",
            "---",
            "",
        ]
        return "\n".join(fm) + self.lyrics.rstrip() + "\n"

    def save(self) -> Path:
        # Avoid clobbering a different existing song with the same slug.
        base = self.slug
        i = 2
        while self.dir.exists() and not self.lyrics_path.exists():
            self.slug = f"{base}-{i}"
            i += 1
        self.dir.mkdir(parents=True, exist_ok=True)
        self.lyrics_path.write_text(self.to_markdown(), encoding="utf-8")
        return self.lyrics_path


def load(slug: str) -> Song:
    path = config.SONGS_DIR / slug / "lyrics.md"
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return Song(
        title=meta.get("title", slug),
        preset=meta.get("preset", ""),
        theme=meta.get("theme", ""),
        lyrics=body.strip(),
        slug=meta.get("slug", slug),
        status=meta.get("status", "draft"),
        created=meta.get("created", ""),
    )


def all_songs() -> list[Song]:
    if not config.SONGS_DIR.exists():
        return []
    songs = []
    for d in sorted(config.SONGS_DIR.iterdir()):
        if (d / "lyrics.md").exists():
            songs.append(load(d.name))
    return songs
