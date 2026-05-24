<h1 align="center">Pika Creative Suite</h1>

<p align="center">
  <b>Give any AI agent a face, a voice, and a full creative studio.</b><br/>
  Image, video, music, editing — one identity, one auth, one bill, across every agent you use.
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/version-v1.4.0-blue" alt="Version"></a>
  <a href="https://mcp.pika.me/api/mcp"><img src="https://img.shields.io/badge/MCP-mcp.pika.me-green" alt="MCP server"></a>
  <a href="./tools-manifest.json"><img src="https://img.shields.io/badge/tools-58_atomic_primitives-purple" alt="Tools"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache_2.0-blue" alt="License"></a>
</p>

```
> /pika:podcast https://pika.art
  scraping page (capture_website)...
  writing 4-act script (Host A · Host B)...
  rendering 4 video acts × ~15s (native multi-shot)...
  done.
View video: https://cdn.pika.art/agent/.../podcast-final.mp4
```

## Three independent ways to install

Pika ships as **three independent surfaces**. Pick one, mix two, or use all three — same Pika Agent identity, same auth, same credit pool across every install.

| Surface | What it gives you | Install mechanism | Works with |
|---|---|---|---|
| **MCP** | 58 atomic creative tools over HTTP MCP with OAuth | Add `https://mcp.pika.me/api/mcp` to any MCP-aware client | Claude Code, Cursor, Codex, Claude Desktop, Claude.ai connectors, any custom MCP agent |
| **Skills** | 9 curated `/pika:*` workflows + MCP wiring | `npx skills add Pika-Labs/Pika-Plugins` | Any skill-aware agent — Claude Code, Cursor, Codex, OpenCode, Cline, plus 50+ more auto-detected by [`vercel-labs/skills`](https://github.com/vercel-labs/skills) |
| **Claude plugin** | Same 9 skills bundled as a Claude Code-native plugin | `claude plugin marketplace add Pika-Labs/Pika-Plugins` | Claude Code only (marketplace + `/plugin` commands) |

These aren't tiers — they're orthogonal mechanisms. A Claude Code user can pick the plugin, the skills, or just the raw MCP. A Cursor user picks skills + MCP. A custom agent picks just MCP.

## Install

### 1. MCP — just the 58 atomic tools

The lightest install. No skill files written to disk. OAuth handles auth automatically on first tool call. Each client expects a slightly different shape — pick the one for your tool:

**Claude Code / Claude Desktop** — `.mcp.json`:

```json
{ "mcpServers": { "pika": { "type": "http", "url": "https://mcp.pika.me/api/mcp" } } }
```

CLI equivalent: `claude mcp add --transport http pika https://mcp.pika.me/api/mcp`.

**Cursor** — `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project). Cursor uses bare `url`, no `type` field:

```json
{ "mcpServers": { "pika": { "url": "https://mcp.pika.me/api/mcp" } } }
```

Then `cursor-agent mcp login pika`.

**Codex CLI**:

```bash
codex mcp add pika --url https://mcp.pika.me/api/mcp
```

**Claude.ai connectors** — add the endpoint URL in Settings → Connectors. **Any other MCP client** — follow your client's docs for the config shape; the endpoint is always `https://mcp.pika.me/api/mcp`.

### 2. Skills — 9 curated workflows + MCP wiring

[`vercel-labs/skills`](https://github.com/vercel-labs/skills) detects your installed agents and writes each skill to the right path. Pass `--agent <name>` to target one agent, `--all` to install to every detected one.

```bash
npx skills add Pika-Labs/Pika-Plugins
```

Then add the MCP block from §1 to your agent. The skills assume the MCP server is registered as `pika`.

### 3. Claude plugin — marketplace install

```bash
claude plugin marketplace add Pika-Labs/Pika-Plugins
claude plugin install pika@pika-plugins
```

Full quit + reopen Claude Code, then run `/mcp` and authenticate `pika`. The plugin bundles the same 9 skills as §2 plus the MCP wiring — no separate `claude mcp add`.

<details>
<summary>Claude Code on the web (claude.ai/code)</summary>

Add this to your repo's `.claude/settings.json`, commit, and push — cloud sessions auto-install at startup:

```json
{
  "extraKnownMarketplaces": {
    "pika-plugins": {
      "source": { "source": "github", "repo": "Pika-Labs/Pika-Plugins" }
    }
  },
  "enabledPlugins": {
    "pika@pika-plugins": true
  }
}
```

`mcp.pika.me` isn't in the default Trusted allowlist — switch the environment's network access to **Full**, or use **Custom** with `mcp.pika.me` added. ([Anthropic network access docs](https://code.claude.com/docs/en/claude-code-on-the-web#network-access))

</details>

## Authenticate

One time per install. Inside your agent, run `/mcp`, find `pika`, hit **Authenticate**. Your browser opens to the Pika sign-in page, the token caches locally, the MCP reconnects.

<details>
<summary>Headless / CI / no browser</summary>

Get a developer key (`dk_*`) at [pika.me/dev](https://www.pika.me/dev/) and export it before launching your agent:

```bash
export MCP_AUTH_TOKEN="dk_..."
claude   # or cursor, codex, etc.
```

Don't hard-code the token into `.mcp.json` or any committed file — keep it in shell env or your secret store. Tokens also come in an agent-key flavor for service-to-service automation; same env var.

</details>

<details>
<summary>Troubleshooting</summary>

| Symptom | Fix |
|---|---|
| `401 Unauthorized` on every call | Token expired. Re-run `/mcp` and re-authenticate, or refresh `MCP_AUTH_TOKEN`. |
| Want to switch accounts | Remove `pika` from your client's MCP list (`claude mcp remove pika`, edit `~/.cursor/mcp.json`, `codex mcp remove pika`, …) → re-add and re-authenticate. |
| Browser doesn't open during OAuth | Allow your agent to open default browser, or fall back to the headless token flow above. |
| `mcp list` shows `Disconnected` | Full quit and restart your agent — `.mcp.json` is only loaded at startup. |

</details>

## Featured workflows

Curated `/pika:*` skills (Surfaces §2 and §3) — one prompt to a finished, shareable video. All consume Pika credits.

| Skill | Input | Output | Invoke |
|---|---|---|---|
| **[Podcast](./skills/podcast/SKILL.md)** | URL or free-form topic | 1-minute two-host conversational video, 4 acts × ~15s | `/pika:podcast` |
| **[Explainer](./skills/explainer/SKILL.md)** | Any URL (GitHub, product, docs) | 60–80s browser walkthrough with avatar lipsync | `/pika:explainer` |
| **[UGC Ads](./skills/ugc-ads/SKILL.md)** | Product URL | 15s creator-style multi-cut UGC ad, 9:16 | `/pika:ugc-ads` |
| **[Baseball-Trend](./skills/baseball-trend/SKILL.md)** | Name + photo | 15s ESPN behind-home-plate broadcast cutaway | `/pika:baseball-trend` |
| **[Kiss Cam](./skills/kiss-cam/SKILL.md)** | Two photos | 15s MSG Jumbotron Kiss Cam moment | `/pika:kiss-cam` |
| **[App Sizzle](./skills/app-sizzle/SKILL.md)** | App name or URL (App Store / website / paths) | Cinematic 1080p iOS app teaser video, GPT-image-2-enhanced screens + "COMING SOON" end card | `/pika:app-sizzle` |
| **[App Store Screens](./skills/app-store-screens/SKILL.md)** | `brand.md` + product screenshots, or App Store URL | 5–6 splashy 1290×2796 PNGs ready for App Store Connect (hook → value → features → proof → close) | `/pika:app-store-screens` |
| **[Build a Brand](./skills/build-a-brand/SKILL.md)** | Idea, website, reference brands, or product photos | Full brand identity + multi-page guidelines PDF (logo, palette, type, voice) | `/pika:build-a-brand` |
| **[Founder Product Video](./skills/founder-product-video/SKILL.md)** | Product URL + founder name/photo (+ brand kit) | 65s founder-talking-head 16:9 1080p MP4 — 4×15s SeeDance acts with real product UI on the founder's phone + 5s branded end card | `/pika:founder-product-video` |

Skills activate from natural language too — saying *"make a podcast about https://pika.art"* fires `/pika:podcast` automatically.

## Capabilities — 58 atomic tools

Behind every curated skill is a flat tool surface (Surface §1) you can drive directly. Inside Claude Code the MCP tool prefix is `mcp__plugin_pika_pika__*`; other agents follow their own prefix convention. Counts are canonical primitives only — 9 deprecation aliases ship for back-compat but aren't counted.

| Family | What it covers | Count |
|---|---|---|
| **Generation** | Image, video, lipsync, music, speech, slide animation, motion-control, keyframes, reference video | 9 |
| **Generative video edit** | One multi-mode tool — cut, extend, and remix existing video | 1 |
| **Scene composition** | Multi-character / multi-object scene compose, generative video inpainting, region replace by mask or text, viral still-image effects | 4 |
| **Editing** | Concat, mix, trim, captions, PiP, animate-zoom, browser-frame, beat-sync, audio denoise, text overlay, add captions | 11 |
| **Capture** | Website screenshot / recording, frame extraction, audio extraction | 3 |
| **Analysis** | Media, brief, transcription, clip highlights | 4 |
| **Identity** | Avatar, voice, persona, memory append / search, sample | 10 |
| **Persistent refs** | Reusable character refs, element refs, cloned voices | 3 |
| **Connect** | Third-party app integrations via auth / discover / call (broad ecosystem) | 3 |
| **Scrape** | Ads, social | 2 |
| **Publish / search / async / utility** | Web publish, music search, skill search, task status/cancel, upload, HTML render, HTML→PDF | 8 |
| **Total** |  | **58** |

Full schema → [`tools-manifest.json`](./tools-manifest.json).

## Requirements

- A Pika account ([sign up at pika.me](https://pika.me)) — carries your persona, voice, avatar, and memory
- One of: an MCP-compatible client (any agent), a skill-aware agent ([50+ supported](https://github.com/vercel-labs/skills)), or Claude Code ≥ v2.0.12 (for the plugin path)

## FAQ

**How does pricing work?**
All generation consumes **Pika credits** from your Pika account. Free credits ship with every account; top up at [pika.me](https://pika.me). Atomic-tool calls and curated `/pika:*` skills draw from the same balance.

**Is my voice clone, avatar, and memory private?**
Yes. Persona, cloned voice, avatar, and memory are scoped to your Pika account and accessible only to your authenticated MCP sessions. They are not used to train shared models. Manage or delete at [pika.me](https://pika.me).

**Can I bring my own provider API keys?**
No — Pika manages provider routing internally so you don't juggle API keys, rate limits, or billing across vendors. One Pika account, one billing surface, every model.

**Issues / questions →** [`Pika-Labs/Pika-Plugins/issues`](https://github.com/Pika-Labs/Pika-Plugins/issues)

## Links

- [Changelog](./CHANGELOG.md) — release history
- [Tool schema](./tools-manifest.json) — all 58 atomic tools with full param surfaces
- [Pika MCP endpoint](https://mcp.pika.me/api/mcp) — raw HTTP MCP
- [Pika Developer Portal](https://www.pika.me/dev/) — keys and SDK references
- [Security policy](./SECURITY.md)
- Open-source skill modules → [`Pika-Labs/Pika-Skills`](https://github.com/Pika-Labs/Pika-Skills)
- Pika consumer products — [pika.me](https://pika.me), [iOS app](https://apps.apple.com/us/app/pika-ai-agent/id6758411447)

## License

Apache 2.0 — see [LICENSE](./LICENSE). Speaks the open [Model Context Protocol](https://modelcontextprotocol.io/); finishing pipeline built on [ffmpeg](https://ffmpeg.org/) and [Playwright](https://playwright.dev/).
