---
name: language-swap
description: >
  Translate and dub a video into another language. One worker call preserves each speaker's
  voice, translates the speech, and returns a fully A/V-synced video. Lipsync ON by default.
  Use when the user says "translate this video", "dub this in <language>",
  "make this Spanish/French/Japanese", "translate the audio", or asks for
  bilingual subtitles on a dubbed/language-swap output.
  NOT for: subtitles/captions only (use add_captions or video-captions), transcription only
  (use transcribe_audio directly), or translating on-screen text overlays.
argument-hint: "<video-url> --to <language> [--no-lipsync] [--no-bgm] [--bilingual-subtitles]"
required-capabilities:
  - mcp__claude_ai_pika__upload_asset
  - mcp__plugin_pika_pika__dub_video
  - mcp__plugin_pika_pika__task_status
  - mcp__claude_ai_pika__extract_audio_from_video
  - mcp__claude_ai_pika__transcribe_audio
  - mcp__claude_ai_pika__edit_lipsync
  - mcp__claude_ai_pika__add_captions
---

<!-- source-of-truth: pika-claude-plugin/skills/language-swap -->

# /pika:language-swap

Translate and dub a video into another language while preserving the original speaker's voice. Pipeline: dub (one worker call) → lipsync (default ON) → burn target-language captions or bilingual captions.

The dubbing worker does the heavy lifting in a single call: it transcribes, translates, preserves each speaker's voice server-side (no separate clone step), and returns a fully A/V-synced video — so there is no manual transcribe/clone/TTS/replace chain to manage and no duration-drift handling to do by hand.

## Segmented / multi-language dub (per-range languages)

Use this when the user wants **different languages on different parts** of one video (e.g. first half Spanish, second half Japanese), or wants to **translate only some sections** and keep the rest in the original voice. Both are the same thing: a timeline of segments, each tagged with a language; any uncovered range keeps the original audio.

`mcp__plugin_pika_pika__dub_video` takes a `segments` plan **instead of** `target_language` (pass exactly one — they are mutually exclusive):

```
mcp__plugin_pika_pika__dub_video(source_video_url=<video_url>, segments=[
  {start_s: 0,  end_s: 30, target_language: "es"},
  {start_s: 30, end_s: 60, target_language: "ja"}
])
```

How to build the plan: the user needs to know *where* the content is before they can pick ranges, so **transcribe first** — extract the audio with `mcp__claude_ai_pika__extract_audio_from_video`, then `mcp__claude_ai_pika__transcribe_audio(audio=<audio_url>, timestamps=true)`, show the user the timestamped segments, and let them say which time range goes to which language. Then assemble `segments[]` (seconds, ordered, non-overlapping) and make ONE `dub_video` call. There is no separate "video understanding" tool — the timestamped transcript is the understanding step.

Behavior of the segmented path:
- **Shared voice across all segments.** The source speaker is cloned once and every segment — in every language — is spoken in that same cloned voice, then the clone is recycled, all inside the one `dub_video` call. You never clone or delete a voice yourself.
- **Keep-original.** Any time range NOT covered by a segment plays the original audio (voice + background) untouched. To translate only parts of a video, list only the parts you want translated.
- **Length-locked.** Output stays exactly the source length (each dubbed range is speed-fit to its window), so boundaries line up with the original timeline.
- **Provider.** Mixed-language-per-range always uses the voice-cloning route automatically; the single-call whole-video dubbing route can't mix languages per range, so don't force a single-call provider for a segmented plan. Every covered language must be supported on the voice-cloning route — if one isn't, surface the error and consult `references/language-coverage.md`.
- **Result.** Same dubbed-video result; `target_language` echoes the covered languages comma-joined (e.g. `"spa,jpn"`), and no single `transcript_language` is returned (the track is multi-language). Lipsync (Step 2, default ON, ≤5 min) still runs on the whole dubbed video. For captions (Step 3), use the returned multi-language `subtitles[]` in `caption_mode="manual"`; auto re-transcription can't pick a single language for a mixed track.

If `mcp__plugin_pika_pika__dub_video` rejects `segments` (older deployment without segmented support), fall back to dubbing each range single-language and concatenating — but prefer the one-call segmented path when available.

## Behavior defaults

