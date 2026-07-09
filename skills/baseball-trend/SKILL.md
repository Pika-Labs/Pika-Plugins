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

15-second ESPN-style broadcast cutaway of a user, sitting behind home plate at a fake Yankees vs Red Sox ALCS Game 3 game at Fenway Park, with two announcers naming them on air.

Fixed-recipe skill — the prompts below are calibrated. Substitute the username and keep the marked anchors intact.

## Cost transparency gate

Before any paid MCP call, call `identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the run with this exact message:

> Estimated cost: about 3,000-5,500 credits (~$30-$55) for the GPT-image-2 broadcast still, one or two Kling v3-omni pro 15s renders (includes one Step 2 corrective retry with a changed payload), and post-flight analyze_media QA. This exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. This is the only yes/no gate; after `proceed`, the pipeline runs end-to-end.

## Voice selection note

This skill uses Kling-omni's native broadcast commentary: two male announcers, matching MLB broadcast convention. The `identity_voice` setting is NOT consumed because this fixed recipe does not use agent-side TTS or custom voice IDs.

If the user wants a female-coded announcer or any custom voice, baseball-trend is the wrong skill. Route them to `/pika:podcast` with a baseball framing, which has an agent-side voice path and can honor explicit voice choices.

## Stage 0 — Intake

If invoked with empty args and no usable prior context, print this menu and stop:

> **Who should appear in the fake MLB broadcast cutaway?** Required:
>
> - **Name** — exactly as it should appear in the chyron and announcer dialogue
> - **Reference photo** — one front-facing or 3/4 portrait, local path or HTTPS URL

If only one field is missing, ask only for that field. Otherwise ask the two questions below one at a time.

**1. Username** *(required)* — used both in the broadcast chyron and in the announcers' commentary, e.g. `"Jane Doe"`. Save as `state.username`. This replaces every literal `${username}` in the prompts below.

**2. Reference image** *(required)* — one front-facing 3/4 portrait, good lighting, one face. Resolve to a CDN URL and save as `state.reference_image_url`:

- **`https://…` URL** → use as-is.
- **Local path** → upload the file with `upload_asset`, then use the returned public URL.
- **Claude Desktop, photo pasted inline** → inline pastes don't reach MCP tools yet (Anthropic limitation). Reply with:

  > Heads up — pasted images don't reach MCP tools on Claude Desktop yet. Two options:
  > - **Paste a URL** if it's already hosted somewhere — fastest.
  > - **Attach the image file** so I can upload it before generation.

  When a local file arrives: convert it to a public URL with `upload_asset` and use `public_url`.

After both answers are in, run the Cost transparency gate, then echo one short confirmation ("Generating behind-home-plate cutaway for **{username}**…") and start the pipeline. **No further yes/no gates after the cost gate** — the pipeline runs end-to-end.

### Stage 0.5 — Avatar-type probe for the reference image

Before any paid `generate_image_edit` or `generate_reference_video` call, run this Avatar-type probe on `state.reference_image_url`. The baseball-trend recipe turns the subject into a fake broadcast guest, so IP-derived avatars and celebrity/public-figure references are especially likely to fail moderation.

Call `analyze_media` once:

```
query: "Classify this image for paid video generation. Is it a photograph of a real human face, an AI-generated realistic portrait, a stylized / illustrated character, or a recognizable trademarked / copyrighted character such as Batman, Pikachu, or Mickey Mouse? Return strict JSON only: { \"avatar_type\": \"real_human\" | \"ai_realistic\" | \"stylized_illustrated\" | \"recognized_ip\", \"recognized_character\": string | null, \"moderation_risk\": \"low\" | \"medium\" | \"high\", \"recommendation\": \"proceed\" | \"warn\" | \"reject\" }. Use null for `recognized_character` when no specific character is recognized; never write \"none\", \"unknown\", or explanatory prose in that field."
```

