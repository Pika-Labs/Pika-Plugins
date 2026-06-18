---
name: viral-hook
description: >-
  Prepend a 4s viral hook + optional designed title to a user's video, then hard-cut into
  the real clip. An attention-grabbing event erupts into the user's OWN scene; the title is
  rendered in-scene by Seedance. One MCP call does the whole render. Requires Pika MCP.
  Triggers: "add a viral hook", "disruption hook on my video", "hook + title on my clip",
  "viral hook with typography", "scroll-stopper intro".
argument-hint: "[video path or URL] [optional title line]"
required-capabilities:
  - mcp__plugin_pika_pika__upload_asset
  - mcp__plugin_pika_pika__analyze_media
  - mcp__plugin_pika_pika__generate_viral_hook
  - mcp__plugin_pika_pika__task_status
---

# Viral Hook

Prepends an extreme, no-dialogue ~4s hook to a user's video — an attention-grabbing event
that erupts into the user's own scene, with an optional designed title burned into the
lower third — then hard-cuts into the untouched clip.

`mcp__plugin_pika_pika__generate_viral_hook` does the whole render in one call and returns BOTH
the hook and the stitched final. This skill's job is the creative judgment the tool can't
make: read the scene, pick a hook action from the menu, and write a title.

## Hook rules (govern what you WRITE as `hook_action`)

1. **Certain to grab attention, fast.** Extreme and unmissable inside ~2s — over plausibility
   or relevance to the video's topic.
2. **Erupts into the user's OWN scene.** Same person, location, lighting — the tool anchors
   on the best visual anchor frame: 0s when usable, otherwise the first detectable face frame.
   Describe the event entering THAT space, never a different setting.
3. **Use the scene's real geometry.** Enter through a doorway with depth, a wall behind the
   subject, headroom above.
4. **No dialogue.** Voice-free (only ambient / impact SFX) — don't write spoken lines into
   `hook_action`.

## Hook super-category menu

Four super-categories. **Rotate** super-category per run on the same clip/session — without
rotation, regenerates collapse to vehicle / explosion / creature. Archetypes are starting
points, not a closed list; invent freely within the category.

### A. Destructive intrusion — external force violently enters and damages the scene

| Archetype | What happens | Scene affordance |
|---|---|---|
| Incoming vehicle | car / truck / bus smashes through a wall or doorway and barrels at camera | background depth or a back wall |
| Flash flood / wave | a wall bursts and water surges down toward camera | corridor / back wall |
| Structural collapse | ceiling / wall / shelf caves in, debris rains down | headroom / walls |
| Explosion / blast | fireball erupts behind them, shockwave + debris rush forward | a background surface |
| Creature attack | animal / monster lunges from off-frame or bursts in | open off-frame edge |
| Absurd intruder | dinosaur, elephant, UFO, giant hand enters behind them | background space |
| Natural disaster | tornado / meteor / lightning / sinkhole | exterior or large space |

### B. Physics anomaly — laws of physics break, photoreal; scene + subject stay, motion goes wrong

| Archetype | What happens | Scene affordance |
|---|---|---|
| Gravity flips upward | subject, loose objects, and dust fall UP toward the ceiling | any indoor scene |
| Time freeze around subject | every other object holds mid-air while the subject keeps moving | scene with loose / moving objects |
| Magnetic pull from ceiling | hair, clothing, jewelry, small objects yank upward as if a ceiling magnet fired | indoor scene + loose props |
| Room rotates 90° | walls + floor rotate around the upright subject until "down" is now a wall | enclosed space, visible walls + floor |
| Object orbit | all small loose objects lift off and orbit the subject like a tornado | scene with props on surfaces |
| Inverted color flash | the scene briefly inverts to negative colors and back, like a glitch | any scene |

### C. Content-supersized — an element FROM the clip appears building-sized and crashes in

Pull the element from the scene reading (Step 2) — hero product, pet, drink, phone, logo.

| Archetype | What happens | Source element |
|---|---|---|
| Giant hero product | the product being shown appears at 10× scale and smashes through the wall / ceiling | the product in the clip |
| Building-scale pet | the subject's pet appears at building height in the window / doorway | a pet in the clip |
| Giant drink | the cup / can / bottle becomes building-sized and tips over the room | a drink in the clip |
| Giant phone | the subject's phone scales up to fill the back wall, screen glowing | a phone in the clip |
| Giant logo | a brand mark on a wall / shirt / packaging grows to cover the back wall | any logo in the clip |

