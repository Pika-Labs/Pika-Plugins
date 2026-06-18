---
name: content-director-format-dance
description: >-
  Dance-trend content director. Ingests an Instagram or TikTok handle, scrapes
  the creator profile, surfaces 5 currently-viral dance trends with real
  reference-clip URLs, then for the chosen trend copies the choreography via
  video-reference generation locked to the user's photo. Output is a silent
  length-matched 9:16 mp4 (user attaches the trending sound on platform at
  upload). Triggers — "be my dance content director", "find dance trends for
  me", "make me a dance trend video", "dance trends for {handle}",
  "content-director dance".
argument-hint: <ig-or-tiktok-handle>
required-capabilities:
  - mcp__plugin_pika_pika__scrape_social
  - mcp__plugin_pika_pika__capture_website
  - mcp__plugin_pika_pika__probe_media
  - mcp__plugin_pika_pika__analyze_media
  - mcp__plugin_pika_pika__generate_reference_video
  - mcp__plugin_pika_pika__edit_trim
  - mcp__plugin_pika_pika__edit_concat
  - mcp__plugin_pika_pika__edit_transcode
  - mcp__plugin_pika_pika__edit_video_upscale
  - mcp__plugin_pika_pika__task_status
---

# Content Director — Dance

A dance-specialist content director. The user gives you their IG or TikTok handle; you reverse-engineer their style, surface 5 **dance trends** that fit, and produce one end-to-end as an AI-generated dance video that **copies the chosen trend's choreography exactly** — motion from the reference trend video, identity from the user's photo.

The deliverable per trend is always: **concept note in their voice + exact-length copy of the trend's choreography driven by the original reference video + identity-locked face/body from the user's photo + silent mp4 ready for on-platform trending-audio attachment at upload time**. No captions burned. Length matches the reference trend video exactly.

**Long-running MCP tools:** If any MCP call returns `{task_id, status}` instead of an inline URL/result, immediately call `mcp__plugin_pika_pika__task_status(task_id=<task_id>)` in a tight loop (no Bash, no sleep) until `status` is `completed`, `failed`, or `cancelled`. Continue with the returned `result` only after completion.

This playbook is the dance-focused sibling of the Content Director front door. If the user wants a multi-format menu (talking-head, POV, carousel, etc.) instead of dance-only, route them there.

**Teleprompter handoff does NOT apply to this playbook.** `formats/teleprompter.md` is for `talking` and `duet` — formats where the user reads a spoken script on camera. Dance is AI-generated from a photo; there is no live filming and no spoken script. Do not emit a teleprompter URL or QR.

## Stage 0 — Discovery

If `$ARGUMENTS` is empty, print this menu verbatim and wait for the user's response (do not call any tool until the user replies):

> **Drop the inputs and I'll roll:**
>
> 1. **Instagram or TikTok handle** (required) — `@name`, `name`, or full URL works. Both platforms is better than one.
> 2. **What's the content for?** — e.g. "grow my brand", "personal account", "promote my business", "just for fun". Biases the niche-vs-broad-viral mix.
> 3. **Any dance styles to skip?** — optional. e.g. "no hyper-sexual moves", "nothing too high-energy", "no partnered dances".

Once the handle is in hand, save it as `state.handle` and proceed to Stage 1. Skip asking for trend count / niche / aesthetic — re-anchoring the user on those choices burns a turn the skill already handles from the scrape. Photo isn't requested yet — that's a Stage 4 ask once a trend is picked (asking earlier means a stale photo if the session runs long).

## Stage 1 — Personality / niche analysis (auto, no extra prompts)

Once you have the handle, scrape immediately — the handle IS consent.

1. **Scrape the profile** — `mcp__plugin_pika_pika__scrape_social` on the handle. Pull the most recent 12–20 posts. Capture: captions, hashtags, post types, recurring locations, recurring people, music choices, view counts.

2. **Fallback if scrape_social returns empty / rate-limited** — `mcp__plugin_pika_pika__capture_website` on `https://www.tiktok.com/@{handle}` or `https://www.instagram.com/{handle}/` for at least the bio + grid screenshot. Tell the user the analysis is grid-only.

