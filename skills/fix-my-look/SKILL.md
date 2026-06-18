---
name: fix-my-look
description: >
  Change ANYTHING inside a video — background, scene, lighting, outfit, weather,
  mood — from a free-form prompt, while keeping the EXACT original facial
  identity, motion, speech, audio AND closest supported output ratio. Edits the
  first frame with gpt-image-2, then propagates that look across the clip with
  Kling reference-video using the original clip as the identity anchor.
  Triggers:
  "change anything in my video", "edit my video with a prompt", "change the
  background of this video", "change my outfit in this clip", "restyle this
  video without changing the person", "put me on a beach", "make this video at
  night", "/fix-my-look".
required-capabilities:
  - mcp__plugin_pika_pika__upload_asset
  - mcp__plugin_pika_pika__normalize_video
  - mcp__plugin_pika_pika__estimate_cost
  - mcp__plugin_pika_pika__generate_image
  - mcp__plugin_pika_pika__generate_reference_video
  - mcp__plugin_pika_pika__edit_concat
  - mcp__plugin_pika_pika__extract_audio_from_video
  - mcp__plugin_pika_pika__edit_audio_replace
  - mcp__plugin_pika_pika__edit_lipsync
  - mcp__plugin_pika_pika__task_status
---

# fix-my-look

Edit the source's first usable frame with `gpt-image-2` from the user's prompt,
then propagate that look across the clip with `kling` reference-video while
locking the original face, motion and audio via the original video + audio as
references. All prep happens in one `mcp__plugin_pika_pika__normalize_video`
call for short clips, or one normalize call per segment for longer clips. The
output ratio uses the normalized clip's closest supported output ratio; this
skill does NOT reframe the source video.

## Inputs

- `<source>` — path or URL to a video file with audio
- `<change_prompt>` — what to change (e.g. "make it night with neon lights",
  "change my shirt to a leather jacket", "put me on a beach in Hawaii")

## Empty-args menu

1. "What's the source video path?"
2. "What do you want to change? (e.g. 'put me on a beach', 'make it night')"

## Workflow

Working dir: `~/Downloads/fix-my-look/<run-id>/`.

### Step 0 — Cost, timer and task IDs

Use the `mcp__plugin_pika_pika__*` names below as the canonical plugin
namespace. If the host exposes the same tools under a local namespace such as
`mcp__pika-mcp__*` or `mcp__pika-prod__*`, map by tool suffix and keep the same
arguments.

Start a timer when the source and change prompt are known. Before paid
generation, call `mcp__plugin_pika_pika__estimate_cost` for the planned
`mcp__plugin_pika_pika__generate_image`,
`mcp__plugin_pika_pika__generate_reference_video`, any multi-segment
`mcp__plugin_pika_pika__edit_concat`, and any optional audio/lipsync repair
call. If cost is not surfaced by the host, say
`Cost not surfaced by this harness` in the final report instead of guessing.
When any tool returns a
`task_id`, copy the exact value into the run notes and reuse it verbatim; do not
hand-type long JWT-style task IDs.

### Step 1 — Prepare the clip

Local file? `mcp__plugin_pika_pika__upload_asset` it first; an HTTPS media URL
passes directly. Decide the source windows before normalizing: use one 14.8s
window for sources <=15s, and split longer sources into ordered 14.8s windows.
Call
`mcp__plugin_pika_pika__normalize_video(video_url=<source>, start_s=<offset>, max_duration_s=14.8, extract_audio=true, extract_face_frame=true)`
once per window. Use the first window's `face_frame_url` for the edited still;
use each window's `video_url` as that segment's motion/identity reference. For
multi-window clips, also call
`mcp__plugin_pika_pika__extract_audio_from_video(video_url=<source>)` so the
final merged output can be restored to one continuous source audio track.

