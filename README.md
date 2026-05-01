<h1 align="center">Pika-fy your Claude</h1>

<p align="center">
  <b>Give your Claude a face, name, voice, and personality</b> — plus a full creative stack of image, video, audio, and editing tools. All in your terminal.
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/plugin-v1.0.0-blue" alt="Plugin version"></a>
  <a href="https://mcp.pika.me/api/mcp"><img src="https://img.shields.io/badge/MCP-mcp.pika.me-green" alt="MCP server"></a>
  <a href="./tools-manifest.json"><img src="https://img.shields.io/badge/tools-42_atomic_primitives-purple" alt="Tools"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache_2.0-blue" alt="License"></a>
</p>

```
> /pika:podcast https://pika.art
  scraping page (capture_website)...
  writing 4-act script (Host A · Host B)...
  rendering 4 video acts × ~15s (native multi-shot)...
  concatenating final clip...
  done.
View video: https://cdn.pika.art/agent/<task-id>/podcast-final.mp4
```

Until now, every Claude was just *Claude*. With the **Pika MCP + Plugin** it can be a person you design — a 3D avatar, a cloned voice, a long-term memory of who you are — driving Pika's complete creative stack: video, image, voice cloning, music generation, deterministic HTML→video rendering, automatic captions, and ffmpeg-based finishing. **AI-native by design — not a GUI wrapped in an API.**

## How Pika fits together

Pika has three layers — your **Agent** (persona), the **MCP server** (protocol), and the **Claude Code plugin** (curated skills). The plugin auto-registers the MCP via its bundled `.mcp.json` — you don't have to wire anything by hand.

