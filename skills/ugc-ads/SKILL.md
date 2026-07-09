---
name: ugc-ads
description: >-
  Multi-cut jump-cut UGC product ad — HOOK + 3 JUMP CUTs + OUTRO, 15s, 9:16
  vertical (3:4 optional, seedance only), POV first-person talking-head selfie,
  every beat has spoken dialogue with native lip-sync, 5-act narrative arc
  (set → name → reveal → twist → punchline). Six category essences
  (HAUL / APP / FOOD / BEAUTY / FITNESS / TECH) auto-picked from the input URL.
  Creator-style raw UGC talking-head with multi-beat conversational dialogue.
  Use when the user asks to "make a UGC ad", "jump-cut product ad",
  "POV product reveal", "creator-style ad", "haul-style ad", "unboxing ad",
  "TikTok-style product video", or "talking-head ad about [URL]".
argument-hint: <url> [avatar_url=<url>] [provider=seedance|kling] [aspect_ratio=9:16|3:4] [variants=9:16,16:9,1:1] [category=auto|HAUL|APP|FOOD|BEAUTY|FITNESS|TECH] [captions=true]
---

# /pika:ugc-ads

## Parameters

| Param | Default | Notes |
|---|---|---|
| `url` | required | product URL — drives category detection and beat substitution |
| `avatar_url` | built-in fallback | persona portrait URL; fed as `@Image1` reference. When omitted, the skill uses a pre-generated Pixar-style female creator portrait |
| `provider` | `seedance` | seedance: strong at UGC selfie / talking-head POV with native lip-sync, multi-segment in single prompt, supports 3:4. kling: explicit `shots[]`, 9:16/16:9 only |
| `aspect_ratio` | `9:16` | `3:4` is seedance-only (kling rejects 3:4) |
| `variants` | unset | Optional comma list for shared-generation exports. Supported: `9:16`, `16:9`, `1:1`. Keeps the expensive UGC render shared, then reframes the final stage. |
| `category` | auto | `HAUL` / `APP` / `FOOD` / `BEAUTY` / `FITNESS` / `TECH`; auto-picked from URL |
| `captions` | `true` | TikTok-style word-chunked captions burned on top of the final video |

## Cost transparency gate

