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

    # --- lane (gospel by default; the affirmation presets override these) ---
    opener: str = "A gospel worship song."   # first line of the Lyria prompt
    dynamics: str = ""                       # replaces the default anthemic build
    art: str = "gospel"                      # which cover style to paint
    art_scene: str = ""                      # the figure/scene for cosmic covers

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
    # ------------------------------------------------------------------
    # The affirmation lane: intention, manifestation, "I speak, it is done".
    # Not worship songs — first-person affirmations built to be looped.
    # ------------------------------------------------------------------
    "affirmation-soul": Preset(
        key="affirmation-soul",
        name="Affirmation Soul",
        feel="Warm neo-soul affirmations · 78-88 BPM head-nod",
        genre="neo-soul and contemporary R&B affirmation song, warm and confident",
        bpm="laid-back 78-88 BPM head-nod groove",
        tonality="warm, sunny major-seventh and ninth chords, smooth and unhurried",
        instrumentation=(
            "Rhodes electric piano, round sub bass, soft crisp drums with finger "
            "snaps, muted clean guitar licks, a light vinyl warmth"
        ),
        vocals=(
            "smooth, confident female lead, close and conversational, with stacked "
            "harmonies answering her on the hook"
        ),
        production="clean, warm, intimate modern R&B mix; the vocal sits right up front",
        arrangement=(
            "the voice comes in almost immediately, an easy verse, then a hook that "
            "repeats like an affirmation, a stripped-back bridge, and the hook again"
        ),
        lyric_voice="first person, present tense, calm certainty; statements, never requests",
        lyric_themes="the power of your own word, self-belief, intention, abundance, alignment, self-worth",
        lyric_imagery="morning light, mirrors, open doors, seeds and harvest, a steady voice, things arriving on time",
        lyric_devices="'I am' and 'I speak' statements, a short hook that works as a daily affirmation, echoed lines",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
        opener=(
            "An uplifting affirmation song about intention and self-belief — "
            "spiritual but not religious, with no church or worship language."
        ),
        dynamics=(
            " Begin singing within the first ten seconds — no long instrumental "
            "intro. Keep the groove relaxed and steady: an easy verse, a warm, "
            "confident hook, a stripped-back bridge. On the final chorus settle "
            "into a vamp (repeat one short affirmation with layered harmonies), "
            "then land a clear, resolved ending (do not cut off abruptly)."
        ),
        art="cosmic",
        art_scene=(
            "A single figure standing calm and upright, one hand lifted, with "
            "warm golden light streaming from their open palm up into the stars."
        ),
    ),
    "cosmic": Preset(
        key="cosmic",
        name="Cosmic",
        feel="Electrifying synth-pop · 'written in the stars' · 120-126 BPM",
        genre="euphoric, high-energy synth-pop and electro-pop, cosmic and electrifying",
        bpm="driving, danceable 120-126 BPM with a four-on-the-floor pulse",
        tonality="bright, soaring major with wide open chords and a big sense of lift",
        instrumentation=(
            "bright arpeggiated synths, a punchy driving synth bass, big "
            "four-on-the-floor electronic drums with claps, wide shimmering pads, "
            "sparkling bell tones, rising sweeps into each chorus"
        ),
        vocals=(
            "powerful, clear lead vocal full of conviction, big stacked harmonies "
            "and gang vocals that explode on the chorus"
        ),
        production="huge, glossy and wide; punchy low end, sparkling top, festival-sized energy",
        arrangement=(
            "the voice enters early over a pulsing bass, tension builds into a "
            "chorus that explodes, a breakdown bridge that drops out and rebuilds, "
            "then the chorus returns even bigger"
        ),
        lyric_voice="first person, wonder mixed with certainty; destiny as something already set in motion",
        lyric_themes="destiny, alignment, timing, being guided, what is meant for you arriving, trust in the unseen",
        lyric_imagery="stars and constellations, orbits, the moon and tides, maps of light, gravity, the night sky",
        lyric_devices="a short celestial hook, repeated affirmations, simple declarative lines",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
        opener=(
            "An uplifting song about destiny, intention and manifestation — "
            "spiritual but not religious, with no church or worship language."
        ),
        dynamics=(
            " Begin singing within the first ten seconds — no long instrumental "
            "intro. Keep the verse tight and pulsing, build tension into a chorus "
            "that explodes with full energy, drop the bridge down and rebuild it. "
            "On the final chorus break into a vamp (repeat one short phrase with "
            "rising intensity), then land a clear, resolved ending (do not cut "
            "off abruptly)."
        ),
        art="cosmic",
        art_scene=(
            "A single figure standing tall with arms thrown wide and head tilted "
            "back, seen from behind, electric with energy, as bright stars snap "
            "into dramatic lines and streaks of light overhead. Dynamic and "
            "triumphant, not calm."
        ),
    ),
    "mantra": Preset(
        key="mantra",
        name="Mantra",
        feel="Slow hypnotic chant · one phrase that builds · 66-72 BPM",
        genre="hypnotic mantra song, meditative chant with a gentle pulse",
        bpm="slow, steady 66-72 BPM",
        tonality="grounded and warm, built on a sustained drone with simple, circling chords",
        instrumentation=(
            "a low sustained drone, soft hand drum and shaker, warm harmonium-like "
            "pad, gentle plucked strings, singing bowl accents"
        ),
        vocals=(
            "a calm lead voice joined by a small group of voices chanting together, "
            "more layers added each time the phrase returns"
        ),
        production="earthy, close and warm; hypnotic and unhurried, with natural room sound",
        arrangement=(
            "the chant begins almost immediately, a short spoken-sung verse, then "
            "the chanted phrase returns again and again with more voices each time"
        ),
        lyric_voice="first person, present tense, simple and absolute; words meant to be repeated",
        lyric_themes="the spoken word becoming real, intention, calm power, belief, being settled",
        lyric_imagery="breath, the tongue, seeds, roots, water finding its way, a flame held steady",
        lyric_devices="one short mantra repeated many times, very few words, call and echo between lead and group",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
        opener=(
            "A meditative mantra song about intention and the power of the spoken "
            "word — spiritual but not religious, with no church or worship language."
        ),
        dynamics=(
            " Begin singing within the first ten seconds — no long instrumental "
            "intro. Keep it hypnotic and even; it grows only by adding voices and "
            "layers, never by getting loud or fast. On the final chorus let the "
            "mantra repeat with every voice joined, then land a clear, settled "
            "ending (do not cut off abruptly)."
        ),
        art="cosmic",
        art_scene=(
            "A small circle of seated figures around a low, steady flame, seen "
            "from a distance, with rings of light rippling outward from them "
            "into the night sky."
        ),
    ),
    "meditation": Preset(
        key="meditation",
        name="Meditation",
        feel="Ambient, sparse and still · soft voice · 58-64 BPM",
        genre="ambient meditation song, soft and spacious",
        bpm="very slow 58-64 BPM with a barely-there pulse",
        tonality="soft, open and consonant; slow-moving chords that never rush to resolve",
        instrumentation=(
            "warm ambient pads, soft felt piano, singing bowls, a distant airy "
            "texture, no drums or only the faintest pulse"
        ),
        vocals=(
            "a gentle, breathy, close-mic voice, almost a whisper, with a soft "
            "halo of harmony; long pauses between lines"
        ),
        production="deep, spacious and quiet; long reverb tails, nothing sharp or sudden",
        arrangement=(
            "the voice enters early and softly, sparse lines with room to breathe, "
            "a chorus that is a gentle return rather than a lift"
        ),
        lyric_voice="first person, present tense, slow and reassuring; very few words",
        lyric_themes="stillness, intention, breath, trust, releasing, receiving, being exactly where you should be",
        lyric_imagery="breath, still water, soft light, open hands, night sky, a slow tide",
        lyric_devices="short affirmations with space around them, gentle repetition, simple words",
        structure="One Verse, Chorus, Bridge, Chorus, Chorus — a single verse, then the chorus, a bridge, then the chorus twice to close. No second verse; keep it lean so a ~3-minute song breathes.",
        opener=(
            "A calm meditation song of affirmations and intention — spiritual but "
            "not religious, with no church or worship language."
        ),
        dynamics=(
            " Begin singing within the first fifteen seconds. Keep it calm and "
            "even from start to finish — no big build, no drums crashing in; the "
            "chorus is a gentle return, not a lift. On the final chorus let one "
            "short phrase repeat softly, then fade to a settled, peaceful ending "
            "(do not cut off abruptly)."
        ),
        art="cosmic",
        art_scene=(
            "A lone figure seated in stillness at the edge of perfectly still "
            "water that mirrors the stars, soft and quiet, with a large gentle moon."
        ),
    ),
}


def get_preset(key: str) -> Preset:
    key = key.lower().strip()
    if key not in PRESETS:
        raise KeyError(key)
    return PRESETS[key]
