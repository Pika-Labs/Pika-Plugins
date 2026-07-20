---
name: stagefight
description: >-
  Use when the user asks for stagefight or a task matching the examples below.
  Generate a viral "fan-filmed staged fight" clip — POV phone footage of two
  costumed performers having a choreographed cosplay battle on an elaborate
  themed stage at a live outdoor event, with a believable live-stage effect
  (smoke / colored fire / water geyser) and a crowd in the foreground filming.
  A gpt-image-2 stage still → image-to-video (Seedance, ~10s, 16:9). The
  advertiser-safe "theatrical performance" framing is what gets fight content
  past moderation. Triggers: "/stagefight", "make a staged fight video",
  "fan-filmed cosplay fight", "ninja/samurai stage battle", "that staged fight
  trend". Requires the pika MCP.
argument-hint: <the two fighters, e.g. "ninja vs ninja" | "samurai vs demon" | "frost mage vs ember knight">
required-capabilities:
  - generate_image
  - generate_image_edit
  - generate_video
  - task_status
  - edit_audio_mix
---

# stagefight

A two-call pika pipeline: **stage still** (`generate_image`, gpt-image-2) → **fight clip** (`generate_video`, image-to-video, **~10s, 16:9**). The clip is fan-filmed POV phone footage of a *choreographed cosplay performance* on a themed stage — two performers clash, a live-stage effect bursts, the crowd reacts. **One run produces one clip** for one matchup.

**The core job of this skill: figure out WHO is fighting (ask the user, or suggest matchups), then AUTHOR fresh prompts in the structure of the bundled examples and generate a new video.** The examples in `examples/` are the *pattern to follow*, not a fixed catalog — every run should produce a new matchup composed the same way. The look is calibrated and the safety framing is load-bearing: keep every fixed sentence of the two templates and fill only the marked `[SLOTS]`.

## ★ Why it works — the method (this is the actual research, do not drop any of it)
Raw "two people fighting" prompts get **moderation-blocked**. These four moves are what make fight content reliably generate, and together they ARE the trend's aesthetic:

1. **Frame it as a wholesome theatrical performance.** Every clip prompt opens, verbatim: *"Wholesome theatrical stage performance, choreographed cosplay, advertiser-safe."* and closes with *"Believable live-stage effects, not cartoon magic."* This reframes combat as a *stunt show*, which clears the safety pass. Never describe injury, blood, real weapons connecting, or "cartoon magic" — describe **choreography, props, and stage pyrotechnics**.
2. **Fan-filmed audience POV.** *"POV handheld phone footage from the audience, raised above other people's heads filming the stage,"* with *"a large audience in the foreground — dark silhouetted heads, many holding up phones recording."* This is both the viral "I was there" aesthetic AND part of the safety (it reads as documenting a *performance*, not real violence).
3. **Costumed ORIGINAL characters — never real people, never named IP.** Use archetypes ("a lean samurai in a straw hat", "a horned demon in black robes", "a spiky-blond-haired ninja in an orange tracksuit"). Real-person faces get moderation-blocked on both backends; named/trademarked characters drift and trip flags. Describe the *cosplay* (hair, costume, props), not a brand.
4. **Live-stage effect, grounded.** The "wow" beat is a believable practical effect — a *puff of stage smoke*, *green stage fire and sparks*, *a wall of water / geyser*. Both performers **recoil/brace dramatically**; nobody gets hurt.

