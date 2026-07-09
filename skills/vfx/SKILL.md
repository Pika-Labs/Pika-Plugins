---
name: vfx
description: >-
  Turn a plain video clip into a cinematic AI-VFX shot at 1080p by default
  (or 4K / 720p on request). Give Claude a video and the change you want; it
  reads EVERY frame via local contact sheets and understands the audio,
  writes a Seedance-faithful prompt that locks your face, gestures, and
  camera move, then re-renders the same shot with the VFX baked in via
  Seedance reference-to-video.
argument-hint: "[the VFX change you want, e.g. 'turn the plaza into an open desert on a finger snap'] [--resolution 720p|1080p|4k, default 1080p]"
required-capabilities:
  - upload_asset
  - probe_media
  - analyze_media
  - transcribe_audio
  - estimate_cost
  - generate_reference_video
  - task_status
---

# vfx

Maps a video-to-video VFX move onto the Pika MCP's **Seedance reference-to-video**, at **1080p by default** (bump to 4K, or drop to 720p, only if the user asks). The user hands you a clip + the change they want; you **read EVERY frame** (locally extracted with ffmpeg and tiled into contact sheets) **and understand the audio** (speech + music + SFX + ambience), author a Seedance-faithful prompt that locks the original (face, gestures, camera move) and time-codes the change to the right beat, then re-render the **same shot** with the VFX baked in. **One run produces one clip** for one requested change.

> For a 4K-only version of this skill with no resolution choice, see `/pika:4k-vfx`.

## How it works — why reading EVERY frame (and the audio) is the mechanism (do not skip the reading pass)
Seedance treats the reference video as a **motion/style anchor, NOT a pixel-locked base** — it does not copy the input frame-for-frame, it re-generates the shot guided by your prompt. So fidelity comes from the **PROMPT**: the more exhaustively the prompt describes the original (subject identity, exact gestures, camera move, framing, lighting, palette, wardrobe) **and the audio** (dialogue + lip-sync, music/SFX beats), the more the output reads as the *same* shot with the change layered on, at any resolution. **Reading EVERY frame — not a sample — is how you build that exhaustive description:** you locally extract all frames with ffmpeg, tile them 25-to-a-contact-sheet (5×5), and analyze every sheet so the prompt is built from the *entire* timeline rather than a handful of stills. Skip the read (or read only a sample) and the output drifts — a different face, a different camera move, a different room, a missed motion beat. The reading pass — all frames + the audio — IS the skill.

## Prerequisites
pika MCP available, and **local `ffmpeg`** in the run environment (used to extract every frame and build the contact sheets). Two inputs from the user: **(1) a video clip** (a local file or a public URL) and **(2) the VFX change** they want made to it. A third input is optional: **(3) a resolution** — defaults to 1080p if not specified. Tools used: `upload_asset`, `probe_media`, `analyze_media`, `transcribe_audio`, `estimate_cost`, `generate_reference_video`, `task_status` (frame extraction + tiling is done locally with ffmpeg, not an MCP tool).

## Stage 0 — Gather inputs (settle this first)
You need exactly two things before generating, plus one implicit default:
1. **The video** — the original clip to transform. If they gave a local file, you will upload it (Step 1); if they gave a public URL, keep it.
2. **The change / VFX** — what should be different in the output (e.g. "turn the plaza into an open desert on a finger snap", "make it snow", "set the room on fire behind me", "morph my jacket into glowing armor").
3. **The resolution (`state.resolution`)** — default to **`1080p`** unless the user's request says otherwise. Look for explicit signals: "4K", "highest quality", "max resolution" → `state.resolution = "4k"`; "720p", "cheaper", "faster", "lower res is fine" → `state.resolution = "720p"`. Absent any signal, stay at `1080p` — do not ask "which resolution do you want?", just default silently and let the Step-6 gate surface the choice for confirmation. Set `state.seedance_model` from `state.resolution` right away, since Step 6 quotes it: **`standard`** for `1080p` or `4k` (`fast`/`mini` cap at 720p — REQUIRED), **`fast`** for `720p` (cheaper, faster, and sufficient at that resolution).

