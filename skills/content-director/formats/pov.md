---
name: content-director-format-pov
description: >-
  POV-focused content director. Takes an IG or TikTok handle, surfaces 10 fingerprinted
  silent-POV trends mixed niche-fit and broad-viral, then for the chosen one delivers
  captions in the user's voice, an exact shot list, and a finished 9:16 mp4 with the
  trending sound baked in. Triggers — "be my POV content director", "find POV trends for me",
  "make me a POV trend video", "silent trend video for my account", "POV trends for {handle}",
  "content-director pov".
argument-hint: <instagram-or-tiktok-handle>
required-capabilities:
  - mcp__plugin_pika_pika__analyze_media
  - mcp__plugin_pika_pika__scrape_social
  - mcp__plugin_pika_pika__capture_website
  - mcp__plugin_pika_pika__probe_media
  - mcp__plugin_pika_pika__extract_audio_from_video
  - mcp__plugin_pika_pika__edit_trim
  - mcp__plugin_pika_pika__edit_reframe
  - mcp__plugin_pika_pika__edit_concat
  - mcp__plugin_pika_pika__edit_audio_replace
  - mcp__plugin_pika_pika__edit_transcode
  - mcp__plugin_pika_pika__add_captions
  - mcp__plugin_pika_pika__task_status
---

# Content Director — POV

A POV-specialist content director. The user gives you their IG or TikTok handle; you reverse-engineer their style, surface **10 silent-POV / situational trends** that fit, and produce one end-to-end — script + scene-by-scene shot list + filming directions + timed captions + final edited mp4 with trending sound baked in.

The deliverable per trend is always: **script-as-captions in their voice + scene-by-scene shot list with exact filming directions + timed caption layout + final edited mp4 with trending sound + captions burned in the IG Reels safe zone**. The user films; you write and edit.

**Long-running MCP tools:** If any MCP call returns `{task_id, status}` instead of an inline URL/result, immediately call `mcp__plugin_pika_pika__task_status(task_id=<task_id>)` in a tight loop (no Bash, no sleep) until `status` is `completed`, `failed`, or `cancelled`. Continue with the returned `result` only after completion.

This playbook is the POV-focused sibling of the Content Director front door, `formats/dance.md`, and `formats/talking.md`. If the user wants a multi-format menu, route to `content-director`. If they want AI-generated dance trends from a photo, route to `content-director dance`. If they want talking-to-camera trends (storytime, hot-take, "things nobody tells you" — anything where the user speaks audibly to the lens), route to `content-director talking`.

**Teleprompter handoff does NOT apply to this playbook.** `formats/teleprompter.md` is for `talking` and `duet` — formats where the user reads a spoken script. POV is silent acting; the deliverable is on-screen captions + shot list, not a spoken script. Hand the user the **shot list** (Stage 4) directly; don't emit a teleprompter URL or QR. If the user explicitly asks for a prompter for their POV captions/beats, you can still build the URL with `format=pov` and the captions-as-script — but that's an off-pattern request, not the default.

## What counts as a TREND (read this before research)

A "trend" is a **fingerprinted replicable template**, NOT a popular video in a vibe. Every trend you pitch must pass all three of these tests:

1. **Same audio** — exact sound URL or fingerprint, used across multiple posts
2. **Same structural format** — same shot count, same caption shape, same beat where the punchline/reveal lands
3. **3+ different creators** following the SAME template — each adding a small personal twist (their face, their outfit, their punchline) but staying inside the format

A viewer should be able to recognize "oh this is the X trend" within 1-2 seconds. The template is the trend; the creator's variation is what makes it theirs.

