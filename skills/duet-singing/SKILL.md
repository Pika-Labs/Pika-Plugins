---
name: duet-singing
description: >
  Make a TikTok-style split-screen duet video: user singing on the left + AI digital
  twin lip-synced to the same vocal on the right, with a diatonic harmony voice
  layered into the audio track. User provides a singing video and an avatar image
  (or the agent uses the registered persona avatar). Pipeline auto-tunes the user's
  vocal first so the AI presenter is lipsynced to an in-tune source, then adds the
  harmony, then composites the split-screen with the harmonised audio in one shot.
  Use when the user says "duet this", "sing with me", "duet video", "split-screen
  singing", "split-screen duet", "tiktok duet", "sing together", "make a duet of
  my singing", or "I want my AI self to sing along with me".
  NOT for: solo singing video (use `singing-video` for avatar-only performance),
  audio-only harmony (use `auto-harmonise` for "just add harmony to this audio"),
  or multi-person video (single user + AI twin only).
argument-hint: "<video-url> [--avatar <url>] [--harmony-vol 0.4] [--autotune-strength 0.7] [--key \"A minor\"] [--orientation horizontal|vertical] [--no-harmony] [--no-autotune]"
required-capabilities:
  - mcp__claude_ai_pika__extract_audio_from_video
  - mcp__claude_ai_pika__edit_audio_autotune
  - mcp__claude_ai_pika__generate_harmony
  - mcp__claude_ai_pika__generate_lipsync
  - mcp__claude_ai_pika__edit_split_screen
  - mcp__claude_ai_pika__identity_avatar_url
  - mcp__claude_ai_pika__identity_set_avatar
  - mcp__claude_ai_pika__upload_asset
  - mcp__claude_ai_pika__edit_trim
  - mcp__claude_ai_pika__edit_audio_separate
  - mcp__claude_ai_pika__task_status
  - mcp__claude_ai_pika__generate_image
---

# /pika:duet-singing

TikTok-style split-screen duet: user singing on one side, AI digital twin on the other side, lip-synced + autotuned + harmonised in one pipeline.

## Behavior defaults

