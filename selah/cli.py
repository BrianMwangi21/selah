"""Selah CLI — a pretty, in-the-loop gospel songwriting studio in the terminal."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from selah import config
from selah.vibes import PRESETS, get_preset

app = typer.Typer(
    add_completion=False,
    help="Selah — vibe + theme -> lyrics -> song. A pause where the house listens.",
    rich_markup_mode="rich",
)
console = Console()

ACCENT = "bright_magenta"


def _banner():
    console.print()
    console.print(
        Panel(
            Text("SELAH", style=f"bold {ACCENT}", justify="center"),
            subtitle="[dim]a pause in the music[/dim]",
            border_style=ACCENT,
            padding=(0, 8),
        ),
        justify="center",
    )


def _render_lyrics(title: str, lyrics: str, preset_name: str, theme: str) -> Panel:
    body = Text()
    for line in lyrics.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            body.append(line + "\n", style=f"bold {ACCENT}")
        else:
            body.append(line + "\n")
    return Panel(
        body,
        title=f"[bold]{title}[/bold]",
        subtitle=f"[dim]{preset_name} · {theme}[/dim]",
        border_style=ACCENT,
        padding=(1, 3),
    )


@app.command("presets")
def list_presets():
    """Show the available vibe presets."""
    table = Table(title="Vibe presets", border_style=ACCENT, title_style=f"bold {ACCENT}")
    table.add_column("key", style="bold")
    table.add_column("in the spirit of")
    table.add_column("feel", style="dim")
    for p in PRESETS.values():
        table.add_row(p.key, p.name, p.feel)
    console.print(table)
    console.print("[dim]Full spec for one:[/dim] selah preset <key>")


@app.command("preset")
def preset_detail(key: str):
    """Show the full musical + lyrical spec for one preset."""
    try:
        p = get_preset(key)
    except KeyError:
        console.print(f"[red]Unknown preset '{key}'.[/red] Try: {', '.join(PRESETS)}")
        raise typer.Exit(1)

    music = Text()
    for label, val in [
        ("Genre", p.genre), ("BPM", p.bpm), ("Tonality", p.tonality),
        ("Instruments", p.instrumentation), ("Vocals", p.vocals),
        ("Production", p.production), ("Arrangement", p.arrangement),
    ]:
        music.append(f"{label}: ", style=f"bold {ACCENT}")
        music.append(val + "\n\n")

    lyric = Text()
    for label, val in [
        ("Voice", p.lyric_voice), ("Themes", p.lyric_themes),
        ("Imagery", p.lyric_imagery), ("Devices", p.lyric_devices),
        ("Structure", p.structure),
    ]:
        lyric.append(f"{label}: ", style=f"bold {ACCENT}")
        lyric.append(val + "\n\n")

    console.print(Panel(music, title=f"[bold]{p.name}[/bold] — music (→ Lyria)", border_style=ACCENT, padding=(1, 2)))
    console.print(Panel(lyric, title=f"[bold]{p.name}[/bold] — lyrics (→ Gemini)", border_style=ACCENT, padding=(1, 2)))


@app.command("new")
def new(
    preset: str = typer.Option(..., "--preset", "-p", help="Vibe preset (see `selah presets`)."),
    theme: str = typer.Option(..., "--theme", "-t", help="Core element, e.g. 'grace', 'the prodigal'."),
    temp: float = typer.Option(
        config.GEMINI_TEMPERATURE, "--temp", min=0.0, max=2.0,
        help="Creativity 0-2. Higher = wilder/more varied for experimentation.",
    ),
):
    """Draft lyrics from a vibe + theme, tweak with notes, then save."""
    from selah import lyrics as lyricgen
    from selah.storage import Song

    try:
        pre = get_preset(preset)
    except KeyError:
        console.print(f"[red]Unknown preset '{preset}'.[/red] Try: {', '.join(PRESETS)}")
        raise typer.Exit(1)

    _banner()
    console.print(
        f"[dim]Writing in the spirit of[/dim] [bold]{pre.name}[/bold] "
        f"[dim]on[/dim] [bold]{theme}[/bold] [dim](temp {temp})[/dim]\n"
    )

    try:
        with console.status("[bold]Summoning the first draft…[/bold]", spinner="dots"):
            sheet = lyricgen.draft(pre, theme, temperature=temp)
    except config.ConfigError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    # The tweak loop.
    while True:
        console.print(_render_lyrics(sheet.title, sheet.lyrics, pre.name, theme))
        console.print(
            f"[dim]  [{ACCENT}]a[/{ACCENT}]ccept · "
            f"[{ACCENT}]n[/{ACCENT}]otes (regenerate) · "
            f"[{ACCENT}]t[/{ACCENT}]itle · "
            f"[{ACCENT}]q[/{ACCENT}]uit[/dim]"
        )
        choice = Prompt.ask("», choose", choices=["a", "n", "t", "q"], default="a")

        if choice == "a":
            song = Song(title=sheet.title, preset=pre.key, theme=theme, lyrics=sheet.lyrics)
            path = song.save()
            console.print(f"\n[green]✓ Saved[/green] [bold]{song.title}[/bold] → [dim]{path}[/dim]")
            console.print(f"[dim]  render audio later with:[/dim] selah render {song.slug}\n")
            return
        if choice == "q":
            console.print("[dim]Nothing saved.[/dim]")
            raise typer.Exit()
        if choice == "t":
            sheet.title = Prompt.ask("new title", default=sheet.title)
            continue
        if choice == "n":
            notes = Prompt.ask("what should change?")
            with console.status("[bold]Reworking…[/bold]", spinner="dots"):
                sheet = lyricgen.regenerate(pre, theme, sheet.lyrics, notes, temperature=temp)


@app.command("list")
def list_songs():
    """List all songs written so far."""
    from selah.storage import all_songs

    songs = all_songs()
    if not songs:
        console.print("[dim]No songs yet. Start one with:[/dim] selah new -p elevation -t grace")
        return
    table = Table(title="Songs", border_style=ACCENT, title_style=f"bold {ACCENT}")
    table.add_column("slug", style="bold")
    table.add_column("title")
    table.add_column("preset", style="dim")
    table.add_column("theme", style="dim")
    table.add_column("status")
    for s in songs:
        color = {"draft": "yellow", "approved": "cyan", "rendered": "green"}.get(s.status, "white")
        table.add_row(s.slug, s.title, s.preset, s.theme, f"[{color}]{s.status}[/{color}]")
    console.print(table)


@app.command("show")
def show(slug: str):
    """Print a song's lyrics."""
    from selah.storage import load

    try:
        song = load(slug)
    except FileNotFoundError:
        console.print(f"[red]No song '{slug}'.[/red] See `selah list`.")
        raise typer.Exit(1)
    console.print(_render_lyrics(song.title, song.lyrics, song.preset, song.theme))


@app.command("render")
def render(
    slug: str,
    full: bool = typer.Option(False, "--full", help="Render the full song instead of a short preview clip."),
):
    """Generate audio for a saved song with Lyria."""
    from selah import music
    from selah.storage import load

    try:
        song = load(slug)
    except FileNotFoundError:
        console.print(f"[red]No song '{slug}'.[/red] See `selah list`.")
        raise typer.Exit(1)

    kind = "full song" if full else "preview clip"
    try:
        with console.status(f"[bold]Lyria is singing the {kind}…[/bold]", spinner="dots"):
            out = music.render(song, preview=not full)
    except config.ConfigError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
    except Exception as e:  # surface Lyria API surprises clearly
        console.print(f"[red]Lyria call failed:[/red] {e}")
        raise typer.Exit(1)
    console.print(f"[green]✓ {kind.capitalize()} written →[/green] [dim]{out}[/dim]")


if __name__ == "__main__":
    app()
