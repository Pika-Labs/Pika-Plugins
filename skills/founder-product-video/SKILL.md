---
name: founder-product-video
description: >-
  Generate a 65-second founder-style product video from a product URL + user-supplied imagery.
  Output is a 16:9 1080p MP4 — 4 × 15s SeeDance acts of a talking founder + 5s branded end card +
  background music. The user's actual product screenshots are composited onto product reveal shots
  after Seedance generation, so readable UI and brand text are real, not AI-imagined. Triggers — "founder video", "product video",
  "60s pitch video", "make a video of [founder] for [URL]", "talking founder explainer". Requires
  Pika MCP. Uses a supplied brand kit folder (`brand.json` or an exported build-a-brand kit with
  `brand.md`, tokens, logo assets); if no kit exists, run build-a-brand first.
argument-hint: <product-url> --founder "<name, role>" [--photo <path|url|generate>] [brand-kit=<path>] [aspect=16:9|9:16|1:1] [--quick] [--config <path>]
required-capabilities:
  - add_captions
  - analyze_brief
  - analyze_media
  - capture_website
  - edit_audio_mix
  - edit_concat
  - edit_video_compose
  - edit_text_overlay
  - extract_frame
  - generate_image
  - generate_music
  - generate_reference_video
  - generate_slide_animation
  - html_to_png
  - identity_balance
  - render_html_animation
  - task_status
  - task_cancel
  - upload_asset
---

# founder-product-video

You generate a 65-second founder-style product video from a product URL plus user-provided imagery: 60 seconds of talking-founder body video plus a 5-second branded end card. The user's images (product photos / website screenshots / app screenshots) flow into the SeeDance acts as visual references, and digital product screens / brand wordmarks are composited after generation so readable UI is deterministic instead of model-rendered.

No cutaways. No website CSS extraction. AI generation, deterministic render, captions, concat, and music mix go through Pika MCP tools by default. Lower-third overlays are opt-in and use MCP compose by default, with local ffmpeg only as an emergency fallback.

## Cost transparency gate

