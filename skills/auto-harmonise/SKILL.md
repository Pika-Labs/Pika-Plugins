---
name: auto-harmonise
description: >
  Add a diatonic third-above harmony voice to a monophonic vocal or single-instrument
  recording. Detects the key automatically and blends a phase-coherent harmony track
  back with the lead. Use when the user says "add harmony to this", "harmonise this",
  "harmonize this", "make this a duet", "add a second voice", "auto-harmonise", or
  "give me a harmony track for this audio". Single audio in, single mixed audio out
  (optionally also returns the isolated harmony track).
  NOT for: polyphonic mixes (full songs with backing instruments — won't track pitch
  cleanly), choir-style 4-part harmony (single third-above only), or autotuning a
  recording (use `/pika:autotune` / `edit_audio_autotune` for pitch correction).
argument-hint: "<audio-url> [--key \"A minor\"] [--harmony-vol 0.4] [--no-trim] [--with-harmony-only]"
required-capabilities:
  - mcp__claude_ai_pika__generate_harmony
  - mcp__claude_ai_pika__edit_audio_separate
  - mcp__claude_ai_pika__upload_asset
---

# /pika:auto-harmonise

Add an in-key harmony voice (diatonic third above) to a monophonic vocal recording. One-step wrap of `mcp__claude_ai_pika__generate_harmony` with sensible defaults and key-confidence handling.

## Behavior defaults

- **Auto-trim**: ON — strips leading/trailing silence before processing.
- **Harmony volume**: `0.4` (natural blend; original lead stays dominant).
- **Key detection**: Krumhansl-Schmuckler auto. On low-confidence minor (<0.8), the tool auto-flips to the relative major because that consistently sounds better — when this happens, surface it to the user.
- **Harmony-only track**: NOT returned by default. Pass `--with-harmony-only` to also get the isolated harmony WAV.

## State variables produced and consumed

- `audio_url`: input — from positional arg
- `harmony_vol`: number — from `--harmony-vol` or default 0.4
- `key_override`: text or null — from `--key`
- `mixed_url`: produced by Step 2
- `harmony_only_url`: produced by Step 2 (only when `--with-harmony-only`)
- `detected_key`: text — produced by Step 2
- `key_confidence`: number — produced by Step 2
- `auto_flipped`: boolean — produced by Step 2

## Step 0 — Parse input

Required:
- Positional `audio_url` — MUST be `https://...`. Single voice or single instrument (monophonic). Reject `file://`, `MEDIA:`, attached paths — instruct the user to call `mcp__claude_ai_pika__upload_asset` first.

Optional:
- `--key "<root> <major|minor>"` — override auto-detected key. Examples: `"A minor"`, `"C major"`, `"Bb major"` (flat notation accepted, normalized to sharp internally).
- `--harmony-vol <0..1>` — harmony voice volume. Default `0.4`.
  - `0.25–0.35` → subtle background
  - `0.4` → natural blend (default)
  - `0.5–0.6` → strong harmony presence
  - `0.7+` → equal voice blend
- `--no-trim` — keep leading/trailing silence (default trims). Use when the audio's timing must match an external video or backing track.
- `--with-harmony-only` — also return the isolated harmony track (no original lead) for downstream mixing.

If `audio_url` missing, STOP and prompt the user for a vocal recording.

## Step 1 — Surface input expectations

Before calling the tool, briefly remind the user this works best on monophonic recordings (solo voice or single instrument). If they pasted a full song with backing instruments, warn that the result may be noisy and suggest extracting vocals first via `mcp__claude_ai_pika__edit_audio_separate`.

## Step 2 — Generate harmony (state: `mixed_url`, `harmony_only_url`, `detected_key`, `key_confidence`, `auto_flipped`)

Call `mcp__claude_ai_pika__generate_harmony` with:
- `audio_url` — `<audio_url>`
- `harmony_vol` — `<harmony_vol>`
- `key` — `<key_override>` if `--key` was supplied, else omit
- `trim` — `true` (default; `false` if `--no-trim`)
- `include_harmony_only_track` — `true` if `--with-harmony-only`, else `false`

Read response: `url` → `mixed_url`, `detected_key`, `key_confidence`, `auto_flipped_to_major` → `auto_flipped`. If `--with-harmony-only`, also `harmony_only_url`.

## Step 3 — Return

> Here's your harmonised audio: `<mixed_url>`
>
> Detected key: **`<detected_key>`** (confidence `<key_confidence>`)
>
> *(if `auto_flipped=true`)* I auto-flipped to the relative major because the minor detection was low-confidence — this usually sounds better. If you wanted the minor key, re-run with `--key "<root> minor"`.
>
> *(if `key_confidence < 0.7`)* Heads up — key detection confidence is low (`<0.7`). The harmony may sound off. Try re-running with an explicit `--key "<root> <major|minor>"` if you know the song's key.
>
> *(if `--with-harmony-only`)* Isolated harmony track: `<harmony_only_url>`

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Non-HTTPS URL | `file://`, `MEDIA:`, attached file | Instruct user to upload via `mcp__claude_ai_pika__upload_asset` first | None — STOP |
| Polyphonic input | Full mix with backing instruments | Warn before calling; suggest `mcp__claude_ai_pika__edit_audio_separate` first | Proceed at user's risk |
| Audio > 10min / > 100MB | Tool returns `InvalidInput` | Tell user the cap; suggest trimming or splitting | None |
| Low key confidence | `key_confidence < 0.7` | Surface in response (Step 3) | Suggest `--key` override |
| Decode failure | Tool returns `InvalidInput` ("could not decode audio_url") | Surface error; check URL accessibility + format | None |

## Parity notes (vs upstream auto-harmonise skill)

| Upstream feature | v1 status | Reason |
|---|---|---|
| Diatonic third above | retained — core algorithm | The signature blend (no phase resets, smooth +3/+4 transition). |
| Auto-flip minor → major on low confidence | retained — surfaced via `auto_flipped` field | Caller can prompt user to confirm. |
| Auto-trim ambience | retained — default ON | Matches upstream behavior; toggle with `--no-trim`. |
| Custom key override | retained — `--key` | Same syntax. |
| Harmony-only output | retained — `--with-harmony-only` flag | Default off (matches upstream "only surface mixed by default"). |
| Duet video mode (split-screen + lipsync) | separated → `/pika:duet` | Orchestration belongs in a sibling skill, not this one. |

## Compatibility

Primary target: Claude Code. Single MCP tool call; no platform-specific shell.