- **Target language**: required via `--to <language>`. Prefer language codes: `es`, `fr`, `ja`, `de`, `pt-BR`, `zh-Hans`. The dubbing worker accepts ISO/BCP-47-like tags and normalizes script/region subtags before calling ElevenLabs (for example `zh-Hans` → `zh`; `zh-Hant-TW` → `zh`).
- **Lipsync**: ON by default — re-matches the speaker's mouth to the translated audio (fal sync-lipsync; the full-video lip-matcher, distinct from the portrait-image animator). Pass `--no-lipsync` to skip it when the source has no on-camera face or to avoid the meaningful cost (~$4/min on the sync-2-pro tier). **Applies only to videos ≤5 min** — `edit_lipsync` hard-caps at 300 s upstream, so longer sources auto-skip lipsync (see Step 2); the dub itself has no length limit.
- **BGM / background music**: kept by default — the dub lays the translated voice over the original music / SFX bed. Pass `--no-bgm` for a translate-only output: the worker drops the original music and keeps only the translated speech (`drop_background_audio=true`).
- **Captions**: target-language captions are burned by default. When the user asks for bilingual / dual subtitles, burn the target-language (translated) row on top and the source-language (original) row below it — after dubbing, the translated speech is what's actually being said, so it's the primary row; the original is the secondary reference.
- **Bilingual captions**: enable when the user passes `--bilingual-subtitles` or asks for "bilingual subtitles", "dual subtitles", "two-language captions", "original + translated subtitles", "双语字幕", or "原文+译文字幕".
- **Language coverage**: if language support is questioned or a language-related upstream error occurs, consult `references/language-coverage.md`. Do not proactively surface provider-specific language-list details in normal user replies.

## State variables produced and consumed

- `video_url`: input — from positional arg
- `source_input_url`: original positional URL — preserved for diagnostics if `video_url` is rehosted
- `target_language`: text — from `--to <language>`
- `with_lipsync`: boolean — defaults true; false only when `--no-lipsync`
- `no_bgm`: boolean — true when `--no-bgm` (maps to `drop_background_audio=true`)
- `bilingual_subtitles`: boolean — true when the user asks for bilingual / dual subtitles
- `dubbed_video_url`: dubbed, A/V-synced video — produced by Step 1
- `dub_subtitles`: optional target-language timed subtitles from the dub result — consumed by Step 3
- `source_subtitles`: optional source-language timed subtitles from the dub result — consumed by Step 3 for bilingual captions
- `dub_transcript_srt`: optional target-language SRT from the dub result — returned for review/debugging
- `source_transcript_srt`: optional source-language SRT from the dub result — returned for review/debugging
- `source_transcript_language`: optional source-language code from the dub result
- `lipsynced_video_url`: dubbed video with mouth re-matched — produced by Step 2 (when lipsync runs)
- `caption_target_video_url`: final visual video URL before captions are burned
- `final_video_url`: video with target-language captions burned in — produced by Step 3

## Step 0 — Parse input

Required:
- Positional `video_url` — MUST be `https://...`
- `--to <language>` — target language (free-text or BCP-47 code)

Optional:
- `--no-lipsync` — skip the default mouth-matching step.
- `--no-bgm` — translate-only output; drop the original music/SFX bed.
- `--bilingual-subtitles` — burn source-language + target-language subtitle rows.

Infer `bilingual_subtitles=true` from user wording even if the explicit flag is absent.

If `--to` is missing, STOP and prompt the user — UNLESS the user wants different languages on different parts, or to translate only some sections: that is the per-range segmented path (see "Segmented / multi-language dub" above), which uses a `segments` plan instead of `--to`.

For the segmented path, first build the time-range plan: extract the audio with `mcp__claude_ai_pika__extract_audio_from_video`, then transcribe it with timestamps via `mcp__claude_ai_pika__transcribe_audio(audio=<audio_url>, timestamps=true)`, show the user the timestamped segments, and capture which time range maps to which language into `segments[]`.

Outputs: `video_url`, `target_language`, `with_lipsync` (default true), `no_bgm` (default false), `bilingual_subtitles` (default false).

## Step 1 — Dub the video (state: `dubbed_video_url`)

Call `mcp__plugin_pika_pika__dub_video` with:
- `source_video_url` — `<video_url>`
- `target_language` — `<target_language>` (ISO/BCP-47-like tag, e.g. `es`, `pt-BR`, `zh-Hans`)
- `source_language` — `"auto"`
- `drop_background_audio` — `true` only when `no_bgm` is set; otherwise omit (keeps the original music bed)

In Claude plugin installs the tool is exposed as `mcp__plugin_pika_pika__dub_video`. If your host exposes the same Pika server under a different local namespace, call that fully-qualified local tool with the same arguments. The Claude.ai connector surface may lag this plugin-only tool, so do not assume the connector prefix has it.

`mcp__plugin_pika_pika__dub_video` is worker-backed: if the response comes back as `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status` until `completed`, then read the dubbed video from the result (`video_url` for a video source; `audio_url` for an audio source). Also capture optional `subtitles[]`, `transcript_srt`, and `transcript_language` — these are target-language transcript metadata the dub worker produced, consumed in Step 3.