Route from the result:
- **recognized IP / copyright risk** -> **STOP only when** `avatar_type` is `"recognized_ip"`, or `recognized_character` names a specific character (for example `"Batman"`), or when both `moderation_risk` is `"high"` and `recommendation` is `"reject"`. Treat `recognized_character: null`, empty string, `"none"`, `"unknown"`, `"n/a"`, and low/medium `moderation_risk` as not enough to stop by themselves. Run this check before the real/stylized routes. A chibi Batman is still Batman even when `avatar_type` is stylized / illustrated.
- **real human / AI-generated realistic** -> proceed normally.
- **stylized / illustrated** -> proceed with a visible warning that stylized avatars can reduce likeness quality and may be blocked by image/video moderation.
- **trademarked / copyrighted** -> **STOP** before generation. Surface this message: `Your identity avatar appears to be a trademarked character ([X]). Most video providers will moderate this and refuse to generate. Pass --avatar <real-looking-photo-url> to override, or update your identity avatar at pika.me first.` For this skill, ask for a replacement reference photo URL or path if the user did not pass an `--avatar <real-looking-photo-url>` style override.

## Pipeline

Two Pika MCP stages, sequential. Primary engines are locked: `gpt-image-2` for the still, `kling-v3-omni` for the video. The only still-stage fallback is the documented `seedream` pass below when OpenAI declines the broadcast still with `moderation_blocked`.

## Long-running task_status polling

When any long-running generation call returns a `task_id` with or without an initial status, including `{task_id}`, `{task_id, status: "queued"}`, or an initial `queued`, `running`, or `processing` status, record the task id and start time immediately.

- Call `task_status({task_id})` in a tight loop until terminal (`completed | failed | cancelled`). No manual sleep and no Bash polling; the worker holds each status call open.
- Emit ONE visible progress line every 60s while status is `queued`, `running`, or `processing`: `Seedance i2v queued for {N}m {S}s... still processing`. Replace the provider/stage label when polling GPT-image-2 or Kling tasks.
- On `completed`, unwrap the returned result URL and continue.
- On `failed` or `cancelled`, surface failure to the user with `task_id`, status, and the last status message.
- After 15 min total from the original submit, call `task_cancel({task_id})` if the task is still non-terminal, then surface failure to the user. If cancel reports the task is already terminal, call status once more and report that terminal result.
- Do not submit a duplicate request while the original task is still `queued`, `running`, or `processing`.

### Step 1 — Broadcast still (`generate_image_edit`)

The chyron + scorebug get baked into the still at frame 0 (load-bearing — when Kling is asked to "pop in" the chyron mid-clip it appears at second 4–5 with a visible flash and breaks the trend; baking it into the first frame makes Kling treat it as pixel-locked burned-in UI).

Call `generate_image_edit` with:

- `provider`: `gpt-image-2`
- `images`: `[state.reference_image_url]`
- `aspect_ratio`: `16:9`
- `quality`: `medium` (default for speed; `high` is now exposed but ~2 min/call — use only when fidelity matters)
- `output_format`: `png`
- `prompt` (verbatim, `${username}` substituted):

```
A screenshot from a live MLB game TV broadcast on ESPN. The camera cuts to the audience — our reference image person, sitting smiling in premium field-level seats behind home plate at Fenway Park, smiling naturally and unaware they're on camera. Hardlock: Do not alter their facial structure and maintain their likeness. The subject must match the reference person.

The image looks exactly like a real TV screenshot — broadcast color grading, slight compression artifacts, interlacing grain, telephoto broadcast camera feel. It's the New York Yankees vs Boston Red Sox, MLB American League Championship Series (ALCS), Game 3, Boston home stadium (Fenway Park). Yankees lead 2-0 in the ALCS so far.

CRITICAL — broadcast graphics that MUST be visible in this image:
1. A real ESPN-style bottom scorebug for MLB, showing Yankees vs Red Sox with team logos, inning, outs, balls/strikes count, and score (with a small runners-on-base diamond), looking like a real live broadcast scorebug.
2. Directly above the scorebug, a clean broadcast-style lower-third name graphic / chyron that reads exactly: "${username}" — set in a classic ESPN sans-serif, in the network's color treatment. The chyron sits in the lower-left area, above the scorebug, like a real broadcast identifier for the on-camera guest.
3. The ESPN network logo watermark in a corner.

All three graphics must look like real burned-in broadcast UI — not Photoshop overlays. 16:9 aspect ratio.
```

Save the returned URL as `state.broadcast_still_url`.

