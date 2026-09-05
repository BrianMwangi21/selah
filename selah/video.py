"""Video assembly: titled cover + audio -> MP4 with a slow Ken Burns zoom.

Pure ffmpeg, no API and no spend. Takes the finished cover (prefers the titled
one) and the song's audio and produces a YouTube-ready MP4."""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from selah.storage import Song


def render_video(
    song: Song,
    square: bool = False,
    fps: int = 25,
    zoom: float = 0.18,
) -> Path:
    """Assemble cover + song into an MP4 with a gentle Ken Burns zoom.

    square=True renders 1080x1080 (full cover); otherwise 1920x1080 (16:9).
    Returns the path to the written MP4.
    """
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg/ffprobe not found on PATH. Install ffmpeg.")

    cover = _find_cover(song)
    audio = song.dir / "song.mp3"
    if not audio.exists():
        raise FileNotFoundError(
            f"No song audio at {audio}. Render it first:  selah render {song.slug}"
        )

    dur = _audio_duration(audio)
    frames = max(1, math.ceil(dur * fps))
    W, H = (1080, 1080) if square else (1920, 1080)

    # Upscale the still before zoompan — a larger canvas kills the sub-pixel
    # jitter zoompan is infamous for on a static image.
    base = max(W, H) * 2
    z_max = 1.0 + zoom
    z_inc = zoom / frames

    vf = (
        f"[0:v]scale={base}:{base}:force_original_aspect_ratio=increase,setsar=1,"
        f"zoompan=z='min(zoom+{z_inc:.8f}\\,{z_max:.4f})':d={frames}:fps={fps}:"
        f"s={W}x{H}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v]"
    )

    out = song.dir / "video.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", str(fps), "-i", str(cover),
        "-i", str(audio),
        "-filter_complex", vf,
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-r", str(fps),
        # Pin the length to the audio: zoompan + -loop can overrun -shortest.
        "-t", f"{dur:.3f}", "-shortest",
        str(out),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-8:])
        raise RuntimeError(f"ffmpeg failed:\n{tail}")
    return out


def _find_cover(song: Song) -> Path:
    for name in ("cover-titled.jpg", "cover.jpg", "cover.jpeg", "cover.png", "cover.webp"):
        p = song.dir / name
        if p.exists():
            return p
    raise FileNotFoundError(
        f"No cover image in {song.dir} — run `selah cover {song.slug}` first."
    )


def _audio_duration(audio: Path) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nokey=1:noprint_wrappers=1", str(audio)],
        capture_output=True, text=True,
    )
    try:
        return float(proc.stdout.strip())
    except ValueError:
        raise RuntimeError(f"Could not read audio duration from {audio}")
