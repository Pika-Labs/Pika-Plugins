---
name: content-director-format-duet
description: >-
  Personal content director for stitch/duet reaction videos: finds a viral,
  proven, recognizable video worth reacting to and writes the creator's response
  in their voice. Ingests an Instagram/TikTok handle, reads their style, and
  surfaces viral originals (each with real play-count proof) that hand them an
  obvious clever take. Needs the pika MCP (scrape_social) + local ffmpeg.
  Triggers: "be my stitch content director", "find duet trends for me",
  "find a viral video to react to", "make me a stitch video",
  "react to a trending video", "stitch/duet for {handle}", "content-director duet".
argument-hint: "<@handle | instagram/tiktok URL>"
required-capabilities:
  - mcp__claude_ai_pika__scrape_social
  - mcp__claude_ai_pika__transcribe_audio
---

# Content Director — Stitch / Duet (react to a viral video)

A reaction-content director. The core idea is simple: **find a viral, proven, recognizable video → write a clever response in the user's voice → stitch them together so the viral original plays first, then hard-cuts to the user reacting/responding.** The user gives you their IG or TikTok handle; you reverse-engineer their style, surface **up to 10 viral videos worth reacting to** that fit, write the response for the chosen one, and produce the finished 9:16 mp4.

The deliverable per pick is always: **the proven viral original (the agent finds and fetches it) + a response script in the user's voice (what they say/do after the cut) + filming directions + timed captions + the final composited mp4** — original first, hard cut to the user — with audio handled and captions burned in the IG Reels safe zone. **You find the video and write the response; the user just films their half.**

This playbook is the reaction-focused sibling of the Content Director front door, `formats/pov.md`, `formats/talking.md`, and `formats/dance.md`. Multi-format menu → `content-director`. Silent POV → `content-director pov`. Plain talking-head with no original to react to → `content-director talking`. **This playbook is specifically for reacting to / responding to an existing viral video.**

## The default format: STITCH (original → cut → response)

The primary, default build is a **stitch**: the viral original plays first (the hook / claim / moment / question — usually ~2–6s, trimmed to the exact beat worth reacting to), then a **hard cut** to the user's full response. This is the structure the user asked for — *first we see the viral video, then cut to the user responding.*

| Layout | Structure | When to use |
|---|---|---|
| **Stitch (default)** | **Sequential** — viral original first, hard cut to the user reacting/responding/answering/flipping it | Almost always — reacting to a take, answering a question, debunking, deadpanning, one-upping, "my version" |
| **Duet (optional)** | **Side-by-side** — original and user play **simultaneously**, split-screen | Only when the reaction must land *in real time against the playing original* (live shock/laugh beat-for-beat, sing/perform-along) |

Default to **stitch** unless the reaction genuinely needs the original playing at the same time. Both are produced by **compositing** the user's footage with the original locally — see Stage 6 for the exact recipes.

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

1. **Scrape the profile** — `mcp__claude_ai_pika__scrape_social` on the handle. Pull the most recent 12–20 posts. Capture: captions, hashtags, post types (reel / carousel / static), recurring locations, recurring people, view counts, music choices, whether they already stitch/duet anything.

2. **Fallback if scrape_social returns empty / rate-limited** — `mcp__claude_ai_pika__capture_website` on `https://www.tiktok.com/@{handle}` or `https://www.instagram.com/{handle}/` for at least the bio + grid screenshot. Tell the user the analysis is grid-only.

3. **Synthesize a Creator Profile** (internal, then summarized for the user):
   - **Niche** — primary topic cluster
   - **Voice & tone** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Aesthetic** — color palette, lighting, framing, indoor vs outdoor, selfie vs third-person
   - **Caption style** — short clipped vs long rambly; lowercase-only? emoji-heavy? all-caps for emphasis? — copy this EXACTLY for on-screen captions
   - **Reaction style** — how do they emote/argue/joke in their existing posts? (deadpan stare, big laugh, rapid-fire rant, slow build) — this drives the reaction script
   - **Recurring motifs** — repeating props, locations, catchphrases, sign-offs
   - **What works for them** — flag the 2-3 posts with disproportionate engagement
   - **Filming environment baseline** — what spaces appear in their grid