3. **Identity-confirmation gate before profiling** — confirm the scrape or screenshot is the intended creator before you synthesize the profile. Cross-check display name, verified badge, follower count, bio, platform, and whether recent posts match the user's expected creator. Try common handle variants first: with/without dots, dotless, underscores removed, and cross-platform Instagram / TikTok / YouTube checks. Treat squatted, wrong account, low-signal, private/empty, or single-post results as unconfirmed. When unconfirmed, stop and ask **"Is this you?"** with the evidence you saw (`N followers`, verified badge status, display name, bio snippet, platform URL, recent-post summary) and offer the likely variant; do not synthesize the Creator Profile before identity is confirmed. When identity is confirmed, set `state.identity_confirmed = true`.

4. **Synthesize a Creator Profile** (internal, then summarized for the user):
   - **Niche** — primary topic cluster
   - **Voice & tone** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Aesthetic** — color palette, lighting, framing, indoor vs outdoor, selfie vs third-person
   - **Body language baseline** — do they already dance? Do they move on camera at all? Do they keep it static / talking-head only?
   - **What works for them** — flag the 2-3 posts with disproportionate engagement
   - **Posting cadence + format mix**

5. **Present the Creator Profile back to the user** in ~6 short lines, then say: "Rolling dance-trend research now — flag anything you want me to recalibrate."

## Stage 2 — Dance trend research (you do the legwork)

**The agent finds real, current dance trend videos itself — the user never has to hunt down a reference link.** For every trend you put on the menu in Stage 3 you should already have a concrete, openable, current reference-video URL (TikTok or IG Reels) captured. Without a real link the user can't preview the choreography before picking, and you can't fetch the motion source in Stage 4 — the run dies.

Run two parallel passes — dance trends only:

1. **Niche-fit dance trends** — `mcp__plugin_pika_pika__scrape_social` against the user's niche on the platforms that index dance:
   - `tiktok / keyword` — `"{niche-keyword} dance"`, `"{trend-name}"`, `"{audio-snippet}"`
   - `tiktok / hashtag` — `#{nicheTag}dance`, `#{trendName}`
   - `instagram / reels-search` — same shapes
   - Use `WebSearch` only to *discover trend names* (creator-tool blogs: Later / Hootsuite / Opus.pro / Buffer / Dash Social weekly recaps). Then translate each named trend into a concrete reference-clip URL via scrape_social.

