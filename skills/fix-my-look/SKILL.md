---
name: fix-my-look
description: >
  Change ANYTHING inside a video — background, scene, lighting, outfit, weather,
  mood — from a free-form prompt, while keeping the EXACT original facial
  identity, motion, speech, audio AND aspect ratio. Edits the first frame with
  gpt-image-2, then propagates that look across the clip with seedance
  reference-video using the original clip as the identity anchor. Triggers:
  "change anything in my video", "edit my video with a prompt", "change the
  background of this video", "change my outfit in this clip", "restyle this
  video without changing the person", "put me on a beach", "make this video at
  night", "/fix-my-look".
required-capabilities:
  - mcp__claude_ai_pika__upload_asset
  - mcp__claude_ai_pika__normalize_video
  - mcp__claude_ai_pika__generate_image
  - mcp__claude_ai_pika__generate_reference_video
  - mcp__claude_ai_pika__task_status
---

# fix-my-look

Edit the source's first usable frame with `gpt-image-2` from the user's prompt,
then propagate that look across the clip with `seedance` reference-video while
locking the original face, motion and audio via the original video + audio as
references. All prep happens in one `normalize_video` call. Aspect is preserved;
this skill does NOT reframe.

## Inputs

- `<source>` — path or URL to a video file with audio
- `<change_prompt>` — what to change (e.g. "make it night with neon lights",
  "change my shirt to a leather jacket", "put me on a beach in Hawaii")

## Empty-args menu

1. "What's the source video path?"
2. "What do you want to change? (e.g. 'put me on a beach', 'make it night')"

## Workflow

Working dir: `~/Downloads/fix-my-look/<run-id>/`.

### Step 1 — Prepare the clip

Local file? `mcp__claude_ai_pika__upload_asset` it first; an HTTPS media URL
passes directly. Call
`mcp__claude_ai_pika__normalize_video(video_url=<source>, max_duration_s=14.8, extract_audio=true, extract_face_frame=true)`.
For sources >15s where the user wants a window, also pass `start_s=<offset>`.

Wire the result into the rest: `face_frame_url` is the Step 2 edit target;
the normalized `video_url` + `audio_url` are seedance's references in Step 4;
`aspect_ratio` carries through both. Compute
`duration = max(4, min(15, round(duration_s)))`, and use `resolution="720p"`
unless the user asked for high res. If `face_found` is false, no clear face was
found and `face_frame_url` fell back to the t=0 frame — proceed but warn
identity may drift, or re-run with a `start_s` at a section where the subject
faces camera.

### Step 2 — Edit the frame with gpt-image-2 (the "change" stage)

`mcp__claude_ai_pika__generate_image` with `provider="gpt-image-2"`,
`aspect_ratio=<aspect_ratio>`, `reference_images=[<face_frame_url>]`,
`quality="high"`, prompt:

> "Modify the reference photograph as follows: `<change_prompt>`. Keep the
> person's face, identity, hair, body and pose EXACTLY as in the reference.
> CRITICAL: preserve every object the subject is holding or touching — phones,
> products, drinks, bags, props, jewelry — in the exact same hand, position,
> orientation and scale; never remove, replace or restyle them. Change only the
> requested scene, background, clothing, lighting or environment, not who the
> person is."

Keep the "preserve held objects" clause verbatim on every re-render — without
it gpt-image-2 silently drops products/phones the subject is holding.

### Step 3 — Show the edited frame and wait for approval

Surface the edited frame and STOP. Ask "Approve for video generation, or tweak
and re-render?" Do NOT call seedance until approved. For tweaks, re-run Step 2
(locked clauses verbatim) and loop.

### Step 4 — Propagate via seedance reference-video

`mcp__claude_ai_pika__generate_reference_video` with `provider="seedance"`,
`reference_videos=[<normalized video_url>]`, `reference_images=[<edited_frame_url>]`,
`reference_audio=[<audio_url>]`, `aspect_ratio=<aspect_ratio>`,
`duration=<duration>`, `resolution=<resolution>`, prompt:

> "Apply the change shown in @Image1 to @Video1. Keep the person in @Video1 with
> the EXACT same face, identity, expressions, speech, audio (synced to @Audio1),
> motion and timing; the new scene/background/clothing/lighting should match
> @Image1. CRITICAL: preserve every object the subject is holding or touching in
> @Video1 — phones, products, drinks, bags, props — in the same hand and
> orientation every frame, even if @Image1 omits it. Do not invent, drop or
> repeat any spoken words. Do not alter the person's identity."

Append any extra creative direction (e.g. "very cinematic, soft golden light")
after the locked text — never replace it.

Async fallback: if the call returns a `{task_id, status}` envelope, poll
`mcp__claude_ai_pika__task_status({task_id})` in a tight loop until terminal.

### Step 5 — Download + return

Download the result to `~/Downloads/fix-my-look/<run-id>/result.mp4` and return
that path.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Output face drifts from the original | gpt-image-2 over-edited the face AND seedance under-weighted @Video1 | Re-run Step 2 with a stronger "keep the face the same" clause; soften `change_prompt`. |
| Output looks like the original (no change) | Edited image too similar, OR you passed the raw frame not the edited output | Re-run Step 2 with a more dramatic prompt; confirm the edited frame URL. |
| Output aspect doesn't match source | Source aspect not in {16:9, 9:16, 1:1, 4:3, 3:4} | Step 1 snaps to the closest; for exotic aspects ask the user. |