4. **Present the Creator Profile back to the user** in ~6 short lines, then say: "Rolling stitch/duet trend research now — flag anything you want me to recalibrate."

## Stage 2 — Find viral videos worth reacting to (you do the legwork)

**The agent finds the proven viral originals AND fetches them itself — the user never hunts down a link.** For every card on the Stage-3 menu you MUST have already captured a concrete, openable, currently-circulating original-video URL **with its real play count**.

**The hunt is for VIRAL ORIGINALS, not for a replicated template.** You're looking for videos that are blowing up / widely recognized right now and that hand the user an obvious clever response. Two complementary angles — run both:

1. **Reaction magnets (strongest).** Videos people are *already* stitching/dueting — proof they're reaction-bait.
   - `mcp__claude_ai_pika__scrape_social` `tiktok / keyword` — `"stitch this"`, `"duet this"`, `"reply"`, `"react to this"`, plus the user's niche words (`"AI video"`, `"AI art"`, `"is this AI"` for an AI creator)
   - `tiktok / hashtag` — `#stitch`, `#duet`, `#greenscreen`, `#react`, niche tags
   - When you find a stitch/duet getting traction, **trace it back to the ORIGINAL it reacts to** and verify the original's play count.

2. **Viral originals + current moments.** The big videos/claims/clips of the moment that beg for a take.
   - `tiktok / trending-feed` (region-targeted) and `tiktok / popular-hashtags` — pull the genuinely high-play videos
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

### 4b. Filming breakdown — MANDATORY (exact filming directions)

The user MUST know exactly what to shoot. Non-negotiable for every Stage 4 delivery. Numbered shots, each filmable on the user's phone with no crew. For each:
- **Shot #** and **duration (s)** — for duets, this must match the original's length (they play simultaneously); for stitches, the user's clip can run as long as the response needs.
- **Camera position** — tripod / leaned / handheld — and HEIGHT (eye level, chest, low angle).
- **Where to stand / sit** — distance from camera (feet/cm), orientation (facing lens / 3⁄4 / side).
- **Framing** — and for **duets, frame for the split**: the user occupies only HALF the screen, so shoot with the subject biased toward the *inner* edge (toward the original) and leave headroom — a tight-but-not-cramped medium/close works best in a half-frame. Tell them which half they'll be on (see Stage 6 for the convention).
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
- **Position** — bottom safe zone (y ≈ 1255 for 1080×1920) by default. **For duets**, captions go in the bottom safe zone centered across the full 1080 width (they overlay the bottom of both halves) — keep them clear of the vertical split seam at x=540 by centering, and never put a caption in the top unsafe zone. Cross-reference the caption safe-zone guidance for the y-position table.
- **Style** — white Arial Bold ~63px, 4px black stroke per the caption safe-zone guidance. Deviate only if the trend has a signature caption style (call it out).

### 4d. The original clip + audio plan

- Restate the **original-clip URL** (from the menu card) so the user can sanity-check.
- **Stitch point** (for stitches) — the exact original segment used (e.g. "0:00–0:03").
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

Once the user **picks a reaction script variant** from Stage 4a and approves it — hand them the canonical Pika teleprompter via `formats/teleprompter.md` so they can record their half with the script scrolling on their phone (under the lens, per-line pacing, 3-2-1 countdown, Share when done).

**For STITCH:** the script being prompted is the user's response *after* the hard cut from the original. Length should at minimum match what they need to say; aim for the same total length as the original they're reacting to.

**For DUET (side-by-side):** the script is the live reaction running ALONGSIDE the original. They should play the original on a second device for timing, and the teleprompter scrolls their commentary in sync.

**Build the URL** against the deployed app at `https://teleprompter.pika.bot/`:

```python
import urllib.parse
url = "https://teleprompter.pika.bot/?" + urllib.parse.urlencode({
    "script": state.script_text,            # the chosen reaction script variant
    "handle": state.handle.lstrip("@"),
    "trend":  state.pick.name,               # e.g. "@calvin.james41 — everything is AI"
    "format": "duet",
})
```

