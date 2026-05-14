---
name: baseball-trend
description: >
  Viral fake "ESPN behind-home-plate broadcast cutaway" of a user — broadcast-style still
  + 15s Kling-omni clip with native two-announcer commentary that names the user. Fixed
  trend: Yankees vs Red Sox ALCS Game 3 at Fenway Park, premium seats, scorebug + chyron
  with the user's name. Triggers: "make me a behind-home-plate cutaway", "fake MLB
  broadcast of me", "AI ESPN baseball crowd shot", "viral MLB broadcast trend",
  "Yankees Red Sox cutaway with me". Needs the user's name + one reference photo.
argument-hint: <username> <photo-url-or-path>
---

# baseball-trend

A two-call pika pipeline: ESPN broadcast still (`gpt-image-2`) → 15-second behind-home-plate cutaway with two-announcer commentary (`kling-v3-omni`, first-frame-locked to the still). The trend look is calibrated — substitute the user's name and keep everything else as written. Step 1 and Step 2 prompts are scaffolds: required elements + verbatim anchor phrases; write the connective prose yourself.

## Prerequisites

pika MCP available in the host. Tool name prefix varies by mount point — use whatever the host exposes. Tools needed: `upload_asset`, `generate_image`, `generate_reference_video`, `task_status`.

## Stage 0 — Intake

Ask the user for two things, both required: their **name** (will appear in the lower-third chyron and announcer dialogue) and a **reference photo** (front-facing 3/4 portrait, good lighting, one face; local file or https URL). For a local file, use the MCP upload tool to get a public URL. On Claude Desktop, pasted inline images don't reach MCP — ask for a URL or a `.zip` attachment instead.

Confirm back in one line ("Generating behind-home-plate cutaway for **{username}**…") and start. **No further yes/no gates after this point** — the pipeline runs end-to-end.

## Step 1 — Broadcast still (`generate_image`, gpt-image-2)

Compose a prompt that frames the output as a live ESPN MLB broadcast frame of a fan in premium seats behind home plate. The chyron + scorebug get baked into the still at frame 0 — load-bearing, so Kling treats them as pixel-locked burned-in UI in Step 2 instead of animating them mid-clip.

The prompt must contain:

- **Frame type** (verbatim opener): `A screenshot from a live MLB game TV broadcast on ESPN.` Then describe broadcast color grading, slight compression artifacts, interlacing grain, telephoto broadcast camera feel — like a real TV screenshot, not a clean photo.
- **Framing (verbatim)**: `The camera cuts to the audience` — to find our reference image person in the crowd. (This crowd-cutaway framing primitive is load-bearing; without it gpt-image-2 sometimes composes a player-action shot.)
- **Camera position (verbatim, load-bearing)**: `Camera is positioned in the foul-ground photographers' pit just past home plate, low angle, shooting BACK at the premium seats — the baseball field is BEHIND the camera and NOT visible anywhere in the frame.` Only the subject, surrounding fans (also facing camera, because they're facing the field which is where the camera is), and the seat / dugout-wall / backstop-netting backdrop should appear. **If grass or infield dirt shows up behind the subject, the camera angle is inverted (camera ended up in the upper deck looking toward the field instead of in the pit looking at the crowd) — re-roll Step 1.**
- **Subject position**: premium field-level seats **behind home plate** at **Fenway Park**, smiling naturally, unaware they're on camera.
- **Matchup** (verbatim names): **New York Yankees vs Boston Red Sox**, **MLB American League Championship Series (ALCS), Game 3**, Boston home stadium (Fenway Park), Yankees lead 2-0 in the ALCS so far.
- **Broadcast overlay** — frame this block with imperative emphasis (verbatim header): `CRITICAL — broadcast graphics that MUST be visible in this image:` All three must look like real burned-in broadcast UI, not Photoshop overlays:
  1. ESPN-style bottom scorebug — Yankees vs Red Sox with team logos, inning, outs, balls/strikes count, score, small runners-on-base diamond.
  2. Lower-third chyron in the **lower-left area, directly above the scorebug**, reading exactly `${username}` (the username **alone** — no suffix like "- AI Creator"; the trend illusion depends on it reading like a real broadcast identifier). Set in a **classic ESPN sans-serif**, in the **network's color treatment**, like a real broadcast identifier for the on-camera guest.
  3. ESPN network logo watermark in a corner.
- **Identity hardlock** (verbatim phrases): `Hardlock: Do not alter their facial structure and maintain their likeness` and `The subject must match the reference person`.

**Call params:**

- `provider`: `gpt-image-2`
- `reference_images`: `[<user's photo URL>]`
- `aspect_ratio`: `16:9`
- `quality`: `medium` *(don't pass `high` — exceeds the proxy 180s timeout and returns 502)*
- `output_format`: `png`

Save the returned URL — it's the first frame for Step 2.

**Agent-side self-check before Step 2**: the chyron must spell the username correctly and the scorebug must look like real broadcast UI. If either looks wrong, re-roll Step 1 (everything downstream pixel-locks to this frame). This is the agent's own check — do not ask the user.

**On failure** (any reason — content policy, billing, etc.): fall back once to `provider: nano-banana-pro` with the same prompt, references, and `aspect_ratio` (drop `quality` and `output_format`). Tell the user you switched and why — don't degrade silently.

## Step 2 — Behind-home-plate cutaway (`generate_reference_video`, kling-v3-omni)

Compose the prompt around the scaffold below. Keep it under 2500 characters (kling's cap) including the substituted name.

**Call params:**

- `provider`: `kling`
- `kling_model`: `kling-v3-omni`
- `duration`: `15`
- `aspect_ratio`: `16:9`
- `quality_mode`: `pro` — 1080p (the broadcast UI grading + chyron text legibility benefit from the extra resolution; std muddies the scorebug)
- `reference_images`: `[<Step 1 still URL>]`
- `image_types`: `["first_frame"]` — locks the still as the opening frame
- `sound`: `true`
- `prompt_adherence`: `strict`
- `negative_prompt`: `"scene cuts, camera angle changes, scorebug animation, chyron pop-in, chyron fade-in, chyron text changes, graphics animating, exaggerated acting, direct address to camera, blurry face, identity drift, distorted anatomy"`

`prompt_adherence: strict` paired with the full `negative_prompt` anchor list are load-bearing — without both, kling animates the scorebug late in the clip and the face drifts.

**Prompt scaffold** (seven required elements):

1. **First-frame anchor (verbatim opener)**: `First frame is the provided reference image. The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked across all 15 seconds. Do NOT animate them, do NOT change their text.`

2. **Cinematic setup**: one continuous take, no cuts, no angle changes; telephoto broadcast camera lands on a notable guest in the crowd between innings; setting is premium field-level seats behind home plate at Yankees vs Red Sox ALCS Game 3 in Boston, Fenway Park; subject stays seated behind home plate the full shot; movement subtle, believable, human; brief glances between the field and camera, no eye-contact lock, no talking to camera, no exaggerated gestures.

3. **Broadcast look**: real live sports broadcast look, telephoto broadcast camera feel, natural ballpark lighting, slight broadcast compression, slight interlacing / TV grain, authentic crowd movement in the background, realistic field-level framing.

4. **Locked graphics block** — use the literal label `On-screen graphics (LOCKED — do NOT animate):` so kling treats them as static:
   - Bottom Yankees vs Red Sox ALCS scorebug, unchanged for the full 15s.
   - Lower-third chyron above the scorebug reading `${username}` (username alone, no suffix), matching the ESPN broadcast UI theme.

5. **Audio spec**: natural live sports-broadcast commentary from two male MLB broadcast announcers talking about him being at the game tonight. Casual, warm, authentic — like real MLB commentators noticing a known guest. Let kling assign voices freely across the 15s — no per-beat speaker prescription. Three sample lines (include all three; `${username}`, `Fenway`, and `Game 3` land verbatim):

   - `"${username} is here tonight at Fenway, taking in this massive playoff matchup."`
   - `"You can see he's enjoying himself here behind home plate for Game 3."`
   - `"Great atmosphere in the building, and ${username} getting a lot of love from the crowd."`

6. **Four synchronized visual beats** (announcers speak over the whole shot — beats describe what the camera sees, not who's talking). Each beat is a labeled block: `BEAT N (X–Ys) — <short label>. Visual: <one sentence>.` Per-beat visuals:

   - **BEAT 1 (0–4s) — camera finds him.** Visual: subject smiling casually in his seat as the camera lands on him; looks around naturally, not paying attention to camera.
   - **BEAT 2 (4–7s) — relaxed natural wave + glance at Jumbotron.** Visual: relaxed natural wave toward the camera (crowd cheers on the first wave); glances up at the Jumbotron above him, then back to camera.
   - **BEAT 3 (7–11s) — brief cheer + exchange with friend on the left.** Visual: subject **cheers briefly with visible excitement, reacting to the playoff atmosphere**, then turns to his friend on the left, exchanges words, laughs. Subject's voice is not audible; announcers speak over the shot.
   - **BEAT 4 (11–15s) — natural clap.** Visual: claps naturally while smiling.

7. **Closing identity reinforcement (verbatim)**: `Preserve identity strongly. Keep him seated behind home plate throughout. Genuine MLB TV broadcast crowd cutaway feel.`

**On failure**: re-run kling — don't switch video engines. Kling is the only model that handles real-person photos for this recipe (Seedance fails on output-side face moderation — see "Engine choice" below). If the rejection points at the still itself, re-run Step 1 with a different photo.

Long calls may return `{ task_id, status }` — poll `task_status` to completion. Client-layer timeouts leave the upstream task orphaned with no recovery handle; re-run from scratch.

## Step 3 — Deliver

Report progress as you go — which step is running, when each call returns. When both calls complete, echo the CDN URLs (still + video) in plaintext; the host environment handles rendering / downloading / opening.

End with a one-line summary: *"Behind-home-plate cutaway for {username} — 15s, 16:9, 1080p, kling-v3-omni, native two-announcer commentary."*

## Load-bearing phrases (keep verbatim)

- `A screenshot from a live MLB game TV broadcast on ESPN.` (Step 1 frame-type opener)
- `The camera cuts to the audience` (Step 1 framing primitive — crowd-cutaway anchor)
- `Camera is positioned in the foul-ground photographers' pit just past home plate, low angle, shooting BACK at the premium seats — the baseball field is BEHIND the camera and NOT visible anywhere in the frame.` (Step 1 camera-position lock — without it, gpt-image-2 sometimes places the camera in the upper deck shooting toward the field, producing a wrong-direction shot)
- `CRITICAL — broadcast graphics that MUST be visible in this image:` (Step 1 overlay-block imperative header)
- `Hardlock: Do not alter their facial structure and maintain their likeness` and `The subject must match the reference person` (Step 1 prompt)
- `First frame is the provided reference image. The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked across all 15 seconds. Do NOT animate them, do NOT change their text.` (Step 2 opener)
- `Preserve identity strongly. Keep him seated behind home plate throughout. Genuine MLB TV broadcast crowd cutaway feel.` (Step 2 closer)
- `On-screen graphics (LOCKED — do NOT animate):` (Step 2 graphics block label)
- The full `negative_prompt` anchor list, comma-separated
- `BEAT N (X–Ys) —` block labels with timestamps
- `prompt_adherence: "strict"` and `image_types: ["first_frame"]` call params

## Engine choice: Kling-only (with one caveat)

Seedance has a two-stage `partner_validation_failed` 422 gate (validated 2026-05-12 across 4 runs on the NBA sibling skill):

- **Input-side** (`body.image_urls`): rejects if the reference contains a recognizable real person.
- **Output-side** (`body.generated_video`): rejects AFTER generation if the produced clip contains recognizable-looking faces — and every broadcast cutaway has a crowd full of faces.

The output-side gate is unavoidable for this trend regardless of subject, so Seedance is functionally unusable here. Kling is the engine that works **for ordinary user photos**.

**Kling caveat — recognizable celebrities are blocked too.** Kling has its own content-moderation gate that fires on celebrity references (validated 2026-05-13: a Michael Jordan reference + "Ke Wang" chyron returned `task_status: failed, task_status_msg: "Failure to pass the risk control system"` at submit-time). This is correct behavior — the trend illusion only works with a non-public-figure reference where the chyron name + face are coherent. If a user supplies a celebrity photo, surface the gate to them and ask for a non-celebrity reference instead.

**Kling trade-offs**: 2500-char `prompt` cap (scaffold above fits comfortably under cap), no `seed` param (re-rolls are non-reproducible — to re-roll just call again).

## Failure cheat sheet

| Symptom | Fix |
|---|---|
| Step 1 fails (any reason — content policy, billing, etc.) | Fall back once to `nano-banana-pro` with the same prompt + references + aspect_ratio; tell the user you switched and why |
| Step 1 returns `400 invalid_image_file` from `openai v1/images/edits` | Reference is a HEIC-derived JPEG with heavy EXIF and/or extreme aspect ratio (e.g. 2316×3088). Re-encode before upload: `convert in.jpg -strip -auto-orient -resize 1536x1536\> out.png`, then upload the cleaned PNG |
| Step 1 returns 502 / proxy timeout | `quality` was set to `high` (>180s). Pass `quality: "medium"` |
| Step 2 fails | Re-run kling — don't switch engines. If the still is the issue, re-run Step 1 with a different photo |
| Kling `task_status: failed` with `task_status_msg: "Failure to pass the risk control system"` | Reference photo is a recognizable celebrity / public figure. Ask for a non-celebrity reference — Kling correctly blocks celebrity-face + fake-event-chyron impersonation patterns |
| Step 2 times out with no task_id | Re-run from scratch — client-side timeouts orphan the upstream task |
| Generated still shows baseball field / grass / infield dirt behind the subject | Camera angle inverted — camera ended up in the upper deck looking toward the field instead of in the photographers' pit looking back at the crowd. Re-roll Step 1; verify the verbatim camera-position phrase (`Camera is positioned in the foul-ground photographers' pit … the baseball field is BEHIND the camera and NOT visible`) is present in the composed prompt |
| Chyron pops in mid-clip (~4–5s flash) | Chyron not baked into the still. Re-run Step 1; verify chyron is visible in the still URL before Step 2 |
| Scorebug or chyron animates / morphs mid-clip | Missing `prompt_adherence: strict` or trimmed `negative_prompt`. Restore both |
| Identity drifts after ~10s | Re-run Step 2 first (often resolves on a fresh roll). If drift persists, re-run Step 1 with a tighter face crop on the still — more facial pixels = stronger lock |
| Seedance `partner_validation_failed` 422 | Tried Seedance instead of Kling. Use Kling only — Seedance's output-side face-moderation gate is unavoidable for this trend (see "Engine choice") |
| Announcer mispronounces the name | Re-run Step 2 only — burned-in audio is single-take; don't try to fix in post |
| Kling `400 prompt: size must be between 0 and 2500` | Tighten connective prose; the seven scaffold elements fit comfortably under cap |

## What not to do

- **Don't sport-swap.** NBA / NFL / soccer variants → fork this skill; don't parameterize this one. Yankees vs Red Sox ALCS Game 3 Fenway is the trend.
- **Don't add suffixes to the chyron** (e.g. " - AI Creator"). Chyron is the username alone — the trend illusion depends on it reading like a real broadcast identifier.
- **Don't run a post-processing layer** (`add_captions`, `generate_music`, `edit_concat`, `edit_text_overlay`, `edit_pip`, any `edit_*`). Kling burns the scorebug + chyron + native commentary directly; anything added afterward breaks the broadcast illusion.
- **Don't expand audio beyond the four beats** — more dialogue forces kling to compress speech.