- **Orientation**: `horizontal` (user left, AI twin right). Pass `--orientation vertical` for user top, AI twin bottom.
- **Autotune strength**: `0.7` (natural studio polish — neither raw nor T-Pain). Disable with `--no-autotune` if the user wants the AI twin lipsynced to the raw vocal.
- **Harmony volume**: `0.4` (natural blend). Disable with `--no-harmony` for a clean lipsync duet without harmony.
- **Avatar resolution**: `--avatar <url>` > `mcp__claude_ai_pika__identity_avatar_url` > `mcp__claude_ai_pika__generate_image` synthesises a **Shiro** persona (the auto-harmonise skill's original AI singer — Japanese-style anime aesthetic, light/silver hair, gentle singer expression). Shiro is the canonical duet partner when the user has no persona set.
- **Key**: auto-detected by autotune + harmony. The two algorithms cross-validate (they share a key-detection path). If `key_confidence < 0.7` is surfaced by either, prompt the user to supply `--key`.

## State variables produced and consumed

- `user_video_url`: input — positional arg
- `avatar_url`: from `--avatar` or persona — Step 0
- `original_audio_url`: extracted from user video — Step 1
- `autotuned_audio_url`: pitch-corrected vocal — Step 2 (skipped if `--no-autotune`)
- `harmonised_audio_url`: lead + harmony mix — Step 3a (skipped if `--no-harmony`)
- `ai_singing_video_url`: AI twin lipsynced — Step 3b
- `final_video_url`: split-screen with harmonised audio — Step 4

## Step 0 — Parse input

Required:
- Positional `user_video_url` — MUST be `https://...`. A clip of the user singing (5-30s ideal). Reject `file://`, `MEDIA:`, attached paths — call `mcp__claude_ai_pika__upload_asset` first.

Optional:
- `--avatar <url>` — override the registered persona avatar.
- `--harmony-vol <0..1>` — default `0.4`. 0.25–0.35 subtle; 0.5–0.6 strong; 0.7+ equal blend.
- `--autotune-strength <0..1>` — default `0.7`. 0=off, 0.3–0.5 subtle, 0.9–1.0 heavy T-Pain.
- `--key "<root> <major|minor>"` — override auto-detected key. Applied uniformly to autotune AND harmony (so both algorithms operate in the same key).
- `--orientation <horizontal|vertical>` — default `horizontal`.
- `--no-autotune` — feed the raw vocal into lipsync; AI twin will sing slightly off-key if the user did.
- `--no-harmony` — final audio is just the (autotuned) lead, no second voice.

If `user_video_url` missing, STOP and prompt the user for a singing video.

## Step 1 — Avatar + audio (parallel, state: `avatar_url`, `original_audio_url`)

**A. Avatar** (waterfall):
1. If `--avatar` supplied → use directly.
2. Else call `mcp__claude_ai_pika__identity_avatar_url`. If non-null → use.
3. Else fall back to **Shiro** — the canonical duet partner from the original auto-harmonise skill. Generate via `mcp__claude_ai_pika__generate_image` with prompt:

   > "Anime-style singer portrait, female, light silver/white hair (the name Shiro means 'white' in Japanese), gentle warm expression, soft studio lighting, microphone hint in frame, vertical 9:16 close-up portrait, expressive eyes, mid-song, soulful performance energy"

   Pass `aspect_ratio="9:16"`. Use the returned `url` as `avatar_url`. Surface to the user in Step 5 that Shiro was used as the duet partner because no persona was set — they can re-run with `--avatar <url>` or set their own via `mcp__claude_ai_pika__identity_set_avatar` to make their own twin sing instead.

**B. Audio**:
Call `mcp__claude_ai_pika__extract_audio_from_video(video_url=<user_video_url>, format=mp3)`. Read `audio_url` → `original_audio_url`.

## Step 2 — Autotune (state: `autotuned_audio_url`)

**If `--no-autotune`**: `autotuned_audio_url = original_audio_url`. Skip.

**Else**: Call `mcp__claude_ai_pika__edit_audio_autotune` with:
- `audio_url` — `<original_audio_url>` (NOTE: passing audio not video here — we want bare audio out for the next two steps to consume in parallel)
- `strength` — `<autotune_strength>` (0.7 default)
- `key` — `<key>` if `--key` was supplied (so step 3a stays in the same key)
- `trim` — `false` (preserve timing — must match the user video duration)

Read `url` → `autotuned_audio_url`. Also capture `detected_key` and `key_confidence` for the warning logic in Step 5.

## Step 3 — Lipsync + harmony (parallel, state: `ai_singing_video_url`, `harmonised_audio_url`)

**3a. Harmony** (skipped if `--no-harmony`):
Call `mcp__claude_ai_pika__generate_harmony` with:
- `audio_url` — `<autotuned_audio_url>`
- `harmony_vol` — `<harmony_vol>` (0.4 default)
- `key` — `<key>` if supplied OR re-pass the `detected_key` from Step 2 so both algorithms agree
- `trim` — `false`
- `include_harmony_only_track` — `false` (final audio is the mix; we don't need the isolated track for duet)

Read `url` → `harmonised_audio_url`.

**If `--no-harmony`**: `harmonised_audio_url = autotuned_audio_url` — final audio is just the corrected lead.

**3b. AI lipsync video**:
Call `mcp__claude_ai_pika__generate_lipsync` with:
- `image` — `<avatar_url>`
- `audio` — `<autotuned_audio_url>` (NOTE: lipsync uses autotuned not harmonised; the AI twin lipsyncs to the LEAD vocal, not the harmony voice. The harmony is added back into the final audio in Step 4.)
- `prompt` — `"expressive singing performance, emotional, eyes closing on high notes, head swaying to the rhythm, soulful"` — feel free to tailor based on the song's mood detected from the user video or from `--topic` (if introduced in a future arg).

Read `url` → `ai_singing_video_url`.

These two calls have no data dependency on each other — issue them concurrently if your runtime supports it.

## Step 4 — Split-screen + audio swap in one call (state: `final_video_url`)

Call `mcp__claude_ai_pika__edit_split_screen` with:
- `main_video_url` — `<user_video_url>` (left for horizontal, top for vertical)
- `overlay_video_url` — `<ai_singing_video_url>` (right for horizontal, bottom for vertical)
- `orientation` — `<orientation>` (default `horizontal`)
- `audio_url` — `<harmonised_audio_url>` (this replaces the composed output's audio track in the SAME call — saves a separate audio-replace step)

Read `url` → `final_video_url`.

The `audio_url` shortcut is the key versatility of `mcp__claude_ai_pika__edit_split_screen` — without it this skill would need a separate audio-replace step; with it we land in 4 total tool calls.

## Step 5 — Return

> Here's your duet: `<final_video_url>`
>
> Detected key: **`<detected_key>`** (confidence `<key_confidence>` from autotune)
>
> *(if `key_confidence < 0.7`)* Heads up — key detection confidence is low. The harmony and autotune may sound slightly off. Re-run with `--key "<root> <major|minor>"` if you know the song's key.
>
> Pipeline: user video → autotune (strength `<autotune_strength>`) → AI twin lipsync + harmony (vol `<harmony_vol>`) → `<orientation>` split-screen.

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Non-HTTPS user video | `file://`, `MEDIA:`, attached file | Instruct user to upload via `mcp__claude_ai_pika__upload_asset` first | STOP |
| No avatar available | `--avatar` missing AND `mcp__claude_ai_pika__identity_avatar_url` returns null | STOP and prompt user to set persona avatar first | None |
| Video too long | > 30s lipsync starts to queue heavily on Pika lipsync | Warn user, suggest trimming with `mcp__claude_ai_pika__edit_trim` first | Proceed with warning |
| Audio decode failure | `mcp__claude_ai_pika__extract_audio_from_video` returns error | Surface error; check video has an audio track | STOP |
| Polyphonic input | User video has backing instruments → noisy harmony | Warn before Step 3a; consider `mcp__claude_ai_pika__edit_audio_separate` to isolate vocals first | Proceed (lower-quality harmony) |
| Lipsync long-running | Step 3b exceeds 260s budget | Tool returns `task_id`; poll `mcp__claude_ai_pika__task_status` in tight loop | None |
| Low key confidence | `key_confidence < 0.7` from autotune | Surface in Step 5; suggest `--key` override | Proceed |
| Split-screen dimension mismatch | User video and AI lipsync have wildly different aspects | Worker scales to match main video's height/width preserving aspect; output may be wide; acceptable v1 | None |

## Parity notes (vs upstream auto-harmonise skill bundle)

| Upstream feature | v1 status | Reason |
|---|---|---|
| Autotune before lipsync | retained — Step 2 | Source-of-truth for both lipsync target and harmony target. |
| Diatonic third-above harmony | retained — Step 3a | Same algorithm as `/pika:auto-harmonise`. |
| Pika lipsync for AI twin | retained — Step 3b | Default provider; `kling` available via prompt tweaking. |
| Split-screen hstack/vstack | retained — Step 4 via `mcp__claude_ai_pika__edit_split_screen` | Single-call composite + audio swap. |
| Persistent avatar workdir + checkpoint | dropped | Upstream's local file resumability isn't relevant for stateless MCP calls. |
| Center-crop to 9:16 per panel | simplified | v1 scales to main video's height (horizontal) or width (vertical) preserving aspect. If user wants strict 9:16 panels, chain `mcp__claude_ai_pika__edit_reframe` per side before this skill. |
| Selfie portrait synthesis | dropped | Uses the user's existing persona avatar via `mcp__claude_ai_pika__identity_avatar_url`. |
| Beat-aligned cuts | dropped | Out of scope; pair with `/pika:music-beat-sync` if needed. |

## Compatibility

Primary target: Claude Code. Uses 6 MCP tool calls in 4 sequential steps (steps 1A+1B and 3a+3b each have intra-step parallelism). Standard MCP only — no platform-specific shell or local file IO.
