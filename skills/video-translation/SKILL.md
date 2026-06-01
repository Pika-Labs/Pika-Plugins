---
name: video-translation
description: >
  Translate and dub a video into another language. Extracts audio, transcribes, translates,
  clones the speaker's voice, generates TTS in the target language, and replaces the
  original audio track. Optional lipsync. Use when the user says "translate this video",
  "dub this in <language>", "make this Spanish/French/Japanese", "translate the audio".
  NOT for: subtitles/captions (use add_captions or video-captions), transcription only
  (use transcribe_audio directly), or translating on-screen text overlays.
argument-hint: "<video-url> --to <language> [--with-lipsync] [--no-bgm]"
required-capabilities:
  - mcp__claude_ai_pika__upload_asset
  - mcp__claude_ai_pika__extract_audio_from_video
  - mcp__claude_ai_pika__transcribe_audio
  - mcp__claude_ai_pika__clone_voice
  - mcp__claude_ai_pika__generate_speech
  - mcp__claude_ai_pika__edit_audio_replace
  - mcp__claude_ai_pika__edit_audio_stitch
  - mcp__claude_ai_pika__add_captions
  - mcp__claude_ai_pika__edit_lipsync
---

<!-- source-of-truth: pika-claude-plugin/skills/video-translation -->

# /pika:video-translation

Translate and dub a video into another language using the original speaker's cloned voice. Pipeline: extract audio → transcribe → translate (in-prose) → clone voice → TTS in target language → replace audio track → burn target-language captions (optional lipsync).

## Fast path — one-shot dub (preferred when available)

`mcp__claude_ai_pika__generate_speech` with `mode=dub` translates AND dubs a video in a single worker call. It preserves each speaker's voice server-side (no separate clone step), keeps the original background music / SFX bed under the translated voice, and returns a fully A/V-synced **video** — so it also avoids the duration-drift handling the manual chain needs. It collapses manual Steps 1–6 into one call:

```
generate_speech(mode="dub", provider="elevenlabs",
                source_video_url=<video_url>, target_language=<iso>,
                source_language="auto")
```

`mode=dub` is worker-backed: if the response comes back as `{task_id, status}`, poll `task_status` until `completed`, then read the dubbed video from the result (`video_url` for a video source). For `--with-lipsync`, extract the audio from the dubbed video and run `mcp__claude_ai_pika__edit_lipsync` on it; then Step 7 captions.

**Try the fast path first.** Fall back to the manual chain below when: `mode=dub` returns an output-validation error (dub support may not be live on that deployment yet), the caller needs the intermediate transcript/translation for review, the caller wants a **translate-only** result with no background music (the manual chain drops the original track — see Behavior defaults), or finer per-step control is required. The manual chain is fully documented below as the fallback.

## Behavior defaults

- **Default target language**: required via `--to <language>`. Examples: `Spanish`, `French`, `Japanese`, `zh-Hans`, `de`, `pt-BR`.
- **Lipsync**: OFF by default. Enable with `--with-lipsync` to re-match the speaker's mouth to the translated audio via `mcp__claude_ai_pika__edit_lipsync` (fal sync-lipsync — takes a full video + the new audio track; it is the full-video lip-matcher, distinct from the portrait-image animator). Cost is meaningful (~$8/min on the sync-3 tier), which is why it's opt-in.
- **BGM / background music**: depends on the path. The **fast-path dub preserves** the original music / SFX bed under the translated voice by default. The **manual chain is translate-only** — Step 6 (`mcp__claude_ai_pika__edit_audio_replace`) replaces the whole original track, dropping background music and SFX. So: default (keep BGM) → prefer the fast path; `--no-bgm` (translate-only, no music) → run the manual chain, which is already BGM-free.
- **70+ languages supported** via the underlying TTS providers (ElevenLabs default).

## State variables produced and consumed

- `video_url`: input — from positional arg
- `source_input_url`: original positional URL — preserved for diagnostics if `video_url` is rehosted
- `target_language`: text — from `--to <language>`
- `original_audio_url`: extracted from video — produced by Step 1
- `transcript`: text (with timestamps) — produced by Step 2
- `translated_transcript`: text in target language — produced by Step 3 (in-prose translation)
- `cloned_voice_id`: ElevenLabs voice ID — produced by Step 4
- `translated_audio_url`: TTS output — produced by Step 5
- `dubbed_video_url`: video with original audio replaced by translated track — produced by Step 6
- `final_video_url`: dubbed video with target-language captions burned in — produced by Step 7