For bilingual captions, also capture optional `source_subtitles[]`, `source_transcript_srt`, and `source_transcript_language`. These source-language transcript fields are best-effort. The dubbed media is still valid when transcript fields are absent.

**Source not worker-fetchable:** if `mcp__plugin_pika_pika__dub_video` fails because the source URL cannot be fetched — especially HTTP `403` / `4xx`, hotlink protection, UA-gated hosts (Wikimedia/news CDNs), or "Access Denied" errors — do **not** keep retrying the same call. Rehost first:

1. Download the source bytes in the client/host environment using a normal browser/download path or an HTTP client with a real user-agent.
2. Call `mcp__claude_ai_pika__upload_asset` with the downloaded filename, MIME type, and exact byte size, then upload the bytes to the returned presigned URL.
3. Set `source_input_url = <original URL>` and replace `video_url` with the returned Pika CDN `public_url`. Do not construct CDN URLs manually.
4. Retry Step 1 once against the Pika CDN URL. All later steps must use the updated `video_url`.

If the client/host also cannot download the source bytes, stop and tell the user the host blocks direct fetch; ask them to upload the file or provide a different URL.

Outputs: `dubbed_video_url`, `dub_subtitles`, `source_subtitles`, `dub_transcript_srt`, `source_transcript_srt`, `source_transcript_language`.

## Step 2 — Lipsync (state: `lipsynced_video_url`)

Default ON. Skip entirely when `--no-lipsync` is passed (then Step 3 captions `dubbed_video_url` directly).

**Hard 5-minute cap — check duration before calling.** `mcp__claude_ai_pika__edit_lipsync` enforces a **300-second (5-minute) audio limit** upstream (sync.so) and rejects anything longer with `invalid_input` before billing; every `variant` tier shares the same cap, so falling back through tiers does NOT help. If the dubbed video's `duration_seconds` (returned by Step 1) is **> 300**, skip lipsync entirely, go straight to Step 3 captioning `dubbed_video_url`, and tell the user lipsync isn't available past 5 minutes (the dub itself works at any length). Only run the lipsync call below when `duration_seconds ≤ 300`.

**Cost heads-up first.** Lipsync is the dominant cost (~$4/min on the v2-pro tier). Before calling it, estimate from the dubbed video's `duration_seconds` (returned by Step 1) — `ceil(duration_seconds / 60) × $4` — and send the user a one-line heads-up, e.g. "Lipsync on — ~2 min video, est. ~$8 (pass `--no-lipsync` to skip). Starting now." Then proceed straight into the call; this is a heads-up, not an approval gate.

Call `mcp__claude_ai_pika__edit_lipsync(video_url=<dubbed_video_url>)` with **no** `audio_url` — the worker syncs to the dubbed video's own embedded translated audio. Do not extract the audio just to feed it back in. (`variant` defaults to `v2-pro`, with `sync-3` / `v2` as fallbacks.)

Outputs: `lipsynced_video_url` (read from `url` of response). When this step runs, Step 3 captions **this** video, not `dubbed_video_url` — otherwise the lip-matching is dropped.

## Step 3 — Burn target-language captions (state: `final_video_url`)

Caption the final video so the output carries readable subtitles (matches the common "translate + subtitle" expectation). Set `caption_target_video_url` to `lipsynced_video_url` when lipsync ran (the default), or `dubbed_video_url` when `--no-lipsync` skipped it.

If this request is part of a Double video / split-screen comparison flow, build that Double video first and set `caption_target_video_url` to the final composed video URL. Do not burn captions onto only one panel before the Double video is composed; the bilingual caption burn should happen once, on the final visual output.

Call `mcp__claude_ai_pika__add_captions` once on `caption_target_video_url`.

When `bilingual_subtitles=true`, use manual bilingual mode if both tracks are available: call `mcp__claude_ai_pika__add_captions(video_url=<caption_target_video_url>, caption_mode="manual", subtitles=<dub_subtitles>, secondary_subtitles=<source_subtitles>, language=<target_language>, secondary_language=<source_transcript_language if available>, secondary_subtitles_position="below", style="branded-space-mono", position="bottom")`. The target-language (translated) row is the primary `subtitles` and renders on top; the source-language (original) row is the secondary reference and renders below it (`secondary_subtitles_position="below"`) — after dubbing the translated speech is what's actually spoken, so it leads. It works for every dub worker provider branch as long as `mcp__plugin_pika_pika__dub_video` returns both subtitle tracks.

If `bilingual_subtitles=true` but `source_subtitles` is missing, fall back to target-language captions only and tell the user the source transcript was unavailable from the dubbing provider. Do not invent a source-language row by retranscribing the final dubbed audio; that audio is already in the target language.

