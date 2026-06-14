---
name: content-director-format-duet
description: >-
  Personal content director for stitch/duet reaction videos: finds a viral,
  proven, recognizable video worth reacting to and writes the creator's response
  in their voice. Ingests an Instagram/TikTok handle, reads their style, and
  surfaces viral originals (each with real play-count proof) that hand them an
  obvious clever take. Uses Pika MCP tools for fetch, probe, edit, mix, and captions.
  Triggers: "be my stitch content director", "find duet trends for me",
  "find a viral video to react to", "make me a stitch video",
  "react to a trending video", "stitch/duet for {handle}", "content-director duet".
argument-hint: "<@handle | instagram/tiktok URL>"
required-capabilities:
  - mcp__plugin_pika_pika__scrape_social
  - mcp__plugin_pika_pika__capture_website
  - mcp__plugin_pika_pika__probe_media
  - mcp__plugin_pika_pika__transcribe_audio
  - mcp__plugin_pika_pika__edit_trim
  - mcp__plugin_pika_pika__edit_reframe
  - mcp__plugin_pika_pika__edit_concat
  - mcp__plugin_pika_pika__edit_split_screen
  - mcp__plugin_pika_pika__edit_audio_mix
  - mcp__plugin_pika_pika__edit_audio_trim
  - mcp__plugin_pika_pika__extract_audio_from_video
  - mcp__plugin_pika_pika__render_html_animation
  - mcp__plugin_pika_pika__add_captions
  - mcp__plugin_pika_pika__create_teleprompter_handoff
  - mcp__plugin_pika_pika__task_status
---

# Content Director — Stitch / Duet (react to a viral video)

A reaction-content director. The core idea is simple: **find a viral, proven, recognizable video → write a clever response in the user's voice → stitch them together so the viral original plays first, then hard-cuts to the user reacting/responding.** The user gives you their IG or TikTok handle; you reverse-engineer their style, surface **up to 10 viral videos worth reacting to** that fit, write the response for the chosen one, and produce the finished mp4. Stitches and native side-by-side duets are delivered as 9:16 via MCP; `edit_split_screen` is only a disclosed fallback when the user accepts the tool's non-native co-equal output shape.

The deliverable per pick is always: **the proven viral original (the agent finds and fetches it) + a response script in the user's voice + filming directions + timed captions + the final composited mp4** — stitch = original first then hard cut to the user; duet = side-by-side simultaneous reaction — with audio handled and captions burned in the IG Reels safe zone. **You find the video and write the response; the user just films their half.**

**Long-running MCP tools:** If any MCP call returns `{task_id, status}` instead of an inline URL/result, immediately call `mcp__plugin_pika_pika__task_status(task_id=<task_id>)` in a tight loop (no Bash, no sleep) until `status` is `completed`, `failed`, or `cancelled`. Continue with the returned `result` only after completion.

This playbook is the reaction-focused sibling of the Content Director front door, `formats/pov.md`, `formats/talking.md`, and `formats/dance.md`. Multi-format menu → `content-director`. Silent POV → `content-director pov`. Plain talking-head with no original to react to → `content-director talking`. **This playbook is specifically for reacting to / responding to an existing viral video.**

## The default format: STITCH (original → cut → response)

The primary, default build is a **stitch**: the viral original plays first (the hook / claim / moment / question — usually ~2–6s, trimmed to the exact beat worth reacting to), then a **hard cut** to the user's full response. This is the structure the user asked for — *first we see the viral video, then cut to the user responding.*

| Layout | Structure | When to use |
|---|---|---|
| **Stitch (default)** | **Sequential** — viral original first, hard cut to the user reacting/responding/answering/flipping it | Almost always — reacting to a take, answering a question, debunking, deadpanning, one-upping, "my version" |
| **Duet (optional)** | **Side-by-side** — original and user play **simultaneously**, split-screen | Only when the reaction must land *in real time against the playing original* (live shock/laugh beat-for-beat, sing/perform-along) |

Default to **stitch** unless the reaction genuinely needs the original playing at the same time. Both are produced by **compositing** the user's footage with the original through MCP edit tools — see Stage 6 for the exact recipes.

## The native-feature reality (read this, and tell the user)

TikTok has in-app **Duet** and **Stitch** buttons. Using them gives the original creator an attribution link and taps the post into TikTok's native stitch/duet discovery rails. We **cannot** trigger those in-app buttons programmatically, and the original creator must have stitch/duet *enabled* for their video.

So this playbook produces a **composited mp4** — the user's clip and the original combined into one file, formatted to look exactly like a native stitch/duet. This is:
- **The only path on Instagram Reels** (IG has no native stitch/duet — a composited file is how every IG creator does this format).
- **A valid path on TikTok**, uploaded as a normal post. It loses the native attribution badge but works when the original has duet/stitch disabled, and lets you control the exact crop, timing, and captions.

**Tell the user once, plainly:** "I'll build you a finished stitch/duet file you can post anywhere. On TikTok specifically, if the original allows it, using TikTok's in-app Stitch/Duet button on your pre-filmed clip gives you the native attribution link — but my composited file is what works on Reels and gives you full control over the cut and captions." Don't belabor it; build the file either way (it's the deliverable they asked for). This mirrors the honest audio-attachment note in `formats/dance.md`.

## What counts as a TREND here (read this before research — this is the whole game)

**The "trend" in this playbook is a VIRAL, PROVEN, RECOGNIZABLE video that's worth reacting to — the proof lives on the ORIGINAL video, not on a wave of identical copies.** The format is always: **the viral original plays first → hard cut → the user responds** (talking about it, reacting to it, answering it, flipping it) in a funny / clever / interesting way that's true to their voice. You find the proven viral video; you write the response.

This is the key distinction from the other content-director skills: a *dance* or *sound* trend is a fingerprinted template that 10+ people copy identically. A *stitch/duet reaction* is the opposite — **everyone reacts to the SAME viral original in their OWN different way.** So do NOT require a replicated template here. The thing that must be proven is that **the original video is genuinely viral and recognizable.** The response is bespoke (you write it).