Before any paid MCP call, call `identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the run with this exact message:

> Estimated cost: about 4,000 credits (~$40) for a typical Seedance UGC ad with fallback/retry budget. This exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. The gate runs after the product URL is known and before avatar analysis, screenshot capture, video generation, captions, or paid retries.

## Runtime expectations

Typical end-to-end run: **6–12 minutes**. Breakdown:

- Step 1 (WebFetch) + Step 3 (capture_website screenshot): ~10–30s
- Step 7 (`generate_reference_video`): ~3–5 min for seedance, ~5–7 min for kling
- Step 7b/c (cartoonize + retry): adds ~1–2 min if seedance moderation rejects the avatar
- Step 8 (deterministic brand/spec overlays): 1-2 `edit_text_overlay` calls, ~30s–5 min total
- Step 9 (captions): single `add_captions` call, ~30s–5 min (transcribe + burn in one shot)

If the run exceeds 15 min without progress, something is wrong — inspect the tool-reported generation status and error message.

## Pre-generation wall-clock guard

Start a timer at skill start once the product URL is available and the cost gate has passed. Time spent waiting for the user's `proceed` reply is not prep time and must not trigger this guard. The first paid generation call is `generate_reference_video`, the long-pole paid stage, and it must be invoked within 5 minutes of skill start. If you have not invoked `generate_reference_video` within 5 minutes of skill start, stop before any paid generation call and report `failed_pre_generation_timeout` with what you have so far: fetched product facts, chosen category, avatar source, screenshot status, draft dialogue, and the exact blocker. Do not keep refining script wording, prompt grounding, or shot order.

Print a single-line progress checkpoint after each prep stage and right before the paid generation call:
- `Stage 1/3 done — product fetched and categorized.`
- `Stage 2/3 done — avatar and screenshot ready, composing dialogue.`
- `Stage 3/3 done — prompt locked, calling Seedance now.`

Script and prompt iteration is maximum 2 passes. After the max 2 passes, ship what you have to `generate_reference_video`; do not continue polishing the hook, punchline, or screen-close-up wording.

## Long-running task_status polling

When any long-running generation or edit call returns a `task_id` with or without an initial status, including `{task_id}`, `{task_id, status: "queued"}`, or an initial `queued`, `running`, or `processing` status, record the task id and start time immediately.

- Call `task_status({task_id})` in a tight loop until terminal (`completed | failed | cancelled`). No manual sleep and no Bash polling; the worker holds each status call open.
- Emit ONE visible progress line every 60s while status is `queued`, `running`, or `processing`: `Seedance i2v queued for {N}m {S}s... still processing`. Replace the provider/stage label when polling Kling, GPT-image-2, caption, or edit tasks.
- On `completed`, unwrap the returned result URL and continue.
- On `failed` or `cancelled`, surface failure to the user with `task_id`, status, and the last status message.
- After 15 min total from the original submit, call `task_cancel({task_id})` if the task is still non-terminal, then surface failure to the user. If cancel reports the task is already terminal, call status once more and report that terminal result.
- Do not submit a duplicate request while the original task is still `queued`, `running`, or `processing`.
- Async polling budget: one active task with one 15 min polling window. After the polling cap is exhausted, cancel the task and surface failure instead of submitting another paid render unless a later step explicitly allows a separate capped retry after the original task is terminal.

## Engine choice: Seedance default, Kling fallback

Default to Seedance for UGC selfie/talking-head ads because it handles native lip-sync, single-prompt multi-beat pacing, and optional 3:4 output well. Use Kling when the caller explicitly passes `provider=kling`, or after Seedance exhausts the capped cartoonized retry only if the user chooses Kling from the stop message. Kling's tradeoff is stricter aspect-ratio support but a separate moderation path and explicit shot segmentation.

## Steps

### 0. Resolve input (empty-args menu)

Strip flags and `key=value` parameters from `$ARGUMENTS`. If no product URL remains and there is no usable product URL in prior context, print this menu and stop:

> **Which product should the UGC ad promote?** Required:
>
> - **Product URL** — page to fetch for product name, category, visual references, and language
>
> Optional: `avatar_url=`, `provider=seedance|kling`, `aspect_ratio=9:16|3:4`, `variants=9:16,16:9,1:1`, `category=auto|HAUL|APP|FOOD|BEAUTY|FITNESS|TECH`, `captions=true|false`.

If the product URL is present, skip this step silently.

### 1. Fetch + categorize

`WebFetch` the URL: pull `product_name`, `brand_name`, value prop, brand color, product form, packaging, hero copy, target user, category, **and the primary language of the page**. Use `category=` if passed; else trust the WebFetch signal; fall back to HAUL for physical, APP for digital.

Build two grounded fact lists from the fetched page:

```json
{
  "grounded_specs": [
    {
      "claim_text": "250W total output",
      "value": "250",
      "unit": "W",
      "source_quote": "visible source-page text containing the exact value",
      "source_url": "<product URL>"
    }
  ],
  "claims_allowlist": ["250W total output"]
}
```

Every numeric spec claim (`W`, `mAh`, `%`, minutes, ports, price, dimensions, counts, charging speeds, battery size, rankings) must come from visible source-page text and include a `source_quote`. If the source page does not visibly support a number, leave it out of `grounded_specs` and `claims_allowlist`. Do not infer specs from product category, model name, common knowledge, or competitor pages.

### 2. Resolve the avatar (fallback to built-in if missing)

- If `avatar_url` was passed → use it as-is.
- If NOT passed → use this built-in fallback:
  ```
  https://cdn.pika.art/v2/files/agent/17d62bf9-0edb-49e4-9ba9-2c5419fa518f/seedream-1777624057811.jpeg
  ```
  Pre-generated 3D animated Pixar-style portrait of a young female creator — pre-cartoonized so seedance moderation accepts it directly, neutral enough to fit any category. Note in the final summary that the fallback was used so the caller knows to supply their own portrait for persona consistency next time.

### 2.5 Avatar-type probe for creator portraits

Run this probe before Step 7 and before any paid `generate_reference_video` call. It applies to caller-supplied `avatar_url`, the built-in fallback, or any creator portrait chosen as `@Image1`. The built-in fallback is already a non-IP stylized creator, but still document its source in the final summary.

Call `analyze_media` once:

```
query: "Classify this image for paid video generation. Is it a photograph of a real human face, an AI-generated realistic portrait, a stylized / illustrated character, or a recognizable trademarked / copyrighted character such as Batman, Pikachu, or Mickey Mouse? Return strict JSON only: { \"avatar_type\": \"real_human\" | \"ai_realistic\" | \"stylized_illustrated\" | \"recognized_ip\", \"recognized_character\": string | null, \"moderation_risk\": \"low\" | \"medium\" | \"high\", \"recommendation\": \"proceed\" | \"warn\" | \"reject\" }. Use null for `recognized_character` when no specific character is recognized; never write \"none\", \"unknown\", or explanatory prose in that field."
```

Route from the result:
- **recognized IP / copyright risk** -> **STOP only when** `avatar_type` is `"recognized_ip"`, or `recognized_character` names a specific character (for example `"Batman"`), or when both `moderation_risk` is `"high"` and `recommendation` is `"reject"`. Treat `recognized_character: null`, empty string, `"none"`, `"unknown"`, `"n/a"`, and low/medium `moderation_risk` as not enough to stop by themselves. Run this check before the real/stylized routes. A chibi Batman is still Batman even when `avatar_type` is stylized / illustrated.
- **real human / AI-generated realistic** -> proceed normally.
- **stylized / illustrated** -> proceed with a visible warning that stylized avatars may be accepted by Kling but can be inconsistent under Seedance moderation; continue only if the user supplied or accepted that avatar.
- **trademarked / copyrighted** -> **STOP** before generation. Surface this message: `The avatar appears to be a trademarked character ([X]). Most video providers will moderate this and refuse to generate. Pass avatar_url=<real-looking-photo-url> to override.`

### 3. Capture the product screenshot (best-effort)

Call `capture_website` with `mode: "screenshot"`. Use `mobile=true` for handheld-product categories (APP / FITNESS / BEAUTY) so the captured page renders as a portrait phone screen; `mobile=false` for desktop-context categories (HAUL / TECH / FOOD).

If the call fails (timeout, browser pool down), retry **once**. If still failing, proceed without the screenshot — the skill is degraded but functional. The close-up beat then describes the page from prose only and Beat 2's `reference_images` is just `[avatar_url]`.

Capture URL → `screenshot_url` (or null).

### 4. Compose the prompt

The full prompt is a single multi-beat string passed to **one** `generate_reference_video` call. Structural prose (not markdown bullets). Every beat has a `Says: "..."` line for lip-sync. Pacing target ~5.5–6 words per second across the whole 15-second ad (≈85–90 words total). `@Image1` is the avatar, `@Image2` is the screenshot when available.

**Write all `Says: "..."` lines in the language detected from step 1's WebFetch.** Both seedance and kling lip-sync handle multilingual; if the product page is Chinese / Japanese / Spanish / etc., the dialogue should be in that language. Hook archetypes from step 5 are language-agnostic — adapt the rhetorical move to the language's natural register.

**Spec-grounding rule:** forbid inventing numbers. Any spoken or visual number/unit claim must appear verbatim in `claims_allowlist`. If a number is not in `claims_allowlist`, rewrite the line qualitatively ("charges fast", "multiple ports", "big battery") or omit the claim. Do not say "50% in 28 minutes", "3 ports", "140W", prices, counts, or time windows unless that exact claim is source-backed.

**Brand/spec text rendering rule:** Do not ask Seedance or the video model to render the brand wordmark, product wordmark, packaging label, or spec text from prose. Video-model text comes out garbled. The prompt may show `@Image2` as a reference, but any new brand name or spec copy that must be readable is added later by the deterministic Step 8 overlay.

```
HOOK (0–3 sec) <visual setting + creator framing + face/body cue>. Says to camera, fast and energetic: "<hook line>". <style anchor — POV handheld, authentic, raw>.