Retry budget: Step 1 still generation gets at most 3 total attempts, including the primary still, self-check re-rolls, invalid-image retries, `quality` downgrades, and the one-shot `seedream` fallback below. Track `state.step1_attempt_count` before every paid still call.

**OpenAI moderation fallback**: if the Step 1 `gpt-image-2` call returns `moderation_blocked`, treat it as a known policy surface for "real person + ESPN-branded live feed + real MLB team context." Do not keep re-rolling the same OpenAI call. Try `seedream` once with the same `images`, `aspect_ratio`, and prompt text, omitting `quality` and `output_format` because those are `gpt-image-2`-only fields.

- If `seedream` succeeds, save that URL as `state.broadcast_still_url`, set `state.broadcast_still_provider = "seedream_fallback"`, and continue to the self-check below. The fallback is one-shot: do not call `gpt-image-2` again and do not call `seedream` a second time in this run.
- If `seedream` also fails or returns a policy/safety block, stop and surface this exact user-facing message:

  > OpenAI declined this image. Try using a fresh AI-generated headshot instead of a personal photo, or pick a non-MLB sport variant.

**Agent-side self-check before Step 2**: the chyron must spell the username correctly and the scorebug must look like real broadcast UI. If either looks wrong after the primary `gpt-image-2` still, re-roll Step 1 once per failed self-check while the Step 1 cap has attempts remaining (everything downstream pixel-locks to this frame). If either looks wrong after `state.broadcast_still_provider = "seedream_fallback"`, do not re-roll Step 1; stop and ask the user for a fresh AI-generated headshot or a non-MLB sport variant using the same message above. This is the agent's own check — do not ask the user unless the one-shot fallback path has already failed QA. After either cap is exhausted, stop and ask for a better reference photo or permission to deliver the best attempt; include the best still/video URL and the failing check.

### Step 2 — 15s broadcast video (`generate_reference_video`)

`image_types: ["first_frame"]` locks `state.broadcast_still_url` as Kling's literal frame 0, keeping the chyron + scorebug pixel-static for the full 15s.

Call `generate_reference_video` with:

- `provider`: `kling`
- `kling_model`: `kling-v3-omni`
- `duration`: `15`
- `aspect_ratio`: `16:9`
- `quality_mode`: `pro`
- `reference_images`: `[state.broadcast_still_url]`
- `image_types`: `["first_frame"]`
- `sound`: `true`
- `prompt_adherence`: `strict` *(load-bearing — without it the scorebug animates and identity drifts late in the clip)*
- `negative_prompt` *(verbatim, load-bearing — without these entries Kling occasionally morphs the scorebug or fades the chyron)*:

```
scene cuts, camera angle changes, scorebug animation, chyron pop-in, chyron fade-in, chyron text changes, graphics animating, exaggerated acting, direct address to camera, blurry face, identity drift, distorted anatomy
single announcer, one announcer only, single narrator, announcer monologue
```

