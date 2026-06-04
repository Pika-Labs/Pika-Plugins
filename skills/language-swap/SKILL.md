---
name: language-swap
description: >
  Translate and dub a video into another language. One worker call preserves each speaker's
  voice, translates the speech, and returns a fully A/V-synced video. Lipsync ON by default.
  Use when the user says "translate this video", "dub this in <language>",
  "make this Spanish/French/Japanese", "translate the audio".
  NOT for: subtitles/captions only (use add_captions or video-captions), transcription only
  (use transcribe_audio directly), or translating on-screen text overlays.
argument-hint: "<video-url> --to <language> [--no-lipsync] [--no-bgm]"
required-capabilities:
  - mcp__claude_ai_pika__upload_asset
  - mcp__plugin_pika_pika__dub_video
  - mcp__plugin_pika_pika__task_status
  - mcp__claude_ai_pika__edit_lipsync
  - mcp__claude_ai_pika__add_captions
---

<!-- source-of-truth: pika-claude-plugin/skills/language-swap -->

# /pika:language-swap

Translate and dub a video into another language while preserving the original speaker's voice. Pipeline: dub (one worker call) → lipsync (default ON) → burn target-language captions.

The dubbing worker does the heavy lifting in a single call: it transcribes, translates, preserves each speaker's voice server-side (no separate clone step), and returns a fully A/V-synced video — so there is no manual transcribe/clone/TTS/replace chain to manage and no duration-drift handling to do by hand.

## Behavior defaults

- **Target language**: required via `--to <language>`. Prefer language codes: `es`, `fr`, `ja`, `de`, `pt-BR`, `zh-Hans`. The dubbing worker accepts ISO/BCP-47-like tags and normalizes script/region subtags before calling ElevenLabs (for example `zh-Hans` → `zh`; `zh-Hant-TW` → `zh`).
- **Lipsync**: ON by default — re-matches the speaker's mouth to the translated audio (fal sync-lipsync; the full-video lip-matcher, distinct from the portrait-image animator). Pass `--no-lipsync` to skip it when the source has no on-camera face or to avoid the meaningful cost (~$4/min on the sync-2-pro tier).
- **BGM / background music**: kept by default — the dub lays the translated voice over the original music / SFX bed. Pass `--no-bgm` for a translate-only output: the worker drops the original music and keeps only the translated speech (`drop_background_audio=true`).
- **Language coverage**: if language support is questioned or a language-related upstream error occurs, consult `references/language-coverage.md`. Do not proactively surface provider-specific language-list details in normal user replies.

## State variables produced and consumed

- `video_url`: input — from positional arg
- `source_input_url`: original positional URL — preserved for diagnostics if `video_url` is rehosted
- `target_language`: text — from `--to <language>`
- `with_lipsync`: boolean — defaults true; false only when `--no-lipsync`
- `no_bgm`: boolean — true when `--no-bgm` (maps to `drop_background_audio=true`)
- `dubbed_video_url`: dubbed, A/V-synced video — produced by Step 1
- `dub_subtitles`: optional target-language timed subtitles from the dub result — consumed by Step 3
- `dub_transcript_srt`: optional target-language SRT from the dub result — returned for review/debugging
- `lipsynced_video_url`: dubbed video with mouth re-matched — produced by Step 2 (when lipsync runs)
- `final_video_url`: video with target-language captions burned in — produced by Step 3

## Step 0 — Parse input

Required:
- Positional `video_url` — MUST be `https://...`
- `--to <language>` — target language (free-text or BCP-47 code)

Optional:
- `--no-lipsync` — skip the default mouth-matching step.
- `--no-bgm` — translate-only output; drop the original music/SFX bed.

If `--to` is missing, STOP and prompt the user.

Outputs: `video_url`, `target_language`, `with_lipsync` (default true), `no_bgm` (default false).

## Step 1 — Dub the video (state: `dubbed_video_url`)

Call `mcp__plugin_pika_pika__dub_video` with:
- `source_video_url` — `<video_url>`
- `target_language` — `<target_language>` (ISO/BCP-47-like tag, e.g. `es`, `pt-BR`, `zh-Hans`)
- `source_language` — `"auto"`
- `drop_background_audio` — `true` only when `no_bgm` is set; otherwise omit (keeps the original music bed)

In Claude plugin installs the tool is exposed as `mcp__plugin_pika_pika__dub_video`. If your host exposes the same Pika server under a different local namespace, call that fully-qualified local tool with the same arguments. The Claude.ai connector surface may lag this plugin-only tool, so do not assume the connector prefix has it.

`mcp__plugin_pika_pika__dub_video` is worker-backed: if the response comes back as `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status` until `completed`, then read the dubbed video from the result (`video_url` for a video source; `audio_url` for an audio source). Also capture optional `subtitles[]`, `transcript_srt`, and `transcript_language` — these are target-language transcript metadata the dub worker produced, consumed in Step 3.

**Source not worker-fetchable:** if `mcp__plugin_pika_pika__dub_video` fails because the source URL cannot be fetched — especially HTTP `403` / `4xx`, hotlink protection, UA-gated hosts (Wikimedia/news CDNs), or "Access Denied" errors — do **not** keep retrying the same call. Rehost first:

1. Download the source bytes in the client/host environment using a normal browser/download path or an HTTP client with a real user-agent.
2. Call `mcp__claude_ai_pika__upload_asset` with the downloaded filename, MIME type, and exact byte size, then upload the bytes to the returned presigned URL.
3. Set `source_input_url = <original URL>` and replace `video_url` with the returned Pika CDN `public_url`. Do not construct CDN URLs manually.
4. Retry Step 1 once against the Pika CDN URL. All later steps must use the updated `video_url`.

If the client/host also cannot download the source bytes, stop and tell the user the host blocks direct fetch; ask them to upload the file or provide a different URL.

Outputs: `dubbed_video_url`, `dub_subtitles`, `dub_transcript_srt`.

## Step 2 — Lipsync (state: `lipsynced_video_url`)

Default ON. Skip entirely when `--no-lipsync` is passed (then Step 3 captions `dubbed_video_url` directly).

**Cost heads-up first.** Lipsync is the dominant cost (~$4/min on the v2-pro tier). Before calling it, estimate from the dubbed video's `duration_seconds` (returned by Step 1) — `ceil(duration_seconds / 60) × $4` — and send the user a one-line heads-up, e.g. "Lipsync on — ~2 min video, est. ~$8 (pass `--no-lipsync` to skip). Starting now." Then proceed straight into the call; this is a heads-up, not an approval gate.

Call `mcp__claude_ai_pika__edit_lipsync(video_url=<dubbed_video_url>)` with **no** `audio_url` — the worker syncs to the dubbed video's own embedded translated audio. Do not extract the audio just to feed it back in. (`variant` defaults to `v2-pro`, with `sync-3` / `v2` as fallbacks.)

Outputs: `lipsynced_video_url` (read from `url` of response). When this step runs, Step 3 captions **this** video, not `dubbed_video_url` — otherwise the lip-matching is dropped.

## Step 3 — Burn target-language captions (state: `final_video_url`)

Caption the final video so the output carries readable target-language captions (matches the common "translate + subtitle" expectation). The target video is `lipsynced_video_url` when lipsync ran (the default), or `dubbed_video_url` when `--no-lipsync` skipped it.

Prefer the target-language subtitles the dub worker already returned: if `dub_subtitles` is non-empty, call `mcp__claude_ai_pika__add_captions(video_url=<final_pre_caption_video>, caption_mode="manual", subtitles=<dub_subtitles>, language=<target_language>, style="classic")`. Manual mode skips a duplicate transcription pass and preserves the dubbing provider's target-language text.

If `dub_subtitles` is missing, empty, or rejected by `mcp__claude_ai_pika__add_captions`, fall back to auto: call `mcp__claude_ai_pika__add_captions(video_url=<final_pre_caption_video>, caption_mode="auto", language=<target_language>, style="classic")`. Auto mode re-transcribes the dubbed audio; use it only as the fallback because it costs extra time and can introduce CJK/proper-noun drift.

Use `style="classic"` (clean bottom subtitle bar) unless the user asks for a punchier style (`tiktok` / `hormozi` / `karaoke`). Skip this step only if the user explicitly asked for audio-only dubbing with no captions.

Outputs: `final_video_url` (read from `url` of response).

## Step 4 — Return

Reply with `final_video_url` + the translated transcript (from `dub_transcript_srt` / the dub result) for user review.

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Source URL not worker-fetchable | `mcp__plugin_pika_pika__dub_video` returns 403 / 4xx, hotlink / UA-gated fetch failure, or "Access Denied" for a public HTTPS URL | Download source bytes in the client/host environment, `mcp__claude_ai_pika__upload_asset` them to Pika, replace `video_url` with the Pika CDN URL, then retry Step 1 once | If local download also fails, ask the user to upload the file or provide a different URL |
| Extra target language | Target is Cantonese (`yue` / `cantonese` / `zh-HK`), Thai, Hebrew, Persian, Slovenian, Catalan, Norwegian Nynorsk, or Afrikaans | Supported — call `mcp__plugin_pika_pika__dub_video` with the target as usual; the original speaker's voice is kept | Background music isn't preserved for these languages (dubbed speech only) |
| Dub call fails (not fetchability) | `mcp__plugin_pika_pika__dub_video` errors for another reason — unsupported target language, provider/worker 5xx, `status: failed` from `mcp__plugin_pika_pika__task_status` | Surface the error to the user; if the message points at the language, check `references/language-coverage.md` and suggest a supported tag; otherwise suggest a retry. There is no manual chain to fall back to — dub is the single path | None — return the error, do not silently produce a non-dubbed video |
| Dub returns no speech | Silent video — nothing to translate | Surface to user: "no detectable speech in video — nothing to translate" | None |
| Original voice can't be kept | For the languages above, the source is too short or noisy to keep the original speaker's voice | Surface the error and ask the user for a cleaner / longer source clip | None — the dub fails rather than using a different voice |
| Lipsync step fails | `mcp__claude_ai_pika__edit_lipsync` errors (no clear face track, provider 4xx) | Fall back through `variant` tiers (v2-pro → sync-3 → v2); if all fail, return the dubbed video without lip-matching and tell the user | Audio-replaced video, no lip-match |
| Captions wrong language | Step 3 auto-transcription mis-detects language | Pass explicit `language` tag; if `dub_subtitles` exists, use `caption_mode="manual"` with it instead of auto | Manual `subtitles[]` |

## Compatibility

Primary target: Claude Code. Uses standard MCP tools only. Works on Codex / Cursor / Claude Desktop.