**The original video MUST pass ALL of these (this is the trend proof):**

1. **VIRAL — hard numbers on the ORIGINAL.** The source video has real, provable reach: **≥500K plays** (ideally millions). This is non-negotiable — the whole point of a stitch/duet is to borrow a video the algorithm and the audience already know. A low-view clip = nothing to borrow. Capture the actual play count as proof.
2. **RECOGNIZABLE — people online know it.** A chronically-online viewer sees the first 2 seconds and goes "oh, THAT video." It has a name, a known creator, a meme'd moment, or a quotable line. If you can't say what it is in one sentence, it's not it.
3. **CURRENTLY CIRCULATING — recent / still alive.** The original is going off **right now** (last ~30–60 days) OR is in an active resurgence people are reacting to this week. Don't pitch a video whose moment passed months ago.
4. **REACTION-WORTHY — there's an obvious take.** The video gives the user something to push against, agree with, escalate, debunk, deadpan at, or one-up. If there's no clever response to be had, it's not a candidate.
5. **REACTION-PROVEN (strong signal, not strictly required).** Bonus confirmation that people are ALREADY stitching/dueting/reacting to it — `#stitch`/`#duet`/`#reply` versions exist with traction. This proves it's a reaction magnet, not just a video that happens to be popular. Note it when present; a freshly-exploding original with an obvious take can still qualify on #1–4 even before the reaction wave forms.

**Trend proof on every menu card = the original's play count + its name/what-it-is + a tappable URL + recency.** No proof → not on the menu. Never pitch a low-view clip, and never substitute a blog mention for the real view count.

**What ISN'T a candidate (do not surface these):**
- A low-view video, no matter how funny — there's nothing for the algorithm or audience to recognize. Virality of the original is the entire premise.
- A vague topic or vibe ("react to AI drama") with no specific, nameable, viral source video attached.
- A stale viral moment whose wave passed months ago with no current resurgence.
- Something you invented — the original must actually exist and actually be viral, with the play count to prove it.

**If fewer than 10 reaction-worthy viral originals clear the bar, deliver fewer cards and say so — never pad the menu with low-view clips.** Cross-reference the trend fingerprint gate and the virality receipts gate (those govern fingerprinted *template* trends — this playbook borrows their virality/recognizability bar but applies it to the ORIGINAL video being reacted to, not to a replication wave).

## What counts as a stitch/duet trend (the archetypes)

Beyond the trend gate, this playbook only surfaces trends where the user's footage pairs with an existing clip:

| Archetype | Layout | Template shape |
|---|---|---|
| **React-to-take** | Stitch | Original drops a hot take/claim (2–4s) → cut to user agreeing/disagreeing/escalating |
| **Answer-the-question** | Stitch | Original asks "stitch this with ___" → user answers |
| **Finish-the-sentence** | Stitch | Original sets up "the craziest thing that ever happened to me was…" → user's story |
| **Bait-and-correct** | Stitch | Original states something wrong/incomplete → user corrects with authority |
| **My-version** | Stitch | Original shows a process/result → user does their own take of the same thing |
| **Real-time-reaction duet** | Duet | Original plays; user reacts on camera beat-for-beat (shock, laugh, deadpan) |
| **Sing/perform-along duet** | Duet | Original is a song/sound; user harmonizes, dances, or mirrors |
| **Versus / side-by-side** | Duet | Original vs user — same prompt, two outcomes, comedic contrast |
| **Co-sign / amplify duet** | Duet | Original makes a point; user nods/gestures agreement, captions add commentary |

For tech/AI niches, **stitch architecture is the strongest hook** — cold-open on the original's claim, hard cut to the user's reaction. Cross-reference the stitch hook guidance. If a trend doesn't fit an archetype, force it into the closest one.

## Stage 0 — Discovery

Ask in a single message:

1. **Instagram or TikTok handle** (required). One is enough; both is better. Accept `@name`, `name`, or full URL.
2. **What do you want this content for?** (free text — "grow my brand", "personal account", "promote my SaaS", "just for fun") — biases the niche-vs-broad-viral mix.
3. **Comfort on camera?** (face + voice / face but silent / faceless) — gates archetypes. Faceless excludes real-time-reaction duets where the face is the punchline; "silent" routes to reaction-by-expression + caption commentary rather than spoken responses.
4. **Filming constraints?** (e.g. "only at home", "no props", "desk setup only") — optional, biases feasibility.

Do NOT ask: trend count (default 10), niche (derive from scrape), aesthetic (derive from scrape), stitch-vs-duet preference (the trend dictates the layout).

## Stage 1 — Personality / niche analysis (auto, no extra prompts)

Once you have the handle, scrape immediately — the handle IS consent.

1. **Scrape the profile** — `mcp__plugin_pika_pika__scrape_social` on the handle. Prefer `digest: true` with `digest_top_n: 12` for the first profile read so large `user-posts` payloads do not flood the context; fetch raw posts only for specific media URLs you need to verify. Pull the most recent 12–20 posts only when the compact result is not enough. Capture: captions, hashtags, post types (reel / carousel / static), recurring locations, recurring people, view counts, music choices, whether they already stitch/duet anything.

2. **Fallback if scrape_social returns empty / rate-limited** — `mcp__plugin_pika_pika__capture_website` on `https://www.tiktok.com/@{handle}` or `https://www.instagram.com/{handle}/` for at least the bio + grid screenshot. Tell the user the analysis is grid-only.

3. **Identity-confirmation gate before profiling** — confirm the scrape or screenshot is the intended creator before you synthesize the profile. Cross-check display name, verified badge, follower count, bio, platform, and whether recent posts match the user's expected creator. Try common handle variants first: with/without dots, dotless, underscores removed, and cross-platform Instagram / TikTok / YouTube checks. Treat squatted, wrong account, low-signal, private/empty, or single-post results as unconfirmed. If the default scrape returns only one stale post but the bio/follower/name signal suggests the account may be real, try `user-reels`/`user-posts` with digest and the common variants before calling the account dead. When unconfirmed, stop and ask **"Is this you?"** with the evidence you saw (`N followers`, verified badge status, display name, bio snippet, platform URL, recent-post summary) and offer the likely variant; do not synthesize the Creator Profile before identity is confirmed. When identity is confirmed, set `state.identity_confirmed = true`.