- `prompt` (verbatim, `${username}` substituted everywhere; pre-trimmed to fit Kling's 2500-char cap; chyron-on-frame-0 lock at top):

```
First frame is the provided reference image. The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked across all 15 seconds. Do NOT animate them, do NOT change their text.

Realistic live MLB broadcast cutaway of the subject in premium field-level seats behind home plate at Yankees vs Red Sox ALCS Game 3 at Fenway Park. It feels like the broadcast camera found a notable guest between innings.

The subject stays seated, smiling naturally, not over-performing, not locked into eye contact. Occasionally glances toward the field, then camera, then back to the field. One continuous take. No cuts. No angle changes.

Action timeline:
0-4s: smiling casually in his seat as the camera lands on him; looks around naturally, not paying attention to camera.
4-7s: relaxed natural wave toward the camera (crowd cheers when he waves the first time); glances up at the Jumbotron above him then back to camera.
7-11s: cheers briefly with visible excitement, reacting to the playoff atmosphere; turns to his friend on the left, exchanges words, laughs (we don't hear him speak).
11-15s: claps naturally while smiling.

Keep all movement subtle, believable, human. No exaggerated acting. No direct talking to camera.

Broadcast styling: live sports TV look, telephoto broadcast camera, natural ballpark lighting, slight compression / interlacing grain, authentic crowd movement, realistic field-level framing.

Audio: two distinct male voices, not a single narrator. Announcer A is play-by-play; Announcer B is the color commentator. Alternate A/B lines with natural broadcast handoffs so both voices are clearly heard:
Announcer A: "${username} is here tonight at Fenway, taking in this massive playoff matchup."
Announcer B: "You can see he's enjoying himself behind home plate for Game 3."
Announcer A: "Great atmosphere in the building tonight."
Announcer B: "And ${username} is getting a lot of love from the crowd."
The announcers are OFF-SCREEN; the subject does not lip-sync or talk to camera.

Constraints: Preserve identity strongly. Keep him seated behind home plate throughout. No constant eye contact with camera. No talking to camera. No exaggerated gestures. No scene cuts. Scorebug + chyron do not change at any point. Genuine MLB TV broadcast crowd cutaway feel.
```

Save the returned video URL as `state.broadcast_video_url`. If generation completes asynchronously, follow the MCP tool's returned status handle until the video reaches a terminal state.

Step 2 Kling video generation gets at most 2 total attempts (initial render + one corrective retry for drift, scorebug/chyron movement, or announcer mispronunciation). kling-v3-omni has no seed, and identical Kling payloads can resolve to the same job/asset. Do not submit an identical Kling payload just to seek variation. Before the corrective retry, materially change the payload by using an updated `state.broadcast_still_url`, restoring missing strict params / negative_prompt entries, or shortening / clarifying the A/B announcer block. Track `state.step2_attempt_count`. After either cap is exhausted, stop and ask for a better reference photo or permission to deliver the best attempt; include the best still/video URL and the failing check.

### Step 3 — Deliver

Return both Pika CDN URLs: the still image URL and the final video URL. If the host client requires local media markers, create the local preview outside this skill after confirming both CDN URLs are reachable.

One-line summary: *"Behind-home-plate cutaway for {username} — 15s, 16:9, 1080p, Kling v3-omni, native two-announcer commentary."*

## Post-flight quality gate

Before declaring success, call `analyze_media` on `state.broadcast_video_url` and ask for a structured verdict:

```
Return JSON only: {
  "verdict": "clean" | "degraded" | "catastrophic",
  "announcer_count": 0 | 1 | 2,
  "observations": string[],
  "audio_warning": string | null,
  "quality_warning": string | null,
  "re_roll_suggestion": string | null
}
Check that the chyron still reads the exact username, the subject's identity stays stable throughout, the scorebug remains stable, the final clip has no black frames or wrong-sport shots, and the audio contains two distinct male announcer voices — not just one narrator.
```

- If `announcer_count < 2`, treat the result as at least `degraded`, include `audio_warning`, and use the one Step 2 corrective retry only after changing the A/B audio payload. Do not submit an identical Kling payload.
- If `verdict` is `clean`, return the still URL and final video URL normally.
- If `verdict` is `degraded`, return the URLs plus the `quality_warning` and `audio_warning` so the user can review before publishing.
- If `verdict` is `catastrophic`, do not call the run complete; surface the verdict and `re_roll_suggestion` instead of declaring success.

## Load-bearing phrases (don't strip these)

These are empirical behavior dependencies, not writing style — removing them breaks the recipe:

- In the **still prompt**: `Hardlock: Do not alter their facial structure and maintain their likeness` + `The subject must match the reference person` (without these, identity drifts on the first frame, and everything downstream inherits the drift).
- In the **video prompt**: `Preserve identity strongly` + `The ESPN scorebug AND the "${username}" lower-third chyron are ALREADY on screen at frame 0 — keep them visible, unchanged, pixel-locked` (without these, Kling re-animates the chyron mid-clip).
- The full **negative_prompt** list — every entry there came from a specific failure mode in prior runs.
- `prompt_adherence: "strict"` and `image_types: ["first_frame"]` — see inline notes above.

## Engine choice: Kling-only (with one caveat)

Seedance has a two-stage `partner_validation_failed` 422 gate observed across repeated NBA-sibling runs:

- **Input-side** (`body.image_urls`): rejects if the reference contains a recognizable real person.
- **Output-side** (`body.generated_video`): rejects AFTER generation if the produced clip contains recognizable-looking faces — and every broadcast cutaway has a crowd full of faces.

The output-side gate is unavoidable for this trend regardless of subject, so Seedance is functionally unusable here. Kling is the engine that works **for ordinary user photos**.

**Kling caveat — recognizable celebrities are blocked too.** Kling has its own content-moderation gate that fires on celebrity references. A celebrity-reference prompt plus matching broadcast chyron can fail at submit-time with `task_status: failed, task_status_msg: "Failure to pass the risk control system"`. This is correct behavior — the trend illusion only works with a non-public-figure reference where the chyron name + face are coherent. If a user supplies a celebrity photo, surface the gate to them and ask for a non-celebrity reference instead.

**Kling trade-offs**: 2500-char `prompt` cap (recipe above is pre-trimmed). kling-v3-omni has no seed; identical Kling payloads can collapse to the same job/asset, so a corrective retry must materially change the first-frame still, prompt, negative_prompt, or audio wording. Do not submit an identical Kling payload for variation.

## Runtime expectations

Typical run time is 4-7 minutes:

| Step | Wall clock | Notes |
|---|---:|---|
| Reference upload | 5-30s | Skip when the user supplies HTTPS |
| Broadcast still | 60-120s | Re-roll before video if the chyron or scorebug is wrong, capped by the Step 1 retry budget |
| Kling video | 3-5 min | One 15s pro render with native commentary |
| Delivery check | <30s | Verify final URL and obvious identity/chyron continuity |

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Chyron pops in mid-clip (~4–5s flash) | Chyron not baked into the still | Re-run Step 1 within the Step 1 retry budget; verify chyron is visible in `state.broadcast_still_url` before Step 2 |
| Scorebug animates / morphs mid-clip | `prompt_adherence` not `strict`, or `negative_prompt` was trimmed | Restore strict adherence and the full negative_prompt |
| Identity drift late in the clip (face changes after ~10s) | Reference image too small / Kling losing the face | Use the one Step 2 corrective retry only after materially changing the payload, usually by re-running Step 1 with a tighter face crop on the still if Step 1 budget remains |
| Only one announcer voice is heard | Kling collapsed the A/B commentary into one native narrator | Shorten or clarify the A/B announcer lines before the one Step 2 corrective retry; after the cap is exhausted, surface the audio warning and ask whether to deliver the best attempt |
| Username mispronounced by announcers | Native audio is one take | Add a pronunciation hint or shorten the announcer line before the one Step 2 corrective retry; otherwise surface the audio warning |
| OpenAI `moderation_blocked` on Step 1 | `gpt-image-2` safety gate on real person + ESPN-branded live feed + real MLB team context | Try `seedream` once with the same reference image and prompt while Step 1 budget remains. If it also blocks, tell the user: "OpenAI declined this image. Try using a fresh AI-generated headshot instead of a personal photo, or pick a non-MLB sport variant." |
| Seedance `partner_validation_failed` 422 | Tried Seedance instead of Kling | Use Kling only — see engine-choice section above |
| Kling `task_status: failed` with `task_status_msg: "Failure to pass the risk control system"` | Reference photo is a recognizable celebrity / public figure | Ask the user for a non-celebrity reference. Kling correctly blocks impersonation patterns (celebrity face + fake-event chyron) |
| `generate_image_edit` 400 `invalid_image_file` from `openai v1/images/edits` | Reference is an iPhone HEIC-derived JPEG with heavy EXIF and/or extreme aspect ratio (e.g. 2316×3088) | Re-encode the reference before upload: `convert in.jpg -strip -auto-orient -resize 1536x1536\> out.png`, then upload the cleaned PNG |
| `quality: "high"` runs feel slow (~2 min/call) | gpt-image-2 high is a deliberately slower fidelity tier, not a bug — upstream typical is around two minutes per the manifest | Wait it out — most runs return cleanly. If a specific run does fail, retry once within the Step 1 retry budget; fall back to `quality: "medium"` only if it persists |

## What NOT to do

- Don't sport-swap. NBA / NFL / soccer variants → fork this skill; don't parameterize this one.
- Don't add suffixes to the chyron (e.g. " - AI Creator"). Chyron is the username alone — the trend illusion depends on it reading like a real broadcast identifier.
- Don't add post-edits — no `add_captions`, `generate_music`, `edit_*`. Kling burns the scorebug + chyron + native commentary directly; anything added afterward breaks the broadcast illusion.
