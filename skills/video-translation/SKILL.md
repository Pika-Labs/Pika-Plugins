---
name: video-translation
description: >
  Translate and dub a video into another language. Extracts audio, transcribes, translates,
  clones the speaker's voice, generates TTS in the target language, and replaces the
  original audio track. Optional lipsync. Use when the user says "translate this video",
  "dub this in <language>", "make this Spanish/French/Japanese", "translate the audio".
  NOT for: subtitles/captions (use add_captions or video-captions), transcription only
  (use transcribe_audio directly), or translating on-screen text overlays.
argument-hint: "<video-url> --to <language> [--with-lipsync] [--preserve-bgm]"
required-capabilities:
  - mcp__claude_ai_pika__extract_audio_from_video
  - mcp__claude_ai_pika__transcribe_audio
  - mcp__claude_ai_pika__clone_voice
  - mcp__claude_ai_pika__generate_speech
  - mcp__claude_ai_pika__edit_audio_mix
  - mcp__claude_ai_pika__generate_lipsync
---

<!-- source-of-truth: pika-claude-plugin/skills/video-translation -->

# /pika:video-translation

Translate and dub a video into another language using the original speaker's cloned voice. Pipeline: extract audio → transcribe → translate (in-prose) → clone voice → TTS in target language → mix back to video (optional lipsync).

## Behavior defaults

- **Default target language**: required via `--to <language>`. Examples: `Spanish`, `French`, `Japanese`, `zh-Hans`, `de`, `pt-BR`.
- **Lipsync**: OFF by default (skips `mcp__claude_ai_pika__generate_lipsync`). Enable with `--with-lipsync`. v1 limitation: lipsync only works for talking-head shots (`generate_lipsync` takes portrait image, not video — see Parity notes).
- **BGM preservation**: ON by default — agent attempts to extract music/SFX track via vocal isolation. Disable with `--no-bgm` (translate-only, no music).
- **70+ languages supported** via the underlying TTS providers (ElevenLabs default).

## State variables produced and consumed

- `video_url`: input — from positional arg
- `target_language`: text — from `--to <language>`
- `original_audio_url`: extracted from video — produced by Step 1
- `transcript`: text (with timestamps) — produced by Step 2
- `translated_transcript`: text in target language — produced by Step 3 (in-prose translation)
- `cloned_voice_id`: ElevenLabs voice ID — produced by Step 4
- `translated_audio_url`: TTS output — produced by Step 5
- `final_video_url`: video with translated audio mixed — produced by Step 6

## Step 0 — Parse input

Required:
- Positional `video_url` — MUST be `https://...`
- `--to <language>` — target language (free-text or BCP-47 code)

Optional:
- `--with-lipsync` — enable lipsync on talking-head shots (see Parity for limitations)
- `--no-bgm` — disable BGM preservation (cleaner translation-only output)

If `--to` is missing, STOP and prompt the user.

Outputs: `video_url`, `target_language`, `with_lipsync` (boolean), `preserve_bgm` (boolean, default true).

## Step 1 — Extract audio (state: `original_audio_url`)

Call `mcp__claude_ai_pika__extract_audio_from_video(video_url=<video_url>)`.

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
- `voice_name` — `"tr_<short-hash>"` (keep under 16 chars to avoid upstream length limits; NOT `name`)
- `provider` — `"elevenlabs"` (default; aligns with Step 5 TTS provider)

Read the `voice_id` from the response.

Outputs: `cloned_voice_id`.

## Step 5 — Generate translated TTS (state: `translated_audio_url`)

Call `mcp__claude_ai_pika__generate_speech` with:
- `text` — `translated_transcript.text` (the full translated body)
- `voice_id` — `cloned_voice_id` (from Step 4 — MUST be an ElevenLabs voice ID since Step 4 cloned via ElevenLabs)
- `provider` — `"elevenlabs"` (aligns with the clone provider; cross-provider voice IDs don't work)
- `target_language` — `<target_language>` (manifest param is `target_language`, NOT `language`)

Outputs: `translated_audio_url` (read from response `url` field per manifest output schema).

## Step 6 — Mix back into video (state: `final_video_url`)

Call `mcp__claude_ai_pika__edit_audio_mix(video_url=<video_url>, audio_url=<translated_audio_url>, audio_volume=1.0)`.

**Known v1 limitation — original audio not removed AND cannot dominate**: per manifest, `mcp__claude_ai_pika__edit_audio_mix` OVERLAYS the new track at `audio_volume` (range 0-1; max 1.0). The original video audio stays at native volume underneath the translated voice — both will be audible. v1 ships with this caveat:

- For users who don't mind layered audio, the translated voice is clearly understandable at `audio_volume=1.0`
- For cleanest replacement, the user should mute or duck the original video audio BEFORE piping into this skill
- A worker-side `replace_audio` MCP primitive (or an `audio_mode=replace` extension to `mcp__claude_ai_pika__edit_audio_mix`) would solve this cleanly.

If `--with-lipsync`: this is currently NOT supported on full videos via `mcp__claude_ai_pika__generate_lipsync` (which takes a portrait image only). Surface to user: "lipsync on full videos isn't supported in v1; the translated audio overlays the original at high volume without lip-matching".

Outputs: `final_video_url` (read from `url` of response).

## Step 7 — Return

Reply with `final_video_url` + the translated transcript text for user review.

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Audio extraction fails | Step 1 worker error | Surface error to user; can't proceed without audio | None |
| Transcription returns empty | Step 2 returns no text (silent video) | Surface to user: "no detectable speech in video — nothing to translate" | None |
| Translation contains untranslated terms | Step 3 agent produces incomplete translation | Self-review: re-run translation with prompt to translate ALL non-proper-noun text | None — agent retries inline |
| Voice clone too short | Step 4 fails (audio < 10s needed for clone) | Fall back to a default voice in target language (skip Step 4, pick a `mcp__claude_ai_pika__generate_speech` preset matching gender/age from transcript metadata) | Generic TTS voice |
| TTS exceeds video duration | translated audio longer than original | Surface warning; trim TTS to original duration OR pad video to TTS duration (user choice) | User decision |
| Lipsync requested but unsupported | --with-lipsync flag set | Surface message: "lipsync not supported on full videos in v1; output uses audio replacement only" | Continue with audio-only translation |

## Parity notes (v1 simplifications)

| Hub-skill feature | v1 status | Reason |
|---|---|---|
| Whisper → Deepgram → Gemini transcription waterfall | partial → `mcp__claude_ai_pika__transcribe_audio` | Plugin uses single MCP tool; provider waterfall happens worker-side. |
| LLM-based translation (direct Anthropic call) | dropped → in-prose | Executing agent translates directly; no separate LLM call. |
| Per-segment time-aligned TTS generation | partial | v1 generates a single TTS for the full translated text; per-segment alignment for precise lip-matching deferred. v1.5 may use `segment_align.py`-equivalent logic. |
| Demucs vocal isolation for BGM preservation | dropped | No MCP tool for vocal isolation. v1 surfaces original audio URL so user can manually mix BGM if needed. |
| fal sync-3 lipsync on full videos | dropped | `mcp__claude_ai_pika__generate_lipsync` takes portrait image only. Full-video lipsync deferred to v1.5 (would need a new MCP primitive). |
| BCP-47 language code normalization | partial | v1 passes `--to` value through to `mcp__claude_ai_pika__generate_speech`'s `language` param; worker handles normalization. |
| 70+ language coverage | retained | Via ElevenLabs (default) — same upstream as hub-skill. |

## Compatibility

Primary target: Claude Code. Uses standard MCP tools only. Works on Codex / Cursor / Claude Desktop.