Before any paid MCP call, call `identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the run with this exact message:

> Estimated cost: about 4,000 credits (~$40) for a typical four-act Seedance founder video plus supporting assets. This exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. For non-interactive `--quick` or `--config` callers, require `cost_ack=proceed` in the config; if it is absent, stop with the estimate instead of spending credits.

## [0] Intake — run first, before any pipeline step

**If invoked with empty args**, print this menu verbatim and stop — wait for the user to paste inputs:

> **What founder video do you want to make?** Required:
> - **Product URL** — `https://...` (anything with a real homepage)
> - **Founder** — name + role, e.g. *"Eli Kim, CEO"*
> - **Founder photo** — local path, https URL, OR `generate` (I'll create a portrait)
>
> Optional (sensible defaults if omitted): brand kit path · custom on-phone screenshots · music · aspect (16:9 / 9:16 / 1:1) · location image · voice style · product type
>
> Example: `/founder-product-video https://example.com --founder "Eli Kim, CEO" --photo ~/Pictures/eli.jpg`

**If args carry partial input in interactive mode**, skip the menu and gather the missing required fields by asking one at a time — ask, wait, ask the next. Don't bundle questions into one block. If the user supplies a field unprompted (e.g. they pasted a URL in the trigger message), skip that question and confirm the value back to them once at the end. Don't start the pipeline until all required fields are answered. If the non-interactive fast lane applies, use step [0.5] instead.

### [0.5] Non-interactive fast lane

Use this path when the caller passes `--quick` or `--config <path>`, or when the
caller states they are running from CI, a subagent, a batch job, or any other
non-interactive harness.

This section has precedence over the interactive ask/wait instructions below.
When it applies, use this fast lane and do not fall through to the multi-turn
intake unless `url` or founder name/role is truly missing.

- `--config <path>` points to a JSON file with pre-baked values for the canonical
  input contract: `url`, `brand_kit_path` or `build_brand`, `founder_name`,
  `founder_role`, `founder_photo`, `assets`, `music_url`, `aspect_ratio`,
  `location_image_url`, `voice_style`, `product_type`, and `lower_third`.
- `--quick` means use defaults for optional extras, auto-build the brand kit with
  `build-a-brand --quick` if `brand-kit` is omitted, and use `founder_photo =
  "generate"` when no photo is supplied.
- For `--quick` or `--config`, do not stop for confirmation at the brand-kit
  branch, founder-photo generation prompt, optional-extras prompt, script
  choices, or end-card/caption defaults. Record assumptions inline and continue.
- If `url` or founder name/role cannot be found in args or config, stop once with
  a single compact missing-fields list instead of starting a multi-turn Q&A loop.

**1. Product URL** *(required)* — `https://...`. Used to (a) derive the brief in step [1] and (b) feed the brand-kit branch below.

**2. Brand kit** *(required)* — interactive mode: ask *"Do you already have a brand kit folder, or should I build one first?"*
- If a path -> use it (`state.brand_kit_path = <path>`). Accept either `brand.json` or an exported `build-a-brand` kit containing `brand.md`, `tokens/tokens.json`, and logo assets.
- If "build" -> invoke the `build-a-brand` skill on the URL/brief and wait for the exported brand kit. This is a full identity workflow and may pause for user choices; surface those prompts in interactive mode.
- Fast lane: if config provides `brand_kit_path`, use it. If config sets `build_brand` or `--quick` omits `brand-kit`, invoke `build-a-brand --quick` on the URL/brief and wait for the exported brand kit; do not surface build-a-brand prompts or stop for identity choices. After either branch, set `state.brand_kit_path`. Only stop with a single compact missing-fields list if there is no path and the brand kit cannot be built.

**3. Founder identity** *(required)* — interactive mode: ask all three together:
- `founder_name` — e.g. "Avery"
- `founder_role` — e.g. "CEO, ExampleCo"
- `founder_photo` — local path / https URL / OR the literal string `generate` to auto-create a portrait. If `generate`, prompt the user for a 1-line vibe ("warm, casual smart attire" / "Pixar-style 3D animation" / etc.) — this becomes the seed prompt for `generate_image` in step [4].
- Fast lane: use founder values from args/config. If `founder_photo` is omitted, set `founder_photo = "generate"` and use a neutral founder-portrait vibe derived from the product tone; do not stop for a separate photo-vibe prompt.

Default to no lower-third so the happy path stays lean. If the user explicitly asks for a lower-third, record `state.lower_third = true`; in interactive mode confirm that `edit_video_compose` will add the transparent overlay after rendering.

**4. Optional extras** — interactive mode: offer these once as a single message, then proceed without waiting if no answer comes back in the same turn. Fast lane: use the defaults below without asking.
- *Custom imagery* — list of `assets` (product photos / app screenshots) shown on the founder's phone. **Default if omitted:** use screenshots from `brand.json.screenshots` when present, otherwise look for obvious screenshots or product images inside the brand kit, otherwise capture the product URL with `capture_website(mode:"screenshot")` before step [2]. Do not proceed to script or SeeDance without real product UI / product imagery unless `product_type` is explicitly `service` and the user accepts an environment-only video. In the fast lane, if no supplied/brand-kit/captured asset exists, stop once with a compact missing-assets error instead of silently shipping a generic talking-head video.
- *Music* — local path / https URL / OR `generate` (instrumental, ~60s). Default: `generate` via Kling background mode.
- *Lower-third* — optional. Default: off. If enabled, render the transparent `.mov` through MCP and overlay it onto the body with `edit_video_compose`.
- *Aspect ratio* — `16:9` (default), `9:16`, `1:1`.
- *Location* — defaults to a flat seamless backdrop in `state.brand.colors.accent` (clean studio-shoot look, character against a single brand color, whatever the brand's accent is). Override with a path / URL / text description if the user wants office, outdoor, etc.
- *Voice style* — VO direction string for SeeDance, e.g. "warm authentic founder energy, conversational". Default: derived from `brief.tone`.
- *Product type* — `digital | physical_apparel | physical_object | consumable | service`. Default: auto-derived in step [2] from asset analyses.

After Stage 0 completes, store all gathered values in `state.inputs`. If you already created a local work directory for this run, optionally persist the same object as `<workdir>/inputs.json`; do not require a predefined work-directory environment variable. Then enter the pipeline at step [1].

### [0.6] Avatar-type probe for founder photos

Before any paid `generate_reference_video` call, run this Avatar-type probe on the resolved founder photo/avatar URL after local upload or user-supplied URL normalization. This applies to any founder photo used as the character reference — whether supplied via `--photo` or generated.

Call `analyze_media` once:

```
query: "Classify this image for paid video generation. Is it a photograph of a real human face, an AI-generated realistic portrait, a stylized / illustrated character, or a recognizable trademarked / copyrighted character such as Batman, Pikachu, or Mickey Mouse? Return strict JSON only: { \"avatar_type\": \"real_human\" | \"ai_realistic\" | \"stylized_illustrated\" | \"recognized_ip\", \"recognized_character\": string | null, \"moderation_risk\": \"low\" | \"medium\" | \"high\", \"recommendation\": \"proceed\" | \"warn\" | \"reject\" }. Use null for `recognized_character` when no specific character is recognized; never write \"none\", \"unknown\", or explanatory prose in that field."
```

Route from the result:
- **recognized IP / copyright risk** -> **STOP only when** `avatar_type` is `"recognized_ip"`, or `recognized_character` names a specific character (for example `"Batman"`), or when both `moderation_risk` is `"high"` and `recommendation` is `"reject"`. Treat `recognized_character: null`, empty string, `"none"`, `"unknown"`, `"n/a"`, and low/medium `moderation_risk` as not enough to stop by themselves. Run this check before the real/stylized routes. A chibi Batman is still Batman even when `avatar_type` is stylized / illustrated.
- **real human / AI-generated realistic** -> proceed normally.
- **stylized / illustrated** -> proceed with a visible warning that stylized avatars may be less reliable for Seedance likeness and moderation, then continue only if the user supplied or accepted that avatar.
- **trademarked / copyrighted** -> **STOP** before generation. Surface this message: `Your founder photo appears to be a trademarked character ([X]). Most video providers will moderate this and refuse to generate. Pass --photo <real-looking-photo-url> to override.` For this skill, `--photo <real-looking-photo-url>` is the accepted concrete flag; you may also mention the cross-skill `--avatar <real-looking-photo-url>` wording because users may know that convention.

## Required inputs (canonical contract)

After Stage 0, these are the fields downstream steps consume:

- `url` — the product website (https://). Drives step [1] brief.
- `brand_kit_path` — brand kit folder. Required. End card AND lower-third consume `brand.json` when present, otherwise `brand.md`, `tokens/tokens.json`, and logo assets from a `build-a-brand` export. See step [4.5].
- `founder_name` + `founder_role` + `founder_photo` — required from intake. Step [4] normalizes `founder_photo` into `founder_photo_url` and `character_url` before any SeeDance call.
- `assets` — optional array of `{ url, role?, caption? }`. Defaults to the screenshots captured by the brand kit; when the brand kit has no screenshots, capture the product URL before step [2] and store the returned `image_url` as a real product UI asset. `role` is a hint string mapping the asset to a script beat (`hero`, `feature_a`, `cta`, etc.).
- `location_image_url` — optional. Defaults to a generated solid-color backdrop in `state.brand.colors.accent`.
- `music_url` — optional. Defaults to `generate` (Kling 60s background bed in step [7]).
- `aspect_ratio` — default `16:9`.
- `voice_style` — optional, defaults to `brief.tone`.
- `product_type` — optional, auto-derived in step [2].

## State

Keep a simple `state` object as you work and save every CDN URL there so a partial run can be resumed. Treat `task_status` value `completed` as the successful terminal state (`failed` and `cancelled` are the failure terminals), then unwrap `result.structuredContent` when present. The final video lives on Pika's CDN; no local workspace is required unless MCP compose is unavailable and you explicitly trigger the local lower-third fallback in step [8b].

## Long-running task_status polling

When any long-running generation or edit call returns a `task_id` with or without an initial status, including `{task_id}`, `{task_id, status: "queued"}`, or an initial `queued`, `running`, or `processing` status, record the task id and start time immediately in `state`.

- Call `task_status({task_id})` in a tight loop until terminal (`completed | failed | cancelled`). No manual sleep and no Bash polling; the worker holds each status call open.
- Emit ONE visible progress line every 60s while status is `queued`, `running`, or `processing`: `Seedance i2v queued for {N}m {S}s... still processing`. Replace the provider/stage label when polling music, captions, render, concat, mix, or edit tasks.
- On `completed`, unwrap the returned result URL and save it into `state`.
- On `failed` or `cancelled`, surface failure to the user with `task_id`, status, and the last status message.
- After 15 min total from the original submit, call `task_cancel({task_id})` if the task is still non-terminal, then surface failure to the user. If cancel reports the task is already terminal, call status once more and report that terminal result.
- Do not submit a duplicate request while the original task is still `queued`, `running`, or `processing`.

## Pipeline overview

```
[Stage 0] intake          you (Claude): ask user for url + brand-kit (path or build) + founder (name/role/photo) + optional extras
  → [0.5] brand-kit auto-build (only if user said "build")
                          invoke `build-a-brand`; in non-interactive mode use `build-a-brand --quick`
  → [1] analyze_brief             pika MCP: product name + tagline + features + tone + CTA
  → [2] resolve product UI assets pika MCP: use supplied/brand-kit screenshots, or capture_website(product URL)
  → [2] analyze_media × N         pika MCP: understand what each real asset shows
  → [3] write script              you (Claude): 4 acts × 15s; map assets to acts
  → [4] founder/location refs     pika MCP: upload or generate founder ref; carry supplied custom location
  → [4.5] brand-kit ingestion     parse brand.json OR brand.md + tokens → state.brand; generate default brand-accent location if needed
  → [5] generate_reference_video × 4 IN PARALLEL  pika MCP: SeeDance acts, asset images as refs
  → [5.5] digital UI overlays     pika MCP: composite real product UI / wordmark onto digital reveal acts + OCR QA
  → [6] edit_concat acts          pika MCP: 60s stitched base (dialogue-only audio)
  → [7] generate_music            pika MCP: Kling 60s soft instrumental background bed
  → [8] captions / lower-third    pika MCP: add_captions for subtitles; render lower-third as transparent .mov, then overlay it with edit_video_compose when lower-third is enabled.
  → [9] render_html_animation     pika MCP: 5s end card — author inline HTML, brand-kit fonts inlined, aspect matches body, no corner clutter, CSS @keyframes (NOT GSAP)
  → [10] edit_concat + audio_mix  pika MCP: concat body + end card, then mix music over the full ~65s
  → [10.5] final duration probe   pika MCP: analyze final_url and enforce the 55s duration floor before delivery
  → [11] final_url                save the MCP returned final_url; upload only if a local fallback created the final MP4
  → [12] deliver
```

## Operational notes

Keep the main workflow focused on sequencing. Historical server validation details live in `references/ops-notes.md`; only the active constraints stay here:

- Use a unique `seed` per SeeDance act (101, 202, 303, 404). Identical generation params can replay cached failures.
- Kling music bed generation uses `provider: "kling-audio"`, `mode: "text_to_audio"`, `background: true`, and `duration_seconds: 60`; the MCP worker generates one 10s Kling seed and extends it locally.
- If SeeDance rejects a real-person founder photo, re-roll the founder ref with stronger stylization rather than retrying the same rejected reference.
- For local brand-kit logos, upload only logo-appropriate raster assets (`image/png`, `image/jpeg`, or `image/webp`). Do not send SVGs to `upload_asset`; choose the PNG export from `build-a-brand` or rasterize first.
- Use CSS `background-image: url(...)` for CDN-hosted logo/photo assets in end-card HTML; `<img crossorigin>` is blocked by CDN CORS.
- Use server-side deterministic tools for captions, lower-third compose, concat, and mix. Local ffmpeg is only the fallback if `edit_video_compose` is unavailable while `state.lower_third = true`.
- Decompose every 15s act into 3 time-coded sub-shots. Single-shot acts look static.
- Open each act with the style-match location framing and repeat the same `WARDROBE LOCK:` sentence across all 4 act prompts.

## [1] Analyze brief

```
analyze_brief(
  sources=[{ type: "url", url: <product_url> }],
  context: "Founder-style 60-second product video. Need: product name, one-line tagline, 3-5 key features, target audience, brand tone, and a call-to-action."
)
```
Save the result as `brief`. You'll reference `brief.product_name`, `brief.tagline`, `brief.key_features`, `brief.tone`, `brief.call_to_action` throughout.

## [2] Resolve product UI assets, then analyze each asset + derive `product_type`

Before analyzing assets, normalize `assets` so product reveal shots have a real visual reference:

1. Use any caller-provided `assets` first.
2. If none were supplied, read screenshots from `brand.json.screenshots` when present.
3. If `brand.json` has no screenshots, look for obvious raster screenshots or product images inside the brand kit (`screenshots/`, `assets/`, `product/`, or image files named like `hero`, `screen`, `app`, `dashboard`, `product`).
4. **When `assets` is empty after those checks, call `capture_website` on the product URL**:

```
capture_website(
  url: <product_url>,
  mode: "screenshot",
  mobile: false
)
# Save result.image_url as assets[0].url with role="website_capture".
```

If the product is likely mobile-first, also run a second capture with `mobile: true` and keep both URLs when available. Save these as real product UI assets before continuing.

Do not proceed to script writing, `generate_reference_video`, or any paid SeeDance call without at least one real product UI / product imagery asset, unless the caller explicitly set `product_type: "service"` and accepted an environment-only video. If capture fails or returns no `image_url`, surface: `Could not capture <url>. Please provide screenshots or hosted product assets; founder-product-video will not silently ship without real product UI.`

For each entry in `assets`, run `analyze_media` to extract content + visual style + **asset type**. Run all in parallel in one tool batch:

```
analyze_media(
  media: <asset.url>,
  query: 'Describe this product image briefly. Return STRICT JSON:
  {
    "content_description": "1-line summary of what is visible",
    "asset_type": "digital_screen | physical_apparel | physical_object | consumable | infographic | other",
    "key_elements": ["3-5 specific UI elements / features / objects in the image"],
    "visible_copy": "any text visible — heading, button label, tagline, t-shirt graphic text (or empty string)",
    "primary_colors": ["#hex", "#hex", "#hex"],
    "vibe": "1-line visual feeling",
    "best_for_act": "hook | problem | solution | proof"
  }
  Return ONLY the JSON.'
)
```

`asset_type` decoder:
- `digital_screen` — app UI / website screenshot / SaaS dashboard / mobile app capture
- `physical_apparel` — t-shirts, hoodies, hats, anything wearable (model + garment)
- `physical_object` — gadgets, accessories, packaged goods, anything held in hand
- `consumable` — food, beverages, supplements (something used/eaten/drunk)
- `infographic` — chart, diagram, data viz, illustration
- `other` — anything else; describe and pick best fit

Save as `asset_analyses[i]`.

After analysis, build:

```
usable_product_assets = asset_analyses
  .map((analysis, i) => ({
    asset_index: i,           # original assets[] index to use in script.shots[].asset_index
    asset_url: assets[i].url, # public URL passed to reference_images later
    asset_type: analysis.asset_type,
    analysis
  }))
  .filter(entry.asset_type in [
    "digital_screen",
    "physical_apparel",
    "physical_object",
    "consumable"
  ])
```

If `usable_product_assets` is empty and you have not already tried a URL capture, call `capture_website(mode:"screenshot")` on the product URL, append the returned `image_url` to `assets`, run `analyze_media` on that capture, save the analysis at the same new index, and rebuild `usable_product_assets`. The captured screenshot must therefore have its own `asset_index`; do not reuse a logo/hero/infographic index for a product reveal.

Do not auto-derive `product_type = "service"` from logo-only, hero-only, infographic, abstract brand, or `other` assets. Those are not real product reveal anchors. If `usable_product_assets` is empty after the capture attempt, stop unless the caller explicitly set `product_type: "service"` and accepted an environment-only video. Surface the missing-assets error instead of falling through to the service reveal pattern.

### Derive `product_type`

Look at the dominant `asset_type` across `usable_product_assets`:

```
product_type = mode(usable_product_assets[i].asset_type) → mapped to {
  digital_screen → "digital"
  physical_apparel → "physical_apparel"
  physical_object → "physical_object"
  consumable → "consumable"
}
```

If user passed `product_type` explicitly, use that and skip auto-derivation; `service` is valid only when explicitly chosen/accepted. The `product_type` value drives **which shots are picked in step [3] and how the founder reveals the product in step [5]**. Get this right or the video shows the wrong thing on screen.

## Product type → reveal pattern (the most important table in this skill)

`product_type` (set in step [2]) controls which shots to pick AND how the asset is revealed in each shot. **The reveal beat in the SeeDance prompt is product-specific; using the wrong one makes the founder hold a phone for a t-shirt brand.**

For `digital` products, the SeeDance prompt is only responsible for the founder, camera move, phone gesture, and a blank / neutral screen placeholder. **Do not ask Seedance or the video model to render readable brand wordmark or product UI text.** The real screenshot, product UI, and exact brand spelling are composited in step [5.5].

| product_type | Reveal shots | Reveal beat (used in SeeDance prompt) | Which acts get assets |
|---|---|---|---|
| `digital` | C-phone, E-phone | "founder lifts her phone toward camera; the phone has a blank neutral screen placeholder reserved for the real UI overlay; do not render readable UI text or brand wordmark" | shots C and E only |
| `physical_apparel` | G-hold, G-wear, E-detail | "founder lifts a charcoal-washed graphic tee toward camera; the shirt design exactly matches @ImageN — match the print/graphic exactly, do not invent" OR "founder is wearing the t-shirt from @ImageN — match the print exactly" | EVERY shot where a t-shirt is visible (C/E/F + the "wearing" variants) |
| `physical_object` | C-hold, E-detail, F-twoshot | "founder holds the [product name] up toward camera; the product exactly matches @ImageN — match shape, color, branding" | shots that show the product |
| `consumable` | C-hold, E-detail, H-using | "founder holds/uses the [product]; the packaging/product matches @ImageN exactly" | shots that show the product |
| `service` | A, B, D, F (environment) | no specific product reveal — focus on founder + environment | none of the shots reference assets |

For physical products, every shot where the product appears in frame should pass that asset as a reference image; otherwise SeeDance tends to invent a generic-looking product. For apparel, if the founder is wearing a t-shirt and the script says "we make t-shirts", the founder's t-shirt needs to reference one of the assets even in shots that are not reveal moments. Pass the asset URLs in `reference_images` for those acts and write prompt language like "the founder is wearing the t-shirt from @Image3 — print matches exactly".

## [3] Write script + character voice + per-shot asset + per-line beats (you do this — no model call)

Three sub-products, all written by you (Claude) in one inline JSON:

1. **`character_voice_profile`** — 3-4 lines describing the character's DEFAULT delivery (carries through every act for consistency)
2. **Per-shot `asset_index` + `reveal_beat`** — what asset is visible in this shot and how it's revealed
3. **Per-shot `beats[]`** — line-by-line acting direction with `emotion` + `physical` + silence beats between sentences

This is what separates a generic AI-talking-head from a character that actually feels intentional. Read all four sub-sections below ([3.0] founder voice, [3a] character voice profile, [3b] beats, [3c] transitions, [3c.1] acting energy, [3d] full JSON) before writing.

### [3.0] Founder voice — write a PITCH, not a feature list

The single most common failure mode in this skill is dialogue that reads like a marketing-page bullet list ("It can reason. Code. Even write your emails. No proxies. No selectors. No maintenance. Plug it into LangChain. LlamaIndex. MCP. Twenty-four thousand stars on GitHub. MIT licensed. Production-grade.") — clean copy, but it's not how a founder talks. Field feedback: *"the script sounds like a list of features, not like a founder would sell their product on camera."*

Real founders pitching their own product on camera use:
- **First-person ownership** — "I built", "we shipped", "we use it ourselves", "honestly we just want this everywhere"
- **A personal stake or origin moment** — Act 1 should reference a frustration the founder lived through, NOT the product abstractly. "Every time I tried building X, I hit the same wall" beats "X is hard."
- **Conversational connectives** — "look", "honestly", "the thing is", "so", "actually", trailing "..." for thinking. These are throwaway words in writing but the breath of natural speech.
- **A "bet" framing for the product** — "what if X just worked?", "we asked ourselves", "the whole idea was". Founders frame their product as an answer to a question they asked themselves, not as a list of capabilities.
- **One concrete anchor** — a specific number, a specific time, a specific scenario. "24 thousand devs starred it last year" beats "it's popular." "At 3 AM the layout breaks" beats "scrapers are unreliable."
- **Invitation-energy CTA** — "come try us", "go play with it", "we just want it everywhere". NOT "stop scraping. start extracting." (that's a Don Draper tagline, not a founder).

**Banned patterns** (each was empirically called out by the user, do not repeat):

| ❌ Banned pattern | Example | Why |
|---|---|---|
| Triple-negation chant | "No proxies. No selectors. No maintenance." | Feels like a marketing chant, not human speech |
| Capability staccato | "It can reason. Code. Even write your emails." | Reads as a feature checklist |
| Integration-list-as-pitch | "Plug it into LangChain. LlamaIndex. MCP." | Listing integrations is fine ONCE in passing — never as a 3-beat hook |
| Tagline closer | "Stop scraping. Start extracting." | Pure ad-copy. Founders close with invitation, not a slogan |
| Specs-as-pitch | "MIT licensed. Production-grade." | Specs go in the README, not the founder's mouth on camera |
| "Just" as filler in a list | "Just one API call. Just any URL. Just structured JSON." | "Just" repeated reads as marketing emphasis, not natural speech |

**Allowed patterns** (use these instead):

| ✅ Pattern | Example |
|---|---|
| Personal-stake hook | "Honestly — every time I tried building X, same thing happened. ..." |
| "What if" framing | "So we built Y. The whole idea was: what if Z just worked?" |
| One concrete claim | "Last year we hit 24 thousand stars. People are plugging us in everywhere." |
| Casual aside on pain | "Hand it a URL. Get clean structured data. The layout changes? Doesn't matter." |
| Invitation closer | "If your agent needs to actually see the live web — come try us." |

**Structure** (4 acts, ~30-40 words per act = 120-160 words total, ~50-60s spoken):

- **Act 1: Personal stake / pain.** First person. Reference a specific frustration the founder lived through. Land on the problem named cleanly.
- **Act 2: The bet.** "So we built X. The idea was — what if [pain] just worked?" One sentence on what it actually does (URL → data, prompt → image, etc).
- **Act 3: Proof + community.** ONE specific number (stars, customers, ARR). One casual mention of integrations or where it's used. Tone: quiet confidence, not bragging.
- **Act 4: Invitation.** "If [reader's situation] — come try us. [URL]. [One inviting line]." End on warmth, not a tagline.

**Self-test before approving the script.** Read each act's dialogue out loud. If you'd be embarrassed to say it on camera as the founder, rewrite it. If it sounds like a 30-second commercial voiceover, rewrite it. If a paragraph has more than two punctuation periods in a row of short fragments, rewrite it.

### [3a] Derive `character_voice_profile` + `wardrobe_lock`

Two separate fields, both required:

**`character_voice_profile`** (3-4 lines) — how the character delivers EVERYTHING: cadence, default expression, signature gestures, hand habits, pause behavior, when smiles arrive. Look at `brief.tone` + the character reference image (`character_image_url` or your generated founder ref) + `product_type`. This is an actor's "circumstance" — not what they're saying, but who they are. It carries through all 4 acts so consistency feels intentional, not accidental.

**`wardrobe_lock`** (1 sentence) — what the character is wearing in every act. SeeDance reads @Image1 fresh for each 15s generation and may interpret different clothing between acts. The wardrobe_lock sentence is repeated verbatim in every act's prompt to keep clothing consistent. Read what the founder is wearing in the reference photo and describe it explicitly. Example: *"wearing the same charcoal hoodie over a dark band tee throughout all 4 acts, black-framed glasses on"*. Without an explicit wardrobe lock, later acts can invent different clothing even when the first act matches @Image1.

**Tonal-template starters** (orchestrator picks/customizes from the brief tone):

| `brief.tone` | Default cadence | Face | Hands | Pauses |
|---|---|---|---|---|
| `casual` | conversational, like explaining to a friend at coffee | slight smirk default, eyebrow flicks on reveals | open out flat on big claims, hand to chin when thinking | held eye contact instead of filling silence |
| `playful` | light staccato, expressive | mischief lives near the eyes, frequent eyebrow flicks, smiles arrive a beat after the punchline | light shoulder bounces, animated count-on-fingers | brief pauses with knowing looks |
| `professional` | measured pace, deliberate | soft direct eye contact, restrained smile | hand positions deliberate not constant, single open palm gesture | confident silences, doesn't fill |
| `technical` | analytical, slightly slower | analytical default, eyes cycle to think then return on landing | hand-to-chin thinking gesture, points to imaginary diagrams | thinking-pauses, eyes go up-left |
| `disruptive / edgy` | staccato, clipped sentences with sudden pauses | dry deadpan default, mischievous grin breaks through then disappears | body stays still, the FACE does the work | sharp pauses, slight head tilts |

**Worked example — developer-tool founder (casual tone, 3D Pixar 20s woman)**:
> "Casual confidence, like explaining the product to a friend at coffee. Slight smirk default. Eyebrow flicks on key reveals. Hand goes to chin when thinking, opens out flat on the big 'meet the A P I' claim. Pauses with held eye contact rather than filling silence. Lands punchlines deadpan and lets a small smile arrive a beat after."

**Worked example — streetwear founder (playful/edgy tone)**:
> "Sharp dry wit. Talks fast in clipped sentences with sudden pauses. Default slight smirk with one raised eyebrow. Eye-rolls on the pain points ('boring', 'generic'). Mischievous grin breaks through on punchlines but disappears immediately. Hands stay mostly still — the FACE does the work."

### [3b] Per-line `beats[]` — line-level direction, not act-level

Each shot's dialogue is broken into `beats`. Each beat is one short sentence (or a deliberate silence) with its own `emotion` + `physical` direction. Silence between beats is part of the performance — fill it with held looks, micro-expressions, gesture transitions.

A beat with `text: "(beat)"` is silent (no spoken text) — it just describes what happens visually during the natural pause between sentences. Use these between dialogue beats that need a held moment for emphasis.

When the SeeDance prompt is built in step [5], beats become the per-shot acting direction (the dialogue text without `(beat)` markers becomes the `<<<voice_1>>>` payload).

### [3c] `transition_from_prev` — choreograph continuous camera motion between shots in the same clip

**The fundamental SeeDance limitation**: each 15s SeeDance generation renders ONE virtual environment with ONE virtual camera. When a multi-shot prompt declares "Shot C, then Shot A" without specifying a continuous camera move between them, SeeDance defaults to *re-framing* the same camera position (zoom or crop). The result reads as a jump zoom, not a real cut — same background, character at different sizes.

**The fix**: every shot beyond the first in an act must declare a `transition_from_prev` field — a one-line description of the *continuous camera motion* that takes us from the previous shot's framing to this one. SeeDance then has to render an actual move-through-space, which means different parts of the room appear behind the character across the clip.

Pattern: name the camera's start position, name where it ends up, name the move that connects them. Movement verbs that work: dolly, pull back, push in, orbit, arc, glide, crane up, crane down, tilt up, tilt down, drift left/right.

Examples:

| `transition_from_prev` | Effect |
|---|---|
| "Camera pulls back and arcs left, revealing the brick wall and standing desk behind her now in frame" | Real spatial change — different background portion |
| "Push past the phone screen into a closer framing of her face — the room blurs behind her" | Continuous motion using rack focus + dolly |
| "Camera glides clockwise around her at a steady distance, picking up the whiteboard and plants on the new side" | Orbit reveals new background |
| "Pull back from her hands holding the phone to a medium shot, then drift right toward the window light" | Two-step continuous move |
| ❌ "Cut to medium shot" / ❌ "Now we see her in a medium shot" | These don't describe motion — SeeDance falls back to same-position re-frame |

**The first shot in an act has no `transition_from_prev`** — it establishes the framing. Every subsequent shot in that act gets one.

**SeeDance can do hard cuts within a single 15s clip when prompted explicitly.** Write `Hard cut:` between time-coded sub-shots (instead of `Transition:`) for distinct framing changes — SeeDance honors this and renders a real cut, not a re-frame. Reserve `Transition:` for continuous-motion handoffs where you want the camera to glide between framings. Pattern: hard cuts feel like a real edited piece (different framings, different camera angles, different acting energy); transitions feel like a single moving long take.

### [3c.1] Acting energy floor — every beat needs explicit body movement

A frequent failure mode: beats are written with only facial micro-expressions ("slight nod", "eyebrow flick", "eyes hold camera"). SeeDance renders this as a near-frozen founder — eyes barely move, no presence. Result reads as "static, frozen, no excitement."

Rule: every beat's `physical` field needs at least one of:
- A hand or arm gesture (open palm, count on fingers, dismissive flick, point at self/camera, hand to chest, wider arm sweep, hand-to-temple thinking)
- A torso shift (lean forward, lean back, slight body turn, shoulder shift)
- A head action LARGER than a micro-flick (turn left/right and back, tilt 8°+, slow head shake, head bob on rhythm)
- A directional eye flick combined with eyebrow movement (look down then snap up to camera, etc.)

Facial-only beats are acceptable only for:
- Silent `(beat)` markers between spoken sentences (those are *meant* to be still — the held look is the point)
- Final landing beat at end of an act when the camera is already moving (camera does the work)

When you write the SeeDance prompt, make sure the assembled "Acting beats" block reads physically dense — if you scan it and see five beats in a row that all say "slight nod" or "small smirk" with no other movement, the founder will look frozen. Rewrite with bigger movement.

### [3d] Script JSON

```json
{
  "product_type": "<from step [2]>",
  "character_voice_profile": "Casual confidence, like explaining to a friend at coffee. Slight smirk default. Eyebrow flicks on key reveals. Hand goes to chin when thinking, opens out flat on big claims. Pauses with held eye contact rather than filling silence. Lands punchlines deadpan, lets a small smile arrive a beat after.",
  "segments": [
    {
      "act": 1,
      "shots": [
        {
          "type": "A",
          "asset_index": null,
          "beats": [
            { "text": "Assistants are brilliant.", "emotion": "declarative respect — say it like she means it", "physical": "soft direct eye contact, slight nod" },
            { "text": "(beat)", "physical": "subtle smirk arrives, eyes hold camera" },
            { "text": "But it's also kind of...", "emotion": "playful pivot, ellipsis hangs", "physical": "slight head tilt right, eyes drift up briefly on the ellipsis" },
            { "text": "shapeless.", "emotion": "deadpan landing", "physical": "eyes return to camera, single dismissive shrug" }
          ]
        },
        {
          "type": "B",
          "asset_index": null,
          "transition_from_prev": "Camera pushes in slowly from the medium framing into a tighter close-up, drifting slightly off-axis to her right so a different slice of the brick wall and window light is visible behind her",
          "beats": [
            { "text": "No face. No voice. No personality of its own.", "emotion": "staccato dismissal", "physical": "small head shake on each, eyebrow flick on 'personality'" },
            { "text": "(beat)", "physical": "held look, eyes lock camera, soft smile starts to arrive" },
            { "text": "Just an empty assistant waiting for orders.", "emotion": "flat, slightly resigned deadpan", "physical": "neutral face" },
            { "text": "(beat)", "physical": "soft confident smile arrives, lean forward begins" },
            { "text": "That's about to change.", "emotion": "grounded conviction, the turn", "physical": "lock eyes, single confident nod on 'change'" }
          ]
        }
      ]
    },
    {
      "act": 2,
      "shots": [
        {
          "type": "C",
          "asset_index": 0,
          "reveal_beat": "The character holds her phone up toward camera at chest height, screen facing the viewer. The screen is a clean blank neutral placeholder reserved for the real product UI overlay in step [5.5]; do not render readable UI text, brand wordmark, or fake app chrome.",
          "beats": [
            { "text": "Meet the A P I.", "emotion": "introduction with quiet pride", "physical": "phone lifts to camera, eyes flick from screen to lens" },
            { "text": "One workflow that gives your product a face, a voice, and a story.", "emotion": "warm steady build", "physical": "free hand counts the three on fingers — face, voice, story" }
          ]
        },
        {
          "type": "A",
          "asset_index": null,
          "transition_from_prev": "Camera pulls back from the phone and arcs slightly left, the phone lowers out of frame as we end on a medium shot of the character with the desk and whiteboard now visible behind her",
          "beats": [
            { "text": "And the ability to make videos, images, audio.", "emotion": "expanding the promise", "physical": "open-palm gesture sweeps wider on each item" },
            { "text": "Right inside the chat.", "emotion": "the grounding kicker", "physical": "hand lands flat, eyebrows up, slight smile arrives" }
          ]
        }
      ]
    },
    {
      "act": 3,
      "shots": [
        {
          "type": "D",
          "asset_index": null,
          "beats": [
            { "text": "Setup takes thirty seconds.", "emotion": "matter-of-fact reassurance", "physical": "walks past a desk, glances at a laptop briefly" },
            { "text": "Open the dashboard, paste the URL, sign in.", "emotion": "quick rhythmic checklist", "physical": "counts three on fingers as she walks" }
          ]
        },
        {
          "type": "E",
          "asset_index": 1,
          "reveal_beat": "Close-up of hands holding phone. The screen is a clean blank neutral placeholder reserved for the real product UI overlay in step [5.5]; do not render readable UI text, brand wordmark, or fake app chrome.",
          "transition_from_prev": "Camera dollies in fast past her shoulder to land on a tight close-up of her hands and the phone, the loft background drops fully out of focus",
          "beats": [
            { "text": "Your app becomes a guide.", "emotion": "the soft surprise reveal", "physical": "small smile at the phone, then up to camera, eyes warm" }
          ]
        },
        {
          "type": "A",
          "asset_index": null,
          "transition_from_prev": "Camera pulls back and tilts up from the phone to find her face in a medium shot, the brick wall and afternoon light now visible behind her on a different side of the loft than Shot D",
          "beats": [
            { "text": "Or whoever you build.", "emotion": "casual aside", "physical": "small shrug, slight smirk" },
            { "text": "(beat)", "physical": "held look, smirk fades into warm sincerity" },
            { "text": "Now talk to her like a person.", "emotion": "the real point — quiet conviction", "physical": "single nod on 'person', eyes hold" }
          ]
        }
      ]
    },
    {
      "act": 4,
      "shots": [
        {
          "type": "F",
          "asset_index": null,
          "beats": [
            { "text": "Skills bundled in.", "emotion": "casual confidence, intro to a list", "physical": "slight tilt of the chin, knowing look" },
            { "text": "Podcasts. Explainer videos. U G C ads.", "emotion": "rhythmic three-beat list", "physical": "small nod on each, eyebrow flick on 'U G C'" },
            { "text": "All from chat.", "emotion": "the grounding tag", "physical": "open-palm gesture lands flat, slight smile arrives" }
          ]
        },
        {
          "type": "B",
          "asset_index": null,
          "transition_from_prev": "Camera pushes in slowly from the wider brand-context framing into an intimate medium close-up; the environment recedes into soft bokeh, the character fills more of the frame",
          "beats": [
            { "text": "So stop wrestling with generic A I.", "emotion": "direct address, low-key challenge", "physical": "raised eyebrow, slight head tilt" },
            { "text": "(beat)", "physical": "held look, smirk grows" },
            { "text": "Give it a real presence.", "emotion": "the brand line, said with certainty", "physical": "lean slightly into camera, lock eyes" },
            { "text": "Start at example dot com slash demo.", "emotion": "warm CTA, the invitation", "physical": "soft confident smile, single closing nod on 'demo'" }
          ]
        }
      ]
    }
  ]
}
```

**Per-shot asset assignment rules**:
1. **For digital products**: only shots `C` and `E` get an `asset_index` (phone-reveal moments). These are overlay pointers for step [5.5] and are excluded from the Seedance reference image array. Other shots show the founder without a specific UI reference.
2. **For physical products**: any shot where the product is visible in frame gets an `asset_index`. The asset is the source of truth for what that product looks like. Acts can reuse the same asset across multiple shots, OR show a different asset per shot to demo product variety.
3. **For service products**: no `asset_index` anywhere — the script relies on dialogue + environment.

Every non-null `asset_index` must come from `usable_product_assets[*].asset_index`. Never assign a logo-only, hero-only, infographic, abstract brand, or `other` asset index to a product reveal shot. When using product details in dialogue, prefer `usable_product_assets[*].analysis.key_elements` and `usable_product_assets[*].analysis.visible_copy` so the spoken pitch tracks the same real product artifact shown on screen.

**Reference image array per act** = the union of Seedance-safe asset URLs across that act's shots. Digital `digital_screen` assets are not Seedance-safe; they stay overlay-only for step [5.5]. Within the SeeDance prompt, refer to non-digital assets by their position in the array as `@Image3`, `@Image4` (positions 3+ — positions 1 and 2 are always character + location refs). The orchestrator computes this mapping when building the prompt in step [5].

**Dialogue rules** — TOTAL across all 4 acts must read aloud in 55–60s (~150 wpm = ~150 words total, ~37 per act). Short, punchy, speakable. Avoid em-dashes (founders don't speak them). Use natural contractions. **Reference the user's actual product features** (drawn from `usable_product_assets[*].analysis.key_elements` and `usable_product_assets[*].analysis.visible_copy`), not invented ones.

### TTS pronunciation rewrites

SeeDance's native lip-sync TTS reads `<<<voice_1>>>` text literally — it has no semantic awareness that "Ari" is a name, "Vercel" is pronounced "ver-SELL", "UGC" is an acronym to spell, or "example.com" is a URL. Rewrite the dialogue text the way you want it *pronounced*, then submit. Apply these substitutions:

| Pattern | Wrong (literal) | Correct (rewrite for TTS) |
|---|---|---|
| Names ending in `-i` | "Ari" → "ah-REE" | **"Airy"** (or "Tess" / "Mae" / "Sam" — phonetic) |
| Names with unfamiliar spellings | "Aoife" → confused | **"Eefa"** (phonetic) |
| Non-phonetic product / brand names from `state.brand.name` or `brief.product_name` | "Vercel" → "Verkon"; "Linear" → "Lineer" | Create a TTS-only phonetic alias, e.g. **"ver-SELL"**, and use it whenever the brand is spoken inside dialogue / `<<<voice_1>>>`. |
| Acronyms meant to be spelled out | "UGC" → "uhg" / "ugg"; "MCP" → "mehp" / silent | **"U G C"** / **"M C P"** (single spaces between letters) |
| Acronyms spoken as words | "NASA" → "nasa" ✅ (already correct); "IKEA" → "ikea" ✅ | leave alone |
| Domain dots | "example.com" → "examplecom" | **"example dot com"** |
| URL slashes / paths | "example.com/API" → "examplecom-api" | **"example dot com slash A P I"** |
| Symbols | "$50" → silent; "@user" → "at user" or silent | **"fifty bucks"** / **"at-sign user"** |
| Numbers in weird formats | "2026" → ambiguous | **"twenty twenty-six"** for years; **"two thousand"** for round numbers |

When in doubt about how a brand pronounces an acronym (NASA vs N.A.S.A.) or non-obvious product name, check the brand's own website / videos. Default to spelled-out letters for unclear acronyms and a simple phonetic alias for non-phonetic names. For domains that include the brand, combine both rewrites: `Vercel.com` becomes `ver-SELL dot com` in the `<<<voice_1>>>` payload.

**Worked example** — original script vs TTS-safe rewrite:

```
Original:  "UGC ads. All from chat. Launch the API. Start at example.com/API."
TTS-safe:  "U G C ads. All from chat. Launch the A P I. Start at example dot com slash A P I."

Original:  "Your app becomes Ari."
TTS-safe:  "Your app becomes Airy."

Original:  "Vercel ships at vercel.com."
TTS-safe:  "ver-SELL ships at ver-SELL dot com."
```

Keep the rewrites in the *dialogue text* only — your script JSON's `dialogue` field is what flows into the SeeDance prompt verbatim and then into each `<<<voice_1>>>` block. Visual surfaces keep the canonical original spelling: `state.brand.name`, `brief.product_name`, product UI overlays, wordmarks, end card text, URLs, filenames, and QA expectations must stay unchanged. Never replace deterministic visual text with the phonetic alias.

## Shot type reference

Each shot has variants depending on `product_type`. Pick the variant that matches.

⚠️ **Avoid film-industry shot terminology that SeeDance interprets literally.** SeeDance reads named shot types as a literal recipe — including any *implied subjects* the term carries. Specifically:
- ❌ "Two-shot" → adds a SECOND PERSON to the frame (term means "shot with two subjects" in film, but SeeDance just sees "two" + "person").
- ❌ "Three-shot" — same trap.
- ❌ "Over-shoulder" / "OTS" → adds a phantom shoulder/back-of-head in the foreground for the character to interact with. The character then performs *toward that phantom person*, not toward the camera.
- ❌ "Master shot" — can be misread as "the master / their boss".
- ✅ "Medium shot", "Close-up", "Wide" are safe; they're commonly used colloquially.

The fix in every case is **plain language about what the camera sees**, not film vocabulary that implies extra subjects. Examples:
- "Over-shoulder reveal" → "the character holds her phone up toward camera, screen facing the viewer at chest height"
- "Two-shot" → "wide framing of the character with [product/logo/environment] in frame"
- "POV" → "low camera angle from the character's eyeline"

| Shot | All variants | Camera |
|------|-------------|--------|
| A | Medium shot, waist up, the character centered. (No product in frame, OR if `physical_apparel`: the character is WEARING one of the brand's shirts — pass the asset as ref and add reveal_beat.) | slow subtle push-in dolly |
| B | Medium close-up, chest up, intimate. (No product, OR if `physical_apparel`: shirt visible from neckline, reference the asset.) | gentle handheld breathing motion |
| C | **Phone/product reveal — direct to camera.** `digital` → the character holds her phone up toward camera at chest height, screen facing the viewer, with a blank neutral screen placeholder for step [5.5]'s real UI overlay. (NOT "over-shoulder" — that vocabulary triggers a phantom person.) `physical_apparel` → the character holds a t-shirt up toward camera, print facing the viewer, matching @ImageN. `physical_object` → the character lifts the product up toward camera. `consumable` → the character holds the package toward camera. | slow push-in toward the held object |
| D | Wide + environment, full body in expansive space. (No specific product moment.) | slow tracking shot, parallax depth |
| E | **Close-up reveal.** `digital` → close-up of hands holding phone with a blank neutral screen placeholder for step [5.5]'s real UI overlay. `physical_apparel` → close-up of hands holding the shirt fabric, design clearly visible. `physical_object` → close-up of the product in hand, detail shot. `consumable` → close-up of using/eating/drinking the product. | subtle rack focus, slow tilt up |
| F | **Brand context shot.** Wider framing of the character with product/environment context surrounding them. `digital` → the character in a brand-styled environment with no readable product UI or wordmark. `physical_apparel` → the character wearing the brand's t-shirt, the print clearly visible mid-frame. `physical_object` → the character with the product on a desk/shelf. | slow pull-back, gentle zoom-out |

## [4] Founder + custom location reference images

Prepare `character_url` before any SeeDance call:

- If `founder_photo` is an HTTPS URL, set `founder_photo_url = character_url = founder_photo`.
- If `founder_photo` is a local path, upload it with `upload_asset`, then set `founder_photo_url = character_url = public_url`.
- If `founder_photo` is `generate`, call `generate_image` and use the returned URL:

```
generate_image(
  prompt: "<founder vibe>. Professional founder portrait, clean studio lighting, sharp focus on face, confident expression, suitable as character reference for video generation.",
  aspect_ratio: "3:4",
  resolution: "2K"
)
```

Handle location only when the user supplied a custom location:

- If `location_image_url` is an HTTPS URL, set `location_url = location_image_url`.
- If it is a local path, upload it with `upload_asset` and set `location_url = public_url`.
- If it is a text description, generate a custom location reference with `generate_image`.
- If no custom location was supplied, do nothing here. Step [4.5] generates the default brand-accent backdrop after `state.brand` exists.

Save the resulting URLs into `state`. If SeeDance later rejects the founder ref on content policy, see "Known infra quirks" — re-roll with stronger stylization.

## [4.5] Brand-kit ingestion (always — Stage 0 guarantees `brand_kit_path`)

`brand_kit_path` is required by Stage 0 — either user-supplied or built first with `build-a-brand`. Parse it once and reuse across the end card and the lower-third. If the folder is missing in interactive mode, ask the user to provide or rebuild the brand kit before continuing. In the non-interactive fast lane, try the `build-a-brand --quick` branch first; if that cannot produce a kit, stop once with a single compact missing-fields list.

Preferred source is `brand.json` when present. Otherwise extract from a `build-a-brand` export:
- `brand.md` for name, tagline, voice, typography names, and logo descriptions.
- `tokens/tokens.json` for colors and font tokens.
- `logo/` assets for wordmark, symbol/icon, and lockups.

Extract into `state.brand`:

| `state.brand` field | Source | Notes |
|---|---|---|
| `name` | `brand.json.name` or `brand.md` quick reference | brand display name |
| `wordmark_path` | `logo.wordmark.path` or best raster `logo/wordmark/*.{png,jpg,jpeg,webp}` | upload local raster asset via `upload_asset`, save `public_url` as `state.brand.wordmark_url`; do not upload SVG |
| `icon_url` | `logo.icon_mark.path` or best raster `logo/symbol/*.{png,jpg,jpeg,webp}` | upload local raster asset via `upload_asset`, save `public_url` as `state.brand.icon_url`; do not upload SVG |
| `colors.primary` | palette role `ink_primary`, `surface_dark`, or `tokens.color.text` | text and border color |
| `colors.surface` | palette role `surface_page_bg`, `surface_white`, or `tokens.color.background` | page/background color |
| `colors.accent` | CTA/primary brand color from palette or `tokens.color.primary` | end-card CTA pill bg + lower-third accent |
| `colors.highlight` | secondary light/highlight color from palette or tokens | lower-third border / highlight |
| `fonts.display_family` | typography display token or `brand.md` | use as-is if available; fall back to Space Grotesk |
| `fonts.text_family` | typography body/text token or `brand.md` | fall back to system sans |
| `fonts.mono_family` | typography mono token if present | fall back to Space Mono |

**Upload step is required** when the brand-kit assets are local files. Without public wordmark/icon URLs, the HTML rendered by `render_html_animation` can't reach them. Use the MCP `upload_asset` flow with raster logo files only and save the returned `public_url` values on `state.brand`. `upload_asset` rejects `image/svg+xml`; if the best logo is an SVG, pick the sibling PNG export from the brand kit or rasterize the SVG to PNG via `html_to_png` by inlining the SVG inside an HTML `<svg>` block and using the returned PNG `public_url`.

**Brand-accent backdrop default location** — when `location_url` was not set by Step [4], render a solid-color PNG via `html_to_png` using `state.brand.colors.accent`. Match the requested video aspect so the reference is not cropped later:

| `aspect_ratio` | Backdrop size |
|---|---|
| `16:9` | 1920×1080 |
| `9:16` | 1080×1920 |
| `1:1` | 1080×1080 |

Save the returned `file_url` as `location_url`. This produces the clean studio-shoot aesthetic — character against a flat seamless wall in the brand's own accent color, no furniture or background detail. This is more reliable than AI-generated office sets and renders SeeDance reliably.

```
html_to_png(
  html: "<body style='margin:0;background:{accent}'></body>",
  format: "png",
  mode: "sync",
  raster_options: { viewport_px: { width: W, height: H }, device_scale: 1 }
)
# Save result.file_url as location_url
```

## [5] Generate 4 SeeDance acts in parallel

**CRITICAL**: Step [5] requires `generate_reference_video` (multi-ref). The `@Image1` / `@Image2` / `@Image3` tokens in this skill's prompt template are **only resolved by** `generate_reference_video`. If you call `generate_video` (single-image i2v) by mistake, `@ImageN` tokens are silently ignored and Seedance will hallucinate UI from prompt text alone, typically misspelling the product name. Stop and fix the tool call before firing any paid video generation.

For `product_type: "digital"`, this is now a style/gesture generation step, not the final readable UI step. Do not ask Seedance to spell the product name, render a readable brand wordmark, or reproduce product-screen copy. Phone reveals must ask for a blank neutral screen placeholder, because real product UI is composited in step [5.5]. Do not pass `digital_screen` assets in `reference_images`; any `digital_screen` asset index is an overlay pointer for step [5.5] only, even if a mixed or explicitly non-digital run also has physical assets.

For each act, **collect the union of `asset_index` values across all shots in that act** to build the `reference_images` array:

```
act_asset_indices = unique(shot.asset_index for shot in act.shots if shot.asset_index !== null)
act_asset_entries = usable_product_assets.filter(entry.asset_index in act_asset_indices)
if act_asset_entries.length !== act_asset_indices.length: stop; a shot references an unusable/missing asset_index
seedance_asset_entries = act_asset_entries.filter(entry => entry.asset_type !== "digital_screen")
act_asset_urls    = [entry.asset_url for entry in seedance_asset_entries]
reference_images  = [character_url, location_url, ...act_asset_urls]
```

The asset entry's position in `reference_images` determines its `@ImageN` token (positions 1, 2 are character + location; usable product assets start at position 3). When writing the prompt, map each non-digital shot's `asset_index` to its matching `seedance_asset_entries` position. For any `digital_screen` asset, do not reference an `@ImageN` token in the Seedance prompt; use the blank phone-screen placeholder language and let step [5.5] consume the original `act_asset_entries` entry.

### Prompt template

**Refer to the character through the `@Image1` reference, not descriptive prompt prose.** When the prompt says both "young creative streetwear founder" and `@Image1` is the character ref, the two descriptions can fight — SeeDance may try to satisfy both by inventing a second figure. Same rule applies to the location and `@Image2`. Let the reference images carry the visual identity.

Each act's prompt has three layers, top to bottom:

1. **Character + location identity** (always the same opening line).
2. **Character voice** — the act prompt repeats `script.character_voice_profile` verbatim. This carries the actor's personality through every shot.
3. **Per-shot blocks** — each shot gets its composition (or `reveal_beat` if defined), then a per-line "Acting beats" list built from the shot's `beats[]`, then the dialogue inside `<<<voice_1>>>`.

⚠️ **The opener line, `WARDROBE LOCK:`, `Background context:`, `<<<voice_1>>>`, `Transition:` / `Hard cut:`, and the closing `Native lip-synced dialogue audio, no music overlay.` line are all load-bearing** — each is documented in `## Load-bearing phrases` near the bottom with the specific failure mode it prevents. Paraphrasing any of them silently breaks the recipe (literal backdrop, sung lyrics, jump zooms, wardrobe drift, etc.). Leave them verbatim; the connective prose around them is yours to compose.

Template:

```
The character (matching @Image1) in a setting whose visual style, palette, lighting and materials match @Image2.

CHARACTER VOICE: {script.character_voice_profile}
WARDROBE LOCK (verbatim across all 4 acts): {script.wardrobe_lock}

Shot {first}: {if shot.reveal_beat exists: shot.reveal_beat ELSE: composition + camera from Shot table}. Background context: {distinct physical position in the space — which wall / window / feature is behind the character}.
Acting beats:
  • "{beat[0].text}" — {beat[0].emotion}; {beat[0].physical}.
  • (silence) — {silence beat physical}.
  • "{beat[N].text}" — {beat[N].emotion}; {beat[N].physical}.
<<<voice_1>>>{joined beat texts excluding (beat) markers, with periods and commas as written}<<<voice_1>>>

[If 2+ shots in this act:] Transition: {shot[1].transition_from_prev}.
Shot {second}: {composition or reveal_beat}. Background context: {a DIFFERENT physical position from Shot {first} — different wall / different angle / different background feature}.
Acting beats: ...
<<<voice_1>>>...<<<voice_1>>>

[If 3 shots:] Transition: {shot[2].transition_from_prev}.
Shot {third}: ... Background context: {a THIRD distinct physical position — must be visually different from Shots {first} and {second}}.

Native lip-synced dialogue audio, no music overlay.
```

Notes on the template:
- Open with **"The character (matching @Image1) in a setting whose visual style ... match @Image2"** — never "inside the location matching @Image2". SeeDance reads the LITERAL backdrop from @Image2 if you say "inside the location" — see Known infra quirks.
- Don't describe the character in prose — SeeDance reads visual identity from `@Image1`. EXCEPTION: lock wardrobe explicitly via the `WARDROBE LOCK` line (e.g. "wearing the same charcoal hoodie over a dark band tee throughout"). @Image1 alone doesn't lock wardrobe across separate 15s generations.
- Don't add aesthetic adjectives that contradict the references. If `@Image1` is a 3D Pixar-style character, don't add "photorealistic" anywhere in the prompt.
- **The CHARACTER VOICE + WARDROBE LOCK lines appear once per prompt, before the shots.** They prime SeeDance for the actor's whole vibe + clothing continuity.
- **Each shot block includes a `Background context:` line** describing a distinct physical position in the space — different wall, different window, different background feature than the other shots in this act and ideally distinct from the other acts. This forces SeeDance to render scene variety while keeping the brand aesthetic anchored to @Image2.
- **`(beat)` markers stay OUT of the `<<<voice_1>>>` payload.** They're acting direction only — the natural pause between sentences in the dialogue text is where they happen.
- **Every shot beyond the first in an act gets a `Transition: …` line** built from `shot.transition_from_prev`. This narrates the camera move between framings, forcing SeeDance to render real spatial motion (different parts of the room behind the character) instead of an unmotivated re-frame that reads as a jump zoom.

### Worked example — `physical_apparel`, Act 2 (with voice + beats)

Act 2 has shots `[C, A]`. Shot C has `asset_index: 0` and a reveal_beat about the search-history t-shirt. Shot A has no asset_index. Asset 0 = `@Image3`. Character voice profile is the streetwear-founder example from step [3a].

```
The character (matching @Image1) in a setting whose visual style, palette, lighting and materials match @Image2.

CHARACTER VOICE: Sharp dry wit. Talks fast in clipped sentences with sudden pauses. Default slight smirk with one raised eyebrow. Eye-rolls on the pain points. Mischievous grin breaks through on punchlines but disappears immediately. Hands stay mostly still — the FACE does the work.
WARDROBE LOCK: wearing the same charcoal-washed brand graphic tee under an unbuttoned indigo-denim chore jacket throughout all 4 acts.

Shot C: The character lifts a charcoal-washed graphic tee toward camera, holding it flat at chest height. The shirt design exactly matches @Image3 — 'I SAW YOUR SEARCH HISTORY' with shocked cat illustration in bold white type. Match the print exactly, do not invent. Camera: slow lateral arc pan around toward eyeline. Background context: standing near the apparel rack against the brick wall on the right side of the loft, soft midday window light from camera-left.
Acting beats:
  • "You know that thing you almost typed?" — knowing low-key accusation; raised eyebrow on 'almost typed', slight head tilt.
  • "That weird search?" — held look, eyebrow stays up, hint of smirk arrives.
  • (silence) — beat lands, smirk grows, eyes flick to lens.
  • "Your cat saw it." — mischievous deadpan; lifts shirt slightly higher, single confident nod.
<<<voice_1>>>You know that thing you almost typed? That weird search? Your cat saw it.<<<voice_1>>>

Transition: Camera pulls back from the held shirt and arcs slightly left, the shirt lowers out of frame as we end on a medium shot with the apparel rack and brick wall now visible behind her.
Shot A: Medium shot, waist up, the character centered, looking at camera. Camera: slow subtle push-in dolly.
Acting beats:
  • "We turned it into a t-shirt." — matter-of-fact reveal; eyebrows up, slight smile arrives.
  • " — graphic tees with attitude." — the brand-line punctuation; smirk lands on 'attitude', eyes hold.
<<<voice_1>>>We turned it into a t-shirt — graphic tees with attitude.<<<voice_1>>>

Native lip-synced dialogue audio, no music overlay.
```

### Physical product consistency across shots

For `physical_apparel`, if the character is **wearing** the brand's product across multiple acts (e.g. acts where no specific product reveal happens but the character is still in a brand t-shirt), pick one hero shirt asset and pass it to those acts too with prompt language like *"the character is wearing the t-shirt from @Image3 — print matches exactly"*. Otherwise SeeDance invents a generic-looking shirt, defeating the asset coverage goal.

### Fire all 4 acts in parallel — 3 sub-shots per act

Fire all 4 acts in parallel in a single tool batch. Every act prompt should contain 3 time-coded sub-shots; single-shot 15s clips render as static, frozen-looking founder regardless of how detailed the prompt is. If a run looks "very static, no body language, camera work boring", the fix is decomposing each act into 3 time-coded sub-shots within the prompt.

**Default decomposition: 3 sub-shots per act**, sized by dialogue density (e.g. `(0-4s)`, `(4-9s)`, `(9-15s)`).

Each sub-shot needs:
1. **A different camera framing** — never two consecutive sub-shots with the same shot type. Mix medium / close-up / wide / lower-angle. The user reads variety as production value.
2. **A different camera motion** — push-in, pull-back, lateral arc, orbit, handheld, static-held, rack-focus. Not all "slow push-in".
3. **A different physical position in the space** — see Location-reference rule in "Known infra quirks". Each shot must describe a different wall / window / feature visible behind the character so SeeDance moves through the space instead of reproducing one literal backdrop.
4. **An ENERGETIC physical action per beat** — see [3c.1] above. Hand gestures, leans, head turns, shoulder shifts. No facial-only beats.
5. **The dialogue sub-portion for that window**, wrapped in `<<<voice_1>>>...<<<voice_1>>>` tokens inside the shot's block.

SeeDance firing pattern:

```
generate_reference_video(
  provider: "seedance",
  resolution: "1080p",
  aspect_ratio: "16:9",
  duration: 15,
  seed: 101,                   # unique per act (101, 202, 303, 404) — busts the idempotency cache
  sound: true,                 # native lip-sync from each <<<voice_1>>> block
  reference_images: [character_url, location_url, ...assets_for_this_act],
  prompt: <full prompt — see template in section above, 3 time-coded sub-shots inline>
)
# ... × 4 acts, all in the same message ...
```

Notes:
- Each act runs ~3-8 min on SeeDance. If generation completes asynchronously, follow the MCP tool's returned status handle until the act reaches a terminal state.
- The full prompt (opening line + CHARACTER VOICE + 3 sub-shots with Acting beats + `<<<voice_1>>>` per shot + Transition lines) goes in the single `prompt` parameter. SeeDance has no `shots:[]` array — the multi-shot structure is encoded in prose.
- Use unique seeds (101, 202, 303, 404) so identical-looking calls don't hash to the same cached task ID. The `seed` parameter is seedance-only.

Save the 4 returned URLs in submission order as `act_urls = [act1, act2, act3, act4]`.

## [5.5] Deterministic digital UI overlays

This step runs after all four Seedance acts are available and before step [6]. For efficiency, run the cross-act identity QA below first and use the final accepted `act_urls`; if identity QA later retries an act, discard the old overlay outputs and rerun this step. Its job is to make digital product reveals pixel-grounded: the phone / product-screen visual seen by the viewer comes from the real captured screenshot or rendered wordmark, not from Seedance.

If `product_type !== "digital"`, set `ui_grounded_act_urls = act_urls` and continue.

If `product_type === "digital"`:

1. Build `digital_reveal_shots` from every scripted shot whose type is `C` or `E`. Every scripted `C` or `E` digital reveal must have a non-null `asset_index` and that index must resolve to a `digital_screen` entry in `usable_product_assets`. If any scripted C/E digital reveal has `asset_index: null`, stop and surface the script shot; do not proceed to Seedance concat or copy raw `act_urls`. Build `digital_reveal_plan` from the validated reveal shots. Each planned overlay stores:
   - `act`, `shot`, `asset_index`, `asset_url`
   - `visible_copy` from `usable_product_assets[*].analysis.visible_copy`
   - `brand_name = state.brand.name`
   - the expected text list: exact `brand_name` plus any short, readable `visible_copy` phrases that matter for the pitch

   If `digital_reveal_plan` is empty, stop and surface the script shots plus `usable_product_assets`; do not silently ship a digital product video without real UI. If any scripted C/E digital reveal points at a missing or non-`digital_screen` asset, stop before composing. Do not copy raw `act_urls` through when a digital reveal is missing its overlay; only acts with no digital reveal shot may pass through unchanged.

2. For each unique `asset_url`, render a 15-second overlay clip with `render_html_animation` using `format: "mov"` when alpha is needed. Save the returned URL as `ui_overlay_clip_url`.
   - The HTML should place the real screenshot / captured UI inside a rounded phone-screen frame with the correct aspect ratio.
   - If the real screenshot's brand wordmark is too small to read after scaling, include an exact deterministic wordmark row using `state.brand.name`; do not invent a shorter alias.
   - Keep the overlay background transparent or visually isolated so it works as a deterministic phone/UI overlay over the generated act.

3. Composite the overlay onto each planned act with `edit_video_compose`:

```
edit_video_compose(
  base_video_url: act_urls[act - 1],
  overlays: [{
    video_url: ui_overlay_clip_url,
    position_px: <safe phone-screen or panel placement>,
    width_px: <large enough for OCR-readable brand/product UI>
  }]
)
```

Use the phone-screen placement when the generated phone target is stable. If the phone target is not stable enough to cover cleanly, use a stable overlay-panel placement that does not cover the founder's face or the caption area. Save each edited result into `ui_grounded_act_urls[act - 1]`; untouched acts copy through from `act_urls`.

4. When a short exact brand label is still needed after the compose pass, call `edit_text_overlay` on that act with `text: state.brand.name`. This is only for deterministic brand spelling, not captions. Save the updated URL back into `ui_grounded_act_urls[act - 1]`.

5. Run OCR QA on each overlaid reveal act before concat with `extract_frame` and `analyze_media`:

```
extract_frame(video_url: ui_grounded_act_urls[act - 1], time_s: <midpoint of the reveal shot>)

analyze_media(
  media: overlay_qa_frame_url,
  query: "OCR/read all visible text on the product UI or wordmark. Return JSON only: {
    \"brand_name_visible\": \"yes\" | \"no\" | \"unclear\",
    \"brand_name_exact\": \"yes\" | \"no\" | \"unclear\",
    \"visible_copy_ok\": \"yes\" | \"no\" | \"unclear\",
    \"garbled_text\": string[],
    \"misspellings\": string[],
    \"verdict\": \"clean\" | \"degraded\" | \"catastrophic\"
  }. The exact expected brand name is ${brand_name}. The exact expected visible_copy is ${visible_copy}; visible_copy_ok: "yes" only when the important expected UI copy is present/readable, or when no short visible_copy was provided. Examples like Lineer, Figoff, random letters, malformed UI copy, or AI-imagined UI copy that replaces the expected visible_copy are garbled/misspelled."
)
```

Only `brand_name_visible: "yes"`, `brand_name_exact: "yes"`, `visible_copy_ok: "yes"`, and `verdict: "clean"` can continue. If OCR says the brand is missing, misspelled, garbled, expected visible copy is missing/replaced, or `verdict` is `degraded` / `catastrophic`, stop and surface the `overlay_qa_frame_url`, `ui_overlay_clip_url`, expected `brand_name`, expected `visible_copy`, and the QA JSON. Do not proceed to step [6] with raw or AI-imagined phone text.

### Cross-act identity QA before step [6]

Before `edit_concat`, run a cross-act identity check on a single comparable visual artifact. The goal is to catch a founder swap while the bad act can still be regenerated, not after the 60s body is already stitched.

1. Extract one representative frame from each of the three sub-shot windows in every act. One frame at the middle of the act is not enough; a founder swap can happen in the first or final sub-shot and still pass.

```
identity_frame_times_s = [2, 7, 12]
for each act_urls[i]:
  for each time_s in identity_frame_times_s:
    extract_frame(video_url: act_urls[i], time_s)
# Save as act_identity_frames = [
#   { label: "act 1 shot 1", act: 1, shot: 1, time_s: 2, url: ... },
#   ...
#   { label: "act 4 shot 3", act: 4, shot: 3, time_s: 12, url: ... }
# ]
```

2. Render a single identity contact sheet with `html_to_png`. Use CSS `background-image: url(...)` for each remote image. The sheet must include thirteen labeled panels in one image: `founder reference` (`founder_photo_url` / `character_url`), then `act 1 shot 1`, `act 1 shot 2`, `act 1 shot 3`, through `act 4 shot 3`. Save the returned file as `identity_contact_sheet_url`.

```
html_to_png(
  html: "<html>... founder reference ... act 1 shot 1 ... act 1 shot 2 ... act 1 shot 3 ... act 2 shot 1 ... act 3 shot 1 ... act 4 shot 3 ...</html>",
  format: "png",
  mode: "sync",
  raster_options: { viewport_px: { width: 2200, height: 1600 }, device_scale: 1 }
)
```

3. Run one `analyze_media` call on `identity_contact_sheet_url`:

```
analyze_media(
  media: identity_contact_sheet_url,
  query: "Return JSON only: {
    \"same_founder_as_reference\": \"yes\" | \"unclear\" | \"no\",
    \"same_founder_across_acts\": \"yes\" | \"unclear\" | \"no\",
    \"wardrobe_consistent_with_lock\": \"yes\" | \"unclear\" | \"no\",
    \"bad_act_numbers\": number[],
    \"bad_frame_labels\": string[],
    \"identity_observations\": string[],
    \"verdict\": \"clean\" | \"degraded\" | \"catastrophic\"
  }
  Compare the founder reference panel against all twelve act panels: act 1 shot 1 through act 4 shot 3. Check face, hair, age, body type, and wardrobe; do not treat normal pose, expression, camera angle, or lighting changes as identity drift."
)
```

If the contact sheet cannot be rendered, stop and surface the contact-sheet failure; do not proceed with unverified identity. Only a clean `yes` / `yes` / `yes` identity QA can proceed. If the QA returns `same_founder_as_reference: "no"` or `same_founder_as_reference: "unclear"`, `same_founder_across_acts: "no"` or `same_founder_across_acts: "unclear"`, `wardrobe_consistent_with_lock: "no"` or `wardrobe_consistent_with_lock: "unclear"`, `bad_act_numbers` non-empty, `bad_frame_labels` non-empty, or `verdict: "degraded"` or `verdict: "catastrophic"`, do not proceed to concat. Retry only the bad act(s) once with the same prompt, same `reference_images`, and a new seed (`original_seed + 1000`) plus one added prompt sentence: `Identity continuity is mandatory: the on-camera founder remains the same person as @Image1 for the entire act.` After retry, extract all three frame times for the retried act(s), rebuild the full contact sheet, and rerun the same QA. If any `act_urls` entry changes after a bad-act retry, discard `ui_grounded_act_urls` and any previous overlay/OCR evidence, rerun step [5.5] against the final `act_urls`, then rerun its OCR QA before step [6]. If the retry still fails cross-act identity QA, stop and surface `identity_contact_sheet_url`, the bad act URL(s), `bad_frame_labels`, and the QA JSON; do not ship a stitched video with a different founder.

### Duration floor and partial-act recovery

All 4 act_urls are required before step [6]. Do not concat a partial act list.
Three completed acts plus the end card produce a ~50s asset, which misses the
55s duration floor and must not be reported as a successful founder video.

If one SeeDance act reaches a failure terminal, reaches `cancelled`, or is
terminal or successfully cancelled by the long-running polling contract while
other acts completed:
- Retry the missing act once with the same prompt, `reference_images`,
  `duration`, `sound`, `resolution`, and `aspect_ratio`, but a new seed
  (`original_seed + 1000`). Do not rerun successful acts.
- If the retry completes, insert that URL into the original act slot and
  continue with `act_urls = [act1, act2, act3, act4]`.
- If the retry cannot complete, stop and surface the upstream SeeDance timeout.
  You may return completed act URLs as a diagnostic preview, but do not deliver
  a partial concat as `final_url`, do not call it production-ready, and do not
  proceed to step [6].

Do not retry a stalled act while its original task is still `queued`, `running`,
or `processing`. Continue polling it with visible progress, then call
`task_cancel({task_id})` at the 15 min total ceiling before
using the one missing-act retry.

## [6] Stitch acts into 60s base

```
edit_concat(video_urls=ui_grounded_act_urls)
```
Save as `base_url` (60 seconds, 16:9, native dialogue audio). `ui_grounded_act_urls` equals `act_urls` for non-digital products; for digital products it contains the step [5.5] overlaid reveal acts. Do not feed the raw `act_urls` into concat when a digital UI overlay plan exists.

## [7] Generate background music — INSTRUMENTAL, target ~60s

**The pattern is fixed. The sound is a per-brand creative decision.** Use Kling audio because it supports `background: true` and the MCP worker now handles the long-bed gap: it generates one 10s Kling seed, then extends it locally with ffmpeg looping/crossfade to the requested 60s. WHAT genre / instrumentation / mood goes in the prompt is your job — pick something that fits the brand's tone, the founder's voice, and the product. Do NOT copy the piano example below verbatim; that's one possible sound, not a template.

### Fixed pattern (don't change):
- `provider: "kling-audio"`
- `mode: "text_to_audio"`
- `background: true`
- `duration_seconds: 60`
- No `lyrics` field. Kling uses the prompt only.
- No second provider call or manual tiling. The MCP worker owns the one-seed extension path.
- `prompt` must be `<= 200` characters. Kling rejects longer prompts with validation code `1201`, so keep the style snapshot short.

### Creative decision (per video — pick from `brief.tone` + script vibe + product context):

Examples of what the music register might be for different brands. Don't use these literally — match the vibe of YOUR brand:

| Brand register | Genre direction | Sound palette |
|---|---|---|
| Technical / dev-tool / B2B SaaS | corporate cinematic underscore, Apple-keynote calm | warm felt piano, soft synth pad, sparse low-end pulse, 80–90 BPM |
| Playful / streetwear / consumer | lo-fi hip-hop, chill beat | dusty drums, jazzy chord stabs, vinyl crackle, 70–85 BPM |
| Disruptive / edgy / fintech / crypto | minimal electronic, dark synthwave | analog synth bass, side-chained pad, half-time kick, 90–100 BPM |
| Fashion / luxury / lifestyle | minimal house, modern fashion-film score | filtered house pad, soft 4-on-floor kick, French-touch chord, 100–110 BPM |
| Fitness / energy / sports | driving electronic pulse, workout register | pulsing synth bass, building arp, hi-hat eighth-notes, 110–125 BPM |
| Food / hospitality / café | acoustic warmth, indie folk | fingerpicked acoustic guitar, brushed snare, light upright bass, 80–95 BPM |
| Cinematic / brand-story / docu | orchestral score, hopeful crescendo | strings layer, soft piano lead, swelling brass, tempo build |
| Gaming / dev-tools / creator-tools | chiptune-modern hybrid, retro-pixel | square-wave lead, modern synth pad, snappy snare, 105–120 BPM |

When in doubt: read `brief.tone` (technical / casual / playful / professional / disruptive) and pick a register that wouldn't feel weird next to the founder's voice profile + the script's emotional arc. Match the energy, don't fight it.

### Canonical call (substitute YOUR creative direction into prompt, staying <= 200 chars):

```
generate_music(
  provider: "kling-audio",
  mode: "text_to_audio",
  background: true,
  duration_seconds: 60,
  prompt: "<=200 chars: soft instrumental background bed; <register>, <main instrument>, <mood>, <BPM>; no vocals; leave room for narration>"
)
```

How it works (load-bearing):
- **Kling generates one 10s seed**: the paid provider call stays short and background-capable.
- **The worker extends locally**: MCP loops/crossfades the 10s seed with local ffmpeg to reach `duration_seconds: 60`, then returns the extended CDN `audio_url`.
- **`prompt` field carries the style snapshot**. Include "soft instrumental background bed", "no vocals", and "leave room for narration" so the mix does not fight the founder dialogue. Keep it <= 200 characters; if Kling returns `1201`, shorten the same style idea instead of retrying the long prompt.

Save as `music_url`. Read `result.duration_seconds`:
- If `>= 55s` → mix it. Expected path with the Kling worker extension.
- If `< 55s` → do not silently accept a short bed. Retry once with the same `kling-audio` call; if it still returns short, stop and surface the tool result because the worker extension path did not satisfy the contract.

**Banned anti-patterns** (each empirically caused a failure):
- ❌ `provider: "minimax-music"` for the default generated bed — MiniMax does not support `background: true` and can foreground the melody under narration.
- ❌ Manual 10s tiling in the skill — the MCP worker already extends one 10s Kling seed locally.
- ❌ Putting duration only in `prompt` text ("60 second instrumental") — use `duration_seconds: 60`.
- ❌ Adding a `lyrics` field — this path is Kling prompt-only.
- ❌ Copying the same piano-and-pads example for every brand — the recipe is the pattern, not the sound. Pick a register per brand.

## [8] Composition layer — lower-third + subtitles

> **Pipeline ordering note** — music mix happens in step [10], AFTER end-card concat. Mixing music into the body before the end card is concatenated leaves the end card silent (the music track ends at the cut). Always: overlays on body → end card → concat → THEN mix music over the full assembled clip.

Use MCP tools first. `add_captions` handles subtitle timing and burn-in server-side; `render_html_animation` handles authored HTML motion; `edit_video_compose` handles transparent lower-third overlays.

### Default paths

| Requested layer | Default action |
|---|---|
| No lower-third, no subtitles | `body_with_overlays_url = base_url` |
| Subtitles only | call `add_captions(video_url: base_url, caption_mode:"auto", style:"classic", position:"bottom", font:"inter")`; save returned `url` as `body_with_overlays_url` |
| Lower-third only | render lower-third `.mov` via `render_html_animation`, then call `edit_video_compose`; save returned `url` as `body_with_overlays_url` |
| Lower-third + subtitles | render and compose the lower-third first, then call `add_captions` on the composed checkpoint URL |

If `state.lower_third` is false or unset, skip [8a] and [8b]. This keeps the default path fully MCP-native.

Do not call local Whisper/caption scripts or chained `edit_text_overlay` for captions. If exact original-script spelling matters, pass manual `subtitles[]` only when you already have exact timed segments from a trusted source; otherwise prefer the `add_captions` auto waterfall.

### [8a] Render the lower-third (only if `state.lower_third = true`)

Skip this sub-step unless `state.lower_third = true`. Render via `render_html_animation` with `format: "mov"` (ProRes 4444 with yuva420p — preserves alpha). **Do NOT use `format: "webm"`** — HyperFrames currently emits webm as VP9 `pix_fmt=yuv420p` with no alpha channel, so "transparent" areas come out as literal black pixels and the composited LT shows a black box outside the pill. The `.mov` ProRes path is the only reliable alpha path right now.

- Native dimensions: 800×220 (matches the placement size on a 1280×720 frame, so no scaling artifacts)
- Pill: `state.brand.colors.primary` bg (default `#0d0d0d`), `state.brand.colors.highlight` border (default `#fefbcf`), `state.brand.colors.accent` drop shadow (default `#cfc3ff`), 18px border-radius
- Two-line text: `founder_name` (Space Grotesk 800, 80px, white) + `founder_role` (Space Grotesk 500, 28px, butter)
- NO logo inside the pill — brand mark lives in the end card; lower-third is about the person
- CSS `@keyframes` only: slide in 0–0.6s from `translateX(-900px)`, subtle box-shadow pulse around 3s, slide out 4–5s. Do not use GSAP for lower-third animation; the same per-frame seek concerns as the end card apply.
- Save URL as `lower_third_url` (file extension `.mov`)

If you need to verify the `.mov`, inspect the video stream pixel format and confirm it contains alpha (`yuva...`). If it is plain `yuv...`, the alpha was dropped — switch render format or re-render.

### [8b] Lower-third overlay

Use this only when the lower-third is enabled. Default to the MCP compose path:

```
edit_video_compose(
  base_video_url: base_url,
  overlays: [{
    video_url: lower_third_url,
    position_px: { x: 50, y: <video_height - 220 - 100> },
    width_px: 800,
    height_px: 220,
    start_s: 0,
    end_s: 5
  }]
)
```

Save the returned `url` as `body_with_lower_third_url`.

Local fallback contract, only if MCP compose is unavailable:
- Download `base_url` and `lower_third_url` only for this local composition step.
- Overlay the 800×220 lower-third at `x=50`, `y=video_height - 220 - 100`, enabled for `t=0..5s`.
- Preserve the original body audio without re-encoding so lip-sync stays exact.
- Use visually lossless H.264 settings for the local checkpoint.
- Upload the checkpoint with `upload_asset` and save the returned `public_url` as `body_with_lower_third_url`.

If subtitles are requested too, call `add_captions(video_url: body_with_lower_third_url, ...)` and save its returned `url` as `body_with_overlays_url`. If not, `body_with_overlays_url = body_with_lower_third_url`.

### [8c] Captions via MCP

Default call:

```
add_captions(
  video_url: <base_url or body_with_lower_third_url>,
  caption_mode: "auto",
  style: "classic",
  position: "bottom",
  font: "inter",
  font_color: "#ffffff",
  highlight_color: state.brand.colors.accent or "#cfc3ff",
  outline_color: state.brand.colors.primary or "#111111",
  font_size: 42
)
```

Save returned `url` as `body_with_overlays_url`. The returned `transcript` is useful for QA, but the video URL is the pipeline artifact.

## [9] Animated end card (5s) — author inline HTML, render via HyperFrames

We do NOT use `generate_slide_animation` here. That tool delegates HTML authoring to a slide-card LLM, which routinely adds corner clutter (top-left wordmarks, bottom-right URLs), picks wrong aspects, and produces animations that don't reliably play through HyperFrames' per-frame seek. Instead, the orchestrator authors the end-card HTML directly and renders it via `render_html_animation`. Same engine the lower-third uses.

### Hard rules — empirically verified, do not deviate

These are NOT stylistic preferences. Each was discovered by rendering, extracting frames, comparing to expectations, and observing a specific failure. Reverting any of them will reproduce a known bug.

1. **Aspect ratio matches the body video.** Read `aspect_ratio` (default `16:9`). Compute `data-width` × `data-height` for the `#stage`: `16:9 → 1920×1080`, `9:16 → 1080×1920`, `1:1 → 1080×1080`. Hardcoding the wrong orientation produces a side-bar concat where the body and end card play side-by-side instead of in sequence.

2. **No corner clutter.** No top-left wordmark. No bottom URL. No icon squircle next to the title. The end card is a single centered message + CTA. The brand mark is implied by the typography and palette; an explicit logo competes with the title and reads as cluttered. (If the user explicitly asks for a logo, place it integrated into the centered stack — never in a corner.)

3. **Use CSS `@keyframes` for the entrance animation, not GSAP `tl.from()`.** HyperFrames Chrome seeks per-frame via BeginFrame; GSAP's `tl.from()` records its initial state lazily on first play and never fires under seek-only playback — every frame renders the static FINAL state with no entrance motion. CSS `@keyframes` are tied to Chrome's compositor clock and animate deterministically per frame. Declare duration through the `#stage` / `#card` `data-duration` attributes; do not add a GSAP script just to establish timing. Repeated frame captures with GSAP showed identical frames at t=0 and t=2s; switching to CSS `@keyframes` fixes it.

4. **All entrance animations must complete by `t = duration - 0.5s`.** Half-second hold so the final state sits readable before the cut. With `duration: 5s` that's all `animation-delay + animation-duration <= 4.5s`.

5. **Use absolute positioning for animated elements, not flex.** Flex layout doesn't fully settle by frame 0 in HyperFrames Chrome, which compounds the GSAP-from() bug above — elements pop in mid-animation as flex finishes its second pass. Pure absolute positioning gives stable, deterministic layout from frame 0.

6. **Give each `@font-face` a unique `font-family` name; don't rely on weight matching.** Declaring two `@font-face { font-family: "telka"; ... font-weight: 700/500; }` blocks is supposed to let CSS `font-weight: 500` pick the 500 face — but in HyperFrames Chrome the matching is unreliable for some weights. Use distinct families: `"telka-ext-900"`, `"telka-700"`, `"telka-500"`. When weight matching fails, the tagline can render in a serif fallback; switching the tagline to an explicitly loaded family avoids that.

7. **`telkaextended-900-normal.woff2` and `telka-700-normal.woff2` are KNOWN-WORKING in HyperFrames Chrome. `telka-500-normal.woff2` is KNOWN-BROKEN — it parses successfully via fontTools (correct OS/2.usWeightClass=500, valid cmap, correct family name) but Chrome silently rejects the @font-face declaration and falls back to system serif.** Workaround: use `telka-700` for the tagline too (same family, slightly heavier — visually still on-brand). If a future end card needs medium weight, test the candidate woff2 by rendering+extracting frame 30 BEFORE shipping. Don't trust that "Telka 400" or "Telka 300" will work just because Telka 700 does.

8. **Inline brand-kit fonts as base64.** Pika CDN doesn't accept font uploads (mime allowlist) and doesn't send CORS headers, so `@font-face` URL references fail in HyperFrames Chrome and the font silently falls back to system serif. Subset each woff2 with `pyftsubset` to just the glyphs in title+tagline+CTA, base64-encode, embed as `data:font/woff2;base64,...`. Subsetted files are typically 5–10 KB each.

9. **Don't write CSS `font-family` fallback chains for brand designs.** If the brand font fails to load, a fallback chain hides the failure — you ship Helvetica thinking it's Telka. Use `font-family: "telka-700"` alone (no fallback). Then a font load failure renders Chrome's default serif, which is visually obvious and triggers a fix.

10. **Composition contract** — the HyperFrames contract: `<div id="stage" data-composition-id="main" data-start="0" data-duration="5" data-width="W" data-height="H">` wraps a SINGLE direct child `<div id="card" class="clip" data-start="0" data-duration="5" data-track-index="0">` which contains everything else. Visible timed elements must include `class="clip"` because HyperFrames uses it for visibility control, and the clip must be nested inside the composition root, not a sibling. Multi-tracked direct children of `#stage` interact poorly with frame seeking. (Fixed by mirroring the working lower-third structure.)

11. **Runtime readiness hook** — include a small compatibility hook before `</body>`:
    `window.__hf = { duration: 5, seek: (t) => { document.documentElement.style.setProperty("--hf-time", String(t)); } };`.
    CSS `@keyframes` still drive the visual animation, but the hook makes the
    prod frame-capture path ready when it probes for `window.__hf`. If the
    worker reports `window.__hf not ready after 45000ms`, treat the HTML as
    invalid for `render_html_animation`; fix the composition contract or hook
    and rerender. Do not fall back to a static PNG.

12. **Always extract frames at t=0, t=1s, t=2s after rendering and visually compare.** If frames 0 and 2 look identical, the entrance animation isn't running. If the tagline looks like a serif, the brand font didn't load. Don't trust the URL alone. Don't ship without this check. (User caught these failures three renders in a row before frame extraction was added.)

### Build steps

```python
# 1. Decide canvas
W, H = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}[aspect_ratio]

# 2. Pick palette + fonts from state.brand (with fallbacks)
bg      = state.brand.colors.surface  if state.brand else "#ffffff"
ink     = state.brand.colors.primary  if state.brand else "#0d0d0d"
accent  = state.brand.colors.accent   if state.brand else (accent_color or "#0d0d0d")
display_font_path = state.brand.fonts.display_path  # e.g. brand-kit/.../telkaextended-900-normal.woff2
body_font_path    = state.brand.fonts.body_path     # used for tagline + CTA
# If state.brand has no fonts, use the fallback branch below and flag this in the deliver step.

# 3. Subset fonts to only the chars used in title/tagline/CTA
glyphs = set(brief.product_name + brief.tagline + brief.call_to_action + " .,'-/")
if display_font_path and body_font_path:
    # Use a standard fontTools pyftsubset command or equivalent local font-subset utility.
    # Then base64-encode the subsetted woff2 bytes and inline them in @font-face data: URLs.
    display_b64 = "<base64 subsetted display woff2 bytes>"
    body_b64 = "<base64 subsetted body woff2 bytes>"
else:
    display_b64 = body_b64 = None

# 4. Author the HTML inline. Do not load a preset/template file.
#    Include #stage/#card contract, CSS @keyframes, absolute positioning,
#    @font-face data URLs when display_b64/body_b64 exist, title lines,
#    tagline, CTA, palette values, and dimensions W/H.

# 5. Render
end_card_url = render_html_animation(html=filled, fps=30, quality="standard", format="mp4")
```

### Layout (centered stack — no corners)

```
┌─────────────────────────────────────────────┐
│ ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ │ ← top accent bar (animated wipe L→R)
│                                             │
│            BIG TITLE LINE 1                 │ ← display font 900, slides up
│            BIG TITLE LINE 2                 │ ← display font 900, slides up (staggered)
│                                             │
│                  ────                       │ ← short accent divider (scaleX in)
│                                             │
│             tagline goes here               │ ← body font 500, fades+rises
│                                             │
│         ╭─ Start with X ─╮                  │ ← CTA pill, accent bg, ink border, back-out pop + breath
│         ╰─────────────────╯                 │
│                                             │
└─────────────────────────────────────────────┘
```

### Animation timing reference (5s end card, CSS @keyframes)

All implemented as CSS `animation: name duration easing delay forwards` on the corresponding element. The element's pre-animation CSS state IS the "from" — no JS needed.

| t (s) | Element | Animation |
|-------|---------|-----------|
| 0.00–0.85 | accent-top | `scaleX:0 → 1`, `cubic-bezier(0.16,1,0.3,1)` |
| 0.25–1.00 | title line 1 (`#title .l1`) | `y:120, opacity:0 → y:0, opacity:1` |
| 0.42–1.17 | title line 2 (`#title .l2`) | same, staggered |
| 1.00–1.50 | divider | `scaleX:0, opacity:0 → 1, 1` |
| 1.20–1.75 | tagline | `y:30, opacity:0 → y:0, opacity:0.9` |
| 1.55–2.15 | CTA pill | `y:60, opacity:0, scale:0.92 → y:0, opacity:1, scale:1`, `cubic-bezier(0.34,1.56,0.64,1)` (back-ease pop) |
| 2.60–4.20 | CTA pill | `scale:1 → 1.05 → 1`, alternate (subtle breath) |
| 2.80–4.80 | accent-top | `opacity:1 → 0.55 → 1`, alternate (gentle shimmer) |
| 4.80–5.00 | hold | (final readable state) |

Reference implementation pattern: use a centered-stack HTML recipe. Author the filled HTML inline in the orchestrator and pass it directly to `render_html_animation`; do not call a bundled helper script or rely on a separate `presets/` directory.

If the brand-kit lacks fonts (`state.brand.fonts` is null) — fall back to system `-apple-system, sans-serif` for tagline/CTA but DROP the title down to a system-display weight. Don't render brand-typography end cards with fallback fonts; they always look wrong. Flag this in the deliver step so the user knows the brand-kit is incomplete.

Save the returned MP4 URL as `end_card_url`. `end_card_url` must be an MP4 video segment, not a static PNG, because step [10] concatenates it with the body video. Download it only if you need local visual QA frames or a local fallback assembly.

## [10] Assemble body + end card + music via MCP

Use the server-side deterministic edit tools for final assembly. The current MCP server `edit_concat` normalizes mismatched inputs before concat, and `edit_audio_mix` preserves the original video audio while mixing the music track.

```
assembled = edit_concat(video_urls=[body_with_overlays_url, end_card_url])
assembled_url = assembled.url

if music_url:
  mixed = edit_audio_mix(video_url=assembled_url, audio_url=music_url, audio_volume=0.16)
  final_url = mixed.url
else:
  final_url = assembled_url
```

Mix music after concat, never before, so the score continues through the end card. If `edit_audio_mix` fails because the music file is too short or malformed, set `final_url = assembled_url`, surface the music issue, and still run step [10.5] before delivery; do not rerun expensive SeeDance acts.

### [10.5] Final duration floor

Before reporting `final_url` to the user, probe the assembled result:

```
analyze_media(
  media: final_url,
  query: "Return JSON with duration_seconds for this video."
)
```

Save the result as `final_duration_seconds`. It must be `>= 55` and `<= 75`
before reporting `final_url` as the completed deliverable.
If `final_duration_seconds` is under 55s, treat the run as a failed partial
assembly: do not deliver the URL as final, do not mark the skill complete, and
return to the missing-act recovery above. If all 4 acts were present but the
probe is still under 55s, stop and surface the concat/provider truncation for
investigation instead of padding with unrelated footage.

## [11] Final URL

Save `final_url` into `state`. If a local fallback assembly produced the final MP4, upload that checkpoint through `upload_asset` and replace `final_url` with the returned `public_url`.

## Post-flight quality gate

Before declaring success, call `analyze_media` on `final_url` and ask for a structured verdict:

```
Return JSON only: {
  "verdict": "clean" | "degraded" | "catastrophic",
  "observations": string[],
  "quality_warning": string | null,
  "re_roll_suggestion": string | null
}
Check that `brief.product_name` / `product_name` is spelled correctly anywhere it appears, any phone screen / product screen shows the intended product instead of a hallucinated substitute, required product assets are visible in the expected acts, and the final video has no black frames or partial-act truncation.
```

- If `verdict` is `clean`, deliver the final URL normally.
- If `verdict` is `degraded`, deliver the final URL plus the `quality_warning` so the user can review before publishing.
- If `verdict` is `catastrophic`, do not call the video complete; surface the verdict and `re_roll_suggestion` instead of declaring success.

## [12] Asset bundle (optional)

Return the final URL first. If the user asks for editable source assets, provide a bundle containing:

- `final_url`
- `act_urls`
- `character_url`, `location_url`, and any product/screenshot asset URLs
- `music_url`
- `end_card_url`
- optional `lower_third_url` / `body_with_overlays_url`
- the script, brand quick-reference, and act-to-asset map

Why this matters:
- The user can swap a layer (founder photo, sub timing, music) and re-render WITHOUT re-fetching everything
- The brand kit is the single source of truth for any future video for the same brand — re-using it is one folder copy away
- The act-level `.mp4`s are valuable on their own (e.g. the user might want to clip just one act for a specific channel)
- Users often ask to save the generated refs next to the video so they can reuse those assets. Codified as default.

## [13] Deliver

Report `final_url` to the user. Include:
- Asset bundle URL/path only if the user asked for one
- Total duration from `final_duration_seconds` (~65s = 60s body + 5s end card)
- Intermediate URLs or local files useful for reruns: `base_url`, optional `body_with_overlays_url`, `music_url`, `end_card_url`, `final_url`, and each `act_urls[i]`
- The brief (`brief.product_name` / `brief.tagline`) so the user can confirm the model picked up the right product
- A 1-line summary of which asset went into which act, so the user can confirm placement

## Verification gates

| Step | Check |
|------|-------|
| Brief | `product_name` non-empty |
| Asset analyses | One JSON object per asset, each with non-empty `content_description` and `best_for_act` |
| Script | 4 acts; total dialogue 100–180 words; each asset is referenced by at least one act, OR explicitly noted as unused |
| Refs | `character_url` and `location_url` are https URLs |
| Acts | All 4 act_urls returned (each with a unique seed); for acts containing shots with non-null `asset_index`, vision-check ONE such act with `analyze_media` to confirm the asset is actually visible AND the reveal pattern is correct for `product_type` (e.g. for `physical_apparel`, verify the founder is HOLDING/WEARING the actual t-shirt with the right print — NOT showing it on a phone screen) |
| Stitch | `base_url` returned |
| Music | URL returned; `duration_seconds >= 55` from the `kling-audio` background-bed path; retry once if under 55, then stop and surface |
| Overlays | `body_with_overlays_url` returned (or `body_with_overlays_url = base_url` if step [8] skipped) |
| End card | `end_card_url` returned as an MP4; inspect early frames with `extract_frame`/`analyze_media`: frame 0 should show the empty background before entrance, and a later first-second frame should show partial entrance — confirms CSS @keyframes are firing, not static |
| Final assembly | `assembled_url` returned by `edit_concat`; `final_url` returned by `edit_audio_mix` when music is present, otherwise `final_url = assembled_url` |
| Final duration | `analyze_media` reports `final_duration_seconds >= 55` and `<= 75` before delivery |
| Local fallback upload | Only if local fallback assembly was used: `final_url` replaced with an uploaded `public_url` |

## Failure modes

Except for the one missing-act retry documented in "Duration floor and partial-act recovery", stop and surface on first verification failure. Don't auto-retry expensive calls (SeeDance acts run 3–8 min each — repeated failures burn credits).

### Recovering from upstream 5xx on analyze_brief / generate_image / generate_reference_video / generate_music / upload_asset

If any paid generation, brief analysis, music, render, edit, or asset MCP call returns:
- `code: "provider_5xx"` AND `retry_class: "retry_after_backoff"`
- Or HTTP 502 / 503 / 504 from any upstream provider (Seedance, Kling, OpenAI, Gemini, storage)

Do this:
1. Wait 5 seconds.
2. Re-call the exact same MCP tool with the exact same arguments. Do not rewrite the brief, product name, founder photo, act prompt, seed, reference-image order, music prompt, or upload payload.
3. If the retry also fails with 5xx, abort and surface to the user: "Provider returned a transient upstream error twice. Try again in 1-2 minutes; this usually clears on its own."

Do not retry more than once. This path is for transient provider outages; changing creative inputs after a 5xx creates a different artifact and can duplicate spend.

### Recovering from upstream 4xx / moderation_blocked

If `generate_image` returns an upstream 4xx or `moderation_blocked` while creating a founder/location/product reference:
1. Do NOT retry the same prompt; moderation and most 4xx validation failures are deterministic.
2. If the asset is not user-critical, try a fallback provider once only when the substitute still matches the brief. For founder identity photos, no fallback provider should alter the user's identity; ask for a safer/user-supplied reference instead.
3. If the fallback provider also fails or would change the product/founder identity, surface to the user: "Image provider declined this reference prompt. Provide a different reference image or choose a less recognizable/stylized direction."

For Seedance act moderation, follow the duration-floor / missing-act recovery only where it applies. Do not run repeated blind act retries.

### Recovering from upstream 429 (rate limit)

If any upstream returns HTTP 429 with a backoff hint:
1. Wait the hinted backoff, or 30 seconds if no hint is provided.
2. Re-call the exact same MCP tool with the exact same arguments.
3. Do not retry more than once. If it still returns 429, abort and surface the rate-limit message.

### `capture_website` returning empty / page-not-loaded

This skill usually extracts product facts with `analyze_brief`, but URL brief helpers may call `capture_website`. If `capture_website` returns 200 but `action_bboxes` is empty or `recording_viewport` is 0x0:
1. Do NOT retry; the page failed to render in the capture environment.
2. Surface: "Could not capture <url>. The page may be blocked / paywalled / require auth. Please provide a product brief, screenshots, or hosted assets instead."

### `upload_asset` network / auth failure

If `upload_asset` fails while converting founder photos, product assets, brand logos, lower-thirds, or fallback local assemblies to hosted URLs, do not continue with local filesystem paths in `reference_images` or HTML. Retry once only for the 5xx or 429 classes above. For `auth_error`, unsupported MIME, network failure, or repeated upload failure, stop and ask for a hosted URL or supported raster export.

### Long-running `task_status` exceeding ceiling

Each async MCP call returns either an inline result or `{task_id, status}` for polling. Use these ceilings before deciding a task is stuck:
- Seedance i2v: 10 min per call
- Kling audio: 5 min per call
- gpt-image-2 high quality: 3 min per call
- render/edit/upload helpers: 5 min per call

Use whichever is earlier: the provider's ceiling x 1.5 or any skill-specific hard polling cap, including the 15 min total cap in the Long-running task_status polling contract above. If `task_status` returns `status: "processing"` or `status: "queued"` past that earlier limit, call `task_cancel({task_id})` and surface: "Provider taking unusually long; aborting. Try again."

| Symptom | Cause | Fix |
|---|---|---|
| `generate_reference_video` returns 402 "insufficient balance" with a familiar UUID | Idempotency cache replaying an old failed result for identical params | Pass a unique `seed` per call (101 / 202 / 303 / 404 for 4 acts) so the hash differs. |
| SeeDance returns 422 "may contain likenesses of real people" on founder ref | Content-policy filter tripped (intermittent — same photo may pass next attempt) | Re-roll the founder portrait with stronger stylization ("Pixar / Disney 3D animation aesthetic"). Don't auto-retry the same ref — burns credits. |
| Founder shirt changes between acts | @Image1 read fresh each act, no wardrobe lock | Add a `WARDROBE LOCK:` line to every act prompt, identical sentence verbatim. |
| All 4 acts have the same physical backdrop | Opening line says "inside the location matching @Image2" — read literally | Open with "in a setting whose visual style, palette, lighting and materials match @Image2" + add per-shot `Background context:` line. |
| Founder looks frozen / no body language | Beats are facial-only; act is single-shot | Add 3 time-coded sub-shots per act with explicit camera-motion `Transition:` lines; every beat needs a hand/torso/head action (see [3c.1]). |
| Final video is under 55s | One SeeDance act timed out or final concat trimmed the body, producing a partial run | Do not deliver it as final. Retry the missing act once with a new seed while preserving successful acts; if that cannot complete, stop and surface the upstream SeeDance timeout. |
| Music prompt rejected with code `1201` | `kling-audio` prompt exceeded the 200-character provider cap | Shorten the prompt to the canonical <= 200 character style snapshot. Keep `soft instrumental background bed`, `no vocals`, and `leave room for narration`; do not change provider, duration, or background mode. |
| Music returns < 55s | `kling-audio` worker extension did not satisfy the 60s request | Confirm the call used `provider: "kling-audio"`, `mode: "text_to_audio"`, `background: true`, and `duration_seconds: 60`. Retry once; if still short, stop and surface the tool result. |
| Music overpowers dialogue | Prompt asked for foreground melody instead of a bed | Regenerate once with "soft instrumental background bed, no vocals, leave room for narration" and keep `audio_volume` at 0.16 or lower in step [10]. |
| Captions misspell product names | Auto transcription normalized the spoken audio | Use manual `subtitles[]` only if you already have trusted timestamped segments; otherwise surface the transcript limitation instead of running local Whisper by default. |
| Lower-third overlay shows a black box outside the pill | webm format encoded without alpha (yuv420p) | Re-render with `format: "mov"` (ProRes 4444 yuva). Verify with `ffprobe \| grep pix_fmt` showing `yuva*`. |
| Final video audio shorter than video | Local fallback concat used `-c copy` with mismatched audio params | Prefer MCP `edit_concat`. If local concat is unavoidable, normalize all inputs to aac/44100/stereo/192k before concat. |
| End card renders identical at t=0 and t=2s (no entrance animation) | GSAP `tl.from()` used instead of CSS `@keyframes` | Convert entrance to CSS `@keyframes`; keep the GSAP shim only for duration seeking. |
| End-card tagline renders as serif fallback | woff2 font failed to load in HyperFrames Chrome | Use unique `font-family` names per face (not weight-matching); subset + base64-inline the woff2; verify by extracting frame 30 before shipping. |
| `render_html_animation` fails with `window.__hf not ready after 45000ms` | End-card HTML did not expose the runtime readiness hook or valid nested `class="clip"` composition | Add/fix the `window.__hf` hook and `class="clip"` child, then rerender the MP4. Do not fall back to a static PNG and do not proceed to concat until `end_card_url` is a video URL. |

## Load-bearing phrases

These strings go into the SeeDance prompt (or HTML render) verbatim. Each was empirically validated — paraphrasing breaks the recipe silently. When editing prompts, search for these anchors and leave them intact.

| Phrase | Goes into | Why load-bearing |
|---|---|---|
| `The character (matching @Image1) in a setting whose visual style, palette, lighting and materials match @Image2.` | Opening line of every act prompt | "in a setting whose style matches" frees SeeDance to vary backdrop per shot; "inside the location matching" reproduces the literal backdrop across all 4 acts. |
| `WARDROBE LOCK: …` (followed by the same wardrobe sentence verbatim across all 4 prompts) | Header line under `CHARACTER VOICE:` in every act prompt | Locks clothing across separate 15s generations. @Image1 alone can drift across acts. |
| `Background context: …` (one per sub-shot, distinct per position) | Inside every shot block | Forces SeeDance to render a different physical position per shot — different wall, different angle, different background feature. Without it, all 3 sub-shots end up in the same corner. |
| `<<<voice_1>>>…<<<voice_1>>>` | Per-shot dialogue payload | SeeDance native lip-sync token. The tokens are how the engine knows what to mouth-sync; without them no lip-sync at all. |
| `Transition: …` / `Hard cut:` | Between sub-shots in the same prompt | `Transition:` describes continuous camera motion (glide / dolly / arc); `Hard cut:` triggers a real cut. Without either, SeeDance defaults to a same-position re-frame that reads as a jump zoom. |
| `Native lip-synced dialogue audio, no music overlay.` | Closing line of every act prompt | Prevents SeeDance from layering its own ambient music underneath the dialogue, which would fight the dedicated music bed in step [10]. |
| `provider: "kling-audio"`, `mode: "text_to_audio"`, `background: true`, `duration_seconds: 60` | Step [7] `generate_music` call | Uses the only background-capable music provider and triggers the MCP worker's one 10s Kling seed + local ffmpeg extension path. |

## What NOT to do

- **Don't open the SeeDance prompt with "inside the location matching @Image2"** — reproduces the literal backdrop across all acts. Use "in a setting whose visual style ... match @Image2".
- **Don't describe the character in prompt prose** — @Image1 carries identity. Prose conflicts produce phantom figures or wrong outfits. Exception: the `WARDROBE LOCK:` line.
- **Don't use film-industry shot terms** — "Two-shot" / "Three-shot" / "Over-shoulder" / "OTS" / "Master shot" trigger SeeDance phantom-subject artifacts. Describe what the camera sees in plain language.
- **Don't render the lower-third as webm** — alpha not preserved (HyperFrames emits yuv420p). Use `format: "mov"` (ProRes 4444 yuva). Verify with `ffprobe \| grep pix_fmt`.
- **Don't use `generate_slide_animation` for the end card** — that tool's slide-card LLM adds corner clutter and produces animations that don't seek deterministically. Author inline HTML and render via `render_html_animation`.
- **Don't chain pika MCP `edit_text_overlay` / overlay calls for arbitrary text/caption composition** — that cascades quality loss and can introduce lip-sync drift. Use `add_captions` for captions and a single compose/local pass for bounded lower-thirds. Exception: step [5.5] deterministic digital UI overlays deliberately uses one bounded `edit_video_compose` pass plus optional exact-brand `edit_text_overlay`, followed by OCR QA, to prevent Seedance-rendered brand/UI text.
- **Don't use local `ffmpeg concat -c copy` for final assembly unless MCP is unavailable** — the old audio-drop bug was in local concat behavior. Default to MCP `edit_concat` + `edit_audio_mix`.
- **Don't fire SeeDance with identical params across acts** — the MCP idempotency cache hashes to the same task ID and replays old results (sometimes failures). Pass unique `seed` per act.
- **Don't use MiniMax for the default generated bed** — it does not support `background: true` and can foreground the melody under narration.
- **Don't manually tile the 10s Kling clip in the skill** — the MCP worker owns the local ffmpeg extension path for `duration_seconds: 60`.
- **Don't copy the example music sound for every brand** — the recipe is the Kling background-bed call, not the specific instrumentation. Pick a register that matches `brief.tone` (see step [7] table).

## Engine choice: seedance-only (with caveats)

SeeDance (`fal-seedance-2-i2v` via `generate_reference_video` `provider: "seedance"`) is the sole video engine. Picked over alternatives after testing:

- **vs Kling v3-omni**: Kling has a true `shots[]` hard-cut array (cleaner multi-shot) but rejects the `seed` parameter (cache-busting harder), and 4 × pro 1080p outputs sum >50MB and exceed the `edit_concat` upload cap (forces local concat). Kling does have more permissive content policy for real-person photos — it's a worth keeping in mind as a fallback if SeeDance's intermittent 422 becomes a hard block.
- **vs Happy Horse `happyhorse-1.0-r2v`** (Alibaba DashScope): produced clean 1080p with native lip-sync but the multi-shot prompt direction was weaker and visibly less cinematic than SeeDance.
- **SeeDance wins because**: native `<<<voice_1>>>` lip-sync, accepts `seed` (cache-busting), permissive enough on real-person photos that 95%+ runs pass content filter, single 15s prompt with time-coded sub-shots gives enough variation for a talking-head register.

If SeeDance is down or its content filter starts rejecting your founder ref repeatedly, the documented fallback is to re-roll the founder portrait with stronger stylization (Pixar / Disney 3D aesthetic). Switching engines mid-pipeline changes too many assumptions in the prompt, concat, and asset-size flow.

## Runtime expectations

Wall-clock budget per step. Total run is ~12–18 minutes, dominated by the parallel SeeDance batch.

| Step | Wall clock | Notes |
|---|---|---|
| [1] analyze_brief | 20–60s | |
| [2] analyze_media × N | 15–30s per asset, parallel | |
| [4] founder/custom location refs | 10–60s each | Upload local founder photo, use supplied URL, or generate a founder portrait; default location waits for [4.5] |
| [4.5] brand-kit ingestion + default location | 10–30s | Parse brand kit, upload logo assets, render aspect-matched brand-accent backdrop if needed |
| [5] SeeDance × 4 in parallel | 5–9 min wall (slowest act) | Each act 3–8 min and may complete asynchronously |
| [5.5] digital UI overlays | 30–120s for digital products | Render real UI / wordmark overlay clips, composite them onto reveal acts, then OCR QA before concat |
| [6] edit_concat (acts → 60s body) | 30–60s | |
| [7] generate_music | 30–90s, retry once if <55s | Kling generates one 10s seed, then worker extends locally to ~60s |
| [8a] render LT as .mov | 60–120s | ProRes 4444 slower than webm but only path with alpha |
| [8] add_captions | 30–90s | subtitles only, or after lower-third checkpoint |
| [8b] local lower-third overlay fallback | 20–60s | only when lower-third is enabled |
| [9] render end card | 60–120s | |
| [10] edit_concat + edit_audio_mix | 30–90s | server-side normalized concat and music mix |
| **Total** | **12–18 minutes** | |

## Defaults

- 4 × 15s SeeDance acts, parallel, unique seeds (101, 202, 303, 404)
- **Character identity comes from the `@Image1` reference** — avoid describing the character in prompt prose (no "Founder Avery", no "young creative streetwear founder"). Open every prompt with **"The character (matching @Image1) in a setting whose visual style, palette, lighting and materials match @Image2."** Using "inside the location matching @Image2" makes SeeDance reproduce the literal backdrop across all acts. The one exception is a `WARDROBE LOCK:` line in every act prompt to keep clothing consistent across the 4 separate 15s generations.
- **Avoid film-industry shot terminology** that SeeDance reads literally — never write "Two-shot", "Three-shot", or "Master shot". Shot F is "Brand context shot".
- **Every script has a `character_voice_profile`** (3-4 lines describing default delivery — cadence, signature gestures, pause behavior). Repeated verbatim as `CHARACTER VOICE: …` in every act's SeeDance prompt.
- **Every shot has `beats[]`**, not act-level `acting`. Each beat has `text` + `emotion` + `physical`. Silent `(beat)` entries direct what happens BETWEEN spoken sentences (held looks, micro-expressions, gesture transitions). Beats are emitted as a per-shot "Acting beats" block in the SeeDance prompt.
- **Every shot beyond the first in an act has `transition_from_prev`** — a continuous-camera-move description that takes us from the previous framing to this one (dolly, arc, push past, pull back, orbit). Without this, multi-shot acts read as jump zooms because SeeDance reframes the same virtual camera position instead of moving through space.
- **Apply the TTS pronunciation rewrites to dialogue text** before joining into the `<<<voice_1>>>` payload (Ari → Airy, API → A P I, example.com → example dot com, etc.). See "TTS pronunciation rewrites" in step [3].
- 16:9, 1080p (SeeDance `resolution: "1080p"`)
- User-provided assets are revealed product-type-appropriately:
  - `digital` → blank on-phone placeholders in shots C and E, then real UI / wordmark composited in step [5.5]
  - `physical_apparel` → founder wears/holds the actual t-shirts; assets passed as refs to EVERY shot where the shirt appears (not just one reveal beat)
  - `physical_object` → founder holds the product up; assets passed to all shots where product is visible
  - `consumable` → founder uses/eats/drinks; same pattern
  - `service` → no asset reveal; environment + dialogue only
- Music: target ~60s instrumental — call `generate_music` with `provider: "kling-audio"`, `mode: "text_to_audio"`, `background: true`, and `duration_seconds: 60`. Keep `prompt` <= 200 chars and include "soft instrumental background bed", "no vocals", and "leave room for narration". Retry once if under 55s, then stop and surface instead of accepting a short bed.
- 5s end card via `render_html_animation` — author inline HTML per step [9], inline brand-kit fonts as base64. Sources brand from `state.brand` (set in step [4.5]) → real logo, real palette, real fonts.
- **Captions via `add_captions`.** Use server-side word-level caption burn-in by default. Font choices are the tool-supported set (`inter`, `bebas-neue`, `noto-cjk`); use brand accent colors for highlight/outline instead of local custom font drawtext.
- **Lower-third fallback.** Off by default. If `state.lower_third = true`, render a 5s branded pill bottom-left via `render_html_animation(format:"mov")`; the final overlay onto the body uses `edit_video_compose`, or one local ffmpeg pass only if MCP compose is unavailable.
- **Final assembly via MCP.** Use `edit_concat` for body + end card, then `edit_audio_mix` for music. Local concat/mix is a fallback, not the canonical path.
- Provider: `seedance` only. Reference tokens are `@Image1` / `@Image2` / `@Image3`. Native lip-sync via `<<<voice_1>>>...<<<voice_1>>>` tokens per sub-shot. Real-person founder photos pass the content filter the vast majority of the time; intermittent 422 → re-roll with stronger stylization.
