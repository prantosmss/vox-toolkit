# Instructions for the agent

Read this file fully before doing anything, and follow it for the whole project.

## First-run setup (do this once, then never again)
Future agents start with no memory of this file, so the first agent to read it must leave a pointer behind.
1. Open AGENTS.md and CLAUDE.md in the project root. Check each file for the marker `<!-- VOX-TOOLKIT-POINTER -->`.
2. If a file already contains the marker, do nothing to it. The setup is done.
3. If a file does not contain the marker, APPEND (never edit or delete existing text) this block at the very end of that file:

```
<!-- VOX-TOOLKIT-POINTER -->
## Vox documentary toolkit
Before starting any work in this project, read instructions.md in the project root and follow it for the whole task.
<!-- /VOX-TOOLKIT-POINTER -->
```

4. This one append is the only change you are ever allowed to make to AGENTS.md and CLAUDE.md. After the marker exists, never modify those files again.

## Goal
Create a Vox-style documentary animation in HyperFrames using the attached voiceover audio. Build chapters from script.md. Do NOT use HeyGen generation to create images, video or audio. All visuals must be fetched from real sources using the scripts in scripts/.

## What Vox style means
Use this as the visual and audio brief for every video.
- Look: clean explainer design on a light or muted background, one idea per scene, generous empty space. Restraint is the style, so use a small fixed set of effects and repeat them for the whole video.
- Cutouts: people and objects appear as paper cutouts with a white torn edge, soft shadow, slight tilt, and a slow push-in. Stills are never static: add slow zooms and pans.
- Screenshots: article and newspaper screenshots are shown on screen with the key sentence highlighted in yellow, then zoomed into it.
- Text: bold kinetic type for key numbers and names, simple lower thirds, charts and maps that build up piece by piece.
- Motion: transitions are smooth camera-style moves with a touch of blur, paper slides, or shapes that carry the eye from one scene to the next. No flashy effects.
- Pace: change the visual roughly every 3 to 6 seconds, matched to the narration. Cut on the beat of the music where possible.
- Audio: the voiceover is the star. Music sits low and ducks under the voice, and changes about every 20 seconds or at a chapter change. Sound effects are small and tactile: paper shuffles, stamps, typewriter clicks, soft whooshes on transitions. Leave a moment of near silence before an important line.
- Tone: conversational, written to be spoken.

## Audio sources and rules
- Sound effects: run scripts/fetch_audio.py sfx "search phrase". It uses Freesound (needs FREESOUND_API_KEY in .env) and accepts only CC0 and CC BY sounds. Log the license, and add CC BY credit lines to the end credits.
- Music: there is no reliable free music API here. Use royalty-free tracks the user places in assets/music/. If that folder is empty, ask the user for tracks and suggest Pixabay Music or the YouTube Audio Library. Never download copyrighted music.
- Keep sound effects very quiet (about 15 to 25 percent of the voice level) and music lower than that. Duck music under the voiceover.
- Use SFX only at: chapter reveals, screenshot and cutout entrances, and key number reveals. Do not put an effect on every cut.

## Inputs
- The attached voiceover audio file (use it for timing).
- script.md: the voiceover text with visual cues in square brackets.
- .env: holds API keys. Never print, log, commit or zip it.

## Process
1. Transcribe or align the voiceover audio so every script.md line has a start and end time.
2. Split script.md into chapters using the lines that start with `## Chapter`.
3. Parse every visual cue. A cue looks like `[TYPE: search phrase | option=value]`.
4. For each cue, run the matching script from scripts/ (or run scripts/fetch_all.py script.md to do them all). Files go in assets/ and every file is logged in assets/manifest.json with source URL and license.
5. If a fetch fails or returns nothing good, try a better search phrase, then the fallback source. Report anything still missing instead of inventing a replacement.
6. Build the HyperFrames composition: one scene per cue, timed to the audio, Vox-style (clean explainer look, kinetic text, slow push-ins on stills, highlighted screenshot text, bold lower thirds).
7. Apply the chapter transition rules below at every chapter boundary.
8. Add credits from manifest.json at the end.