| Layer | What it is | Where it lives |
|---|---|---|
| **Pika Agent** | Your persona — name, face, voice, and persistent memory — applied to every tool call | [pika.me](https://pika.me/) · [iOS app](https://apps.apple.com/us/app/pika-ai-agent/id6758411447) |
| **Pika MCP** | Open-protocol server exposing 42 atomic creative tools (image, video, voice, music, edit) | `https://mcp.pika.me/api/mcp` |
| **Pika Plugin** | 3 curated `/pika:*` slash commands that orchestrate multi-step pipelines on top of the MCP | This repo |

Same backend, same auth, same output. [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) is Anthropic's open standard for connecting agents to external tools — Pika MCP works with any MCP-compatible client; see [Other Claude surfaces & MCP clients](#other-claude-surfaces--mcp-clients) for non-Claude-Code setups.

> Tool names are shown unprefixed throughout this README (e.g. `generate_video`, `clone_voice`). Inside Claude Code the actual MCP tool prefix is `mcp__plugin_pika_pika__*` — both the curated skills and the tool catalog work without you ever needing to type the prefix.

## Quickstart

Requires Claude Code ≥ v2.0.12 (when the `/plugin` marketplace commands first shipped).

### 1. Create your Pika Agent

If you don't already have one, create your Pika Agent at **[pika.me](https://pika.me/)** or via the **[iOS app](https://apps.apple.com/us/app/pika-ai-agent/id6758411447)**. Your Pika Agent carries your persona, voice, avatar, and persistent memory across every Pika tool call — without it, the plugin has no identity to drive.

### 2. Install the plugin

Pick the surface you use:

#### Claude Code CLI (terminal)

```bash
claude plugin marketplace add Pika-Labs/Pika-Plugins
claude plugin install pika@pika-plugins
```

#### Claude Code Desktop (macOS / Windows app)

UI-driven, with one slash-command line for the one-time marketplace registration. In the **Code** tab:

1. In the prompt box, type `/plugin marketplace add Pika-Labs/Pika-Plugins` and hit Enter.
2. Click the **+** button next to the prompt box → **Plugins** → **Add plugin** → find **pika** → **Install**.

Step 1 goes away once Pika lands in Anthropic's [official marketplace](https://claude.ai/settings/plugins/submit) — until then, the Desktop UI's plugin browser only surfaces plugins from already-configured marketplaces ([tracked in claude-code#52147](https://github.com/anthropics/claude-code/issues/52147)).

### 3. Restart Claude Code

Full quit and reopen — `.mcp.json` only loads at startup, and `/reload-plugins` alone isn't enough.

### 4. Authenticate

Inside Claude Code:

```
> /mcp
```

Find `pika`, hit **Authenticate** — your browser opens to the Pika sign-in page, sign in with the same account as your Pika Agent, the token is cached locally, and Claude Code reconnects automatically. Done. (See [Authentication](#authentication) for headless / CI options.)

### 5. Use it

You don't need to type slash commands — Pika skills auto-fire on natural-language intent. Both forms below do the same thing:

```
> /pika:podcast https://pika.art
> make me a podcast about https://pika.art

> /pika:explainer https://github.com/anthropics/claude-code
> walk me through this repo: https://github.com/anthropics/claude-code

> generate a 5-second video of a red panda dancing in the rain
```

The agent reads your prompt and runs the matching skill (or falls back to atomic MCP tools). Spending is bounded by your Pika account credit balance — no separate per-call confirmation step.

### Verify

```bash
claude plugin list
# pika@pika-plugins    Version: 1.0.0    Status: enabled
claude mcp list
# pika: https://mcp.pika.me/api/mcp (HTTP) - Connected
```

## Other Claude surfaces & MCP clients

The Pika MCP server is a standard MCP endpoint — it works with any MCP-compatible client. The Claude Code plugin (covered above) is the curated experience; below is everything else.

| Client | How to add Pika |
|---|---|
| **Claude Code** (CLI / Desktop) | See [Quickstart Step 2](#2-install-the-plugin) above — full plugin with curated `/pika:*` skills |
| **Claude.ai chat** (regular web app) | Open [claude.ai/settings/connectors](https://claude.ai/settings/connectors) → **Add custom connector** → enter `https://mcp.pika.me/api/mcp` as the MCP server URL → complete the OAuth sign-in. Then enable the connector via the **+** button in any chat. |
| **Claude Desktop chat** (the Chat tab, not the Code tab) | Edit `claude_desktop_config.json` and add Pika as a remote MCP server pointing at `https://mcp.pika.me/api/mcp`. Restart Claude Desktop. |
| **Cursor / Codex / any MCP client** | Add `https://mcp.pika.me/api/mcp` as an HTTP MCP server in your client's MCP config; sign in with the same account as your Pika Agent. |

On non-Claude-Code surfaces you get the **42 atomic tools** (image, video, voice, music, edit, identity) but **not** the curated `/pika:*` slash commands — those are Claude Code-specific. Same backend, same Pika Agent, same auth.

## Launch-spotlight skills

Curated skills designed to take you from a single prompt to a finished, shareable video. Three ship today (Podcast/Interview, Explainer, UGC Ads). All generation skills consume Pika credits (paid via your Pika account).

> [!TIP]
> **Skills activate from natural language — the slash command is optional.** Saying _"make me a podcast about https://pika.art"_ or _"walk me through this repo: github.com/foo/bar"_ triggers the matching skill automatically. The `/pika:*` form is just an explicit shortcut.

### Podcast / Interview Video — `/pika:podcast`

Hand it a URL **or a free-form topic** — get back a finished **1-minute two-host conversational video**. 4 acts × ~15s each, native multi-shot dialogue, with the Matan-authenticity rules baked in: specific jokes tied to concrete details, "wait, actually..." pivots, mid-sentence interruptions, real reactions over generic praise. Optional voice cloning for Host A via `use_avatar`. ~25–30 min wall-clock. **Costs Pika credits.**

**URL mode** — scrape and review a product page, GitHub repo, or blog post:

```
/pika:podcast https://pika.art
/pika:podcast https://github.com/anthropics/claude-code use_avatar
/pika:podcast                                       # ← no args = print input menu
```

**Topic mode** — free-form brief; the skill writes the script from your prose:

```
/pika:podcast Two AI researchers debate whether AGI arrives before 2030
/pika:podcast I and a Mars-obsessed tech CEO talk about colonization timelines
/pika:podcast interview with a seed-stage VC about what kills most startups
```

Triggers from natural language — _"make a podcast about [url-or-topic]"_, _"interview-style clip about X"_, _"two-host take on Y"_, _"I and [persona] talk about Z"_ — or call the slash command directly. Named real people get archetype portraits by default (no auto-deepfake); pass `host_b_img=<url>` to override with a likeness you have rights to.

### Explainer Video — `/pika:explainer`

Hand it **any URL** — a GitHub repo, product page, docs site, blog post, launch announcement — get back a ~60–80s explainer at 1280×800. Drives a real browser through the URL along an element-targeted timeline, generates an avatar lipsync of the narration, and composites it all in a macOS Sonoma frame with a 246-pixel bottom-left circle avatar. **GitHub URLs** activate a repo-aware mode (README scan + live-demo detection); other URLs use a generic page-walkthrough flow. ~5–7 min wall-clock with default `pika` lipsync; ~10–25 min if you opt into `--lipsync-provider kling` for polished-presenter mode. **Costs Pika credits.**

Triggers from natural language too — _"explain this URL"_, _"walk me through [url]"_, _"make a demo video of [product page]"_, _"explainer for [github/product/docs link]"_, _"Loom-style walkthrough of [url]"_ — or use the slash command:

```
/pika:explainer https://github.com/anthropics/claude-code
/pika:explainer https://github.com/<owner>/<repo> --focus "architecture, demo"
/pika:explainer https://github.com/<owner>/<repo> --avatar https://cdn.pika.art/<...>.png
/pika:explainer                                       # ← no args = print URL menu
```

### UGC Ads — `/pika:ugc-ads`

Hand it a product URL — get back a **15s creator-style multi-cut UGC ad** in 9:16 vertical: HOOK + 3 JUMP CUTs + OUTRO, POV first-person talking-head selfie, native lip-synced dialogue on every beat with a 5-act narrative arc (set → name → reveal → twist → punchline). The dialogue is the through-line; the screen close-up + finger-point lands on whichever JUMP CUT the *reveal* line falls on. Six category essences (HAUL / APP / FOOD / BEAUTY / FITNESS / TECH) auto-picked from the URL guide dialogue character per category. Built-in fallback Pixar-style avatar when no `avatar_url` supplied; auto-cartoonize-on-rejection via seedream when fal-queue moderation flags a photorealistic portrait; uses your Pika avatar + cloned voice silently when available. ~6–12 min wall-clock. **Costs Pika credits.**

Triggers from natural language — _"make a UGC ad for [URL]"_, _"jump-cut product ad about [URL]"_, _"creator-style ad for X"_, _"talking-head TikTok ad about Y"_, _"haul-style ad"_, _"unboxing video about [URL]"_ — or use the slash command:

```
/pika:ugc-ads https://pika.art
/pika:ugc-ads https://maisonbrune.com avatar_url=https://cdn/face.png aspect_ratio=3:4
/pika:ugc-ads https://oatly.com category=FOOD
/pika:ugc-ads https://glossier.com avatar_url=https://cdn/face.png provider=kling
/pika:ugc-ads                                       # ← no args = print URL menu
```

## Authentication

You need an authenticated MCP session before any Pika tool call works. The recommended path is one-time `/mcp` connect:

```
> /mcp
```

This opens the MCP manager UI. Find `pika`, hit **Authenticate** — your browser opens to the Pika sign-in page, sign in with the same account as your Pika Agent, the token is cached locally, and Claude Code reconnects automatically. After this, every Pika tool call works without re-prompting.

<details>
<summary><b>Other auth flows: auto-OAuth on first call · static token (headless / CI) · troubleshooting</b></summary>

### Auto-OAuth on first call

Skip `/mcp` and just call any Pika tool. The first call returns `401`, Claude Code auto-discovers the OAuth metadata, opens your browser, you sign in, and the original call retries automatically.

```
> /pika:podcast https://pika.art
[browser opens for OAuth]
[returns to terminal, call retries, video URL appears]
```

### Static token (headless / CI / no browser)

If you can't do an interactive browser flow, set a Pika token in your shell **before launching `claude`**:

```bash
export MCP_AUTH_TOKEN="<your-pika-token>"
claude
```

Tokens come in two flavors — a **developer key** (`dk_*` prefix, long-lived; get one at [pika.me/dev](https://www.pika.me/dev/)) or an **agent key** (service-to-service for trusted automation). Don't hard-code `${MCP_AUTH_TOKEN}` into `.mcp.json` or any file you commit — keep it in your shell env.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `401 Unauthorized` on every call | Token expired. `claude mcp remove pika` then re-run `/mcp` to re-auth. |
| Want to switch accounts | `claude mcp remove pika` → re-run `/mcp` and sign in with the other account. |
| Browser doesn't open during OAuth | Allow Claude Code to open default browser, or fall back to a static token. |
| `claude mcp list` shows `Disconnected` | Restart Claude Code (full quit). `.mcp.json` is only loaded at startup. |

</details>

## What you can do with Pika

The plugin ships 3 curated slash commands; underneath, **42 atomic MCP tools** are at your agent's disposal. You describe the outcome in plain English — Pika picks the right tool.

### Generate video

Text-to-video, image-to-video, multi-reference video, keyframe transitions, lipsync, and motion transfer — all under one schema. Pika auto-routes to the best model for each request; override via the `provider` field if you have a preference.

```
> make a 5-second video of a red panda dancing in the rain
> animate this image
> take these 3 reference images and this audio, build me a 10-second clip
> sync this audio to this face
> apply the motion from this reference video onto this character image
```

`generate_video` · `generate_reference_video` · `generate_keyframes_video` · `generate_lipsync` · `generate_motion_control_video`

### Generate images

Text-to-image, image editing, 4K resolution, ultra-fast iteration. Same auto-routing logic as video.

```
> generate a product photo of a coffee cup on white
> make a 4K vertical wallpaper based on this brief
> edit this image — add a sunset behind it
```

`generate_image`

### Generate + clone voices

Text-to-speech in 100+ languages, voice cloning from a 30-second sample. Cloned `voice_id`s are reusable across `generate_speech` and any video tool that takes voice IDs.

```
> read this script in a calm female voice
> clone my voice from this 30-second sample
> make a podcast where two AI hosts debate Bitcoin
```

`generate_speech` · `clone_voice`

### Generate music

Original music generation, licensed-catalog search, and beat-synced video cuts.

```
> compose a 60-second uplifting electronic track
> find royalty-free music about [topic]
> cut this video on the beat at 128 bpm
```

`generate_music` · `search_music` · `edit_beat_sync`

### Edit + finish

Pure-ffmpeg deterministic ops, ~30s each, stitched together by the agent. Concat, audio mix/trim, captions in 4 styles (`tiktok` · `hormozi` · `classic` · `karaoke`, 100+ languages), text overlays, picture-in-picture (rect or circular), animated zoom, macOS-frame wrap for screen recordings, frame extraction.

`edit_concat` · `edit_audio_mix` · `edit_audio_trim` · `edit_text_overlay` · `edit_pip` · `edit_trim` · `edit_animate_zoom` · `edit_browser_frame` · `add_captions` · `extract_frame`

### Render HTML → video (HyperFrames)

Claude writes HTML, HyperFrames renders deterministically — same input produces byte-identical output. Outputs MP4, WebM, or MOV with transparency.

```
> make me a 30-second animated slide deck about my product launch
> render this HTML composition as a video
```

`generate_slide_animation` · `render_html_animation`

### Analyze + transcribe

Describe media, extract structured briefs from mixed sources, transcribe audio or video, and capture live websites with timed scroll/click actions.

```
> describe this video
> extract a structured product brief from these 3 sources
> transcribe this audio
> screencap this URL with timed scrolling
```

`analyze_media` · `analyze_brief` · `transcribe_audio` · `capture_website`

### Identity + memory

Your Pika Agent's persona, voice, avatar, and a persistent memory store — auto-injected as defaults on every Pika tool call so you never have to repeat yourself.

`identity_whoami` · `identity_persona_read` · `identity_avatar_url` · `identity_voice_id` · `identity_voice_info` · `identity_set_avatar` · `identity_set_voice` · `identity_memory_search` · `identity_memory_append`

### Full schema

→ [`tools-manifest.json`](./tools-manifest.json) — all 42 tools with complete input/output schemas, ready for raw-MCP / OpenAPI consumers.

## FAQ

**How does pricing work?**
All generation skills consume **Pika credits** from your Pika account. Free credits ship with every account; top up at [pika.me](https://pika.me/). Atomic-tool calls (e.g. `generate_video`) and curated skills (`/pika:podcast`, `/pika:explainer`, `/pika:ugc-ads`) both draw from the same balance.

**Can I use Pika MCP without Claude Code?**
Yes — the MCP server at `https://mcp.pika.me/api/mcp` is a standard HTTP MCP endpoint and works with Claude Desktop, Cursor, Codex, or any MCP-compatible client. The curated `/pika:*` slash commands are Claude Code-specific, but the 42 atomic tools are universal. See [Other Claude surfaces & MCP clients](#other-claude-surfaces--mcp-clients).

**Is my voice clone, avatar, and memory private?**
Yes. Your Pika Agent's persona, cloned voice, avatar, and memory are scoped to your Pika account and only accessible to your authenticated MCP sessions. They are not used to train shared models. Manage or delete them at [pika.me](https://pika.me/).

**Can I bring my own model API keys?**
No — Pika manages provider routing internally so you don't have to juggle API keys, rate limits, or billing across multiple model vendors. One Pika account, one billing surface, every model.

**What's the difference between this and the Pika web app?**
The web app is a hosted creative environment with a UI. The MCP + Plugin is **AI-native** — designed to be driven by an agent in plain English, with no UI. Same backend, same Pika Agent, same output. Use the web app for hands-on direction; use the MCP + Plugin to let an agent compose multi-tool pipelines for you.

## Related projects

| Repo | What it is | Use when |
|---|---|---|
| **[Pika-Labs/Pika-Skills](https://github.com/Pika-Labs/Pika-Skills)** | Open-source `SKILL.md` modules powered by the Pika Developer API. No MCP, no plugin — drop a folder into your agent workspace, set `PIKA_DEV_KEY`, and go. | You want a single-purpose skill (e.g. video meeting agent) without installing the full plugin, or you're on an agent harness without MCP support. |
| **This repo** ([`Pika-Labs/Pika-Plugins`](https://github.com/Pika-Labs/Pika-Plugins)) | Full Claude Code plugin + remote MCP server with 42 atomic tools and curated `/pika:*` slash commands. | You want the complete creative stack inside Claude Code with one install. |

## Manage your install

```bash
claude plugin update pika
claude plugin disable pika
claude plugin uninstall pika
claude plugin marketplace remove pika-plugins
```

## Acknowledgments

Built on [Anthropic Claude Code](https://www.anthropic.com/) and the open [Model Context Protocol](https://modelcontextprotocol.io/), with [ffmpeg](https://ffmpeg.org/) and [Playwright](https://playwright.dev/) for finishing and capture.

## Contributing

Issues + PRs welcome at [`Pika-Labs/Pika-Plugins`](https://github.com/Pika-Labs/Pika-Plugins/issues).

## License

See [LICENSE](./LICENSE).