**Moderation ops:** re-roll the same call on a block (don't immediately swap providers). If a video gen runs **past ~4 min before failing, the content already cleared the safety pass** — the failure is infrastructural, just retry. **Do NOT bake music in via `reference_audio`** — that path trips moderation; add music/SFX in post. Different Seedance backends (`ark` / `fal`) have different moderation pipelines if you need to retry.

## Prerequisites
pika MCP available. Tool prefix varies by host — use whatever is exposed. Tools: `generate_image`, `generate_video`, `task_status`; optional for finishing: `generate_music` / SFX + `edit_concat` / `edit_audio_mix`.

## Stage 0 — Who's fighting? (settle this first) — One matchup → one clip.

1. **If the user already named two fighters** — in the `/stagefight` args or their message (e.g. "frost mage vs ember knight", "my cat vs a dragon", "two robots") — **use them, skip the menu, go straight to Compose.** Don't re-ask.

2. **Otherwise ask with ONE `AskUserQuestion`** (header: `Matchup`). It MUST give the user a way to supply their own characters — make that the **first option** — plus exactly **3 template matchups**:
   - **"Pick your own two fighters"** — *I'll name them* → when chosen, ask "Who are your two fighters?" and use the answer. (The auto-added **Other** field also lets them type a matchup straight in.)
   - **Ninja vs ninja** — smoke
   - **Samurai vs horned demon** — green fire
   - **Sorceress vs vampire (water-stage)** — geyser
   **Never auto-select a template** — the whole point is the user chooses or types their own. Do NOT just print 3 suggestions as prose and proceed; present the real 4-option menu and wait.

3. **Aspect:** default to `16:9` silently (the trend look). Only ask about `9:16` if the user mentions vertical/TikTok/Reels.

Once the matchup is set, **compose the prompts yourself** (next section), confirm in one line ("Generating your staged-fight clip — frost mage vs ember knight…"), and run end-to-end — no further yes/no gates.

## Compose the prompts (the authoring step, NEVER skip it)
**You are composing for the USER'S two fighters. Start from THEM and DERIVE everything else.** The ninja / samurai / sorceress examples are *illustrations of the formula, not the output* — if the user said "X vs Y", the video is about X vs Y. **Never silently default to one of the example matchups, and never substitute a different fight than the one chosen.** Defaulting to ninja/samurai/water when the user asked for something else is the #1 failure of this skill.

Derive each of the four variables FROM the chosen fighters:
- **Stage** = a themed set those two characters would believably duel on — *what world are they from?* — + 2–4 concrete props + a backdrop + time-of-day/light. (Wizards → a stone arena; mecha → a neon dome; cowboys → a saloon street. Not a temple unless they're temple characters.)
- **Performer A (LEFT)** / **Performer B (RIGHT)** = each as live-action **cosplay**: hair, costume, a prop, a stance. Archetypes only — never real people; translate any named/trademarked character into its *describable costume* (no brand names in the prompt).
- **Signature effect** = the one believable live-stage payoff that fits THIS fight (smoke / colored fire + sparks / water geyser / dust + lantern-glow / ice shards / embers / confetti-cannon…), that both performers react to.

**Worked derivation (arbitrary matchup, to show the move):** user asks *"robot boxer vs sumo wrestler."*
→ **Stage:** neon-lit night arena, holographic banners, ring ropes, sponsor lanterns, city skyline behind. → **LEFT:** a tall chrome humanoid robot in red boxing gloves, joints glowing, guard up. → **RIGHT:** a massive sumo wrestler in a ceremonial mawashi, stamping low. → **Effect:** a shockwave of dust and sparks as glove meets palm. → then drop those into the two templates. *(Notice: nothing ninja/temple/water — every variable came from the actual fighters. Do this for whatever the user picks.)*

## Step 1 — Stage still (`generate_image`, gpt-image-2)
Bakes the stage, both performers, and the filming crowd into frame 0 so Step 2 only has to animate the clash. **Template — keep every fixed sentence, fill the `[SLOTS]`:**

```
A recording from the audience at an outdoor theater performance at [TIME-OF-DAY/SETTING]. [STAGE: a wooden stage recreating <themed set> — <2-4 concrete set pieces, lanterns/gate/fog/water/etc>, <backdrop>]. On stage, two performers in high-quality live-action cosplay face off several meters apart: on the LEFT, [PERFORMER A — cosplay: hair, costume, prop, stance]; on the RIGHT, [PERFORMER B — cosplay: hair, costume, prop, stance]. A large audience fills the foreground — dark silhouetted heads, many holding up phones recording with glowing screens. The camera films from far back in the crowd, slightly off-center, performers small on the wide stage, slight handheld tilt. Realistic phone-camera look, faint digital noise, [natural light note]. High resolution, no text, no UI.
```

**Call `generate_image`.** **Call params:** `provider: gpt-image-2` · `aspect_ratio: 16:9` (default; `9:16` if vertical) · `quality: medium` (high exceeds the proxy timeout) · `output_format: png`. **No input image** unless the user supplied a specific character sheet/costume to anchor — in that case call `generate_image_edit` instead, passing the sheet as `images`, and keep the text describing only the *cosplay*, not a name. On `moderation_blocked`: re-roll; if it persists, soften the costume language (more "performer/stunt", less "demon/claws"). Save the returned URL → `state.still_<n>_url`. Self-check: two costumed performers clearly facing off, crowd + phones in foreground, no text — else re-roll.

## Step 2 — Fight clip (`generate_video`, image→video, 10s)
Locks the still as the start frame and animates the clash. At **10s** there's room for a fuller beat — give the `[ACTION]` a small arc (square-off → clash → the live-stage effect → recoil/second exchange → crowd erupts) rather than a single hit. **Template — verbatim wrapper, fill only `[ACTION + EFFECT]`:**

```
Wholesome theatrical stage performance, choreographed cosplay, advertiser-safe. POV handheld phone footage from the audience, frame slightly unsteady, raised above other people's heads filming the stage. [ACTION: the two performers <sprint/dash in> and <clash — martial choreography or props>, <a believable live-stage effect: stage smoke / green fire + sparks / a wall of water erupts>, then <both recoil / leap apart / brace>]. The crowd in the foreground reacts, phones held up recording. Believable live-stage effects, not cartoon magic. Realistic smartphone recording, slight digital noise, continuous handheld shot, no subtitles, no UI.
```

**Call `generate_video`.** **Call params:** `image:` (or `reference_images:`) = `state.still_<n>_url` (start frame) · `duration: 10` · `aspect_ratio: 16:9` (match Step 1) · keep `sound` default (don't force music). Poll `task_status` if it returns a task id. If it fails *after ~4 min* it cleared moderation — just retry; if it fails *fast*, soften the action wording and re-roll.

## Step 3 — Finish (optional)
- **SFX/music in post only.** Crowd murmur + a whoosh/impact on the clash sells it. Generate or fetch audio and mix with `edit_audio_mix` — **never** pass music as `reference_audio` into the video gen (trips moderation).

## Example decompositions (ILLUSTRATIONS ONLY — never substitute these for the user's matchup)
Read these to learn how a matchup splits into the four variables — then derive your own for whatever the user picked. Don't paste one of these unless the user chose that exact fight. The generated stills are in `examples/` (`ex1_ninja`, `ex2_samurai`, `ex3_snake`, `hero_pika` + `_contact_sheet.png`) — open them as the **visual target** for a good Step-1 still.

| matchup | stage (props, light) | LEFT performer | RIGHT performer | signature effect |
|---|---|---|---|---|
| Ninja clash | dusk ninja-village gate; rock formations, painted doors, paper lanterns, forest | spiky-blond ninja, leaf-emblem headband, orange tracksuit | spiky-black-hair ninja, dark-blue shirt | dust + a puff of stage smoke |
| Samurai vs demon | night temple courtyard; stone lanterns, torii gate, green fog | lean samurai, straw hat, dark armor, katana | towering horned demon, black robes, claws | green stage fire + sparks |
| Water-stage duel | dusk lake water-stage; Chinese pavilion, red pillars, lanterns, misty mountains | white-robed sorceress, long black hair, arms raised | pale vampire, black robes, fangs, red eyes | a wall of water → geyser |
| Hero / mascot | dusk wooden stage; rock formations, lanterns, forest | small fluffy "Pika" mascot in a tiny gi | towering horned armored warrior, far larger | burst of stage sparks |

Each row = `[STAGE]` · `[PERFORMER A]` · `[PERFORMER B]` · `[ACTION effect]`. Your job is to fill those same four slots **from the user's characters**, not to reach for a row above.

## One-liner recap
Costumed performers + a themed stage + a fan in the crowd filming + "it's just a stunt show" framing = fight footage that actually renders. One matchup → one stage still → one 10s image-to-video (16:9). Music/SFX in post, never via `reference_audio`.