Wire the result into the rest: `face_frame_url` is the Step 2 edit target;
each normalized `video_url` is Kling's reference for that segment in Step 4;
set `aspect_ratio = result.aspect_ratio ?? result.closest_aspect_ratio` for
each normalize result, then carry that local `aspect_ratio` through the image
and video calls. If neither field is present, stop and report that normalization
output is missing an aspect label. Compute
`duration = max(4, min(15, round(duration_s)))` per segment, and use
`resolution="720p"`
unless the user asked for high res. If `face_found` is false, no clear face was
found and `face_frame_url` fell back to the t=0 frame — proceed but warn
identity may drift, or re-run with a `start_s` at a section where the subject
faces camera.

Reference-video providers can reject oversized reference assets. If the
normalize result or the downstream provider error shows a normalized video is
over the provider limit, retry `mcp__plugin_pika_pika__normalize_video` once
with `crf=28` and the same `start_s`, `max_duration_s`, `extract_audio`, and
`extract_face_frame` values. If the reference is still too large, stop before
another paid video attempt and report that
`mcp__plugin_pika_pika__normalize_video` needs a worker-side 1080-edge /
reference-size cap. Do not patch this with local shell media commands.

### Step 2 — Edit the frame with gpt-image-2 (the "change" stage)

`mcp__plugin_pika_pika__generate_image` with `provider="gpt-image-2"`,
`aspect_ratio=<aspect_ratio>`, `resolution="2K"`,
`reference_images=[<face_frame_url>]`, `quality="high"`, prompt:

> "Modify the reference photograph as follows: `<change_prompt>`. Keep the
> person's face, identity, hair, body and pose EXACTLY as in the reference.
> CRITICAL: preserve every object the subject is holding or touching — phones,
> products, drinks, bags, props, jewelry — in the exact same hand, position,
> orientation and scale; never remove, replace or restyle them. Change only the
> requested scene, background, clothing, lighting or environment, not who the
> person is."

Keep the "preserve held objects" clause verbatim on every re-render — without
it gpt-image-2 silently drops products/phones the subject is holding.

If gpt-image-2 returns a content-policy false positive for fashion, glam, or
beauty prompts, retry once with the same intent but a modest / editorial wording
such as "polished event styling, opaque clothing, natural pose, non-sexual
fashion portrait". For makeup prompts, explicitly preserve the original eye
shape, eyelids, iris color and gaze; heavy eyeliner/eye shadow is a high-risk
identity-drift source.

### Step 3 — Show the edited frame and wait for approval

Surface the edited frame and STOP. Ask "Approve for video generation, or tweak
and re-render?" Do NOT call video generation until approved. For tweaks, re-run Step 2
(locked clauses verbatim) and loop.

### Step 4 — Propagate via Kling reference-video

For each normalized segment, call `mcp__plugin_pika_pika__generate_reference_video`
with `provider="kling"`, `reference_videos=[<segment video_url>]`,
`reference_images=[<edited_frame_url>]`, `aspect_ratio=<aspect_ratio>`,
`duration=<segment duration>`, `sound=false`, `video_keep_sounds=[true]`,
prompt:

> "Apply the change shown in <<<image_1>>> to <<<video_1>>>. Keep the person in
> <<<video_1>>> with the EXACT same face, identity, expressions, motion and
> timing; preserve the original video's kept sound track. The new
> scene/background/clothing/lighting should match <<<image_1>>>. CRITICAL:
> preserve every object the subject is holding or touching in <<<video_1>>> —
> phones, products, drinks, bags, props — in the same hand and orientation every
> frame. Keep mouth motion active through the final frame when the person is
> speaking. Do not alter the person's identity."

Append any extra creative direction (e.g. "very cinematic, soft golden light")
after the locked text — never replace it.

Do not pass `sound=true` to Kling with a video input. Kling rejects that
combination with `error:1201 sound on is not supported with video input`; use
`sound=false` plus `video_keep_sounds=[true]` to keep the source video's audio.

If the source was split into multiple windows, call
`mcp__plugin_pika_pika__edit_concat(video_urls=[<segment outputs in order>])`.
After concat, run
`mcp__plugin_pika_pika__edit_audio_replace(video_url=<concat_url>, audio_url=<full_source_audio_url>, duration_policy="video")`
when the merged output audio is missing, drifted, or discontinuous.