**Do NOT pass `?upload=...`** in v1 — Share-only flow (see talking SKILL.md Stage 4f for the TTL reasoning). The user records and shares the take back manually.

**Emit the URL and, when already available, an approved server/CDN QR image URL** (canonical handoff — see `formats/teleprompter.md`):

```python
qr_image_url = state.teleprompter_qr_image_url  # optional: approved server/CDN QR for this exact url
qr_block = f"![Scan QR]({qr_image_url})" if qr_image_url else ""
```

**Caption to surface to the user** (verbatim, swap the original's reference):

> 📱 **Film your reaction on your phone.** Open the link below; if a QR image is included, scan it. Your reaction script is already loaded, with the read zone at the top right under the camera lens. Play the original on a second device for timing.
>
> {qr_block}
>
> 🔗 Or open here: {url}
>
> When the take is ready, hit **Share** → **AirDrop** back to this Mac (or save to Photos + drag it into the chat). I'll pick it up and compose the stitch/duet.

If `qr_image_url` is empty, omit that markdown image line entirely; do not generate a local QR PNG.
The hosted page still renders its own QR on desktop if the user opens the link there first.

After this — wait for the take. Stage 5's "Receive + sanity-check the user's footage" begins when the file lands.

## Stage 5 — Acquire the original + receive the user's footage

This playbook needs **two** video inputs: the original clip (agent fetches) and the user's response (user uploads).

### Fetch the original clip yourself (don't make the user supply it)

- For TikTok/IG public URLs — `mcp__claude_ai_pika__scrape_social` (`tiktok / video` or `instagram / post`) to get the direct mp4 media URL, then `curl` it locally, then `mcp__claude_ai_pika__upload_asset` to Pika CDN so it's available to the edit tools.
- If scrape returns no media URL (private / age-gated / region-locked), tell the user and ask them to upload a local copy of the original.
- **Probe the original** — `ffprobe` (or `mcp__claude_ai_pika__analyze_media`): capture exact duration, resolution, aspect ratio, fps. For stitches, confirm the stitch-point segment exists. For duets, this duration is the target length for the user's clip.

### Receive + sanity-check the user's footage

When the user's clip arrives:
1. **Probe** — `ffprobe` / `mcp__claude_ai_pika__analyze_media`: confirm portrait orientation, ≥1080×1920, duration, fps.
2. **Sanity-check against the shot list** — was the response captured? For duets, is it ≥ the original's length? If a clip is unusable (wrong orientation, blurry, missing the reaction, too short for a duet), call it out and ask for a reshoot of *only that shot*.
3. **Phone-cameo gate** — if the user's clip shows a phone (common in reaction content), confirm it's a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

## Stage 6 — Compose the stitch / duet + edit

The composite is mechanical once both clips are in hand. Use local ffmpeg for the composite and the caption burn (MCP tools don't produce the exact split-screen / hard-cut layout or the Instagram-native caption look).

**ffmpeg binary:**
Resolve at runtime. Prefer `ffmpeg` on `PATH`. If unavailable, install `imageio-ffmpeg`
and resolve its bundled binary with `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.

Create `state.work_dir` in a host-local writable directory, such as `${TMPDIR:-/tmp}/pika_duet`.
Download both clips locally first (original segment + user clip).

### 6a. STITCH composite (sequential)

1. **Trim the original to the stitch segment** (e.g. 0:00–0:03) — `mcp__claude_ai_pika__edit_trim` or local ffmpeg `-ss`/`-to`. → `orig_seg.mp4`.
2. **Normalize + concat** both to 1080×1920, same fps, SAR=1, with each segment keeping its own audio:
   ```
   ffmpeg -i orig_seg.mp4 -i user.mp4 -filter_complex \
   "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v0]; \
    [1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v1]; \
    [v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -c:a aac -movflags +faststart {state.work_dir}/stitch_nocaption.mp4
   ```
   - `force_original_aspect_ratio=increase` + `crop` = cover/center-crop (no stretching, no bars). If a clip is already 9:16 this is a no-op crop.
   - If the original segment has no audio track, add `-f lavfi -t {dur} -i anullsrc` or generate silence so `concat` audio counts match.

### 6b. DUET composite (side-by-side, simultaneous)

**Convention:** original on the **right**, user on the **left** (TikTok's duet layout puts your new camera on the left). State this to the user; it's a one-line swap if they want it flipped.

1. **Match lengths** — both halves play together. Trim the user's clip to the original's duration (or vice-versa). `hstack` stops at the shortest, so equalize first.
2. **Cover-crop each to 540×1920, then hstack to 1080×1920**, and mix audio per the 4d plan:
   ```
   ffmpeg -i user.mp4 -i original.mp4 -filter_complex \
   "[0:v]scale=540:1920:force_original_aspect_ratio=increase,crop=540:1920,setsar=1,fps=30[left]; \
    [1:v]scale=540:1920:force_original_aspect_ratio=increase,crop=540:1920,setsar=1,fps=30[right]; \
    [left][right]hstack=inputs=2[v]; \
    [0:a]volume=1.0[ua];[1:a]volume=0.32[oa];[ua][oa]amix=inputs=2:duration=shortest:dropout_transition=0[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -c:a aac -movflags +faststart {state.work_dir}/duet_nocaption.mp4
   ```
   - **Reaction duet:** original `volume=0.32` (~−10 dB), user `volume=1.0` — values above.
   - **Performance / sing-along duet:** flip it — original `volume=1.0`, user `volume=0.0` (or low) since the original IS the trending sound.
   - Cover-crop (`force_original_aspect_ratio=increase` + `crop=540:1920`) fills each half like native TikTok. If a creator prefers letterboxed full frames, swap to `decrease` + `pad=540:1920:(ow-iw)/2:(oh-ih)/2:black`.

### 6c. Burn captions — LOCAL ffmpeg drawtext (NOT MCP captioning tools)

MCP captioning tools (`edit_text_overlay`, `add_captions`) don't produce the Instagram-native white-text-with-4px-black-stroke look. Always do this locally on the composited file from 6a/6b.

- **If the user speaks a scripted response** (talking stitch / reaction with dialogue): auto-transcribe via `mcp__claude_ai_pika__transcribe_audio` on the user's clip, then burn word-synced captions over the user's segment (offset by the original-segment duration for stitches so timings line up).
- **If the response is silent** (expression-only reaction, performance): burn the title-card captions from the 4c layout.

**Pipeline:**
```
a. font: copy an available bold sans font → `{state.work_dir}/font.ttf`
b. caption text → `{state.work_dir}/caption.txt` (use textfile= to avoid shell escaping)
c. drawtext on the composited mp4
d. save final → `{state.work_dir}/{user_slug}_{trend_slug}_v{N}.mp4`
```

**drawtext params (validated):**
- `fontfile={state.work_dir}/font.ttf` (bold sans)
- `textfile={state.work_dir}/caption.txt`
- `fontsize=57` (default; 50-72 per readability)
- `fontcolor=white`, `bordercolor=black`, `borderw=4`
- `x=(w-text_w)/2` (centered — clears the duet split seam at x=540)
- `y=1255` single-line bottom-safe-zone, OR triplet `1255/1335/1415` for 3 stacked lines
- Encode: `-c:v libx264 -preset medium -crf 20 -c:a copy -movflags +faststart`

**IG Reels safe zone (1080×1920):** top unsafe y=0-270, bottom unsafe y=1480-1920. Captions sit inside y=270–1475, ~80px margin from left/right edges. Default bottom (y=1255). **Emoji warning:** Arial Bold has no color emoji glyphs — drop emoji from the burned caption (they go in the post description at upload).

### Pre-delivery gates

**1. Composite-integrity gate** — open the final. For stitches: the cut is clean, the original segment is the right hook, audio doesn't clip at the seam. For duets: the split is even (540|540), neither half is stretched, both play in sync, audio mix is balanced (you can hear the user over the original in a reaction duet; you hear the original in a performance duet).

**2. Caption legibility gate** — readable at phone-screen size on first pass; doesn't overlap a face; for duets, centered and clear of the seam. Split long captions across two cards. See the caption safe-zone guidance.

**3. Audio-sync gate** — for stitches, does the user's hook land right after the cut? For duets, do the user's reactions land on the original's beats? Re-trim if not.

**4. Orientation gate** — verify pixel orientation, not just metadata: `cv2.VideoCapture(...).read()` returns `shape[0] > shape[1]`. Re-encode with `ffmpeg -vf "transpose=2"` if a source clip's pixels are rotated *before* compositing.

**5. Phone-cameo gate** — any phone visible in the user's half must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

**Output:** 1080×1920 H.264, AAC, 9:16, saved to `{state.work_dir}/{user_slug}_{trend_slug}_v{N}.mp4` — versioned, never overwrite. Plus a post caption + hashtag set in the user's voice (text-only, lives in the description).

## Stage 7 — Loop

After delivering one stitch/duet, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**.

If they pick another, return to Stage 4 with that trend. Do NOT re-run trend research unless they ask — the Stage-3 menu of 10 stays warm for the session.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `mcp__claude_ai_pika__scrape_social` → `provider_unavailable` / rate-limited | Upstream scraper outage | Retry after 30–60s; if it persists, switch the discovery angle (`trending-feed` ↔ `keyword` ↔ `hashtag`) and tell the user research is degraded — don't fabricate cards to fill the gap |
| Scrape returns no media URL for the chosen original | Private / age-gated / region-locked source video | Tell the user and ask them to upload a local copy of the original |
| `mcp__claude_ai_pika__transcribe_audio` returns one big segment, no per-word timing | Whisper emitted no word-level stamps | Run `silencedetect` (`silencedetect=noise=-32dB:d=0.25`) on the user audio to find phrase gaps, then map captions to those real boundaries |
| User clip plays rotated / sideways after composite | iPhone `.MOV` `displaymatrix` rotation not applied before compositing | Verify pixel orientation (`cv2` frame `h>w`); ffmpeg auto-rotates on decode — if pixels are still rotated, bake it with `transpose` before scaling |
| `concat` errors or audio drops at the seam | Original & user clips have different sample rates / channel counts | Normalize both to 48k stereo AAC (`aresample=48000 -ac 2`) before concat |
| Original already has burned captions + narrator audio (AI brainrot, subtitled clips) | Source isn't clean | Keep the stitch beat short (≤ the hook) so it reads as "the chaos"; don't fight it — your captions only go on the user's half |
| Menu comes back under 10 cards | Few originals clear the ≥500K viral bar this week | Deliver fewer and say "only N viral originals clear the bar right now" — never pad with low-view clips |
| Original is taller/shorter than 9:16 (e.g. 576×1048, 1:1, landscape) | Source aspect ≠ 1080×1920 | Cover-crop on composite (`force_original_aspect_ratio=increase` + `crop=1080:1920`); never stretch |

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
- **Don't stretch the clips in the composite.** Always cover-crop (or letterbox) — never distort aspect to fill a half. Duet halves are 540×1920 each; stitch frames are 1080×1920.
- **Don't desync a duet.** Both halves must be the same length and play together. Equalize duration before `hstack`; trim, don't let one half freeze mid-reaction.
- **Don't bury the user under the original in a reaction duet.** The user's audio sits ON TOP (0 dB), the original ducks (~−10 dB). For performance duets it's the reverse. Pick per the 4d plan.
- **Don't burn captions outside the IG Reels safe zone**, and for duets keep them centered (clear of the x=540 seam). Always inside y=270–1475. See the caption safe-zone guidance.
- **Don't use MCP captioning tools for the final burn.** `edit_text_overlay` gives black-text-on-white-pill; `add_captions` gives a preset look. Use LOCAL ffmpeg drawtext (white text, 4px black stroke, Arial Bold) — see Stage 6c and the caption safe-zone guidance.
- **Don't claim the composite gets native TikTok stitch/duet attribution.** It doesn't — be honest (see the native-feature reality section). It's the only path on Reels and a controllable path on TikTok; the in-app button is the native-credit alternative.
- **Don't show old phones.** Any phone in the user's footage must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't skip the Stage 3 menu and jump to production.** Present the menu (up to 10), always wait for a pick. Producing without a selection burns the user's budget and tokens on a video they may not want.
