# Changelog

All notable changes to the Pika Claude Code plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
