---
name: content-director-format-talking
description: >-
  Talking-to-camera content director. Takes an IG or TikTok handle, surfaces TTC
  trends with hard view-count proof (storytime, hot-take, "He's a 10 but…", GRWM-talk,
  confessional, "things nobody tells you", "POV explaining" — niche-fit + broad-viral),
  then for the chosen one writes a spoken script in the user's voice, an exact shot list,
  and finishes a 9:16 mp4 with trending audio mixed under the voice and word-sync
  captions burned in the IG Reels safe zone. Triggers — "be my talking-head content
  director", "find storytime trends for me", "make me a talking-to-camera trend",
  "TTC trends for {handle}", "hot-take trend for my niche", "content-director talking".
argument-hint: <instagram-or-tiktok-handle>
required-capabilities:
  - mcp__claude_ai_pika__scrape_social
  - mcp__claude_ai_pika__capture_website
  - mcp__claude_ai_pika__transcribe_audio
  - mcp__claude_ai_pika__analyze_media
---

# Content Director — Talking-to-Camera

A talking-to-camera specialist content director. The user gives an IG or TikTok handle; this playbook reverse-engineers their voice, finds TTC trends that pass a hard virality gate, and produces one end-to-end: spoken script in their voice + shot list + final edited mp4 with captions + trending audio mixed under the spoken track.

Sibling routing: `formats/pov.md` (silent / situational), `formats/dance.md` (AI-generated dance from a photo), the Content Director front door (multi-format menu), `formats/duet.md` (stitch / duet reactions).

## Parameters

- **handle** (required) — IG or TikTok handle, in any of `@name` / `name` / full URL form. Saved as `state.handle`.
- **goal**, **camera_comfort**, **filming_constraints**, **language** — optional bias inputs collected in Stage 0. Saved as `state.brief`.

## Stage 0 — Intake (empty-args menu)

If `$ARGUMENTS` is empty or carries no handle, print this menu verbatim and stop — without a handle the rest of the pipeline can't run:

> **What's your handle?** Drop your Instagram or TikTok in any format:
> - `@yourname`
> - `yourname`
> - `https://instagram.com/yourname` or `https://tiktok.com/@yourname`
>
> Optional context that biases the menu:
> - **What's this content for?** ("grow my brand", "personal account", "promote my SaaS", "just for fun")
> - **Camera comfort?** full face / face partially obscured / voiceover-only
> - **Filming constraints?** ("only at home", "no outdoor", "phone selfie only")
> - **Language / accent?** (English / Hebrew / Spanish / etc., plus any specifics like "casual NYC", "British dry")

Once a handle arrives, save it as `state.handle` and the optional bias as `state.brief`, then continue. Niche and aesthetic are derived from the scrape — don't re-ask.

## Stage 1 — Creator profile (`state.profile`)

The goal: capture the user's *written* voice AND *spoken* voice. TTC lives on spoken delivery, so spoken voice matters more than written; but written is the fallback when no audio exists on the grid.

1. **Scrape** — call `mcp__claude_ai_pika__scrape_social` on `state.handle` (instagram profile + user-reels + user-posts, or tiktok profile + profile-videos). Pull the most recent 12-20 posts.
2. **Listen** — if any scraped posts are reels with the creator talking, transcribe one or two via `mcp__claude_ai_pika__transcribe_audio` to capture cadence, fillers, sign-offs, energy curve.
3. **Fallback** — if scrape returns empty / rate-limited, run `mcp__claude_ai_pika__capture_website` on the public profile URL for a grid screenshot, and tell the user the profile is grid-only (spoken voice will be inferred from caption style).
4. **Synthesize** `state.profile`:
   - **Niche** — primary topic cluster
   - **Voice (written)** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Voice (spoken)** — separate from written; delivery speed, energy floor and ceiling, fillers, catchphrases, sign-offs. Note explicitly when this is unknown (no talking-head content on grid) so Stage 4 inherits written voice as a placeholder.
   - **Caption style** — short clipped vs long rambly, casing, emoji habits, punctuation. Copy this into on-screen title text so muted viewers feel the same voice as the spoken delivery.
   - **Aesthetic, recurring motifs, what works, filming environment baseline** — see the multi-option script and shot-list contract for what to capture.