### D. Content-projectile — a relevant object FROM the clip flies at the subject at speed

Source from the scene reading.

| Archetype | What happens | Source element |
|---|---|---|
| Hero-object slam | the product they're showing flies at high speed into their face | the hero product |
| Food / drink splash | their food or drink hurtles into them, splattering everywhere | food or drink in the clip |
| Swarm pelt | many copies of a small object (sneakers / pills / cans) pelt them like hail | a small repeating object |
| Prop whip | an object on a surface (mug, lamp, book) whips off and slams into them | any heavy prop visible |

## Title rules (when the user wants one)

- **≤7 words, ALL CAPS, one punchy line.** Tie it to BOTH the hook action AND the clip's
  actual content. Example: giant-sneaker projectile + sneaker unboxing → "THIS DROP HITS DIFFERENT."
- Optional — omit for a title-free hook.
- **Typography** defaults to bold distressed display type with a thick black outline. The user
  may override via `type_style` (a free-form style string) or by pasting a `brand.md` — extract
  ONLY the typography directives (fonts, weights, treatments), ignore logos / palette / voice.
  Warn that thin / un-outlined styles may wobble over the 4s.

## Workflow

### Step 0 — Intake (empty args)

If no video was provided, print this menu verbatim and STOP — do not call any tool:

> **What would you like a viral hook on?** Paste any of:
> - **A local video path** — e.g. `/Users/me/Desktop/clip.mp4`
> - **An https URL** to an mp4
> - **A path + a title** — e.g. `clip.mp4 — "YOUR PROMPTS WON'T SAVE YOU"`
> - **A path + "surprise me"** — agent picks the hook action and title

Wait for the next message. Don't guess an input.

### Step 1 — Get a URL

If the input is a local file, `mcp__plugin_pika_pika__upload_asset` it and use the returned
`public_url`. If it's already an https URL, use it directly. Any format is fine — no
transcoding or probing here.

### Step 2 — Read the scene

`mcp__plugin_pika_pika__analyze_media(video_url)` → capture the subject + framing, indoor/outdoor + setting,
lighting, photoreal vs stylized aesthetic, and the spirit/topic. Also note the **hero
objects** (product, pet, drink, phone, logos), including whether each one is visible near the
opening or only appears later — required for super-categories C and D. This reading is passed
verbatim as the `scene` parameter.

### Step 3 — Pick the hook action

Rotate super-category vs the previous run on this clip; pick a different one if possible.
Choose the strongest archetype the scene's geometry supports (A/B) or the most prominent hero
object (C/D). Write the specific hook action — entry vector + motion + scale + peak — as one
vivid sentence. This is `hook_action`. For C/D, name the exact hero object so the tool ties
it to the clip. If the hero object appears later in the clip rather than near the opening,
make the first hook frame explicit: "from the first frame, the subject is holding/using
[hero object]".

### Step 4 — Title + style

Ask whether the user wants a title. If yes, propose a ≤7-word ALL-CAPS line tying the hook
action to the topic, get approval, and offer typography choices before rendering: default,
custom direction, or `brand.md`. If the user has no preference, use default and say so. If no
title is wanted, skip — the hook renders title-free.

### Step 5 — Render

Call `mcp__plugin_pika_pika__generate_viral_hook({ video_url, scene, hook_action, title?, type_style? })`.
If it returns `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status(task_id)` in a tight
loop until terminal, then read the result. On `failed`, surface the error — don't retry blindly.

### Step 6 — Deliver

Present both clips:
- hook only: `[[video:<hook_url>]]`
- final stitched: `[[video:<final_url>]]`

## What NOT to do

- **Don't re-implement the render in the skill.** No extract_frame / generate_image /
  edit_concat / transcode here — `generate_viral_hook` owns all of it. If the hook looks
  wrong, change the `hook_action` / `title` text, not the pipeline.
- **Don't pass a seed.** Variations should come from `hook_action`, `title`, or `type_style`.
- **Don't bake a title onto the real video.** The title belongs only on the hook.
- **Don't auto-edit an approved title.** If a rephrase is needed, ask.