If **either video or change** is missing, ask for it before doing anything else — do not invent a change, and do not proceed on a clip you cannot reach. Once both are in hand, say in one line what you're about to do ("Reading every frame of your clip to build the desert-on-snap 1080p prompt…") and run Steps 1–5 without further check-ins — but **stop at the Step 6 agreement gate before generating**: the render is the expensive, irreversible step, and it only fires after the user approves the prompt, resolution, and cost.

## Step 1 — Upload the clip (`upload_asset`)
Real video must be uploaded — inline base64 only works for tiny assets (<~3MB), so any actual clip goes through the presigned-upload path.

1. Call `upload_asset` with `filename`, `mime_type` (`video/mp4` for mp4), and `size_bytes` (the file's byte size).
2. PUT the raw bytes to the returned `presigned_url`.
3. Keep the returned `public_url` → `state.clip_url`.

If the user already gave a **public URL**, skip this step and set `state.clip_url` to it.

## Step 2 — Probe (`probe_media`)
Call `probe_media` on `state.clip_url` to read **duration, fps, dimensions, and aspect ratio**. Use these to: (a) sanity-check the all-frame extraction in Step 3 (duration × fps ≈ total frame count ≈ 25 × number of sheets), and (b) choose the output `aspect_ratio` and `duration` here, matched to the source — the Step-6 gate quotes this choice (plus `state.resolution` from Stage 0) to the user and Step 7 fires with it.

## Step 3 — Extract EVERY frame locally and tile into contact sheets (ffmpeg)
Read the **whole** video, not a sample. Use local ffmpeg to extract **every** frame at the source rate (no drops, no exceptions), then tile them into legible contact sheets at **25 frames per sheet (5×5 grid)** so each `analyze_media` call covers 25 consecutive frames at once.

Work in a **relative** working directory (do not use an absolute system temp path):

```
mkdir -p frames sheets
ffmpeg -i INPUT -vsync 0 frames/f_%05d.png            # every frame, no drops
```

Then build the 25-per-sheet contact sheets (5×5), scaling each frame down so the sheet is legible and stamping the frame index onto each tile:

```
ffmpeg -i INPUT -vf "scale=480:-1,drawtext=text='%{n}':x=4:y=4:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.5,tile=5x5" sheets/sheet_%03d.png
```

`drawtext=text='%{n}'` stamps the frame index on each tile so the analysis can reference exact frames; `tile=5x5` groups 25 consecutive frames per sheet. If `drawtext` is unavailable in the local ffmpeg build, fall back to plain `scale=480:-1,tile=5x5`. `INPUT` is the local clip (or a local copy of the URL). Confirm the sheet count lines up with the probe in Step 2 — **every frame must land on a sheet, no exceptions.**

## Step 4 — Read EVERY sheet + understand the audio (`upload_asset`, `analyze_media`, `transcribe_audio`)
This is the fidelity step, and it has two mandatory halves: **read all the frames** and **understand the audio**. Neither is optional.

### 4a — Read all the frames (every sheet)
For **each** contact sheet from Step 3 (cover ALL of them — every frame is on a sheet, no exceptions): upload it with `upload_asset` (the sheets are images, so upload to get a URL), then call `analyze_media` on that sheet URL with a `query` that reads the **full progression across those 25 frames** — pulling out everything the prompt must lock:
- **Subject / identity** — who/what is in frame; face, hair, build, distinguishing features.
- **Exact motion & gestures** — what the subject does, beat by beat, referencing the stamped frame indices (e.g. "raises right hand around frame 0048, snaps fingers around frame 0072").
- **Camera move** — static / pan / push-in / handheld / orbit, and its timing.
- **Framing** — shot size (close/medium/wide), subject position, headroom.
- **Lighting** — direction, hardness, color temperature, time of day.
- **Palette** — dominant colors, mood.
- **Wardrobe / props / setting** — clothing, objects, background.

Carry the read across **all** sheets so the **entire timeline** is understood start-to-end, not just a sampled middle.

### 4b — Understand the audio (mandatory, not just speech)
Always read the audio — it is required, not optional. Two passes:
- `transcribe_audio` for **speech + timestamps** (the words and when they're said), so the prompt can preserve dialogue and lip-sync beats.
- `analyze_media` on the audio (or the video URL) to understand the **NON-speech audio too** — music, sound effects, ambience, tone, and rhythm/beats.

Fold the audio understanding into the prompt where it matters — preserve dialogue + lip-sync if anyone speaks, and **time the VFX change to an audio beat / sound cue** when the change should land on the music or a sound (e.g. snap, hit, downbeat) rather than a bare timestamp.

Assemble the all-frame read **and** the audio read into a single faithful description of the original — that description is the raw material for Step 5.

## Step 5 — Write the Seedance prompt (the authoring step, NEVER skip it)
Compose ONE prompt = **a faithful, exhaustive description of the original** (the locked elements) **+ the user's requested change, time-coded** + a reference to the input clip via the **`@Video1`** token. Be thorough: every detail you read in Step 4 that you omit is a detail Seedance is free to change.

**Template — fill the `[SLOTS]` from your Step-4 read (`[RESOLUTION LABEL]` = `4K` / `1080p` / `720p` matching `state.resolution`):**

```
Re-render this exact shot @Video1 in cinematic [RESOLUTION LABEL]. LOCK the original: [SUBJECT/IDENTITY — face, hair, build, wardrobe], performing [EXACT GESTURES, beat by beat]. Keep the SAME camera move ([CAMERA: static / pan / push-in / handheld], [timing]), the SAME framing ([SHOT SIZE + subject position]), the SAME lighting ([direction, hardness, color temp, time of day]) and the SAME palette ([dominant colors / mood]). CHANGE: [the VFX], time-coded — at [t0]–[t1]s [what the scene looks like before the change], then at [t2]s [the change triggers / VFX appears] and [how the scene reads after]. Everything not described by the change stays identical to @Video1. Photorealistic, high detail, consistent identity throughout.
```

Time-code the change so Seedance knows *when* it happens relative to the locked motion (e.g. "at 0–3s the plaza is unchanged as the subject raises their hand; at 3s on the finger snap the plaza dissolves into an open desert, sand and heat-haze replacing the buildings while the subject, camera move, and framing stay identical"). The stronger and more specific the time-coded change clause, the less Seedance ignores it.

## Step 6 — Agreement gate (`estimate_cost`) — MANDATORY before generating
The render is the expensive step, and once fired it can't be un-spent. **Never call `generate_reference_video` without explicit user approval in this session.** Present, in one message:

1. **The full Step-5 prompt** — verbatim, so the user can catch a wrong detail (face, gesture, timing) before it costs money.
2. **The generation recipe** — provider `seedance`, model `state.seedance_model`, resolution `state.resolution` (state plainly that this is `1080p` unless the user asked for something else), plus the `aspect_ratio` and `duration` you chose from the Step-2 probe.
3. **The estimated cost** — call `estimate_cost` for the Step-7 `generate_reference_video` call and quote the result. If the estimate errors, say the cost is unknown and flag that 4K is the top-price tier if that's what's selected — do not silently skip the number.

Then **wait**. Three outcomes:
- **Approve** → proceed to Step 7 unchanged.
- **Revise** — the user corrects a detail, the change clause, or the resolution → update the Step-5 prompt (re-reading specific sheets if the correction demands it) and re-present the gate.
- **Abort / no answer** → do not generate. Never treat silence as approval.

Only skip this gate if the user **explicitly pre-authorized the spend in this session** ("just run it, don't ask", a standing instruction to render without confirmation). Having provided the clip and the change is NOT pre-authorization — that's just Stage 0 input.

## Step 7 — Generate (Seedance reference-to-video) (`generate_reference_video`)
Call `generate_reference_video` with the recipe matched to `state.resolution`:
- `provider`: **`seedance`**
- `seedance_model`: **`state.seedance_model`** — set back in Stage 0 (`standard` for `1080p`/`4k`, REQUIRED since `fast`/`mini` cap at 720p; `fast` for `720p`).
- `resolution`: **`state.resolution`** — `1080p` unless Stage 0 / the Step-6 gate settled on `4k` or `720p`.
- `reference_videos`: **`[state.clip_url]`** — the original footage as the motion/style anchor (Seedance accepts up to 3 videos).
- `reference_images`: optional — style/creature/identity anchors (e.g. a generated reference image), only if you have one.
- `prompt`: the Step-5 prompt (uses the **`@Video1`** token to reference the input clip; no max length, so be exhaustive).
- `aspect_ratio`: **`auto`** (or match the source from Step 2).
- `duration`: matched to the source, OR set `auto_duration`: **`true`**.

**Do NOT pass `negative_prompt`** (not supported on seedance — the call is rejected) and **do NOT pass any fps param** (it doesn't exist).

## Step 8 — Deliver
If the call returns inline, you have the video URL. If it returns `{ task_id, status: running/background }`, poll `task_status(task_id)` in a tight loop until `completed` / `failed` / `cancelled`. On completion, return the **video URL** to the user. Note: the output CDN may be egress-blocked for in-session download — so deliver the URL itself rather than trying to fetch the bytes locally.

## Failure modes
| symptom | cause → fix |
|---|---|
| Clip too long / too large | Upload still works for large files; if Seedance rejects on duration, trim the source to the segment that matters, or set `auto_duration: true` and match a shorter `duration`. |
| No face / subject found in the read | A sheet may not show the subject clearly — re-run `analyze_media` on the specific sheet(s) covering the frames where the subject is visible (use the stamped frame indices), or rebuild the sheets without downscaling so detail is preserved. Do NOT drop to a sampled extraction — every frame stays on a sheet. |
| ffmpeg missing / `drawtext` unavailable | The run environment needs local `ffmpeg`; if the build lacks the `drawtext` filter, fall back to plain `scale=480:-1,tile=5x5` (sheets without stamped indices — still read every frame). |
| Identity / shot drift (different face, room, or camera move in the output) | The prompt description was not exhaustive enough. Go back to Step 4–5 and add the missing locked details (more on face, gestures, camera move, lighting) from the contact-sheet read — Seedance only preserves what the prompt names. Re-render = new spend: re-pass the Step-6 gate with the revised prompt before firing again. |
| Requested resolution rejected / output downgraded | `seedance_model` must be `standard` for `1080p` or `4k` — `fast`/`mini` silently cap at 720p. If the wrong-param call already completed (and was charged), the corrected call is a second render — re-pass the Step-6 gate before re-firing; if the call was rejected outright (nothing charged), re-fire the corrected call under the original approval. |
| Speech / audio not preserved or change off-beat | Run BOTH `transcribe_audio` (speech + timing) and `analyze_media` on the audio (music/SFX/ambience), then describe the dialogue + lip-movement beats and pin the time-coded change to the right audio cue/beat in the prompt so the re-render stays in sync. |
| Seedance ignores the requested change | Strengthen the time-coded change clause in Step 5 — make it more specific and explicitly time-anchored ("at Ns the change triggers"). The revised prompt is a new, never-approved prompt and the re-render is new spend: re-pass the Step-6 gate before firing again. |
| Job fails after a long run | If it ran several minutes before failing, the content already cleared the safety pass — the failure is infrastructural; re-fire the same call (the user's Step-6 approval covers retrying the identical, already-approved call — no need to re-gate). |

## One-liner recap
Extract EVERY frame locally with ffmpeg → tile into 25-per-sheet (5×5) contact sheets and analyze every sheet → understand the audio (transcribe speech + analyze music/SFX/ambience) → write an exhaustive Seedance-faithful prompt that locks the original and time-codes the change to the right audio beat → **agreement gate: show the prompt + recipe (resolution 1080p by default, 4K/720p on request) + `estimate_cost` and wait for approval** → re-render the same shot via `generate_reference_video` (`seedance`, model matched to resolution, original as `reference_videos`, `@Video1` in the prompt, no `negative_prompt`).