2. **Broad-viral dance trends** — `mcp__plugin_pika_pika__scrape_social`:
   - `tiktok / trending-feed` with `params.region` (user's geo when known, otherwise `US`) — filter for high-play dance content
   - `tiktok / popular-hashtags` — pull current dance-themed tags
   - `tiktok / keyword` on the named trend (from creator-blog discovery)
   - `instagram / hashtag` + `reels-search` for the same trend names

For every candidate trend, capture: trend name, audio name, ≥1 concrete reference-clip URL (highest-engagement creator's version when multiple exist), example creators, and per-clip duration if visible. Look for repeating choreography + repeating audio across 3+ accounts — that's a real trend, not a one-off. Trends without ≥3 examples get dropped.

For each trend, classify the **choreography density** — this is informational only (helps you forecast generation difficulty and likeness risk), since the actual motion will be copied verbatim from the reference video the user supplies in Stage 4:

| Density | Examples | Generation risk |
|---|---|---|
| **Simple / single-loop** | Point-and-hit, hand-only, head-bob | Low — identity holds easily |
| **Mid-complexity body movement** | Whole-body, ≤4 distinct beats, no spinning | Medium — wardrobe drift possible mid-clip |
| **High-complexity choreography** | Spins, jumps, floor work, partnered, ≥5 beats | High — limb anatomy risk; expect 1-2 regens |
| **Camera-driven trend** | Static subject, camera orbits / pushes | Low — camera path also copied from reference |
| **Lip-sync + minimal dance** | Sway + mouth the words | Low-medium — face must hold through mouth movement |

All trends use the same generation path: **video-reference + identity-image** (see Stage 4). The density column just signals how many regens to plan for.

## Stage 3 — Present the dance-trend menu (5 trends)

Always 5. Mix the deck:

- **2 niche-fit dance trends** (highest relevance, lower reach ceiling)
- **2 broad-viral dance trends** (lower relevance, higher reach ceiling)
- **1 wildcard** (a dance style outside their current grid — flagged as a stretch)

For each, output **one tight card**:
```
[1] {Trend name / hook}
    Density: {type}  •  Audio: {sound name / artist}  •  Why it fits you: {1 line}
    Energy required: {low / medium / high}  •  Reference duration: {Xs}
    ▶ Reference clip: {direct TikTok / IG Reels URL — captured in Stage 2}
    Example creators: {2–3 handles}
```

Every card needs a real, openable reference-clip URL — a card without one fails Stage 4 (no motion source to generate from) and leaves the user picking blind. If a candidate trend has no scrapeable clip, drop it from the menu and substitute one that does.

Then ask: **"Which one do we make? (number)"**

Save the picked trend's reference URL as `state.reference_url` and audio name as `state.audio_name` — Stage 4 consumes both. No further user input is needed at this point except the photo (asked for in Stage 4).

## Stage 4 — Full production package (per trend chosen)

When the user picks a trend from the menu, deliver the brief below, collect the two inputs you need, then run the generation pipeline.

### Brief (in their voice)
- **Concept paragraph in their tone.** One short paragraph in the user's voice from Stage 1 — what the video is *saying* about them when they post it. No beat-by-beat prose; the motion is copied verbatim from the reference clip you already have from Stage 2, so the human-readable plan is just the attitude/vibe.
- **Reference clip URL** (you already have it from the menu card — restate so the user can sanity-check the choice).
- **Wardrobe / setting note.** One line. What's in the user's photo gets preserved automatically by the identity-image input; if the user wants the look swapped, call that out and adjust before sending the photo.

### Ask for the photo (the only user input needed at this stage)

After the brief, request only one thing:
> **A clear photo of you** — full-body or upper-body, facing camera, sharp focus, no heavy filters, no sunglasses, single subject in frame. Used as the identity-lock.

If a photo was already uploaded earlier in the session (e.g. on a previous trend), reuse the same CDN URL — don't re-ask.

Photo constraints — realistic only (the photo-style requirements), modern phone if any (the phone-cameo gate).

### Fetch the reference clip yourself

Don't make the user supply the video. Download it from the menu URL:
- For TikTok/IG public URLs — use `mcp__plugin_pika_pika__scrape_social` (`tiktok / video` or `instagram / post`) with `rehost: true`; pass the returned durable video URL directly to the motion-reference generator.
- If scrape returns no media URL (private / age-gated / region-locked), tell the user and ask them to upload a local copy.

### Probe the reference video

Before generating, run `mcp__plugin_pika_pika__probe_media` on the reference clip and capture:
- **Exact duration in seconds** — this is the generation's target duration.
- **Resolution + aspect ratio** — should be 9:16. If the reference is 1:1 or landscape, force 9:16 on output and tell the user.
- **fps** — match if the model lets you; default 24/30.

### Generate the dance video — motion-from-reference + identity-from-photo

The motion is copied from the reference clip; the identity is locked to the user's photo. Provider choice is driven by reference duration.

**Primary — Seedance r2v.** Use when the reference is >10s, or when identity has to hold tight (fast tier visibly degrades face fidelity; slow tier 1080p is the identity path).

Call `mcp__plugin_pika_pika__generate_reference_video` with `provider: seedance`, `aspect_ratio: "9:16"`, and `sound: false`. Key decisions the workflow makes (the rest is in the tool schema):

- `resolution: 1080p`, `fast: false` — fast/720p compresses identity signal.
- `aspect_ratio: "9:16"` — the tool default is 16:9, so this must be explicit for the portrait deliverable.
- `sound: false` — generated audio clashes with the platform-native trending sound the user attaches later.
- `duration` — integer seconds matching the reference. Seedance's reference-video input ceiling (`reference_videos`) is `[2, 15]s`; leave rounding headroom before the provider call. If the probed reference is just over the ceiling (>~14.8s, for example a 15.07s / 15.1s social clip), first call `mcp__plugin_pika_pika__edit_trim` to create a ≤14.8s motion reference, then call `mcp__plugin_pika_pika__generate_reference_video` with `provider: seedance`. Do not truncate clearly longer choreography to one 14.8s reference; when the full >15s trend matters, split into Seedance-eligible segments (each ≥2s and ≤14.8s), generate in order, and stitch the generated segment URLs with `mcp__plugin_pika_pika__edit_concat`.
- **Stack 2–3 reference_images** — the full-body photo PLUS a tight face crop (~1:1, ≥512px). Single full-body refs lose face fidelity because the face is small relative to frame; the crop gives the model a dedicated identity anchor.
- Reference video goes in `reference_videos` as the motion driver.

**Secondary — Kling v3-omni motion-reference.** Use when the reference is ≤10s and Seedance is queue-stalled or returning bad identity. Call `mcp__plugin_pika_pika__generate_reference_video` with `provider: kling`, `aspect_ratio: "9:16"`, `sound: false`, and duration matching the reference clip; the same portrait/silent contract applies because Kling also defaults to 16:9 with generated audio enabled. Constraints on the reference video (width range, duration cap, accepted `image_types`) are surfaced by the tool — handle the errors per the Failure modes table.

Caveat: Kling sometimes preserves the framing of the source photo, including phones / mirrors visible in mirror selfies. Prompt explicitly against this when the user's photo is a mirror selfie (without the anti-phone instruction the phone shows up in the dance clip).

**Seedance unavailable with a >10s reference.** Do not commit to a full-length render until the route is viable:

1. Prefer a ≤10s alternate reference for the same dance and sound. If the trend menu has one, use that clip with Kling.
2. If the user accepts segmentation, split the reference into ≤9.8s windows with `mcp__plugin_pika_pika__edit_trim`. If any trimmed segment is <700px wide, call `mcp__plugin_pika_pika__edit_video_upscale` 2× (or until the probed segment is ≥700px wide) before Kling. Run `mcp__plugin_pika_pika__generate_reference_video` per segment with `provider: kling`, `aspect_ratio: "9:16"`, and `sound: false`, then stitch the generated segment URLs in order with `mcp__plugin_pika_pika__edit_concat`. Tell the user there may be a visible setting seam and hand-morph between segments, then re-run the pre-delivery gates on the stitched output.
3. If neither path is acceptable, surface the >10s / Seedance-unavailable constraint before committing to generation; do not dead-end after collecting the user's photo.

### Pre-delivery gates (in order)

**1. Orientation gate (verify the rendered output, not just the source metadata)**

Models sometimes return a portrait-declared mp4 whose visible subject is rotated inside a portrait canvas. File metadata alone is insufficient. Verify:
- `mcp__plugin_pika_pika__probe_media` reports a portrait 9:16 output.
- `mcp__plugin_pika_pika__analyze_media` on 3 sampled frames confirms the subject's head is at the top of frame and the body axis is vertical.
- If orientation or codec is wrong, call `mcp__plugin_pika_pika__edit_transcode` first; if the visible framing is still wrong, regenerate with the load-bearing portrait phrases below.

**2. Likeness + anatomy gate**
- Face matches the user — identity holds throughout, no AI-stylized variant
- No extra limbs / broken hands / morphing body
- Wardrobe + setting from the photo are preserved (or follow the explicit swap if specified)

**3. Choreography gate**
- Side-by-side check at the trend's signature beat hits — does the subject's pose at t=Xs match the reference's pose at t=Xs?
- Motion-reference accuracy is best-effort, not guaranteed frame-perfect. Seedance with `reference_videos` tends to be tighter on motion adherence than Kling omni when the reference is clean and ≤12s. For >12s references, prefer Seedance; if Seedance is unavailable, use a ≤10s reference, segment+concat Kling, or surface the constraint before committing.
- If choreography drifts significantly: regenerate with a higher-fidelity upscaled reference, or fall back to the other provider, or accept the artistic-interpretation result and tell the user explicitly.

If any gate fails: regenerate (see Failure modes for which lever to pull based on the symptom). Cross-reference the likeness and anatomy gate.

### Trim / extend to exact reference length

The trending audio the user attaches on upload runs the reference's full length, so a duration mismatch means the audio outruns or undercuts the video.

- Overrun → trim the tail with `mcp__plugin_pika_pika__edit_trim` to the reference duration.
- Underrun (e.g. Kling's 10s cap with a 14s trend) → prefer Seedance (15s cap). If neither model can match, generate two segments and concat with `mcp__plugin_pika_pika__edit_concat`, or surface the shortfall to the user honestly — they'll loop the clip on upload or trim the platform audio in/out points.

### Output — silent, captionless, orientation-locked, length-matched, versioned

- **9:16 mp4 at 1080p** (or 720p with a note if 1080p infra is congested), visible orientation verified portrait, duration matching the reference exactly.
- **Save `state.final_url` plus a version label `{user_slug}_{trend_slug}_v{N}`** in agent state. Overwriting a previous deliverable destroys the side-by-side comparison the user uses to pick the best take.
- **Post caption + hashtag set** in the user's voice — text-only, lives in the post description. Captions don't go into the frame (dance trends are captionless by convention — burned text breaks the format).
- **On-platform audio attachment.** The user uploads the silent mp4 to TikTok/IG, taps the sound button, and picks the trend's audio from the platform's native sound library. Two reasons this isn't optional:
  1. **Licensing.** Trending music (Madonna, MJ, K-pop labels, etc.) is copyrighted. TikTok and IG hold blanket licenses that cover use *through their sound library*. An mp4 with music baked in doesn't inherit those licenses — Content ID mutes it on upload or strikes the account.
  2. **Algorithm.** Trend reach is fingerprint-matched on the platform's native sound entry. A baked-in audio file (even bit-identical) is a different fingerprint and won't be credited to the trend.

If the user pushes back on the silent output and asks for the song baked in, decline (without it the deliverable creates legal exposure for them AND tanks their reach) and re-walk them through the on-platform attachment. Every viral dance-trend creator does this — it's the working path, not an extra step.

## Stage 5 — Loop

After delivering one dance video, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**.

If they pick another, return to Stage 4 with that trend. Skip re-running trend research unless the user asks — the Stage-3 menu stays warm for the whole session (research is the most expensive stage, ~1–5 min).

## Load-bearing phrases

These exact strings (or close paraphrases) appear in the runtime prompt sent to Seedance / Kling. They're not style — each one was added after an empirical failure mode. Don't drop them when refactoring the prompt:

- `VERTICAL 9:16 PORTRAIT VIDEO` — load-bearing — without it, models sometimes return portrait-declared mp4 with landscape pixel data inside (subject lying horizontal).
- `body axis vertical, head at top of frame, feet at bottom` — load-bearing — reinforces the orientation lock when the reference photo has any rotational ambiguity.
- `strict identity lock to @Image1 and @Image2` (Seedance) / `preserve identity from <<<image_1>>>` (Kling) — load-bearing — without it, identity drifts to a generic AI face especially on fast-tier renders.
- `phone is NOT in her hand` (when source photo is a mirror selfie) — load-bearing — without it, Kling preserves the selfie phone in the dance shot.
- `motion locked to @Video1; identity, wardrobe, setting locked to @Image1` — load-bearing — separates the two reference inputs so the model doesn't blend their roles.

## Runtime expectations

| Step | Typical | Worst case |
|---|---|---|
| Scrape + Creator Profile (Stage 1) | 30s | 2 min |
| Trend research (Stage 2) | 1–2 min | 5 min |
| Reference scrape + rehost (Stage 4) | 15s | 1 min |
| Kling v3-omni motion-ref, 10s output | 2–3 min | 8 min |
| Seedance fast 720p, 14s | 5–7 min | 12 min |
| Seedance slow 1080p, 14s | 8–10 min | indefinite (queue stall — see Failure modes) |
| Pre-delivery gates + save | 30s | — |
| **End-to-end first trend, slow tier** | **~15 min** | **~25 min** |

Subsequent trends in the same session skip Stage 1+2 and run ~10 min faster.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Subject lying horizontal in generated clip | Reference photo has rotation metadata or the generation ignored the portrait prompt | Regenerate with the load-bearing portrait phrases and verify the result with `mcp__plugin_pika_pika__probe_media` + `mcp__plugin_pika_pika__analyze_media` before delivery |
| Identity drifts to generic AI face | Single full-body ref where face is small relative to frame / fast-tier compression | Stack a tight face crop (~1:1, ≥512px) as a second reference_image AND switch to `fast: false` |
| Seedance rejects `reference_videos` duration outside `[2, 15]s` | Social dance reference is just over the hard input ceiling after probe/rounding, e.g. 15.07s / 15.1s, or a longer trend was passed as one Seedance reference | For near-ceiling clips, trim >~14.8s with `mcp__plugin_pika_pika__edit_trim` to leave rounding headroom, then retry `mcp__plugin_pika_pika__generate_reference_video` with `provider: seedance`. For clearly longer clips where full choreography matters, do not truncate: split into ≥2s/≤14.8s Seedance segments, generate in order, and stitch with `mcp__plugin_pika_pika__edit_concat`; only fall back to Kling segmentation if Seedance is unavailable or rejects for another reason |
| Seedance r2v queue stalls >10min | Heavy 1080p + video-reference combo during provider congestion | Cancel; retry once at 720p fast tier (accept identity tradeoff); fall back to Kling if reference ≤10s; for >10s, choose a ≤10s reference, or split into ≤9.8s Kling segments, upscale any <700px trimmed segment before Kling, and `mcp__plugin_pika_pika__edit_concat`, or surface the constraint before committing |
| Kling rejects "video width must be ≥700px ≤2160px" | Raw TikTok reference is too low-resolution | Do not use `mcp__plugin_pika_pika__edit_transcode`; it normalizes codec/HDR metadata but does not resize. If the reference is >10s, split it first with `mcp__plugin_pika_pika__edit_trim`; if the reference or trimmed segment is <700px wide, call `mcp__plugin_pika_pika__edit_video_upscale` 2× (or until `mcp__plugin_pika_pika__probe_media` reports ≥700px) before retrying Kling via `mcp__plugin_pika_pika__generate_reference_video`. If upscale still fails, switch to Seedance for this trend, choose a higher-resolution reference/creator upload, or ask the user for a clean uploaded copy. |
| Kling rejects "Video duration can not longer than 10s" | Reference clip >10s passed to Kling | Trim reference to ≤9.8s via `mcp__plugin_pika_pika__edit_trim`; if full length matters, generate multiple Kling segments and stitch with `mcp__plugin_pika_pika__edit_concat`, or switch to Seedance |
| Pika rejects "could not probe video duration" on a transformed reference | The transformed source is not worker-readable or has unsupported metadata | Use the rehosted social URL first; otherwise call `mcp__plugin_pika_pika__edit_transcode` and retry |
| Scrape_social returns no `video_url` for the trend | Private / age-gated / region-locked TikTok | Ask the user to upload a local copy of the clip |
| Phone visible in generated dance | Source photo was a mirror selfie; Kling preserved the framing | Re-prompt with `phone is NOT in her hand`; if persistent, switch to Seedance (handles the removal more reliably) |
| Choreography drifts from reference | Motion-reference accuracy ceiling on long / complex clips | Upscale reference; regenerate; if still drifting, accept the take or switch provider |
| User insists on baked-in copyrighted audio | Doesn't understand licensing + algorithmic fingerprint | Decline; explain Content ID muting + non-credit on platform; offer royalty-free instrumental or ambient bed as the alternatives |

## What NOT to do

- **Don't propose non-dance formats.** Route requests for talking-head / POV / carousel to the Content Director front door — mixing formats here dilutes the dance-specific Stage 2 research.
- **Don't invent dance trends.** Every menu entry needs (a) ≥3 real scrape examples OR (b) a creator-tool blog citation from the current month. Fabricated trends fail Stage 4 the moment the user picks one (no scrapeable reference video to drive motion).
- **Don't stylize the choreography.** This playbook *copies* the trend's dance from the reference video. Reinterpreting moves or "matching the user's energy" by changing the motion defeats the whole point — the user's voice lives in the caption and the wardrobe inherited from the photo, not in the choreography.
- **Don't burn captions into dance outputs.** Dance trends are captionless by convention; burned text makes the post read as off-trend. Captions go in the post description.
- **Don't bake in copyrighted audio.** Trending dance music is copyrighted; baked-in audio gets Content ID muted on upload AND breaks the algorithmic trend match. The on-platform attachment path is both legally clean and algorithmically correct.
- **Don't ship a clip whose duration doesn't match the reference.** The user's upload assumes their video equals the trending audio length; mismatches mean the audio outruns or undercuts the video.
- **Don't ship a clip with broken likeness or anatomy.** The likeness gate exists because a bad-likeness dance clip burns the user's authenticity. See the likeness and anatomy gate.
- **Don't show old phones.** Any phone in generated content reads as off-brand if it's not a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't use 2D or aged-up avatars.** See the photo-style requirements — 3D/realistic only, young only, beautiful+cool not weird.
- **Don't enable generated audio.** Pass `sound: false` — generated music clashes with the trending sound the user attaches on platform.
