"""Presets: detailed, multi-dimensional fingerprints. Each carries a *musical*
spec (for Lyria) and a *lyrical* brief (for Gemini). AIs reward specifics —
so every field is concrete: real BPM, named instruments, vocal arrangement,
production character. Tune freely once you hear real output; this is the ear."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    key: str
    name: str
    feel: str            # one-line label for tables

    # --- musical spec (assembled into the Lyria prompt) ---
    genre: str
    bpm: str
    tonality: str
    instrumentation: str
    vocals: str
    production: str
    arrangement: str

    # --- lyrical brief (fed to Gemini) ---
    lyric_voice: str
    lyric_themes: str
    lyric_imagery: str
    lyric_devices: str
    structure: str

    def music_prompt(self) -> str:
        """Dense, comma-rich style descriptor for the music model."""
        return (
            f"Genre: {self.genre}. "
            f"Tempo: {self.bpm}. "
            f"Tonality: {self.tonality}. "
            f"Instrumentation: {self.instrumentation}. "
            f"Vocals: {self.vocals}. "
            f"Production: {self.production}. "
            f"Arrangement/dynamics: {self.arrangement}."
        )

    def lyric_brief(self) -> str:
        return (
            f"Voice & tone: {self.lyric_voice}\n"
            f"Themes: {self.lyric_themes}\n"
            f"Imagery bank to draw from (don't force all of it): {self.lyric_imagery}\n"
            f"Lyrical devices: {self.lyric_devices}\n"
            f"Suggested structure: {self.structure}"
        )


PRESETS: dict[str, Preset] = {
    "elevation": Preset(
        key="elevation",
        name="Elevation Worship",
        feel="Anthemic arena worship · builds 70→136 BPM",
        genre="modern anthemic worship, arena/stadium worship-rock, contemporary praise",
        bpm="half-time anthem around 70-76 BPM that opens up to a driving 132-138 BPM feel in the final choruses",
        tonality="bright, hopeful major key; verses may sit in the relative minor and resolve up into the chorus; big IV-I lifts",
        instrumentation=(
            "prominent, driving live drums up front — strong backbeat, powerful "
            "kick and snare, big climbing tom-fills that build into the choruses; "
            "layered ambient electric guitars with heavy delay and reverb swells, "
            "warm analog synth pads, grand piano, deep sub bass, subtle electronic "
            "programming"
        ),
        vocals=(
            "confident male worship-leader lead, huge mixed-gender congregational "
            "gang vocals on the chorus, spontaneous shouted response layers, wide "
            "unison stacks with octave doubling"
        ),
        production=(
            "polished radio-worship master, wide stereo image, big cinematic reverb, "
            "sidechained swells, dramatic dynamic range from intimate to explosive"
        ),
        arrangement=(
            "intimate verse, enormous chorus, a stripped-back "
            "moment where the drums pull right back, then a spontaneous shout-it "
            "bridge that builds the drums back up, slamming into a final chorus "
            "with the full kit"
        ),
        lyric_voice="first-person testimony blended with corporate 'we'; declarative, present-tense faith stated as fact; urgent and hopeful, never cheesy",
        lyric_themes="victory over the grave, breakthrough, God's faithfulness and promises, freedom from shame, resurrection power",
        lyric_imagery="graves into gardens, walls falling, dead things rising, chains breaking, raging rivers, dawn tearing the dark, debt/courtroom cancelled",
        lyric_devices="short shout-able declarative hooks, anaphora ('There is no…'), call-and-response bridge, the name of Jesus landing as the climax",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
    "maverick-city": Preset(
        key="maverick-city",
        name="Maverick City Music",
        feel="Raw collective gospel-worship · 68-92 BPM soul groove",
        genre="gospel-worship fusion, spontaneous collective worship, soul-gospel",
        bpm="unhurried 68-92 BPM, pocket groove, often long and meditative with an extended vamp",
        tonality="warm gospel harmony with extended chords (maj7, 9ths, passing diminished), soulful and slightly loose",
        instrumentation=(
            "Rhodes and Wurlitzer electric pianos, Hammond B3 organ, gospel grand "
            "piano, live drums sitting deep in the pocket, upright/electric bass, "
            "hand percussion, subtle warm strings; organic live-room sound"
        ),
        vocals=(
            "multiple lead vocalists (male and female) trading lines, rich gospel "
            "choir stacks, soulful improvised runs and ad-libs, congregational "
            "responses, raw and emotional live energy"
        ),
        production=(
            "organic and intentionally raw, audible room ambience, warm analog "
            "character, wide dynamic range, feels captured live rather than polished"
        ),
        arrangement=(
            "conversational verse, communal chorus, then a long spontaneous vamp/tag "
            "that builds with choir, ad-libs and rising intensity"
        ),
        lyric_voice="intimate, honest, conversational; communal; vulnerable testimony that turns into corporate praise — favor the process of trusting God over triumphant declaration",
        lyric_themes="God's faithfulness in the waiting, kept promises, His presence in pain, surrender, deep gratitude",
        lyric_imagery="promises, morning coming after night, the wait, 'still' and 'again', mountains and valleys, family and the table",
        lyric_devices="call-and-response between a lead and the choir (mark lines (Lead)/(Choir)/(All)), gentle spontaneous repetition, plainspoken-yet-poetic lines, an extended vamp/tag that grows with ad-libs and choir hits",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
    "bethel": Preset(
        key="bethel",
        name="Bethel Music",
        feel="Intimate atmospheric worship · 62-74 BPM, spacious",
        genre="intimate atmospheric worship, ambient worship ballad, prophetic worship",
        bpm="slow and spacious 62-74 BPM with a gentle, patient build",
        tonality="tender major with suspended chords and unresolved suspensions that create longing; dreamy and open",
        instrumentation=(
            "reverb-drenched ambient electric guitar swells, soft felt piano, warm "
            "analog synth pads, atmospheric textures, brushed/soft drums entering "
            "late, minimal rounded bass"
        ),
        vocals=(
            "intimate singer-songwriter lead (male or female), breathy close-mic "
            "delivery, soft layered harmonies, understated — building to full but "
            "never shouty"
        ),
        production=(
            "spacious and ethereal, generous reverb and delay, wide ambient bed, "
            "cinematic-but-soft, dynamics from a whisper to a warm swell"
        ),
        arrangement=(
            "sparse intro, tender verse, warm chorus, a second "
            "build, a prophetic building bridge, then a resolving final chorus"
        ),
        lyric_voice="personal devotional 'You and me' intimacy with God; tender, awe-filled, first-person",
        lyric_themes="the kindness and goodness of God, rest, being found and pursued, wonder, surrender, overwhelming love",
        lyric_imagery="oceans and deep waters, relentless pursuit, wilderness, morning, kindness, breath, coming home",
        lyric_devices="poetic image-rich lines, quiet repetition, a bridge refrain that builds, tender confession",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
    "hillsong": Preset(
        key="hillsong",
        name="Hillsong Worship",
        feel="Cinematic arena worship · lush & polished",
        genre="cinematic arena pop-rock worship, congregational anthem",
        bpm="anthemic 68-74 BPM ballad feel, or up to ~120 BPM on driving songs; polished pop-rock",
        tonality="grand, lush major; cinematic uplifting resolves; strong, singable melodic contour",
        instrumentation=(
            "lush layered production, full live band, driving reverb-washed electric "
            "guitars, grand piano, sweeping orchestral strings, synth pads, powerful "
            "arena drums, wide electric bass"
        ),
        vocals=(
            "strong lead vocal (male or female), massive congregational choir, "
            "polished stacked harmonies, anthemic unison lines built for global "
            "congregational singing"
        ),
        production=(
            "highly polished and radio-ready, cinematic, wide and glossy mix, big "
            "reverb, professional master"
        ),
        arrangement=(
            "intro, verse, soaring chorus, verse, chorus, an epic bridge "
            "that is the emotional peak, then a final chorus"
        ),
        lyric_voice="grand, reverent adoration; majestic corporate worship — centered on who God is and what He has done, not on personal testimony",
        lyric_themes="the majesty and name of Jesus, the salvation story (creation, cross, resurrection, reign), awe, surrender, His beauty and worth",
        lyric_imagery="the beautiful name, oceans, mountains, the King, cross and empty grave, wonder and majesty",
        lyric_devices="singable global hooks, clear memorable lines, a cyclical building bridge, reverent declaration",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
    "mary-mary": Preset(
        key="mary-mary",
        name="Mary Mary",
        feel="Urban contemporary gospel · 90-110 BPM R&B groove",
        genre="urban contemporary gospel, R&B and hip-hop-influenced gospel",
        bpm="groove-driven 90-110 BPM with hand-clap energy and a contemporary beat",
        tonality="soulful R&B harmony, contemporary chord changes, a funky gospel blend",
        instrumentation=(
            "tight programmed and live drums, groovy electric bass, gospel keys and "
            "Hammond organ, funky electric-guitar licks, punchy horn stabs, hand "
            "claps, hip-hop-influenced production"
        ),
        vocals=(
            "female sister-duo leads with tight harmonies, soulful runs, confident "
            "sassy ad-libs, layered gospel background stacks, radio-ready"
        ),
        production=(
            "modern urban-gospel mix, clean and punchy, groove-forward, polished "
            "radio single"
        ),
        arrangement=(
            "intro hook, verse, hook, verse, hook, bridge, hook out"
        ),
        lyric_voice="encouraging, confident, real-life; streetwise-but-saved; first-person testimony you can relate to",
        lyric_themes="overcoming, God as help through the struggle, joy, gratitude, everyday faith, resilience",
        lyric_imagery="shackles and chains breaking, going through it and coming out, morning after the storm, everyday blessings, getting back up",
        lyric_devices="a catchy hook-first structure, groove-friendly and rhythmic phrasing, sister-duo trade-offs with ad-lib responses (mark asides in parentheses), confident declarations, relatable everyday diction",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
    "ron-kenoly": Preset(
        key="ron-kenoly",
        name="Ron Kenoly",
        feel="90s celebratory praise · 108-135 BPM, live & brassy",
        genre="celebratory 90s corporate praise & worship, live integrity-style praise",
        bpm="uptempo and jubilant 108-135 BPM",
        tonality="bright, triumphant, celebratory major",
        instrumentation=(
            "bright brass-section stabs, full live band, congas and African "
            "percussion, Hammond organ, piano, funky bass; festive, recorded with a "
            "live congregation"
        ),
        vocals=(
            "male worship leader with a full live gospel choir, call-and-response, "
            "congregational shouts, jubilant and celebratory"
        ),
        production=(
            "warm 90s live-album feel, audible congregation, celebratory and "
            "energetic, natural room"
        ),
        arrangement=(
            "intro, verse, celebratory chorus, verse, chorus, a call-and-response "
            "bridge, then a reprise"
        ),
        lyric_voice="exuberant corporate praise and thanksgiving; Scripture-quoting; declarative worship",
        lyric_themes="praise and thanksgiving, the sacrifice of praise, lifting the name of the Lord, victory, God's greatness",
        lyric_imagery="lifting hands and lifting the name, gates and courts, the sacrifice of praise, dancing, Ancient of Days, banners",
        lyric_devices="leader/choir call-and-response (mark lines (Leader)/(Choir)/(Congregation)), congregational shout-backs, direct Scripture quotation (Psalm 100 gates/courts, Isaiah 61 garment of praise, Hebrews 13 'sacrifice of praise'), repeated praise declarations",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
    ),
}


def get_preset(key: str) -> Preset:
    key = key.lower().strip()
    if key not in PRESETS:
        raise KeyError(key)
    return PRESETS[key]