## Chapter transitions
At every boundary between two chapters:
- Cut the voiceover audio. Split the audio at the exact moment the last word of the old chapter ends, and start the next chapter's audio only after the reveal below finishes. Leave a short beat of silence (about 1 second) before the reveal.
- Insert a chapter reveal section between the chapters, about 3 to 5 seconds long. It shows a bold title card with the chapter number and the chapter title (taken from the `## Chapter N: Title` line), animated in Vox style (kinetic type, clean background, a subtle sound sting or whoosh if one is available in the project).
- If a CHAPTER cue sits right under the chapter heading in script.md, use its title and subtitle text for the reveal instead of the heading text.
- The first chapter also gets a reveal, right after the opening hook if script.md has one, otherwise at the very start.
- Keep the audio and visuals in sync: the reveal is extra time added to the video, so shift every later scene by the length of the reveal and the silence beat.
- Log each chapter reveal timing (start, end) in assets/manifest.json under a "chapters" key.

## Cue types
- FOOTAGE: stock video, from Pixabay then Pexels. Script: fetch_stock_video.py
- IMAGE: stock photo, from Pixabay then Pexels. Script: fetch_stock_image.py
- LOGO: company logo, from Wikimedia Commons or the company press kit. Script: fetch_logo.py
- ARTICLE: screenshot of a web article. Script: screenshot.py
- NEWSPAPER: screenshot of a newspaper or archive page. Script: screenshot.py
- PERSON: cutout of a person, a transparent PNG with the background removed. Script: fetch_person.py. In the composition, give cutouts the Vox paper-cutout look: white torn-paper outline, soft drop shadow, slight tilt, slow push-in.
- SFX: optional sound effect on a moment, for example `[SFX: paper shuffle]`. Script: fetch_audio.py sfx
- CHAPTER: optional. Sets the reveal title and subtitle for the chapter it sits under. No script needed, the agent builds it in HyperFrames.

Options: `duration` (seconds of footage wanted), `orientation` (horizontal or vertical), `source` (pixabay, pexels, wikimedia), `selector` (CSS selector to crop a screenshot to), `highlight` (text to highlight in the screenshot), `fullpage` (true or false), `hint` (extra search word for a person), `subtitle` (for CHAPTER).

## Source tiers
Work down the tiers in order and stop at the first good result. Never skip to a lower tier while a higher one still has a usable result.

Tier 1, free API or open license, use first:
- Pixabay and Pexels (stock footage and images, scripts handle these)
- Wikimedia Commons (logos, people, historical images, scripts handle this)
- Public domain archives: Library of Congress, NASA, US government sites, Internet Archive, national archives

Tier 2, free to reuse but needs a per-file license check:
- Flickr Creative Commons search (accept only CC0, CC BY, CC BY-SA, or public domain, never NonCommercial or NoDerivs)
- Unsplash
- Company press kits, newsroom and investor-relations pages (headshots, logos, product photos)
- Official government, university, and organization media pages

Tier 3, use only for commentary, cite the source, flag for review:
- Screenshots of news articles, newspaper archives, and public web pages (use screenshot.py)
- Official social media posts and public video thumbnails, shown as screenshots, not downloaded media
- Wikipedia infobox photos, after checking the file license on Commons

Tier 4, last resort:
- Ask the user to supply the file. Never scrape or download from Getty, Shutterstock, AP, Reuters, Alamy, paywalled sites, or private social profiles.

Catch-all for any source not named above: place it in the lowest tier that matches its license. No clear license means Tier 3 at best, and only as a screenshot. Always write the source URL, license, and tier into assets/manifest.json, and list every Tier 3 item in the credits and in a final report so the user can review it.

If a tier has an API key in .env, use it. If a source needs a new key, do not guess. Add the missing key name to .env.example and tell the user.

## Rules
- Prefer reusable sources (Pixabay, Pexels, Wikimedia Commons, press kits). Log license per file.
- Pixabay has no company logos, so always use LOGO cues for logos.
- Never fabricate a source or license.
- Run every script with the project's .venv Python (.venv/bin/python on Mac and Linux, .venv\Scripts\python on Windows), never the system Python. If .venv does not exist, run python init.py first.
- Never modify AGENTS.md or CLAUDE.md, except for the single one-time pointer append described in First-run setup.