## Step 0 — Parse input

Required:
- Positional `video_url` — MUST be `https://...`
- `--to <language>` — target language (free-text or BCP-47 code)

Optional:
- `--with-lipsync` — re-match the mouth to the translated audio via `mcp__claude_ai_pika__edit_lipsync` (full-video lip-sync; see Step 6)
- `--no-bgm` — translate-only output with no background music. Routes to the manual chain (Step 6 replaces the whole track, so it's BGM-free). Without this flag, the fast-path dub keeps the original music bed.

If `--to` is missing, STOP and prompt the user.

Outputs: `video_url`, `target_language`, `with_lipsync` (boolean), `no_bgm` (boolean — when true, route to the manual chain for a translate-only result; see Behavior defaults).

## Step 1 — Extract audio (state: `original_audio_url`)

Call `mcp__claude_ai_pika__extract_audio_from_video(video_url=<video_url>)`.

If Step 1 fails because the source URL is not worker-fetchable — especially HTTP `403` / `4xx`, hotlink protection, UA-gated hosts such as Wikimedia/news CDNs, or "Access Denied" fetch errors — do **not** keep retrying the same worker call. Rehost the source first:

1. Download the source bytes from the original URL in the client/host environment using a normal browser/download path or an HTTP client with a real user-agent. This covers reachable public files that the worker cannot fetch directly.
2. Call `mcp__claude_ai_pika__upload_asset` with the downloaded filename, MIME type, and exact byte size, then upload the bytes to the returned presigned URL.
3. Set `source_input_url = <original URL>` and replace `video_url` with the returned Pika CDN `public_url`. Do not construct CDN URLs manually.
4. Retry Step 1 against the Pika CDN URL exactly once. All later steps, including Step 6 audio replacement and optional lipsync/captions, must use the updated `video_url` so the pipeline stays on worker-fetchable media.

If the client/host environment also cannot download the source bytes, stop and tell the user the host blocks direct fetch; ask them to upload the file or provide a different URL.

Outputs: `original_audio_url` (read from `url` of response).

## Step 2 — Transcribe (state: `transcript`)

Call `mcp__claude_ai_pika__transcribe_audio(audio=<original_audio_url>, timestamps=true)`.

Read the transcript text + timestamps from the response (`text` + `segments[]` per manifest). (Manifest canonical param names: `audio` not `audio_url`, `timestamps` not `with_timestamps`.)

Outputs: `transcript` (structured: `{text, segments: [{start, end, text}]}`).

## Step 3 — Translate (state: `translated_transcript`)

**Prose-only** — the executing agent translates the transcript into `target_language` directly. Preserve segment timestamps. Output structure:

```
translated_transcript = {
  text: <full translated text>,
  segments: [{start: <orig>, end: <orig>, text: <translated>}, ...]
}
```

The agent should preserve the speaker's tone and idioms appropriate to the target culture; not just literal word-for-word translation.

## Step 4 — Clone voice (state: `cloned_voice_id`)

Call `mcp__claude_ai_pika__clone_voice` with:
- `action` — `"clone"` (manifest enum: `clone | design | list | get | delete`)
- `voice_url` — `<original_audio_url>` (NOT `audio_url`; manifest param is `voice_url`)
- `voice_name` — `"tr_<short-hash>"` (keep under 20 chars per the `mcp__claude_ai_pika__clone_voice` schema cap; NOT `name`)
- `provider` — `"elevenlabs"` (default; aligns with Step 5 TTS provider)

Read the `voice_id` from the response.

**Clone normally** and only take the fallback below on a genuine error — do NOT skip cloning preemptively, or the dub won't match the speaker. (An earlier ElevenLabs `400 ... v1/voices/add: "Unsupported Model"` clone failure has since been resolved.)

**Fallback when clone fails** — do NOT fall through to the agent's own persona voice (that makes the dub sound like the agent, not the speaker). Instead pass an explicit preset `voice_id` in Step 5 that matches the speaker's apparent gender/age (inferred from the transcript / video). Do NOT just omit `voice_id` — the provider default is a fixed voice (ElevenLabs defaults to "Rachel", female), so omitting it mismatches gender for a male speaker. Surface to the user that the original voice could not be cloned.

Outputs: `cloned_voice_id` (or the fallback preset voice id).

## Step 5 — Generate translated TTS (state: `translated_audio_url`)

Call `mcp__claude_ai_pika__generate_speech` with:
- `text` — `translated_transcript.text` (the full translated body). **Cap: 10000 chars.** If the translated text exceeds 10k, split it on segment boundaries, synthesize each chunk separately, then join the chunk audios back-to-back in order with `mcp__claude_ai_pika__edit_audio_stitch` (it takes timed `clips` with `start_s`/`end_s` — lay the chunks end to end; this is the audio stitcher, not the video-concat tool). The stitched track feeds Step 6. A single oversized `text` hard-fails the call.
- `voice_id` — `cloned_voice_id` (from Step 4 — MUST be an ElevenLabs voice ID since Step 4 cloned via ElevenLabs)
- `provider` — `"elevenlabs"` (aligns with the clone provider; cross-provider voice IDs don't work)
- `language` — target-language BCP-47 tag (e.g. `es`). (For `text_to_speech` mode the param is `language`; `target_language` is only for `mode=dub`.)
- `expected_duration_s` — the source video duration (optional), so the response returns `drift_seconds` / `drift_pct`. If you don't have the duration handy, omit it — drift reporting is just skipped.

**Duration drift is expected**: target languages like Spanish run ~20–35% longer than English, so the TTS will usually overrun the source. Read `drift_pct` from the response. If the audio is longer than the video, Step 6 handles it via `duration_policy` (freeze-frame pad). Only re-synthesize at a faster pace if drift is extreme (>40%) or the user needs a hard length match.

Outputs: `translated_audio_url` (read from the response `audio_url`; for the >10k chunked path, use the stitched track's `url` instead), `drift_pct`.

## Step 6 — Replace the audio track (state: `dubbed_video_url`)

Call `mcp__claude_ai_pika__edit_audio_replace` with:
- `video_url` — `<video_url>`
- `audio_url` — `<translated_audio_url>`
- `duration_policy` — set to `audio` when the translated track is longer than the source: this freeze-frame-pads the video to the full audio length so no dubbed speech is cut off. (The tool's own default is `video`, which would trim the dub to the source length — not what we want here, so pass `audio` explicitly.) Use `video` only if the caller requires the output to stay exactly the source length (trailing audio is then trimmed).

This **replaces** the original audio (discards the English track) — no audio bleed. This supersedes the old audio-overlay-mix approach (which left the original audio audible underneath; the prior overlay limitation is now resolved by `mcp__claude_ai_pika__edit_audio_replace`).

Outputs: `dubbed_video_url` (read from `url` of response).

If `--with-lipsync`: after the dubbed video exists, call `mcp__claude_ai_pika__edit_lipsync(video_url=<dubbed_video_url>, audio_url=<translated_audio_url>)` to re-match the speaker's mouth to the translated track (fal sync-lipsync; `variant` defaults to `sync-3`, with `v2` / `v2-pro` as cheaper fallbacks). This consumes the dubbed video from Step 6 and the translated audio from Step 5. (Use the full-video lip-sync tool above, not the portrait-image animator.)

Outputs: `lipsynced_video_url` (read from `url` of response). When this step runs, Step 7 captions **this** video, not `dubbed_video_url` — otherwise the opted-in lip-matching is dropped.

## Step 7 — Burn target-language captions (state: `final_video_url`)

Call `mcp__claude_ai_pika__add_captions` on the final video so the output carries readable target-language captions (matches the common "translate + subtitle" expectation):
- `video_url` — `<lipsynced_video_url>` when `--with-lipsync` ran, otherwise `<dubbed_video_url>` (caption the most-processed video so lip-matching isn't lost)
- `language` — target-language tag (e.g. `es`); this transcribes the freshly-dubbed audio so caption timings align with the translated voice.
- `style` — `classic` (clean bottom subtitle bar) unless the user asks for a punchier style (`tiktok` / `hormozi` / `karaoke`).

Auto mode (no `subtitle_text`) re-transcribes the dubbed audio, which gives correct word-level timing for the target-language track — more reliable than reusing the source English timestamps, which no longer match after TTS drift.

Skip this step only if the user explicitly asked for audio-only dubbing with no captions.

Outputs: `final_video_url` (read from `url` of response).

## Step 8 — Return

Reply with `final_video_url` + the translated transcript text for user review.

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Audio extraction fails | Non-fetchability Step 1 worker error, such as invalid media, unsupported container, missing audio track, or repeated extraction failure after any rehost retry | Surface error to user; can't proceed without audio. For 403 / 4xx hotlink or Access Denied fetch failures, use the source-rehost row below | None |
| Source URL not worker-fetchable | Step 1 returns 403 / 4xx, hotlink / UA-gated fetch failure, or "Access Denied" for a public HTTPS video URL | Download source bytes in the client/host environment, `mcp__claude_ai_pika__upload_asset` them to Pika, replace `video_url` with the Pika CDN URL, then retry Step 1 once against the Pika CDN URL | If local download also fails, ask the user to upload the file or provide a different URL |
| Transcription returns empty | Step 2 returns no text (silent video) | Surface to user: "no detectable speech in video — nothing to translate" | None |
| Translation contains untranslated terms | Step 3 agent produces incomplete translation | Self-review: re-run translation with prompt to translate ALL non-proper-noun text | None — agent retries inline |
| Voice clone fails | Step 4: `Unsupported Model` OR audio < ~5s | Skip clone; pass an explicit preset `voice_id` matching the speaker's gender/age (NOT the agent's persona voice, and do NOT omit `voice_id` — the provider default is a fixed female voice, see Step 4); tell the user the original voice couldn't be cloned | Gender-matched preset voice |
| TTS exceeds video duration | translated audio longer than original (normal for ES/FR/etc.) | Step 6 `duration_policy=audio` freeze-frame-pads the video to fit; only re-synthesize faster if drift >40% or a hard length match is required | Freeze-frame pad |
| Captions wrong language | Step 7 auto-transcription mis-detects language | Pass explicit `language` tag; if still wrong, fall back to manual mode with the translated segments from Step 3, mapping each `{start, end}` to `mcp__claude_ai_pika__add_captions`'s `{start_s, end_s}` field names | Manual `subtitles[]` |
| Lipsync step fails | `mcp__claude_ai_pika__edit_lipsync` errors (e.g. no clear face track, provider 4xx) | Fall back through `variant` tiers (sync-3 → v2-pro → v2); if all fail, return the dubbed video without lip-matching and tell the user | Audio-replaced video, no lip-match |

## Parity notes (v1 simplifications)

| Hub-skill feature | v1 status | Reason |
|---|---|---|
| Whisper → Deepgram → Gemini transcription waterfall | partial → `mcp__claude_ai_pika__transcribe_audio` | Plugin uses single MCP tool; provider waterfall happens worker-side. |
| LLM-based translation (direct Anthropic call) | dropped → in-prose | Executing agent translates directly; no separate LLM call. |
| Per-segment time-aligned TTS generation | partial | v1 generates a single TTS for the full translated text; per-segment alignment for precise lip-matching deferred. v1.5 may use `segment_align.py`-equivalent logic. |
| Demucs vocal isolation for BGM preservation | retained via the fast path | The dub fast path preserves the original music bed server-side, so no separate vocal-isolation step is needed. The manual-chain fallback stays translate-only (drops BGM). |
| fal sync-3 lipsync on full videos | retained → `mcp__claude_ai_pika__edit_lipsync` | The full-video lip-sync primitive (fal sync-lipsync) shipped; `--with-lipsync` calls it. (The portrait-image animator is a separate tool.) |
| Audio replacement (no original-audio bleed) | retained → `mcp__claude_ai_pika__edit_audio_replace` | Earlier v1 used an audio-overlay mix (original audio audible). Now uses `mcp__claude_ai_pika__edit_audio_replace` for a clean track swap. |
| Target-language captions | added → `mcp__claude_ai_pika__add_captions` | v1 had no caption step; Step 7 now burns target-language subtitles (auto-transcribed from the dubbed audio). |
| BCP-47 language code normalization | partial | v1 passes `--to` value through to `mcp__claude_ai_pika__generate_speech`'s `language` param; worker handles normalization. |
| 70+ language coverage | retained | Via ElevenLabs (default) — same upstream as hub-skill. |

## Compatibility

Primary target: Claude Code. Uses standard MCP tools only. Works on Codex / Cursor / Claude Desktop.