For target-language-only captions, prefer the target-language subtitles the dub worker already returned: if `dub_subtitles` is non-empty, call `mcp__claude_ai_pika__add_captions(video_url=<caption_target_video_url>, caption_mode="manual", subtitles=<dub_subtitles>, language=<target_language>, style="branded-space-mono", position="bottom")`. Manual mode skips a duplicate transcription pass and preserves the dubbing provider's target-language text.

If `dub_subtitles` is missing, empty, or rejected by `mcp__claude_ai_pika__add_captions`, fall back to auto: call `mcp__claude_ai_pika__add_captions(video_url=<caption_target_video_url>, caption_mode="auto", language=<target_language>, style="branded-space-mono", position="bottom")`. Auto mode re-transcribes the dubbed audio; use it only as the fallback because it costs extra time and can introduce CJK/proper-noun drift.

Use `style="branded-space-mono"` unless the user asks for a punchier style (`tiktok` / `hormozi` / `karaoke`). Skip this step only if the user explicitly asked for audio-only dubbing with no captions.

Outputs: `final_video_url` (read from `url` of response).

## Step 4 — Return

Reply with `final_video_url` + the translated transcript (from `dub_transcript_srt` / the dub result) for user review.

**Offer a bilingual-subtitle version.** When this run burned target-language-only captions (`bilingual_subtitles=false`) and a source transcript is available (`source_subtitles` is non-empty), close the reply by asking whether the user also wants a dual-subtitle version, e.g. "Want a bilingual version with the original + translated subtitles stacked? I can add it." If they say yes, re-run Step 3 in bilingual manual mode on the same `caption_target_video_url` (the pre-caption visual video) — no re-dub or re-lipsync is needed, only the caption burn changes — and return the new `final_video_url`. Skip the offer when bilingual captions were already burned (`bilingual_subtitles=true`), or when `source_subtitles` is missing — without a source transcript a bilingual version can't be produced (the dubbed audio is already in the target language), so do not offer what can't be delivered.

## Failure modes

| Class | Trigger | Mitigation | Fallback |
|---|---|---|---|
| Source URL not worker-fetchable | `mcp__plugin_pika_pika__dub_video` returns 403 / 4xx, hotlink / UA-gated fetch failure, or "Access Denied" for a public HTTPS URL | Download source bytes in the client/host environment, `mcp__claude_ai_pika__upload_asset` them to Pika, replace `video_url` with the Pika CDN URL, then retry Step 1 once | If local download also fails, ask the user to upload the file or provide a different URL |
| Extra target language | Target is Cantonese (`yue` / `cantonese` / `zh-HK`), Thai, Hebrew, Persian, Slovenian, Catalan, Norwegian Nynorsk, or Afrikaans | Supported — call `mcp__plugin_pika_pika__dub_video` with the target as usual; the original speaker's voice is kept | Background music isn't preserved for these languages (dubbed speech only) |
| Dub call fails (not fetchability) | `mcp__plugin_pika_pika__dub_video` errors for another reason — unsupported target language, provider/worker 5xx, `status: failed` from `mcp__plugin_pika_pika__task_status` | Surface the error to the user; if the message points at the language, check `references/language-coverage.md` and suggest a supported tag; otherwise suggest a retry. There is no manual chain to fall back to — dub is the single path | None — return the error, do not silently produce a non-dubbed video |
| Dub returns no speech | Silent video — nothing to translate | Surface to user: "no detectable speech in video — nothing to translate" | None |
| Original voice can't be kept | For the languages above, the source is too short or noisy to keep the original speaker's voice | Surface the error and ask the user for a cleaner / longer source clip | None — the dub fails rather than using a different voice |
| Lipsync source too long | Dubbed video >5 min — `mcp__claude_ai_pika__edit_lipsync` rejects with `invalid_input` (sync.so 300 s cap); all variant tiers share the cap so retrying won't help | Check `duration_seconds` from Step 1 first and skip lipsync when >300; caption `dubbed_video_url` directly and tell the user lipsync caps at 5 min | Dubbed video, no lip-match |
| Lipsync step fails | `mcp__claude_ai_pika__edit_lipsync` errors (no clear face track, provider 4xx) | Fall back through `variant` tiers (v2-pro → sync-3 → v2); if all fail, return the dubbed video without lip-matching and tell the user | Audio-replaced video, no lip-match |
| Captions wrong language | Step 3 auto-transcription mis-detects language | Pass explicit `language` tag; if `dub_subtitles` exists, use `caption_mode="manual"` with it instead of auto | Manual `subtitles[]` |
| Bilingual source row unavailable | User asked for bilingual subtitles but `source_subtitles` is absent | Use target-language captions and explain the source transcript was unavailable | Target-language captions only |

## Compatibility

Primary target: Claude Code. Uses standard MCP tools only. Works on Codex / Cursor / Claude Desktop.