5. **Present** the profile to the user in ~6 short lines (with separate "writes like" / "talks like" rows), then continue to Stage 2.

## Stage 2 — Trend research → `state.menu`

The goal: produce a menu of TTC trends that each have **3 reference clips with real view counts above the threshold**. The hardest failure mode this playbook has shipped historically is filling the menu with low-view topical content — guard against that explicitly. See the virality receipts gate.

### What counts as a trend (two-tier gate)

**Tier 1 — Fingerprinted viral trend** — a specific viral instance with all of: a named handle in ≤4 words, a fingerprint (same audio URL OR same verbatim opening sentence across replicators), 3+ reference clips each above the play threshold, 10+ replicators in past 30-60 days, same shot count / beat / duration window. Examples: "He's a 10 but…" card game (verbatim phrase + same structure + millions of plays), "I'm looking for a man in finance" (named audio).

**Tier 2 — Culturally-recognized viral TTC format** — fallback when Tier 1 yields fewer than ~5 cards. Formats that any regular TikTok viewer can name on sight (storytime, GRWM-talk, "things nobody tells you", confessional, "POV: explaining"). Tier 2 cards still need 3 reference clips at the play threshold — the format is evergreen but the example replicators must be at viral scale. Mark these cards `TIER 2 — Viral Format` so the user knows the differentiator is their voice + content angle, not a single audio.

### Play-count threshold (load-bearing)

- **Broad-viral cards:** each reference clip ≥ **500K plays**
- **Niche-fit cards:** each reference clip ≥ **50K plays**

Why: anything below these reads to viewers as "a creator doing a format," not a viral trend. See the virality receipts gate for the source incident — a prior menu padded with 200-15K-play clips broke user trust.

### Hard exclusions

- Topical clusters of low-view clips with no shared opener or structure → that's a vibe cluster, not a trend.
- Format archetypes shipped as trends without a specific viral instance (e.g. "Hot take ___" with no fingerprint) — only allowed as Tier 2 cards, with reference clips that still hit the play threshold.
- A creator's signature format that nobody else copies.
- An aesthetic / genre / hashtag without a shared structural template.

### TTC archetypes (reference, not exhaustive)

Storytime · Hot take / unpopular opinion · POV explaining (spoken, not silent) · Things nobody tells you · Confessional / "I'll be honest" · Reaction / response · Rant · GRWM-monologue · Spoken listicle · Day-in-the-life narration · "What I wish I knew" · "Answering your questions" · Lip-sync-then-talk hybrid. If a candidate doesn't fit one of these and isn't a Tier 1 fingerprinted instance, drop it — it's likely a vibe cluster.

If the trend requires silent acting and narrative-by-caption only → route to `formats/pov.md`. If it's pure lip-sync with no original spoken content → route to the Content Director front door's lip-sync path.

### Research order (don't skip — this order is the gate)

Topical keyword searches return vibe clusters of low-view content. The correct order is named-trend discovery first, virality verification second, TTC filter third.