4. **Synthesize a Creator Profile** (internal, then summarized for the user):
   - **Niche** — primary topic cluster
   - **Voice & tone** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Aesthetic** — color palette, lighting, framing, indoor vs outdoor, selfie vs third-person
   - **Caption style** — short clipped vs long rambly; lowercase-only? emoji-heavy? all-caps for emphasis? — copy this EXACTLY for on-screen captions
   - **Reaction style** — how do they emote/argue/joke in their existing posts? (deadpan stare, big laugh, rapid-fire rant, slow build) — this drives the reaction script
   - **Recurring motifs** — repeating props, locations, catchphrases, sign-offs
   - **What works for them** — flag the 2-3 posts with disproportionate engagement
   - **Filming environment baseline** — what spaces appear in their grid

5. **Present the Creator Profile back to the user** in ~6 short lines, then say: "Rolling stitch/duet trend research now — flag anything you want me to recalibrate."

## Stage 2 — Find viral videos worth reacting to (you do the legwork)

**The agent finds the proven viral originals AND fetches them itself — the user never hunts down a link.** For every card on the Stage-3 menu you MUST have already captured a concrete, openable, currently-circulating original-video URL **with its real play count**.

**The hunt is for VIRAL ORIGINALS, not for a replicated template.** You're looking for videos that are blowing up / widely recognized right now and that hand the user an obvious clever response. Two complementary angles — run both:

1. **Reaction magnets (strongest).** Videos people are *already* stitching/dueting — proof they're reaction-bait.
   - `mcp__plugin_pika_pika__scrape_social` `tiktok / keyword` — `"stitch this"`, `"duet this"`, `"reply"`, `"react to this"`, plus the user's niche words (`"AI video"`, `"AI art"`, `"is this AI"` for an AI creator)
   - `tiktok / hashtag` — `#stitch`, `#duet`, `#greenscreen`, `#react`, niche tags
   - When you find a stitch/duet getting traction, **trace it back to the ORIGINAL it reacts to** and verify the original's play count.