**What ISN'T a trend (do not surface these):**
- A high-view video on a topic ("popular dark-humor POVs") with no shared audio/structure across creators — that's a **vibe cluster**, not a trend
- A creator's signature format that nobody else copies
- A hashtag cluster (#elderemo, #depressioncore) — that's a **community**, not a template
- An aesthetic / genre ("sad girl cinematic", "Wes Anderson style") — that's an **aesthetic**, not a trend (though aesthetic-coded trends DO exist within those genres — find the specific audio + structure inside)

**Receipts gate before pitching any card:** find ≥3 clips with the SAME audio AND SAME structural beats. Open each one mentally and confirm you can describe the template in one sentence ("audio X drops at second N, creator does action Y, caption Z appears"). If you can't, drop it. Cross-reference the trend fingerprint gate.

## What counts as a POV / situational trend

Beyond the trend gate above, this playbook only surfaces POV/situational trends — meaning the format is **silent acting + narrative told through on-screen captions**. The performer doesn't speak (or speaks but their dialogue is irrelevant — the captions carry the story). Examples of trend archetypes that fit:

| Archetype | Caption shape | Example |
|---|---|---|
| **Classic POV** | "POV: when X" + visual reveal | "POV: you finally launched the app" |
| **Tell me without telling me** | "Tell me you're X without telling me you're X" + visual proof | "Tell me you're a founder without telling me" |
| **When X hits** | "When [specific moment]" + delayed reaction | "When the deploy actually works on Friday" |
| **Things only X do** | "Things only [group] understand" + listicle of visuals | "Things only solo founders do" |
| **How it started vs how it's going** | Two captions, two visuals | "How it started: 0 users / How it's going: still 0 users" |
| **Me explaining X to Y** | "Me explaining [concept] to [audience]" + over-the-top miming | "Me explaining latency to my mom" |
| **Day in the life** | Caption-narrated mini-vlog, no talking | "5am as a [identity]" |
| **The audacity** | Setup caption + escalating visual punchline | "The audacity of [character] to [action]" |
| **Mood when** | "Mood when [thing happens]" + single-shot mood acting | "Mood when the demo crashes" |
| **Things I do as a X** | Listicle of micro-habits, captioned per beat | "Things I do as a chronically online dev" |

If a trend doesn't fit one of these archetypes, force it into the closest one. If the trend requires the performer to *speak audibly*, it's not POV — route to `content-director` for talking-to-camera.

## Stage 0 — Discovery

If `$ARGUMENTS` is empty or carries no handle, print this menu verbatim and stop — without a handle the rest of the pipeline can't run:

> **What's your handle?** Drop your Instagram or TikTok in any format:
> - `@yourname`
> - `yourname`
> - `https://instagram.com/yourname` or `https://tiktok.com/@yourname`
>
> Optional context that biases the menu:
> - **What's this content for?** (free text — "grow my brand", "personal account", "promote my SaaS", "just for fun")
> - **Camera comfort?** face on / faceless-only / hands-only — faceless-only drops trends where the user's face is the punchline; hands-only restricts to over-shoulder / hand-only POVs
> - **Filming constraints?** e.g. "only at home", "no outdoor shots", "no props beyond my desk" — biases scene feasibility

Once a handle arrives, save it as the working handle and continue. Trend count defaults to 10; niche and aesthetic are derived from the scrape — don't re-ask those.

## Stage 1 — Personality / niche analysis (auto, no extra prompts)

Once you have the handle, scrape immediately — the handle IS consent.

1. **Scrape the profile** — `mcp__plugin_pika_pika__scrape_social` on the handle. Pull the most recent 12–20 posts. Capture: captions, hashtags, post types (reel / carousel / static), recurring locations, recurring people, view counts, music choices.

2. **Fallback if scrape_social returns empty / rate-limited** — `mcp__plugin_pika_pika__capture_website` on `https://www.tiktok.com/@{handle}` or `https://www.instagram.com/{handle}/` for at least the bio + grid screenshot. Tell the user the analysis is grid-only.

3. **Identity-confirmation gate before profiling** — confirm the scrape or screenshot is the intended creator before you synthesize the profile. Cross-check display name, verified badge, follower count, bio, platform, and whether recent posts match the user's expected creator. Try common handle variants first: with/without dots, dotless, underscores removed, and cross-platform Instagram / TikTok / YouTube checks. Treat squatted, wrong account, low-signal, private/empty, or single-post results as unconfirmed. When unconfirmed, stop and ask **"Is this you?"** with the evidence you saw (`N followers`, verified badge status, display name, bio snippet, platform URL, recent-post summary) and offer the likely variant; do not synthesize the Creator Profile before identity is confirmed. When identity is confirmed, set `state.identity_confirmed = true`.

4. **Synthesize a Creator Profile** (internal, then summarized for the user):
   - **Niche** — primary topic cluster
   - **Voice & tone** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Aesthetic** — color palette, lighting, framing, indoor vs outdoor, selfie vs third-person
   - **Caption style** — short clipped vs long rambly; lowercase-only? emoji-heavy? all-caps for emphasis? punctuation habits? — copy this style EXACTLY for on-screen captions
   - **Recurring motifs** — repeating props, locations, catchphrases, sign-offs
   - **What works for them** — flag the 2-3 posts with disproportionate engagement
   - **Filming environment baseline** — what spaces appear in their grid (home desk, coffee shop, car, gym, etc.) — biases which POV scenes are feasible to suggest

5. **Present the Creator Profile back to the user** in ~6 short lines, then say: "Rolling POV trend research now — flag anything you want me to recalibrate."

## Stage 2 — POV trend research (you do the legwork)

The agent finds real, current POV/situational trend videos itself — the user never has to hunt down a reference link. Every menu card carries a concrete, openable, current reference-video URL (TikTok or IG Reels); without it the user can't sanity-check the trend before picking, and the receipts gate in Stage 3 can't be enforced.

Search broadly across topics — pre-filtering trends to the user's niche or vibe excludes ~90% of real currently-active templates and leaves you with vibe clusters (which then fail the fingerprint test). Trends are vibe-agnostic templates; the user's voice gets applied later via the caption text in Stage 4. A dry-deadpan AI creator can ride a princess-reveal trend, a Sabrina-Carpenter audio trend, a "what's in my bag" trend — the trend gives the format, the user's caption ("haters will say it's AI") turns it into their post. Cross-reference the trend-vs-voice separation rule.

Run two parallel passes — silent POV / situational only:

1. **Niche-fit POV trends** — `mcp__plugin_pika_pika__scrape_social` against the user's niche:
   - `tiktok / keyword` — `"POV {niche-keyword}"`, `"tell me you're a {niche-role}"`, `"things only {niche-people} do"`, `"when you {niche-action}"`
   - `tiktok / hashtag` — `#POV{nicheTag}`, `#{nicheTag}life`, `#{nicheTag}tok`
   - `instagram / reels-search` — same shapes
   - `WebSearch` only to *discover trend names* (creator-tool blogs: Later / Hootsuite / Opus.pro / Buffer / Dash Social weekly recaps). Translate each named trend into a concrete reference-clip URL via scrape_social.

2. **Broad-viral POV trends** — `mcp__plugin_pika_pika__scrape_social`:
   - `tiktok / trending-feed` with `params.region` (user's geo when known, otherwise `US`) — filter for silent-POV / caption-driven content
   - `tiktok / popular-hashtags` — pull current POV-themed tags (`#POV`, `#fyp`, `#relatable`)
   - `instagram / hashtag` + `reels-search` for the same trends

For every candidate trend, capture: trend name, **exact audio URL/fingerprint**, **≥3 concrete reference-clip URLs from DIFFERENT creators all using the same audio AND same structural template** (highest-engagement versions preferred), example creators, and per-clip duration. Cross-check the 3 clips: do they share the same audio fingerprint? Do they share the same shot count and caption shape? If yes → real trend. If they only share a topic or vibe → drop it, that's a vibe cluster (see the trend fingerprint gate).

For each trend, classify the **scene density**:

| Density | Examples | Filming difficulty |
|---|---|---|
| **Single-shot** | One locked-off shot, mood + caption | Low — phone on tripod, one take |
| **2-3 shot mini-story** | Setup → reaction, or before → after | Low-medium — needs ≤3 framings |
| **4-6 shot listicle** | Each caption gets its own visual beat | Medium — script the shot list tight |
| **POV-with-prop** | Hand/object actions, over-shoulder | Medium — prop continuity matters |
| **Multi-location** | Beats in 2+ rooms or settings | High — flag as a stretch in the menu |

## Stage 3 — Present the POV trend menu (10 trends)

Always 10, mixed general/broad + niche-fit (never all-broad, never all-niche) — the user picks across both. Some weeks they'll ride a universal meme; other weeks they'll want a niche-relevant template; a single-flavor menu strips that agency. See the broad-versus-niche menu rule.

- **4 niche-fit POV trends** (highest relevance to the user's page, lower reach ceiling)
- **4 broad-viral POV trends** (universal templates, lower personal relevance, higher reach ceiling)
- **2 wildcards** (POV archetypes the user doesn't currently use — flagged as stretches)

For each, output **one tight card**:
```
[1] {Trend name / hook}
    Archetype: {POV / Tell-me-without / When-X / etc.}  •  Density: {single-shot / 2-3 / 4-6 / prop / multi-loc}
    Audio: {EXACT sound URL or TT/IG sound name + artist}  •  Reference duration: {Xs}
    The template: {one sentence describing the SAME structure all 3+ replicators follow — e.g. "audio drops at 0:03, creator on couch looks up, deadpan stare, caption appears '___' at the drop"}
    Why it fits you: {1 line}
    ▶ Reference clips (3, all same audio + same template):
       1. {URL of replicator A}
       2. {URL of replicator B}
       3. {URL of replicator C}
    Example creators: {handles}
```

Every card carries 3 working reference-clip URLs from different creators using the same audio + same template — without them you can't verify the trend is fingerprinted (it's the gate against vibe-cluster padding). See the trend fingerprint gate. If you can only find 1-2 clips on a candidate trend, drop it and replace with another that has 3+ verified replicators — padding the menu with sub-threshold cards leaks vibe-cluster trends into production and the resulting video won't ride any algorithmic rail.

Then ask: **"Which one do we make? (pick a number)"**

Hold the full script and shot list until they pick — writing them upfront wastes tokens on trends they may skip.

## Stage 4 — Full production package (per trend chosen)

When the user picks a trend, deliver the full package below in one message, then walk them through filming → editing.

### 4a. Caption + concept options (in their voice, multiple variations)

POV videos have no spoken dialogue — the script IS the captions. Deliver **6-10 caption + visual-concept variations** for the user to pick from. Single-option deliveries leave the user with no creative agency and feel like a take-it-or-leave-it — the variation set is what lets them pick the angle that hits hardest. Each variation pairs one caption (or set of beat captions for multi-beat trends) with a concrete visual concept it would film against. Write all captions in the user's voice from Stage 1:
- Mirror their caption style exactly — if they write lowercase-only with no punctuation, do that. If they use specific emoji, use them. If they have catchphrases or sign-offs, fold them in.
- Match the trend's caption *structure* (e.g. "POV: ..." opening, "tell me you're X without telling me" framing) but the *content* is theirs.
- Total caption length should fit the reference audio's duration with breathing room — overflow gets clipped on mobile (~2 words/sec readable).
- Hook caption (the opening title) lands in the first 1-2 seconds. The audience decides to keep watching in that window — a hook that lands at 2.5s+ has already lost ~30% of viewers.
- See the multi-option script and shot-list contract for the multi-option + filming-breakdown contract every Stage 4 delivery has to honor.

### 4b. Filming breakdown (exact filming directions)

The user needs to know exactly what to shoot, how, and where — vibe descriptions ("show a moody shot in the kitchen") leave them guessing and the resulting footage doesn't cut together. Numbered shots, each filmable on the user's phone with no crew. For each:
- **Shot #** and **duration (s)** — tied to the audio beat structure
- **Camera position** — phone on tripod / leaned against book / handheld / propped on shelf — and HEIGHT (eye level, chest, low angle, top-down)
- **Where to stand / sit** — distance from camera (in feet/cm), orientation (facing lens / 3/4 / side / back-to-camera)
- **Framing** — wide / medium / close / extreme close, what's in frame
- **Action** — exact micro-movement with timing ("look down at phone, then slowly raise eyes to lens at 2.5s")
- **Props in frame** — every prop named and placed
- **Look direction** — at lens / off-camera / down / at prop
- **Lighting** — window light / desk lamp / ring light / overhead; key light position relative to face
- **Wardrobe note** — what to wear (single line, only if it matters for the trend)

Be filmable, not vibey. "Stand 3 feet from kitchen counter, phone leaned against toaster at eye level, hold a coffee mug in your right hand, look at the steam for 2 seconds then deadpan to lens" — not "show coffee morning vibes". Cross-reference the multi-option script and shot-list contract.

### 4c. Caption layout (timed + positioned)

For each on-screen caption, specify:
- **Text** (exact words, exact casing, exact punctuation/emoji)
- **In/out timing** — `t=0.0s → 2.4s`
- **Position** — top safe zone (y ≈ 270-450 for 1080×1920) or bottom safe zone (y ≈ 1350-1475). Default to top for opening title cards, bottom for ongoing narration / payoff beats. Cross-reference the caption safe-zone guidance for the y-position table.
- **Style** — default `reels-clean` bold white text with 4px black outline per the caption safe-zone guidance. Only deviate if the trend has a signature caption style (e.g. monospace typewriter for "tech bro" trends, hand-script for soft/aesthetic trends) — and call it out explicitly.

### 4d. Trending audio (URL + structure)

- The exact audio URL or TikTok search string (the captured menu reference clip's sound).
- Beat structure — where the drop / hook / punchline hits in the audio (e.g. "beat drop at 0:04, dialogue snippet at 0:07-0:09, outro at 0:13"). The shot list must line up with this structure.

### 4e. Filming checklist (handed to the user)

Before the user films, give them a tight pre-shoot checklist:
- Phone in airplane mode + Do Not Disturb (so no notifications kill a take)
- Vertical / portrait orientation locked
- 4K 30fps or 1080p 60fps (slo-mo trends only — flag explicitly)
- Clean lens
- One light source minimum — a window during day, a ring light or desk lamp at night
- Lock exposure before filming (tap-and-hold on the subject in the iOS camera) — prevents auto-exposure pumping mid-shot
- Film each shot 2-3 times — gives the editor cutaways

## Stage 5 — User films and uploads

After delivering the production package, ask the user to film and upload their clips. Wait for the upload.

When the clips arrive:

1. **Finalize manifest** — build `state.clip_manifest[]` in shot-list order with `{clip_id, url, planned_duration_s, beat_label}` for every uploaded clip or manually attached fallback. If the user sends one combined take, use one manifest entry; if they send multiple takes, map each to the matching shot-list beat. If ordering is ambiguous, ask before editing. Do not continue to Stage 6 until every clip has a stable `clip_id` and URL.
2. **Probe each clip** — iterate `state.clip_manifest[]` and call `mcp__plugin_pika_pika__probe_media` on each `url` to confirm orientation (portrait), resolution (≥1080×1920), duration, framerate.
3. **Sanity-check against the shot list** — verify each shot was captured. If a clip is unusable (wrong orientation, blurry, missing the action), call it out and ask for a reshoot of *only that shot* — don't re-shoot the whole sequence.
4. **Fetch the trending audio** — call `mcp__plugin_pika_pika__scrape_social` on the reference clip (`tiktok / video` or `instagram / post`) with `rehost: true`; pass the returned durable video URL to `mcp__plugin_pika_pika__extract_audio_from_video` and save the returned audio URL as `state.audio_track`.

## Stage 6 — Edit pipeline

The edit is mechanical once the clips and audio are in hand:

1. **Trim each clip** to its beat (`mcp__plugin_pika_pika__edit_trim`) — iterate `state.clip_manifest[]` in order, match the duration prescribed in the shot list, and save the returned URL as `trimmed_url` on the same manifest entry.
2. **Normalize each clip to portrait** — call `mcp__plugin_pika_pika__edit_reframe` on each manifest entry's `trimmed_url` with `target_aspect="9:16"` and `fill_mode="crop"` for normal POV shots; use `fill_mode="pad"` only when preserving the full frame matters more than filling the screen. Save the returned URL as `normalized_url` on the same manifest entry. This locks the geometry before concat, audio replacement, and 1080×1920 caption margins.
3. **Concatenate clips in order when needed** — collect manifest `normalized_url` values in order. If there is only one `normalized_url`, skip `mcp__plugin_pika_pika__edit_concat` and set `state.concat_url` to that single normalized URL because the concat tool requires at least two inputs. If there are two or more normalized URLs, call `mcp__plugin_pika_pika__edit_concat` and save the returned URL as `state.concat_url`. Use no transitions unless the trend uses them (most POV trends are hard cuts).
4. **Lock duration, then replace audio with the trending sound** — call `mcp__plugin_pika_pika__probe_media` on `state.concat_url` and `state.audio_track`, saving `state.concat_duration_s` and `state.audio_duration_s`. If `state.concat_duration_s > state.audio_duration_s`, shorten the visual with `mcp__plugin_pika_pika__edit_trim(video_url=state.concat_url, start_s=0, end_s=state.audio_duration_s)` so the video does not run past the usable sound, save that result as `state.visual_locked_url`, and set `state.visual_locked_duration_s=state.audio_duration_s`; otherwise set `state.visual_locked_url=state.concat_url` and `state.visual_locked_duration_s=state.concat_duration_s`. Then call `mcp__plugin_pika_pika__edit_audio_replace(video_url=state.visual_locked_url, audio_url=state.audio_track, duration_policy="video")` at full volume and save the returned URL as `state.audio_locked_url`. Use `duration_policy="video"` only when the audio tail can be trimmed to the already-locked visual. If the hook lands late, adjust upstream clip trims before replacing audio. The trending sound IS the soundtrack; the user's on-set audio gets dropped entirely.
5. **Burn captions with `mcp__plugin_pika_pika__add_captions` as the final media step** — use `caption_mode="manual"` and the timed rows from Stage 4c, adjusted after any trim changes made in steps 1-4. Before each caption pass, cap rows to `state.visual_locked_duration_s`: drop any row whose start timestamp is at or beyond `state.visual_locked_duration_s`, and clamp each remaining row's end timestamp to `state.visual_locked_duration_s`. `add_captions` has one global position per call, so run one pass per caption position layer:
   - **Top opener layer**: when Stage 4c includes a top hook/title, call `mcp__plugin_pika_pika__add_captions(video_url=state.audio_locked_url, caption_mode="manual", subtitles=state.top_caption_rows, style="reels-clean", position="top", margin_v=380, font_color="white", outline_color="black", outline_width=4)`; save the returned URL as `state.latest_captioned_url`. `state.top_caption_rows` must be `[{start_s, end_s, text}]`.
   - **Bottom narrative/payoff layer**: call `mcp__plugin_pika_pika__add_captions(video_url=state.latest_captioned_url, caption_mode="manual", subtitles=state.bottom_caption_rows, style="reels-clean", position="bottom", margin_v=665, font_color="white", outline_color="black", outline_width=4)` after the top pass, or the same call with `video_url=state.audio_locked_url` when there was no top layer; save the returned URL as `state.latest_captioned_url`. `state.bottom_caption_rows` must be `[{start_s, end_s, text}]`.
   - If all captions share one zone, use a single pass for that zone. Do not run any trim/reframe/concat/audio step after captions; if timing changes, rebuild Stage 4c rows and re-run the caption phase.
6. **Final output** — read the returned `url` from the last caption call and save it as `state.final_url`. Keep a version label in agent state (`{user_slug}_{trend_slug}_v{N}`) so the next render never overwrites the previous deliverable.

### Pre-delivery gates

**1. Caption legibility gate** — view the final at actual phone-screen size (zoom out in the preview). Every caption must be readable on first pass. If a caption is too long for its time-on-screen window, split it across two cards. If a caption overlaps the subject's face, move to the other safe zone — see the caption safe-zone guidance.

**2. Audio-sync gate** — does the punchline caption land on the audio's punchline beat? Does the hook caption land before the audio's first hook? If beats don't align, retime captions OR re-trim clips to shift the timing.

**3. Orientation gate** — same as `formats/dance.md`. Verify pixel orientation with `mcp__plugin_pika_pika__probe_media` after the final edit. If the result is not portrait, re-run the relevant MCP reframe/transcode step or request a corrected upload.

**4. Phone-cameo gate** — if any of the user's clips show a phone on screen (very common in POV trends about scrolling / texting / using an app), confirm it's a current-gen iPhone (15 Pro / 16 / Air). If the user filmed with an old or non-iPhone visible, ask them to reshoot or compose so the phone isn't visible. See the phone-cameo gate.

## Stage 7 — Loop

After delivering one POV video, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**.

If they pick another, return to Stage 4 with that trend. Do NOT re-run trend research unless they ask — the Stage-3 menu of 10 stays warm for the session.

## Load-bearing values

Every value below is empirically validated — changing any of them without re-validating against a real render will quietly drift the output off the Instagram-native look that the rest of the skill assumes. If a future maintainer simplifies them, the visible-output regression will not show up in tests (analyze_media doesn't catch subtle stroke / weight drift) — it only shows up when the post lands flat.

| Value | Where | Why it's load-bearing |
|---|---|---|
| `style = reels-clean` | Stage 6 step 4 captions | Closest MCP preset to the validated IG-native bold white text with no pill |
| `font_size ≈ 57` | Stage 6 step 4 captions | Sweet spot at 1080 width. Range 50-72 by readability; outside that, reads off-brand |
| `outline_color = black` + `outline_width = 4` | Stage 6 step 4 captions | 4px black stroke = the IG look. <4px reads as auto-caption; >4px reads too heavy |
| `font_color = white` | Stage 6 step 4 captions | White-on-stroke is the only combination that reads on any background (light kitchen, dark night, mixed gradient) |
| Bottom caption visual y≈1255 | Stage 6 step 4 captions | Top of bottom safe zone. Top placement frequently overlaps the subject's face on the first frame |
| Bottom safe zone: y = 270–1475 | Stage 6 step 4 + Don'ts | Outside this range gets clipped by IG Reels UI (status bar top, like/share buttons bottom) |
| Caption phase after audio replacement | Stage 6 step 4 captions | Keeps caption timing tied to the final audio; use one pass per caption position layer when top and bottom rows both exist |
| Receipts gate: 3+ same-audio same-template replicators | Stage 2 + Stage 3 | The fingerprint test. 1-2 replicators is a vibe cluster, not a trend — the post won't ride any algorithmic rail |

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Stage 2 finds < 10 fingerprinted trends | Niche too narrow OR audio space fragmented | Drop niche-fit count to 2, pad with broad-viral. Tell user explicitly what's underrepresented |
| Candidate trend has only 1-2 same-template replicators | Vibe cluster, not a real trend | Drop the card; replace with one that has 3+. Never pad — see the trend fingerprint gate |
| Clip pixels rotated despite portrait metadata | iPhone orientation flag drift | Re-run the normalization step through `mcp__plugin_pika_pika__edit_transcode` or reframe with the correct aspect before concat |
| Decorative emoji renders inconsistently | Burned-caption font support varies by platform/glyph | Drop emoji from burned caption; user adds in post description |
| `mcp__plugin_pika_pika__analyze_media` reports caption hits y < 270 | Wrong caption position or margin | Re-run the affected caption layer with `position="bottom"`/`margin_v≈665`, or `position="top"`/`margin_v≈380` only when the top zone is intentionally clear |
| `mcp__plugin_pika_pika__analyze_media` reports caption overlaps subject's face | Bottom safe zone collides with the subject in this footage | Try a lower `margin_v`, or split the caption into top-and-bottom beats per the caption safe-zone guidance |
| audio_replace output silent | Apple preview URL expired (short TTL) | Re-search music; grab fresh `preview_m4a_url` and re-run audio_replace |
| Final video duration mismatches audio | Visual duration was not locked before audio replacement | Probe `state.concat_url` and `state.audio_track`; if `state.concat_duration_s > state.audio_duration_s`, trim with `mcp__plugin_pika_pika__edit_trim(video_url=state.concat_url, start_s=0, end_s=state.audio_duration_s)` before `mcp__plugin_pika_pika__edit_audio_replace`. If the audio hook has not landed by video-end, shorten upstream clips so the drop hits inside the locked duration. |
| User's wardrobe changes between shots (continuity break) | Footage filmed across sessions | Hard cuts mask the break in most before/after trends — flag it to the user, ship if they accept, otherwise ask for a re-shoot of the mismatched shot only |
| Phone visible in user's clip is non-iPhone or old iPhone | Filmed without checking the phone-cameo gate | Ask for a re-shoot composing the phone out of frame, OR a re-shoot with a current iPhone (15 Pro / 16 / Air) |

## Don'ts

- **Don't propose talking-head or dance formats.** This playbook is silent-POV / situational only. If the user wants to talk to camera, route to the Content Director front door. If they want dance trends, route to `formats/dance.md`.
- **Don't invent trends.** Every trend in the menu must be backed by either (a) a real scrape result with ≥3 examples or (b) a creator-tool blog citation from the current month. If research comes back empty, tell the user and ask if they want to broaden the search — don't fabricate.
- **Don't strip the user's voice to chase the trend.** Match the trend's *caption structure* (the "POV: X" framing, the "tell me without telling me" shape) but write the captions in the user's actual voice — their casing, punctuation, emoji, catchphrases. The trend is the format and the audio; the voice is theirs.
- **Don't film for the user.** This playbook writes the plan and runs the edit. The user films their own footage. No AI-generated footage for POV trends — the authenticity is the format.
- **Don't write vibey shot lists.** Every shot must be filmable with explicit camera position, distance, framing, action, and look direction. "Vibe shot in kitchen" is useless. "Stand 3 feet from counter, phone leaned against toaster at eye level, hold mug, look at steam then deadpan to lens" is filmable.
- **Don't burn captions outside the IG Reels safe zone.** Always content-aware, always inside y=270 to y=1475 for 1080×1920, with ~80px margin from left/right edges. See the caption safe-zone guidance.
- **Don't chain arbitrary text overlays for captions or edit after captions.** Use `mcp__plugin_pika_pika__add_captions` with `reels-clean`, 4px black outline, and safe-zone placement. If Stage 4c uses both a top opener and bottom narrative/payoff captions, run one caption pass per position layer and keep the caption phase last.
- **Don't put ongoing captions at the very top.** User has flagged that top placement hides the subject's face. Bottom-of-safe-zone (visual y≈1255) is the validated default for ongoing narration/payoff rows. Top placement is only for a short opening hook/title when Stage 4c confirms the subject's face is clear.
- **Don't drop the trending audio.** For POV/situational trends the sound is the trend — the algorithm fingerprint-matches on audio. Substituting a different track (even a similar one) lands the post outside the trend's algorithmic rail and the reach falls off a cliff. Replace on-set audio with the trend's exact sound at full volume.
- **Don't burn the user's on-set audio under the trending sound.** Most POV trends are silent-acted; on-set audio is filler. Replace, don't mix.
- **Don't propose 10 of the same archetype.** Mix POV / tell-me-without / when-X / things-only-X-do / how-it-started-vs / etc. across the 10-card menu so the user has a real choice based on what they can film today.
- **Don't show old phones.** If any user-filmed clip shows a phone, it must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't skip the Stage 3 menu and jump to production.** Always present 10, always wait for a pick. Producing without selection burns the user's budget and the agent's tokens on a video they may not want.
