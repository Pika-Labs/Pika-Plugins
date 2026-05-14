# Changelog

All notable changes to the Pika Claude Code plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.2.3] — 2026-05-14

### Added

- **`/pika:kiss-cam`** — Viral fake "in-arena Kiss Cam moment" of any two subjects. Takes two reference photos (any visual style — photoreal human, 3D toy, illustrated avatar — the recipe preserves whichever style each reference uses), generates a spectator-POV phone shot of the Madison Square Garden Jumbotron with the retro red kiss cam graphic + adjacent Knicks vs Bulls scoreboard baked into frame 0 (`gpt-image-2`), then locks that as Kling's first frame for a 15s `kling-v3-omni` clip with the entire decorative UI pixel-static across all 15s — only the two subjects inside the kiss cam panel animate. Native off-screen PA-announcer commentary + packed-arena crowd reaction, no names, no chyron. Kling-only (Seedance's two-stage face-moderation gate rejects every in-arena reaction shot because of the crowd faces). README and plugin manifest updated to **5 curated `/pika:*` slash commands** (was 4).

## [1.2.2] — 2026-05-14

### Fixed

- **`/pika:baseball-trend`** — Fix inverted camera angle on the Step 1 broadcast still. The 1.2.0 release used a bullet-scaffold prompt for Step 1; `gpt-image-2` rendered the camera in the upper deck looking toward the field (with the subject turned around to face it) instead of in the foul-ground photographers' pit looking back at the premium seats. Two iterations tried explicit camera-position anchors in the scaffold without success — the model's "fan at MLB game" training prior kept overriding them. Final fix: revert Step 1 to the pre-refactor **verbatim calibrated prompt block**. The same constraints, expressed as a narrative paragraph instead of a bullet checklist, are weighted differently by `gpt-image-2` and reliably produce the correct broadcast-camera composition. Step 2 scaffold, call params, fallback, engine choice, and failure cheat sheet unchanged.

## [1.2.0] — 2026-05-14

### Added

- **`/pika:baseball-trend`** — Viral ESPN-style 15s behind-home-plate broadcast cutaway. Takes a username + one reference photo, generates a broadcast still (`gpt-image-2`) with a real-looking scorebug + chyron baked into frame 0, then locks that as Kling's first frame for a `kling-v3-omni` 15s clip with native two-announcer commentary that names the user on air. Fixed-recipe trend (Yankees vs Red Sox ALCS Game 3, Fenway Park). Kling-only — Seedance's output-side face-moderation rejects every broadcast cutaway, and Kling correctly gates celebrity references.

### Changed

- README and plugin manifest updated to reflect **4 curated `/pika:*` slash commands** (was 3).

## [1.0.0] — 2026-05-01

Initial public release of the Pika Claude Code plugin at [`Pika-Labs/Pika-Plugins`](https://github.com/Pika-Labs/Pika-Plugins).

### What ships

- **`/pika:podcast`** — Two-host podcast video for any URL or free-form topic. 1-minute, 4 acts × ~15s, native multi-shot Kling Omni dialogue with optional voice cloning for Host A.
- **`/pika:explainer`** — ~60–80s explainer video for any URL (GitHub repo, product page, docs site, blog post). Drives a real browser through the URL with element-targeted zoom, generates an avatar lipsync of the narration, and composites into a 1280×800 macOS Sonoma frame.
- **`/pika:ugc-ads`** — 15s creator-style multi-cut UGC product ad in 9:16 vertical (3:4 optional, seedance only). HOOK + 3 JUMP CUTs + OUTRO with spoken dialogue + native lip-sync on every beat, driven by a 5-act narrative arc (set → name → reveal → twist → punchline). Six category essences (HAUL / APP / FOOD / BEAUTY / FITNESS / TECH) auto-picked from the input URL.
- **42 atomic MCP tools** at [`mcp.pika.me`](https://mcp.pika.me/api/mcp) — generation (image / video / lipsync / music / speech / slide animation), editing (concat / mix / trim / captions / PiP / animate-zoom / browser-frame / beat-sync), capture (website / frame extraction), analysis (media / brief / transcribe), search (music / skill), identity (avatar / voice / persona / memory), persistent assets (Kling element / voice clone), and async (task status / cancel). Full schema at [`tools-manifest.json`](./tools-manifest.json).

### Install paths

Works on every Claude Code surface — CLI and Desktop (macOS / Windows app). The 42 atomic tools also work with any other MCP client (Claude.ai chat connectors, Claude Desktop chat, Cursor, Codex, etc.) at the raw MCP endpoint `https://mcp.pika.me/api/mcp`. See [README — Quickstart](./README.md#quickstart) for the install command per surface.

### License

Apache 2.0 — see [LICENSE](./LICENSE).