2. **Viral originals + current moments.** The big videos/claims/clips of the moment that beg for a take.
   - `tiktok / trending-feed` with `params.region` (user's target posting region when known, otherwise `US`) and `tiktok / popular-hashtags` — pull the genuinely high-play videos. Show the region used on the menu; if the user says another region, re-run the trend scrape for that region before they pick.
   - `WebSearch` for this week's viral videos / viral moments / controversial clips / "everyone is talking about" — then **verify each on-platform for the real view count** (a blog mention is a lead, never proof)
   - `instagram / reels-search` + `instagram / hashtag` for the same

**Bias toward originals with an obvious angle for THIS user.** A dry-deadpan AI creator gets the most mileage reacting to: AI-skeptic takes ("AI will never make real art"), "is this real or AI" guessing clips, viral fashion/tech hot-takes, absurd internet moments she can deadpan at. The original is vibe-agnostic — the user's *response* is where their voice goes (cross-reference the trend-vs-voice separation rule).

For every candidate, capture:
- **What it is** — one line, the recognizable handle ("the guy who says AI art has no soul", "the $7 coffee rant")
- **The original video** — direct TikTok/IG URL, **with its real play count** (≥500K; millions ideal)
- **The exact beat to stitch** — which seconds of the original to show before the cut (the claim / the question / the punchline-setup), e.g. "show 0:00–0:05 where he says '___'"
- **The response angle** — the one-line take the user fires back (this becomes the script in Stage 4)
- **Recency** — confirm the original is circulating now (posted/resurging in ~last 30–60 days)
- **Reaction-proof (if any)** — note existing stitch/duet versions + their traction; it's a strong plus, not a hard requirement

**Gate each candidate against "What counts as a TREND here":** is the ORIGINAL genuinely viral (≥500K, real number in hand)? recognizable? circulating now? is there an obvious clever response? If yes → it's a card. If the original is low-view, or there's no real take to be had, or you can't name it in a sentence → **drop it.** If you run out of qualifying originals, deliver fewer than 10 and say so — never pad with low-view clips.

For each card, classify the **response density**:

| Density | Examples | Filming difficulty |
|---|---|---|
| **Single-shot reaction** | One locked-off take responding to camera | Low — phone on tripod, one take |
| **2-3 shot mini-response** | Setup → reveal, or claim → demo | Low-medium |
| **Talking response** | User speaks a scripted reply (transcribe for captions) | Medium |
| **Show-and-tell / prop** | User shows or makes something to answer the original | Medium — prop + framing continuity |
| **Real-time duet** | User reacts beat-for-beat against the playing original (use duet layout) | Medium — timing to the original matters |

## Stage 3 — Present the menu (up to 10 viral videos to react to)

Aim for 10, but **only as many as genuinely clear the viral bar** — a short honest menu beats a padded one. **Mix broad + niche. Never all-broad, never all-niche.** Cross-reference the broad-versus-niche menu rule.

- **~4 niche-fit originals** (in/around the user's world — AI, art, fashion, internet culture — that still clear the view bar)
- **~4 broad-viral originals** (universally recognized moments/clips — bigger reach ceiling)
- **~2 wildcards** (an unexpected viral original with a surprisingly good angle for them)

Each card is built around ONE viral original to react to — the proof (the original's play count) is visible right on the card, and you preview the response you'd write:
```
[1] {What the original is — the recognizable handle, e.g. "AI bro: 'real artists will never use AI'"}
    🔥 Viral proof: {original's play count, e.g. "4.1M plays"}  •  posted/resurging {recency}  •  {"+ N stitch/duet reactions already" if reaction-proven}
    ▶ Original video: {direct tappable TikTok/IG URL}
    Show this beat: {which seconds to play before the cut — e.g. "0:00–0:05, the 'no soul' line"}
    Your response (the angle): {one-line preview of the take you'll script in their voice — e.g. "cut to you, deadpan: 'made this in 4 seconds. anyway' + reveal"}
    Layout: {Stitch (default) / Duet}  •  Response density: {single / 2-3 / talking / show-and-tell / real-time}
    Requirements before picking: {none OR required prop/disclosure/source constraint/portrait filming note, stated plainly}
    Why it's a fit: {1 line — why this original + this angle lands for them}
```

**Every card MUST show: what the original is, its real play count (≥500K), a working URL, and the beat to stitch.** The proof is the ORIGINAL's virality — no play count, no card. Mix **broad-viral** (universally recognized originals) with **niche-fit** (originals in/around the user's world that still clear the view bar). If fewer than 10 reaction-worthy viral originals clear the bar, **deliver fewer and say "only N viral originals clear the bar right now"** — never pad with low-view clips. Cross-reference the trend fingerprint gate, the virality receipts gate.

Then ask: **"Which one do we make? (pick a number)"**

Do NOT write the full script or fetch/probe the original yet — wait for the pick. Saves work if they want something else.

## Stage 4 — Full production package (per trend chosen)

When the user picks a trend, deliver the package below in one message, then walk them through filming → compositing.

### 4a. Reaction / continuation script + concept options (in their voice, MULTIPLE variations)

Deliver **6-10 response variations** for the user to pick from — never just one. Each variation pairs one reaction/continuation script (what the user says or does) with the concrete visual concept it films against. Write all in the user's voice from Stage 1:
- Mirror their voice, cadence, and reaction style EXACTLY — if they're deadpan, the response is deadpan; if they rant, it rants. Use their catchphrases / sign-offs.
- Match the trend's *structure* (the stitch sets up, the user pays off; the duet reaction lands on the original's beat) but the *content* is theirs.
- For **stitches**: the user's response must make sense *cutting from* the original's segment. Write the response to land its hook in the first 1-2 seconds after the cut — that's where retention is decided.
- For **talking responses**: keep spoken length to the trend's response length (most 8–20s). Give a one-line delivery direction ("first sentence fast, then drop tempo").
- For **performance duets**: note the beat the user mirrors/hits relative to the original's timeline.
- Cross-reference the multi-option script and shot-list contract — multi-option scripts + explicit filming breakdown are MANDATORY for every Stage 4 delivery.

Save the chosen reaction script as `state.script_text` once the user picks a variation. Keep any broader concept metadata separately; the teleprompter URL reads `state.script_text` directly.

### 4b. Filming breakdown — MANDATORY (exact filming directions)

The user MUST know exactly what to shoot. Non-negotiable for every Stage 4 delivery. Numbered shots, each filmable on the user's phone with no crew. For each:
- **Shot #** and **duration (s)** — for duets, this must match the original's length (they play simultaneously); for stitches, the user's clip can run as long as the response needs.
- **Camera position** — tripod / leaned / handheld — and HEIGHT (eye level, chest, low angle).
- **Where to stand / sit** — distance from camera (feet/cm), orientation (facing lens / 3⁄4 / side).
- **Framing** — and for **duets, frame for the split**: the user occupies one panel, so shoot with the subject biased toward the *inner* edge (toward the original) and leave headroom — a tight-but-not-cramped medium/close works best in a split panel. Tell them which side they'll be on (see Stage 6 for the convention).
- **Action / performance** — exact micro-movement with timing ("at the cut, look dead into lens, hold 1s, then 'absolutely not'"). For duets, tie reactions to the original's beats ("laugh when the original says 'and then it deployed itself'").
- **Props in frame** — every prop named and placed.
- **Look direction** — at lens / off-camera / at the original (for duets, many creators glance toward the original's side as if watching it).
- **Lighting** — window / desk lamp / ring light; key position relative to face.
- **Wardrobe note** — one line, only if it matters.

Be filmable, not vibey. Cross-reference the multi-option script and shot-list contract.

### 4c. Caption layout (timed + positioned)

For each on-screen caption, specify:
- **Text** (exact words, casing, punctuation/emoji — the user's style).
- **In/out timing** — `t=0.0s → 2.4s`, tied to the stitch cut or the duet beats.
- **Position** — bottom safe zone (y ≈ 1255 for 1080×1920 stitch output) by default. **For duets**, captions go in the bottom safe zone of the final split-screen output, centered across the composite and clear of the vertical split. Do not assume a fixed x-coordinate; verify the output dimensions with `mcp__plugin_pika_pika__probe_media` before captioning. Cross-reference the caption safe-zone guidance for the placement table.
- **Style** — `reels-clean`, bold white text, 4px black outline per the caption safe-zone guidance. Deviate only if the trend has a signature caption style (call it out).

### 4d. The original clip + audio plan

- Restate the **original-clip URL** (from the menu card) so the user can sanity-check.
- **Stitch point** (for stitches) — the exact original segment used (e.g. "0:00–0:03"). Save it as `state.original_segment_start_s` and `state.original_segment_end_s`; every stitch trim, caption offset, and optional post-hook bed slice must use those same bounds.
- **Audio plan** — state which audio survives in the final cut:
  - **Stitch**: original segment keeps its own audio; hard-cut to the user's clip with the user's own audio. (Sequential — no mixing needed unless a continued bed is wanted.)
  - **Reaction duet**: original audio ducked to ~−10 dB; user's voice/audio at 0 dB on top.
  - **Performance / sing-along duet**: original audio full (it's the trending sound); user's mic off or low — the user performs to it.

### 4e. Filming checklist (handed to the user)

- Phone in airplane mode + Do Not Disturb.
- Vertical / portrait orientation locked.
- 1080p 60fps (or 4K 30fps).
- Clean lens; lock exposure (tap-and-hold) before filming.
- **For duets — play the original on a second device while filming** so reactions/performance land on the right beats. (You'll still composite from the clean source, but performing to it gets the timing right.)
- **For duets — match the original's length** (film a take at least as long as the original).
- Film each shot 2-3 times for cutaways.

### 4f. Teleprompter handoff (hand the reaction script to the user's phone)

Once the user **picks a reaction script variant** from Stage 4a and approves it — hand them the canonical Pika teleprompter via `formats/teleprompter.md` so they can record their half with the script scrolling on their phone (under the lens, per-line pacing, 3-2-1 countdown, Upload when done).

**For STITCH:** the script being prompted is the user's response *after* the hard cut from the original. Length should at minimum match what they need to say; aim for the same total length as the original they're reacting to.

**For DUET (side-by-side):** the script is the live reaction running ALONGSIDE the original. They should play the original on a second device for timing, and the teleprompter scrolls their commentary in sync.

**Create the handoff** through MCP. Do not build a long URL yourself:

```python
handoff = mcp__plugin_pika_pika__create_teleprompter_handoff(
    script=state.script_text,            # the chosen reaction script variant
    handle=state.handle.lstrip("@"),
    trend=state.pick.name,               # e.g. "@calvin.james41 — everything is AI"
    format="duet",
    aspect_ratio=getattr(state, "recording_aspect_ratio", "9:16"),
    filename=f"{state.handle.lstrip('@')}-duet-take.webm",
    mime_type="video/webm",          # preferred; upload-return accepts browser mp4/webm variants
    max_size_bytes=350_000_000,
    expires_in_s=86400,
)
state.teleprompter_url = handoff["teleprompter_url"]
state.teleprompter_qr_image_url = handoff["qr_image_url"]
state.teleprompter_status_url = handoff["status_url"]
state.teleprompter_aspect_ratio = handoff["aspect_ratio"]
url = state.teleprompter_url
```

**Do NOT pass raw presigned media URLs** into the teleprompter. Use `create_teleprompter_handoff` only: it creates the browser-safe upload-return session behind the token, gives the agent a `status_url`, mints the CDN presign only after the user starts uploading, and avoids TTL failures from recording sessions that take more than a few minutes. The hosted page fetches `script`, `upload_url`, and `aspect_ratio` from MCP, POSTs `{mime_type,size_bytes}` to `upload_url`, receives `direct_upload_url`, `attempt_id`, and `complete_url`, PUTs the Blob to the CDN URL, then completes by POSTing `attempt_id` to `complete_url`. Keep `status_url` in agent state only; do not put it in the browser URL.

**Emit the URL and returned QR image URL** (canonical handoff — see `formats/teleprompter.md`):

```python
qr_image_url = state.teleprompter_qr_image_url
qr_block = f"![Scan QR]({qr_image_url})"
```

**Caption to surface to the user** (verbatim, swap the original's reference):

> 📱 **Film your reaction on your phone.** Scan the QR image or open the link below. Your reaction script is already loaded, with the read zone at the top right under the camera lens. Play the original on a second device for timing.
>
> {qr_block}
>
> 🔗 Or open here: {url}
>
> When the take is ready, hit **Upload**. I'll watch the upload status and compose the stitch/duet as soon as it lands. If upload fails, use Share/Save and send the MP4 back here.

Do not generate a local QR PNG and do not call a third-party QR service; use the `qr_image_url`
returned by `create_teleprompter_handoff`.

After this — poll `state.teleprompter_status_url` until it returns `status="uploaded"` with `public_url`, then save `public_url` as both `state.user_take_url` and `state.user_clip_url`. `state.user_clip_url` is the field Stage 5 probes and Stage 6 trims/reframes, so do not leave it unset after a successful teleprompter upload. If upload fails and the user sends a manual attachment, Stage 5's "Receive + sanity-check the user's footage" begins when the file lands.

## Stage 5 — Acquire the original + receive the user's footage

This playbook needs **two** video inputs: the original clip (agent fetches) and the user's response (user uploads).

### Fetch the original clip yourself (don't make the user supply it)

- For TikTok/IG public URLs — call `mcp__plugin_pika_pika__scrape_social` (`tiktok / video` or `instagram / post`) with `rehost: true`; save the returned durable video URL as `state.original_video_url` and use that URL directly in the edit tools.
- If scrape returns no media URL (private / age-gated / region-locked), tell the user and ask them to upload a local copy of the original.
- **Probe the original** — `mcp__plugin_pika_pika__probe_media`: capture exact duration, resolution, aspect ratio, fps. For stitches, confirm the stitch-point segment exists. For duets, this duration is the target length for the user's clip.

### Receive + sanity-check the user's footage

When the user's clip arrives:
1. **Probe** — save the uploaded clip URL as `state.user_clip_url`, then call `mcp__plugin_pika_pika__probe_media`: confirm portrait orientation, ≥1080×1920, duration, fps. The teleprompter should upload a 9:16 take even when the raw camera stream is 16:9; if the clip is still landscape, ask for a phone/portrait reshoot unless the user explicitly accepts a center-crop rescue.
2. **Sanity-check against the shot list** — was the response captured? For duets, is it ≥ the original's length? If a clip is unusable (wrong orientation, blurry, missing the reaction, too short for a duet), call it out and ask for a reshoot of *only that shot*.
3. **Phone-cameo gate** — if the user's clip shows a phone (common in reaction content), confirm it's a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

## Stage 6 — Compose the stitch / duet + edit

The composite is mechanical once both clips are in hand. Use MCP edit tools for trimming, reframing, layout, audio balance, and caption burn.

### 6a. STITCH composite (sequential)

1. **Trim the original to the stitch segment** with `mcp__plugin_pika_pika__edit_trim(video_url=state.original_video_url, start_s=state.original_segment_start_s, end_s=state.original_segment_end_s)`, then save the returned URL as `state.original_segment_url` and set `state.original_segment_duration_s = state.original_segment_end_s - state.original_segment_start_s`. Do not use a separate hard-coded hook range here; the stitch video, caption offsets, and optional bed continuation must all share the exact Stage 4d bounds.
2. **Normalize both stitch inputs to 9:16** — call `mcp__plugin_pika_pika__edit_reframe(video_url=state.original_segment_url, target_aspect="9:16", fill_mode="crop")` and save the returned URL as `state.original_segment_normalized_url`; call `mcp__plugin_pika_pika__edit_reframe(video_url=state.user_clip_url, target_aspect="9:16", fill_mode="crop")` and save the returned URL as `state.user_response_normalized_url`. Use `fill_mode="pad"` only when preserving the full source frame matters more than filling the screen.
3. **Concat original segment → user response** with `mcp__plugin_pika_pika__edit_concat(video_urls=[state.original_segment_normalized_url, state.user_response_normalized_url])`, save the returned URL as `state.stitch_concat_url`, and set `state.caption_input_url=state.stitch_concat_url` unless optional bed continuation replaces it. Each segment keeps its own audio: the original hook first, then the user's response.
4. **Optional bed continuation** — only if the original's sound should continue under the response. First call `mcp__plugin_pika_pika__extract_audio_from_video` on `state.original_video_url`, then use the probed original duration as `state.original_audio_duration_s`. Reuse the already-set `state.original_segment_start_s`, `state.original_segment_end_s`, and `state.original_segment_duration_s` from the stitch trim step. Call `mcp__plugin_pika_pika__edit_audio_trim(audio_url=<original_audio_url>, start_s=state.original_segment_end_s, end_s=<original_audio_duration_s>)` to create `state.post_hook_bed_audio_url`; `end_s` is required by the tool schema, so do not omit it. Mix that trimmed bed onto the concat with `mcp__plugin_pika_pika__edit_audio_mix(video_url=state.stitch_concat_url, audio_url=state.post_hook_bed_audio_url, original_gain_db=0, audio_gain_db=-15, audio_offset_s=state.original_segment_duration_s)`, then save the returned URL as `state.stitch_mixed_url` and set `state.caption_input_url=state.stitch_mixed_url`. Use -15 dB as the default bed level; adjust within -12 to -18 dB only by passing a single concrete number. Both steps are load-bearing: trimming starts after the exact original segment end in the full source, and the positive offset delays the post-hook bed until the user's response starts in the stitched concat. If `edit_audio_trim` fails, skip the bed, keep the clean stitch, and set `state.caption_input_url=state.stitch_concat_url` rather than replaying the hook.

### 6b. DUET composite (side-by-side, simultaneous)

**Convention:** original on the **right**, user on the **left** (TikTok's duet layout puts your new camera on the left). State this to the user; it's a one-line swap if they want it flipped.

1. **Match lengths** — both halves play together. Use the Stage 5 probes to set `state.original_duration_s` and `state.user_clip_duration_s`, then set `state.matched_duration_s=state.original_duration_s` unless the user explicitly approved a shorter original segment. If `state.user_clip_duration_s < state.matched_duration_s`, ask for a longer take instead of freezing a panel. Trim both sources with explicit URLs: call `mcp__plugin_pika_pika__edit_trim(video_url=state.original_video_url, start_s=0, end_s=state.matched_duration_s)` and save the returned URL as `state.original_duet_trimmed_url`; call `mcp__plugin_pika_pika__edit_trim(video_url=state.user_clip_url, start_s=0, end_s=state.matched_duration_s)` and save the returned URL as `state.user_duet_trimmed_url`.
2. **Probe and pre-normalize inputs** — call `mcp__plugin_pika_pika__probe_media` on `state.user_duet_trimmed_url` and `state.original_duet_trimmed_url`, then reframe only when a source is not already clean portrait: call `mcp__plugin_pika_pika__edit_reframe(video_url=state.user_duet_trimmed_url, target_aspect="9:16", fill_mode="crop")` for the user panel and `mcp__plugin_pika_pika__edit_reframe(video_url=state.original_duet_trimmed_url, target_aspect="9:16", fill_mode="crop")` for the original panel. Save the exact panel-source URLs as `state.user_panel_url` and `state.original_panel_url`: use the reframe result when reframe ran, otherwise use the corresponding trimmed URL. These same panel-source URLs must be used for both `state.duet_html` and the later audio extraction so the rendered panels and mixed tracks come from the same timeline.
3. **Render the native 9:16 side-by-side visual** — author `state.duet_html` as a HyperFrames HTML document and call `mcp__plugin_pika_pika__render_html_animation(html=state.duet_html, format="mp4", fps=30, quality="standard")`. The root composition must be `data-composition-id="content-director-duet"`, `data-width="1080"`, `data-height="1920"`, and `data-duration="<matched_duration_s>"`. Put the user's video in a left panel at `x=0,width=540,height=1920` and the original in a right panel at `x=540,width=540,height=1920`, with each video using cover-crop/object-fit semantics so neither panel stretches. Include a timed `class="clip"` composition child with `data-start="0"`, `data-duration="<matched_duration_s>"`, and stable `data-track-index`, plus a real `window.__hf.seek(t)` implementation that seeks both video elements before the renderer captures the frame. Minimal template:
   ```html
   <div data-composition-id="content-director-duet" data-width="1080" data-height="1920" data-duration="<matched_duration_s>">
     <div class="clip" data-start="0" data-duration="<matched_duration_s>" data-track-index="0">
       <video id="user-panel" src="<state.user_panel_url>" muted playsinline preload="auto" style="position:absolute;left:0;top:0;width:540px;height:1920px;object-fit:cover;"></video>
       <video id="original-panel" src="<state.original_panel_url>" muted playsinline preload="auto" style="position:absolute;left:540px;top:0;width:540px;height:1920px;object-fit:cover;"></video>
     </div>
   </div>
   <script>
   const duration = Number("<matched_duration_s>");
   const videos = Array.from(document.querySelectorAll("video"));
   const ready = Promise.all(videos.map((video) => new Promise((resolve) => {
     if (video.readyState >= 2) return resolve();
     video.addEventListener("loadeddata", resolve, { once: true });
   })));
   async function seek(t) {
     await ready;
     const target = Math.max(0, Math.min(Number(t), duration));
     await Promise.all(videos.map((video) => new Promise((resolve) => {
       video.pause();
       if (Math.abs(video.currentTime - target) < 0.001 && video.readyState >= 2) return resolve();
       video.addEventListener("seeked", resolve, { once: true });
       video.currentTime = target;
     })));
   }
   window.__hf = { duration, ready, seek };
   </script>
   ```
   Save the returned URL as `state.duet_visual_url`.
4. **Add the duet audio with `mcp__plugin_pika_pika__edit_audio_mix`** — extract audio from `state.user_panel_url` and `state.original_panel_url` with `mcp__plugin_pika_pika__extract_audio_from_video`, then mix tracks onto `state.duet_visual_url` with `original_gain_db=-60` so any audio captured by the HTML render cannot double the extracted mix. Save the returned URL as `state.duet_mixed_url` and set `state.caption_input_url=state.duet_mixed_url`:
   - **Reaction duet:** `tracks=[{url: user_audio_url, gain_db: 0}, {url: original_audio_url, gain_db: -10}]`.
   - **Performance / sing-along duet:** `tracks=[{url: original_audio_url, gain_db: 0}]`, adding `{url: user_audio_url, gain_db: -18}` only if the user's mic should remain faintly audible.
   - **No dialogue / silent reaction:** use the original audio track unless the user's on-set sound is explicitly part of the bit.

MCP caveat: `mcp__plugin_pika_pika__edit_split_screen` is not the native duet production path because horizontal split-screen is a co-equal stacked output shape rather than a guaranteed 1080×1920 half-canvas render. Use it only if the user explicitly accepts that fallback, and always probe/disclose the returned dimensions. Do not crop a finished split-screen just to force 9:16; that can cut off one panel.

### 6c. Burn captions with `mcp__plugin_pika_pika__add_captions`

Use `mcp__plugin_pika_pika__add_captions` on `state.caption_input_url` from 6a/6b, never on the pre-audio visual render or pre-mix stitch concat.

- **If the user speaks a scripted response** (talking stitch / reaction with dialogue): transcribe the same user timeline that will appear in the final composite. For stitches, transcribe `state.user_response_normalized_url`; offset those caption rows by `state.original_segment_duration_s` so timings line up after the original hook. For side-by-side duets, transcribe `state.user_panel_url` or `state.user_duet_trimmed_url`, never the longer raw upload; drop any row whose start timestamp is at or beyond `state.matched_duration_s`, and clamp each remaining row's end timestamp to `state.matched_duration_s`. Build `state.caption_rows` as `[{start_s, end_s, text}]` segment/phrase rows, then call `mcp__plugin_pika_pika__add_captions(video_url=state.caption_input_url, caption_mode="manual", subtitles=state.caption_rows, style="reels-clean", position="bottom", margin_v=665, font_color="white", outline_color="black", outline_width=4)`.
- **If the response is silent** (expression-only reaction, performance): pass the title-card caption rows from the 4c layout in manual mode.

After the final caption pass, read the returned `url` and save it as `state.final_url`. Do not return `state.duet_visual_url`, the pre-caption audio mix, or any intermediate stitch concat as the deliverable.

**Caption params (validated):**
- `style="reels-clean"`
- `font_size≈57` (default; 50-72 per readability)
- `font_color="white"`, `outline_color="black"`, `outline_width=4`
- `position="bottom"`, `margin_v≈665` for the bottom safe-zone default
- For duets, keep captions centered across the final composite so they clear the vertical split; use `mcp__plugin_pika_pika__probe_media` after `render_html_animation` before picking margins.
- Keep caption rows short enough to render without clipping. Split long rows manually before `add_captions`; do not rely on automatic wrapping for long one-line punchlines.

**IG Reels safe zone (1080×1920 stitch/native duet output):** top unsafe y≈0-270, bottom unsafe y≈1480-1920. Captions sit inside y≈270-1475, ~80px margin from left/right edges. Default bottom visual placement is near y≈1255. For explicitly accepted `edit_split_screen` fallback output, scale the same safe-zone intent to the probed output height. **Emoji warning:** decorative emoji can render inconsistently in burned captions; put emoji in the post description at upload.

### Pre-delivery gates

**1. Composite-integrity gate** — open the final. For stitches: the cut is clean, the original segment is the right hook, audio doesn't clip at the join. For duets: the split is even inside the 1080×1920 render, neither panel is stretched, both play in sync, output dimensions match `mcp__plugin_pika_pika__probe_media`, and audio mix is balanced (you can hear the user over the original in a reaction duet; you hear the original in a performance duet).

**2. Caption legibility gate** — readable at phone-screen size on first pass; doesn't overlap a face or the mouth/chin; for duets, centered and clear of the split. No row is clipped by the left/right edge. Split long captions across two cards, reduce font size within 50-72, or adjust safe-zone margin and re-render. See the caption safe-zone guidance.

**3. Audio-sync gate** — for stitches, does the user's hook land right after the cut? For duets, do the user's reactions land on the original's beats? Re-trim if not.

**4. Orientation gate** — verify final portrait output with `mcp__plugin_pika_pika__probe_media`. If a source clip is rotated or framed wrong, re-run `mcp__plugin_pika_pika__edit_reframe` before compositing.

**5. Phone-cameo gate** — any phone visible in the user's half must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

**Output:** for stitches and native side-by-side duets, 1080×1920 H.264/AAC, 9:16. If the user explicitly accepted the `edit_split_screen` fallback, record the probed dimensions from `mcp__plugin_pika_pika__probe_media` and disclose that it is not the native half-canvas deliverable. Return `state.final_url` with version label `{user_slug}_{trend_slug}_v{N}` — never overwrite. Plus a post caption + hashtag set in the user's voice (text-only, lives in the description).

## Stage 7 — Loop

After delivering one stitch/duet, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**.

If they pick another, return to Stage 4 with that trend. Do NOT re-run trend research unless they ask — the Stage-3 menu of 10 stays warm for the session.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `mcp__plugin_pika_pika__scrape_social` → `provider_unavailable` / rate-limited | Upstream scraper outage | Retry after 30–60s; if it persists, switch the discovery angle (`trending-feed` ↔ `keyword` ↔ `hashtag`) and tell the user research is degraded — don't fabricate cards to fill the gap |
| Scrape returns no media URL for the chosen original | Private / age-gated / region-locked source video | Tell the user and ask them to upload a local copy of the original |
| `mcp__plugin_pika_pika__transcribe_audio` returns one big segment | ASR emitted coarse segment timing | Use the approved reaction script to create manual phrase rows, align them to the planned delivery beats, and keep the uncertainty visible in the delivery note |
| User clip plays rotated / sideways after composite | iPhone rotation metadata was not normalized before compositing | Verify with `mcp__plugin_pika_pika__probe_media`; if pixels are still rotated, re-run `mcp__plugin_pika_pika__edit_reframe` before composing |
| `mcp__plugin_pika_pika__edit_concat` errors or audio drops at the join | Original & user clips have incompatible audio layouts | Re-run `mcp__plugin_pika_pika__edit_reframe` on both sources, then retry `mcp__plugin_pika_pika__edit_concat`; if the original has no audio, keep the hook short and surface that caveat |
| Original already has burned captions + narrator audio (AI brainrot, subtitled clips) | Source isn't clean | Keep the stitch beat short (≤ the hook) so it reads as "the chaos"; don't fight it — your captions only go on the user's half |
| Menu comes back under 10 cards | Few originals clear the ≥500K viral bar this week | Deliver fewer and say "only N viral originals clear the bar right now" — never pad with low-view clips |
| Original is taller/shorter than 9:16 (e.g. 576×1048, 1:1, landscape) | Source aspect ≠ 1080×1920 | Run `mcp__plugin_pika_pika__edit_reframe(target_aspect="9:16", fill_mode="crop")`; never stretch |
| User teleprompter take is landscape | User opened the link on a desktop camera or the browser ignored portrait capture | Ask for a phone/portrait reshoot unless the user accepts center-crop rescue; do not treat landscape as the expected path. |
| Caption row clips at the frame edge | Long punchline sent as one row | Split the caption into shorter timed rows before re-running `mcp__plugin_pika_pika__add_captions`. |

## Don'ts

- **Don't propose formats with no original clip to pair against.** This playbook is stitch/duet only — the user's footage MUST combine with an existing creator's video. Plain talking-head → `formats/talking.md`. Silent POV → `formats/pov.md`. AI dance → `formats/dance.md`. Multi-format → the Content Director front door.
- **Don't make the user find the original.** The agent finds AND fetches the viral original itself (Stage 5) — the user only films their response.
- **Don't invent originals.** Every card needs a real, tappable original-video URL with a real play count in hand. If research comes back empty, tell the user and broaden — don't fabricate.
- **Don't require a replicated template.** This is the big one: a stitch/duet reaction is NOT a fingerprinted trend that 10 people copy identically — everyone reacts to the SAME viral original in their OWN way. The proof is the ORIGINAL's virality, not a replication wave. Don't drop a great reaction-worthy viral video just because nobody's stitched it in a specific repeated format.
- **Don't pitch a low-view original.** Hard floor on the ORIGINAL: ≥500K plays (millions ideal). The entire point is borrowing a video the algorithm and audience already recognize. A low-view source = nothing to borrow. Drop it.
- **Don't pitch a vague topic instead of a specific video.** "React to AI drama" is not a card. "React to {this specific 4M-play clip}, show 0:00–0:05, here's your line" is a card. Always a specific, nameable, viral source video.
- **Don't pad the menu to hit 10.** If fewer than 10 viral reaction-worthy originals clear the bar, deliver fewer and say "only N clear the bar right now." Never inflate with low-view clips or blog-citation-only entries.
- **Don't pitch a stale moment.** The original must be circulating now (last ~30–60 days) or in an active resurgence. A viral moment whose wave passed months ago is dead air.
- **Don't strip the user's voice from the response.** The original is the original; the *response* is 100% theirs — casing, punctuation, catchphrases, deadpan/rant cadence. Cross-reference the trend-vs-voice separation rule.
- **Don't stretch the clips in the composite.** Always cover-crop (or letterbox) before composing — never distort aspect to fill a panel. For native side-by-side duets, render the 1080×1920 half-canvas via `mcp__plugin_pika_pika__render_html_animation`; use `edit_split_screen` only as a disclosed fallback.
- **Don't desync a duet.** Both halves must be the same length and play together. Equalize duration before `mcp__plugin_pika_pika__render_html_animation`; trim, don't let one half freeze mid-reaction.
- **Don't bury the user under the original in a reaction duet.** The user's audio sits ON TOP (0 dB), the original ducks (~−10 dB). For performance duets it's the reverse. Pick per the 4d plan.
- **Don't burn captions outside the safe zone**, and for duets keep them centered and clear of the vertical split. For 9:16 stitch/native duet output, stay inside y=270-1475. For explicitly accepted split-screen fallback output, scale the same safe-zone intent to the probed dimensions. See the caption safe-zone guidance.
- **Don't chain arbitrary text overlays for captions.** Use one `mcp__plugin_pika_pika__add_captions` pass with `reels-clean`, 4px black outline, and safe-zone placement — see Stage 6c and the caption safe-zone guidance.
- **Don't claim the composite gets native TikTok stitch/duet attribution.** It doesn't — be honest (see the native-feature reality section). It's the only path on Reels and a controllable path on TikTok; the in-app button is the native-credit alternative.
- **Don't show old phones.** Any phone in the user's footage must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't skip the Stage 3 menu and jump to production.** Present the menu (up to 10), always wait for a pick. Producing without a selection burns the user's budget and tokens on a video they may not want.