1. **Discover named trends this week.** WebSearch for "TikTok trends {currentMonth} {currentYear}" and "Instagram Reels trends this week {currentMonth} {currentYear}" — cross-reference 3+ creator-tool blogs (Later, Hootsuite, NewEngen, Manychat, Buffer, OpusClip). Only trends named by 2+ blogs are still warm. In parallel: `mcp__claude_ai_pika__scrape_social tiktok / trending-feed` and `tiktok / popular-hashtags` to spot sounds with 5+ creators in the top 50.
2. **Capture the fingerprint** per candidate — exact audio name + artist + sound URL, OR the verbatim opening phrase. If creators paraphrase the opener, it's a format not a trend.
3. **Verify replicators** — for each candidate, scrape 3+ high-view clips via `mcp__claude_ai_pika__scrape_social tiktok / hashtag` (the trend's specific tag, not generic) or `tiktok / keyword` (using the verbatim phrase). Read each clip's `play_count` field and confirm threshold. Drop candidates that don't have 3 above the line.
4. **Filter for TTC** — the format must involve audible spoken delivery from the creator. Pure lip-sync, pure POV/silent, pure dance → drop.
5. **Score for the user's voice** — last step, ranking only, NOT a filter. The trend's format is vibe-agnostic; the user's voice attaches via the script in Stage 4. See the trend-vs-voice separation rule.

If fewer than 10 trends survive, ship fewer cards. Better 4 strong cards with receipts than 10 padded ones — the user has flagged inflation as a trust break.

### Card format

```
[N] {Named trend or format (≤4 words)}  •  TIER 1 — Fingerprinted Trend  (or TIER 2 — Viral Format)
    Density: {single-selfie / walk-and-talk / +b-roll / multi-loc / lipsync-then-talk}  •  Reference duration: {Xs}
    Fingerprint: {audio name + artist (Tier 1) OR verbatim opener (Tier 1) OR format name + signature opener shape (Tier 2)}
    Template: {one sentence — the SAME structure all replicators follow}
    Why it fits {handle}: {1 line}
    ▶ Reference clips (3, all hitting the view threshold):
       1. {URL} — {play_count} plays, {creator handle}, {date}
       2. {URL} — {play_count} plays, {creator handle}, {date}
       3. {URL} — {play_count} plays, {creator handle}, {date}
```

Save the full set as `state.menu`. Aim for the mix (when budget allows): 4 niche-fit + 4 broad-viral + 2 wildcards. When budget is thin, ship whatever passes.

## Stage 3 — Present menu, wait for pick

Print the menu cards. End with: **"Which one do we make? (pick a number)"**. Don't write the script or shot list before the pick — saves work if they want something else. Save the choice as `state.pick`.

## Stage 4 — Production package for `state.pick`

Deliver in one message:

### 4a. Spoken script + concept variations

Ship **6-10 spoken-script + concept variations**, not one option. Multi-option is mandatory — the user needs creative agency to pick the angle that hits. See the multi-option script and shot-list contract.

Per variation:
- **Opener is fixed** — the trend's verbatim opener (`storytime: that time I…`, `he's a 10 but…`, etc.) appears word-for-word. Paraphrasing breaks the algorithmic fingerprint and the viewer-recognition signal; the rest of the script is the user's voice.
- **Body** mirrors the user's *spoken* voice from `state.profile` (sentence length, fillers, pet phrases, sign-offs). When spoken voice is unknown (no talking-head content on grid), inherit the *written* voice and flag the variation as a take-1 calibration that may need retuning.
- **Length** fits the reference duration. Count words at ~2.5 spoken words/sec — going over the trend's window (15s / 30s / 45s / 60s) tanks completion rate.
- **Hook caption** (the on-screen title) lands in the first 1-2s, mirroring or paraphrasing the spoken opener so muted viewers recognize the trend instantly.

Variation template:
```
Variation {N} — {one-line concept hook}

Full spoken script (~{duration}s):
[0:00 — opener, dead at lens] {verbatim opener}
[0:03 — pivot] {body in their voice}
[~end — stinger] {payoff line}

On-screen opening title (0:00-2.0s): "{exact title text}"
Stinger title (optional, last 1-2s): "{exact text or 'none'}"
```

Save the chosen variation as `state.script`.

### 4b. Filming breakdown

Numbered shots, each filmable on the user's phone with no crew. Per shot:

- **Shot #** and **duration**
- **Camera position** — tripod / leaned against book / handheld selfie / propped, plus height (eye level default; just-below-eye for slight up-angle)
- **Where to sit/stand** — orientation to lens
- **Framing** — chest-up selfie / medium close-up is the TTC default; head upper-third, eyes near the rule-of-thirds line
- **Action** — exact delivery direction with timing ("look dead at lens, deliver opener flat 0:00-0:02, raise brow on beat drop 0:03")
- **Energy / pacing** — TTC lives or dies on delivery energy; spell out tempo and emotional arc
- **Props, look direction, lighting, wardrobe** — every prop named and placed
- **Audio capture** — phone mic at 18-24 inches works; AirPods better. Note background noise to avoid.
- **Re-takes** — 2-3 per shot for selects. For long scripts, split at a natural beat and mark with a clap so the editor can stitch invisibly.

The validated default — **phone at eye level, 18-24 inches from face, chest-up framing, window light from camera-side** — is load-bearing for the natural selfie/FaceTime feel TTC depends on.

Be filmable, not vibey. See the multi-option script and shot-list contract for the bar — "phone on tripod at eye level, 22 inches from face, sit on the edge of the bed facing the window so the natural light hits your left cheek" beats "morning storytime energy."

For b-roll inserts: list each insert separately with its own framing + duration, specify which spoken line it cuts in over, keep inserts silent so the A-roll voiceover carries under.

For lip-sync-then-talk hybrid: specify the exact lip-sync window (first 2-3s) and lyric being mouthed, plus the pivot moment where audio ducks and the user starts talking.

### 4c. Caption layout

Two layers of on-screen text:

**Layer 1 — Opening title card** (muted-viewer hook). Top safe zone, `y=380` for 1080×1920. Text mirrors or paraphrases the spoken opener. In 0:00-2.0s. Style: white Arial Bold ~57-63px with 4px black stroke (Instagram-native look — see Load-bearing phrases).

**Layer 2 — Word-sync captions** for the spoken script. Bottom safe zone, `y=1255`. Auto-generated from `mcp__claude_ai_pika__transcribe_audio` word-level timestamps in Stage 6. 2-4 word chunks, ~1.5-2.5s each, no chunk crossing a sentence break.

Pre-deliver the user a preview of how the word-sync captions will look for one or two variations (the punchy hook + the stinger) so they can flag rewording before filming.

### 4d. Trending audio role

The exact sound URL and where its beats land, plus how it sits in the mix:

- **Bed-under** (most common for TTC): trending sound at -12 to -18 dB under the spoken voice. The vibe of the sound colors the post; the algorithm matches on audio fingerprint.
- **Sting-then-duck**: trending sound full-volume for the first 2-3s (often a viral musical hit), then ducks hard so spoken voice takes over.
- **End-tag only**: trending sound silent for most of the video, fades in at the final 2-3s as a stinger.
- **Lip-sync-then-talk**: trending sound full volume in the lip-sync window, ducks to -15 dB once the user starts talking, optionally returns at the end.

Save the chosen role as `state.audio_role` — Stage 6 references it.

### 4e. Filming checklist (handed to the user)

- Phone in airplane mode + Do Not Disturb
- Vertical / portrait orientation locked
- 4K 30fps or 1080p 60fps
- Clean lens (front-facing if selfie)
- One light source — window during day, ring/desk lamp at night, aimed at the face from camera-side
- Lock exposure AND focus before filming (tap-and-hold on the face in iOS camera)
- Mic distance — phone 18-24 inches from face; AirPods if available
- Background — nothing identifying you don't want public (mail, screens, kids)
- 2-3 takes per shot
- For multi-chunk scripts, mark chunk breaks with a clap or finger snap

### 4f. Teleprompter handoff (hand the script to the user's phone)

Once the user **approves** the script in Stage 4 — *don't* leave them to copy-paste it into a separate prompter app. Hand them the canonical Pika teleprompter via `formats/teleprompter.md` so they get camera + scrolling read-zone + per-line pacing in one tap.

**Build the URL** against the deployed app at `https://teleprompter.pika.bot/`:

```python
import urllib.parse
url = "https://teleprompter.pika.bot/?" + urllib.parse.urlencode({
    "script": state.script_text,           # the full approved script with newlines
    "handle": state.handle.lstrip("@"),     # e.g. "matancohengrumi"
    "trend":  state.pick.name,              # e.g. "Wow, ok challenge"
    "format": "talking",
})
```

**Do NOT pass `?upload=...`** in v1 — Share-only flow. Pika's `upload_asset` presigned URLs expire in minutes, which would break for any user who spends >5 min recording. The user records on their phone and **shares the take back** (AirDrop / Save to Photos / attach to chat). When/if a long-TTL upload primitive ships, this is where we'd add `&upload=<presigned>` and resume Stage 5 by polling `public_url`.

**Emit the URL and, when already available, an approved server/CDN QR image URL** (canonical Pika-MCP handoff — see `formats/teleprompter.md`'s "The handoff" section):

```python
qr_image_url = state.teleprompter_qr_image_url  # optional: approved server/CDN QR for this exact url
qr_block = f"![Scan QR]({qr_image_url})" if qr_image_url else ""
```

**Caption to surface to the user** (use this verbatim, swap the trend name):

> 📱 **Film it on your phone.** Open the link below; if a QR image is included, scan it. Your script is already loaded with the read zone at the top right under the camera lens. You get 3-2-1 countdown, per-line pacing, re-shoot, and Share when you're done.
>
> {qr_block}
>
> 🔗 Or open here: {url}
>
> When the take is ready, hit **Share** → **AirDrop** back to this Mac (or save to Photos + drag it into the chat). I'll pick it up and run Stage 5.

If `qr_image_url` is empty, omit that markdown image line entirely; do not generate a local QR PNG.
The hosted page still renders its own QR on desktop if the user opens the link there first.

After this — wait for the user to deliver the clip via chat attachment. Stage 5's first action ("When the clips arrive") starts when the file lands.

## Stage 5 — User films, uploads → `state.clips`

When the clips arrive:

1. **Probe** — `ffprobe` or `mcp__claude_ai_pika__analyze_media` per clip. Confirm orientation (portrait — see Failure modes for the iPhone displaymatrix gotcha), resolution (≥1080×1920 after rotation), duration, framerate, and audio presence.
2. **Transcribe** — `mcp__claude_ai_pika__transcribe_audio` (whisper provider, timestamps=true) on each A-roll clip. Save word-level timestamps as `state.transcript` for the caption burn.
3. **Opener verbatim check** — listen to the first 2-3s of each clip; if the opener was paraphrased, ask for a reshoot of just the opener.
4. **Shot list check** — confirm each scripted shot was captured. If a single clip is unusable (wrong orientation, blown exposure, blurry, silent), reshoot only that shot.
5. **Fetch trending audio** — `mcp__claude_ai_pika__scrape_social tiktok / video` to get the media URL, curl it locally, extract via `mcp__claude_ai_pika__extract_audio_from_video`. Save as `state.audio_track`.

## Stage 6 — Edit pipeline → `state.final`

Mechanical once `state.clips`, `state.transcript`, and `state.audio_track` are in hand.

1. **Measure end-of-speech per clip** — run `ffmpeg -af silencedetect=noise=-30dB:d=0.2` on each source clip to find the precise trailing-silence start. Trim each clip to `(end_of_speech + 100ms)` so verdicts land hard against the cut. See the trim measurement guidance for the lesson — eyeballed trims left 1.5s of dead air per clip and broke the deadpan rhythm.
2. **Transcode each clip to portrait 1080×1920** — `scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2`, H.264 + AAC, 30fps. iPhone clips arrive with displaymatrix rotation metadata; ffmpeg auto-applies on decode, so the pixel orientation flips to portrait without an explicit transpose.
3. **Concat in script order** — `ffmpeg -f concat -safe 0 -i list.txt -c copy concat.mp4`. Same codec across clips → stream-copy is safe.
4. **Mix audio** per `state.audio_role` (Stage 4d). The user's spoken voice is the deliverable, so the trending audio sits under it — never replace.
5. **Burn captions locally with ffmpeg drawtext** — not MCP captioning tools. The Instagram-native white-text-with-4px-black-stroke Arial Bold look is load-bearing; MCP `edit_text_overlay` produces a black-text-on-white-pill, `add_captions` produces a stylized preset that misses the look. See Load-bearing phrases below for the validated params.
6. **Final encode** — `-c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart`. Save to `{state.work_dir}/{user_slug}_{trend_slug}_v{N}.mp4` in a host-local writable directory. Versioned — never overwrite a previous deliverable.

### Pre-delivery gates

- **Opener-verbatim** — the first 2-3s of the final cut delivers the trend's opener word-for-word. Paraphrasing breaks the trend fingerprint.
- **Caption legibility + sync** — every chunk readable on first pass at phone screen size, lands on the right spoken words within ±100ms. If chunks lag or lead, re-derive timings from the transcript and re-render.
- **Audio balance** — spoken voice intelligible above the bed. Lower bed by 3-6 dB if it clips the voice; normalize down if voice peaks > -3 dB.
- **Audio-sync** — trending audio's beat drop lands on the script's pivot moment, stinger lands on the closing line. Retime the audio offset if misaligned.
- **Pixel orientation** — verify with `cv2.VideoCapture(...).read()` returning `shape[0] > shape[1]`. Re-encode with `ffmpeg -vf "transpose=2"` if a clip's pixels are still landscape after auto-rotate (rare but happens with edited iPhone exports).
- **Phone-cameo** — if any clip shows a phone on screen, it must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

## Stage 7 — Loop

After delivering `state.final`, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**. If they pick another, return to Stage 4 with that trend — the Stage 3 menu stays warm for the session.

## Load-bearing phrases

Each phrase below is verbatim-anchored — agents simplifying the skill should not edit these without re-validating, because empirical behavior depends on them. Source incidents linked.

### Caption render (validated `pika-trendy-reel` pattern)

- Font: copy an available bold sans font to `{state.work_dir}/font.ttf` to avoid space-in-path issues. Good defaults: macOS Arial Bold, Linux DejaVu Sans Bold, or Windows Arial Bold.
- `fontsize=57` (scale 50-72 per readability)
- `fontcolor=white`
- `bordercolor=black`
- `borderw=4` — the 4px black stroke is the Instagram-native look. MCP captioning tools produce a different look that misses this.
- `x=(w-text_w)/2` — horizontally centered
- Top opening title: `y=380` (inside top safe zone)
- Bottom word-sync: `y=1255` (inside bottom safe zone, avoids face overlap)
- IG Reels safe zone (1080×1920): captions sit inside `y=270 to y=1475`, ~80px margin from left/right edges
- `enable='between(t,{start},{end})'` — gates each chunk's time window
- Use `textfile=...` per chunk (one textfile per caption) — avoids shell-escape pain on quotes/apostrophes
- Emoji warning: Arial Bold has no color emoji glyphs. Drop 🖤 🖼️ etc. from burned captions; tell the user to put emoji in the post description at upload.

### ffmpeg binary

Resolve at runtime. Prefer `ffmpeg` on `PATH`. If unavailable, install `imageio-ffmpeg`
and resolve its bundled binary with `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.

### Trim measurement

`silencedetect=noise=-30dB:d=0.2` then trim to `(last silence_start + 100ms)`. Eyeballed trims have shipped 1.5s of dead air per clip in production — measure, don't guess. See the trim measurement guidance.

### Filming defaults

Phone at eye level, 18-24 inches from face, chest-up framing, window light from camera-side. Validated for the natural selfie/FaceTime feel TTC depends on.

### Audio mix levels

Bed-under: trending audio at -15 dB, voice at 0 dB. Sting: 0 dB sting → duck to -18 dB once voice enters. End-tag: -3 dB fade-in for the last 2-3s.

### Play-count thresholds

≥500K plays (broad-viral) or ≥50K plays (niche-fit) per reference clip. Anything below reads as a creator doing a format, not a viral trend.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `mcp__claude_ai_pika__scrape_social` returns empty / rate-limited | Profile blocked, region-locked, or quota exhausted | Fall back to `mcp__claude_ai_pika__capture_website` on the public URL for grid screenshot. Tell the user the spoken voice will be inferred from caption style. |
| Whisper `mcp__claude_ai_pika__transcribe_audio` returns 0 segments | Short clip with no detected speech, or audio track is silent / corrupted | Re-run with `provider="gemini"` via `mcp__claude_ai_pika__analyze_media` to double-check. If both fail, ask the user to confirm the clip has audible audio. |
| Whisper mis-transcribes a phrase ("haters will say" → "hey don't") | Short clip + Israeli accent + brand-name words. Whisper degrades on <3s clips. | Use the scripted line verbatim for the caption. Don't re-transcribe — the user knows what they said. |
| User delivers a paraphrased opener | Forgot the exact wording mid-take | Reshoot only the opening 2-3s and splice in. Don't re-shoot the whole sequence. |
| iPhone clip metadata shows `1920x1080` (landscape) | iPhone stores rotation in displaymatrix, not pixel layout | ffmpeg auto-applies the displaymatrix on decode — output will be 1080×1920 portrait. Verify the post-decode dimensions, not the file metadata. Add `transpose=2` explicitly only if a clip pixel-checks as landscape after decode. |
| Tail silence between cards in concat output | Trims eyeballed instead of measured | Re-run `silencedetect` per clip, trim to `(last silence_start + 100ms)`. See Load-bearing phrases. |
| Caption text overlaps the speaker's face | Top zone caption placed too low, or word-sync caption escaped the safe zone | Top = y=380, bottom = y=1255 for 1080×1920. Re-render with corrected y values. |
| Concat fails with "Non-monotonic DTS" warning | Source clips have slight timestamp drift after trim | Warning is benign for visual output. If the audio glitches on playback, re-encode each clip with `-fflags +genpts` before concat. |
| ffmpeg drawtext filter string fails to parse | Apostrophes / colons / commas in caption text leak into the filter | Always use `textfile=...` per chunk, never inline `text='...'`. One textfile per caption, generated by a Python helper. |
| Stage 3 menu has < 10 cards | Fewer than 10 trends pass the strict virality gate this week | Ship what passed (could be 3, 5, 7). Tell the user "only N trends qualified this week" and list the formats that were popular but lacked fingerprinting. Never inflate — see the virality receipts gate. |
| Final video exceeds the trend's duration window | User's natural delivery is longer than the trend's reference clips | Trim filler / breath / dead air in the edit. If still over, trim the script before re-filming. Going over kills completion rate. |

## What NOT to do

- **Don't ship format archetypes as trends without reference receipts.** "Hot take ___" / "Storytime: that time I…" / "Things nobody tells you about ___" are evergreen FORMATS. They only earn a card slot when accompanied by 3 reference clips at the play threshold (Tier 2). Without receipts, the menu becomes a vibe cluster — the user has flagged this as the failure mode.
- **Don't pad reference URLs with creator-tool blog citations alone.** Blog citations help discover trend names. They do not stand in for the 3 viral reference URLs.
- **Don't keyword-search topical content as the primary research method.** "storytime AI artist" returns vibe clusters of low-view content. Order: blog recaps → named-audio discovery → trending-feed scan → verify each candidate has 3 high-view replicators.
- **Don't deliver 10 cards when fewer pass the gate.** Ship 3, 5, or 7 if that's what survives. Inflating burns user trust.
- **Don't paraphrase the trend's fixed opener.** The verbatim opener is the algorithmic fingerprint and the viewer-recognition signal. Paraphrasing breaks both.
- **Don't strip the user's voice from the body of the script.** Match the trend's opener and structure; write the post-opener body in the user's actual spoken voice.
- **Don't film for the user.** This playbook writes the plan and runs the edit; the user films their own talking-head footage. No AI-generated TTC footage — the authenticity of the actual delivery is the format's value.
- **Don't write vibey shot lists.** Every shot needs explicit camera position, distance, framing, energy direction, look direction.
- **Don't burn captions outside the IG Reels safe zone.** Inside `y=270 to y=1475` for 1080×1920, ~80px left/right margin. See the caption safe-zone guidance.
- **Don't use MCP captioning tools for the final caption burn.** `edit_text_overlay` produces black-text-on-white-pill (wrong); `add_captions` produces a stylized preset that misses the Instagram-native look. Use local ffmpeg drawtext per Load-bearing phrases.
- **Don't put word-sync captions over the user's face.** Bottom safe zone (y=1255). Top is reserved for the opening title-card hook.
- **Don't replace the user's spoken audio with the trending sound.** Mix under (bed-under / sting-then-duck / end-tag). Audio-replace is for pure lip-sync only.
- **Don't exceed the trend's duration window.** 15s / 30s / 45s / 60s. Over kills completion rate; cut tighter or trim the script.
- **Don't propose 10 of the same archetype.** Mix storytime / hot-take / POV-explaining / things-nobody-tells-you / rant / GRWM-monologue across the menu.
- **Don't show old phones.** If a clip shows a phone, it must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't skip the Stage 3 menu and jump to production.** Always present cards, always wait for a pick. Producing without selection burns tokens and budget on a video the user may not want.
