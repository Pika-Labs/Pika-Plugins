# Changelog

All notable changes to the Pika Claude Code plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **Kling re-roll guidance** — `/pika:app-sizzle`, `/pika:baseball-trend`, `/pika:kiss-cam`, `/pika:podcast`, and `/pika:ugc-ads` now document that Kling v3-omni has no seed and that completed quality re-renders must change the payload (prompt, negative prompt, first-frame still, spoken lines, or act wording) instead of submitting identical params that can dedupe back to the same job/asset.

## [1.4.0] — 2026-05-22

### Added — four new curated skills

Production skill count grows from **5 → 9**. All four new skills are MCP-first: they reach for `mcp__plugin_pika_pika__*` tools (App Store fetch, HTML render, image generation, video generation) instead of bundled local helpers, so the install footprint stays at a folder of `SKILL.md` files with no shell scripts.

- **`/pika:app-sizzle`** — Cinematic 1080p iOS app teaser videos built from real App Store screenshots, with a `gpt-image-2` enhancement pass on each selected screen before SeeDance generation. Output is a beat-driven cinematic teaser ending with the brand logo/icon + "COMING SOON" title card. Screens sourced from Pika MCP App Store fetch, a live website (auto-captured), user-supplied files, or URLs. Triggers on "app sizzle", "app teaser", "app promo", "coming soon", etc.
- **`/pika:app-store-screens`** — Generates 5–6 splashy 1290×2796 App Store screenshots in a given brand's aesthetic from a `brand.md`, raw product screenshots, or a public App Store listing fetched through Pika MCP. Story-driven (hook → value → features → proof → close), ready to drop into App Store Connect.
- **`/pika:build-a-brand`** — Full brand identity + multi-page guidelines PDF from any input (an idea, an existing website, a list of reference brands, product photos, or a rebrand request). Covers logo, palette, typography, voice, and brand directions. Pairs with `/pika:founder-product-video` and `/pika:app-store-screens` via shared `brand.md` / `brand.json` kit.
- **`/pika:founder-product-video`** — 65-second founder-style product video from a product URL + user-supplied imagery. Output is a 16:9 1080p MP4 — 4×15s SeeDance acts of a talking founder + 5s branded end card + background music, with real product screenshots shown on the founder's phone in reveal shots (on-screen UI is real, not AI-imagined). Consumes a `build-a-brand` kit.

### Changed

- **Plugin metadata** — README, `marketplace.json`, and all three plugin manifests (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`) now advertise **9 curated skills**; version bumped `1.3.0` → `1.4.0` across all four manifests.
- **`marketplace.json` `skills:` array** — extended from 5 to 9 entries (canonical Anthropic string-array form, stable order: originals first, four new skills appended).
- **Featured workflows table in README** — extended from 5 to 9 rows with input / output / invoke for each new skill, so the table is the single source of truth for the curated surface.

### Notes

- The 58-tool MCP surface (`tools-manifest.json`, 58 canonical primitives + 9 deprecation aliases = 67 entries) is unchanged in this release. Future tool-surface refreshes will ship in their own minor/patch versions.

## [1.3.0] — 2026-05-20

### Repositioned

- **Pika Creative Suite** — README rewritten from "Pikafy your Claude" (Claude-Code-centric) to "Pika Creative Suite — Give any AI agent a face, a voice, and a full creative studio." Reflects the actual product surface: the same MCP, skills, and plugin work natively across Claude Code, Cursor, Codex, and any of 50+ skill-aware agents. The previous hero overstated Claude exclusivity and undersold the cross-agent reality.

### Added — cross-agent distribution

- **`.cursor-plugin/plugin.json`** — native Cursor plugin manifest mirroring the first-party shape used in [`cursor/plugins`](https://github.com/cursor/plugins) (`category`, `tags`, `skills: "./skills/"`). Lets Cursor pick up Pika via its own plugin format.
- **`.codex-plugin/plugin.json`** — native Codex plugin manifest with documented `interface` block (`displayName`, `defaultPrompt` ≤3, `capabilities`, `brandColor`, etc.). Lets Codex CLI pick up Pika via its own plugin format.
- **`marketplace.json` `skills:` array** — explicit `["./skills/<name>", ...]` registry so cross-agent installers (`vercel-labs/skills`, etc.) don't have to walk the filesystem. Canonical string-array form matching [`anthropics/skills`](https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json) and the documented `plugin-manifest.ts` schema.

### Changed

- **MCP tool surface: 42 → 58 atomic primitives + 9 back-compat deprecation aliases** (compounded across pika-mcp-server back-end releases). Net 16 new canonical primitives — most prominently the Sora generative-edit suite collapsed into a single `sora_edit` tool with a `mode` discriminator; the Pika tool family renamed to `pika_scene` / `pika_addition` / `pika_swap` / `pika_effect`; `edit_audio_isolate` → `edit_audio_denoise`; `extract_audio` → `extract_audio_from_video`; Composio integration via `connect_auth` / `connect_discover` / `connect_call`; wave-2 atomics (`analyze_clip_highlights`, `scrape_social`, `scrape_ads`, `web_publish`); and `html_to_pdf`. All old names remain as deprecation aliases — non-breaking for existing skills and prompts.
- **`generate_image`** new fields — `reference_images: string[]` (multi-ref), `mask` (gpt-image-2 inpainting), `watermark` (seedream), `n: 1–10` (batch). Output now includes `urls: string[]`; the singular `reference_image` field remains as a deprecated alias.
- **`generate_video`** new per-provider knobs — kling: `quality_mode` / `image_tail` / `voice_ids` / `kling_model`; pika: `negative_prompt` / `seed` / `pika_model`; veo3: `resolution` / `veo3_model` / `negative_prompt` / `seed`; sora: `sora_model` / `size` / `character_id`; minimax: `minimax_model` / `last_frame_image` / `resolution` / `prompt_optimizer`.
- **Plugin/marketplace descriptions** retired the legacy "Pika-fy your Claude" tagline in favor of "Pika Creative Suite — give any AI agent a face, a voice, and a full creative studio" matching the README hero.
- **Capabilities surface** in the README documented as 11 tool families summing to 58 canonical primitives, with the prefix convention (`mcp__plugin_pika_pika__*` inside Claude Code, agent-defined elsewhere) called out so cross-agent users can name what they see.

### Install paths (new section in README)

Three independent surfaces, equal weight:

1. **MCP** — drop `https://mcp.pika.me/api/mcp` into any MCP-aware client (per-client config shape documented for Claude Code, Cursor, Codex, Claude.ai connectors).
2. **Skills** — `npx skills add Pika-Labs/Pika-Plugins` writes the 5 curated `SKILL.md` files to whichever agent the [`vercel-labs/skills` CLI](https://github.com/vercel-labs/skills) detects on your machine.
3. **Claude plugin** — `claude plugin marketplace add Pika-Labs/Pika-Plugins` + `/plugin install pika@pika-plugins` for the Claude-native install with bundled MCP wiring.

### Fixed

- **README Cursor `mcp.json` snippet** previously included an unverified `"transport": "http"` field. Cursor's [official docs](https://cursor.com/docs/context/mcp) show the bare `url` form; removed the unverified transport hint.
- **README `npx skills` framing** previously implied multi-agent fan-out by default. Corrected to describe actual flag behavior — default writes to detected agents; `--agent <name>` targets one; `--all` or `--agent '*'` installs to every detected one.
- **License footer** previously said "Built on Anthropic Claude Code"; now says "Speaks the open Model Context Protocol; finishing pipeline built on ffmpeg and Playwright" — reflects that Pika works with any MCP-aware agent, not Claude Code exclusively.

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