JUMP CUT 1 (3–6 sec) <wide POV — creator's body language, product partially in frame edge>. <face cue>, says fast: "<setup line>".

JUMP CUT 2 (6–9 sec) <next visual beat — could be the screen close-up showing @Image2 OR another reaction beat, depending on which beat the dialogue arc puts the reveal>. Says (or voice continues over the shot if it's a screen close-up), fast and confident: "<reveal line>".

JUMP CUT 3 (9–12 sec) <next visual beat — same logic; one of the JUMP CUTs is the screen close-up, the others are wide-POV reaction shots>. Says, fast: "<insight twist line>".

OUTRO (12–15 sec) <selfie POV, mid-chest framing, same setting>. Says to camera, fast: "<punchline line>".

avatar is image 1, asset is image 2
```

**Screen-close-up beat — exactly one across the ad, position is dialogue-driven:**
- Place the screen close-up on whichever JUMP CUT (1, 2, or 3) the *reveal* line lands on. Most ads put it on JUMP CUT 2; if the narrative needs it earlier or later, JUMP CUT 1 or JUMP CUT 3 is fine. Pick by content, not by slot number.
- The screen close-up beat shows `@Image2` exactly as-is and includes ONE finger-point gesture (a single finger entering from the frame edge, pointing at the hero text or product — no tap, no swipe, no scroll, no hover-on-CTA). The point gesture is the only screen interaction in the entire ad.
- The other JUMP CUTs are wide-POV reaction beats: hands stay on knees, on the bed, or at sides.

**Trust `@Image2`** — when the product page is shown, reference the image; do NOT describe its UI in prose. Describing UI triggers the model to invent extra panels / dropdowns / sidebars / animations. Reference the image; trust it.

### 5. Category essences

Each essence is the brief you read before composing the 5 beats. Pick one from category in step 1 and write the actual `Says: "..."` lines tailored to the real product.

**Category numeric guard:** category archetypes are rhetoric/camera guidance, not permission to invent dates, durations, counts, discounts, costs, ratings, charging times, port counts, output figures, or urgency windows. Any numeric phrase must be rewritten unless the exact claim appears in `claims_allowlist`. When `claims_allowlist` lacks a matching number, use non-numeric language such as "after using it", "during the routine", "the source-backed spec", "launch offer", or "available now".

#### HAUL_UNBOX
- **When to use & why**: fashion, handbags, jewelry, shoes, designer drops, streetwear, luxury cosmetics with packaging story, accessories — anything where brand packaging + texture/material is the value prop. Viewers convert on vicarious-unboxing dopamine + "I just got this" social proof; texture and hardware ARE what the customer pays for, so the close-up lands on materials, not function. Not TECH (→ TECH_UNBOX), not skincare/makeup application (→ BEAUTY_APPLY).
- **Sensory anchors**: tissue rustle, fabric slide, hardware clinks (chains / clasps / buckles), leather/fabric grain under fingertips, foil glint.
- **Setting**: white unmade bed in natural window light; bathroom mirror in background for the outro held-up reveal; streetwear drops may use desk/floor.
- **Close-up beat device**: NOT a screen — product close-up. `@Image2` is a product photo (or brand-site mobile view); the single finger-point lands on a hardware detail (chain, clasp, embossed logo).
- **Dialogue character**: hook is **mystery tease** — frame the unboxing as something the viewer doesn't yet know the contents of; do NOT name the product in the hook line. Arc: hook the unboxing mystery → brand name + drop context → reveal the material/silhouette while close-up holds on hardware → tactile/wearability insight (how it feels on the body) → punchline that invites the viewer to imagine themselves with the artifact.

#### APP_REVEAL
- **When to use & why**: SaaS, AI tools, mobile/web apps, agent-style products, dev tools, productivity tools — anything where the screen IS the product. Viewers convert when they see live UI doing the thing quickly; the close-up beat is the demo, the bookends are the social proof. Not pure hardware (→ TECH_UNBOX).
- **Sensory anchors**: micro-thumb gesture, brand-color highlight, UI alive with small motion, ambient room tone.
- **Setting**: cozy bedroom or couch POV; jeans/joggers at frame edges; warm window light.
- **Close-up beat device**: laptop on bed (desktop screenshot) or phone in hand (mobile screenshot — set `mobile=true` in step 3).
- **Dialogue character**: hook is **bewildered curiosity** — the creator can't categorize the thing yet, that's the point. Do NOT use feature lists or marketing language in the hook; lean into "I don't know what to call this" / "this is wild" register that makes the viewer wait for the name. Arc: bewildered hook → name the product + interaction model in human terms ("you just talk to it", "it builds X from Y") → reveal what it produces (concrete comma-separated examples) while close-up shows the page → personal-insight twist (what it replaces / changes in the user's workflow) → punchline + implicit/explicit "go try it" CTA.

#### FOOD_ASMR
- **When to use & why**: food brands, drinks, kitchen tools, snacks, restaurants with a takeout product — anything where the sensory peak (pour / sizzle / steam / first bite) carries the value prop. Viewers convert on hunger response — show the sensory peak, don't describe it.
- **Sensory anchors**: packaging rustle, knife-on-board, sizzle, pour stream, steam rising, satisfied exhale on the first bite.
- **Setting**: marble counter or warm wood kitchen, top-down framing.
- **Close-up beat device**: a product/dish close-up rather than a screen; phone in hand on the counter only if the brand has a delivery/recipe app.
- **Dialogue character**: hook is **show-don't-tell** — frame as a demonstration the viewer is watching unfold, not a description. The hook line lands while a hand or first ingredient is already in motion; the visual carries the curiosity. Arc: demonstration hook → name the product + first impression → narrate the sensory peak as it happens (pour / sizzle / steam) → satisfaction insight ("this is the new default") → punchline that hands off the recipe or shop link.

#### BEAUTY_APPLY
- **When to use & why**: skincare, makeup, cosmetics, fragrance, hair products, body care — anything where before/after + application ritual is the value prop. Viewers convert on visual transformation under matched lighting; symmetry between hook and outro is what sells the result as real. Not packaging-heavy luxury (→ HAUL_UNBOX).
- **Sensory anchors**: pump press, squeeze, glide on skin, glow lift, droplet beading, brush sweep.
- **Setting**: bathroom mirror, natural daylight or vanity lighting; same angle for the hook and the outro.
- **Close-up beat device**: a product close-up (bottle / tube / compact held in hand), not a screen.
- **Dialogue character**: hook is **routine social proof** — signal real use through a specific moment in the routine, not an invented duration. The hook plants the symmetry payoff that arrives in the after-shot. Arc: routine-use hook → name + source-backed key ingredient or claim → narrate the application as it happens (close-up of fingers/brush on skin) → after-shot reveal (same angle as hook) → punchline that signals exclusivity or repurchase intent.

#### FITNESS_TRANSFORM
- **When to use & why**: workout equipment, supplements, recovery tools, activewear, fitness apps with tracking — anything where the work-to-result transformation is the value prop. Viewers convert on relatable struggle followed by earned payoff — showing the protein-shake bottle is not enough, you have to show the workout.
- **Sensory anchors**: heavy breathing, scoop hitting powder, equipment click, sweat catching light, post-workout exhale.
- **Setting**: gym or home-gym; workout gear at frame edges; floor or bench level.
- **Close-up beat device**: phone in hand showing app stats / heart rate / time elapsed, OR product packaging close-up (scoop in jar, bottle pour).
- **Dialogue character**: hook is **relatable resistance** — name the struggle / friction / not-wanting-to ("I did NOT want to do this", "almost skipped today", "this was supposed to be a rest day"); earns trust by sharing the tired feeling before showing the work. Arc: resistance hook → name the product + non-numeric routine or source-backed claim → narrate mid-work moment while close-up shows the device or scoop → satisfaction insight that earns trust → punchline that frames continued use.

#### TECH_UNBOX
- **When to use & why**: gadgets, hardware, electronics, smart-home devices, wearables, peripherals, AI hardware (Framework laptop, AirPods, Whoop, Rabbit r1, Friend pendant, mechanical keyboards, ergonomic gear) — anything where the device + first-use moment is the value prop. The box ceremony signals premium positioning; viewers convert on seeing "does it actually work / what does it do" — the first-use beat is the conversion moment. Not HAUL (→ HAUL_UNBOX), not pure software/SaaS (→ APP_REVEAL).
- **Sensory anchors**: utility-knife slice, plastic peel, foam slide-out, power-on chime, tactile button press, haptic click, fan spin-up.
- **Setting**: wood desk, top-down framing during unbox; handheld during first-use; desk/lap context for ongoing use.
- **Close-up beat device**: the device itself once unboxed and powered on. `@Image2` is typically a real photo of the device's screen at its key UI moment (first measurement, paired status, hero feature open); if the device has no screen, a clean hero photo of it mid-use.
- **Dialogue character**: hook is **arrival ceremony** — name that this is happening *now* ("just got this", "opening it"). Anticipation > description; the hook plants the question "what does it do?" that the first-use beat answers. Do NOT lead with specs. Arc: arrival hook → name + source-backed spec headline when `claims_allowlist` has one, otherwise qualitative headline → first-use reveal while close-up is on the device doing its thing → workflow-change insight ("this replaces / changes / fixes my X") → punchline that hands off where to find it without inventing cost or urgency.

### 6. Voice — model default

This skill has no voice-cloning input; the video model produces the spoken dialogue with its own default voice. No voice sample is fetched or passed. Proceed to step 7.

### 7. Generate — first attempt with the avatar, cartoonize on rejection, retry

After the Avatar-type probe in step 2.5 passes, attempt the call **first** with the avatar resolved in step 2 (caller-supplied or built-in fallback) exactly as-is. Only when seedance rejects the call do we restyle.

Retry budget: Seedance generation gets at most 2 total video attempts: the original avatar render in 7a, plus one cartoonized-avatar retry in 7c. Do not start a third Seedance render. If the second attempt fails, surface the 7d message or switch to Kling only when the user explicitly requested `provider=kling` or chooses it after the stop message.

**7a. First attempt — avatar as-is**

Call `generate_reference_video`:
- `provider`: `seedance` (default) or `kling` if user passed `provider=kling`
- `aspect_ratio`: `9:16` (default); `3:4` allowed only on seedance
- `resolution`: `720p` (seedance only)
- `duration`: 15
- `reference_images`: `[avatar_url, screenshot_url]` (drop `screenshot_url` if step 3 failed)
- `prompt`: the multi-beat string from step 4
- `sound`: true (default — ambient + lip-sync produced by the model)

For `provider=kling`: convert the multi-beat prose into `shots: [{prompt, duration}, ...]` (5 shots × 3s = 15s sum), plus a top-level `prompt` summarizing the ad. References use `<<<image_1>>>` / `<<<image_2>>>` instead of `@Image1` / `@Image2`.

If the call returns `{ task_id, status: "queued" }`, poll `task_status(task_id)` using the async polling budget above until terminal (`completed | failed | cancelled`). On `completed`, capture `result.url` → `video_url` and proceed to step 8.

**7b. On rejection — auto-cartoonize the avatar**

If 7a returns `422 content_policy_violation` on `image_urls` / `reference_images` (seedance + fal-queue moderation flags portraits that read as too photorealistic — even some Pixar-style 3D avatars get flagged), restyle the avatar in-place:

Call `generate_image_edit`:
- `provider: "seedream"` (native Pixar/3D-animated look)
- `images: [avatar_url]`
- `aspect_ratio`: same as the ad's aspect ratio
- `resolution: "1K"`
- `watermark: false` (seedream-only knob — keep the restyled avatar clean of provider watermark for the downstream lip-sync re-render)
- `prompt: "Stylized 3D game character render — Unreal Engine 5 / Overwatch / Valorant / Apex Legends visual style. Anatomically grounded facial proportions with subtle stylization: slightly larger expressive eyes, defined sculpted cheekbone planes, smooth skin shader (smoother than photoreal, no micropore detail), idealized but believable features. PBR materials with subtle subsurface scattering, strand-based hair simulation, crisp cloth shader. Cinematic three-point studio lighting with strong rim light. Clearly a stylized AAA-game-character render — NOT photorealistic person, NOT Pixar plastic-toy cartoon, NOT exaggerated big-head proportions. Same person, same glasses, same outfit, same accessories. Centered medium portrait, neutral indoor background."`

Capture returned URL → `avatar_url_cartoon`.

**7c. Retry seedance with the cartoonized avatar**

Re-run the exact same `generate_reference_video` call from 7a, swapping the avatar reference: `reference_images: [avatar_url_cartoon, screenshot_url]` (or `[avatar_url_cartoon]` if step 3 failed). All other params unchanged. Capture `result.url` → `video_url`.

**7d. Final fallback — still rejected**

If 7c also returns `content_policy_violation`, stop. Tell the user: the avatar reads as too realistic for seedance moderation even after auto-restyling; ask them to either supply a more stylized portrait themselves or rerun with `provider=kling` (kling has a separate moderation pipeline that accepts realistic avatars).

### 8. Deterministic brand/spec overlays

Before captions, add readable brand/spec copy with deterministic post-generation overlays. This is deliberately separate from the Seedance prompt because video-model text rendering corrupts brand wordmarks and spec labels.

Build overlay copy from Step 1:

```json
{
  "brand_overlay_text": "<brand_name>",
  "grounded_spec_overlay_text": "<one short source-backed claim from claims_allowlist, or empty>",
  "overlay_font_color": "#111111 | #ffffff"
}
```

Rules:
- `brand_overlay_text` is always the exact `brand_name` from WebFetch. If `brand_name` is empty, use `product_name`; do not let the model invent a logo/wordmark.
- `grounded_spec_overlay_text` must be empty or one exact claim from `claims_allowlist`. Never overlay a number that is absent from `claims_allowlist`.
- Choose `overlay_font_color` for contrast against the generated frame, not brand aesthetics. If the screenshot/product surface is light or unknown, use `#111111`; use `#ffffff` only on clearly dark footage. Post-flight OCR must be able to read the overlay.
- Do not use this step for captions or per-word subtitles; Step 9 handles captions with one `add_captions` call.

Call `edit_text_overlay` once for the brand name:

```
edit_text_overlay(
  video_url: video_url,
  text: brand_overlay_text,
  position: "top_left",
  font_size: 54,
  font_color: overlay_font_color,
  start_s: 0.2,
  end_s: 15
)
```

Save the returned URL as `brand_guarded_url`. If `grounded_spec_overlay_text` is non-empty, call `edit_text_overlay` once more on `brand_guarded_url`:

```
edit_text_overlay(
  video_url: brand_guarded_url,
  text: grounded_spec_overlay_text,
  position: "top_right",
  font_size: 42,
  font_color: overlay_font_color,
  start_s: 6,
  end_s: 10
)
```

Save that returned URL as `guarded_video_url`. If no spec overlay is needed, set `guarded_video_url = brand_guarded_url`. If either overlay call returns `{ task_id }`, poll `task_status` using the long-running task contract. If the deterministic overlay fails, stop and surface the failure instead of delivering a video whose only readable brand/spec text depends on Seedance.

Run frame-level OCR on the overlay window before captions. Video-level analysis can miss short-lived top-corner overlays, so extract one frame while both overlays should be visible:

```
extract_frame(
  video_url: guarded_video_url,
  time_s: grounded_spec_overlay_text ? 7 : 1
)
# Save returned url as overlay_qa_frame_url

analyze_media(
  media: overlay_qa_frame_url,
  query: "Expected brand text: ${brand_overlay_text}
Expected spec text: ${grounded_spec_overlay_text}
Return JSON only: { \"visible_text_ocr\": string[], \"brand_visible\": boolean, \"spec_visible\": boolean, \"observations\": string[] }. OCR/read all visible text. brand_visible is true only if the exact expected brand text above is readable. spec_visible is true if expected spec text is empty or the exact expected spec text above is readable."
)
```

If `brand_visible` is false, or `spec_visible` is false when `grounded_spec_overlay_text` is non-empty, stop and rerender the deterministic overlay once with the opposite `overlay_font_color` (`#111111` ↔ `#ffffff`). Re-extract `overlay_qa_frame_url` and rerun the same OCR check. If the retry still fails, stop and surface `overlay_qa_frame_url` and the OCR JSON; do not proceed to captions.

### 9. Captions — single-shot styled burn (default on)

If `variants` is requested, do not run the single-output `add_captions` call in this step. Leave `guarded_video_url` uncaptioned and continue to **Aspect-ratio variants**, where each requested aspect is reframed first and captioned once after reframe.

If `variants` is absent and `captions=false`, skip caption generation and set `final_url = guarded_video_url`. Otherwise, use **one** `add_captions` call instead of chaining `edit_text_overlay` per chunk — much faster (≤5 min single call vs 5–8 min sequential), and the styles position captions correctly out of the box.

Call `add_captions`:
- `video_url`: `guarded_video_url` from step 8
- `style`: `"tiktok"` (default — word-by-word purple highlight, Bebas Neue, all caps, rendered at the **bottom** of the frame; classic TikTok-creator look that keeps the face and screen clear). Alternatives: `"hormozi"` (lower-middle yellow highlight, more aggressive — overlays part of the phone-in-hand close-up beat), `"classic"` (plain bottom subtitle bar, safest), `"karaoke"` (progressive color fill, also bottom).
- `font_size`: `60` — overrides the per-style default; tuned for 9:16 readability without dominating the frame.
- `language`: pass the BCP-47 code for the page language detected in step 1 (`"en"`, `"zh"`, `"ja"`, `"es"`, etc.) — skips auto-detect and avoids misrouting CJK to a Latin-only font path.

Capture the returned URL → `final_url`.

## Aspect-ratio variants

Use optional `variants=9:16,16:9,1:1` when the user wants vertical short-form, landscape, and square feed outputs from the same UGC ad. `variants` overrides `aspect_ratio` to native `9:16`; `aspect_ratio=3:4` is single-output only and must not be combined with variants. If the user requests `variants` with `aspect_ratio=3:4`, use the `9:16` native variant flow and state that `3:4` applies only to single-output runs.

Call `generate_reference_video` once for the native `9:16` ad, then run Step 8 deterministic overlays once to produce `guarded_video_url`. Do not re-run product fetch, avatar analysis, screenshot capture, avatar cartoonization, Seedance/Kling generation, deterministic overlays, or any other expensive provider call for extra variants.

Do not run the single-output `add_captions` call from step 9. Build raw `variant_sources` first, then build a flat `variant_urls` object:

```json
{
  "9:16": "<native final_url>",
  "16:9": "<edit_reframe url>",
  "1:1": "<edit_reframe url>"
}
```

- For `9:16`, set `variant_sources["9:16"] = guarded_video_url`.
- For `16:9` and `1:1`, call `edit_reframe(video_url=guarded_video_url, target_aspect="<aspect>", fill_mode="blur")` and save each returned URL into `variant_sources`. Blur fill preserves the full native vertical ad over a blurred background instead of cutting off the creator or captions.
- If `captions=true`, caption after reframe: run `add_captions` on each `variant_sources` value so burned captions are positioned for that aspect, then save those captioned URLs into `variant_urls`. If `captions=false`, save the uncaptioned native and reframed URLs directly into `variant_urls`.
- Set `final_url = variant_urls["9:16"]` so the primary deliverable matches the native requested variant.
- Treat `edit_reframe` and per-variant caption burn as the cheap final composite / reframe stage. If a reframe fails, return the successful variant URLs plus the failed aspect and tool error; do not resubmit the expensive generation.

> **Heads up — variants use blur fill.** `16:9` and `1:1` keep the full native `9:16` ad visible over a blurred background. Keep the creator, product, and captions centered for readability, but do not describe these outputs as cropped variants.

### 10. Return

Return `final_url` on one line, plus a one-line summary: which category ran, whether the avatar was caller-supplied / built-in fallback / cartoonize-recovered, whether the screenshot was used or fell back to prose, the provider chosen, the language detected for dialogue, and whether captions were burned on. If `variants` was requested, include the flat `variant_urls` object in the same response.

## Post-flight quality gate

Before declaring success, call `analyze_media` on `final_url` when captions were burned, or on `guarded_video_url` when `captions=false`, and ask for a structured verdict. If `variants` was requested, run the same gate on each `variant_urls` value and key any warning by aspect ratio.

Before calling `analyze_media`, substitute concrete expectations into the query: include exact `brand_name`, exact `product_name`, and the actual `claims_allowlist` values as a JSON array. Do not leave placeholders for the model to infer.

```
Expected brand: ${brand_name}
Expected product: ${product_name}
Allowed numeric/spec claims: ${JSON.stringify(claims_allowlist)}

Return JSON only: {
  "verdict": "clean" | "degraded" | "catastrophic",
  "visible_text_ocr": string[],
  "unauthorized_numeric_claims": string[],
  "observations": string[],
  "quality_warning": string | null,
  "re_roll_suggestion": string | null
}
OCR / read all visible text. Use the concrete expected values above when checking that `brand_name` and `product_name` are spelled correctly anywhere they appear, deterministic brand/spec overlays are legible, captions are present when requested and not garbled, and no visible numeric claim appears unless it exactly matches one of the actual `claims_allowlist` values above. Also check that the avatar / creator remains visually stable, the product screenshot or prose fallback matches the product page, and there are no black frames or wrong-product shots.
```

- If `verdict` is `clean`, return `final_url` normally.
- If `verdict` is `degraded`, return `final_url` plus the `quality_warning` so the user can review before publishing.
- If `verdict` is `catastrophic`, if `visible_text_ocr` contains garbled brand/spec text, if `brand_name` is misspelled, or if `unauthorized_numeric_claims` contains any claim not in `claims_allowlist`, do not call the ad complete; surface the verdict and `re_roll_suggestion` instead of declaring success.

## Failure modes

| Symptom | Likely cause | Recovery |
|---|---|---|
| Product page cannot be fetched or captured | The page is gated, blocked, or has too little product evidence | Use caller-provided product facts only if they are explicit; otherwise stop and ask for a product summary or a better URL. |
| Avatar preflight flags recognizable IP, unsafe likeness, or unusable face framing | The provided creator image is not suitable for paid generation | Stop before paid generation and ask for a safer creator image, or fall back to the built-in stylized creator when no caller avatar was supplied. |
| Provider returns 4xx or `moderation_blocked` during image/video generation | The prompt, source image, or product content is rejected deterministically | Do not retry the same payload. Remove the rejected input or switch to the documented fallback provider only when that stage has one. |
| Deterministic overlay OCR fails after the one color retry | The brand/spec copy is still unreadable | Stop with `overlay_qa_frame_url` and the OCR JSON; do not proceed to captions or final delivery. |
| Variant reframe or per-variant caption burn fails | A cheap final composite step failed after the expensive native ad succeeded | Return the successful variants plus the failed aspect/tool error; do not rerun product fetch, avatar prep, or video generation. |

## Load-bearing phrases

These anchors keep the ad from drifting into a generic product demo:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `HOOK + 3 JUMP CUTs + OUTRO` | Prompt skeleton | Forces the TikTok-style multi-cut rhythm instead of one continuous presenter shot. |
| `Every beat has a Says: "..." line` | Prompt skeleton | Gives the video engine explicit lip-sync material across all beats. |
| `Trust @Image2` | Screen close-up rule | Prevents invented product UI when a real screenshot is already supplied. |
| `exactly one` screen-close-up beat | Prompt composition | Keeps the ad from becoming a screen recording instead of a creator-style reveal. |
| `Write all Says lines in the language detected from step 1` | Dialogue rule | Keeps localized product pages from getting English dialogue by default. |
| `forbid inventing numbers` | Prompt grounding | Prevents unsupported spec claims from entering narration or overlays. |
| `Deterministic brand/spec overlays` | Step 8 | Keeps readable brand names and spec copy out of video-model text rendering. |
| `single add_captions call` | Caption step | Avoids quality loss and drift from chained text overlays. |

## Examples

- `/pika:ugc-ads https://pika.me avatar_url=https://cdn/face.png` → APP_REVEAL, 9:16, seedance, real screenshot, captions on
- `/pika:ugc-ads https://maisonbrune.com avatar_url=https://cdn/face.png aspect_ratio=3:4` → HAUL_UNBOX, 3:4, seedance
- `/pika:ugc-ads https://pika.me avatar_url=https://cdn/face.png provider=kling captions=false` → APP_REVEAL, 9:16, kling shots[], no captions
- `/pika:ugc-ads https://pika.me` → no `avatar_url` → uses the built-in fallback Pixar-style female creator portrait, runs end-to-end