Only try Seedance if the user explicitly asks for it, or if Kling fails and a
second provider attempt is useful. Use the same segmenting rule and record the
provider error plainly if Seedance rejects the input or drops speech/action.

Async handling: if any call returns a `{task_id, status}` envelope, poll
`mcp__plugin_pika_pika__task_status({task_id})` in a tight loop until terminal.

### Step 5 — Audio, duration and identity QA

Before reporting success, verify the generated video against the source:

- Duration must not be meaningfully cut off. If output duration differs from the
  intended source window or merged source duration by more than 0.5s, mark the
  run as failed / needs follow-up.
- If the source has speech, audio must be present through the tail and mouth
  movement must not freeze before the spoken content ends. If words are missing,
  garbled, silent, or visibly out of sync, do not call the run `PASS`.
- The approved frame corrections must persist into the video. If the provider
  reintroduces a removed artifact such as eyeglass glare, mark it as a
  propagation caveat or re-render from a stronger approved frame.
- Compare identity at start, middle, segment boundaries, and end. If Kling
  preserved motion but changed the face, call that out as a provider limitation
  instead of a pass.

If the video is visually acceptable but speech audio is missing, incomplete, or
drifted, offer one paid repair pass:

1. `mcp__plugin_pika_pika__edit_audio_replace(video_url=<generated_video_url>, audio_url=<full_source_audio_url or segment_audio_url>, duration_policy="video")`
2. `mcp__plugin_pika_pika__edit_lipsync(video_url=<audio_restored_url>, audio_url=<full_source_audio_url or segment_audio_url>, variant="v2-pro")`

If the model froze the mouth near the end, do not keep escalating to `sync-3`
automatically; lip-sync cannot reliably recover a face track with no mouth motion.
Offer trim / regenerate instead.

### Step 6 — Download + return

Download the result to `~/Downloads/fix-my-look/<run-id>/result.mp4` and return
that path plus the final report fields: source, edited frame URL, final video
URL, provider, job/task IDs, cost estimate or `not surfaced`, elapsed
time, QA notes, and follow-up issue.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Output face drifts from the original | gpt-image-2 over-edited the face OR the provider under-weighted the source video | Re-run Step 2 with a stronger "keep the face the same" clause; soften `change_prompt`. |
| Output looks like the original (no change) | Edited image too similar, OR you passed the raw frame not the edited output | Re-run Step 2 with a more dramatic prompt; confirm the edited frame URL. |
| Output aspect doesn't match source | Source aspect not in {16:9, 9:16, 1:1, 4:3, 3:4} | Step 1 returns `aspect_ratio`, or `closest_aspect_ratio` on older worker payloads; use it as the closest supported output label and ask the user for exotic aspects. |
| Provider rejects the normalized video as too large | normalize output can remain too large for 4K/iPhone sources | Retry normalize once with `crf=28`; if still too large, stop and file worker follow-up for a 1080-edge / reference-size cap. |
| Long source only returns the first short window | The caller normalized once with `max_duration_s=14.8` and skipped segmenting | Split into 14.8s windows, generate each segment, then `mcp__plugin_pika_pika__edit_concat` in order and restore full source audio if needed. |
| Speaking clip loses sound, drops words, or freezes mouth at the tail | Provider regenerated speech/audio instead of preserving the source, or the face track has no mouth motion to drive | Mark as not pass. Offer one `mcp__plugin_pika_pika__edit_audio_replace` + `mcp__plugin_pika_pika__edit_lipsync` repair pass; if tail mouth motion is frozen, offer trim/regenerate instead. |
| Approved frame fix disappears in the video | Provider propagation reintroduced the original artifact | Re-render from a stronger approved frame or mark provider propagation caveat; do not claim the frame correction shipped. |
| Kling rejects with `error:1201 sound on is not supported with video input` | `sound=true` was passed with a video reference | Retry the Kling call with `sound=false` and `video_keep_sounds=[true]`; do not use `reference_audio` for Kling video input. |
| Kling output is shorter than the normalized source | Provider returned a shorter render, or the caller accidentally passed a trimmed reference | Do not mark pass. Compare output duration to the normalized source, then regenerate that segment or ask the user for a shorter window. |
